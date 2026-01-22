"""Configuration handling for lumpy_log output formats."""

import os
import yaml
from pathlib import Path

DEFAULT_OUTPUT_FORMAT = "obsidian"
VALID_FORMATS = {"obsidian", "devlog", "docx"}

def _load_config_file(repo_path: str = ".") -> dict:
    """Load .lumpyconfig.yml from repo_path if present."""
    config_file = Path(repo_path) / ".lumpyconfig.yml"
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: could not read {config_file}: {e}")
            return {}
    return {}

def get_output_format(args: dict, repo_path: str = ".") -> list:
    """Determine output format(s) from CLI args and config file.
    
    Args:
        args: CLI arguments dict
        repo_path: Repository path for config file lookup
        
    Returns:
        List of output formats: ["obsidian"], ["devlog"], ["docx"], or combinations
    """
    # Load config file
    config = _load_config_file(repo_path)
    config_formats = config.get("output_format", DEFAULT_OUTPUT_FORMAT)
    if isinstance(config_formats, str):
        config_formats = [config_formats]
    
    # CLI args override config
    if args.get("output_format"):
        cli_formats = args["output_format"]
        if isinstance(cli_formats, str):
            cli_formats = [cli_formats]
        return [f for f in cli_formats if f in VALID_FORMATS] or [DEFAULT_OUTPUT_FORMAT]
    
    return [f for f in config_formats if f in VALID_FORMATS] or [DEFAULT_OUTPUT_FORMAT]
