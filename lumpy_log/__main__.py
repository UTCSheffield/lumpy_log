import argparse
from .lumpy_log import main

parser = argparse.ArgumentParser(prog='Prettify GitHub Log', description='Make git logs easier for use in scenerioas when communicating the progress of a project to none experts.')
parser.add_argument("-r", "--repo", default='https://github.com/UTCSheffield/lumpy_log.git')
parser.add_argument("-o", "--outputfolder", default="output")
parser.add_argument("-f", "--fromcommit", dest="from_commit")
parser.add_argument("-t", "--tocommit", dest="to_commit")
parser.add_argument("-a", "--allbranches", action="store_true")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-b", "--branch", dest="branch")
parser.add_argument("--force", action="store_true")
parser.add_argument("-d", "--dryrun", action="store_true")
args = parser.parse_args()

main(vars(args))