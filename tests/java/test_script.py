# Unitary tests for the JavaScriptSniffer class

import os

import javalang

from unittest import TestCase
from unittest.mock import patch
from unittest.mock import mock_open

from spanalyzer.java.script import FunctionSpecs
from spanalyzer.java.script import JavaScriptSniffer

class TestJavaScriptSniffer(TestCase):

    def setUp(self):
        """
        Description: Set up the test environment.
        """

        base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        self.script_1 = os.path.join(base_path, 'tests', 'samples', 'java', 'script_1.java')
        self.script_2 = os.path.join(base_path, 'tests', 'samples', 'java', 'script_2.java')
        self.script_3 = os.path.join(base_path, 'tests', 'samples', 'java', 'script_3.java')
        self.script_4 = os.path.join(base_path, 'tests', 'samples', 'java', 'script_4.java')

    def test_get_javadoc_for_method_basic(self):
        """
        Description: Test that the function can duly capture a function with a very basic docstring.
        """

        test_code = '''
        public class TestClass {
        /**
         * This is a test function.
         */
            public void testFunction() {
            }
        }
        '''

        with patch("builtins.open", mock_open(read_data=test_code)):
            sniffer = JavaScriptSniffer("Dummy.java")

            comments = sniffer._extract_comments()
            tree = javalang.parse.parse(test_code)

            method_node = None
            for path, node in tree.filter(javalang.tree.MethodDeclaration):
                if node.name == "testFunction":
                    method_node = node
                    break

            self.assertIsNotNone(method_node, "Method node not found")

            actual = sniffer._get_javadoc_for_method(method_node, comments)
            expected = "* This is a test function."

            self.assertEqual(actual, expected)

    def test_get_javadoc_for_method_complex(self):
        """
        Description: Test that the function can duly capture a more complex docstring (i.e. a docstring
        containing multiple lines with input arguments speciifications, examples, etc.)
        """

        test_code = '''
        public class TestClass {
        /**
         * This is a test function.

            _Example_:
            >>> test_function(1, 'test')
            2

            Args:
                arg1 [int]: the first argument
                arg2 [str]: the second argument

            Returns:
                int: the result of the function
         */
            public void testFunction() {
            }
        }
        '''

        with patch("builtins.open", mock_open(read_data=test_code)):
            sniffer = JavaScriptSniffer("Dummy.java")

            comments = sniffer._extract_comments()
            tree = javalang.parse.parse(test_code)

            method_node = None
            for path, node in tree.filter(javalang.tree.MethodDeclaration):
                if node.name == "testFunction":
                    method_node = node
                    break

            self.assertIsNotNone(method_node, "Method node not found")

            actual = sniffer._get_javadoc_for_method(method_node, comments)
            expected = '''* This is a test function.

            _Example_:
            >>> test_function(1, 'test')
            2

            Args:
                arg1 [int]: the first argument
                arg2 [str]: the second argument

            Returns:
                int: the result of the function'''

            self.assertEqual(actual, expected)

    def test_get_javadoc_for_method_exception(self):
        """
        Description: Test that the function can duly capture a function with no docstring.
        """

        test_code = '''
        public class TestClass {
            public void testFunction() {
            }
        }
        '''

        with patch("builtins.open", mock_open(read_data=test_code)):
            sniffer = JavaScriptSniffer("Dummy.java")

            comments = sniffer._extract_comments()
            tree = javalang.parse.parse(test_code)

            method_node = None
            for path, node in tree.filter(javalang.tree.MethodDeclaration):
                if node.name == "testFunction":
                    method_node = node
                    break

            self.assertIsNotNone(method_node, "Method node not found")

            actual = sniffer._get_javadoc_for_method(method_node, comments)
            expected = None

            self.assertEqual(actual, expected)

    def test__estimate_method_end_basic(self):
        """
        Description: Test that the method end line is correctly estimated for a method that
        doesn't have any documentation.
        """

        test_code = '''
        public class Example {
            public void testFunction() {
                int x = 5;
                System.out.println(x);
            }
        }
        '''

        with patch("builtins.open", mock_open(read_data=test_code)):
            sniffer = JavaScriptSniffer("Dummy.java")

            start_line = 1

            actual = sniffer._estimate_method_end(start_line)
            expected = 7

            self.assertEqual(actual, expected)

    def test__estimate_method_end_complex(self):
        """
        Description: Test that the method end line is correctly estimated for a method that
        has a docstring.
        """

        test_code = '''
        public class Example {
            /**
             * Adds two integers and returns the result.
             *
             * @param a the first integer
             * @param b the second integer
             * @return the sum of a and b
             */
            public int add(int a, int b) {
                return a + b;
            }
        }
        '''

        with patch("builtins.open", mock_open(read_data=test_code)):
            sniffer = JavaScriptSniffer("Dummy.java")

            start_line = 1

            actual = sniffer._estimate_method_end(start_line)
            expected = 13

            self.assertEqual(actual, expected)

    def test__extract_comments_basic(self):
        """
        Description: Test that the function can duly capture a function with a very basic docstring.
        """

        test_code = '''
        public class TestClass {
        /**
         * This is a test function.
         */
            public void testFunction() {
            }
        }
        '''

        with patch("builtins.open", mock_open(read_data=test_code)):
            sniffer = JavaScriptSniffer("Dummy.java")

            actual = sniffer._extract_comments()
            expected = [(3, '        /**\n         * This is a test function.\n         */')]

            self.assertEqual(actual, expected)

    def test__extract_comments_complex(self):
        """
        Description: Test that the function can duly capture a function with a more complex docstring.
        """

        test_code = '''
        public class TestClass {
        /**
         * This is a test function.

            _Example_:
            >>> test_function(1, 'test')
            2

            Args:
                arg1 [int]: the first argument
                arg2 [str]: the second argument

            Returns:
                int: the result of the function
         */
            public void testFunction() {
            }
        }
        '''

        with patch("builtins.open", mock_open(read_data=test_code)):
            sniffer = JavaScriptSniffer("Dummy.java")

            actual = sniffer._extract_comments()
            expected = [(3, 
                "        /**\n"
                "         * This is a test function.\n\n"
                "            _Example_:\n"
                "            >>> test_function(1, 'test')\n"
                "            2\n\n"
                "            Args:\n"
                "                arg1 [int]: the first argument\n"
                "                arg2 [str]: the second argument\n\n"
                "            Returns:\n"
                "                int: the result of the function\n"
                "         */"
            )]

            self.assertEqual(actual, expected)

    def test_visit_methods_basic(self):
        """
        Description: Test that visit_methods extracts method name, docstring, and line numbers.
        """

        test_code = '''
        public class TestClass {
            /**
             * Sample method JavaDoc.
             */
            public void exampleMethod() {
                int a = 1;
            }
        }
        '''

        with patch("builtins.open", mock_open(read_data=test_code)):
            sniffer = JavaScriptSniffer("Test.java")

            tree = javalang.parse.parse(test_code)
            comments = sniffer._extract_comments()

            sniffer.visit_methods(tree, comments)

            actual = sniffer.functions_list
            expected = [
                FunctionSpecs(
                    name="exampleMethod",
                    docstring="* Sample method JavaDoc.",
                    start_lineno=6,
                    end_lineno=8
                )
            ]

            self.assertEqual(actual, expected)

    def test_visit_methods_complex(self):
        """
        Description: Test that visit_methods extracts method name, docstring, and line numbers, but this
        time the method has a considerable amount of documentation and code.
        """

        test_code = '''
        public class Example {
            /**
             * Adds two integers and returns the result.
             *
             * @param a the first integer
             * @param b the second integer
             * @return the sum of a and b
             *
             * _Example_:
             * >>> add(1, 2)
             * 3
             */
            public int add(int a, int b) {
                return a + b;
            }
        }
        '''

        with patch("builtins.open", mock_open(read_data=test_code)):
            sniffer = JavaScriptSniffer("Test.java")

            tree = javalang.parse.parse(test_code)
            comments = sniffer._extract_comments()

            sniffer.visit_methods(tree, comments)

            actual = sniffer.functions_list
            expected = [
                FunctionSpecs(
                    name="add",
                    docstring="* Adds two integers and returns the result.\n"
                    "             *\n"
                    "             * @param a the first integer\n"
                    "             * @param b the second integer\n"
                    "             * @return the sum of a and b\n"
                    "             *\n"
                    "             * _Example_:\n"
                    "             * >>> add(1, 2)\n"
                    "             * 3",
                    start_lineno=14,
                    end_lineno=16
                )
            ]

            self.assertEqual(actual, expected)

    def test_run_basic(self):
        """
        Description: Test that run correctly parses the code and extracts the method information when a
        very simple script is provided.
        """

        sniffer = JavaScriptSniffer(self.script_1)
        sniffer.run()

        actual = sniffer.functions_list
        expected = [
            FunctionSpecs(
                name='randomFunction',
                docstring='* Random function that will contain the following opentelemetry resources:\n'
                '     * - span\n'
                '     * - span.setAttribute',
                start_lineno=15,
                end_lineno=25
            )
        ]

        self.assertEqual(actual, expected)

    def test_run_complex(self):
        """
        Description: Test that run correctly parses the code and extracts the method information when a
        more complex script is provided.
        """

        sniffer = JavaScriptSniffer(self.script_2)
        sniffer.run()

        actual = sniffer.functions_list
        expected = [
            FunctionSpecs(
                name='randomFunction1',
                docstring='* Random function that will perform the addition of two values.\n'
                '     *\n'
                '     * @param val1 the first value to be added\n'
                '     * @param val2 the second value to be added\n'
                '     * @return the sum of the two values',
                start_lineno=29,
                end_lineno=38
            ),
            FunctionSpecs(
                name='randomFunction2',
                docstring='* Random function that will perform the subtraction of two values.\n'
                '     *\n'
                '     * @param val1 the first value to be subtracted\n'
                '     * @param val2 the second value to be subtracted\n'
                '     * @return the difference of the two values',
                start_lineno=47,
                end_lineno=68
            ),
            FunctionSpecs(
                name='randomFunction3',
                docstring='* Random function containing three different spans.',
                start_lineno=73,
                end_lineno=96
            ),
            FunctionSpecs(
                name='randomFunction4',
                docstring='* Random function demonstrating counter usage.',
                start_lineno=101,
                end_lineno=125
            )
        ]

        self.assertEqual(actual, expected)

