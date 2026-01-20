import os
import re
try:
    import mdformat
except ImportError:
    mdformat = None

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
