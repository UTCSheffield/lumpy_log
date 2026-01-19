# Development Guide

## Setup Development Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/UTCSheffield/lumpy_log.git
   cd lumpy_log
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in editable mode**:
   ```bash
   pip install -e .
   ```

   This installs the package in "editable" mode, so changes to the code are immediately reflected without reinstalling.

## Project Structure

```
lumpy_log/
├── lumpy_log/              # Main package directory
│   ├── __init__.py        # Package initialization
│   ├── __main__.py        # Enables `python -m lumpy_log`
│   ├── cli.py             # Command-line interface with subcommands
│   ├── core.py            # Core git log processing
│   ├── test_processor.py  # Test result processing
│   ├── test_runner.py     # Test execution and reporting
│   ├── tap_parser.py      # TAP format parser
│   ├── changelump.py      # Change analysis
│   ├── languages.py       # Language definitions
│   ├── languages.yml      # Language configuration
│   └── templates/         # Jinja2 templates
│       ├── commit.md      # Commit header template
│       ├── modified_files.md  # Modified files template
│       ├── obsidian_index.md  # Unified index template
│       └── test_results.md    # Test results template
├── tests/                 # Unit tests
│   ├── test_changelump.py
│   └── test_tap_parser.py
├── output/                # Default output directory
│   ├── index.md          # Unified index
│   ├── commits/          # Git commit logs
│   └── tests/            # Test result logs
├── pyproject.toml         # Package configuration
├── pytest.ini             # Pytest configuration
├── MANIFEST.in            # Package data files
├── LICENSE                # MIT License
├── README.md              # User documentation
├── QUICKSTART.md          # Quick reference
├── OBSIDIAN.md            # Obsidian integration guide
├── DEVELOPMENT.md         # This file
├── PUBLISHING.md          # PyPI publishing guide
└── test_install.sh        # Installation test script
```

## Running During Development

### Git commit logs:
```bash
# Using the log command
lumpy-log log -i /path/to/repo -o devlog

# Backwards compatible (defaults to log)
lumpy-log -i /path/to/repo -o devlog
```

### Test results:
```bash
# Process test output
pytest --tap | lumpy-log test

# With raw output included
pytest --tap | lumpy-log test --raw-output
```

### Rebuild index:
```bash
# Rebuild from existing files
lumpy-log rebuild

# With changelog order (newest first)
lumpy-log rebuild --changelog
```

### As Python module:
```bash
python -m lumpy_log log -i /path/to/repo -o output
```

### Directly via Python:
```python
from lumpy_log.core import main

args = {
    'repo': '/path/to/repo',
    'outputfolder': 'devlog',
    'verbose': True,
    'dryrun': False,
    'force': False,
    'allbranches': False,
    'branch': None,
    'from_commit': None,
    'to_commit': None,
}
main(args)
```

## Testing Changes

1. **Run unit tests**:
   ```bash
   pytest
   
   # With verbose output
   pytest -v
   
   # Run specific test file
   pytest tests/test_tap_parser.py
   
   # With TAP output (dogfooding!)
   pytest --tap | lumpy-log test
   ```

2. **Quick functional test**:
   ```bash
   lumpy-log log -i . -o test_devlog --dryrun --verbose
   ```

3. **Full test with this repository**:
   ```bash
   lumpy-log log -i . -o test_devlog --verbose --force
   ```

4. **Run the test script**:
   ```bash
   chmod +x test_install.sh
   ./test_install.sh
   ```

## Making Changes

### Adding new features:

1. Make changes in `lumpy_log/` directory
2. Test with `lumpy-log` command
3. Update version in `pyproject.toml` and `lumpy_log/__init__.py`
4. Update documentation if needed

### Adding new CLI arguments:

1. Edit `lumpy_log/cli.py` to add the argument
2. Update `lumpy_log/core.py` to handle it
3. Update README.md with the new option

### Modifying templates:

Templates are in `lumpy_log/templates/` and use Jinja2 syntax (`.md` files).

**Jinja2 syntax examples:**
```jinja2
{{ variable }}                  {# Output variable #}
{% for item in list %}          {# Loop #}
  {{ item }}
{% endfor %}
{% if condition %}              {# Conditional #}
  {{ value }}
{% endif %}
```

**Available templates:**
- `commit.md` - Individual commit header
- `modified_files.md` - Modified file section within a commit
- `obsidian_index.md` - Unified index with commits and test results
- `test_results.md` - Test result report format

### Adding new languages:

Edit `lumpy_log/languages.yml` to add language definitions.

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

## Debugging

Enable verbose mode for detailed output:
```bash
lumpy-log -i . -o output --verbose
```

Or add print statements in the code (they'll show with `--verbose`).

## Building for Distribution

1. **Clean previous builds**:
   ```bash
   rm -rf dist/ build/ *.egg-info/
   ```

2. **Build**:
   ```bash
   pip install build
   python -m build
   ```

3. **Check the build**:
   ```bash
   twine check dist/*
   ```

## Common Issues

### "No module named lumpy_log"
- Reinstall in editable mode: `pip install -e .`
- Check you're in the right virtual environment

### "lumpy-log: command not found"
- Reinstall: `pip install -e .`
- Check your PATH includes pip's bin directory
- Try `python -m lumpy_log` instead

### Template/config files not found
- Check `MANIFEST.in` includes the files
- Reinstall: `pip install -e .`
- Verify paths in `core.py` use `_get_template_path()`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI](https://pypi.org/)
- [Setuptools Documentation](https://setuptools.pypa.io/)
