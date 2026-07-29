"""Corrected version of the synthetic review target."""

from __future__ import annotations

import csv
import io
from pathlib import Path


def destination_for(base_directory: str, requested_name: str) -> Path:
    """Return a destination that remains inside the configured base."""
    base = Path(base_directory).resolve()
    candidate = (base / requested_name).resolve()
    if not candidate.is_relative_to(base):
        raise ValueError("requested path escapes the export directory")
    return candidate


def remember_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    """Append a tag without sharing state between calls."""
    output = list(tags) if tags is not None else []
    output.append(tag)
    return output


def completion_rate(completed: int, total: int) -> float:
    """Return the completed fraction for a positive total."""
    if total <= 0:
        raise ValueError("total must be greater than zero")
    return completed / total


def parse_quantity(value: str) -> int:
    """Convert a submitted quantity to a non-negative integer."""
    quantity = int(value)
    if quantity < 0:
        raise ValueError("quantity must not be negative")
    return quantity


def format_csv_row(values: list[object]) -> str:
    """Serialize values with standards-compliant CSV escaping."""
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="")
    writer.writerow(values)
    return buffer.getvalue()
