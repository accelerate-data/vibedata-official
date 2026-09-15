"""Publish the canonical operator documentation to the vibedata-official wiki.

The canonical source is this repository's ``docs/**`` (top-level markdown); the
GitHub wiki is a separate git repository (``<repo>.wiki.git``) whose pages are its
top-level ``*.md`` files. This script clones that repository, replaces every page
with the canonical set — each page stripped of its YAML front matter (the wiki
does not render it) and with internal ``.md`` links rewritten to wiki page names —
writes the generated sidebar, and, for a release, renders the released version,
studio commit, and release notes into ``Release.md``.

It is release-coupled: ``publish.yml``'s payload gate is the authoritative gate,
and this script runs with the identity that gate validated. With no tag and sha it
publishes the current docs without a release page. It is a no-op when the rendered
pages already match what the wiki holds.

Canonical contract: studio ``docs/design/operator-documentation/README.md``.

Environment:
  WIKI_REMOTE  the ``*.wiki.git`` remote to clone and push (required)
  DOCS_DIR     canonical docs directory (default ``docs``)
  TAG          released version to stamp (optional)
  SHA          studio commit the release was built from (optional)
  NOTES        release notes to render on ``Release.md`` (optional)
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HOME_PAGE = "Home.md"
SIDEBAR_PAGE = "_Sidebar.md"
RELEASE_PAGE = "Release.md"
RELEASE_STEM = "Release"

GIT_AUTHOR_NAME = "github-actions[bot]"
GIT_AUTHOR_EMAIL = "41898282+github-actions[bot]@users.noreply.github.com"

# The sidebar reading path. The page names are wiki page names (no extension) —
# the onboarding pages 01a-09 and 90, then the Operate pages.
GETTING_STARTED_PAGES: tuple[tuple[str, str], ...] = (
    ("Overview", "Home"),
    ("01a · Microsoft Entra admin", "01a-prereqs-entra-admin"),
    ("01b · Microsoft Fabric admin", "01b-prereqs-fabric-admin"),
    ("01c · GitHub organisation owner", "01c-prereqs-github-org-owner"),
    ("01d · Azure infrastructure owner", "01d-prereqs-azure-infra"),
    ("01e · MotherDuck organisation admin", "01e-prereqs-motherduck-admin"),
    ("02 · Operator setup", "02-prereqs-operator"),
    ("03 · Deploy: Local Docker", "03-deploy-docker"),
    ("04 · Deploy: Kubernetes on Azure", "04-deploy-kubernetes-azure"),
    ("05 · Configure the organisation", "05-configure-org"),
    ("06 · Create your first domain", "06-first-domain"),
    ("07 · Confirm you are done", "07-verify"),
    ("08 · Domain contributor", "08-getting-started-contributor"),
    ("09 · Worked example", "09-worked-example-salesforce"),
    ("90 · Troubleshooting", "90-troubleshooting"),
)

OPERATE_PAGES: tuple[tuple[str, str], ...] = (
    ("Update Studio", "update"),
    ("Roll back a release", "rollback"),
    ("Cloud installer", "cloud-installer"),
)


def wiki_pages(docs_dir: str | Path) -> dict[str, Path]:
    """Map wiki page name to canonical source path.

    ``README.md`` becomes ``Home.md``; every other top-level ``docs/*.md`` keeps
    its filename. Subdirectories and non-markdown files are ignored. The mapping
    is ordered with ``Home.md`` first.
    """
    docs = Path(docs_dir)
    pages: dict[str, Path] = {}
    readme = docs / "README.md"
    if readme.is_file():
        pages[HOME_PAGE] = readme
    for source in sorted(docs.glob("*.md")):
        if source.name == "README.md":
            continue
        pages[source.name] = source
    return pages


def strip_front_matter(text: str) -> str:
    """Drop a leading ``--- ... ---`` YAML block.

    The GitHub wiki renderer does not consume YAML front matter, so the block
    would otherwise render as a stray rule and heading. Text without a leading
    delimiter, or with an unterminated one, is returned unchanged.
    """
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "".join(lines[index + 1 :])
    return text


def rewrite_wiki_links(text: str) -> str:
    """Point internal markdown links at the wiki page names.

    A wiki page is served at ``/wiki/<page>`` (without the extension), so
    ``](X.md)`` and ``](X.md#anchor)`` must lose the ``.md``; ``README.md`` and
    ``README`` name the ``Home`` page. External URLs, pure ``#anchor`` links, and
    non-``.md`` targets are left untouched.
    """
    return _LINK_RE.sub(_rewrite_link, text)


def _rewrite_link(match: re.Match[str]) -> str:
    target = match.group(1)
    if target.startswith(("#", "//", "mailto:")) or "://" in target:
        return match.group(0)
    path, sep, anchor = target.partition("#")
    if path in ("README", "./README"):
        return f"](Home{sep}{anchor})"
    if path.endswith(".md"):
        stem = path[:-3].removeprefix("./")
        return f"]({'Home' if stem == 'README' else stem}{sep}{anchor})"
    return match.group(0)


_LINK_RE = re.compile(r"\]\(([^)\n]+)\)")


def render_release_page(tag: str, sha: str, notes: str) -> str:
    """Render the generated ``Release.md`` naming the released build."""
    # The notes are raw model-generated text. GitHub sanitizes wiki markdown on
    # its own origin; the VitePress `markdown.html:false` control was retired
    # with the Pages surface (VD-5737).
    body = notes.rstrip("\n")
    return (
        f"# Release {tag}\n"
        "\n"
        f"This documentation was published for **{tag}**, "
        f"built from studio commit `{sha}`.\n"
        "\n"
        "## Release notes\n"
        "\n"
        f"{body}\n"
    )


def render_sidebar(has_release: bool) -> str:
    """Render ``_Sidebar.md``; the Latest release group only when one exists."""
    lines = ["### Getting started", ""]
    lines += [f"- [{label}]({page})" for label, page in GETTING_STARTED_PAGES]
    lines += ["", "### Operate", ""]
    lines += [f"- [{label}]({page})" for label, page in OPERATE_PAGES]
    if has_release:
        lines += [
            "",
            "### Latest release",
            "",
            f"- [Release notes]({RELEASE_STEM})",
        ]
    return "\n".join(lines) + "\n"


def _run(args: list[str]) -> str:
    result = subprocess.run(args, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)
    return result.stdout


def main() -> int:
    remote = os.environ.get("WIKI_REMOTE", "").strip()
    docs_dir = Path(os.environ.get("DOCS_DIR", "docs"))
    tag = os.environ.get("TAG", "").strip()
    sha = os.environ.get("SHA", "").strip()
    notes = os.environ.get("NOTES", "")

    if not remote:
        print("::error::WIKI_REMOTE is not set", file=sys.stderr)
        return 1
    if not docs_dir.is_dir():
        print(f"::error::DOCS_DIR not found: {docs_dir}", file=sys.stderr)
        return 1

    # A release publish must name its own build: a tag without the studio commit
    # and the release notes is a malformed invocation. publish.yml's payload gate
    # is authoritative; this guard is the executable-side check for the manual
    # trigger too.
    if tag and not (sha and notes.strip()):
        print(
            "::error::a release tag requires both SHA (studio commit) and "
            "NOTES (release notes)",
            file=sys.stderr,
        )
        return 1

    has_release = bool(tag and sha)
    pages = wiki_pages(docs_dir)
    # Removing the existing pages is destructive: refuse a source set that is
    # empty or has no README.md (no Home.md), which would wipe the wiki.
    if not pages or HOME_PAGE not in pages:
        print(
            f"::error::refusing to replace the wiki: {docs_dir} has no README.md "
            "(no Home.md) — the canonical page set is empty or misconfigured",
            file=sys.stderr,
        )
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp) / "wiki"
        _run(["git", "clone", "--depth", "1", remote, str(workdir)])

        # A stale page must never linger: the wiki is exactly the canonical set.
        for stale in workdir.glob("*.md"):
            stale.unlink()

        for page_name, source in pages.items():
            rendered = rewrite_wiki_links(
                strip_front_matter(source.read_text(encoding="utf-8"))
            )
            (workdir / page_name).write_text(rendered, "utf-8")
        (workdir / SIDEBAR_PAGE).write_text(render_sidebar(has_release), "utf-8")
        if has_release:
            (workdir / RELEASE_PAGE).write_text(
                rewrite_wiki_links(render_release_page(tag, sha, notes)), "utf-8"
            )

        _run(["git", "-C", str(workdir), "config", "user.name", GIT_AUTHOR_NAME])
        _run(["git", "-C", str(workdir), "config", "user.email", GIT_AUTHOR_EMAIL])
        _run(["git", "-C", str(workdir), "add", "-A"])

        diff = subprocess.run(
            ["git", "-C", str(workdir), "diff", "--cached", "--quiet"], check=False
        )
        if diff.returncode == 0:
            print("Wiki already matches the canonical docs; nothing to publish.")
            return 0

        message = (
            f"Publish operator documentation for {tag}"
            if has_release
            else "Publish operator documentation"
        )
        _run(["git", "-C", str(workdir), "commit", "-m", message])
        _run(["git", "-C", str(workdir), "push", "origin", "HEAD"])

    print(f"Published {len(pages)} wiki pages (home, sidebar, release={has_release}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
