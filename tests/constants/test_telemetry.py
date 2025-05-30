# Unitary test to the telemetry constants

from unittest import TestCase

from spanalyzer.constants.telemetry import TelemetryKeywords

class TestTelemetryKeywords(TestCase):

    def test_telemetry_keywords_values(self):
        """
        Description: check if the values of the TelemetryKeywords enum are duly encapsulated in
        a set.
        """

        actual = TelemetryKeywords.values()
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