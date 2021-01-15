#!/usr/bin/python3


## pip3 install pydriller Pygments Jinja2

import sys, getopt
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
from jinja2 import Template, Environment, FileSystemLoader
from pydriller import RepositoryMining


def main(argv):
    repo = '../mote_light_painting'
    outputfile = 'mlp2.html'
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["irepo=","ofile="])
    except getopt.GetoptError:
        print ('main.py -i <repo> -o <outputfile>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <repo> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--irepo"):
            repo = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    #print ('Input file is "', repo)
    #print ('Output file is "', outputfile)

    commits = []
    for commit in RepositoryMining(repo).traverse_commits():
        newcommit = {
            "author":commit.author.name,
            "msg":commit.msg,
            "date":commit.author_date,
            "modifications":[]
        }
        for m in commit.modifications:
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

    of = open(outputfile, "w")
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

    #import pdfkit 
    #pdfkit.from_file(outputfile, outputfile+'.pdf') 


if __name__ == "__main__":
    main(sys.argv[1:])
   
   


