# Test Script 2

import time

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

    with tracer.start_as_current_span('random_function_1') as span:
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

    span = tracer.start_span('random_function_2')
    span.set_attributes({
        'input_1': val1,
        'input_2': val2
    })

    try:
        result = val1 - val2
        span.add_event('calculation_completed', {
            'operation': 'subtraction',
            'result': result
        })
        return result
    finally:
        span.end()

def random_function_3():
    """
    Random function containing three different spans.
    """

    with tracer.start_as_current_span('random_function_3'):
        
        load_user_span = tracer.start_span('load_user_from_db')
        load_user_span.add_events([
            {'name': 'operation_started', 'timestamp': time.time(), 'description': 'Load User from DB'},
            {'name': 'operation_completed', 'timestamp': time.time(), 'description': 'User loaded from DB'}
        ])
        pass

        with tracer.start_as_current_span('call_billing_services'):
            pass
