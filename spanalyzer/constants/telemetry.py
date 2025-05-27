# Constants for the spanalyzer project

from enum import Enum

# TODO. add imports to the list of keywords
class TelemetryKeywords(str, Enum):
    """
    Enum containing OpenTelemetry trace keywords.

    This includes keywords for the following:
    - Tracer Setup
    - Span Context
    - Attributes
    - Error Handling
    - Events
    """
    
    # Tracer Setup
    GET_TRACER = "get_tracer"
    
    # Span Context
    START_AS_CURRENT_SPAN = "start_as_current_span"
    START_SPAN = "start_span"
    END_SPAN = "end"
    # TODO. these two are not being captured on the observability.py file
    # TODO. include them as functions to capture
    GET_CURRENT_SPAN = "get_current_span"
    USE_SPAN = "use_span"
    
    # Attributes
    SET_ATTRIBUTE = "set_attribute"
    SET_ATTRIBUTES = "set_attributes"
    
    # Exceptions and Error Capturing
    RECORD_EXCEPTION = "record_exception"

    # Events
    ADD_EVENT = "add_event"
    ADD_EVENTS = "add_events"

    # Create Instrumentation    
    CREATE_COUNTER = "create_counter"
    # TODO. assess if we actually want to capture the following operations
    CREATE_UP_DOWN_COUNTER = "create_up_down_counter"
    CREATE_HISTOGRAM = "create_histogram"
    CREATE_OBSERVABLE_GAUGE = "create_observable_gauge"
    CREATE_RESOURCE = "create_resource"

    # Instrumentation
    INSTRUMENT = "instrument"

    @classmethod
    def values(cls) -> set[str]:
        """
        Get all keyword values as a set.
        """

        return {member.value for member in cls}
