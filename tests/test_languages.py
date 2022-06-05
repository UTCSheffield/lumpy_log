import pytest

from lumpy_log.languages import Languages

languages = Languages()

class TestLanguages():
    @pytest.mark.parametrize("ext, lang", 
        [(".py", "Python"), (".java", "Java"), (".js", "JavaScript"), (".css", "CSS")]
    )
    def test__getByExtension(self, ext, lang):
        assert languages._getByExtension(ext) == lang

    @pytest.mark.parametrize("ext, lang", 
        [(".py", "Python"), (".java", "Java"), (".js", "JavaScript"), (".css", "CSS")]
    )
    def test_getByExtension(self, ext, lang):
        languages = Languages()
        assert languages.getByExtension(ext).name == lang

    @pytest.mark.parametrize("ext, markdown_name", 
        [(".py", "python"), (".java", "java"), (".js", "javascript"), (".css", "css")]
    )
    def test_markdown_name(self, ext, markdown_name):
        languages = Languages()
        assert languages.getByExtension(ext).markdown_name == markdown_name

    @pytest.mark.parametrize("ext, comment_family", 
        [(".py", "Python"), (".java", "C"), (".js", "C"), (".css", "CSS")]
    )
    def test_comment_family(self, ext, comment_family):
        languages = Languages()
        assert languages.getByExtension(ext).comment_family == comment_family




    
    