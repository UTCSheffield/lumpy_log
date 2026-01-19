# Publishing to PyPI

This guide walks you through publishing `lumpy-log` to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on both [Test PyPI](https://test.pypi.org/account/register/) and [PyPI](https://pypi.org/account/register/)

2. **API Tokens**: Generate API tokens for authentication:
   - [Test PyPI tokens](https://test.pypi.org/manage/account/token/)
   - [PyPI tokens](https://pypi.org/manage/account/token/)

3. **Install build tools**:
   ```bash
   pip install --upgrade build twine
   ```

## Building the Package

1. **Clean previous builds** (if any):
   ```bash
   rm -rf dist/ build/ *.egg-info/
   ```

2. **Build the package**:
   ```bash
   python -m build
   ```

   This creates two files in the `dist/` directory:
   - `lumpy_log-0.1.0.tar.gz` (source distribution)
   - `lumpy_log-0.1.0-py3-none-any.whl` (wheel distribution)

## Testing on Test PyPI (Recommended First Step)

1. **Upload to Test PyPI**:
   ```bash
   twine upload --repository testpypi dist/*
   ```

   When prompted, enter:
   - Username: `__token__`
   - Password: Your Test PyPI API token (including the `pypi-` prefix)

2. **Test installation from Test PyPI**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ lumpy-log --no-cache-dir
   ```

3. **Verify it works**:
   ```bash
   lumpy-log --help
   ```

## Publishing to PyPI

Once you've verified everything works on Test PyPI:

1. **Upload to PyPI**:
   ```bash
   twine upload dist/*
   ```

   When prompted, enter:
   - Username: `__token__`
   - Password: Your PyPI API token (including the `pypi-` prefix)

2. **Verify on PyPI**: Visit https://pypi.org/project/lumpy-log/

3. **Test installation**:
   ```bash
   pip install lumpy-log
   ```

## Using GitHub Actions (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Then add your PyPI API token as a repository secret named `PYPI_API_TOKEN`.

## Version Updates

To release a new version:

1. Update version in `pyproject.toml`
2. Update version in `lumpy_log/__init__.py`
3. Commit changes
4. Create a new git tag:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```
5. Rebuild and republish following the steps above

## Troubleshooting

### "Package already exists" error
- You cannot replace an existing version on PyPI
- Increment the version number in `pyproject.toml` and rebuild

### Import errors after installation
- Ensure all package data is included in `MANIFEST.in`
- Check `[tool.setuptools.package-data]` in `pyproject.toml`

### Missing dependencies
- Verify all dependencies are listed in `pyproject.toml`
- Test in a clean virtual environment
