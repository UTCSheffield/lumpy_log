# Configuration File

Lumpy Log supports configuration via a `.lumpyconfig.yml` file in your repository root.

## Quick Start

Create a `.lumpyconfig.yml` file:

```yaml
# Output format(s)
output_format:
  - obsidian
  # - devlog
  # - docx

# Enable verbose output
verbose: true

# Limit to recent entries (optional)
# limit: 10
```

## Available Options

See [.lumpyconfig.yml.example](.lumpyconfig.yml.example) for a complete list of all available configuration options with documentation.

### Key Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `output_format` | string or list | `obsidian` | Output format(s): `obsidian`, `devlog`, `docx` |
| `outputfolder` | string | `devlog` | Output folder for generated files |
| `verbose` | boolean | `false` | Enable verbose output |
| `limit` | integer | none | Limit to N most recent entries |
| `changelog` | boolean | `false` | Use changelog order (newest first) |
| `hcti_api_user_id` | string | none | HCTI API User ID for code-as-images |
| `hcti_api_key` | string | none | HCTI API Key for code-as-images |

## Priority

Configuration values are resolved in this order:
1. **CLI arguments** (highest priority)
2. **Environment variables** (for HCTI credentials)
3. **Config file** (`.lumpyconfig.yml`)
4. **Defaults** (lowest priority)

This means CLI flags always override config file settings.

## HCTI Credentials

For code-as-images in DOCX files, you can configure HCTI API credentials in three ways:

1. **Environment variables** (highest priority):
   ```bash
   export HCTI_API_USER_ID="your-user-id"
   export HCTI_API_KEY="your-api-key"
   ```

2. **Config file**:
   ```yaml
   hcti_api_user_id: "your-user-id"
   hcti_api_key: "your-api-key"
   ```

3. **Not set** (falls back to text rendering)

See [CODE_AS_IMAGE.md](CODE_AS_IMAGE.md) for more information.

## Output Format

You can choose the output format(s) for your dev log:

- `obsidian`: Unified index.md for Obsidian (default)
- `devlog`: Combined devlog.md with all entries
- `docx`: Combined devlog.docx with all entries

Example config:

```yaml
output_format:
  - obsidian
  # - devlog
  # - docx
```

## Code Block Images in DOCX

To enable code block image rendering in DOCX output (for syntax highlighting and advanced formatting):

- Install Playwright:

  ```bash
  pip install lumpy-log[docx-playwright]
  playwright install chromium
  ```

- Optionally configure HCTI API credentials for cloud rendering, or use Playwright for local rendering.
- See [CODE_AS_IMAGE.md](CODE_AS_IMAGE.md) for full setup and usage instructions.

## Example Configurations

### Minimal (defaults)

```yaml
output_format: obsidian
```

### Development Mode

```yaml
  - obsidian
  - devlog
  - docx
verbose: true
limit: 10  # Only process the 10 most recent entries
```

### Full Docx with code as images

```yaml
output_format:
  - docx
verbose: true
changelog: false  # oldest first
render_code_as_images: true
hcti_api_user_id: "your-id"
hcti_api_key: "your-key"
```

## Notes

- All settings are optional
- Boolean values: `true` or `false` (lowercase)
- The config file is read from the repository root (current directory by default)
- Invalid or unrecognized options are silently ignored
