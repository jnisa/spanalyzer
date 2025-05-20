# Script containing the routines that will be sniffing the telemetry calls in a script

import ast
from ast import Call
from ast import Name
from ast import Attribute
from ast import NodeVisitor

# TODO. this will be necessary eventually
# from spanalyzer.constants.telemetry import TelemetryKeywords

class TelemetryDetector(NodeVisitor):
    """
    This class will be used to sniff the telemetry calls in a script.

    It will be used to capture the telemetry calls in a script and return the list of telemetry calls.

    Args:
        function_code [str]: the code of the function to be analyzed
        trace_keywords [List[str]]: the list of trace keywords to be analyzed
    """

    def __init__(self, source_code):
        self.source_code = source_code
        
        # TODO. not sure if we should have namedtuple for this
        self.tracers = set()
        self.spans = set()
        self.attributes = []

    # TODO. there might be other patterns that we should be capturing

    def visit_Assign(self, node):
        """
        Visit the assign node and capture the tracer = trace.get_tracer(...) call.

        Args:
            node [ast.Assign]: the assign node
        """

        if (isinstance(node.value, Call) and
            isinstance(node.value.func, Attribute) and
            node.value.func.attr == "get_tracer"):

            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.tracers.add(target.id)

        self.generic_visit(node)

    def visit_With(self, node):
        """
        Visit the with node and capture the span.start_as_current_span(...) call.

        Args:
            node [ast.With]: the with node
        """

        for item in node.items:
            context_expr = item.context_expr
            if isinstance(context_expr, Call) and isinstance(context_expr.func, Attribute):
                if context_expr.func.attr == "start_as_current_span":
                    if isinstance(context_expr.func.value, Name):
                        tracer_name = context_expr.func.value.id
                        if tracer_name in self.tracers:
                            if item.optional_vars and isinstance(item.optional_vars, Name):
                                self.spans.add(item.optional_vars.id)

        self.generic_visit(node)

    def visit_Call(self, node: Call):
        """
        Visit the call node and capture the span.set_attribute(...) call.

        Args:
            node [ast.Call]: the call node
        """

        if isinstance(node.func, Attribute):
            if node.func.attr == "set_attribute":
                if isinstance(node.func.value, Name):
                    span_name = node.func.value.id
                    if span_name in self.spans:
                        # TODO. not sure it this is the best way to do this
                        # might want to consider the inclusion of a namedtuple for this
                        self.attributes.append({
                            "span": span_name,
                            "attribute": ast.literal_eval(node.args[0]),
                            "value": ast.literal_eval(node.args[1]),
                            "line": node.lineno
                        })
        
        self.generic_visit(node)

    def run(self):
        """
        Run the detector over the source code.
        """

        self.visit(self.source_code)
