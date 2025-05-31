# Unitary tests for the PythonScriptSniffer class

import os

import ast

import textwrap

from unittest import TestCase

from spanalyzer.python.script import FunctionSpecs
from spanalyzer.python.script import PythonScriptSniffer

class TestPythonScriptSniffer(TestCase):
    
    def setUp(self):
        """
        Description: Set up the test environment.
        """

        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        
        self.script_1 = os.path.join(base_path, 'tests', 'samples', 'python', 'script_1.py')
        self.script_2 = os.path.join(base_path, 'tests', 'samples', 'python', 'script_2.py')
        self.script_3 = os.path.join(base_path, 'tests', 'samples', 'python', 'script_3.py')
        self.script_4 = os.path.join(base_path, 'tests', 'samples', 'python', 'script_4.py')

    def test_has_docstring_basic(self):
        """
        Description: Test that the function can duly capture a function with a very basic docstring.
        """

        test_function = textwrap.dedent('''
        def test_function():
            """
            This is a test function.
            """
        ''')

        test_function_ast = ast.parse(test_function)
        test_function_node = test_function_ast.body[0]

        sniffer = PythonScriptSniffer(test_function)

        actual = sniffer._has_docstring(test_function_node)
        expected = 'This is a test function.'

        self.assertEqual(actual, expected)

    def test_has_docstring_complex(self):
        """
        Description: Test that the function can duly capture a more complex docstring (i.e. a docstring
        containing multiple lines with input arguments speciifications, examples, etc.)
        """

        test_function = textwrap.dedent('''
        def test_function():
            """
            This is a test function.

            _Example_:
            >>> test_function(1, 'test')
            2

            Args:
                arg1 [int]: the first argument
                arg2 [str]: the second argument

            Returns:
                int: the result of the function
            """
        ''')

        test_function_ast = ast.parse(test_function)
        test_function_node = test_function_ast.body[0]

        sniffer = PythonScriptSniffer(test_function)

        actual = sniffer._has_docstring(test_function_node)
        expected = '''This is a test function.

    _Example_:
    >>> test_function(1, 'test')
    2

    Args:
        arg1 [int]: the first argument
        arg2 [str]: the second argument

    Returns:
        int: the result of the function'''

        self.assertEqual(actual, expected)

    def test_has_docstring_exception(self):
        """
        Description: when the function doesn't have a docstring.
        """

        test_function = textwrap.dedent('''
        def test_function():
            pass
        ''')

        test_function_ast = ast.parse(test_function)
        test_function_node = test_function_ast.body[0]

        sniffer = PythonScriptSniffer(test_function)

        actual = sniffer._has_docstring(test_function_node)
        expected = None

        self.assertEqual(actual, expected)

    def test_script_sniffer_basic(self):
        """
        Description: test the sniffer operating with a basic script (i.e. a script with a single funnction with very basic
        docstring, no arguments, etc)
        """

        script_sniffer = PythonScriptSniffer(self.script_1)
        script_sniffer.run()

        # Define the expected docstrings
        expected_docstring = """Random function that will contain the following opentelemetry resources:
    - span
    - span.set_attribute"""

        actual = script_sniffer.functions_list
        expected = [
            FunctionSpecs(
                name='random_function',
                docstring=expected_docstring,
                start_lineno=7,
                end_lineno=16
            )
        ]

        self.assertEqual(actual, expected)
    
    def test_script_sniffer_complex(self):
        """
        Description: test the sniffer operating with a complex script (i.e. a script with multiple functions with
        docstrings, arguments, etc)
        """

        script_sniffer = PythonScriptSniffer(self.script_2)
        script_sniffer.run()

        # Define the expected docstrings
        expected_docstring_1 = """Random function that will perform the addition of two values.

    _Example_:
    >>> result = random_function_1(1, 2)
    >>> print(result)
    3

    Args:
        val1 [int]: the first value to be added
        val2 [int]: the second value to be added

    Returns:
        [int]: the sum of the two values"""

        expected_docstring_2 = """Random function that will perform the subtraction of two values.

    _Example_:
    >>> result = random_function_2(1, 2)
    >>> print(result)
    -1

    Args:
        val1 [int]: the first value to be subtracted
        val2 [int]: the second value to be subtracted

    Returns:
        [int]: the difference of the two values"""

        expected_docstring_3 = """Random function containing three different spans."""
        expected_docstring_4 = """Random function demonstrating counter usage."""

        actual = script_sniffer.functions_list
        expected = [
            FunctionSpecs(
                name='random_function_1',
                docstring=expected_docstring_1,
                start_lineno=17,
                end_lineno=38
            ),
            FunctionSpecs(
                name='random_function_2',
                docstring=expected_docstring_2,
                start_lineno=40,
                end_lineno=71
            ),
            FunctionSpecs(
                name='random_function_3',
                docstring=expected_docstring_3,
                start_lineno=73,
                end_lineno=86
            ),
            FunctionSpecs(
                name='random_function_4',
                docstring=expected_docstring_4,
                start_lineno=88,
                end_lineno=109
            ),
        ]

        self.assertEqual(actual, expected)

    def test_script_sniffer_exception(self):
        """
        Description: test the sniffer operating with an empty script.
        """

        script_sniffer = PythonScriptSniffer(self.script_3)
        script_sniffer.run()

        actual = script_sniffer.functions_list
        expected = []

        self.assertEqual(actual, expected)

    def test_async_function_def(self):
        """
        Description: Test that the sniffer can handle async functions with telemetry.
        """

        script_sniffer = PythonScriptSniffer(self.script_4)
        script_sniffer.run()

        actual = script_sniffer.functions_list
        expected = [
            FunctionSpecs(
                name='fetch_mock_data',
                docstring="""Simulate async data fetch with delay.""",
                start_lineno=12,
                end_lineno=15
            ),
            FunctionSpecs(
                name='process_mock_data',
                docstring="""Simulate async data processing.""",
                start_lineno=17,
                end_lineno=20
            ),
            FunctionSpecs(
                name='async_fetch_data',
                docstring="""Async function that fetches data with telemetry.""",
                start_lineno=22,
                end_lineno=41
            )
        ]

        self.assertEqual(actual, expected)
