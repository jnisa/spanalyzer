# Unitary tests to the Java Hunter

from unittest import TestCase

from javalang.tree import Literal
from javalang.tree import MemberReference
from javalang.tree import MethodInvocation
from javalang.tree import ClassCreator
from javalang.tree import Assignment
from javalang.tree import BinaryOperation
from javalang.tree import ReferenceType
from javalang.tree import ForStatement
from javalang.tree import IfStatement
from javalang.tree import ReturnStatement
from javalang.tree import VariableDeclarator
from javalang.tree import StatementExpression
from javalang.tree import BlockStatement

from spanalyzer.java.hunters import java_ast_extractor


class TestJavaHunter(TestCase):
    """
    Unitary tests to the Java Hunter.
    """

    def test_java_ast_extractor_literal(self):
        """
        Description: check if the extractor is capable of dealing with ast literal values.
        """

        test_literal = Literal(value="test")

        actual = java_ast_extractor(test_literal)
        expected = "test"

        self.assertEqual(actual, expected)

    def test_java_ast_extractor_member_reference(self):
        """
        Description: check if the extractor is capable of dealing with ast member reference values.
        """

        test_member_reference = MemberReference(
            member="test_member"
        )

        actual = java_ast_extractor(test_member_reference)
        expected = "test_member"

        self.assertEqual(actual, expected)

    def test_java_ast_extractor_method_invocation(self):
        """
        Description: check if the extractor is capable of dealing with different types of method invocations.
        """

        test_method_invocation_1 = MethodInvocation(
            member="spanBuilder",
            qualifier="tracer",
            arguments=[
                Literal(value="test_span")
            ],
        )

        test_method_invocation_2 = MethodInvocation(
            member="setAttribute",
            qualifier="span",
            arguments=[
                Literal(value="test_key"),
                Literal(value="test_value")
            ],
        )

        test_method_invocation_3 = MethodInvocation(
            member="addEvent",
            qualifier=MemberReference(member="loadUserSpan"),
            arguments=[
                Literal(value='"operation_started"'),
                MethodInvocation(
                    member="build",
                    arguments=[],
                    qualifier=MethodInvocation(
                        member="put",
                        arguments=[
                            Literal(value='"description"'),
                            Literal(value='"Load User from DB"')
                        ],
                        qualifier=MethodInvocation(
                            member="put",
                            arguments=[
                                Literal(value='"timestamp"'),
                                MethodInvocation(
                                    member="toString",
                                    arguments=[],
                                    qualifier=MethodInvocation(
                                        member="now",
                                        arguments=[],
                                        qualifier=MemberReference(member="Instant")
                                    )
                                )
                            ],
                            qualifier=MethodInvocation(
                                member="builder",
                                arguments=[],
                                qualifier=MemberReference(member="Attributes")
                            )
                        )
                    )
                )
            ]
        )

        actual = (
            java_ast_extractor(test_method_invocation_1),
            java_ast_extractor(test_method_invocation_2),
            java_ast_extractor(test_method_invocation_3)
        )
        expected = (
            {
                "method": "spanBuilder",
                "qualifier": "tracer",
                "arguments": ["test_span"],
                "selectors": None
            },
            {
                "method": "setAttribute",
                "qualifier": "span",
                "arguments": ["test_key", "test_value"],
                "selectors": None
            },
            {
                "method": "addEvent",
                "qualifier": "loadUserSpan",
                "arguments": [
                    "operation_started",
                    {
                        "method": "build",
                        "qualifier": {
                            "method": "put",
                            "qualifier": {
                                "method": "put",
                                "qualifier": {
                                    "method": "builder",
                                    "qualifier": "Attributes",
                                    "arguments": [],
                                    "selectors": None
                                },
                                "arguments": [
                                    "timestamp",
                                    {
                                        "method": "toString",
                                        "qualifier": {
                                            "method": "now",
                                            "qualifier": "Instant",
                                            "arguments": [],
                                            "selectors": None
                                        },
                                        "arguments": [],
                                        "selectors": None
                                    }
                                ],
                                "selectors": None
                            },
                            "arguments": [
                                "description",
                                "Load User from DB"
                            ],
                            "selectors": None
                        },
                        "arguments": [],
                        "selectors": None
                    }
                ],
                "selectors": None
            }
        )

        self.assertEqual(actual, expected)

    def test_java_ast_extractor_class_creator(self):
        """
        Description: check if the extractor is capable of parsing OpenTelemetry-style ClassCreator expressions.
        """

        test_creator_1 = ClassCreator(
            type=MemberReference(member="HashMap"),
            arguments=[],
            body=None
        )

        test_creator_2 = ClassCreator(
            type=MemberReference(member="Attributes$Builder"),
            arguments=[],
            body=[
                MethodInvocation(
                    member="put",
                    qualifier="builder",
                    arguments=[
                        Literal(value="operation"),
                        Literal(value="subtraction")
                    ]
                ),
                MethodInvocation(
                    member="put",
                    qualifier=None,
                    arguments=[
                        Literal(value="result"),
                        Literal(value="123")
                    ]
                ),
                MethodInvocation(
                    member="build",
                    qualifier=None,
                    arguments=[]
                )
            ]
        )

        test_creator_3 = ClassCreator(
            type=MemberReference(member="SomeTracer"),
            arguments=[],
            body=[
                MethodInvocation(
                    member="spanBuilder",
                    qualifier=None,
                    arguments=[
                        Literal(value="span_name")
                    ]
                )
            ]
        )

        actual = (
            java_ast_extractor(test_creator_1),
            java_ast_extractor(test_creator_2),
            java_ast_extractor(test_creator_3)
        )

        expected = (
            {
                "type": "HashMap",
                "arguments": [],
                "body": None,
            },
            {
                "type": "Attributes$Builder",
                "arguments": [],
                "body": [
                    {
                        "method": "put",
                        "qualifier": "builder",
                        "arguments": ["operation", "subtraction"],
                        "selectors": None
                    },
                    {
                        "method": "put",
                        "qualifier": None,
                        "arguments": ["result", "123"],
                        "selectors": None
                    },
                    {
                        "method": "build",
                        "qualifier": None,
                        "arguments": [],
                        "selectors": None
                    }
                ],
            },
            {
                "type": "SomeTracer",
                "arguments": [],
                "body": [
                    {
                        "method": "spanBuilder",
                        "qualifier": None,
                        "arguments": ["span_name"],
                        "selectors": None
                    }
                ]
            }
        )

        self.assertEqual(actual, expected)

    def test_java_ast_extractor_assignment(self):
        """
        Description: check if the extractor is capable of parsing Assignment expressions.
        """

        test_assignment_1 = Assignment(
            expressionl=MemberReference(member="span"),
            value=MethodInvocation(
                member="spanBuilder",
                qualifier="tracer",
                arguments=[Literal(value="test")]
            ),
            type=Literal(value="=")
        )

        test_assignment_2 = Assignment(
            expressionl=MemberReference(member="span"),
            value=MethodInvocation(
                member="startSpan",
                qualifier=MethodInvocation(
                    member="spanBuilder",
                    qualifier="tracer",
                    arguments=[Literal(value="example_span")]
                ),
                arguments=[]
            ),
            type=Literal(value="=")
        )

        actual = (
            java_ast_extractor(test_assignment_1),
            java_ast_extractor(test_assignment_2),
        )

        expected = (
            {
                "expression": "span",
                "value": {
                    "method": "spanBuilder",
                    "qualifier": "tracer",
                    "arguments": ["test"],
                    "selectors": None
                },
                "operator": "=",
            },
            {
                "expression": "span",
                "value": {
                    "method": "startSpan",
                    "qualifier": {
                        "method": "spanBuilder",
                        "qualifier": "tracer",
                        "arguments": ["example_span"],
                        "selectors": None
                    },
                    "arguments": [],
                    "selectors": None
                },
                "operator": "=",
            }
        )

        self.assertEqual(actual, expected)

    def test_java_ast_extractor_binary_operation(self):
        """
        Description: check if the extractor is capable of parsing BinaryOperation expressions.
        """

        test_binary_operation_1 = BinaryOperation(
            operandl=MemberReference(member="span"),
            operator=Literal(value="="),
            operandr=MethodInvocation(
                member="spanBuilder",
                qualifier="tracer",
                arguments=[Literal(value="test")],
                selectors=None
            ),
        )
        
        test_binary_operation_2 = MethodInvocation(
            member="setAttribute",
            qualifier="span",
            arguments=[
                Literal(value="request_time"),
                BinaryOperation(
                    operandl=MemberReference(member="processingTime"),
                    operator=Literal(value="+"),
                    operandr=MemberReference(member="offset"),
                )
            ],
            selectors=None
        )

        test_binary_operation_3 = MethodInvocation(
            member="println",
            qualifier=MemberReference(member="System.out"),
            arguments=[
                BinaryOperation(
                    operandl=Literal(value="Span delay: "),
                    operator=Literal(value="+"),
                    operandr=BinaryOperation(
                        operandl=MemberReference(member="end"),
                        operator=Literal(value="-"),
                        operandr=MemberReference(member="start"),
                    ),
                )
            ],
            selectors=None
        )

        actual = (
            java_ast_extractor(test_binary_operation_1),
            java_ast_extractor(test_binary_operation_2),
            java_ast_extractor(test_binary_operation_3)
        )
        expected = (
            {
                'operandl': 'span',
                'operator': '=',
                'operandr': {
                    'method': 'spanBuilder',
                    'qualifier': 'tracer',
                    'arguments': ['test'],
                    'selectors': None
                }
            },
            {
                'method': 'setAttribute',
                'qualifier': 'span',
                'arguments': [
                    'request_time',
                    {
                        'operandl': 'processingTime',
                        'operator': '+',
                        'operandr': 'offset'
                    }
                ],
                'selectors': None
            },
            {
                'method': 'println',
                'qualifier': 'System.out',
                'arguments': [
                    {
                        'operandl': 'Span delay: ',
                        'operator': '+',
                        'operandr': {
                            'operandl': 'end',
                            'operator': '-',
                            'operandr': 'start'
                        }
                    }
                ],
            'selectors': None})

        self.assertEqual(actual, expected)
        
    def test_java_ast_extractor_reference_type(self):
        """
        Description: check if the extractor is capable of parsing ReferenceType expressions.
        """

        test_ref_1 = ReferenceType(name=["io", "opentelemetry", "api", "trace", "Tracer"])
        test_ref_2 = ReferenceType(name=["io", "opentelemetry", "api", "trace", "Span"])
        test_ref_3 = ReferenceType(name=["io", "opentelemetry", "api", "trace", "SpanBuilder"])
        test_ref_4 = ReferenceType(name=["io", "opentelemetry", "context", "Context"])

        actual = (
            java_ast_extractor(test_ref_1),
            java_ast_extractor(test_ref_2),
            java_ast_extractor(test_ref_3),
            java_ast_extractor(test_ref_4),
        )

        expected = (
            "io.opentelemetry.api.trace.Tracer",
            "io.opentelemetry.api.trace.Span",
            "io.opentelemetry.api.trace.SpanBuilder",
            "io.opentelemetry.context.Context",
        )

        self.assertEqual(actual, expected)

    def test_java_ast_extractor_for_statement(self):
        """
        Description: check if the extractor is capable of parsing ForStatement expressions.
        """

        test_for_statement_1 = ForStatement(
            control=MemberReference(member='span'),
            body=MethodInvocation(
                member='setAttribute',
                qualifier='span',
                arguments=[Literal(value='test')]
            )
        )

        test_for_statement_2 = ForStatement(
            control=MemberReference(member='request'),
            body=BlockStatement(
                statements=[
                    ReturnStatement(
                        expression=MemberReference(member='requestId')
                    ),
                    MethodInvocation(
                        member='add',
                        qualifier='requestCounter',
                        arguments=[
                            Literal(value=1),
                            MethodInvocation(
                                member='of',
                                qualifier='Attributes',
                                arguments=[
                                    Literal(value='endpoint'),
                                    MemberReference(member='path'),
                                    Literal(value='method'),
                                    MemberReference(member='method')
                                ]
                            )
                        ]
                    )
                ]
            )
        )
        
        actual = (
            java_ast_extractor(test_for_statement_1),
            java_ast_extractor(test_for_statement_2),
        )
        
        expected = (
            {
                "control": "span",
                "body": {
                    "method": "setAttribute",
                    "qualifier": "span",
                    "arguments": ["test"],
                    "selectors": None
                }
            },
            {
                "control": "request",
                "body": [
                    {
                        "expression": "requestId"
                    },
                    {
                        "method": "add",
                        "qualifier": "requestCounter",
                        "arguments": [
                            1, 
                            {
                                "method": "of",
                                "qualifier": "Attributes",
                                "arguments": [
                                    "endpoint",
                                    "path",
                                    "method",
                                    "method"
                                ],
                                "selectors": None
                            }
                        ],
                        "selectors": None
                    }
                ],
            }
        )

        self.assertEqual(actual, expected)

    def test_java_ast_extractor_if_statement(self):
        """
        Description: check if the extractor is capable of parsing IfStatement expressions.
        """
        
        test_if_statement = IfStatement(
            condition=BinaryOperation(
                operator='!=',
                operandl=MemberReference(member='span'),
                operandr=Literal(value='null')
            ),
            then_statement=BlockStatement(statements=[
                VariableDeclarator(
                    name='attributes',
                    initializer=MethodInvocation(
                        member='of',
                        qualifier='Attributes',
                        arguments=[
                            Literal(value='error.type'),
                            MemberReference(member='errorType'),
                            Literal(value='error.message'),
                            MemberReference(member='errorMessage')
                        ]
                    )
                ),
                StatementExpression(
                    expression=MethodInvocation(
                        member='setStatus',
                        qualifier='span',
                        arguments=[
                            MemberReference(member='StatusCode.ERROR'),
                            MemberReference(member='errorDescription')
                        ]
                    )
                ),
                StatementExpression(
                    expression=MethodInvocation(
                        member='recordException',
                        qualifier='span',
                        arguments=[MemberReference(member='exception')]
                    )
                )
            ]),
            else_statement=None
        )

        actual = java_ast_extractor(test_if_statement)
        expected = {
            'condition': {
                'operandl': 'span',
                'operator': None,
                'operandr': 'null'
            },
            'then_statement': [
                {
                    'name': None,
                    'dimensions': None,
                    'initializer': {
                        'method': 'of',
                        'qualifier': 'Attributes',
                        'arguments': [
                            'error.type',
                            'errorType',
                            'error.message',
                            'errorMessage'
                        ],
                        "selectors": None
                    }
                },
                {
                    'expression': {
                        'method': 'setStatus',
                        'qualifier': 'span',
                        'arguments': [
                            'StatusCode.ERROR', 
                            'errorDescription'
                        ],
                        "selectors": None
                    }
                },
                {
                    'expression': {
                        'method': 'recordException',
                        'qualifier': 'span',
                        'arguments': [
                            'exception'
                        ],
                        "selectors": None
                    }
                }
            ],
            'else_statement': None
        }

        self.assertEqual(actual, expected)

        