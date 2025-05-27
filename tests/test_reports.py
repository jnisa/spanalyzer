# Unitary tests for the reports module

from unittest import TestCase

from spanalyzer.reports import terminal_report

class TestReports(TestCase):

    def compare_terminal_reports(self, actual, expected):
        """
        Compares the actual and expected terminal reports.

        Comparing the actual and expected terminal reports line by line to avoid the comparison
        of the strings directly because of the formatting.
        """

        actual = actual.split('\n')
        expected = expected.split('\n')

        for a, e in zip(actual, expected):
            self.assertEqual(a, e)
        

    def test_detailed_report_basic(self):
        """
        Description: when there's only one record to report.
        """

        pass

    def test_detailed_report_complex(self):
        """
        Description: when there's multiple records to report.
        """

        pass

    def test_detailed_report_exception(self):
        """
        Description: when there's an exception in the report generation.
        """

        pass

    def test_terminal_report_basic(self):
        """
        Description: when there's only one record to report.
        """

        test_report = [
            {'script': 'test_program.py', 'spans': True, 'traces': True, 'metrics': True, 'events': True, 'attributes': True, 'coverage': 100}
        ]

        actual = terminal_report(test_report)
        expected = """Script                     Spans    Traces    Metrics    Events    Attributes    Coverage   
--------------------------------------------------------------------------------------------
test_program.py            ✓        ✓         ✓          ✓         ✓             100%       
--------------------------------------------------------------------------------------------"""

        breakpoint()

        self.compare_terminal_reports(actual, expected)

    def test_terminal_report_complex(self):
        """
        Description: when there's multiple records to report.
        """

        test_report = [
            {'name': 'program_1.py', 'attribute_1': True, 'attribute_2': True, 'attribute_3': False, 'attribute_4': True, 'attribute_5': False, 'attribute_6': 74},
            {'name': 'program_2.py', 'attribute_1': False, 'attribute_2': False, 'attribute_3': False, 'attribute_4': True, 'attribute_5': True, 'attribute_6': 63},
            {'name': 'program_3.py', 'attribute_1': True, 'attribute_2': True, 'attribute_3': True, 'attribute_4': True, 'attribute_5': True, 'attribute_6': 82},
        ]

        actual = terminal_report(test_report)
        expected = """Name                       Attribute_1    Attribute_2    Attribute_3    Attribute_4    Attribute_5    Attribute_6   
--------------------------------------------------------------------------------------------------------------------
program_1.py               ✓              ✓              ✗              ✓              ✗              74%           
program_2.py               ✗              ✗              ✗              ✓              ✓              63%           
program_3.py               ✓              ✓              ✓              ✓              ✓              82%           
--------------------------------------------------------------------------------------------------------------------"""

        self.compare_terminal_reports(actual, expected)

    def test_terminal_report_exception(self):
        """
        Description: when the provided data is empty.
        """

        test_report = [{}]
        actual = terminal_report(test_report)
        expected = ""

        self.compare_terminal_reports(actual, expected)
