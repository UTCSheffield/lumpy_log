#!/usr/bin/env python
"""Quick test of the new markdown to docx converter."""

import tempfile
from pathlib import Path
from lumpy_log.md_to_docx import markdown_file_to_docx, markdown_to_docx

def test_basic():
    """Test basic conversion."""
    print("Testing basic conversion...")
    markdown = "# Test\n\nThis is a test."
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "test.docx"
        result = markdown_to_docx(markdown, str(output))
        print(f"  Result: {result}")
        print(f"  File exists: {output.exists()}")
        if output.exists():
            print(f"  File size: {output.stat().st_size} bytes")
        return result and output.exists()

def test_complex():
    """Test complex markdown."""
    print("\nTesting complex markdown...")
    markdown = """# Development Log

Generated: 2024-01-15
Items: 2 (1 commits, 1 tests)

## Commit One

This is a **commit** with *important* details.

```python
def hello():
    print("world")
```

---

## Test Entry

- Test 1: Passed
- Test 2: Passed
- Test 3: Needs review"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "complex.docx"
        result = markdown_to_docx(markdown, str(output))
        print(f"  Result: {result}")
        print(f"  File exists: {output.exists()}")
        if output.exists():
            print(f"  File size: {output.stat().st_size} bytes")
        return result and output.exists()

def test_file():
    """Test file-based conversion."""
    print("\nTesting file conversion...")
    with tempfile.TemporaryDirectory() as tmpdir:
        md_file = Path(tmpdir) / "test.md"
        md_file.write_text("# File Test\n\nContent from file.")
        
        result = markdown_file_to_docx(str(md_file))
        docx_file = md_file.with_suffix(".docx")
        
        print(f"  Result: {result}")
        print(f"  Input: {md_file}")
        print(f"  Output exists: {docx_file.exists()}")
        if docx_file.exists():
            print(f"  Output size: {docx_file.stat().st_size} bytes")
        return result and docx_file.exists()

if __name__ == "__main__":
    print("Running markdown to docx converter tests...\n")
    
    try:
        test1 = test_basic()
        test2 = test_complex()
        test3 = test_file()
        
        print("\n" + "=" * 50)
        print(f"Results:")
        print(f"  Basic conversion: {'✓ PASS' if test1 else '✗ FAIL'}")
        print(f"  Complex markdown: {'✓ PASS' if test2 else '✗ FAIL'}")
        print(f"  File conversion:  {'✓ PASS' if test3 else '✗ FAIL'}")
        print(f"\nOverall: {'✓ ALL TESTS PASSED' if all([test1, test2, test3]) else '✗ SOME TESTS FAILED'}")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
