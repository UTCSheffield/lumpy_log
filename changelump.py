class ChangeLump(object):
    def __init__(self, lang, lines, start=None, end=None, func=None):
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
        #print("extendOverComments", "self.start", self.start)
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
        #print("code", code)
        return code
    
    # languages.yml now contains a comment field 
    # i.e. comment : C 
    # https://geekflare.com/how-to-add-comments/
    def lineIsComment(self, i):
        firstLine = (i == self.start - 1 )
        line = self.lines[i].strip()

        if (self.multiLine and self.multiLineStart is None):
            if (self.lang in ["python"]) and (line[:3] in [ "'''" , '"""']):
                self.multiLineStart = i
                return True
            if (self.lang in ["c", "javascript"]) and (line[:2] in ["/*"]):
                self.multiLineStart = i
                return True
            return True
        
        if(len(line) == 0):
            return False

        if(firstLine):
            if (self.lang in ["python"]) and (line[-3:] in [ "'''" , '"""']):
                self.multiLine = True
                return True
            if (self.lang in ["c", "javascript"]) and (line[-2:] in ["*/"]):
                self.multiLine = True
                return True
        
        if (self.lang in ["python"]):
            return line[0] == "#"
        if (self.lang in ["c", "javascript"]):
            return (line[:2] in ["//"])

        return False
        
