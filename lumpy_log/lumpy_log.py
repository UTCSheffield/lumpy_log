#!/usr/bin/python3
import yaml
from pybars import Compiler # http://handlebarsjs.com documentation
from genericpath import exists
from re import split
import sys, os
from pydriller import Repository, Commit
from .change_lump import ChangeLump
from .languages import Languages
from importlib_resources import files
import wrapt

languages = Languages()

class LumpyLog(object):
    languages = None
    sCommit = ""
    sModifiedFiles = ""
    commits = []

    change_verbs_past = {
        "ADD" : "Added",
        "COPY" : "Copied",
        "RENAME" : "Renamed",
        "DELETE" : "Removed",
        "MODIFY" : "Modified",
        "UNKNOWN" : "Unknown"
    }
    
    excludeParams = ["dryrun","outputfolder", "force","verbose", "allbranches", "branch", "repo"]
    
    def __init__(self, args):
        ## pip3 install pydriller pybars4
        
        sCommit = files("lumpy_log.templates").joinpath('commit.hbs').read_text()
        sModifiedFiles = files("lumpy_log.templates").joinpath('modified_files.hbs').read_text()

        compiler = Compiler()

        # Compile the template
        tCommit = compiler.compile(sCommit)
        tModifiedFiles = compiler.compile(sModifiedFiles)

        self.args = args

    def isRelevant(self, commit):
        return (self.args["allbranches"] or (
            (self.args["branch"] is None and commit.in_main_branch)
            or (self.args["branch"] in commit.branches) 
        ))        

    def createLumpyCommit(self, commit):
        return lumpyCommit(commit)
        
    def makeCommitOutput(self, commit):
        '''genfilename = 
            genfilepath = os.path.join(self.args['outputfolder'], genfilename)
            
            if(self.args["force"] or not os.path.exists(genfilepath)):
                if(self.args["verbose"]):
                    print("Making", genfilepath)

                newcommit["markdown"] = tCommit(newcommit)
        '''
        pass

                
    @property
    def commits(self):
        kwargs = {}
        for param in self.args.keys():
            if not param in self.excludeParams:
                if self.args[param]:
                    kwargs[param] = self.args[param]

        if not exists(self.args['outputfolder']):
            os.makedirs(self.args['outputfolder'])

        commits = Repository(self.args['repo'], **kwargs).traverse_commits().filter(self.isRelevant)
        
        lumpyCommits = commits.map()
        
        return commits
    
class lumpyFile(wrapt.ObjectProxy):
    lumps = []
    source = ""
    
    @property
    def language(self):
        filename, file_extension = os.path.splitext(self.filename)
        return languages.getByExtension(file_extension)
    
    @property
    def change_verb(self):
        return self.change_type.name[0]+self.change_type.name[1:].lower()
    
    @property
    def change_verb_past(self):
        return change_verbs_past[self.change_type.name],
                            
    @property
    def is_image(self):                        
        return self.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))                    
    
    @property
    def is_text(self):
        return not self.is_image()                        
    
    @property
    def lumps(self):
        if(self.is_image()):
            self.lumps = []
        elif self.change_type.name in ["COPY", "RENAME", "DELETE", "UNKNOWN"]:
            self.lumps = []  
        elif self.change_type.name == "ADD":
            lines = str.splitlines(self.source_code)
            self.lumps = [ChangeLump(self.language, lines)]
        elif self.change_type.name == "MODIFY":
            lines = str.splitlines(self.source_code)
            if (len(self.changed_methods)):
                self.lumps = self.changed_methods.map(lumpyMethod)
            else :
                lump = None
                lumps = []
                for (linenum, linetext) in self.diff_parsed["added"]:
                    if lump is None:
                        lump = ChangeLump(self.language, lines, start=linenum, verbose=self.args["verbose"])
                        lump.extendOverText()
                        lumps.append(lump)    
                    if(not lump.inLump(linenum - 1)):
                        lump = ChangeLump(self.language, lines, start=linenum, verbose=self.args["verbose"])
                        lump.extendOverText()
                        lumps.append(lump)
                self.lumps = lumps
                    
        return self.lumps
    '''
    @property
    def code(self):                        
        if(self.is_image()):
            return None

        if self.change_type.name in ["COPY", "RENAME", "DELETE", "UNKNOWN"]:
            return None
        
        if self.change_type.name == "ADD":
            return [self.source_code]
                
        if self.change_type.name == "MODIFY":
            lines = str.splitlines(self.source_code)
                
            if(False and self.args["verbose"]):
                print ("self.changed_methods", self.changed_methods)
            if (len(self.changed_methods)):
                for c in self.changed_methods:
                    newfunc = c.__dict__
                    lump = ChangeLump(language, lines, func=c.__dict__, verbose=self.args["verbose"])
                    lump.extendOverComments()
                    newfunccode = lump.code
                    newmod["source"] = "changed_methods"
                    newmod["code"].append(newfunccode)
                    newmod["lumps"].append(lump)
            else:
                if(False and self.args["verbose"]):
                    print ("Change m", m.diff_parsed)
                
                newmod["source"] = "line change"
                
                lump = None
                lumps = []
                for (linenum, linetext) in m.diff_parsed["added"]:
                    if lump is None:
                        lump = ChangeLump(language, lines, start=linenum, verbose=self.args["verbose"])
                        lump.extendOverText()
                        lumps.append(lump)    
                    if(not lump.inLump(linenum-1)):
                        lump = ChangeLump(language, lines, start=linenum, verbose=self.args["verbose"])
                        lump.extendOverText()
                        lumps.append(lump)
                
                for lump in lumps:
                    if(False and self.args["verbose"]):
                        print("lump.code", lump.code)
                    newmod["code"].append(lump.code)
                    newmod["lumps"].append(lump)
                
                #newmod["code"].append(m.source_code)
    '''
    
class lumpyMethod(wrapt.ObjectProxy, ChangeLump):
    
    pass   
    
class lumpyCommit(wrapt.ObjectProxy):
    
    @property
    def commitname(self):
        return self.author_date.strftime("%Y%m%d %H%M")+" "+self.hash[:4]
    
    @property 
    def filename(self):
        return self.commitname+".md"
    
    @property 
    def date_str(self):
        return self.author_date.strftime("%Y-%m-%d"),
    
    def createLumpyFile(self, m):
        return 
    
    @property          
    def modifications(self):
        if hasattr(self, "modified_files"):
            pass
            '''
            for m in self.modified_files:
                
            
                            newcommit["markdown"] += "\n\n" + tModifiedFiles(newmod)
                            
                        newcommit["modifications"].append(newmod)
                
                commits.append(newcommit)
                
                if(not self.args["dryrun"]):
                    with open( genfilepath, "w") as file1:
                        # Writing data to a file
                        #file1.write("\n\n".join(newcommit["markdown"]))
                        file1.write(newcommit["markdown"])
            '''