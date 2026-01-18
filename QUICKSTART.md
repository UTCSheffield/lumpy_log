# Lumpy Log - Quick Start

## Installation

```bash
# For development
pip install -e .

# For users (when published to PyPI)
pip install lumpy-log
```

## Usage

### Git Commit Logs

```bash
# Basic usage - process current directory
lumpy-log log

# Process specific repository
lumpy-log log -i /path/to/repo -o output

# With options
lumpy-log log -i /path/to/repo -o output --verbose --force

# Backwards compatible (defaults to log command)
lumpy-log -i /path/to/repo -o output
```

### Test Results

```bash
# Process pytest TAP output
pytest --tap | lumpy-log test

# With raw output included
pytest --tap | lumpy-log test --raw-output

# From file
lumpy-log test --input test_output.txt
```

### Rebuild Index

```bash
# Rebuild index from existing commits and tests
lumpy-log rebuild

# Rebuild with changelog order (newest first)
lumpy-log rebuild --changelog
```

## As Python Module

```bash
python -m lumpy_log -i /path/to/repo -o output
```

## Quick Options

### Log Command (Git Commits)

- `-i, --repo`: Path to the local Git repository (default: current directory)
- `-o, --outputfolder`: Output folder for generated files (default: output)
- `-f, --fromcommit`: Start from this commit
- `-t, --tocommit`: End at this commit
- `-a, --allbranches`: Include all branches
- `-v, --verbose`: Verbose output
- `-b, --branch`: Specific branch to process
- `--force`: Force overwrite existing files
- `-d, --dryrun`: Dry run - don't write files
- `-n, --no-obsidian-index`: Don't generate index.md

### Test Command

- `-o, --outputfolder`: Output folder for test results (default: output)
- `--input`: Input file with test output (reads from stdin if not specified)
- `-v, --verbose`: Verbose output
- `--raw-output`: Include raw test output in the report

### Rebuild Command

- `-o, --outputfolder`: Output folder containing commits/ and tests/ (default: output)
- `-v, --verbose`: Verbose output
- `--changelog`: Use changelog order (newest first) instead of default (oldest first)

## Obsidian Integration

Automatically generates `index.md` with embedded commits using `![[filename]]` syntax.
Perfect for viewing all commits in a single Obsidian note!

## Publishing to PyPI

```bash
# Install tools
pip install build twine

# Build
python -m build

# Upload to Test PyPI (test first!)
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Files

- **README.md** - User documentation
- **DEVELOPMENT.md** - Developer guide  
- **PUBLISHING.md** - PyPI publishing guide
- **test_install.sh** - Test script

## Package Structure

- `lumpy_log/` - Main package
  - `cli.py` - Command-line interface
  - `core.py` - Core functionality
  - `changelump.py` - Change analysis
  - `languages.py` - Language support
  - `templates/` - Handlebars templates
