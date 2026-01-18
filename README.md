# Lumpy Log - Prettified Git Logs

Make git logs easier for use in scenarios when communicating the progress of a project to non-experts.

## Features

- Generates readable markdown reports from Git commit history

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

```bash
# Process current directory repository
lumpy-log

# Process a specific repository
lumpy-log -i /path/to/repo -o /path/to/output

# Process with options
lumpy-log -i /path/to/repo -o output --verbose --force
```

### As a Python Module

You can also run it as a module:

```bash
python -m lumpy_log -i /path/to/repo -o output
```

### Command-line Options

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