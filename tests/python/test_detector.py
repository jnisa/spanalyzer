# Unitary tests for the observability module

import os

import ast

from unittest import TestCase

from spanalyzer.constants.telemetry import TelemetryCall
from spanalyzer.python.detector import PythonTelemetryDetector


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

class TestPythonTelemetryDetector(TestCase):
    
    def setUp(self):
        """
        Set up the test case.
        """

        test_script_1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'samples', 'python', 'script_1.py')
        test_script_2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'samples', 'python', 'script_2.py')
        test_script_3 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'samples', 'python', 'script_3.py')
        test_script_4 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'samples', 'python', 'script_4.py')

        self.code_1 = ast.parse(read_script(test_script_1))
        self.code_2 = ast.parse(read_script(test_script_2))
        self.code_3 = ast.parse(read_script(test_script_3))
        self.code_4 = ast.parse(read_script(test_script_4))

    def test_telemetry_detector_basic(self):
        """
        Description: check if the Telemetry Detector class is able to deal with a script that has part of
        the telemetry calls that this method is looking for.
        """
        
        detector = PythonTelemetryDetector()
        
        
        actual = detector.run(self.code_1)
        expected = {
            'tracers': [
                TelemetryCall(func='script_1_tracer', line_number=5, args=None)
            ],
            'spans': [
                TelemetryCall(func='random_function', line_number=14, args=None)
            ],
            'attributes': [
                TelemetryCall(func='set_attribute', line_number=15, args={'func': 'span.set_attribute', 'args': ['attribute_1', 'value_1']}),
                TelemetryCall(func='set_attribute', line_number=16, args={'func': 'span.set_attribute', 'args': ['attribute_2', 'value_2']})
            ],
            'events': [],
            'counter': [],
        }

        self.assertEqual(actual, expected)

    def test_telemetry_detector_complex(self):
        """
        Description: check if the Telemetry Detector class is able to deal with a script that has multiple
        telemetry calls of different types.
        """
        
        detector = PythonTelemetryDetector()

        actual = detector.run(self.code_2)
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

        expected = {
            'tracers': [
                TelemetryCall(func='__name__', line_number=8, args=None)
            ],
            'spans': [
                TelemetryCall(func='random_function_2', line_number=57, args=None, keywords=None),
                TelemetryCall(func='last_function', line_number=86, args=None, keywords=None),
                TelemetryCall(func='random_function_1', line_number=34, args=None, keywords=None),
                TelemetryCall(func='random_function_3', line_number=78, args=None, keywords=None),
                TelemetryCall(func='load_user_from_db', line_number=80, args=None, keywords=None),
                TelemetryCall(func='last_function', line_number=94, args=None, keywords=None),
            ],
            'attributes': [
                TelemetryCall(func='set_attributes', line_number=58, args={'func': 'span.set_attributes', 'args': [{'input_1': 'val1', 'input_2': 'val2'}]}),
                TelemetryCall(func='set_attribute', line_number=35, args={'func': 'span.set_attribute', 'args': ['val1', 'val1']}),
                TelemetryCall(func='set_attribute', line_number=36, args={'func': 'span.set_attribute', 'args': ['val2', 'val2']}),
                TelemetryCall(func='set_attribute', line_number=108, args={'func': 'span.set_attribute', 'args': ['counter_updated', True]}),
            ],
            'events': [
                TelemetryCall(func='add_event', line_number=65, args={'func': 'span.add_event', 'args': [
                    'calculation_completed',
                    {
                        'operation': 'subtraction',
                        'result': 'result'
                    }
                ]}),
                TelemetryCall(func='add_events', line_number=81, args={
                    'func': 'load_user_span.add_events', 'args': [[
                        {
                            'name': 'operation_started',
                            'timestamp': {
                                'func': 'time.time',
                                'args': [],
                            },
                            'description': 'Load User from DB'
                        },
                        {
                            'name': 'operation_completed',
                            'timestamp': {
                                'func': 'time.time',
                                'args': [],
                            },
                            'description': 'User loaded from DB'
                        }
                    ]]
                }),
            ],
            'counter': [
                TelemetryCall(
                    func='add', 
                    line_number=95, 
                    args={
                        'func': 'request_counter.add',
                        'args': [1], 
                    },
                    keywords=None
                ),
                TelemetryCall(
                    func='add',
                    line_number=97,
                    args={
                        'func': 'request_counter.add',
                        'args': [
                            1, 
                            {'endpoint': '/api/v1', 'method': 'GET'}
                        ],
                    },
                    keywords=None
                ),
                TelemetryCall(
                    func='add',
                    line_number=102,
                    args={
                        'func': 'request_counter.add',
                        'args': [2], 
                        'keywords': {
                            'attributes': {
                                'endpoint': '/api/v1', 
                                'method': 'POST', 
                                'status': 'success'
                            }
                        }
                    },
                    keywords=None
                )
            ]
        }

        self.assertEqual(actual, expected)

    def test_telemetry_detector_exception(self):
        """
        Description: check if the telemetry detector can visit a script that contains only async functions
        and telemetry operators that haven't been tested yet.
        """

        detector = PythonTelemetryDetector()

        actual = detector.run(self.code_4)
        expected = {
            'tracers': [
                TelemetryCall(func='script_4_tracer', line_number=10, args=None)
            ],
            'spans': [
                TelemetryCall(func='fetch_data', line_number=26, args=None)
            ],
            'attributes': [
                TelemetryCall(
                    func='set_attribute',
                    line_number=27, 
                    args={
                        'func': 'span.set_attribute',
                        'args': ['request_type', 'async'
                    ]}
                ),
                TelemetryCall(
                    func='set_attribute',
                    line_number=30,
                    args={
                        'func': 'span.set_attribute', 
                        'args': [
                            'data_size', 
                            {
                                'func': 'len', 
                                'args': ['raw_data']
                            }
                        ]
                    }
                ),
            ],
            'events': [
                TelemetryCall(
                    func='add_event',
                    line_number=33,
                    args={
                        'func': 'span.add_event',
                        'args': [
                            'data_processed',
                            {
                                'input_size': {
                                    'func': 'len',
                                    'args': ['raw_data']
                                },
                                'output_size': {
                                    'func': 'len',
                                    'args': ['processed_data']
                                }
                            }
                        ]
                    }
                ),
            ],
            'counter': [],
        }

        self.assertEqual(actual, expected)
