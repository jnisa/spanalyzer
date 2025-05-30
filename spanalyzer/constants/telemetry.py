# Constants for the spanalyzer project

from enum import Enum

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from dataclasses import dataclass

# TODO. add a conversion to the telemetry call to a dictionary
# TODO. this will then be used on the report layer
@dataclass
class TelemetryCall:
    """Represents a telemetry operation with its details."""
    func: str
    line_number: int
    args: Optional[List[Any]] = None
    keywords: Optional[Dict[str, Any]] = None

class TelemetryKeywords(str, Enum):
    """
    Enum containing OpenTelemetry trace keywords.

    This includes keywords for the following:
    - Tracer Setup
    - Span Context
    - Attributes
    - Events
    """
    
    # Tracer Setup
    GET_TRACER = "get_tracer"
    
    # Span Context
    START_AS_CURRENT_SPAN = "start_as_current_span"
    START_SPAN = "start_span"
    # TODO. add later on
    # END_SPAN = "end"
    GET_CURRENT_SPAN = "get_current_span"
    USE_SPAN = "use_span"
    
    # Attributes
    SET_ATTRIBUTE = "set_attribute"
    SET_ATTRIBUTES = "set_attributes"
    
    # Exceptions and Error Capturing
    # TODO. add later on
    # RECORD_EXCEPTION = "record_exception"

    # Events
    ADD_EVENT = "add_event"
    ADD_EVENTS = "add_events"

    # Create Instrumentation    
    ADD_COUNTER = "add"

    # Instrumentation
    INSTRUMENT = "instrument"

    @classmethod
    def values(cls) -> set[str]:
        """
        Get all keyword values as a set.
        """

        return {member.value for member in cls}
    
    @classmethod
    def get_attributes_structure(cls) -> Dict[str, List]:
        """
        Get the attributes structure for a given keyword.
        """

        return {
            'tracers': [],
            'spans': [],
            'attributes': [],
            'events': [],
            'counter': [],
        }
