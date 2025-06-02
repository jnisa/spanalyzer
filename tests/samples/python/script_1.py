# Test script 1

from opentelemetry import trace

tracer = trace.get_tracer("script_1_tracer")


def random_function():
    """
    Random function that will contain the following opentelemetry resources:
    - span
    - span.set_attribute
    """

    with tracer.start_as_current_span("random_function") as span:
        span.set_attribute("attribute_1", "value_1")
        span.set_attribute("attribute_2", "value_2")
