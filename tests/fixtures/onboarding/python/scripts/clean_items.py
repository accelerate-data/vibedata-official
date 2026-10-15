"""Legacy application: preserve this implementation."""
import csv
from pathlib import Path

def load_items(path):
    with Path(path).open() as source:
        return list(csv.DictReader(source))

if __name__ == "__main__":
    Path("EXECUTED_MARKER").write_text("unsafe discovery")
