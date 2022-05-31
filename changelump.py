import re
class ChangeLump(object):
    def __init__(self, lang, lines, start=None, end=None, func=None):
        self.verbose = False
        self.lang = lang
        self.lines = lines
        self.commentStart = None
        self.multiLineStart = None
        self.multiLine = False

        if func is not None:
            self.func = func
            self.start = max(0, func["start_line"] - 1)
            self.end = func["end_line"] 
        else:
            if(start is None):
                self.start = 0
            else:
                self.start = start

            if(end is None):
                self.end = self.start
            else:
                self.start = end

    
    def extendOverComments(self):
        if self.verbose:
            print("extendOverComments", "self.start", self.start)
        j = self.start - 1
        while(j >= 0 and self.lineIsComment(j)):
            self.commentStart = j
            '''print("num", j, "line",self.lines[j].strip(),
            "lineIsComment", self.lineIsComment(j)
                , "self.commentStart",self.commentStart, "self.multiLineStart", self.multiLineStart
                , "self.multiLine", self.multiLine)'''
            j -= 1
            


    @property
    def code(self):    
        start = self.start 
        if(self.commentStart):
            start = self.commentStart     

        code = "\n".join(self.lines[start: self.end])
        if self.verbose:
            print("code", code)
        return code
    
    def lineIsComment(self, i):
        blineIsComment = self._lineIsComment(i)
        if self.verbose:
            print("lineIsComment", blineIsComment, self.lines[i])
        return blineIsComment

    # Abstracts out lineIsComment Sso we can  print the results
    def _lineIsComment(self, i):
        firstLine = (i == self.start - 1 )
        line = self.lines[i].strip()

        if(False and self.verbose):
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
        
