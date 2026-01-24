# Lumpy Log - Prettified Git Logs

Make git logs easier for use in scenarios when communicating the progress of a project to non-experts.

## Features

- Generates readable markdown reports from Git commit history
- Processes test output (TAP format) and creates test documentation
- Multi-folder organization with unified index

📚 **See Also:**
- [Obsidian Integration Guide](OBSIDIAN.md) - Detailed guide for using with Obsidian
- [Development Guide](DEVELOPMENT.md) - For contributors and developers
- [Publishing Guide](PUBLISHING.md) - How to publish to PyPI
- [Quick Start](QUICKSTART.md) - Quick reference

## Installation

### From PyPI (when published)

```bash
pip install lumpy-log
```

### For Development

```bash
# Clone the repository
git clone https://github.com/UTCSheffield/lumpy_log.git
cd lumpy_log

# Install in editable mode
pip install -e .
```

### Optional: DOCX code blocks as images (no API)

To enable local image rendering for code blocks in DOCX (Playwright fallback):

```bash
pip install "lumpy-log[docx-images]"
playwright install chromium  # or firefox/webkit; export LUMPY_PLAYWRIGHT_BROWSER=firefox
```

If you prefer API-based rendering, see [HCTI_SETUP.md](HCTI_SETUP.md).

## Usage

### As a CLI Command

After installation, you can use the `lumpy-log` command:

#### Generate Git Commit Logs

```bash
# Process current directory repository
lumpy-log log

# Process a specific repository
lumpy-log log -i /path/to/repo

# Process with options
lumpy-log log -i /path/to/repo -o devlog --verbose --force

# Backwards compatible (defaults to log command)
lumpy-log -i /path/to/repo
```

#### Process Test Results

Lumpy Log can process test output in TAP (Test Anything Protocol) format and create markdown documentation alongside your commit logs.

**Install pytest-tap plugin:**

```bash
pip install pytest-tap
```

**Bash/Linux/macOS:**

```bash
# Pipe test output directly
pytest --tap | lumpy-log test

# Or save to file first
pytest --tap > test_output.txt
lumpy-log test --input test_output.txt
```

**Windows cmd.exe or PowerShell:**

```cmd
REM Pipe test output directly
py -m pytest --tap | lumpy-log test

REM Or save to file first
py -m pytest --tap > test_output.txt
lumpy-log test --input test_output.txt

REM Include raw output for debugging
py -m pytest --tap | lumpy-log test --raw-output
```

Test results are saved to `output/tests/` with timestamp filenames (e.g., `20260118_1430.md`), and the index is automatically updated to include both commits and test results.

#### Rebuild Index

If you manually modify or reorganize commit/test files, you can regenerate the index:

```bash
# Rebuild with default order (oldest first - development log style)
lumpy-log rebuild

# Rebuild with changelog order (newest first)
lumpy-log rebuild --changelog
```

### As a Python Module

You can also run it as a module:

```bash
python -m lumpy_log -i /path/to/repo -o output
```

### Command-line Options

#### Log Command (Git Commits)

- `-i, --repo`: Path to the local Git repository (default: current directory)
- `-o, --outputfolder`: Output folder for generated files (default: devlog)
- `-f, --fromcommit`: Start from this commit
- `-t, --tocommit`: End at this commit
- `-a, --allbranches`: Include all branches
- `-v, --verbose`: Verbose output
- `-b, --branch`: Specific branch to process
- `--force`: Force overwrite existing files
- `-d, --dryrun`: Dry run - don't write files
- `-n, --no-obsidian-index`: Don't generate index.md

#### Test Command (Test Results)

- `-o, --outputfolder`: Output folder for test results (default: devlog)
- `--input`: Input file with test output (if not specified, reads from stdin)
- `-v, --verbose`: Verbose output
- `--raw-output`: Include raw test output in the report

#### Rebuild Command (Regenerate Index)

Rebuilds the unified `index.md` from existing commits and test results without re-processing git history or re-running tests.

```bash
# Rebuild index with default order (oldest first)
lumpy-log rebuild

# Rebuild with changelog order (newest first)
lumpy-log rebuild --changelog

# Rebuild from custom output folder
lumpy-log rebuild -o /path/to/output
```

- `-o, --outputfolder`: Output folder containing commits/ and tests/ (default: devlog)
- `-v, --verbose`: Verbose output
- `--changelog`: Use changelog order (newest first) instead of default (oldest first)

### Output Structure

Lumpy Log organizes output into subdirectories:

