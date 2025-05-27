# Unitary tests for the script.py file

import os

import ast

import textwrap

from unittest import TestCase

from spanalyzer.script import ScriptSniffer
from spanalyzer.script import FunctionSpecs

class TestScriptSniffer(TestCase):
    
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

        sniffer = ScriptSniffer(test_function)

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

        sniffer = ScriptSniffer(test_function)

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

        sniffer = ScriptSniffer(test_function)

        actual = sniffer._has_docstring(test_function_node)
        expected = None

        self.assertEqual(actual, expected)

    def test_script_sniffer_basic(self):
        """
        Description: test the sniffer operating with a basic script (i.e. a script with a single funnction with very basic
        docstring, no arguments, etc)
        """

        test_script = os.path.join(os.path.dirname(__file__), 'samples', 'script_1.py')

        script_sniffer = ScriptSniffer(test_script)
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

        test_script = os.path.join(os.path.dirname(__file__), 'samples', 'script_2.py')

        script_sniffer = ScriptSniffer(test_script)
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

        actual = script_sniffer.functions_list
        expected = [
            FunctionSpecs(
                name='random_function_1',
                docstring=expected_docstring_1,
                start_lineno=9,
                end_lineno=30
            ),
            FunctionSpecs(
                name='random_function_2',
                docstring=expected_docstring_2,
                start_lineno=32,
                end_lineno=63
            ),
            FunctionSpecs(
                name='random_function_3',
                docstring=expected_docstring_3,
                start_lineno=65,
                end_lineno=80
            ),
        ]

        self.assertEqual(actual, expected)

    def test_script_sniffer_exception(self):
        """
        Description: test the sniffer operating with an empty script.
        """

        test_script = os.path.join(os.path.dirname(__file__), 'samples', 'script_3.py')

        script_sniffer = ScriptSniffer(test_script)
        script_sniffer.run()

        actual = script_sniffer.functions_list
        expected = []

        self.assertEqual(actual, expected)
