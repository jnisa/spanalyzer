# Script containing the report generation logic

def generate_report(codebase_path: str) -> dict:
    """
    Generate a report for the given codebase.

    Args:
        codebase_path: Path to the codebase to analyze

    Returns:
        A dictionary containing the report

    _Example Output_
        functions:
        - name: fetch_data
            has_span: true
            span_ended: true
            metrics_emitted: [data_fetched_total]

        - name: retry_wrapper
            has_span: true
            span_ended: false
            metrics_emitted: []

        - name: validate
            has_span: false
            span_ended: false
            metrics_emitted: []
    """

    pass