```
devlog/
├── index.md              # Unified index with commits and test results
├── commits/              # Git commit markdown files
│   ├── 20260118_1430_abc1234.md
│   └── 20260118_1500_def5678.md
└── tests/                # Test result markdown files
    ├── 20260118_1430.md
    └── 20260118_1500.md
```

### Ignoring Files (.lumpyignore)

Lumpy Log respects a repository-level `.lumpyignore` file using the same syntax as `.gitignore` (git wildmatch patterns). By default, it ignores Markdown files (`*.md`) so documentation changes don't flood the logs. Add additional patterns to `.lumpyignore` at your repo root to skip files or folders.

Example `.lumpyignore`:

```
# Ignore Markdown (default)
*.md

# Ignore generated docs and build artifacts
docs/
dist/
*.tmp
```

### Running Tests

To run the tests, use the following command:

```bash
pytest
```


# Example Output

## Commit : Refactor verbose logging conditions in ChangeLump methods for clarity

By "Mr Eggleton" on 2026-01-18


### "changelump.py" was Modified



```python
    # Abstracts out lineIsComment so we can  print the results
    def _lineIsComment(self, i):
        line = self.lines[i]
        if(self.verbose):
            print(self.lang.name, "self.lang.comment_structure",self.lang.comment_structure)
        comment_structure = self.lang.comment_structure

        begin = comment_structure.get("begin")
        end = comment_structure.get("end")
        single = comment_structure.get("single")

        # Multiline comments: treat lines with both begin and end as comment,
        # and any line inside unmatched begin/end pairs as comment.
        if begin:
            try:
                beginmatches = re.findall(begin, line)
                endmatches = re.findall(end, line)

                # If both markers appear on the same line, it's a comment line.
                if len(beginmatches) and len(endmatches):
                    return True
                
                # If this line is inside an open multiline comment, it's a comment.
                if self._in_multiline_comment(i, begin, end):
                    return True
            except Exception as Err:
                print(type(Err), Err)
                print(self.lang.comment_family, comment_structure)

        # Single-line comments
        if single:
            try:
                if re.search(single, line.strip()):
                    return True
            except Exception as Err:
                print("Single", type(Err), Err)
                print(self.lang.comment_family, comment_structure["single"])

        return False

```



```python
    @property
    def code(self):    
        start = self.start 
        if(self.commentStart is not None):
            start = self.commentStart     

        #code = ""self.source+"\n"+
        code = ("\n".join(self.lines[start: self.end+1]))
        if self.verbose:
            print("code", code)
        return code
```



```python
    def extendOverComments(self):
        if self.verbose:
            print("extendOverComments", "self.start", self.start)
        j = self.start
        while(j > 0 and self.lineIsComment(j-1)):
            j -= 1
            self.commentStart = j
```



```python
    def lineIsComment(self, i):
        blineIsComment = self._lineIsComment(i)
        if self.verbose:
            print("lineIsComment", blineIsComment, self.lines[i])
        return blineIsComment
```



```python
    def inLump(self,i):
        inLump = (self.start <= i and i <= self.end)
    
        if self.verbose:
            print("inLump", "self.start", self.start,"i", i, "inLump",inLump)
        return inLump
```



```python
        """Return True if line i is inside an unmatched multiline comment block."""
        try:
            # Check if begin and end delimiters are the same (symmetric like """)
            # Strip common regex anchors to compare the actual delimiter strings
            begin_stripped = begin_re.strip('^$\\s')
            end_stripped = end_re.strip('^$\\s')
            symmetric = (begin_stripped == end_stripped)
            
            in_comment = False
            for idx in range(0, i + 1):
                s = self.lines[idx]
                
                if symmetric:
                    # For symmetric delimiters (like """ in Python), each occurrence
                    # toggles the comment state: first one opens, second one closes, etc.
                    # Example: """comment""" means we enter on first """, exit on second
                    matches = re.findall(begin_re, s)
                    for _ in matches:
                        in_comment = not in_comment  # Flip True->False or False->True
                else:
                    # For asymmetric delimiters, track depth
                    begins = len(re.findall(begin_re, s))
                    ends = len(re.findall(end_re, s))
                    
                    # Process begins first, then ends
                    if not in_comment and begins > 0:
                        in_comment = True
                    if in_comment and ends > 0:
                        in_comment = False
                    
            
            return in_comment
        except Exception as Err:
            if self.verbose:
                print("_in_multiline_comment error", type(Err), Err)
            return False

```

## Test Results : 2026-01-20 13:30:12
**Format:** tap


- **Tests Run:** 113
- **Passed:** 113 ✅
- **Failed:** 0 
- **Skipped:** 0 

