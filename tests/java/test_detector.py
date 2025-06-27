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
    with open(path, "r") as file:
        return file.read()


class TestJavaTelemetryDetector(TestCase):
    def setUp(self):
        """
        Set up the test case by parsing example Java scripts.
        """

        base_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "samples", "java"
        )

        self.code_1 = list(
            javalang.parse.parse(read_script(os.path.join(base_path, "script_1.java")))
        )
        self.code_2 = list(
            javalang.parse.parse(read_script(os.path.join(base_path, "script_2.java")))
        )
        self.code_3 = list(
            javalang.parse.parse(read_script(os.path.join(base_path, "script_3.java")))
        )
        self.code_4 = list(
            javalang.parse.parse(read_script(os.path.join(base_path, "script_4.java")))
        )

    def test_telemetry_detector_basic(self):
        """
        Description: Check if the JavaTelemetryDetector can detect basic OpenTelemetry calls
        from a sample Java script.
        """

        detector = JavaTelemetryDetector()

        actual = detector.run(self.code_1)
        expected = {
            "tracers": [
                TelemetryCall(
                    func='"script_1_tracer"', line_number=8, args=None, keywords=None
                )
            ],
            "spans": [
                TelemetryCall(
                    func='"random_function"', line_number=16, args=None, keywords=None
                )
            ],
            "attributes": [
                TelemetryCall(
                    func="setAttribute",
                    line_number=20,
                    args={
                        "method": "setAttribute",
                        "qualifier": "span",
                        "arguments": ["attribute_1", "value_1"],
                        "selectors": None,
                    },
                    keywords=None,
                ),
                TelemetryCall(
                    func="setAttribute",
                    line_number=21,
                    args={
                        "method": "setAttribute",
                        "qualifier": "span",
                        "arguments": ["attribute_2", "value_2"],
                        "selectors": None,
                    },
                    keywords=None,
                ),
            ],
            "events": [],
            "counter": [],
        }

        self.assertEqual(actual, expected)

    def test_telemetry_detector_complex(self):
        """
        Description: Check if the JavaTelemetryDetector can detect complex OpenTelemetry calls
        from a sample Java script.
        """

        detector = JavaTelemetryDetector()

        actual = detector.run(self.code_2)
        expected = {
            "tracers": [
                TelemetryCall(
                    func="ClassReference(postfix_operators=[], prefix_operators=[], qualifier=, selectors=[MethodInvocation(arguments=[], member=getName, postfix_operators=None, prefix_operators=None, qualifier=None, selectors=None, type_arguments=None)], type=ReferenceType(arguments=None, dimensions=None, name=Script2, sub_type=None))",
                    line_number=14,
                    args=None,
                    keywords=None,
                )
            ],
            "spans": [
                TelemetryCall(
                    func='"random_function_1"', line_number=30, args=None, keywords=None
                ),
                TelemetryCall(
                    func='"random_function_2"', line_number=48, args=None, keywords=None
                ),
                TelemetryCall(
                    func='"random_function_3"', line_number=74, args=None, keywords=None
                ),
                TelemetryCall(
                    func='"load_user_from_db"', line_number=76, args=None, keywords=None
                ),
                TelemetryCall(
                    func='"last_function"', line_number=94, args=None, keywords=None
                ),
                TelemetryCall(
                    func='"last_function"', line_number=102, args=None, keywords=None
                ),
            ],
            "attributes": [
                TelemetryCall(
                    func="setAttribute",
                    line_number=32,
                    args={
                        "method": "setAttribute",
                        "qualifier": "span",
                        "arguments": ["val1", "val1"],
                        "selectors": None,
                    },
                    keywords=None,
                ),
                TelemetryCall(
                    func="setAttribute",
                    line_number=33,
                    args={
                        "method": "setAttribute",
                        "qualifier": "span",
                        "arguments": ["val2", "val2"],
                        "selectors": None,
                    },
                    keywords=None,
                ),
                TelemetryCall(
                    func="setAttributes",
                    line_number=50,
                    args={
                        "method": "setAttributes",
                        "qualifier": "span",
                        "arguments": [
                            {
                                "method": "builder",
                                "qualifier": "Attributes",
                                "arguments": [],
                                "selectors": [
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": ["input_1", "val1"],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": ["input_2", "val2"],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "build",
                                        "qualifier": None,
                                        "arguments": [],
                                        "selectors": None,
                                    },
                                ],
                            }
                        ],
                        "selectors": None,
                    },
                    keywords=None,
                ),
                TelemetryCall(
                    func="setAttribute",
                    line_number=120,
                    args={
                        "method": "setAttribute",
                        "qualifier": "span",
                        "arguments": ["counter_updated", "true"],
                        "selectors": None,
                    },
                    keywords=None,
                ),
            ],
            "events": [
                TelemetryCall(
                    func="addEvent",
                    line_number=60,
                    args={
                        "method": "addEvent",
                        "qualifier": "span",
                        "arguments": [
                            "calculation_completed",
                            {
                                "method": "builder",
                                "qualifier": "Attributes",
                                "arguments": [],
                                "selectors": [
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": ["operation", "subtraction"],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": [
                                            "result",
                                            {
                                                "method": "valueOf",
                                                "qualifier": "String",
                                                "arguments": ["result"],
                                                "selectors": None,
                                            },
                                        ],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "build",
                                        "qualifier": None,
                                        "arguments": [],
                                        "selectors": None,
                                    },
                                ],
                            },
                        ],
                        "selectors": None,
                    },
                    keywords=None,
                ),
                TelemetryCall(
                    func="addEvent",
                    line_number=78,
                    args={
                        "method": "addEvent",
                        "qualifier": "loadUserSpan",
                        "arguments": [
                            "operation_started",
                            {
                                "method": "builder",
                                "qualifier": "Attributes",
                                "arguments": [],
                                "selectors": [
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": [
                                            "timestamp",
                                            {
                                                "method": "now",
                                                "qualifier": "Instant",
                                                "arguments": [],
                                                "selectors": [
                                                    {
                                                        "method": "toString",
                                                        "qualifier": None,
                                                        "arguments": [],
                                                        "selectors": None,
                                                    }
                                                ],
                                            },
                                        ],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": [
                                            "description",
                                            "Load User from DB",
                                        ],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "build",
                                        "qualifier": None,
                                        "arguments": [],
                                        "selectors": None,
                                    },
                                ],
                            },
                        ],
                        "selectors": None,
                    },
                    keywords=None,
                ),
                TelemetryCall(
                    func="addEvent",
                    line_number=83,
                    args={
                        "method": "addEvent",
                        "qualifier": "loadUserSpan",
                        "arguments": [
                            "operation_completed",
                            {
                                "method": "builder",
                                "qualifier": "Attributes",
                                "arguments": [],
                                "selectors": [
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": [
                                            "timestamp",
                                            {
                                                "method": "now",
                                                "qualifier": "Instant",
                                                "arguments": [],
                                                "selectors": [
                                                    {
                                                        "method": "toString",
                                                        "qualifier": None,
                                                        "arguments": [],
                                                        "selectors": None,
                                                    }
                                                ],
                                            },
                                        ],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": [
                                            "description",
                                            "User loaded from DB",
                                        ],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "build",
                                        "qualifier": None,
                                        "arguments": [],
                                        "selectors": None,
                                    },
                                ],
                            },
                        ],
                        "selectors": None,
                    },
                    keywords=None,
                ),
            ],
            "counter": [
                TelemetryCall(
                    func="add",
                    line_number=105,
                    args={
                        "method": "add",
                        "qualifier": "requestCounter",
                        "arguments": ["1"],
                        "selectors": None,
                    },
                    keywords=None,
                ),
                TelemetryCall(
                    func="add",
                    line_number=108,
                    args={
                        "method": "add",
                        "qualifier": "requestCounter",
                        "arguments": [
                            "1",
                            {
                                "method": "builder",
                                "qualifier": "Attributes",
                                "arguments": [],
                                "selectors": [
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": ["endpoint", "/api/v1"],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": ["method", "GET"],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "build",
                                        "qualifier": None,
                                        "arguments": [],
                                        "selectors": None,
                                    },
                                ],
                            },
                        ],
                        "selectors": None,
                    },
                    keywords=None,
                ),
                TelemetryCall(
                    func="add",
                    line_number=114,
                    args={
                        "method": "add",
                        "qualifier": "requestCounter",
                        "arguments": [
                            "2",
                            {
                                "method": "builder",
                                "qualifier": "Attributes",
                                "arguments": [],
                                "selectors": [
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": ["endpoint", "/api/v1"],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": ["method", "POST"],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": ["status", "success"],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "build",
                                        "qualifier": None,
                                        "arguments": [],
                                        "selectors": None,
                                    },
                                ],
                            },
                        ],
                        "selectors": None,
                    },
                    keywords=None,
                ),
            ],
        }

        self.assertEqual(actual, expected)

    def test_telemetry_detector_exception(self):
        """
        Description: Check if the telemetry detector can visit a script that contains only async functions
        and telemetry operators that haven't been tested yet.
        """

        detector = JavaTelemetryDetector()

        actual = detector.run(self.code_4)
        expected = {
            "tracers": [
                TelemetryCall(
                    func='"script_4_tracer"', line_number=15, args=None, keywords=None
                )
            ],
            "spans": [
                TelemetryCall(
                    func='"fetch_data"', line_number=55, args=None, keywords=None
                )
            ],
            "attributes": [
                TelemetryCall(
                    func="setAttribute",
                    line_number=59,
                    args={
                        "method": "setAttribute",
                        "qualifier": "span",
                        "arguments": ["request_type", "async"],
                        "selectors": None,
                    },
                    keywords=None,
                ),
                TelemetryCall(
                    func="setAttribute",
                    line_number=63,
                    args={
                        "method": "setAttribute",
                        "qualifier": "span",
                        "arguments": [
                            "data_size",
                            {
                                "method": "get",
                                "qualifier": "rawData",
                                "arguments": ["data"],
                                "selectors": [
                                    {
                                        "method": "size",
                                        "qualifier": None,
                                        "arguments": [],
                                        "selectors": None,
                                    }
                                ],
                            },
                        ],
                        "selectors": None,
                    },
                    keywords=None,
                ),
            ],
            "events": [
                TelemetryCall(
                    func="addEvent",
                    line_number=67,
                    args={
                        "method": "addEvent",
                        "qualifier": "span",
                        "arguments": [
                            "data_processed",
                            {
                                "method": "builder",
                                "qualifier": "Attributes",
                                "arguments": [],
                                "selectors": [
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": [
                                            "input_size",
                                            {
                                                "method": "get",
                                                "qualifier": "rawData",
                                                "arguments": ["data"],
                                                "selectors": [
                                                    {
                                                        "method": "size",
                                                        "qualifier": None,
                                                        "arguments": [],
                                                        "selectors": None,
                                                    }
                                                ],
                                            },
                                        ],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "put",
                                        "qualifier": None,
                                        "arguments": [
                                            "output_size",
                                            {
                                                "method": "size",
                                                "qualifier": "processedData",
                                                "arguments": [],
                                                "selectors": None,
                                            },
                                        ],
                                        "selectors": None,
                                    },
                                    {
                                        "method": "build",
                                        "qualifier": None,
                                        "arguments": [],
                                        "selectors": None,
                                    },
                                ],
                            },
                        ],
                        "selectors": None,
                    },
                    keywords=None,
                )
            ],
            "counter": [],
        }

        self.assertEqual(actual, expected)

    def test_telemetry_detector_empty_script(self):
        """
        Description: Check if the telemetry detector can visit an empty script.
        """

        detector = JavaTelemetryDetector()

        actual = detector.run(self.code_3)
        expected = {
            "tracers": [],
            "spans": [],
            "attributes": [],
            "events": [],
            "counter": [],
        }

        self.assertEqual(actual, expected)
