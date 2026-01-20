#!/usr/bin/python3
"""Process test output and generate markdown documentation."""

import sys
import os
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .tap_parser import parse_test_output
from .utils import _clean_markdown, _get_templates_dir, _format_markdown
class TestProcessor:
    """Process test output and generate markdown files"""
    
    def __init__(self, output_folder: str = "output"):
        self.output_folder = Path(output_folder)
        self.tests_dir = self.output_folder / "tests"
        
        # Set up Jinja2 environment
        self.jinja_env = Environment(loader=FileSystemLoader(_get_templates_dir()))
    
    def setup_directories(self):
        """Create necessary directory structure"""
        self.tests_dir.mkdir(parents=True, exist_ok=True)
    
    def read_input(self, input_file: str = None) -> str:
        """
        Read test output from file or stdin
        
        Args:
            input_file: Path to file, or None to read from stdin
            
        Returns:
            Test output as string
            
        Raises:
            ValueError: If stdin is empty and no file provided
        """
        if input_file:
            with open(input_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # Read from stdin
            if sys.stdin.isatty():
                raise ValueError(
                    "No input provided. Either pipe test output or use --input <file>.\n"
                    "Example: pytest --tap | lumpy-log test"
                )
            
            content = sys.stdin.read()
            if not content or not content.strip():
                raise ValueError(
                    "Empty input received. Please provide test output via pipe or file."
                )
            
            return content
    
    def generate_filename(self) -> str:
        """Generate timestamped filename for test results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        return f"{timestamp}.md"
    
    def process_test_output(
        self,
        output: str,
        verbose: bool = False,
        raw_output: bool = False,
        build_devlog: bool = False,
    ) -> Path:
        """
        Process test output and generate markdown file
        
        Args:
            output: Test output string
            verbose: Print progress messages
            raw_output: Include raw output in the markdown report
            
        Returns:
            Path to generated markdown file
        """
        # Parse test output
        test_data = parse_test_output(output)
        
        # Add metadata
        test_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_data['generation_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Only include raw output if explicitly requested
        if raw_output:
            test_data['raw_output'] = output
        
        # Load template and render
        template = self.jinja_env.get_template("test_results.md")
        markdown_content = template.render(test_data)
        
        # Generate filename and save
        filename = self.generate_filename()
        filepath = self.tests_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(_format_markdown(markdown_content))
        
        if verbose:
            print(f"Test results saved to: {filepath}")
            if test_data['format'] == 'tap':
                print(f"  Tests run: {test_data['tests_run']}")
                print(f"  Passed: {test_data['tests_passed']}")
                print(f"  Failed: {test_data['tests_failed']}")
                print(f"  Skipped: {test_data['tests_skipped']}")
        
        # Rebuild index to include new test results
        self._rebuild_index(verbose, build_devlog=build_devlog)
        
        return filepath
    
    def _rebuild_index(
        self,
        verbose: bool = False,
        changelog_order: bool = False,
        build_devlog: bool = False,
        write_index: bool = True,
    ):
        """Rebuild the unified index with commits and tests interleaved by time.

        Args:
            verbose: Print progress messages
            changelog_order: If True, sort newest first (changelog style). If False (default), oldest first
            build_devlog: When True, also emit a combined devlog.md containing the full contents
                of each commit and test entry in the chosen order.
            write_index: When False, skip writing index.md (used when only devlog is requested).
        """
        # Collect commit files
        commits_dir = self.output_folder / "commits"
        commit_files = []
        if commits_dir.exists():
            commit_files = sorted(commits_dir.glob("*.md"))
        
        # Collect test files
        test_files = []
        if self.tests_dir.exists():
            test_files = sorted(self.tests_dir.glob("*.md"))
        
        # Create combined list with type markers
        items = []
        for f in commit_files:
            items.append({"path": f"commits/{f.name}", "name": f.stem, "type": "commit", "filename": f.name})
        for f in test_files:
            items.append({"path": f"tests/{f.name}", "name": f.stem, "type": "test", "filename": f.name})
        
        # Sort by filename (which includes timestamp)
        # Default (changelog_order=False): oldest first
        # If changelog_order=True: newest first
        items.sort(key=lambda x: x['filename'], reverse=changelog_order)
        
        index_path = self.output_folder / "index.md"
        if write_index:
            template = self.jinja_env.get_template("obsidian_index.md")
            index_content = _clean_markdown(template.render({
                "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "repo_path": ".",
                "items": items,
                "total_items": len(items),
                "total_commits": len(commit_files),
                "total_tests": len(test_files)
            }))

            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(index_content)

            if verbose:
                print(f"Updated index: {index_path}")
                print(f"Order: {'Changelog (newest first)' if changelog_order else 'Development log (oldest first)'}")
        elif verbose:
            print("Index generation skipped (obsidian index disabled)")
        
        if build_devlog:
            devlog_path = self.output_folder / "devlog.md"
            header_lines = [
                "# Devlog",
                "",
                datetime.now().strftime("Generated: %Y-%m-%d %H:%M:%S"),
                f"Items: {len(items)} ({len(commit_files)} commits, {len(test_files)} tests)",
                "",
            ]

            segments = []
            for item in items:
                entry_path = self.output_folder / item["path"]
                try:
                    entry_text = entry_path.read_text(encoding="utf-8").strip()
                except FileNotFoundError:
                    if verbose:
                        print(f"Missing item skipped in devlog: {entry_path}")
                    continue
                segments.append(entry_text)

            devlog_body = "\n\n".join(segments)
            devlog_content_parts = header_lines.copy()
            if devlog_body:
                devlog_content_parts.append(devlog_body)
            devlog_path.write_text(_clean_markdown("\n".join(devlog_content_parts)), encoding="utf-8")

            if verbose:
                print(f"Built devlog: {devlog_path}")

        if verbose and not write_index:
            print(f"Order: {'Changelog (newest first)' if changelog_order else 'Development log (oldest first)'}")



def main(args: dict) -> int:
    """
    Main entry point for test processing
    
    Args:
        args: Dictionary of CLI arguments
    """
    processor = TestProcessor(args.get('outputfolder', 'output'))
    processor.setup_directories()
    
    try:
        # Read input
        output = processor.read_input(args.get('input'))
        
        # Process and generate markdown
        raw_output = bool(args.get("raw_output", False))
        filepath = processor.process_test_output(
            output, 
            verbose=args.get('verbose', False),
            raw_output=raw_output,
            build_devlog=args.get("devlog", False),
        )
        
        if not args.get('verbose'):
            print(f"Test results saved to: {filepath}")
        
        return 0
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error processing test output: {e}", file=sys.stderr)
        if args.get('verbose'):
            import traceback
            traceback.print_exc()
        return 1
