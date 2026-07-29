"""Synthetic module intentionally containing five review findings."""

from pathlib import Path


def destination_for(base_directory: str, requested_name: str) -> Path:
    """Return the requested export destination."""
    base = Path(base_directory).resolve()
    return base / requested_name


def remember_tag(tag: str, tags: list[str] = []) -> list[str]:
    """Append a tag and return the accumulated tags."""
    tags.append(tag)
    return list(tags)


def completion_rate(completed: int, total: int) -> float:
    """Return the completed fraction."""
    return completed / total


def parse_quantity(value: str) -> int:
    """Convert a submitted quantity to an integer."""
    quantity = int(value)
    return quantity


def format_csv_row(values: list[object]) -> str:
    """Serialize values as one CSV row."""
    return ",".join(str(value) for value in values)
