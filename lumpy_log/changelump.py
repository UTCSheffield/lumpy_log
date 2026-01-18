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
                self.end = max(self.start, end - 1)

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
        line = self.lines[i]
        if(self.verbose):
            print(self.lang.name, "self.lang.comment_structure",self.lang.comment_structure)
        comment_structure = self.lang.comment_structure

        begin = comment_structure.get("begin")
        end = comment_structure.get("end")
        single = comment_structure.get("single")

        # Multiline comments: treat lines with both begin and end as comment,
        # and any line inside unmatched begin/end pairs as comment.
        if begin:
            try:
                beginmatches = re.findall(begin, line)
                endmatches = re.findall(end, line)

                # If both markers appear on the same line, it's a comment line.
                if len(beginmatches) and len(endmatches):
                    return True
                
                print("Checking multiline comment for line", i, line, self._in_multiline_comment(i, begin, end))
                # If this line is inside an open multiline comment, it's a comment.
                if self._in_multiline_comment(i, begin, end):
                    return True
            except Exception as Err:
                print(type(Err), Err)
                print(self.lang.comment_family, comment_structure)

        # Single-line comments
        if single:
            try:
                if re.search(single, line.strip()):
                    return True
            except Exception as Err:
                print("Single", type(Err), Err)
                print(self.lang.comment_family, comment_structure["single"])

        return False

    def _in_multiline_comment(self, i, begin_re, end_re):
        print("Running _in_multiline_comment for line", i, self.lines[i])
        """Return True if line i is inside an unmatched multiline comment block."""
        try:
            # Check if begin and end delimiters are the same (symmetric like """)
            # Strip common regex anchors to compare the actual delimiter strings
            begin_stripped = begin_re.strip('^$\\s')
            end_stripped = end_re.strip('^$\\s')
            symmetric = (begin_stripped == end_stripped)
            print("  Symmetric delimiters?", symmetric, "b", begin_re, "e", end_re, "stripped b", begin_stripped, "e", end_stripped) 
            
            in_comment = False
            for idx in range(0, i + 1):
                s = self.lines[idx]
                
                if symmetric:
                    # For symmetric delimiters (like """ in Python), each occurrence
                    # toggles the comment state: first one opens, second one closes, etc.
                    # Example: """comment""" means we enter on first """, exit on second
                    matches = re.findall(begin_re, s)
                    print("  Found", len(matches), "symmetric delimiters in line", idx, s)  
                    for _ in matches:
                        in_comment = not in_comment  # Flip True->False or False->True
                    print("  Checking symmetricline", idx, s, "in_comment now", in_comment)
                else:
                    # For asymmetric delimiters, track depth
                    begins = len(re.findall(begin_re, s))
                    ends = len(re.findall(end_re, s))
                    
                    # Process begins first, then ends
                    if not in_comment and begins > 0:
                        in_comment = True
                    if in_comment and ends > 0:
                        in_comment = False
                    
                    print("  Checking line", idx, s, "begins", begins, "ends", ends, "in_comment now", in_comment)
            
            return in_comment
        except Exception as Err:
            if self.verbose:
                print("_in_multiline_comment error", type(Err), Err)
            return False

