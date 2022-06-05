import re

class ChangeLump(object):
    lang = None 
    lines = []
    commentStart = None
    multiLineStart = None
    multiLine = False
    source = "Source Code"
    start = None
    end = None
            
    def __init__(self, lang=lang, lines=[], start=None, end=None, verbose=False):
    #def __init__(self, lang=lang, lines=[], start=None, end=None, func=None, verbose=False):
        self.lang = lang 
        self.verbose = verbose
        self.lines = [""]
        self.lines.extend(lines)
        
        '''
        if func is not None:
            self.source = "Function" 
            self.func = func
            self.start = func["start_line"]
            self.end = func["end_line"]
        else:
        '''
        if(start is None):
            self.start = 1
        else:
            self.source = "Line Changed" 
            self.start = start

        if(end is None):
            self.end = self.start
        else:
            self.end = end

        if self.verbose:
            print("ChangeLump", "self.start", self.start,"len(self.lines)", len(self.lines))
        
    def extendOverText(self):
        j = self.start
        try:
            while( j >= 1 and len(self.lines[j].strip())):
                self.start = j
                j -= 1
        except Exception as e:
            print("extendOverText", type(e), e, "j", j, "len(self.lines)", len(self.lines))
        
        k = self.end
        while( k < len(self.lines) and len(self.lines[k].strip())):
            self.end = k
            k += 1
        
        if False and self.verbose:
            print("extendOverText", "self.start", self.start,"j", j, "self.end",self.end,"k",k, "len(self.lines)",len(self.lines))
        
    def inLump(self,i):
        inLump = (self.start <= i and i <= self.end)
    
        if False and self.verbose:
            print("inLump", "self.start", self.start,"i", i, "inLump",inLump)
        return inLump
        
    def extendOverComments(self):
        if True and self.verbose:
            print("extendOverComments", "self.start", self.start)
        
        commentStart = self.getCommentStart(self.start - 1)
        if (commentStart == False):
            self.commentStart = None
        
        self.commentStart = commentStart
        return self.commentStart
            
    @property
    def code(self):    
        start = self.start 
        if(self.commentStart):
            start = self.commentStart     

        #code = ""self.source+"\n"+
        code = ("\n".join(self.lines[start: self.end + 1]))
        if True and self.verbose:
            print("code", code)
        return code
    
    def getCommentStart(self, i):
        if(i == 0  or i>= len(self.lines)):
           return False
        
        begins, ends = self._lineIsCommentTerminators(i)
        if begins:
            return i
        
        while i >= 1:
            i -= 1
            begins, ends = self._lineIsCommentTerminators(i)
            if begins and ends:
                return False    
            if (begins):
                return i
            if (ends):
                return False
        return False
    
    
    def _lineIsComment(self, i):
        if(i == 0  or i >= len(self.lines)):
            False
            
        begins, ends = self._lineIsCommentTerminators(i)
        if begins or ends:
            return True
        
        while i >= 1:
            i -= 1
            begins, ends = self._lineIsCommentTerminators(i)
            if (ends):
                return False
            if (begins):
                return True
        return False
        
    def _lineIsCommentTerminator(self, i):
        begins, ends = self._lineIsCommentTerminators(i)
        return begins or ends
        
    # Abstracts out lineIsComment so we can  print the results
    def _lineIsCommentTerminators(self, i):
        begins = False
        ends = False
        if(i == 0  or i >= len(self.lines)):
            return (False, False)
        
        line = self.lines[i].strip()

        if(False and self.verbose):
            print(self.lang.name, "self.lang.comment_structure",self.lang.comment_structure)
        comment_structure = self.lang.comment_structure
        
        if(len(line) == 0):
            return (False, False)
        
        if (comment_structure["begin"] ):
            beginmatches = re.findall(comment_structure["begin"],line)
            endmatches = re.findall( comment_structure["end"],line)
        
            begins = len(beginmatches) > 0
            ends = len(endmatches) > 0
            
            if (begins or ends):
                return (begins, ends)
        
        if (comment_structure["single"]):
            singlematches = re.findall( comment_structure["single"], line)
            begins = ends = len(singlematches) > 0

        return (begins, ends)
