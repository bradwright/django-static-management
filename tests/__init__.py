import unittest
from static_management.management.commands.static_combine import recurse_files

class TestRecursion(unittest.TestCase):
    """tests that the recursion function works correctly"""
    def setUp(self):
        self.files = {
            "filename": ["file7", "file2", "file3"],
            "filename2": ["filename", "file6"],
            "filename3" : ["filename2", "file5"]
        }
    
    def test_level1_recursion(self):
        """test that inheritance works for the first level"""
        recursed = recurse_files('filename', self.files['filename'], self.files)
        self.assertEqual(recursed, ["file7", "file2", "file3"])
    
    def test_level2_recursion(self):
        """test that inheritance works for the second level"""
        recursed = recurse_files('filename2', self.files['filename2'], self.files)
        self.assertEqual(recursed, ["file7", "file2", "file3", "file6"])
        
    def test_level3_recursion(self):
        """test that inheritance works for the third level"""
        recursed = recurse_files('filename3', self.files['filename3'], self.files)
        self.assertEqual(recursed, ["file7", "file2", "file3", "file6", "file5"])
    
