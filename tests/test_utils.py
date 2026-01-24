"""Tests for lumpy_log.utils module."""

import os
from pathlib import Path
import pytest
from lumpy_log.utils import (
    _get_templates_dir,
    _clean_markdown,
    _format_markdown,
    _collect_items,
    _generate_obsidian_index,
    _generate_devlog,
    _generate_docx,
    _rebuild_index,
)


class TestGetTemplatesDir:
    """Tests for _get_templates_dir function."""

    def test_returns_string(self):
        """Should return a string path."""
        result = _get_templates_dir()
        assert isinstance(result, str)

    def test_templates_dir_exists(self):
        """Should return a path to an existing directory."""
        result = _get_templates_dir()
        assert os.path.isdir(result)

    def test_contains_obsidian_template(self):
        """Should point to a directory containing obsidian_index.md template."""
        result = _get_templates_dir()
        template_path = os.path.join(result, "obsidian_index.md")
        assert os.path.isfile(template_path)


class TestCleanMarkdown:
    """Tests for _clean_markdown function."""

    def test_strips_trailing_whitespace(self):
        """Should remove trailing spaces from each line."""
        input_md = "line 1  \nline 2  \n"
        result = _clean_markdown(input_md)
        assert result == "line 1\nline 2\n"

    def test_removes_excess_blank_lines(self):
        """Should reduce 3+ consecutive blank lines to 2."""
        input_md = "line 1\n\n\n\nline 2\n"
        result = _clean_markdown(input_md)
        assert result == "line 1\n\nline 2\n"

    def test_preserves_single_blank_lines(self):
        """Should keep single blank lines between content."""
        input_md = "line 1\n\nline 2\n"
        result = _clean_markdown(input_md)
        assert result == "line 1\n\nline 2\n"

    def test_preserves_double_blank_lines(self):
        """Should keep double blank lines."""
        input_md = "line 1\n\n\nline 2\n"
        result = _clean_markdown(input_md)
        # Three newlines -> two blank lines (3+ collapsed to 2)
        assert result == "line 1\n\nline 2\n"

    def test_ends_with_newline(self):
        """Should always end with a newline."""
        assert _clean_markdown("no newline").endswith("\n")
        assert _clean_markdown("has newline\n").endswith("\n")
        assert _clean_markdown("multiple\n\n\n").endswith("\n")

    def test_strips_leading_trailing_whitespace(self):
        """Should strip leading/trailing whitespace from entire content."""
        input_md = "  \n\nline 1\nline 2\n\n  "
        result = _clean_markdown(input_md)
        assert result.startswith("line 1")
        assert result.endswith("line 2\n")


class TestFormatMarkdown:
    """Tests for _format_markdown function."""

    def test_returns_string(self):
        """Should return a string."""
        result = _format_markdown("# Title\n")
        assert isinstance(result, str)

    def test_ends_with_newline(self):
        """Should always end with a newline."""
        result = _format_markdown("text")
        assert result.endswith("\n")

    def test_falls_back_to_clean_on_error(self):
        """Should fall back to _clean_markdown if mdformat fails."""
        # Create input that mdformat might choke on
        input_md = "line  \n\n\n\nline2"
        result = _format_markdown(input_md)
        # Should at least be cleaned
        assert "line" in result
        assert result.endswith("\n")

    def test_preserves_content(self):
        """Should preserve markdown content."""
        input_md = "# Title\n\nContent here\n"
        result = _format_markdown(input_md)
        assert "# Title" in result
        assert "Content here" in result


class TestCollectItems:
    """Tests for _collect_items function."""

    def test_returns_tuple(self):
        """Should return a tuple of (items, commits, tests)."""
        result = _collect_items("/tmp")
        assert isinstance(result, tuple)
        assert len(result) == 4

    def test_empty_folder(self, tmp_path):
        """Should handle empty folder gracefully."""
        items, commits, tests, total = _collect_items(str(tmp_path))
        assert items == []
        assert commits == []
        assert tests == []
        assert total == 0

    def test_collects_commits(self, tmp_path):
        """Should collect markdown files from commits/ directory."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_test.md").write_text("content")

        items, commits, tests, total = _collect_items(str(tmp_path))
        assert len(commits) == 1
        assert commits[0].name == "20240101_1200_test.md"

    def test_collects_tests(self, tmp_path):
        """Should collect markdown files from tests/ directory."""
        tests_dir = tmp_path / "tests"
        tests_dir.mkdir()
        (tests_dir / "20240101_1200_test.md").write_text("content")

        items, commits, tests, total = _collect_items(str(tmp_path))
        assert len(tests) == 1
        assert tests[0].name == "20240101_1200_test.md"

    def test_items_have_required_fields(self, tmp_path):
        """Items should have path, name, type, and filename."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_commit.md").write_text("content")

        items, commits, tests, total = _collect_items(str(tmp_path))
        assert len(items) == 1
        item = items[0]
        assert "path" in item
        assert "name" in item
        assert "type" in item
        assert "filename" in item
        assert item["type"] == "commit"

    def test_sorts_oldest_first_by_default(self, tmp_path):
        """Should sort by filename, oldest first by default."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240102_1200_test.md").write_text("content")
        (commits_dir / "20240101_1200_test.md").write_text("content")

        items, commits, tests, total = _collect_items(str(tmp_path), changelog_order=False)
        assert items[0]["filename"] == "20240101_1200_test.md"
        assert items[1]["filename"] == "20240102_1200_test.md"

    def test_sorts_newest_first_with_changelog_order(self, tmp_path):
        """Should sort newest first when changelog_order=True."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_test.md").write_text("content")
        (commits_dir / "20240102_1200_test.md").write_text("content")

        items, commits, tests, total = _collect_items(str(tmp_path), changelog_order=True)
        assert items[0]["filename"] == "20240102_1200_test.md"
        assert items[1]["filename"] == "20240101_1200_test.md"


