import hashlib
import json
from pathlib import Path

from summarize_files import main, summarize_directory


def test_summary_is_sorted_and_excludes_hidden_files(tmp_path: Path) -> None:
    (tmp_path / "z.txt").write_text("z", encoding="utf-8")
    (tmp_path / "a.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    (tmp_path / ".secret").write_text("not included", encoding="utf-8")

    summary = summarize_directory(tmp_path)

    assert summary["file_count"] == 2
    expected_bytes = (tmp_path / "a.csv").stat().st_size + (tmp_path / "z.txt").stat().st_size
    assert summary["total_bytes"] == expected_bytes
    assert summary["extensions"] == {".csv": 1, ".txt": 1}
    assert [item["path"] for item in summary["files"]] == ["a.csv", "z.txt"]
    expected_hash = hashlib.sha256((tmp_path / "a.csv").read_bytes()).hexdigest()
    assert summary["files"][0]["sha256"] == expected_hash


def test_cli_writes_json_and_excludes_its_own_output(
    tmp_path: Path, capsys
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "one.md").write_text("# One\n", encoding="utf-8")
    output = source / "summary.json"

    assert main([str(source), "--output", str(output)]) == 0

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["file_count"] == 1
    assert payload["files"][0]["path"] == "one.md"
    expected_bytes = (source / "one.md").stat().st_size
    assert f"Wrote 1 files / {expected_bytes} bytes" in capsys.readouterr().out


def test_hidden_files_can_be_included(tmp_path: Path) -> None:
    (tmp_path / ".env.example").write_text("SAFE=value\n", encoding="utf-8")

    summary = summarize_directory(tmp_path, include_hidden=True)

    assert summary["file_count"] == 1
    assert summary["extensions"] == {".example": 1}
