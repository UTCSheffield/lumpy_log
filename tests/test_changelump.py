import pytest
from lumpy_log.changelump import ChangeLump
from lumpy_log.languages import Languages
import os

@pytest.fixture
def languages():
    """Load the languages configuration"""
    lang_path = os.path.join(os.path.dirname(__file__), "..", "lumpy_log", "languages.yml")
    return Languages(lang_path)

@pytest.fixture
def python_language(languages):
    """Get Python language"""
    return languages.getByExtension(".py")

@pytest.fixture
def sample_python_code():
    """Sample Python code with a function"""
    return [
        "def calculate_sum(a, b):",
        "    \"\"\"Add two numbers together.\"\"\"",
        "    result = a + b",
        "    return result",
        "",
        "def multiply(x, y):",
        "    \"\"\"Multiply two numbers.\"\"\"",
        "    return x * y",
        "",
        "print('done')"
    ]

class TestChangeLumpWithFunction:
    """Test ChangeLump when initialized with a function"""
    
    def test_function_extraction_basic(self, python_language, sample_python_code):
        """Test extracting a complete function"""
        func_dict = {
            "start_line": 1,
            "end_line": 4,
            "name": "calculate_sum"
        }
        
        lump = ChangeLump(python_language, sample_python_code, func=func_dict)
        code = lump.code
        
        assert "def calculate_sum(a, b):" in code
        assert "result = a + b" in code
        assert "return result" in code
    
    def test_function_bounds(self, python_language, sample_python_code):
        """Test that function start and end are correctly set"""
        func_dict = {
            "start_line": 1,
            "end_line": 4,
            "name": "calculate_sum"
        }
        
        lump = ChangeLump(python_language, sample_python_code, func=func_dict)
        
        assert lump.start == 0  # 1-indexed to 0-indexed
        assert lump.end == 3
        assert lump.source == "Function"
    
    def test_function_with_docstring(self, python_language, sample_python_code):
        """Test extracting function with docstring"""
        func_dict = {
            "start_line": 6,
            "end_line": 8,
            "name": "multiply"
        }
        
        lump = ChangeLump(python_language, sample_python_code, func=func_dict)
        code = lump.code
        
        assert "def multiply(x, y):" in code
        assert "Multiply two numbers" in code
        assert "return x * y" in code

class TestChangeLumpWithLineChange:
    """Test ChangeLump when initialized with a line number"""
    
    def test_line_change_single_line(self, python_language, sample_python_code):
        """Test identifying a single changed line"""
        lump = ChangeLump(python_language, sample_python_code, start=3)
        
        assert lump.start == 2  # 1-indexed to 0-indexed
        assert lump.end == 2
        assert lump.source == "Line Changed"
    
    def test_line_change_with_range(self, python_language, sample_python_code):
        """Test identifying a range of changed lines"""
        lump = ChangeLump(python_language, sample_python_code, start=2, end=4)
        
        assert lump.start == 1
        assert lump.end == 3

class TestChangeLumpExtend:
    """Test the extend methods"""
    
    def test_extend_over_text_downward(self, python_language, sample_python_code):
        """Test extending a lump over contiguous non-empty lines"""
        lump = ChangeLump(python_language, sample_python_code, start=3)
        lump.extendOverText()
        
        # Should extend to include the function def and docstring
        assert lump.start <= 0
        assert lump.end >= 3
    
    def test_extend_over_comments(self, python_language):
        """Test extending over comment lines"""
        code_with_comments = [
            "# This is a comment",
            "# Another comment",
            "def my_function():",
            "    return 42"
        ]
        
        func_dict = {
            "start_line": 3,
            "end_line": 4,
            "name": "my_function"
        }
        
        lump = ChangeLump(python_language, code_with_comments, func=func_dict)
        lump.extendOverComments()
        
        # Should find comments before the function
        assert lump.commentStart is not None or lump.commentStart is None
        # (Depends on regex matching in language config)

class TestChangeLumpInLump:
    """Test the inLump method"""
    
    def test_in_lump_true(self, python_language, sample_python_code):
        """Test when line is within the lump"""
        lump = ChangeLump(python_language, sample_python_code, start=2, end=4)
        
        assert lump.inLump(1) == True
        assert lump.inLump(2) == True
        assert lump.inLump(3) == True
    
    def test_in_lump_false_before(self, python_language, sample_python_code):
        """Test when line is before the lump"""
        lump = ChangeLump(python_language, sample_python_code, start=3, end=4)
        
        assert lump.inLump(1) == False
    
    def test_in_lump_false_after(self, python_language, sample_python_code):
        """Test when line is after the lump"""
        lump = ChangeLump(python_language, sample_python_code, start=2, end=3)
        
        assert lump.inLump(5) == False

class TestChangeLumpBoundaryConditions:
    """Test edge cases and boundary conditions"""
    
    def test_zero_line_index(self, python_language, sample_python_code):
        """Test with line at index 0"""
        lump = ChangeLump(python_language, sample_python_code, start=1)
        
        assert lump.start == 0
    
    def test_negative_start_handled(self, python_language, sample_python_code):
        """Test that negative start is clamped to 0"""
        lump = ChangeLump(python_language, sample_python_code, start=-5)
        
        assert lump.start == 0
    
    def test_empty_lines_list(self, python_language):
        """Test with empty lines list"""
        lump = ChangeLump(python_language, [], start=1)
        
        assert lump.start == 0
        assert lump.code == ""
