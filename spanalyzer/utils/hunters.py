# Script containing the functions that will be used to capture the telemetry resources

from ast import Call
from ast import Constant
from ast import Name
from ast import Dict as AstDict

from typing import List
from typing import Union
from typing import Dict

def value_extractor(arg: Union[Constant, Name]) -> str:
    """
    Extract value from AST node.

    Args:
        arg: AST node to extract value from

    Returns:
        Value from AST node
    """

    match arg:
        case Constant():
            return arg.value

        case Name():
            return arg.id

        case AstDict():
            keys_lst = [k.value if isinstance(k, Constant) else k.id for k in arg.keys]
            values_lst = [v.value if isinstance(v, Constant) else v.id for v in arg.values]
            return dict(zip(keys_lst, values_lst))
        
        case _:
            return None


def set_attributes_hunter(attributes_lst: List[Union[Name, Constant]]) -> List[Union[Dict[str, str], str]]:
    """
    Capture OpenTelemetry set_attribute/set_attributes operator details.

    Args:
        attributes_lst: List of AST Call nodes containing attribute operations

    Returns:
        List of attribute values or key-value pairs

    Example:
        >>> calls_lst = [
            Call(
                func=Attribute(
                    value=Name(id='span'),
                    attr='set_attribute'
                ),
                
            )
        ]
        >>> attrs = set_attribute_hunter(calls_lst)
        >>> attrs
        [{'key1': 'value1'}]
    """

    if len(attributes_lst) == 2:
        return {value_extractor(attributes_lst[0]): value_extractor(attributes_lst[1])}

    if any(isinstance(attr, AstDict) for attr in attributes_lst):
        return value_extractor(attributes_lst[0])

    else:
        return None

def add_events_hunter(events_lst: List[Call]) -> List[Union[Dict[str, str], str]]:
    """
    Capture OpenTelemetry add_event/add_events operator details.

    Args:
        events_lst: List of AST Call nodes containing add_event operations

    Returns:
        List of event details

    Example:
        >>> calls_lst = [
            Call(
                func=Attribute(
                    value=Name(id='span'),
                    attr='add_event'
                ),
            )
        ]
        >>> events = add_event_hunter(calls_lst)
    """

    if not events_lst:
        return None

    return [
        value_extractor(event)
        for event in events_lst
    ]
