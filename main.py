#!/usr/bin/python3

import yaml
from pybars import Compiler # http://handlebarsjs.com documentation
from genericpath import exists
from re import split
import sys, os
from pydriller import Repository

## pip3 install pydriller Pygments pybars4

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
        
    secondary = [val for val in LANGUAGES if 'extensions' in val and ext in val['extensions']] 
    
    if (len(secondary)):
        if 'ace_mode' in secondary[0]:
            return secondary[0]['ace_mode']
        return secondary[0]['lang'].lower()
    
    return ext[1:]


with open(os.path.join("templates","commit.hbs")) as f:
    sCommit = f.read()

with open(os.path.join("templates","modified_files.hbs")) as f:
    sModifiedFiles = f.read()

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

def lineIsComment(lang, line, multiline = False):
    '''Needs to be a recursive thing that works backwards and returns a number'''
    if (multiline):
        if (lang in ["python"]):
            return not((line.strip()[:3] == "'''") or (line.strip()[:3] == '"""'))
        if (lang in ["c", "javascript"]):
            return (line.strip()[:2] in ["/*"])
        return False
        
    if (lang in ["python"]):
        return line.strip()[0] == "#"
    if (lang in ["c", "javascript"]):
        return (line.strip()[-2:] == "*/") or (line.strip()[:2] in ["//", "/*"])
    return False
    
def getFunctionCode(lines, lang, newfunc):                                    
    '''Takes in the code, language and function start and end line
    returns the lines of the function including comments
    '''
    startline = newfunc['start_line']-1
    
    if (lineIsComment(lang, lines[startline-1])):
        #print("lines[startline-1]", lines[startline-1])
        pass
    
    return "\n".join(lines[startline: newfunc['end_line']])
    

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
                        language = getFileLanguage(file_extension)
                        change_verb = m.change_type.name[0]+m.change_type.name[1:].lower()
                        
                        newmod = {
                            "filename":m.filename,
                            "change_type":m.change_type.name,
                            "change_verb": change_verb,
                            "change_verb_past": change_verbs_past[m.change_type.name],
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
                                        newfunc = c.__dict__
                                        newfunccode = getFunctionCode(lines, language, newfunc)
                                        #newfunccode = "\n".join(lines[newfunc['start_line']-1: newfunc['end_line']])
                                        #print("newfunccode", newfunccode)
                                        newmod["code"].append(newfunccode)
                                else:
                                    newmod["code"].append(m.source_code)

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
    parser.add_argument("-i", "--repo", default='https://github.com/UTCSheffield/prettify-gh-log.git')
    parser.add_argument("-o", "--outputfolder", default="output")
    parser.add_argument("-f", "--fromcommit", dest="from_commit")
    parser.add_argument("-t", "--tocommit", dest="to_commit")
    parser.add_argument("-a", "--allbranches", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_false")
    parser.add_argument("-b", "--branch", dest="branch")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("-d", "--dryrun", action="store_true")
    args = parser.parse_args()
    
    main(vars(args))
    