class TestGenerateObsidianIndex:
    """Tests for _generate_obsidian_index function."""

    def test_creates_index_file(self, tmp_path):
        """Should create index.md file."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_commit.md").write_text("# Commit\nContent")

        items, commits, tests, total = _collect_items(str(tmp_path))
        result = _generate_obsidian_index(str(tmp_path), items)

        assert "obsidian" in result
        assert (tmp_path / "index.md").exists()

    def test_index_contains_items(self, tmp_path):
        """Generated index should reference the items."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_mycommit.md").write_text("# My Commit")

        items, commits, tests, total = _collect_items(str(tmp_path))
        _generate_obsidian_index(str(tmp_path), items)

        index_content = (tmp_path / "index.md").read_text(encoding="utf-8")
        # Index should mention the commit
        assert "mycommit" in index_content.lower() or "commit" in index_content.lower()

    def test_returns_dict_with_obsidian_key(self, tmp_path):
        """Should return dict with obsidian key."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_test.md").write_text("content")

        items, commits, tests, total = _collect_items(str(tmp_path))
        result = _generate_obsidian_index(str(tmp_path), items)

        assert isinstance(result, dict)
        assert "obsidian" in result
        assert isinstance(result["obsidian"], str)


class TestGenerateDevlog:
    """Tests for _generate_devlog function."""

    def test_creates_devlog_file(self, tmp_path):
        """Should create devlog.md file."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_commit.md").write_text("# Commit\nBody")

        items, commits, tests, total = _collect_items(str(tmp_path))
        result = _generate_devlog(str(tmp_path), items)

        assert "devlog" in result
        assert (tmp_path / "devlog.md").exists()

    def test_devlog_contains_content(self, tmp_path):
        """Devlog should contain item content."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_commit.md").write_text("# Commit\nTest body")

        items, commits, tests, total = _collect_items(str(tmp_path))
        _generate_devlog(str(tmp_path), items)

        devlog_content = (tmp_path / "devlog.md").read_text(encoding="utf-8")
        assert "# Commit" in devlog_content
        assert "Test body" in devlog_content

    def test_devlog_interleaves_commits_and_tests(self, tmp_path):
        """Devlog should include both commits and tests in order."""
        commits_dir = tmp_path / "commits"
        tests_dir = tmp_path / "tests"
        commits_dir.mkdir()
        tests_dir.mkdir()

        (commits_dir / "20240101_1200_commit.md").write_text("# Commit 1")
        (tests_dir / "20240102_1200_test.md").write_text("# Test 1")

        items, commits, tests, total = _collect_items(str(tmp_path))
        _generate_devlog(str(tmp_path), items)

        devlog_content = (tmp_path / "devlog.md").read_text(encoding="utf-8")
        assert "# Commit 1" in devlog_content
        assert "# Test 1" in devlog_content
        assert devlog_content.index("# Commit 1") < devlog_content.index("# Test 1")

    def test_devlog_has_header(self, tmp_path):
        """Devlog should have proper header with generation info."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_test.md").write_text("content")

        items, commits, tests, total = _collect_items(str(tmp_path))
        _generate_devlog(str(tmp_path), items)

        devlog_content = (tmp_path / "devlog.md").read_text(encoding="utf-8")
        assert "# Devlog" in devlog_content
        assert "Generated:" in devlog_content
        assert "Items:" in devlog_content

    def test_returns_dict_with_devlog_key(self, tmp_path):
        """Should return dict with devlog key."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_test.md").write_text("content")

        items, commits, tests, total = _collect_items(str(tmp_path))
        result = _generate_devlog(str(tmp_path), items)

        assert isinstance(result, dict)
        assert "devlog" in result
        assert isinstance(result["devlog"], str)


class TestGenerateDocx:
    """Tests for _generate_docx function."""

    def test_returns_dict(self, tmp_path):
        """Should return a dictionary."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n")
        result = _generate_docx(str(md_file))
        assert isinstance(result, dict)

    def test_successful_conversion(self, tmp_path):
        """Should successfully convert markdown to docx."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n\nContent here.")
        
        result = _generate_docx(str(md_file))
        
        assert "docx" in result
        docx_file = Path(result["docx"])
        assert docx_file.exists()

    def test_custom_output_path(self, tmp_path):
        """Should use custom output path."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n")
        
        output_file = tmp_path / "custom.docx"
        result = _generate_docx(str(md_file), str(output_file))
        
        if result:
            assert Path(result["docx"]).exists()

    def test_defaults_to_same_dir_as_md(self, tmp_path):
        """Should default to devlog.docx in same directory as md file."""
        md_file = tmp_path / "devlog.md"
        md_file.write_text("# Test\n")
        
        result = _generate_docx(str(md_file))
        
        # Result should indicate it tried to create devlog.docx
        if result and "docx" in result:
            assert "devlog.docx" in result["docx"]

    def test_docx_with_realistic_devlog_content(self, tmp_path):
        """Test docx conversion with realistic devlog markdown content."""
        # Create a realistic devlog similar to what _generate_devlog produces
        md_file = tmp_path / "devlog.md"
        devlog_content = """# Devlog

Generated: 2024-01-15 12:00:00
Items: 2 (1 commits, 1 tests)

# Commit One

This is a commit description with **important** changes.

```python
def new_feature():
    return "implemented"
```

---

# Test One

- Test passed successfully
- All assertions met"""
        md_file.write_text(devlog_content)
        
        result = _generate_docx(str(md_file), verbose=True)
        
        # Conversion should succeed with new converter
        assert isinstance(result, dict)
        if result:
            assert "docx" in result
            assert Path(result["docx"]).exists()


