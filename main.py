#!/usr/bin/python3

## pip3 install pydriller Pygments pybars4


# Get a compiler
from pybars import Compiler #http://handlebarsjs.com documentation
compiler = Compiler()

# Compile the template
source = u"{{>header}}{{#list people}}{{firstName}} {{lastName}}{{/list}}"
template = compiler.compile(source)
from genericpath import exists
from re import split
import sys, os
from pydriller import Repository

from guesslang import Guess
guess = Guess()


def main(args):
    kwargs = {}
    for param in args.keys():
        if not param in ["outputfolder", "allbranches", "branch", "repo", "HCTI_API_USER_ID", "HCTI_API_KEY"]:
            if args[param]:
                kwargs[param] = args[param]

    if not exists(args['outputfolder']):
        os.makedirs(args['outputfolder'])

    commits = []

    for commit in Repository(args['repo'], **kwargs).traverse_commits():
        if(args["allbranches"] or (
            (args["branch"] is None and commit.in_main_branch)
            or (args["branch"] in commit.branches) 
        )):
            print(commit.author.name, commit.msg)
            newcommit = {
                "hash":commit.hash,
                "msg":commit.msg,
                "author":commit.author.name,
                "date":commit.author_date.strftime("%Y-%m-%d"),
                "name":commit.author_date.strftime("%Y%m%d %H%M")+" "+commit.hash[:4],
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
                    language = file_extension.replace("","")
                    if language == "js":
                        "javascript"
                    if language == "py":
                        "python"
                    newmod = {
                        "filename":m.filename,
                        "change_type":m.change_type.name,
                        "code" : [],
                        "language": language,#"",#guess.language_name(m.source_code),
                        #"source_code":m.source_code
                        #"hlcode": "",
                        #"images": []
                    }
                                        
                    #if(m.source_code):
                    #    newmod["language"]= guess.language_name(m.source_code)

                    
                    print(
                        m.change_type.name,
                        " '{}'".format(m.filename)
                    )
                    
                    if m.filename.lower().endswith(('.png', '.jpg', '.jpeg', 'gif')) == False:                    
                        if m.change_type.name == "ADD":
                            newmod["code"].append(m.source_code)
                                
                        if m.change_type.name == "MODIFY":
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
            
            with open( os.path.join(args['outputfolder'],newcommit["name"]+".md"), "w") as file1:
                # Writing data to a file
                file1.write("\n\n".join(newcommit["markdown"]))
        
         
    #outputfile = os.path.join(args['outputfolder'], "index.html")
    #of = open(outputfile, "w")
    
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog='Prettify GitHub Log', description='Make git logs easier for use in scenerioas when communicating the progress of a project to none experts.')
    parser.add_argument("-i", "--repo", default='https://github.com/UTCSheffield/prettify-gh-log.git')
    parser.add_argument("-o", "--outputfolder", default="output")
    parser.add_argument("-f", "--fromcommit", dest="from_commit")
    parser.add_argument("-t", "--tocommit", dest="to_commit")
    parser.add_argument("-a", "--allbranches", action="store_true")
    parser.add_argument("-b", "--branch", dest="branch")
    args = parser.parse_args()
    
    main(vars(args))
   
   


