# Unitary tests for the observability module

import os

import ast

from unittest import TestCase

from spanalyzer.observability import TelemetryDetector

def read_script(path: str) -> str:
    """
    Read the script from the given path.

    Args:
        path [str]: the path to the script

    Returns:
        str: the script content
    """

    with open(path, 'r') as file:
        return file.read()

class TestTelemetrySniffer(TestCase):
    
    def setUp(self):
        """
        Set up the test case.
        """

        test_script_1 = os.path.join(os.path.dirname(__file__), 'samples', 'script_1.py')
        test_script_2 = os.path.join(os.path.dirname(__file__), 'samples', 'script_2.py')
        test_script_3 = os.path.join(os.path.dirname(__file__), 'samples', 'script_3.py')

        self.code_1 = ast.parse(read_script(test_script_1))
        self.code_2 = ast.parse(read_script(test_script_2))
        self.code_3 = ast.parse(read_script(test_script_3))

    def test_telemetry_sniffer_test_case_1(self):
        """
        Description: check if the telemetry sniffer can capture a script containing one single span and two set_attribute calls.
        """

        detector = TelemetryDetector(self.code_1)
        detector.run()

        actual = len(detector.attributes)
        expected = 2

        self.assertEqual(actual, expected)