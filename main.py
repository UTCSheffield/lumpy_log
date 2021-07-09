#!/usr/bin/python3

## pip3 install pydriller Pygments Jinja2

import sys, getopt
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
from jinja2 import Template, Environment, FileSystemLoader
from pydriller import Repository
#import imgkit


from html2image import Html2Image
hti = Html2Image()



def main(args):
    #print ("args", args)
    kwargs = {}
    for param in args.keys():
        if not param in ["outputfile", "repo"]:
            if args[param]:
                kwargs[param] = args[param]

    #print("kwargs", kwargs)
    commits = []

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
                    "hlcode": ""
                }

                print(
                    m.change_type.name,
                    " modified {}".format(m.filename),
                )
                

                if m.filename.lower().endswith(('.png', '.jpg', '.jpeg', 'gif')) == False:
                    
                    if m.change_type.name == "ADD":
                        lexer = guess_lexer(m.source_code)
                        newmod["hlcode"] = highlight(m.source_code, lexer, HtmlFormatter(wrapcode=True,linenos=True))
                            
                    if m.change_type.name == "MODIFY":
                        lexer = guess_lexer(m.source_code)
                        #print (m.changed_methods)
                        lines = str.splitlines(m.source_code)
                        
                        for c in m.changed_methods:
                            code = "\n".join(lines[c.__dict__['start_line']-1: c.__dict__['start_line']+ c.__dict__['nloc']])
                            newmod["hlcode"] += "<br /><br />"+highlight(code, lexer, HtmlFormatter(wrapcode=True))#linenostart=c.__dict__['start_line'],wrapcode=True,linenos=True))
                            #print(code)
                            #print(newmod["hlcode"])

                newcommit["modifications"].append(newmod)
        commits.append(newcommit)

    of = open(args['outputfile'], "w")
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    template = env.get_template('pretty.html')

    content={
        "commits":commits
    }
    output = template.render(content)
    #print(output)
    of.write(output)
    of.close()

    
    #imgkit.from_file('output.html', 'output.jpg')
    
    hti.screenshot(
        html_file=args['outputfile'],
        save_as='output.png'
    )

    #import pdfkit 
    #pdfkit.from_file(outputfile, outputfile+'.pdf') 


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog='Prettify GitHub Log', description='Make git logs easier for use in scenerioas when communicating the progress of a project to none experts.')
    parser.add_argument("-i", "--repo", default='https://github.com/UTCSheffield/prettify-gh-log.git')
    parser.add_argument("-o", "--outputfile", default="output2.html")
    parser.add_argument("-f", "--fromcommit", dest="from_commit")
    parser.add_argument("-t", "--tocommit", dest="to_commit")
    args = parser.parse_args()
    
    main(vars(args))
   
   


