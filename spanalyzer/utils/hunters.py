# Script containing the functions that will be used to capture the telemetry resources

from ast import AST
from ast import Call
from ast import Name
from ast import Expr
from ast import Dict
from ast import List
from ast import Constant
from ast import Attribute
from ast import Subscript

from javalang.tree import Literal
from javalang.tree import MemberReference
from javalang.tree import MethodInvocation
from javalang.tree import ClassCreator
from javalang.tree import Assignment
from javalang.tree import BinaryOperation
from javalang.tree import ReferenceType


from typing import Union
from typing import Optional
from typing import Any


def ast_extractor(node: AST) -> Optional[Union[str, dict, list, Any]]:
    """
    Universal AST node value extractor.

    Args:
        node: Any AST node

    Returns:
        Extracted value based on node type:
        - Constant: its value
        - Name: its id
        - Attribute: extracted value with attr
        - List: list of extracted values
        - Dict: dictionary of extracted key-value pairs
        - Call: function name and args
        - Expr: function name and args
        - Subscript: extracted value
        - None: for unsupported nodes

    Example:
        >>> ast_extractor(Constant(value='test'))
        'test'
        >>> ast_extractor(Attribute(value=Name(id='obj'), attr='method'))
        'obj.method'
    """

    match node:
        case Constant():
            return node.value
            
        case Name():
            return node.id
            
        case Attribute():
            base = ast_extractor(node.value)
            return f"{base}.{node.attr}" if base else node.attr
            
        case List():
            return [ast_extractor(elt) for elt in node.elts]
            
        case Dict():
            return {
                ast_extractor(k): ast_extractor(v)
                for k, v in zip(node.keys, node.values)
            }
            
        case Call():
            call_data = {
                'func': ast_extractor(node.func),
                'args': [ast_extractor(arg) for arg in node.args]
            }

            try:
                keywords = {
                    kw.arg: ast_extractor(kw.value)
                    for kw in node.keywords
                }

                if keywords:
                    call_data['keywords'] = keywords
            
            except (AttributeError, TypeError):
                pass
            
            return call_data
        
        case Expr():
            expr_data = {
                'func': ast_extractor(node.value.func),
                'args': [ast_extractor(arg) for arg in node.value.args]
            }
            
            try:
                keywords = {
                    kw.arg: ast_extractor(kw.value)
                    for kw in node.value.keywords
                }
                if keywords:
                    expr_data['keywords'] = keywords
            except (AttributeError, TypeError):
                pass
            
            return expr_data
        
        case Subscript():
            return ast_extractor(node.value)
                
        case _:
            return None

def java_ast_extractor(node: Any) -> Optional[Union[str, dict, list]]:
    """
    Universal extractor for javalang AST nodes.

    Args:
        node: Any javalang AST node

    Returns:
        Extracted value based on node type:
        - Literal: value
        - MemberReference: variable name
        - MethodInvocation: function call details
        - ClassCreator: constructor call
        - Assignment: target and value
        - BinaryOperation: operator and operands
        - ReferenceType: type name
        - List: recursively extract each element
        - None: if node type is unsupported

    Example:
        >>> tree = javalang.parse.parse("class Test { void m() { int x = 3 + 5; } }")
        >>> body = list(tree.types[0].body)[0].body
        >>> java_ast_extractor(body[0].expression)
        {'left': '3', 'operator': '+', 'right': '5'}
    """

    if node is None:
        return None

    match node:
        case Literal():
            return node.value.strip('"').strip("'")

        case MemberReference():
            return node.member

        case MethodInvocation():
            return {
                "method": node.member,
                "qualifier": node.qualifier,
                "arguments": [java_ast_extractor(arg) for arg in node.arguments],
            }

        case ClassCreator():
            return {
                "type": java_ast_extractor(node.type),
                "arguments": [java_ast_extractor(arg) for arg in node.arguments],
                "body": [java_ast_extractor(body) for body in node.body] if node.body else None,
            }

        case Assignment():
            return {
                "expression": java_ast_extractor(node.expression),
                "value": java_ast_extractor(node.value),
                "operator": java_ast_extractor(node.type),
            }

        case BinaryOperation():
            return {
                "expresion": java_ast_extractor(node.operandl),
                "value": java_ast_extractor(node.value),
                "type": node.type,
            }

        case ReferenceType():
            return ".".join(node.name)

        # TODO. assess if this is correct - this was generated by default
        # case list():
        #     return [java_ast_extractor(elem) for elem in node]

        case _:
            return None
