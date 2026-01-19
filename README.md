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


## Building for PyPI

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI (requires credentials)
twine upload dist/*
```

# Lumpy Log

## Running Tests

To run the tests, use the following command:

```bash
pytest
```