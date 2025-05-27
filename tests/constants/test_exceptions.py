# Unitary tests to the exceptions constants

from unittest import TestCase

from spanalyzer.constants.exceptions import ExcludedPaths

class TestExcludedPaths(TestCase):
    
    def test_excluded_paths_values(self):
        """
        Description: check if the values of the ExcludedPaths enum are duly encapsulated in
        a set.
        """
        
        actual = ExcludedPaths.values()
        expected = {
            "venv",
            "tests",
            "node_modules",
            "__pycache__",
            ".git",
            "__init__.py"
        }

        self.assertEqual(actual, expected)