#!/usr/bin/python3
import yaml
from jinja2 import Environment, FileSystemLoader
from genericpath import exists
from re import split
import sys, os
import pathspec
from pydriller import Repository
from .changelump import ChangeLump
from .languages import Languages

def _get_template_path(filename):
    """Get the absolute path to a template file"""
    package_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(package_dir, "templates", filename)

def _get_templates_dir():
    """Get the templates directory path"""
    package_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(package_dir, "templates")

languages = Languages(os.path.join(os.path.dirname(os.path.abspath(__file__)), "languages.yml"))

# Set up Jinja2 environment
jinja_env = Environment(loader=FileSystemLoader(_get_templates_dir()))
tCommit = jinja_env.get_template("commit.md")
tModifiedFiles = jinja_env.get_template("modified_files.md")
tObsidianIndex = jinja_env.get_template("obsidian_index.md")


change_verbs_past = {
    "ADD" : "Added",
    "COPY" : "Copied",
    "RENAME" : "Renamed",
    "DELETE" : "Removed",
    "MODIFY" : "Modified",
    "UNKNOWN" : "Unknown"
}

def _load_lumpy_ignore(repo_path: str):
    """Load .lumpyignore patterns (gitignore-style), with built-in defaults.

    Built-in defaults: ignore Markdown files ("*.md").
    """
    default_patterns = ["*.md"]
    ignore_file = os.path.join(repo_path, ".lumpyignore")

    patterns = list(default_patterns)
    if os.path.isfile(ignore_file):
        try:
            with open(ignore_file, "r", encoding="utf-8") as f:
                # PathSpec.from_lines handles comments; keep non-empty lines
                file_lines = [line.rstrip("\n") for line in f.readlines()]
                patterns.extend([l for l in file_lines if l.strip() != ""])
        except Exception as e:
            # Fail soft: proceed with defaults if file can't be read
            if __name__ == "__main__" or os.environ.get("LUMPY_LOG_VERBOSE_ERRORS"):
                print(f"Warning: could not read .lumpyignore: {e}")

    return pathspec.PathSpec.from_lines("gitwildmatch", patterns)

def main(args):
    kwargs = {}
    for param in args.keys():
        if not param in [
            "dryrun",
            "outputfolder",
            "force",
            "verbose",
            "allbranches",
            "branch",
            "repo",
            "obsidian_index",
            "HCTI_API_USER_ID",
            "HCTI_API_KEY",
        ]:
            if args[param]:
                kwargs[param] = args[param]

    # Only create the output directory when not a dry run
    if not args.get('dryrun') and not exists(args['outputfolder']):
        os.makedirs(args['outputfolder'])

    commits = []

    #print("args", args)
    #return

    # Build ignore spec once per run
    ignore_spec = _load_lumpy_ignore(args['repo'])

    for commit in Repository(args['repo'], **kwargs).traverse_commits():
        if(args["allbranches"] or (
            (args["branch"] is None and commit.in_main_branch)
            or (args["branch"] in commit.branches) 
        )):
            genfilename = commit.author_date.strftime("%Y%m%d_%H%M")+"_"+commit.hash[:7]
            genfilepath = os.path.join(args['outputfolder'], genfilename+".md")
            
            if(args["force"] or not os.path.exists(genfilepath)):
                if(args["verbose"]):
                    print("Making", genfilepath)
                newcommit = {
                    "hash":commit.hash,
                    "msg":commit.msg,
                    "author":commit.author.name,
                    "date":commit.author_date.strftime("%Y-%m-%d"),
                    "name": genfilename,
                    "author_date":commit.author_date,
                    "modifications":[],
                }
                newcommit["markdown"] = tCommit.render(newcommit)
                        
                if hasattr(commit, "modified_files"):
                    for m in commit.modified_files:
                        # Skip files that match .lumpyignore patterns
                        try:
                            if ignore_spec and ignore_spec.match_file(m.filename):
                                if(args["verbose"]):
                                    print(f"Ignoring per .lumpyignore: {m.filename}")
                                continue
                        except Exception:
                            # If matching fails for any reason, do not block processing
                            pass
                        filename, file_extension = os.path.splitext(m.filename)
                        language = languages.getByExtension(file_extension)
                        change_verb = m.change_type.name[0]+m.change_type.name[1:].lower()
                        
                        newmod = {
                            "filename":m.filename,
                            "change_type":m.change_type.name,
                            "change_verb": change_verb,
                            "change_verb_past": change_verbs_past[m.change_type.name],
                            "code" : [],
                            "lumps": [],
                            "language": language.mdname,
                            "source":""
                        }
                                            
                        if m.filename.lower().endswith(('.png', '.jpg', '.jpeg', 'gif')) == False:                    
                            if m.change_type.name == "ADD":
                                newmod["code"].append(m.source_code)
                                
                            if m.change_type.name == "MODIFY":
                                lines = str.splitlines(m.source_code)
                                    
                                if(False and args["verbose"]):
                                    print ("m.changed_methods", m.changed_methods)
                                if (len(m.changed_methods)):
                                    for c in m.changed_methods:
                                        newfunc = c.__dict__
                                        lump = ChangeLump(language, lines, func=c.__dict__, verbose=args["verbose"])
                                        lump.extendOverComments()
                                        newfunccode = lump.code
                                        newmod["source"] = "changed_methods"
                                        newmod["code"].append(newfunccode)
                                        newmod["lumps"].append(lump)
                                else:
                                    if(False and args["verbose"]):
                                        print ("Change m", m.diff_parsed)
                                    
                                    newmod["source"] = "line change"
                                    
                                    lump = None
                                    lumps = []
                                    for (linenum, linetext) in m.diff_parsed["added"]:
                                        if lump is None:
                                            lump = ChangeLump(language, lines, start=linenum, verbose=args["verbose"])
                                            lump.extendOverText()
                                            lumps.append(lump)    
                                        if(not lump.inLump(linenum-1)):
                                            lump = ChangeLump(language, lines, start=linenum, verbose=args["verbose"])
                                            lump.extendOverText()
                                            lumps.append(lump)
                                    
                                    for lump in lumps:
                                        if(False and args["verbose"]):
                                            print("lump.code", lump.code)
                                        newmod["code"].append(lump.code)
                                        newmod["lumps"].append(lump)
                                    
                                    #newmod["code"].append(m.source_code)

                            newcommit["markdown"] += "\n\n" + tModifiedFiles.render(newmod)
                            
                        newcommit["modifications"].append(newmod)
                
                commits.append(newcommit)
                
                if(not args["dryrun"]):
                    with open( genfilepath, "w") as file1:
                        # Writing data to a file
                        #file1.write("\n\n".join(newcommit["markdown"]))
                        file1.write(newcommit["markdown"])
    
        # Generate Obsidian index file if requested
        if not args["dryrun"] and args.get("obsidian_index", True):
            from datetime import datetime
            index_path = os.path.join(args['outputfolder'], "index.md")
            index_content = tObsidianIndex.render({
                "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "repo_path": args['repo'],
                "total_commits": len(commits),
                "commits": sorted(commits, key=lambda x: x['author_date'], reverse=True)
            })
        
            with open(index_path, "w") as f:
                f.write(index_content)
        
            if args["verbose"]:
                print(f"Generated Obsidian index: {index_path}")

    
