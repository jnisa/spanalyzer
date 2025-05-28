# Script containing the Telemetry Detector

from typing import Dict

# TODO. to remove later on - probably
import ast
from ast import Call
from ast import Expr
from ast import Dict
from ast import Constant
from ast import NodeVisitor

from spanalyzer.utils.hunters import add_events_hunter
from spanalyzer.utils.hunters import set_attributes_hunter
from spanalyzer.utils.hunters import counter_hunter

from spanalyzer.constants.telemetry import TelemetryKeywords

# TODO. highlight this class will receive the code of a script at a time, and not multiple scripts
# TODO. improve the docs of this class
class TelemetryDetector(NodeVisitor):
    """
    This class will be used to sniff the telemetry calls in a script.

    It will be used to capture the telemetry calls in a script and return the list of telemetry calls.
    """

    def __init__(self):
        
        # TODO. not sure if we want to have multiple sets and lists as it's not memory efficient
        # TODO. some of these might need to be converted into dictionaries as we'll might want to store
        # the lineno
        
        self.tracers = []
        self.spans = []
        self.attributes = []
        self.events = []
        self.exceptions = False
        self.ends = False
        self.counter = []

    # TODO. this is python specific, we would need to change this if it was meant to be used for Java
    def call_switcher(self, call_type: str, node: Call):
        """
        This function will work as a switch to determine the type of call being made.

        According to the type of call being made, the function that will capture the telemetry details will be
        duly called.

        Args:
            call_type [str]: type of call being made
            node [Call]: code node to be evaluated
        """

        is_constant = lambda node: any(isinstance(arg, Constant) for arg in node.args)

        # TODO. add the lineno to the nodes at each entry
        match call_type:
            case TelemetryKeywords.GET_TRACER:
                # TODO. evaluate the following code
                obj = node.args[0].value if is_constant(node) else node.args[0].id
                self.tracers.append(obj)

            case TelemetryKeywords.START_SPAN:
                # TODO. evaluate the following code
                obj = node.args[0].value if is_constant(node) else node.args[0].id
                self.spans.append(obj)

            case TelemetryKeywords.START_AS_CURRENT_SPAN:
                # TODO. evaluate the following code
                obj = node.args[0].value if is_constant(node) else node.args[0].id
                self.spans.append(obj)
                # TODO. if one of the arguments is end_on_exit then we need to set the ends flag to True

            case TelemetryKeywords.USE_SPAN:
                # TODO. evaluate the following code
                obj = node.args[0].value if is_constant(node) else node.args[0].id
                self.spans.append(obj)

            case TelemetryKeywords.END_SPAN:
                self.ends = True
            
            case TelemetryKeywords.SET_ATTRIBUTE:
                self.attributes.append(set_attributes_hunter(node.args))

            case TelemetryKeywords.SET_ATTRIBUTES:
                self.attributes.append(set_attributes_hunter(node.args))

            case TelemetryKeywords.ADD_EVENT:
                self.events.append(add_events_hunter(node.args))

            case TelemetryKeywords.ADD_EVENTS:
                self.events.append(add_events_hunter(node.args))

            case TelemetryKeywords.RECORD_EXCEPTION:
                self.exceptions = True

            case TelemetryKeywords.ADD_COUNTER:
                self.counter.append(counter_hunter(node))

        self.generic_visit(node)

    def run(self, node: Call) -> Dict:
        """
        Method that can be seen as the heart of the TelemetryDetector class.

        This method will be filtering the type of nodes that are of interest, and will be then calling
        the switcher method - that captures all the telemetry details spanalyzer is looking for.

        Args:
            node [Call]: code node to be evaluated

        Returns:
            Dict: dictionary containing the telemetry details
        """

        for node in ast.walk(node):

            try:
                if isinstance(node, Call):
                    self.call_switcher(node.func.attr, node)
                
                if isinstance(node, Expr):
                    self.call_switcher(node.value.func.attr, node)

            except:
                pass

        return {
            "tracers": list(self.tracers),
            "spans": list(self.spans),
            "attributes": self.attributes,
            "events": self.events,
            "exceptions": self.exceptions,
            "ends": self.ends,
            "counter": self.counter,
        }
