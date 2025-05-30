# Unitary tests to the operations functions

import unittest

from spanalyzer.script import FunctionSpecs

from spanalyzer.constants.telemetry import TelemetryCall

from spanalyzer.utils.operations import conciliation
from spanalyzer.utils.operations import filter_empty_dict

class TestOperations(unittest.TestCase):

    def test_conciliation_basic(self):
        """
        Description: test the conciliation process with a basic dictionary to conciliate.
        """

        test_functions = [
            FunctionSpecs(
                name='function_1',
                start_lineno=1,
                end_lineno=10,
                docstring='This is a test function',
            ),
        ]

        test_telemetry = {
            'tracers': [
                TelemetryCall(func='test_tracer_1', line_number=1, args=None),
                TelemetryCall(func='test_tracer_2', line_number=24, args=None),
            ],
            'spans': [
                TelemetryCall(func='test_span_1', line_number=12, args=None),
                TelemetryCall(func='test_span_2', line_number=24, args=None),
            ],
            'attributes': [
                TelemetryCall(func='test_attribute_1', line_number=19, args=None),
                TelemetryCall(func='test_attribute_2', line_number=24, args=None),
            ],
            'events': [
                TelemetryCall(func='test_event_1', line_number=9, args=None),
                TelemetryCall(func='test_event_2', line_number=13, args=None),
            ],
        }

        actual = conciliation(test_functions, test_telemetry)
        expected = {
            'tracers': [
                TelemetryCall(func='test_tracer_2', line_number=24, args=None),
            ],
            'spans': [
                TelemetryCall(func='test_span_1', line_number=12, args=None),
                TelemetryCall(func='test_span_2', line_number=24, args=None),
            ],
            'attributes': [
                TelemetryCall(func='test_attribute_1', line_number=19, args=None),
                TelemetryCall(func='test_attribute_2', line_number=24, args=None),
            ],
            'events': [
                TelemetryCall(func='test_event_2', line_number=13, args=None),
            ],
            'functions': {
                'function_1': {
                    'docstring': 'This is a test function',
                    'tracers': [
                        TelemetryCall(func='test_tracer_1', line_number=1, args=None),
                    ],
                    'events': [
                        TelemetryCall(func='test_event_1', line_number=9, args=None),
                    ],
                },
            },
        }

        self.assertEqual(actual, expected)

    def test_conciliation_complex(self):
        """
        Description: test the conciliation process with a complex dictionary to conciliate.
        """

        test_functions = [
            FunctionSpecs(
                name='function_1',
                start_lineno=1,
                end_lineno=10,
                docstring='This is a test function 1.',
            ),
            FunctionSpecs(
                name='function_2',
                start_lineno=13,
                end_lineno=20,
                docstring='This is a test function 2.',
            ),
            FunctionSpecs(
                name='function_3',
                start_lineno=25,
                end_lineno=30,
                docstring='This is a test function 3.',
            ),
        ]
        
        test_telemetry = {
            'tracers': [
                TelemetryCall(func='test_tracer_1', line_number=2, args=None),
                TelemetryCall(func='test_tracer_2', line_number=11, args=None),
                TelemetryCall(func='test_tracer_3', line_number=21, args=None),
                TelemetryCall(func='test_tracer_4', line_number=29, args=None),
            ],
            'spans': [
                TelemetryCall(func='test_span_1', line_number=1, args=None),
                TelemetryCall(func='test_span_2', line_number=19, args=None),
                TelemetryCall(func='test_span_3', line_number=29, args=None),
            ],
            'attributes': [
                TelemetryCall(func='test_attribute_1', line_number=19, args=None),
                TelemetryCall(func='test_attribute_2', line_number=24, args=None),
            ],
            'events': [
                TelemetryCall(func='test_event_1', line_number=1, args=None),
                TelemetryCall(func='test_event_2', line_number=19, args=None),
                TelemetryCall(func='test_event_3', line_number=29, args=None),
            ],
            'counter': [
                TelemetryCall(func='test_counter_1', line_number=19, args=None),
                TelemetryCall(func='test_counter_2', line_number=22, args=None),
            ],
        }

        actual = conciliation(test_functions, test_telemetry)
        expected = {
            'tracers': [
                TelemetryCall(func='test_tracer_2', line_number=11, args=None),
                TelemetryCall(func='test_tracer_3', line_number=21, args=None),
            ],
            'attributes': [
                TelemetryCall(func='test_attribute_2', line_number=24, args=None),
            ],
            'counter': [
                TelemetryCall(func='test_counter_2', line_number=22, args=None),
            ],
            'functions': {
                'function_1': {
                    'docstring': 'This is a test function 1.',
                    'tracers': [
                        TelemetryCall(func='test_tracer_1', line_number=2, args=None),
                    ],
                    'spans': [
                        TelemetryCall(func='test_span_1', line_number=1, args=None),
                    ],
                    'events': [
                        TelemetryCall(func='test_event_1', line_number=1, args=None),
                    ],
                },
                'function_2': {
                    'docstring': 'This is a test function 2.',
                    'spans': [
                        TelemetryCall(func='test_span_2', line_number=19, args=None),
                    ],
                    'attributes': [
                        TelemetryCall(func='test_attribute_1', line_number=19, args=None),
                    ],
                    'events': [
                        TelemetryCall(func='test_event_2', line_number=19, args=None),
                    ],
                    'counter': [
                        TelemetryCall(func='test_counter_1', line_number=19, args=None),
                    ],
                },
                'function_3': {
                    'docstring': 'This is a test function 3.',
                    'tracers': [
                        TelemetryCall(func='test_tracer_4', line_number=29, args=None),
                    ],
                    'spans': [
                        TelemetryCall(func='test_span_3', line_number=29, args=None),
                    ],
                    'events': [
                        TelemetryCall(func='test_event_3', line_number=29, args=None),
                    ],
                },
            },
        }

        self.assertEqual(actual, expected)

    def test_filter_empty(self):
        """
        Description: test the filtering process with a basic dictionary to filter.
        """

        test_dict = {
            'key_1': 'value_1',
            'key_2': None,
            'key_3': [],
            'key_4': {},
            'key_5': {
                'key_6': 'value_6',
                'key_7': None,
                'key_8': [],
                'key_9': {},
            },
        }


        actual = filter_empty_dict(test_dict)
        expected = {
            'key_1': 'value_1',
            'key_5': {
                'key_6': 'value_6',
            },
        }

        self.assertEqual(actual, expected)

    def test_filter_empty_exception(self):
        """
        Description: test the filtering process with a dictionary that it's empty.
        """

        test_dict = {}

        actual = filter_empty_dict(test_dict)
        expected = {}

        self.assertEqual(actual, expected)