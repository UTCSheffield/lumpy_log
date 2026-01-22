import os
import re
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import mdformat
from lumpy_log.md_to_docx import markdown_file_to_docx

def _get_templates_dir():
    package_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(package_dir, "templates")

def _clean_markdown(md: str) -> str:
    cleaned_lines = [line.rstrip() for line in md.splitlines()]
    cleaned = "\n".join(cleaned_lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip() + "\n"

def _format_markdown(md: str) -> str:
    if mdformat:
        try:
            return mdformat.text(md).rstrip() + "\n"
        except Exception:
            pass
    return _clean_markdown(md)

def _collect_items(output_folder: str, changelog_order: bool = False) -> tuple:
    """Collect and organize commit and test items from output folder.
    
    Args:
        output_folder: Base output folder containing commits/ and tests/
        changelog_order: If True, sort newest first. If False (default), oldest first
    
    Returns:
        Tuple of (items_list, commit_files, test_files)
    """
    output_path = Path(output_folder)
    commits_dir = output_path / "commits"
    tests_dir = output_path / "tests"
    
    # Collect files
    commit_files = sorted(commits_dir.glob("*.md")) if commits_dir.exists() else []
    test_files = sorted(tests_dir.glob("*.md")) if tests_dir.exists() else []
    
    # Create combined list with type markers
    items = []
    for f in commit_files:
        items.append({"path": f"commits/{f.name}", "name": f.stem, "type": "commit", "filename": f.name})
    for f in test_files:
        items.append({"path": f"tests/{f.name}", "name": f.stem, "type": "test", "filename": f.name})
    
    items.sort(key=lambda x: x['filename'], reverse=changelog_order)
    
    return items, commit_files, test_files

def _generate_obsidian_index(output_folder: str, items: list, verbose: bool = False) -> dict:
    """Generate Obsidian index from items.
    
    Args:
        output_folder: Base output folder
        items: List of items with path, name, type, and filename
        verbose: Print progress messages
    
    Returns:
        Dict with "obsidian" key pointing to index path
    """
    output_path = Path(output_folder)
    commit_count = sum(1 for item in items if item["type"] == "commit")
    test_count = sum(1 for item in items if item["type"] == "test")
    
    # Set up Jinja2 for templates
    jinja_env = Environment(loader=FileSystemLoader(_get_templates_dir()))
    
    index_path = output_path / "index.md"
    template = jinja_env.get_template("obsidian_index.md")
    index_content = _clean_markdown(template.render({
        "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "repo_path": ".",
        "items": items,
        "total_items": len(items),
        "total_commits": commit_count,
        "total_tests": test_count
    }))
    
    index_path.write_text(index_content, encoding="utf-8")
    if verbose:
        print(f"Updated index: {index_path}")
    
    return {"obsidian": str(index_path)}

def _generate_devlog(output_folder: str, items: list, verbose: bool = False) -> dict:
    """Generate devlog markdown from items.
    
    Args:
        output_folder: Base output folder
        items: List of items with path, name, type, and filename
        verbose: Print progress messages
    
    Returns:
        Dict with "devlog" key pointing to devlog path
    """
    output_path = Path(output_folder)
    commit_count = sum(1 for item in items if item["type"] == "commit")
    test_count = sum(1 for item in items if item["type"] == "test")
    
    header_lines = [
        "# Devlog",
        "",
        datetime.now().strftime("Generated: %Y-%m-%d %H:%M:%S"),
        f"Items: {len(items)} ({commit_count} commits, {test_count} tests)",
        "",
    ]
    
    segments = []
    for item in items:
        entry_path = output_path / item["path"]
        try:
            entry_text = entry_path.read_text(encoding="utf-8").strip()
            segments.append(entry_text)
        except FileNotFoundError:
            if verbose:
                print(f"Missing item skipped: {entry_path}")
    
    devlog_body = "\n\n---\n\n".join(segments)
    full_devlog = _clean_markdown("\n".join(header_lines + ([devlog_body] if devlog_body else [])))
    
    devlog_path = output_path / "devlog.md"
    devlog_path.write_text(full_devlog, encoding="utf-8")
    if verbose:
        print(f"Built devlog: {devlog_path}")
    
    return {"devlog": str(devlog_path)}

def _generate_docx(devlog_md_path: str, output_path: str = None, verbose: bool = False) -> dict:
    """Convert devlog markdown to docx using our custom converter.
    
    Args:
        devlog_md_path: Path to devlog.md file
        output_path: Output path for docx file (defaults to devlog.docx in same dir as md)
        verbose: Print progress messages
    
    Returns:
        Dict with "docx" key pointing to docx path, or empty dict if conversion failed
    """
    if output_path is None:
        md_path = Path(devlog_md_path)
        output_path = str(md_path.parent / "devlog.docx")
    
    try:
        success = markdown_file_to_docx(str(devlog_md_path), str(output_path))
        if success:
            if verbose:
                print(f"Built docx: {output_path}")
            return {"docx": str(output_path)}
        else:
            if verbose:
                print(f"Warning: docx conversion failed")
            return {}
    except Exception as e:
        if verbose:
            error_type = type(e).__name__
            print(f"Warning: docx conversion failed ({error_type}): {e}")
        return {}

def _rebuild_index(
    output_folder: str,
    verbose: bool = False,
    changelog_order: bool = False,
    output_formats: list = None,
):
    """Rebuild the unified index with commits and tests interleaved by time.

    Args:
        output_folder: Base output folder containing commits/ and tests/
        verbose: Print progress messages
        changelog_order: If True, sort newest first. If False (default), oldest first
        output_formats: List of output formats (e.g., ["obsidian", "devlog", "docx"])
    """
    if output_formats is None:
        output_formats = ["obsidian"]
    
    results = {}
    
    if verbose:
        print(f"Rebuilding index with formats: {output_formats}")
    
    # Collect items
    items, commit_files, test_files = _collect_items(output_folder, changelog_order)
    
    # Generate obsidian index
    if "obsidian" in output_formats:
        results.update(_generate_obsidian_index(output_folder, items, verbose))
    
    # Generate devlog and/or docx
    if "devlog" in output_formats or "docx" in output_formats:
        devlog_result = _generate_devlog(output_folder, items, verbose)
        results.update(devlog_result)
        devlog_path = devlog_result.get("devlog")
        
        if "docx" in output_formats and devlog_path:
            docx_result = _generate_docx(devlog_path, verbose=verbose)
            results.update(docx_result)
            
            # Clean up devlog.md if only docx was requested
            if "devlog" not in output_formats and docx_result:
                Path(devlog_path).unlink(missing_ok=True)
    
    return results
