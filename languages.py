#!/usr/bin/python3
import yaml

class Languages(object):
    def __init__(self, LANGUAGES_PATH = "languages.yml"):
        with open(self.LANGUAGES_PATH, 'r') as file:
            #self.LANGUAGES = [Language(sLang, oLang) for sLang, oLang in yaml.safe_load(file).items()]
            self.LANGUAGES = yaml.safe_load(file)

    # TODO : Cache the fetched language objects
             
def getByExtension(self, ext):
    Lang = self._getByExtension(ext)
    if(Lang is None):
        return None
    return Language(self.LANGUAGES[Lang])
    
def _getByExtension(self, ext):
    primary = [Lang for Lang in self.LANGUAGES if self.LANGUAGES[Lang]['primary_extension'] == ext] 
    
    if (len(primary)):
        return primary[0]#
        
    secondary = [Lang for Lang in self.LANGUAGES if 'extensions' in self.LANGUAGES[Lang] and ext in self.LANGUAGES[Lang]['extensions']] 
    
    if (len(secondary)):
        return secondary[0]#['lang'].lower()
    
    return None

class Language(object):
    def __init__(self, sLang, oLang):
        self.name = sLang
        self.oLang = oLang
    
    @property
    def commentType(self):
        #comment: C,  lexer: ActionScript 3, group: Shell
        pass
    
    @property
    def highlightname(self):
        if(self.oLang.ace_mode):
            return self.oLang.ace_mode
        return self.name.lower()
    
    