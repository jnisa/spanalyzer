# Constants for the spanalyzer project

from enum import Enum

# TODO. filter some elements of the enum
class TelemetryKeywords(str, Enum):
    """
    Enum containing OpenTelemetry trace keywords.
    """
    
    START_AS_CURRENT_SPAN = "start_as_current_span"
    START_SPAN = "start_span"
    END_SPAN = "end"
    
    # Tracer Setup
    GET_TRACER = "get_tracer"
    SET_TRACER_PROVIDER = "set_tracer_provider"
    
    # Span Context
    GET_CURRENT_SPAN = "get_current_span"
    USE_SPAN = "use_span"
    
    # Span Attributes
    SET_ATTRIBUTE = "set_attribute"
    SET_ATTRIBUTES = "set_attributes"
    
    # Error Handling
    RECORD_EXCEPTION = "record_exception"
    SET_STATUS = "set_status"
    
    # Events
    ADD_EVENT = "add_event"
    ADD_EVENTS = "add_events"
    
    # Span Links
    ADD_LINK = "add_link"
    
    # Context Propagation
    INJECT = "inject"
    EXTRACT = "extract"
    
    # Baggage Operations
    SET_BAGGAGE = "set_baggage"
    GET_BAGGAGE = "get_baggage"
    
    # Metrics (if including metrics instrumentation)
    CREATE_COUNTER = "create_counter"
    CREATE_UP_DOWN_COUNTER = "create_up_down_counter"
    CREATE_HISTOGRAM = "create_histogram"
    CREATE_OBSERVABLE_GAUGE = "create_observable_gauge"
    
    # Resource Operations
    CREATE_RESOURCE = "create_resource"
    MERGE_RESOURCE = "merge_resource"
    
    # Sampling
    SET_SAMPLER = "set_sampler"
    
    # Processor Operations
    ADD_SPAN_PROCESSOR = "add_span_processor"
    
    # Instrumentation
    INSTRUMENT = "instrument"
    
    # Context Management
    ATTACH = "attach"
    DETACH = "detach"
    GET_CURRENT = "get_current"

    # Span Kind
    SERVER = "SERVER"
    CLIENT = "CLIENT"
    PRODUCER = "PRODUCER"
    CONSUMER = "CONSUMER"
    INTERNAL = "INTERNAL"

    @classmethod
    def values(cls) -> set[str]:
        """
        Get all keyword values as a set.
        """
        return {member.value for member in cls}
