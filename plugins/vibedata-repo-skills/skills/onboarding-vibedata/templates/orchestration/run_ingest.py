"""Run registered pipelines against one explicitly selected local DuckDB file."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_ingest(db_path: Path) -> int:
    if not db_path.is_absolute():
        raise ValueError("db_path must be an absolute database file path")
    repo = json.loads((ROOT / "repo-map.json").read_text(encoding="utf-8"))
    pipelines = []
    for source in repo["sources"].values():
        if "pipeline" not in source:
            continue
        path = (ROOT / source["pipeline"]).resolve()
        if (
            Path(source["pipeline"]).is_absolute()
            or not path.is_relative_to(ROOT)
            or not path.is_file()
        ):
            raise ValueError(f"Invalid registered pipeline: {source['pipeline']}")
        if path not in pipelines:
            pipelines.append(path)
    python_path = str(ROOT / "ingestion")
    if os.environ.get("PYTHONPATH"):
        python_path += os.pathsep + os.environ["PYTHONPATH"]
    env = {
        **os.environ,
        "ONBOARDING_DUCKDB_PATH": str(db_path),
        "PYTHONPATH": python_path,
    }
    for pipeline in pipelines:
        result = subprocess.run(
            [sys.executable, str(pipeline)],
            cwd=ROOT / "ingestion",
            env=env,
            check=False,
        )
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db-path", type=Path, required=True)
    args = parser.parse_args()
    try:
        raise SystemExit(run_ingest(args.db_path))
    except ValueError as exc:
        parser.error(str(exc))
