# Using Lumpy Log with Obsidian

## Start an Obsidian Vault for you project

It's likely to be in the repo or a seperate onedrive etc. folder

### In the vault settings / Daily Notes

| Date format       | 2026-01-24     |
| New file location | devlog/journal |

## Example .lumpyconfig.yml for Obsidian

```yaml
output_format:
  - obsidian
outputfolder: /absolute/path/to/your/Obsidian/vault/content/devlog/
# repo: /absolute/path/to/your/local/repo
```

## How to Open in Obsidian

1. Run lumpy-log to generate logs and index in your vault folder:
   ```bash
  lumpy-log
   ```
2. In Obsidian, open your vault and navigate to `devlog/index.md`.
3. All entries and index.md will be available and editable in Obsidian.
4. To open today's daily note / journal entry, either:
   * Click Open today's daily note in the ribbon.
   * Run Open today's daily note from the Command palette.

## Reminder

- Unless you use `--force`, Lumpy Log will not overwrite existing files. This means you can safely edit journal files (especially day pages) directly in Obsidian.
- You will need to run `lumpy-log rebuild` occaisionally to keep `index.md` upto date