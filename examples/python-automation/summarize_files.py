#!/usr/bin/env python3
"""Create a deterministic JSON inventory for a directory."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Sequence


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest for one file without loading it all at once."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_hidden(relative_path: Path) -> bool:
    """Return True when any relative path component begins with a dot."""
    return any(part.startswith(".") for part in relative_path.parts)


def summarize_directory(
    root: Path,
    *,
    include_hidden: bool = False,
    excluded_paths: set[Path] | None = None,
) -> dict[str, object]:
    """Build a stable, machine-readable inventory for *root*."""
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"not a directory: {root}")

    excluded = {path.resolve() for path in (excluded_paths or set())}
    files: list[dict[str, object]] = []
    extension_counts: Counter[str] = Counter()
    total_bytes = 0

    for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file()):
        if path.resolve() in excluded:
            continue
        relative = path.relative_to(root)
        if not include_hidden and is_hidden(relative):
            continue

        size = path.stat().st_size
        extension = path.suffix.lower() or "[none]"
        total_bytes += size
        extension_counts[extension] += 1
        files.append(
            {
                "path": relative.as_posix(),
                "bytes": size,
                "sha256": sha256_file(path),
            }
        )

    return {
        "schema_version": "1.0",
        "root": root.name,
        "file_count": len(files),
        "total_bytes": total_bytes,
        "extensions": dict(sorted(extension_counts.items())),
        "files": files,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Write a deterministic JSON inventory for a directory."
    )
    parser.add_argument("directory", type=Path, help="directory to inspect")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("file-summary.json"),
        help="JSON destination (default: file-summary.json)",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="include files whose relative path contains a dot-prefixed component",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output = args.output.resolve()
    try:
        summary = summarize_directory(
            args.directory,
            include_hidden=args.include_hidden,
            excluded_paths={output},
        )
    except ValueError as error:
        raise SystemExit(str(error)) from error

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {summary['file_count']} files / "
        f"{summary['total_bytes']} bytes to {output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
