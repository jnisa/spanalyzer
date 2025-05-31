# Unitary tests for the Java observability module

import os

import javalang

from unittest import TestCase

from spanalyzer.constants.telemetry import TelemetryCall
from spanalyzer.java.detector import JavaTelemetryDetector


def read_script(path: str) -> str:
    """
    Read the script from the given path.
    """
    with open(path, 'r') as file:
        return file.read()


class TestJavaTelemetryDetector(TestCase):

    def setUp(self):
        """
        Set up the test case by parsing example Java scripts.
        """

        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'samples', 'java')

        self.code_1 = list(javalang.parse.parse(read_script(os.path.join(base_path, 'script_1.java'))))
        self.code_2 = list(javalang.parse.parse(read_script(os.path.join(base_path, 'script_2.java'))))
        self.code_3 = list(javalang.parse.parse(read_script(os.path.join(base_path, 'script_3.java'))))
        self.code_4 = list(javalang.parse.parse(read_script(os.path.join(base_path, 'script_4.java'))))

    def test_telemetry_detector_basic(self):
        """
        Description: Check if the JavaTelemetryDetector can detect basic OpenTelemetry calls
        from a sample Java script.
        """

        detector = JavaTelemetryDetector()

        actual = detector.run(self.code_1)
        expected = {
            'tracers': [
                TelemetryCall(func='"script_1_tracer"', line_number=8, args=None, keywords=None)
            ],
            'spans': [
                TelemetryCall(func='"random_function"', line_number=16, args=None, keywords=None)
            ],
            'attributes': [
                TelemetryCall(func='setAttribute', line_number=20, args={'method': 'setAttribute', 'qualifier': 'span', 'arguments': ['attribute_1', 'value_1']}, keywords=None),
                TelemetryCall(func='setAttribute', line_number=21, args={'method': 'setAttribute', 'qualifier': 'span', 'arguments': ['attribute_2', 'value_2']}, keywords=None)
            ],
            'events': [],
            'counter': [],
        }

        self.assertEqual(actual, expected)