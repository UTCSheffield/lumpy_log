#!/usr/bin/python3
import yaml
from pybars import Compiler # http://handlebarsjs.com documentation
from genericpath import exists
from re import split
import sys, os
from pydriller import Repository
from .change_lump import ChangeLump
from .languages import Languages
from importlib_resources import files

## pip3 install pydriller pybars4
languages = Languages()

sCommit = files("lumpy_log.templates").joinpath('commit.hbs').read_text()
sModifiedFiles = files("lumpy_log.templates").joinpath('modified_files.hbs').read_text()

compiler = Compiler()

# Compile the template
tCommit = compiler.compile(sCommit)
tModifiedFiles = compiler.compile(sModifiedFiles)

change_verbs_past = {
    "ADD" : "Added",
    "COPY" : "Copied",
    "RENAME" : "Renamed",
    "DELETE" : "Removed",
    "MODIFY" : "Modified",
    "UNKNOWN" : "Unknown"
}

def main(args):
    kwargs = {}
    for param in args.keys():
        if not param in ["dryrun","outputfolder", "force","verbose", "allbranches", "branch", "repo", "HCTI_API_USER_ID", "HCTI_API_KEY"]:
            if args[param]:
                kwargs[param] = args[param]

    if not exists(args['outputfolder']):
        os.makedirs(args['outputfolder'])

    commits = []

    #print("args", args)
    #return

    for commit in Repository(args['repo'], **kwargs).traverse_commits():
        if(args["allbranches"] or (
            (args["branch"] is None and commit.in_main_branch)
            or (args["branch"] in commit.branches) 
        )):
            genfilename = commit.author_date.strftime("%Y%m%d %H%M")+" "+commit.hash[:4]
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
                newcommit["markdown"] = tCommit(newcommit)
                        
                if hasattr(commit, "modified_files"):
                    for m in commit.modified_files:
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

                            newcommit["markdown"] += "\n\n" + tModifiedFiles(newmod)
                            
                        newcommit["modifications"].append(newmod)
                
                commits.append(newcommit)
                
                if(not args["dryrun"]):
                    with open( genfilepath, "w") as file1:
                        # Writing data to a file
                        #file1.write("\n\n".join(newcommit["markdown"]))
                        file1.write(newcommit["markdown"])
    
                    
if __name__ == "__main__":
    import argparse
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
    