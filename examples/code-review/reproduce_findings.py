"""Reproduce every finding in sample_before.py without external dependencies."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile

import sample_before


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = Path(directory) / "exports"
        base.mkdir()
        escaped = sample_before.destination_for(
            str(base), "../outside.txt"
        ).resolve()
        path_traversal_escapes = not escaped.is_relative_to(base.resolve())

    sample_before.remember_tag("alpha")
    second_tags = sample_before.remember_tag("beta")

    division_by_zero = False
    try:
        sample_before.completion_rate(0, 0)
    except ZeroDivisionError:
        division_by_zero = True

    csv_row = sample_before.format_csv_row(["Smith, Alice", 3])
    results = {
        "pathTraversalEscapes": path_traversal_escapes,
        "mutableDefaultLeaksState": second_tags == ["alpha", "beta"],
        "zeroTotalRaisesUnexpectedly": division_by_zero,
        "negativeQuantityAccepted": sample_before.parse_quantity("-2") == -2,
        "commaFieldIsUnescaped": csv_row == "Smith, Alice,3",
    }
    if not all(results.values()):
        raise SystemExit("one or more documented findings did not reproduce")
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
