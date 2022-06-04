import pytest



from lumpy_log.change_lump import ChangeLump
from lumpy_log.languages import Languages

languages = Languages()

JavaScript = languages.getByExtension(".js")
JavaScript_lines = '''
// Comment

// The function returns the product of p1 and p2
function myFunction(p1, p2) {
  return p1 * p2;   
}


'''

Python = languages.getByExtension(".py")
Python_lines = '''from importlib_resources import files
# Comment 

class Languages(object):
    def __init__(self, LANGUAGES_PATH = "languages.yml"):
        self.LANGUAGES_PATH = LANGUAGES_PATH
        sLanguages = files("lumpy_log").joinpath(self.LANGUAGES_PATH).read_text()
        self.LANGUAGES = yaml.safe_load(sLanguages)

    # TODO : Cache the fetched language objects

    @property
    def list(self):
        return self.LANGUAGES.keys()

'''
Handlebars = languages.getByExtension(".hbs")
Handlebars_lines = '''
{{! Comment }}

## Commit : {{msg}}

By "{{ author }}" on {{ date }}

'''

HTML = languages.getByExtension(".html")
HTML_lines = '''<!DOCTYPE html>
<!-- Comment -->
<html>
<body>

<p>This is a paragraph.</p>

<!-- <p>This is another paragraph </p> -->

<p>This is a paragraph too.</p>

</body>
</html>
'''
class TestChangeLump():
    @pytest.mark.parametrize("lang, lines, line, isComment", [
        (JavaScript, JavaScript_lines,1,False), 
        (Python, Python_lines,1,False), 
        #(Handlebars, Handlebars_lines,1,False), 
        (HTML, HTML_lines,1,False),
        (JavaScript, JavaScript_lines,2,True), 
        (Python, Python_lines,2,True), 
        #(Handlebars, Handlebars_lines,2,True), 
        (HTML, HTML_lines,2,True)
    ])
    def test___init__is_comment(self, lang, lines, line, isComment):
        Lump = ChangeLump(lang, lines, verbose=True)
        assert Lump._lineIsComment(line) == isComment
    
    
    '''def test___init__start(self, lang, lines, start=1, lump_lines=1):
        Lump = ChangeLump(lang, lines,start=start, verbose=True)
        self.assertEqual(len(Lump.code.splitlines()), lump_lines)
    '''
    '''
    def test___init__lines(self, lang, lines, start=None, end=None, func=None, verbose=False):



    def test__getByExtension(self, ext, lang):
        self.assertEqual(, lang)
            '''