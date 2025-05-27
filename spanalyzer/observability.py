# Script containing the Telemetry Detector

from typing import Dict

# TODO. to remove later on - probably
import ast
from ast import Call
from ast import Name
from ast import With
from ast import Dict
from ast import Assign
from ast import Attribute
from ast import Constant
from ast import literal_eval
from ast import NodeVisitor

from spanalyzer.constants.telemetry import TelemetryKeywords

# TODO. highlight this class will receive the code of a script at a time, and not multiple scripts
class TelemetryDetector(NodeVisitor):
    """
    This class will be used to sniff the telemetry calls in a script.

    It will be used to capture the telemetry calls in a script and return the list of telemetry calls.
    """

    def __init__(self):
        # TODO. not sure if we want to have multiple sets and lists as it's not memory efficient
        self.tracers = []
        self.spans = []
        self.attributes = []
        self.events = []
        self.exceptions = False
        self.ends = False
        self.metrics = []
        self.logs = []
        self.metric_instruments = []
        self.metric_operations = []


    # TODO. adjust the documetation of this method
    def visit_Call(self, node: Call):
        """
        This function will be used to visit the Assign node.

        It will be used to capture the telemetry calls in a script and return the list of telemetry calls.
        
        Args:
            node [Assign]: the Assign node to be visited
        """

        # TODO. not sure if we shouldn't group these by the type of resources we're capturing (_i.e._ tracers, spans, etc.)
        # TODO. not sure if the following lambdas need restructuring
        is_constant = lambda node: any(isinstance(arg, Constant) for arg in node.args)
        is_name = lambda node: any(isinstance(arg, Name) for arg in node.args)

        for node in ast.walk(node):
            if isinstance(node, Call):
                print(node.func.attr) # TODO. this clearly shows that is_constant and is_name need to be adjusted
                if isinstance(node.func, Attribute):# and ( or is_name(node)):

                    attr = node.func.attr

                    # TODO. convert this into a separate function (telemetry_identifier)
                    match attr:

                        case TelemetryKeywords.GET_CURRENT_SPAN:
                            pass

                        case TelemetryKeywords.USE_SPAN:
                            pass

                        case TelemetryKeywords.GET_TRACER:
                            obj = node.args[0].value if is_constant(node) else node.args[0].id
                            self.tracers.append(obj)

                        case TelemetryKeywords.START_SPAN:
                            obj = node.args[0].value if is_constant(node) else node.args[0].id
                            self.spans.append(obj)

                        case TelemetryKeywords.START_AS_CURRENT_SPAN:
                            obj = node.args[0].value if is_constant(node) else node.args[0].id
                            self.spans.append(obj)

                        case TelemetryKeywords.END_SPAN:
                            pass

                        case TelemetryKeywords.SET_ATTRIBUTE:
                            # TODO. probably convert this into a separate function
                            attr_lst = []
                            if len(node.args) > 1:
                                for arg in node.args:
                                    if isinstance(arg, Constant):
                                        attr_lst.append(arg.value)
                                    else:
                                        attr_lst.append(arg.id)
                                self.attributes.append({attr_lst[0]: attr_lst[1]})
                            else:
                                attr_lst = node.args[0].value if is_constant(node) else node.args[0].id
                                self.attributes.append(attr_lst)

                        # TODO. this is not being captured
                        case TelemetryKeywords.SET_ATTRIBUTES:
                            for arg in node.args:
                                if isinstance(arg, Dict):
                                    keys_lst = [k.value if isinstance(k, Constant) else k.id for k in arg.keys]
                                    values_lst = [v.value if isinstance(v, Constant) else v.id for v in arg.values]
                                    self.attributes.append(dict(zip(keys_lst, values_lst)))

                        case TelemetryKeywords.ADD_EVENT:
                            # TODO. probably convert this into a separate function
                            for arg in node.args:
                                if isinstance(arg, Constant):
                                    event_id = arg.value
                                elif isinstance(arg, Name):
                                    event_id = arg.id
                                elif isinstance(arg, Dict):
                                    keys_lst = [k.value if isinstance(k, Constant) else k.id for k in arg.keys]
                                    values_lst = [v.value if isinstance(v, Constant) else v.id for v in arg.values]
                                    event_specs = dict(zip(keys_lst, values_lst))

                            self.events.append({event_id: event_specs})

                        case TelemetryKeywords.ADD_EVENTS:
                            pass

                        case TelemetryKeywords.RECORD_EXCEPTION:
                            pass

                        # TODO. capture the CREATE_

            # TODO. capture the WITH statements


        self.generic_visit(node)

    def visit_With(self, node: With):
        """
        This function will be used to visit the With node.

        It will be used to capture the telemetry calls in a script and return the list of telemetry calls.

        Args:
            node [With]: the With node to be visited
        """

        # TODO. pretty sure this isn't the most effecient way of doing this
        # TODO. this line should be converted into a separate function that iterates over the code
        # and calls all the other functions to check if has any telemetry keywords
        for node in ast.walk(node):
            if isinstance(node, With):
                for item in node.items:
                    context_expr = item.context_expr
                    if isinstance(context_expr, Call) and isinstance(context_expr.func, Attribute):
                        if context_expr.func.attr == TelemetryKeywords.START_AS_CURRENT_SPAN:
                            for span in context_expr.args:
                                self.spans.append(span.value)

        self.generic_visit(node)

    # TODO. adjust the documentation of this method
    def run(self) -> Dict:
        """
        ADD A DESCRIPTION HERE
        """

        # TODO. this might be where we place the iteration over the script provided

        # TODO. check if this is the final structure of the report
        return {
            "tracers": list(self.tracers),
            "spans": list(self.spans),
            "manual_spans": self.manual_spans,
            "attributes": self.attributes,
            "events": self.events,
            "exceptions": self.exceptions,
            "ends": self.ends,
            "metrics_imports": self.metrics,
            "logs_imports": self.logs,
            "metric_instruments": self.metric_instruments,
            "metric_operations": self.metric_operations
        }
