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
            "end",
            "get_current_span",
            "use_span",
            "set_attribute",
            "set_attributes",
            "record_exception",
            "add_event",
            "add_events",
            "create_counter",
            "create_up_down_counter",
            "create_histogram",
            "create_observable_gauge",
            "create_resource",
            "instrument"
        }

        self.assertEqual(actual, expected)