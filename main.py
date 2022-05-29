#!/usr/bin/python3

## pip3 install pydriller Pygments pybars4

import yaml
LANGUAGES_PATH = "languages.yml"

def morphLang(aLang):
    oLang = aLang[1]
    oLang['lang'] = aLang[0]
    return oLang

with open(LANGUAGES_PATH, 'r') as file:
    LANGUAGES = [morphLang(Lang) for Lang in yaml.safe_load(file).items()]
    
def getFileLanguage(ext):
    primary = [val for val in LANGUAGES if val['primary_extension'] == ext] 
    
    if (len(primary)):
        if 'ace_mode' in primary[0]:
            return primary[0]['ace_mode']
        return primary[0]['lang'].lower()
        
    secondary = [val for val in LANGUAGES if 'extensions' in val and val['extensions'] == ext] 
    
    if (len(secondary)):
        if 'ace_mode' in secondary[0]:
            return secondary[0]['ace_mode']
        return secondary[0]['lang'].lower()
        
    return ext[1:]


'''
# Get a compilerWS
from pybars import Compiler #http://handlebarsjs.com documentation
compiler = Compiler()

# Compile the template
source = u"{{>header}}{{#list people}}{{firstName}} {{lastName}}{{/list}}"
template = compiler.compile(source)
'''

from genericpath import exists
from re import split
import sys, os
from pydriller import Repository

def main(args):
    kwargs = {}
    for param in args.keys():
        if not param in ["outputfolder", "force","verbose", "allbranches", "branch", "repo", "HCTI_API_USER_ID", "HCTI_API_KEY"]:
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
                    "markdown" : [
                        "## Commit by "+ commit.author.name+" at "+ str(commit.author_date),
                        commit.hash,
                        commit.msg
                    ]
                }

                if hasattr(commit, "modified_files"):
                    for m in commit.modified_files:
                        filename, file_extension = os.path.splitext(m.filename)
                        language = getFileLanguage(file_extension)

                        newmod = {
                            "filename":m.filename,
                            "change_type":m.change_type.name,
                            "code" : [],
                            "language": language
                        }
                                            
                        if m.filename.lower().endswith(('.png', '.jpg', '.jpeg', 'gif')) == False:                    
                            if m.change_type.name == "ADD":
                                newmod["code"].append(m.source_code)
                                    
                            if m.change_type.name == "MODIFY":
                                if(False and args["verbose"]):
                                    print ("m.changed_methods", m.changed_methods)
                                if (len(m.changed_methods)):
                                    lines = str.splitlines(m.source_code)
                                        
                                    for c in m.changed_methods:
                                        newfunc = "\n".join(lines[c.__dict__['start_line']-1: c.__dict__['start_line']+ c.__dict__['nloc']+1])
                                        #print("newfunc", newfunc)
                                        newmod["code"].append(newfunc)
                                else:
                                    newmod["code"].append(m.source_code)
                        
                            newcommit["markdown"].append("### "+newmod["change_type"]+" : "+ newmod["filename"])
                            newcommit["markdown"].append("```"+newmod["language"])
                            newcommit["markdown"].append("\n".join(newmod["code"]))
                            newcommit["markdown"].append("```")
                        newcommit["modifications"].append(newmod)
                
                commits.append(newcommit)
                
                with open( genfilepath, "w") as file1:
                    # Writing data to a file
                    file1.write("\n\n".join(newcommit["markdown"]))
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog='Prettify GitHub Log', description='Make git logs easier for use in scenerioas when communicating the progress of a project to none experts.')
    parser.add_argument("-i", "--repo", default='https://github.com/UTCSheffield/prettify-gh-log.git')
    parser.add_argument("-o", "--outputfolder", default="output")
    parser.add_argument("-f", "--fromcommit", dest="from_commit")
    parser.add_argument("-t", "--tocommit", dest="to_commit")
    parser.add_argument("-a", "--allbranches", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_false")
    parser.add_argument("-b", "--branch", dest="branch")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    
    main(vars(args))
    