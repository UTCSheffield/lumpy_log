import unittest
from nose2.tools import params

from lumpy_log.languages import Languages

languages = Languages()

class TestLanguages(unittest.TestCase):
    @params((".py", "Python"), (".java", "Java"), (".js", "JavaScript"), (".css", "CSS"))
    def test__getByExtension(self, ext, lang):
        self.assertEqual(languages._getByExtension(ext), lang)

    @params((".py", "Python"), (".java", "Java"), (".js", "JavaScript"), (".css", "CSS"))
    def test_getByExtension(self, ext, lang):
        languages = Languages()
        self.assertEqual(languages.getByExtension(ext).name, lang)

    @params((".py", "python"), (".java", "java"), (".js", "javascript"), (".css", "css"))
    def test_mdname(self, ext, mdname):
        languages = Languages()
        self.assertEqual(languages.getByExtension(ext).mdname, mdname)

    @params((".py", "Python"), (".java", "C"), (".js", "C"), (".css", "CSS"))
    def test_comment_family(self, ext, comment_family):
        languages = Languages()
        self.assertEqual(languages.getByExtension(ext).comment_family, comment_family)




    
    