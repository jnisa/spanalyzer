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
        test_script_4 = os.path.join(os.path.dirname(__file__), 'samples', 'script_4.py')

        self.code_1 = ast.parse(read_script(test_script_1))
        self.code_2 = ast.parse(read_script(test_script_2))
        self.code_3 = ast.parse(read_script(test_script_3))
        self.code_4 = ast.parse(read_script(test_script_4))

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
            detector.counter,
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
        ]

        self.assertEqual(actual, expected)

    def test_telemetry_detector_complex(self):
        """
        Description: check if the Telemetry Detector class is able to deal with a script that has multiple
        telemetry calls of different types.
        """
        
        detector = TelemetryDetector()
        detector.run(self.code_2)

        actual = [
            detector.tracers,
            detector.spans,
            detector.attributes,
            detector.events,
            detector.exceptions,
            detector.ends,
            detector.counter,
        ]
        expected = [
            ['__name__'], 
            [
                'random_function_2',
                'last_function',
                'random_function_1',
                'random_function_3',
                'load_user_from_db',
                'last_function',
            ],
            [
                {
                    'input_1': 'val1',
                    'input_2': 'val2'
                },
                {'val1': 'val1'},
                {'val2': 'val2'},
                {'counter_updated': True},
            ],
            [
                [
                    'calculation_completed',
                    {
                        'operation': 'subtraction',
                        'result': 'result',
                    },
                ],
                [None],
            ],
            False,
            True,
            [
                [
                    'request_counter',
                    [1],
                    [],
                ],
                [
                    'request_counter',
                    [
                        1,
                        {
                            'endpoint': '/api/v1',
                            'method': 'GET',
                        }
                    ],
                    [],
                ],
                [
                    'request_counter',
                    [2],
                    [
                        {
                            'endpoint': '/api/v1',
                            'method': 'POST',
                            'status': 'success',
                        },
                    ],
                ],
            ],
        ]

        self.assertEqual(actual, expected)

    def test_telemetry_detector_exception(self):
        """
        Description: check if the telemetry detector can visit a script that contains only async functions
        and telemetry operators that haven't been tested yet.
        """

        detector = TelemetryDetector()
        detector.run(self.code_4)

        actual = [
            detector.tracers,
            detector.spans,
            detector.attributes,
            detector.events,
            detector.exceptions,
            detector.ends,
            detector.counter,
        ]
        expected = [
            ['script_4_tracer'],
            ['fetch_data'],
            [
                {'request_type': 'async'},
                {'data_size': None},
            ],
            [],
            True,
            False,
            [],
        ]

        self.assertEqual(actual, expected)
