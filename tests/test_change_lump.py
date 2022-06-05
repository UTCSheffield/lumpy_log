import pytest
from lumpy_log.change_lump import ChangeLump
from lumpy_log.languages import Languages

languages = Languages()

JavaScript = languages.getByExtension(".js")
JavaScript_lines = '''
// Comment

/* Multiline on one line */

/* Multiline on 
3
lines */

// The function returns the product of p1 and p2
function myFunction(p1, p2) {
  return p1 * p2;   
}


'''.splitlines()

Python = languages.getByExtension(".py")
Python_lines = '''from importlib_resources import files
# Comment 

""" Multiline on one line """

""" Multiline on 
3
 lines """

# The function returns the product of p1 and p2
class Languages(object):
    def __init__(self, LANGUAGES_PATH = "languages.yml"):
        self.LANGUAGES_PATH = LANGUAGES_PATH
        sLanguages = files("lumpy_log").joinpath(self.LANGUAGES_PATH).read_text()
        self.LANGUAGES = yaml.safe_load(sLanguages)

    # TODO : Cache the fetched language objects

    @property
    def list(self):
        return self.LANGUAGES.keys()

'''.splitlines()

HTML = languages.getByExtension(".html")
HTML_lines = '''<!DOCTYPE html>
<!-- Comment -->

<!-- Comment -->

<!-- Comment 
over 3 
lines -->

<!-- Comment -->
<html>
<body>

<p>This is a paragraph.</p>

<!-- <p>This is another paragraph </p> -->

<p>This is a paragraph too.</p>

</body>
</html>
'''.splitlines()

class TestChangeLump():
    tests = {
        "JavaScript" :  {"lang":JavaScript, "lines":JavaScript_lines},
        "Python" :  {"lang":Python, "lines":Python_lines},
        "HTML" :  {"lang":HTML, "lines":HTML_lines},
    }
    
    
    @pytest.mark.parametrize("lang",["JavaScript", "Python", "HTML"])
    @pytest.mark.parametrize("line, isComment", [
        (0, False), 
        (1, False), 
        (2, True),
        (3, False),
        (4, True),
        (5, False),
        (6, True),
        (7, True), # Should be able to tell middle line of 3 line comment is comment
        (8, True), 
        (9, False),
        (100, False),
    ])
    def test__lineIsComment(self, lang, line, isComment):
        Lump = ChangeLump(lang = self.tests[lang]["lang"], lines = self.tests[lang]["lines"], verbose=True)
        assert Lump._lineIsComment(line) == isComment
    
    @pytest.mark.parametrize("lang",["JavaScript", "Python", "HTML"])
    @pytest.mark.parametrize("line, isComment", [
        (0, False), 
        (1, False), 
        (2, True),
        (3, False),
        (4, True),
        (5, False),
        (6, True),
        (7, False),
        (8, True), 
        (9, False),
        (100, False),
    ])
    def test__lineIsCommentTerminator(self, lang, line, isComment):
        Lump = ChangeLump(lang = self.tests[lang]["lang"], lines = self.tests[lang]["lines"], verbose=True)
        assert Lump._lineIsCommentTerminator(line) == isComment
    
    
    @pytest.mark.parametrize("lang",["JavaScript", "Python", "HTML"])
    @pytest.mark.parametrize("line, commentStart", [
        (0, False), 
        (1, False), 
        (2, 2),
        (3, False),
        (4, 4),
        (5, False),
        (6, 6),
        (7, 6),
        (8, 6), 
        (9, False),
        (100, False),
    ])
    def test_getCommentStart(self, lang, line, commentStart):
        Lump = ChangeLump(lang = self.tests[lang]["lang"], lines = self.tests[lang]["lines"], verbose=True)
        assert Lump.getCommentStart(line) == commentStart
    
    
    @pytest.mark.parametrize("lang",["JavaScript", "Python", "HTML"])
    @pytest.mark.parametrize("line, extendOverComments", [
        (0, False), 
        (1, False), 
        (2, False),
        (3, 2),
        (4, False),
        (5, 4),
        (6, False),
        (7, 6),
        (8, 6), 
        (9, 6),
        (100, False),
    ])
    def test_extendOverComments(self, lang, line, extendOverComments):
        Lump = ChangeLump(lang = self.tests[lang]["lang"], lines = self.tests[lang]["lines"], start=line)
        assert Lump.extendOverComments() == extendOverComments
    