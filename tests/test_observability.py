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

    def test_telemetry_detector_basic(self):
        """
        Description: check if the Telemetry Detector class is able to deal with a script that has part of
        the telemetry calls that this method is looking for.
        """
        
        detector = TelemetryDetector()
        detector.run(self.code_1)

        actual = [
            detector.tracers,
            detector.spans,
            detector.attributes,
            detector.events,
            detector.exceptions,
            detector.ends,
            detector.metrics,
            detector.metric_instruments,
            detector.metric_operations
        ]
        expected = [
            ['script_1_tracer'],
            ['random_function'],
            [
                {'attribute_1': 'value_1'},
                {'attribute_2': 'value_2'},
            ],
            [],
            False,
            False,
            [],
            [],
            [],
        ]

        self.assertEqual(actual, expected)

#     def test_telemetry_detector_visit_Call_complex(self):
#         """
#         Description: check if the visit_Call method is able to deal with a script that has multiple
#         telemetry calls of different types.
#         """
        
#         detector = TelemetryDetector()
#         detector.visit_Call(self.code_2)

#         actual = [
#             detector.tracers,
#             detector.spans,
#             detector.attributes,
#             detector.events,
#         ]
#         expected = [
#             ['__name__'], 
#             [
#                 'random_function_2',
#                 'random_function_1',
#                 'random_function_3',
#                 'load_user_from_db',
#                 'call_billing_services',
#             ],
#             [
#                 {'val1': 'val1'},
#                 {'val2': 'val2'},
#             ],
#             [
#                 {
#                     'calculation_completed': {
#                         'operation': 'subtraction',
#                         'result': 'result',
#                     }
#                 }
#             ]
#         ]

#         self.assertEqual(actual, expected)

#     # def test_telemetry_detector_visit_Call_exception(self):
#     #     pass

#     def test_telemetry_detector_visit_With_basic(self):
#         """
#         Description: check if the telemetry detector can visit the With node.
#         """

#         detector = TelemetryDetector()
#         detector.visit_With(self.code_1)

#         actual = detector.spans
#         expected = ['random_function']

#         self.assertEqual(actual, expected)

#     def test_telemetry_detector_visit_With_complex(self):
#         """
#         Description: check if the telemetry detector can visit a script containing different functions
#         containing With statements including functions that contain multiple With statements.
#         """

#         detector = TelemetryDetector()
#         detector.visit_With(self.code_2)

#         actual = detector.spans
#         expected = [
#             'random_function_1',
#             'random_function_3',
#             'call_billing_services',
#         ]

#         self.assertEqual(actual, expected)

#     def test_telemetry_detector_visit_With_exception(self):
#         """
#         Description: when the provided script is empty.
#         """

#         detector = TelemetryDetector()
#         detector.visit_With(self.code_3)

#         actual = detector.spans
#         expected = []

#         self.assertEqual(actual, expected)

#     # TODO. add tests to the visit_Call node