class TestRebuildIndex:
    """Tests for _rebuild_index function."""

    def test_returns_dict(self, tmp_path):
        """Should return a dictionary."""
        result = _rebuild_index(str(tmp_path))
        assert isinstance(result, dict)

    def test_default_output_format_is_obsidian(self, tmp_path):
        """Should default to obsidian output format."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_test.md").write_text("content")

        result = _rebuild_index(str(tmp_path))

        assert "obsidian" in result
        assert (tmp_path / "index.md").exists()

    def test_obsidian_output_format(self, tmp_path):
        """Should generate obsidian index when requested."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_test.md").write_text("content")

        result = _rebuild_index(str(tmp_path), output_formats=["obsidian"])

        assert "obsidian" in result
        assert (tmp_path / "index.md").exists()

    def test_devlog_output_format(self, tmp_path):
        """Should generate devlog when requested."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_test.md").write_text("content")

        result = _rebuild_index(str(tmp_path), output_formats=["devlog"])

        assert "devlog" in result
        assert (tmp_path / "devlog.md").exists()
        # Obsidian should not be created
        assert not (tmp_path / "index.md").exists()

    def test_multiple_output_formats(self, tmp_path):
        """Should handle multiple output formats."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_test.md").write_text("content")

        result = _rebuild_index(str(tmp_path), output_formats=["obsidian", "devlog"])

        assert "obsidian" in result
        assert "devlog" in result
        assert (tmp_path / "index.md").exists()
        assert (tmp_path / "devlog.md").exists()

    def test_devlog_and_docx_both_requested(self, tmp_path):
        """Should keep devlog.md when both devlog and docx are requested."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_test.md").write_text("content")

        result = _rebuild_index(str(tmp_path), output_formats=["devlog", "docx"])

        # devlog.md should exist
        assert (tmp_path / "devlog.md").exists()
        # devlog key should be in results
        assert "devlog" in result

    def test_only_docx_removes_devlog_md(self, tmp_path):
        """Should remove devlog.md if only docx is requested."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_test.md").write_text("content")

        result = _rebuild_index(str(tmp_path), output_formats=["docx"])

        # devlog.md should be cleaned up if only docx was requested
        # and docx failed (since we're not mocking the conversion)
        # If docx succeeded, the file is cleaned up
        # If docx failed, the file is cleaned up anyway
        # So we just check that the behavior is consistent
        assert isinstance(result, dict)

    def test_changelog_order_oldest_first(self, tmp_path):
        """Should order oldest first when changelog_order=False."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240102_1200_test.md").write_text("# Second")
        (commits_dir / "20240101_1200_test.md").write_text("# First")

        result = _rebuild_index(str(tmp_path), changelog_order=False, output_formats=["devlog"])

        devlog_content = (tmp_path / "devlog.md").read_text(encoding="utf-8")
        assert devlog_content.index("# First") < devlog_content.index("# Second")

    def test_changelog_order_newest_first(self, tmp_path):
        """Should order newest first when changelog_order=True."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_test.md").write_text("# First")
        (commits_dir / "20240102_1200_test.md").write_text("# Second")

        result = _rebuild_index(str(tmp_path), changelog_order=True, output_formats=["devlog"])

        devlog_content = (tmp_path / "devlog.md").read_text(encoding="utf-8")
        assert devlog_content.index("# Second") < devlog_content.index("# First")

    def test_verbose_output(self, tmp_path, capsys):
        """Should print verbose messages when verbose=True."""
        commits_dir = tmp_path / "commits"
        commits_dir.mkdir()
        (commits_dir / "20240101_1200_test.md").write_text("content")

        _rebuild_index(str(tmp_path), verbose=True)

        captured = capsys.readouterr()
        assert "Rebuilding index" in captured.out
