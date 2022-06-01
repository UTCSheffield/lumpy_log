import unittest
from nose2.tools import params

from lumpy_log.change_lump import ChangeLump
from lumpy_log.languages import Languages

languages = Languages()
JavaScript = languages.getByExtension(".js")
JavaScript_lines = '''
'''
Python = languages.getByExtension(".py")
Python_lines = '''
'''
Handlebars = languages.getByExtension(".hbs")
Handlebars_lines = '''
'''

HTML = languages.getByExtension(".html")
HTML_lines = '''
'''
class TestChangeLump(unittest.TestCase):
    @params((JavaScript, JavaScript_lines), (Python, Python_lines), (Handlebars, Handlebars_lines), (HTML, HTML_lines))
    def test___init__start(self, lang, lines, start=None):
        Lump = ChangeLump(lang, lines)

    '''
    def test___init__lines(self, lang, lines, start=None, end=None, func=None, verbose=False):



    def test__getByExtension(self, ext, lang):
        self.assertEqual(, lang)
            '''