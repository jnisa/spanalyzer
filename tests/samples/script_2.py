# Test Script 2

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def random_function_1(val1: int, val2: int) -> int:
    """
    Random function that will perform the addition of two values.

    _Example_:
    >>> result = random_function_1(1, 2)
    >>> print(result)
    3

    Args:
        val1 [int]: the first value to be added
        val2 [int]: the second value to be added

    Returns:
        [int]: the sum of the two values
    """

    with tracer.start_as_current_span('random_function') as span:
        span.set_attribute('val1', val1)
        span.set_attribute('val2', val2)

        return val1 + val2

def random_function_2(val1: int, val2: int) -> int:
    """
    Random function that will perform the subtraction of two values.

    _Example_:
    >>> result = random_function_2(1, 2)
    >>> print(result)
    -1

    Args:
        val1 [int]: the first value to be subtracted
        val2 [int]: the second value to be subtracted

    Returns:
        [int]: the difference of the two values
    """

    with tracer.start_as_current_span('random_function') as span:
        span.set_attribute('val1', val1)
        span.set_attribute('val2', val2)

        return val1 - val2
