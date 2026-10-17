"""Check mapped ADR/design links without importing the onboarding plugin."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"\{[a-zA-Z_][a-zA-Z_0-9]*\}")
LINK = re.compile(r"\[[^\]]*\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)")
CITATION = re.compile(r"\bADR[- ](\d{4})(?!\w)", re.IGNORECASE)


def _path(root: Path, value: str, base: Path | None = None) -> Path:
    path = (base or root) / value
    resolved = path.resolve()
    if Path(value).is_absolute() or not resolved.is_relative_to(root):
        raise ValueError(f"{value}: outside repository")
    if any(
        p.startswith((".env", "secrets.", "credentials."))
        or p.endswith((".key", ".pem"))
        for p in resolved.relative_to(root).parts
    ):
        raise ValueError(f"{value}: secret-bearing reference")
    if not resolved.is_file():
        raise ValueError(f"{value}: missing file")
    return resolved


def _read(path: Path) -> str:
    if path.stat().st_size > 1024 * 1024:
        raise ValueError(f"{path.name}: exceeds 1 MiB limit")
    return path.read_text(encoding="utf-8")


def _files(root: Path, pattern: str) -> set[Path]:
    glob = TOKEN.sub("*", pattern)
    if (
        Path(glob).is_absolute()
        or ".." in Path(glob).parts
        or "{" in glob
        or "}" in glob
        or "\\" in glob
    ):
        raise ValueError(f"{pattern}: invalid mapped pattern")
    static = glob.split("*", 1)[0]
    parent = root / (static if static.endswith("/") else str(Path(static).parent))
    if not parent.resolve().is_relative_to(root):
        raise ValueError(f"{pattern}: outside repository")
    return {
        _path(root, p.relative_to(root).as_posix())
        for p in root.glob(glob)
        if p.suffix == ".md"
    }


def _section(text: str, heading: str) -> str:
    parts = re.split(
        r"^## " + re.escape(heading) + r"\s*$",
        text,
        maxsplit=1,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    return (
        re.split(r"^## ", parts[1], maxsplit=1, flags=re.MULTILINE)[0]
        if len(parts) == 2
        else ""
    )


def validate_adr_links(root: Path) -> list[str]:
    root = root.resolve()
    errors = []
    try:
        roles = json.loads(_read(_path(root, "repo-map.json")))["artifact_paths"]
        adrs = _files(root, roles["adr"])
        designs = set().union(
            *[
                _files(root, roles[k])
                for k in (
                    "design_record_model",
                    "design_record_pipeline",
                    "design_record_area",
                )
                if k in roles
            ]
        )
        texts = {p: _read(p) for p in adrs | designs}
    except (ValueError, KeyError, OSError, RuntimeError) as exc:
        return [str(exc)]

    def links(file, text):
        found = set()
        for raw in LINK.findall(text):
            value = unquote(raw.split("#", 1)[0].strip("<>"))
            if not value or urlsplit(value).scheme in {"https", "http", "mailto"}:
                continue
            try:
                found.add(_path(root, value, file.parent))
            except (ValueError, OSError, RuntimeError) as exc:
                errors.append(f"{file.relative_to(root)}: {exc}")
        return found

    all_links = {p: links(p, t) for p, t in texts.items()}
    rejected = {
        p
        for p in adrs
        if re.search(
            r"^status:\s*[\"\']?rejected\b", texts[p], re.MULTILINE | re.IGNORECASE
        )
    }
    affected = {p: links(p, _section(texts[p], "Affected designs")) for p in adrs}
    for adr, targets in affected.items():
        for target in targets - designs:
            errors.append(
                f"{adr.name}: affected design {target.relative_to(root)} is outside mapped design patterns; retain its native check"
            )
        affected[adr] &= designs
    cited = {p: all_links[p] & adrs for p in designs}
    for design in designs:
        for number in CITATION.findall(texts[design]):
            matches = {
                p
                for p in adrs
                if re.match(
                    r"(?:ADR[- ])?" + number + r"(?:-|\.|$)", p.name, re.IGNORECASE
                )
            }
            if len(matches) == 1:
                cited[design].update(matches)
            else:
                errors.append(
                    f"{design.relative_to(root)}: unresolved or ambiguous ADR {number}"
                )
        for adr in cited[design]:
            if adr in rejected:
                successors = links(adr, _section(texts[adr], "Superseded by")) & (
                    adrs - rejected
                )
                if successors and not successors <= cited[design]:
                    errors.append(
                        f"{design.relative_to(root)}: cite successor of {adr.name}"
                    )
            elif design not in affected[adr]:
                errors.append(
                    f"{adr.name}: missing backlink to {design.relative_to(root)}"
                )
    for adr in adrs - rejected:
        for design in affected[adr]:
            if adr not in cited[design]:
                errors.append(f"{design.relative_to(root)}: must cite {adr.name}")
    return sorted(set(errors))


def test_adr_links():
    assert not (errors := validate_adr_links(ROOT)), "\n".join(errors)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    findings = validate_adr_links(parser.parse_args().root)
    if findings:
        print("\n".join(findings), file=sys.stderr)
    raise SystemExit(bool(findings))
