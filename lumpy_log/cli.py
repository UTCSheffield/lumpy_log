"""Command-line interface for Lumpy Log"""
import argparse
from .core import main as core_main


def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        prog='lumpy-log',
        description='Make git logs easier for use in scenarios when communicating the progress of a project to non-experts.'
    )
    parser.add_argument(
        "-i", "--repo",
        default='.',
        help="Path to the local Git repository (default: current directory)"
    )
    parser.add_argument(
        "-o", "--outputfolder",
        default="content",
        help="Output folder for generated files (default: content)"
    )
    parser.add_argument(
        "-f", "--fromcommit",
        dest="from_commit",
        help="Start from this commit"
    )
    parser.add_argument(
        "-t", "--tocommit",
        dest="to_commit",
        help="End at this commit"
    )
    parser.add_argument(
        "-a", "--allbranches",
        action="store_true",
        help="Include all branches"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "-b", "--branch",
        dest="branch",
        help="Specific branch to process"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing files"
    )
    parser.add_argument(
        "-d", "--dryrun",
        action="store_true",
        help="Dry run - don't write files"
    )
    parser.add_argument(
        "-n", "--no-obsidian-index",
        dest="obsidian_index",
        action="store_false",
        help="Don't generate Obsidian-style index.md file",
    )
    parser.set_defaults(obsidian_index=True)
    
    args = parser.parse_args()
    core_main(vars(args))


if __name__ == "__main__":
    main()
