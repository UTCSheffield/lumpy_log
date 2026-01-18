# Obsidian Integration Example

## What Gets Generated

When you run `lumpy-log`, it creates:

1. **Individual commit files** - One `.md` file per commit in `commits/` folder
   - Format: `YYYYMMDD_HHMM_hash.md`
   - Example: `20220601_0722_be146ce.md`

2. **Test result files** - One `.md` file per test run in `tests/` folder
   - Format: `YYYYMMDD_HHMM.md`
   - Example: `20260118_1430.md`

3. **Unified index file** - `index.md` that links all commits and test results in chronological order

## Example Output Structure

```
output/
├── index.md                          # Unified index with commits and tests
├── commits/                          # Git commit logs
│   ├── 20220601_0723_d5c3a9d.md
│   ├── 20220601_0722_be146ce.md
│   └── 20220531_2251_709aa7d.md
└── tests/                            # Test results
    ├── 20260118_1430.md
    └── 20260118_1500.md
```

## The index.md File

The generated `index.md` provides a unified view of both commits and test results:

```markdown
# Development Log

**Generated:** 2026-01-18 14:30:00

---

## Summary

- **Total Items:** 30
- **Commits:** 27
- **Test Results:** 3

---

## Timeline

### [[commits/20220601_0723_d5c3a9d|Commit 20220601_0723]]

### [[tests/20260118_1430|Tests 20260118_1430]]

### [[commits/20220601_0722_be146ce|Commit 20220601_0722]]

... (continues in chronological order)
```

## Using in Obsidian

### Setup

1. **Generate logs into your Obsidian vault:**
   ```bash
   lumpy-log -i /path/to/repo -o ~/MyVault/project-logs
   ```

2. **Open in Obsidian:**
   - Navigate to `project-logs/index.md`
   - All commits are embedded and fully rendered
   - Click any embedded note to jump to that specific commit

### Benefits

- **Unified Timeline**: See both code commits and test results in chronological order
- **Development Log**: Track progress with both feature development and quality verification
- **Navigation**: Jump between commits and test results easily
- **Linking**: Create links to specific commits or test runs from other notes
- **Searching**: Obsidian search works across all content
- **Tagging**: Add your own tags and notes in the index

### Example Workflow

```bash
# Initial setup - generate logs for your project
lumpy-log log -i ~/projects/myapp -o ~/Vault/myapp-logs

# Run and document tests
pytest --tap | lumpy-log test -o ~/Vault/myapp-logs

# Update logs after new commits
lumpy-log log -i ~/projects/myapp -o ~/Vault/myapp-logs --force

# Rebuild index if needed
lumpy-log rebuild -o ~/Vault/myapp-logs

# Generate with changelog order (newest first)
lumpy-log rebuild -o ~/Vault/myapp-logs --changelog
```

### Customization

Edit `lumpy_log/templates/obsidian_index.md` to customize the index format. The template receives:

- `generation_date` - Timestamp of index generation
- `repo_path` - Repository path (for log command)
- `items` - List of all commits and test results with type markers
- `total_items` - Total count of items
- `total_commits` - Count of commits
- `total_tests` - Count of test results

You can add:
- Custom headers and sections
- Grouping by date or type
- Filtering logic
- Additional metadata
- Custom styling with CSS snippets

## Without Obsidian

If you're not using Obsidian, disable index generation:

```bash
lumpy-log log --no-obsidian-index
```

The individual commit and test files are still useful as standalone markdown documents!
