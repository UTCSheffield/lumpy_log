"""Command-line interface for Lumpy Log"""
import argparse
import sys
from .core import main as core_main
from .test_processor import main as test_main, TestProcessor


def rebuild_main(args):
    """Rebuild index from existing commits and test results"""
    processor = TestProcessor(args.get('outputfolder', 'devlog'))
    try:
        processor._rebuild_index(
            verbose=args.get('verbose', False),
            changelog_order=args.get('changelog', False),
            build_devlog=args.get('devlog', False)
        )
        if not args.get('verbose'):
            base = args.get('outputfolder', 'devlog')
            message = f"Index rebuilt: {base}/index.md"
            if args.get('devlog', False):
                message += f" and {base}/devlog.md"
            print(message)
        return 0
    except Exception as e:
        print(f"Error rebuilding index: {e}", file=sys.stderr)
        if args.get('verbose'):
            import traceback
            traceback.print_exc()
        return 1


def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        prog='lumpy-log',
        description='Make git logs easier for use in scenarios when communicating the progress of a project to non-experts.',
        epilog='Use "lumpy-log <command> --help" for more information about a command.'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Log command (processes git commits)
    log_parser = subparsers.add_parser('log', help='Generate git commit logs (default if no command specified)')
    log_parser.add_argument(
        "-i", "--repo",
        default='.',
        help="Path to the local Git repository (default: current directory)"
    )
    log_parser.add_argument(
        "-o", "--outputfolder",
        default="devlog",
        help="Output folder for generated files (default: devlog)"
    )
    log_parser.add_argument(
        "-f", "--fromcommit",
        dest="from_commit",
        help="Start from this commit"
    )
    log_parser.add_argument(
        "-t", "--tocommit",
        dest="to_commit",
        help="End at this commit"
    )
    log_parser.add_argument(
        "-a", "--allbranches",
        action="store_true",
        help="Include all branches"
    )
    log_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    log_parser.add_argument(
        "-b", "--branch",
        dest="branch",
        help="Specific branch to process"
    )
    log_parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing files"
    )
    log_parser.add_argument(
        "-d", "--dryrun",
        action="store_true",
        help="Dry run - don't write files"
    )
    log_parser.add_argument(
        "-n", "--no-obsidian-index",
        dest="obsidian_index",
        action="store_false",
        help="Don't generate Obsidian-style index.md file",
    )
    log_parser.set_defaults(obsidian_index=True)

    log_parser.add_argument(
        "--devlog",
        action="store_true",
        help="Generate a combined devlog.md with all commit and test content",
    )
    
    # Test command (processes test output)
    test_parser = subparsers.add_parser(
        'test', 
        help='Process test output and generate markdown',
        description='Process test output (TAP format or raw text) and generate markdown documentation.',
        epilog='''
Examples:
  Bash/Linux/macOS:
    pytest --tap | lumpy-log test
    pytest --tap > results.txt && lumpy-log test --input results.txt
  
  Windows (cmd/PowerShell):
    py -m pytest --tap | lumpy-log test
    py -m pytest --tap > results.txt
    lumpy-log test --input results.txt
  
Note: Requires pytest-tap plugin (pip install pytest-tap)
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    test_parser.add_argument(
        "-o", "--outputfolder",
        default="devlog",
        help="Output folder for test results (default: devlog)"
    )
    test_parser.add_argument(
        "--input",
        help="Input file with test output (if not specified, reads from stdin)"
    )
    test_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    test_parser.add_argument(
        "--raw-output",
        action="store_true",
        help="Include raw test output in the report"
    )
    test_parser.add_argument(
        "--devlog",
        action="store_true",
        help="Generate a combined devlog.md alongside index rebuild",
    )
    
    # Rebuild command (regenerates index from existing files)
    rebuild_parser = subparsers.add_parser(
        'rebuild',
        help='Rebuild the index.md from existing commits and test results',
        description='Scans both commits/ and tests/ folders and regenerates index.md with all items interleaved by time.'
    )
    rebuild_parser.add_argument(
        "-o", "--outputfolder",
        default="devlog",
        help="Output folder containing commits/ and tests/ (default: devlog)"
    )
    rebuild_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    rebuild_parser.add_argument(
        "--changelog",
        action="store_true",
        help="Use changelog order (newest first) instead of default (oldest first)"
    )
    rebuild_parser.add_argument(
        "--devlog",
        action="store_true",
        help="Generate a combined devlog.md when rebuilding",
    )
    
    # Parse args, but handle backwards compatibility
    # If first arg looks like an option (starts with -) but is NOT --help/-h, assume 'log' command
    if len(sys.argv) > 1 and sys.argv[1].startswith('-') and sys.argv[1] not in ['--help', '-h']:
        # Insert 'log' as the command for backwards compatibility
        sys.argv.insert(1, 'log')
    
    args = parser.parse_args()
    
    # Default to log if no command specified (backwards compatibility)
    if args.command is None:
        # Create default args dict for log command
        default_args = {
            'command': 'log',
            'repo': '.',
            'outputfolder': 'devlog',
            'from_commit': None,
            'to_commit': None,
            'allbranches': False,
            'verbose': False,
            'branch': None,
            'force': False,
            'dryrun': False,
            'obsidian_index': True,
            'devlog': False
        }
        core_main(default_args)
        return
    
    # Route to appropriate handler
    if args.command == 'test':
        sys.exit(test_main(vars(args)))
    elif args.command == 'rebuild':
        sys.exit(rebuild_main(vars(args)))
    else:
        core_main(vars(args))


if __name__ == "__main__":
    main()
