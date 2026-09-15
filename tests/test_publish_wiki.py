"""Unit tests for scripts/publish_wiki.py, the wiki publication helpers.

The mapping, sidebar, and release-page helpers are pure and asserted directly.
The end-to-end tests publish into a throwaway bare git repository to prove the
replace-stale-pages behaviour, the release gating, and the no-op path of main().
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "publish_wiki.py"
SPEC = importlib.util.spec_from_file_location("publish_wiki", MODULE_PATH)
assert SPEC is not None
publish_wiki = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(publish_wiki)


def _write_docs(root: Path) -> Path:
    docs = root / "docs"
    docs.mkdir()
    (docs / "README.md").write_text("# Home\n", encoding="utf-8")
    (docs / "01a-prereqs-entra-admin.md").write_text("# 01a\n", encoding="utf-8")
    (docs / "update.md").write_text("# Update\n", encoding="utf-8")
    (docs / "notes.txt").write_text("not markdown\n", encoding="utf-8")
    (docs / "security").mkdir()
    (docs / "security" / "nested.md").write_text("# nested\n", encoding="utf-8")
    return docs


class WikiPagesTests(unittest.TestCase):
    def test_readme_maps_to_home_and_others_pass_through(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pages = publish_wiki.wiki_pages(_write_docs(Path(tmp)))
        self.assertEqual(
            {name: source.name for name, source in pages.items()},
            {
                "Home.md": "README.md",
                "01a-prereqs-entra-admin.md": "01a-prereqs-entra-admin.md",
                "update.md": "update.md",
            },
        )
        self.assertEqual(next(iter(pages)), "Home.md")

    def test_ignores_subdirectories_and_non_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            names = set(publish_wiki.wiki_pages(_write_docs(Path(tmp))))
        self.assertNotIn("notes.txt", names)
        self.assertNotIn("nested.md", names)


class RenderReleasePageTests(unittest.TestCase):
    def test_names_the_tag_sha_and_notes(self) -> None:
        body = publish_wiki.render_release_page("v1.4.2", "abc1234", "Fixed a thing.")
        self.assertIn("v1.4.2", body)
        self.assertIn("abc1234", body)
        self.assertIn("Fixed a thing.", body)


class RenderSidebarTests(unittest.TestCase):
    def test_lists_onboarding_and_operate_pages(self) -> None:
        sidebar = publish_wiki.render_sidebar(has_release=False)
        for page in (
            "Home",
            "01a-prereqs-entra-admin",
            "09-worked-example-salesforce",
            "90-troubleshooting",
            "update",
            "rollback",
            "cloud-installer",
        ):
            self.assertIn(f"]({page})", sidebar)
        self.assertIn("### Getting started", sidebar)
        self.assertIn("### Operate", sidebar)

    def test_release_entry_only_when_a_release_exists(self) -> None:
        without = publish_wiki.render_sidebar(has_release=False)
        with_release = publish_wiki.render_sidebar(has_release=True)
        self.assertNotIn("### Latest release", without)
        self.assertNotIn("](Release)", without)
        self.assertIn("### Latest release", with_release)
        self.assertIn("](Release)", with_release)


class PublishWikiEndToEndTests(unittest.TestCase):
    def _git(self, *args: str, cwd: Path | None = None) -> str:
        result = subprocess.run(
            ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
        )
        return result.stdout

    def _bare_with_stale_page(self, root: Path) -> Path:
        wiki = root / "wiki.git"
        self._git("init", "--bare", "--initial-branch=main", str(wiki))
        seed = root / "seed"
        self._git("clone", str(wiki), str(seed))
        (seed / "Stale.md").write_text("old page\n", encoding="utf-8")
        self._git("add", "-A", cwd=seed)
        self._git(
            "-c",
            "user.name=seed",
            "-c",
            "user.email=seed@example.com",
            "commit",
            "-m",
            "seed stale page",
            cwd=seed,
        )
        self._git("push", "origin", "HEAD", cwd=seed)
        return wiki

    def _publish(self, docs: Path, **env: str) -> int:
        full = {**os.environ, "DOCS_DIR": str(docs), **env}
        with patch.dict(os.environ, full, clear=True):
            return publish_wiki.main()

    def _tree(self, wiki: Path) -> list[str]:
        return self._git("-C", str(wiki), "ls-tree", "--name-only", "main").split()

    def test_replaces_stale_pages_and_renders_the_release(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wiki = self._bare_with_stale_page(root)
            docs = _write_docs(root)

            self.assertEqual(
                self._publish(
                    docs,
                    WIKI_REMOTE=str(wiki),
                    TAG="v1.4.2",
                    SHA="abc1234",
                    NOTES="Notes body.",
                ),
                0,
            )

            tree = self._tree(wiki)
            self.assertIn("Home.md", tree)
            self.assertIn("_Sidebar.md", tree)
            self.assertIn("Release.md", tree)
            self.assertNotIn("Stale.md", tree)
            self.assertNotIn("nested.md", tree)

            before = self._git("-C", str(wiki), "rev-parse", "main").strip()
            self.assertEqual(
                self._publish(
                    docs,
                    WIKI_REMOTE=str(wiki),
                    TAG="v1.4.2",
                    SHA="abc1234",
                    NOTES="Notes body.",
                ),
                0,
            )
            after = self._git("-C", str(wiki), "rev-parse", "main").strip()
            self.assertEqual(before, after)

    def test_skips_the_release_page_without_a_tag_and_sha(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wiki = self._bare_with_stale_page(root)
            docs = _write_docs(root)

            self.assertEqual(self._publish(docs, WIKI_REMOTE=str(wiki)), 0)

            tree = self._tree(wiki)
            self.assertIn("Home.md", tree)
            self.assertNotIn("Release.md", tree)


if __name__ == "__main__":
    unittest.main()
