"""Unit tests for scripts/publish_wiki.py, the wiki publication helpers.

The mapping, text-transformation, sidebar, and release-page helpers are pure and
asserted directly. The end-to-end tests publish into a throwaway bare git
repository to prove the replace-stale-pages behaviour, the front-matter/link
rendering, the release gating, and the no-op path of main().
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

DOCS = Path(__file__).resolve().parents[1] / "docs"
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


class TextTransformTests(unittest.TestCase):
    def test_strip_front_matter_removes_a_leading_yaml_block(self) -> None:
        text = "---\napplies-to: v1\nverified-on: 2026-01-01\n---\n\n# Body\n"
        self.assertEqual(publish_wiki.strip_front_matter(text), "\n# Body\n")

    def test_strip_front_matter_leaves_plain_text_alone(self) -> None:
        text = "# Body\n\nNo front matter here.\n"
        self.assertEqual(publish_wiki.strip_front_matter(text), text)

    def test_rewrite_wiki_links_drops_the_extension(self) -> None:
        self.assertEqual(
            publish_wiki.rewrite_wiki_links("[Update](update.md)"),
            "[Update](update)",
        )

    def test_rewrite_wiki_links_preserves_the_anchor(self) -> None:
        self.assertEqual(
            publish_wiki.rewrite_wiki_links(
                "[Sign in](02-prereqs-operator.md#sign-in)"
            ),
            "[Sign in](02-prereqs-operator#sign-in)",
        )

    def test_rewrite_wiki_links_points_readme_at_home(self) -> None:
        self.assertEqual(
            publish_wiki.rewrite_wiki_links("[Back](README.md)"),
            "[Back](Home)",
        )
        self.assertEqual(
            publish_wiki.rewrite_wiki_links("[Back](README)"),
            "[Back](Home)",
        )
        self.assertEqual(
            publish_wiki.rewrite_wiki_links("[Back](README.md#top)"),
            "[Back](Home#top)",
        )

    def test_rewrite_wiki_links_leaves_external_anchors_and_files(self) -> None:
        text = "[Ext](https://example.com/docs.md) [Frag](#the-chart) [Asset](logo.png)"
        self.assertEqual(publish_wiki.rewrite_wiki_links(text), text)

    def test_real_home_page_renders_cleanly(self) -> None:
        # The canonical README is the wiki Home page: no front matter, no .md
        # links left behind.
        rendered = publish_wiki.rewrite_wiki_links(
            publish_wiki.strip_front_matter(
                (DOCS / "README.md").read_text(encoding="utf-8")
            )
        )
        self.assertFalse(rendered.lstrip().startswith("---"))
        self.assertIn("](update)", rendered)
        self.assertNotIn("](update.md)", rendered)


class SidebarCoverageTests(unittest.TestCase):
    def _published_stems(self) -> set[str]:
        return {Path(name).stem for name in publish_wiki.wiki_pages(DOCS)}

    def _referenced(self) -> set[str]:
        return {
            page
            for _, page in (
                publish_wiki.GETTING_STARTED_PAGES + publish_wiki.OPERATE_PAGES
            )
        }

    def test_every_sidebar_page_exists_in_the_published_set(self) -> None:
        self.assertTrue(self._referenced() <= self._published_stems())

    def test_every_published_page_is_reachable_from_the_sidebar(self) -> None:
        # Home is the sidebar's Overview entry; _Sidebar and Release are generated.
        unreachable = (
            self._published_stems()
            - self._referenced()
            - {"Home", "Release", "_Sidebar"}
        )
        self.assertEqual(unreachable, set())


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

    def test_lists_the_latest_release_and_installer_links(self) -> None:
        # Reachable with or without a generated release page: the GitHub Release
        # is the release-notes + assets entry point, and the installer is its
        # attached install.sh asset.
        for has_release in (False, True):
            sidebar = publish_wiki.render_sidebar(has_release=has_release)
            self.assertIn("### Releases", sidebar)
            self.assertIn(
                f"- [Latest release notes]({publish_wiki.RELEASES_URL})", sidebar
            )
            self.assertIn(f"- [Installer]({publish_wiki.INSTALLER_URL})", sidebar)

    def test_generated_release_entry_only_when_a_release_exists(self) -> None:
        without = publish_wiki.render_sidebar(has_release=False)
        with_release = publish_wiki.render_sidebar(has_release=True)
        self.assertNotIn("](Release)", without)
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

    def test_refuses_a_source_set_without_a_home_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wiki = self._bare_with_stale_page(root)
            before = self._git("-C", str(wiki), "rev-parse", "main").strip()

            empty = root / "empty-docs"
            empty.mkdir()
            no_home = root / "no-home-docs"
            no_home.mkdir()
            (no_home / "update.md").write_text("# Update\n", encoding="utf-8")

            for docs in (empty, no_home):
                with self.subTest(docs=docs.name):
                    self.assertEqual(
                        self._publish(
                            docs,
                            WIKI_REMOTE=str(wiki),
                            TAG="v1.4.2",
                            SHA="abc1234",
                            NOTES="Notes body.",
                        ),
                        1,
                    )
                    # The guard runs before the clone, so the wiki is untouched.
                    self.assertEqual(
                        before, self._git("-C", str(wiki), "rev-parse", "main").strip()
                    )
                    self.assertIn("Stale.md", self._tree(wiki))

    def test_requires_sha_and_notes_when_tag_is_supplied(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wiki = self._bare_with_stale_page(root)
            docs = _write_docs(root)
            self.assertEqual(
                self._publish(
                    docs, WIKI_REMOTE=str(wiki), TAG="v1.4.2", SHA="", NOTES="n"
                ),
                1,
            )
            self.assertEqual(
                self._publish(
                    docs, WIKI_REMOTE=str(wiki), TAG="v1.4.2", SHA="abc1234", NOTES=""
                ),
                1,
            )

    def test_published_pages_strip_front_matter_and_rewrite_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wiki = self._bare_with_stale_page(root)
            docs = root / "docs"
            docs.mkdir()
            (docs / "README.md").write_text(
                "---\napplies-to: vibedata v1\n---\n\n# Home\n\n"
                "See [Update](update.md), [Step](02-prereqs-operator.md#sign-in), "
                "[Ext](https://example.com/x.md), and [Frag](#frag).\n",
                encoding="utf-8",
            )
            (docs / "update.md").write_text("# Update\n", encoding="utf-8")
            (docs / "02-prereqs-operator.md").write_text("# Step\n", encoding="utf-8")

            self.assertEqual(
                self._publish(
                    docs,
                    WIKI_REMOTE=str(wiki),
                    TAG="v1.4.2",
                    SHA="abc1234",
                    NOTES="See [Update](update.md).",
                ),
                0,
            )

            home = self._git("-C", str(wiki), "show", "main:Home.md")
            self.assertNotIn("applies-to", home)
            self.assertFalse(home.lstrip().startswith("---"))
            self.assertIn("](update)", home)
            self.assertIn("](02-prereqs-operator#sign-in)", home)
            self.assertIn("](https://example.com/x.md)", home)
            self.assertIn("](#frag)", home)

            release = self._git("-C", str(wiki), "show", "main:Release.md")
            self.assertIn("](update)", release)
            self.assertNotIn("](update.md)", release)


if __name__ == "__main__":
    unittest.main()
