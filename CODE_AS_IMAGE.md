# Code-as-Images in DOCX

## Overview

By default, code blocks in DOCX output are rendered as text with syntax highlighting. However, you can optionally render them as images for better visual appearance.

## Setup Options

### Option 1: .lumpyconfig.yml (Recommended)

Add to your `.lumpyconfig.yml`:

```yaml
hcti_api_user_id: "your-user-id"
hcti_api_key: "your-api-key"
```

**Priority:** Environment variables take precedence over config file credentials.


### Option 2: Environment Variables (Highest Priority)

```bash
export HCTI_API_USER_ID="your-user-id"
export HCTI_API_KEY="your-api-key"
```

Or in Windows:
```cmd
set HCTI_API_USER_ID=your-user-id
set HCTI_API_KEY=your-api-key
```

### Option 3: Local Rendering (Free, No API Keys)

Use the built-in Playwright fallback to render code blocks locally. This is useful if you don't want to use the HCTI API or you run out of quota.

1) Install Playwright and a browser (Chromium by default). Easiest is to use the optional extras so it's tracked in your environment:

```bash
pip install "lumpy-log[docx-playwright]"
playwright install chromium
```

(Or if developing locally from source: `pip install -e .[docx-playwright]`)

2) (Optional) To use Firefox or WebKit instead of Chromium:

```bash
playwright install firefox   # or webkit
export LUMPY_PLAYWRIGHT_BROWSER=firefox  # or webkit
```

3) Run your command as normal (no API keys needed):

```bash
lumpy-log rebuild --output-format docx --verbose
```

The tool will automatically fall back to local rendering when HCTI credentials are not present or if the API fails. Cached images are still used when available.

## Getting Credentials

1. Sign up for a free account at [htmlcsstoimage.com](https://htmlcsstoimage.com/)
2. Get your API credentials (User ID and API Key)
3. Set them using Option 1 or Option 2 above

## Usage

Once credentials are configured, simply generate DOCX as normal:

```bash
lumpy-log rebuild --output-format docx --verbose
```

The tool will automatically detect the credentials and render code blocks as images.

## How It Works

1. Code blocks are converted to HTML with syntax highlighting (using highlight.js)
2. **Cache check:** If the same code block was rendered before, use the cached image
3. HTML is rendered to PNG images via the HCTI API (only if not cached)
4. Images are cached locally in `~/.lumpy_cache/code_images/` for future use
5. Images are embedded in the DOCX document
6. If credentials are not available or the request fails, it falls back to text rendering

### Caching Benefits

- **Drastically reduces API usage:** Identical code blocks are only rendered once
- **Faster generation:** Cached images are retrieved instantly
- **Stays within free tier limits:** 50 renders/month goes much further with caching
- Cache is stored in your home directory: `~/.lumpy_cache/code_images/`
- Cache is based on code content + language (SHA256 hash)

### Cache Management

To clear the cache:
```bash
rm -rf ~/.lumpy_cache/code_images/
```

The cache will automatically regenerate as needed.

## Free Tier Limits

The free tier includes:
- 50 images per month
- No credit card required
- Perfect for development and small projects

For larger projects, consider upgrading or using text rendering (which is free and unlimited).

## Fallback Behavior

If:
- Credentials are not set (neither environment nor config)
- API request fails
- Network is unavailable

The tool will automatically fall back to text-based code rendering with syntax highlighting.

