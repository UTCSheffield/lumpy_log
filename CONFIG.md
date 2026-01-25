# Configuration File

Lumpy Log supports configuration via a `.lumpyconfig.yml` file in your repository root.

## Quick Start

Create a `.lumpyconfig.yml` file:

```yaml
# Output format(s)
output_format:
  - obsidian
  - docx

# Enable verbose output
verbose: true

# Limit to recent entries (optional)
limit: 10
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
| `obsidian_index` | boolean | `true` | Generate Obsidian-style index.md |
| `devlog` | boolean | `false` | Generate combined devlog.md |
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

See [HCTI_SETUP.md](HCTI_SETUP.md) for more information.

## Example Configurations

### Minimal (defaults)
```yaml
# Uses all defaults
output_format: obsidian
```

### Development Mode
```yaml
output_format: obsidian
verbose: true
limit: 5  # Only show 5 most recent entries
```

### Full Documentation
```yaml
output_format:
  - obsidian
  - devlog
  - docx
verbose: true
changelog: false  # oldest first
hcti_api_user_id: "your-id"
hcti_api_key: "your-key"
```

## Notes

- All settings are optional
- Boolean values: `true` or `false` (lowercase)
- The config file is read from the repository root (current directory by default)
- Invalid or unrecognized options are silently ignored
