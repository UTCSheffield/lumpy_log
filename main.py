#!/usr/bin/python3

## pip3 install pydriller Pygments Jinja2

from genericpath import exists
from re import split
import sys, os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
from jinja2 import Template, Environment, FileSystemLoader
from pydriller import Repository
from html2image import Html2Image
import requests

HCTI_API_ENDPOINT = "https://hcti.io/v1/image"
# Retrieve these from https://htmlcsstoimage.com/dashboard
HCTI_API_USER_ID = '22eb3ff9-aa7d-4291-a06d-9f1555f10f3b'
HCTI_API_KEY = '9f99382b-b32c-4865-9a4d-d68d3167ab86'

imagecount = 0
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)


def makeFragmentImage(fragment,hti, args):
    global imagecount, env
    template = env.get_template('minimal.html')
    lines = len(split("\n",fragment))
    content={
        "fragment":fragment
    }
    output = template.render(content)
    imagecount += 1
    imagename = None
    
    if(args["HCTI_API_USER_ID"] and args["HCTI_API_KEY"]):
        #print(imagename)
        data = { 'html': output }
            
        image = requests.post(url = HCTI_API_ENDPOINT, data = data, auth=(args["HCTI_API_USER_ID"], args["HCTI_API_KEY"]))
        ret = image.json()
        if hasattr(ret, 'url') or ret['url']:
            imagename = ret['url']
        else:
            print(ret)
    else :
        if(lines > 60):
            print("Code is "+str(lines)+" lines long it might me too long for this type of image")

        imagename = str(imagecount)+".png"
        hti.screenshot(
        html_str = output,
        save_as = imagename
    )
    

    return imagename



def main(args):
    kwargs = {}
    for param in args.keys():
        if not param in ["outputfolder", "repo", "HCTI_API_USER_ID", "HCTI_API_KEY"]:
            if args[param]:
                kwargs[param] = args[param]

    commits = []

    hti = Html2Image( output_path=args['outputfolder'] )

    for commit in Repository(args['repo'], **kwargs).traverse_commits():
        print(commit.author.name, commit.msg)
        newcommit = {
            "author":commit.author.name,
            "msg":commit.msg,
            "date":commit.author_date,
            "modifications":[]
        }

        if hasattr(commit, "modified_files"):
            for m in commit.modified_files:
                newmod = {
                    "filename":m.filename,
                    "change_type":m.change_type.name,
                    #"source_code":m.source_code
                    "hlcode": "",
                    "images": []
                }

                print(
                    m.change_type.name,
                    " modified {}".format(m.filename),
                )
                
                if m.filename.lower().endswith(('.png', '.jpg', '.jpeg', 'gif')) == False:                    
                    fragment = None
                    if m.change_type.name == "ADD":
                        lexer = guess_lexer(m.source_code)
                        fragment = highlight(m.source_code, lexer, HtmlFormatter(wrapcode=True,linenos=True))
                        newmod["hlcode"] = fragment
                        newmod["images"].append(makeFragmentImage(fragment,hti, args))
                            
                    if m.change_type.name == "MODIFY":
                        lexer = guess_lexer(m.source_code)
                        #print (m.changed_methods)
                        lines = str.splitlines(m.source_code)
                        
                        for c in m.changed_methods:
                            code = "\n".join(lines[c.__dict__['start_line']-1: c.__dict__['start_line']+ c.__dict__['nloc']])
                            fragment = highlight(m.source_code, lexer, HtmlFormatter(wrapcode=True,linenos=True))
                            newmod["hlcode"] += "<br /><br />"+fragment #linenostart=c.__dict__['start_line'],wrapcode=True,linenos=True))
                            newmod["images"].append(makeFragmentImage(fragment,hti, args))
                            #print(code)
                            #print(newmod["hlcode"])
                    
                    
                newcommit["modifications"].append(newmod)
        commits.append(newcommit)

    if not exists(args['outputfolder']):
        os.makedirs(args['outputfolder'])

    outputfile = os.path.join(args['outputfolder'], "index.html")
    of = open(outputfile, "w")
    
    template = env.get_template('pretty.html')

    content={
        "commits":commits
    }
    output = template.render(content)
    #print(output)
    of.write(output)
    of.close()

    
    #imgkit.from_file('output.html', 'output.jpg')
    
    
    #import pdfkit 
    #pdfkit.from_file(outputfile, outputfile+'.pdf') 


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog='Prettify GitHub Log', description='Make git logs easier for use in scenerioas when communicating the progress of a project to none experts.')
    parser.add_argument("-i", "--repo", default='https://github.com/UTCSheffield/prettify-gh-log.git')
    parser.add_argument("-o", "--outputfolder", default="output")
    parser.add_argument("-f", "--fromcommit", dest="from_commit")
    parser.add_argument("-t", "--tocommit", dest="to_commit")
    parser.add_argument("-u", "--hcti_user", dest="HCTI_API_USER_ID")
    parser.add_argument("-k", "--hcti_key", dest="HCTI_API_KEY")
    HCTI_API_USER_ID
    args = parser.parse_args()
    
    main(vars(args))
   
   


