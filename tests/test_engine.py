# Unitary tests for the engine.py file

import os

from pathlib import Path

from dotenv import load_dotenv

from unittest import TestCase

from spanalyzer.engine import Engine

load_dotenv()

class TestEngine(TestCase):

    def setUp(self):
        """
        Description: set up the test environment.
        """

        self.project_path = Path(os.getenv('PROJECT_ROOT_PATH'))

    def test__list_python_scripts(self):
        """
        Description: test if the _list_python_script is able to capture all the python scripts in a nested folder structure.
        """

        test_folder = os.path.join(self.project_path, 'tree')

        engine = Engine(test_folder, 'basic')

        actual = engine._list_python_scripts(test_folder)
        expected = [
            os.path.join(test_folder, 'script_1.py'),
            os.path.join(test_folder, 'subfolder', 'script_2.py'),
            os.path.join(test_folder, 'subfolder', 'subsubfolder', 'script_3.py'),
        ]

        self.assertEqual(actual, expected)