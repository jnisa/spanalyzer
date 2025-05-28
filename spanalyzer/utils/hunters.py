# Script containing the functions that will be used to capture the telemetry resources

from ast import Call
from ast import Name
from ast import Expr
from ast import Constant
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

    Example:
        >>> value_extractor(Constant(value='value'))
        'value'
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
            Dict(
                keys=[Constant(value='key1'), Constant(value='key2')],
                values=[Constant(value='value1'), Constant(value='value2')]
            )
        ]
        >>> attrs = set_attribute_hunter(calls_lst)
        >>> attrs
        {'key1': 'value1', 'key2': 'value2'}
    """

    if len(attributes_lst) == 2:
        return {value_extractor(attributes_lst[0]): value_extractor(attributes_lst[1])}

    if any(isinstance(attr, AstDict) for attr in attributes_lst):
        return value_extractor(attributes_lst[0])

    else:
        return None

def add_events_hunter(events_lst: List[Union[Name, Constant]]) -> List[Union[Dict[str, str], str]]:
    """
    Capture OpenTelemetry add_event/add_events operator details.

    Args:
        events_lst: List of AST Call nodes containing add_event operations

    Returns:
        List of event details

    Example:
        >>> calls_lst = [
            Name(id='event1'),
            Dict(
                keys=[Constant(value='key1')],
                values=[Constant(value='value1')]
            )
        ]
        >>> events = add_event_hunter(calls_lst)
        >>> events
        ['event1', {'key1': 'value1'}]
    """

    if not events_lst:
        return None

    return [
        value_extractor(event)
        for event in events_lst
    ]

def counter_hunter(counter_incrs: Expr) -> List[Union[str, int, Dict[str, str]]]:
    """
    Capture OpenTelemetry counter increment details.

    Args:
        counter_lst: List of AST Call nodes containing counter operations

    Returns:
        List of counter details

    Example:
        >>> counter_iteration = Expr(
                value=Call(
                    func=Attribute(
                        value=Name(id='counter'),
                        attr='add'
                    ),
                    args=[
                        Constant(value=1)
                    ],
                    keywords=[
                        {
                            'arg': 'attributes',
                            'value': Dict(
                                keys=[Constant(value='key1')],
                                values=[Constant(value='value1')]
                            )
                        }
                    ]
                )
        >>> incs = counter_increment_hunter(counter_iteration)
        >>> incs
        ['counter', [1], {'key1': 'value1'}]
    """

    counter_id = value_extractor(counter_incrs.value.func.value)
    counter_incr = [value_extractor(arg) for arg in counter_incrs.value.args]

    try:
        counter_attrs = [
            value_extractor(kw.value)
            for kw in counter_incrs.value.keywords
            if kw.arg == 'attributes'
        ]

    except:
        counter_attrs = None

    return [counter_id, counter_incr, counter_attrs]
