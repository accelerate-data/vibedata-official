"""Install dbt packages and build against one explicitly selected local DuckDB file."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_transform(db_path: Path, target: str = "dev") -> int:
    if not db_path.is_absolute():
        raise ValueError("db_path must be an absolute database file path")
    project = ROOT / "transformation"
    env = {**os.environ, "ONBOARDING_DUCKDB_PATH": str(db_path)}
    for command in ("deps", "build"):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "dbt.cli.main",
                command,
                "--project-dir",
                str(project),
                "--profiles-dir",
                str(project),
                "--target",
                target,
            ],
            cwd=ROOT,
            env=env,
            check=False,
        )
        if result.returncode:
            return result.returncode
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db-path", type=Path, required=True)
    parser.add_argument("--target", default="dev")
    args = parser.parse_args()
    try:
        raise SystemExit(run_transform(args.db_path, args.target))
    except ValueError as exc:
        parser.error(str(exc))
