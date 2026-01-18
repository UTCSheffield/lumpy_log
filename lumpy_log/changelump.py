import re
class ChangeLump(object):
    def __init__(self, lang, lines, start=None, end=None, func=None, verbose=False):
        self.verbose = verbose
        self.lang = lang
        self.lines = lines
        self.commentStart = None
        self.multiLineStart = None
        self.multiLine = False
        self.source = None

        if len(lines) == 0:
            self.start = 0
            self.end = 0
            return
        
        if func is not None:
            self.source = "Function" 
            self.func = func
            self.start = max(0, func["start_line"] - 1)
            self.end = func["end_line"] - 1
        else:
            if(start is None):
                self.start = 0
            else:
                self.source = "Line Changed" 
                self.start = max(0, start - 1)
                
            if(end is None):
                self.end = self.start
            else:
                self.end = max(0, self.start, end - 1)

        self.start = min(self.start, len(self.lines)-1) 
        self.end = min(self.end, len(self.lines)-1)

        if self.verbose:
            print("ChangeLump", "self.start", self.start,"len(self.lines)", len(self.lines))
        
    def extendOverText(self):
        j = self.start-1
        try:
            while( j >= 0 and len(self.lines[j].strip())):
                self.start = j
                j -= 1
        except Exception as e:
            print("extendOverText", type(e), e, "j", j, "len(self.lines)", len(self.lines))
        
        k = self.end
        while( k < len(self.lines) and len(self.lines[k].strip())):
            self.end = k
            k += 1
        
        if self.verbose:
            print("extendOverText", "self.start", self.start,"j", j, "self.end",self.end,"k",k, "len(self.lines)",len(self.lines))
        
        
    def inLump(self,i):
        inLump = (self.start <= i and i <= self.end)
    
        if False and self.verbose:
            print("inLump", "self.start", self.start,"i", i, "inLump",inLump)
        return inLump
        
    def extendOverComments(self):
        if True and self.verbose:
            print("extendOverComments", "self.start", self.start)
        j = self.start
        while(j > 0 and self.lineIsComment(j-1)):
            j -= 1
            self.commentStart = j
            
            
    @property
    def code(self):    
        start = self.start 
        if(self.commentStart is not None):
            start = self.commentStart     

        #code = ""self.source+"\n"+
        code = ("\n".join(self.lines[start: self.end+1]))
        if True and self.verbose:
            print("code", code)
        return code
    
    def lineIsComment(self, i):
        blineIsComment = self._lineIsComment(i)
        if True and self.verbose:
            print("lineIsComment", blineIsComment, self.lines[i])
        return blineIsComment

    # Abstracts out lineIsComment so we can  print the results
    def _lineIsComment(self, i):
        firstLine = (i == self.start )
        line = self.lines[i].strip()

        if(self.verbose):
            print(self.lang.name, "self.lang.comment_structure",self.lang.comment_structure)
        comment_structure = self.lang.comment_structure

        if (comment_structure["begin"] ):
            try:
                beginmatches = re.findall(comment_structure["begin"],line)
                endmatches = re.findall( comment_structure["end"],line)
            
                if (firstLine and len(beginmatches) and len(beginmatches) == len(endmatches)): #both on same line
                    return True

                if(self.multiLine and self.multiLineStart is None):
                    if (len(beginmatches)):
                        self.multiLineStart = i
                        return True
                    return True

                if(firstLine and len(endmatches)):
                    self.multiLine = True
                    return True
            except Exception as Err:
                print(type(Err), Err)
                print(self.lang.comment_family, comment_structure)

        if(len(line) == 0):
            return False
        
        if (comment_structure["single"]):
            try:
                singlematches = re.findall( comment_structure["single"], line)
                return len(singlematches)>0
            except Exception as Err:
                print("Single", type(Err), Err)
                print(self.lang.comment_family, comment_structure["single"])
            
        return False

