# Script containing the report generation logic

from typing import Any
from typing import List
from typing import Dict

class ReportSymbols:
    """Symbols used in report formatting."""
    TRUE = "✓"
    FALSE = "✗"
    PERCENTAGE = "%"

# TODO. not sure if we want to include a landing zone for the repoert to be stored on
# TODO. update the output, a function can have multiple spans
def detailed_report(codebase_path: str) -> dict:
    """
    Generate a report for the given codebase.

    Args:
        codebase_path: Path to the codebase to analyze

    Returns:
        A dictionary containing the report

    _Example Output_        
        - file_path: /path/to/file.py
        functions:
        - name: fetch_data
            span_id: span_1
            span_type: context_manager
            has_span: true
            span_ended: true
            exceptions_recorded: true
            metrics_emitted: [data_fetched_total]
            events_emitted: [data_fetched_event]
            attributes: [data_fetched_attribute]

        - name: retry_wrapper
            span_id: span_2
            span_type: manual
            has_span: true
            span_ended: false
            exceptions_recorded: false
            metrics_emitted: []
            events_emitted: []
            attributes: []

        - name: validate
            has_span: false
            span_ended: false
            exceptions_recorded: false
            metrics_emitted: []
            events_emitted: []
            attributes: []
    """

    pass

def terminal_report(data: List[Dict]) -> str:
    """
    Generates a coverage report table similar to coverage.py output.

    _Example Output_
    Name                         Spans   Traces   Metrics   Events   Attributes   Coverage
    --------------------------------------------------------------------------------------
    my_program.py                True    True     True      True     True         100%
    my_other_module.py           True    True     False     False    False        73%
    --------------------------------------------------------------------------------------

    Args:
        data (list of dict): list of dicts, each dict will be the equivalent of a row in the table.

    Returns:
        str: A formatted string representing the table.
    """

    def format_value(value: Any) -> str:
        """
        Depending on the type of the value, it will be formatted differently.

        Args:
            value (Any): The value to be formatted.

        Returns:
            str: The formatted value.
        """

        if isinstance(value, bool):
            return ReportSymbols.TRUE if value else ReportSymbols.FALSE
        elif isinstance(value, int):
            return f'{value}%'
        else:
            return str(value)

    def record_builder(values: List[str], is_header: bool = False, widths: List[int] = None) -> str:
        """
        Builds the record/row for the terminal report.

        Additionally, if the record is a header, the function will not only return the formatted string
        but also the widths of the columns.

        Args:
            values (list of str): The values to be displayed in the report.
            is_header (bool): Whether the record is a header.
            widths (list of int): The widths of the columns.

        Returns:
            str: A formatted string representing the header.
        """

        widths = [26 if idx == 0 else len(val)+3 for idx, val in enumerate(values)] if widths is None else widths
        formatted_values = [format_value(v) for v in values]
        return " ".join(f"{v:<{w}}" for v, w in zip(formatted_values, widths)), widths

    report_records = []

    headers_lst = [entry.capitalize() for entry in data[0].keys()]
    header, widths = record_builder(headers_lst, True)
    report_records.append(header)
    report_records.append('-' * len(header))

    for entry in data:
        record, _ = record_builder([entry[key] for key in data[0].keys()], False, widths)
        report_records.append(record)

    report_records.append('-' * len(header))

    return '\n'.join(report_records)

