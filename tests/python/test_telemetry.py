# Unitary test to the telemetry constants

from unittest import TestCase

from spanalyzer.constants.telemetry import TelemetryCall

from spanalyzer.python.constants.keywords import PythonTelemetryKeywords

class TestPythonTelemetryKeywords(TestCase):

    def test_telemetry_call_dict(self):
        """
        Description: test the dictionary conversion of the TelemetryCall class.
        """

        test_call = TelemetryCall(func='test_func', line_number=1, args=None, keywords=None)

        actual = test_call.__dict__()
        expected = {
            'func': 'test_func',
            'line_number': 1,
            'args': None,
            'keywords': None,
        }

        self.assertEqual(actual, expected)

    def test_telemetry_keywords_values(self):
        """
        Description: check if the values of the PythonTelemetryKeywords enum are duly encapsulated in
        a set.
        """

        actual = PythonTelemetryKeywords.values()
        expected = {
            "get_tracer",
            "start_as_current_span",
            "start_span",
            "get_current_span",
            "use_span",
            "set_attribute",
            "set_attributes",
            "add_event",
            "add_events",
            "add",
            "instrument"
        }

        self.assertEqual(actual, expected)