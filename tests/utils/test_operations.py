# Unitary tests to the operations functions

import unittest

from spanalyzer.python.script import FunctionSpecs

from spanalyzer.constants.telemetry import TelemetryCall

from spanalyzer.utils.operations import folder_trim
from spanalyzer.utils.operations import conciliation
from spanalyzer.utils.operations import filter_empty_dict
from spanalyzer.utils.operations import remove_call_duplicates


class TestOperations(unittest.TestCase):
    def test_conciliation_basic(self):
        """
        Description: test the conciliation process with a basic dictionary to conciliate.
        """

        test_functions = [
            FunctionSpecs(
                name="function_1",
                start_lineno=1,
                end_lineno=10,
                docstring="This is a test function",
            ),
        ]

        test_telemetry = {
            "tracers": [
                {"func": "test_tracer_1", "line_number": 1, "args": None},
                {"func": "test_tracer_2", "line_number": 24, "args": None},
            ],
            "spans": [
                {"func": "test_span_1", "line_number": 12, "args": None},
                {"func": "test_span_2", "line_number": 24, "args": None},
            ],
            "attributes": [
                {"func": "test_attribute_1", "line_number": 19, "args": None},
                {"func": "test_attribute_2", "line_number": 24, "args": None},
            ],
            "events": [
                {"func": "test_event_1", "line_number": 9, "args": None},
                {"func": "test_event_2", "line_number": 13, "args": None},
            ],
        }

        actual = conciliation(test_functions, test_telemetry)
        expected = {
            "tracers": [
                {"func": "test_tracer_2", "line_number": 24, "args": None},
            ],
            "spans": [
                {"func": "test_span_1", "line_number": 12, "args": None},
                {"func": "test_span_2", "line_number": 24, "args": None},
            ],
            "attributes": [
                {"func": "test_attribute_1", "line_number": 19, "args": None},
                {"func": "test_attribute_2", "line_number": 24, "args": None},
            ],
            "events": [
                {"func": "test_event_2", "line_number": 13, "args": None},
            ],
            "functions": {
                "function_1": {
                    "docstring": "This is a test function",
                    "tracers": [
                        {"func": "test_tracer_1", "line_number": 1, "args": None},
                    ],
                    "events": [
                        {"func": "test_event_1", "line_number": 9, "args": None},
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
                name="function_1",
                start_lineno=1,
                end_lineno=10,
                docstring="This is a test function 1.",
            ),
            FunctionSpecs(
                name="function_2",
                start_lineno=13,
                end_lineno=20,
                docstring="This is a test function 2.",
            ),
            FunctionSpecs(
                name="function_3",
                start_lineno=25,
                end_lineno=30,
                docstring="This is a test function 3.",
            ),
        ]

        test_telemetry = {
            "tracers": [
                {"func": "test_tracer_1", "line_number": 2, "args": None},
                {"func": "test_tracer_2", "line_number": 11, "args": None},
                {"func": "test_tracer_3", "line_number": 21, "args": None},
                {"func": "test_tracer_4", "line_number": 29, "args": None},
            ],
            "spans": [
                {"func": "test_span_1", "line_number": 1, "args": None},
                {"func": "test_span_2", "line_number": 19, "args": None},
                {"func": "test_span_3", "line_number": 29, "args": None},
            ],
            "attributes": [
                {"func": "test_attribute_1", "line_number": 19, "args": None},
                {"func": "test_attribute_2", "line_number": 24, "args": None},
            ],
            "events": [
                {"func": "test_event_1", "line_number": 1, "args": None},
                {"func": "test_event_2", "line_number": 19, "args": None},
                {"func": "test_event_3", "line_number": 29, "args": None},
            ],
            "counter": [
                {"func": "test_counter_1", "line_number": 19, "args": None},
                {"func": "test_counter_2", "line_number": 22, "args": None},
            ],
        }

        actual = conciliation(test_functions, test_telemetry)
        expected = {
            "tracers": [
                {"func": "test_tracer_2", "line_number": 11, "args": None},
                {"func": "test_tracer_3", "line_number": 21, "args": None},
            ],
            "attributes": [
                {"func": "test_attribute_2", "line_number": 24, "args": None},
            ],
            "counter": [
                {"func": "test_counter_2", "line_number": 22, "args": None},
            ],
            "functions": {
                "function_1": {
                    "docstring": "This is a test function 1.",
                    "tracers": [
                        {"func": "test_tracer_1", "line_number": 2, "args": None},
                    ],
                    "spans": [
                        {"func": "test_span_1", "line_number": 1, "args": None},
                    ],
                    "events": [
                        {"func": "test_event_1", "line_number": 1, "args": None},
                    ],
                },
                "function_2": {
                    "docstring": "This is a test function 2.",
                    "spans": [
                        {"func": "test_span_2", "line_number": 19, "args": None},
                    ],
                    "attributes": [
                        {"func": "test_attribute_1", "line_number": 19, "args": None},
                    ],
                    "events": [
                        {"func": "test_event_2", "line_number": 19, "args": None},
                    ],
                    "counter": [
                        {"func": "test_counter_1", "line_number": 19, "args": None},
                    ],
                },
                "function_3": {
                    "docstring": "This is a test function 3.",
                    "tracers": [
                        {"func": "test_tracer_4", "line_number": 29, "args": None},
                    ],
                    "spans": [
                        {"func": "test_span_3", "line_number": 29, "args": None},
                    ],
                    "events": [
                        {"func": "test_event_3", "line_number": 29, "args": None},
                    ],
                },
            },
        }

        self.assertEqual(actual, expected)

    def test_filter_empty_dict(self):
        """
        Description: test the filtering process with a basic dictionary to filter.
        """

        test_dict = {
            "key_1": "value_1",
            "key_2": None,
            "key_3": [],
            "key_4": {},
            "key_5": {
                "key_6": "value_6",
                "key_7": None,
                "key_8": [],
                "key_9": {},
            },
        }

        actual = filter_empty_dict(test_dict)
        expected = {
            "key_1": "value_1",
            "key_5": {
                "key_6": "value_6",
            },
        }

        self.assertEqual(actual, expected)

    def test_filter_empty_dict_exception(self):
        """
        Description: test the filtering process with a dictionary that it's empty.
        """

        test_dict = {}

        actual = filter_empty_dict(test_dict)
        expected = {}

        self.assertEqual(actual, expected)

    def test_remove_call_duplicates(self):
        """
        Description: test the removal of duplicates from a list of telemetry calls.
        """

        test_lst = [
            TelemetryCall(func="test_tracer_1", line_number=1, args=None),
            TelemetryCall(func="test_tracer_2", line_number=1, args=None),
            TelemetryCall(func="test_tracer_3", line_number=2, args=None),
            TelemetryCall(func="test_tracer_1", line_number=1, args=None),
            TelemetryCall(func="test_tracer_2", line_number=1, args=None),
        ]

        actual = remove_call_duplicates(test_lst)
        expected = [
            TelemetryCall(func="test_tracer_1", line_number=1, args=None),
            TelemetryCall(func="test_tracer_3", line_number=2, args=None),
        ]

        self.assertEqual(actual, expected)

    def test_folder_trim(self):
        """
        Description: test if the function is able to perform the trim in a very nested folder
        structure.
        """

        test_lst = [
            {"script": "path/to/the/folder/subfolder/script.py", "attribute_1": "val1"},
            {"script": "path/to/the/folder/script1.py", "attribute_2": "val2"},
            {
                "script": "path/to/the/folder/subfolder/subsubfolder/script.py",
                "attribute_3": "val3",
            },
            {"script": "path/to/the/folder/script2.py", "attribute_4": "val4"},
        ]

        actual = folder_trim(test_lst, folder_key="script")
        expected = [
            {"script": "folder/subfolder/script.py", "attribute_1": "val1"},
            {"script": "folder/script1.py", "attribute_2": "val2"},
            {
                "script": "folder/subfolder/subsubfolder/script.py",
                "attribute_3": "val3",
            },
            {"script": "folder/script2.py", "attribute_4": "val4"},
        ]

        self.assertEqual(actual, expected)
