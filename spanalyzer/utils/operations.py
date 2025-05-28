# Script containing some operations that will be used through the spanalyzer

import json

from typing import Dict
from typing import List

from spanalyzer.script import FunctionSpecs

def conciliation(functions_lst: List[FunctionSpecs], telemetry_lst: List[Dict]) -> Dict:
    """
    Function that will be used to conciliate the functions and the telemetry details.

    Args:
        functions_lst [List[FunctionSpecs]]: list of functions with their specs
        telemetry_lst [List[Dict]]: list of telemetry details

    Returns:
        List[Dict]: list of telemetry details

    _Example_:
        >>> functions_lst = [
        ...     FunctionSpecs(
        ...         name='function_1',
        ...         start_lineno=3,
        ...         end_lineno=10,
        ...     ),
        ...     FunctionSpecs(
        ...         name='function_2',
        ...         start_lineno=13,
        ...         end_lineno=20,
        ...     ),
        ... ]
        >>> telemetry_lst = [
        ...     {
        ...         'tracers': {
        ...             1: 'test_tracer_1',
        ...             24: 'test_tracer_2'
        ...         },
        ...         'spans': {
        ...             12: 'test_span_1',
        ...             24: 'test_span_2'
        ...         },
        ...         'attributes': {
        ...             19: 'test_attribute_1',
        ...             24: 'test_attribute_2'
        ...         },
        ...         'events': {
        ...             2: 'test_event_1',
        ...             13: 'test_event_2'
        ...         },
        ...         'exceptions': {
        ...             2: True,
        ...         },
        ...         'ends': {
        ...             19: True,
        ...         },
        ...         'counter': {
        ...             19: 'test_counter_1',
        ...             24: 'test_counter_2'
        ...         },
        ...     },
        ... ]
        >>> conciliation(functions_lst, telemetry_lst)
        {
            'tracers': ['test_tracer_1', 'test_tracer_2'],
            'spans': ['test_span_1', 'test_span_2'],
            'attributes': ['test_attribute_2'],
            'events': ['test_event_1'],
            'exceptions': True,
            'ends': False,
            'counter': ['test_counter_2'],
            'functions': {
                'function_1': {
                    'attributes': ['test_attribute_1'],
                },
                'function_2': {
                    'events': ['test_event_2'],
                    'ends': True,
                    'counter': ['test_counter_1'],
                },
            },
        }
    """

    # TODO. implement the conciliation
    pass

def write_json(data: Dict, path: str):
    """
    Function that will create a json file with the data provided.

    Args:
        data [Dict]: data to be written into the json file
        path [str]: path to the json file
    """

    with open(path, 'w') as f:
        json.dump(data, f)
