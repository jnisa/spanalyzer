# Unitary tests to the multiple hunters

from unittest import TestCase

from ast import Dict
from ast import Name
from ast import Call
from ast import Expr
from ast import Load
from ast import List
from ast import keyword
from ast import Constant
from ast import Attribute
from ast import Subscript

from javalang.tree import Literal
from javalang.tree import Assignment
from javalang.tree import ClassCreator
from javalang.tree import ReferenceType
from javalang.tree import MemberReference
from javalang.tree import MethodInvocation

from spanalyzer.utils.hunters import ast_extractor
from spanalyzer.utils.hunters import java_ast_extractor

class TestHunters(TestCase):

    def test_ast_extractor_constant(self):
        """
        Description: check if the extractor is capable of dealing with ast constant values.
        """

        test_constant = Constant(value="test")

        actual = ast_extractor(test_constant)
        expected = "test"

        self.assertEqual(actual, expected)

    def test_ast_extractor_name(self):
        """
        Description: check if the extractor is capable of dealing with ast name values.
        """

        test_name = Name(id="test")

        actual = ast_extractor(test_name)
        expected = "test"

        self.assertEqual(actual, expected)

    def test_ast_extractor_attribute(self):
        """
        Description: check if the extractor is capable of dealing with ast attribute values.
        """

        test_attribute = Attribute(value=Name(id="test"), attr="test")

        actual = ast_extractor(test_attribute)
        expected = "test.test"

        self.assertEqual(actual, expected)

    def test_ast_extractor_list(self):
        """
        Description: check if the extractor is capable of dealing with ast list values.
        """

        test_list = List(elts=[Constant(value="test1"), Constant(value="test2")])

        actual = ast_extractor(test_list)
        expected = ["test1", "test2"]

        self.assertEqual(actual, expected)

    def test_ast_extractor_dict(self):
        """
        Description: check if the extractor is capable of dealing with ast dict values.
        """

        test_dict = Dict(
            keys=[Constant(value="key1"), Constant(value="key2")], 
            values=[Constant(value="value1"), Constant(value="value2")]
        )

        actual = ast_extractor(test_dict)
        expected = {"key1": "value1", "key2": "value2"}

        self.assertEqual(actual, expected)

    def test_ast_extractor_call(self):
        """
        Description: check if the extractor is capable of dealing with ast call values.
        """

        test_call = Call(func=Name(id="test"), args=[Constant(value="test1"), Constant(value="test2")])

        actual = ast_extractor(test_call)
        expected = {'func': 'test', 'args': ['test1', 'test2']}

        self.assertEqual(actual, expected)

    def test_ast_extractor_counter(self):
        """
        Description: check if we can capture the counter operator from a code sample containing one
        counter operator.
        """

        test_expr = Expr(
            value=Call(
                func=Attribute(
                    value=Name(id='test_counter'),
                    attr='add'
                ),
                args=[
                    Constant(value=2),
                    Dict(
                        keys=[Constant(value='key1')],
                        values=[Constant(value='value1')]
                    )
                ]
            )
        )

        actual = ast_extractor(test_expr)
        expected = {'func': 'test_counter.add', 'args': [2, {'key1': 'value1'}]}

        self.assertEqual(actual, expected)

    def test_ast_extractor_add_event_simple(self):
        """
        Description: check if we can capture the add_event operator from a code sample containing one
        add_event operator.
        """

        test_expr = Expr(
            value=Call(
                func=Attribute(
                    value=Name(id='span', ctx=Load()),
                    attr='add_event',
                    ctx=Load()
                ),
                args=[
                    Constant(value='custom event')
                ],
                keywords=[
                    keyword(
                        arg='attributes',
                        value=Dict(
                            keys=[Constant(value='key1')],
                            values=[Constant(value='value1')]
                        )
                    )
                ]
            )
        )

        actual = ast_extractor(test_expr)
        expected = {
            'func': 'span.add_event',
            'args': ['custom event'], 'keywords': {'attributes': {'key1': 'value1'}}
        }

        self.assertEqual(actual, expected)

    def test_ast_extractor_add_event_complex(self):
        """
        Description: check if we can capture the add_event operator from a code sample containing a new
        increment is created with no attributes.
        """

        test_expr = Expr(
            value=Call(
                func=Attribute(
                    value=Name(id='span', ctx=Load()),
                    attr='add_event',
                    ctx=Load()
                ),
                args=[
                    Constant(value='data_processed'),
                    Dict(
                        keys=[
                            Constant(value='input_size'),
                            Constant(value='output_size')
                        ],
                        values=[
                            Call(
                                func=Name(id='len', ctx=Load()),
                                args=[
                                    Subscript(
                                        value=Name(id='raw_data', ctx=Load()),
                                        slice=Constant(value='data'),
                                        ctx=Load()
                                    )
                                ],
                                keywords=[]
                            ),
                            Call(
                                func=Name(id='len', ctx=Load()),
                                args=[Name(id='processed_data', ctx=Load())],
                                keywords=[]
                            )
                        ]
                    )
                ],
                keywords=[]
            )
        )

        actual = ast_extractor(test_expr)
        expected = {
            'func': 'span.add_event',
            'args': [
                'data_processed', 
                {
                    'input_size': {
                        'func': 'len', 
                        'args': ['raw_data'],
                    },
                    'output_size': {
                        'func': 'len',
                        'args': ['processed_data'],
                    },
                }
            ]
        }

        self.assertEqual(actual, expected)

    def test_ast_extractor_add_events(self):
        """
        Description: check if we can capture the add_events operator from a code sample containing a new
        increment is created with no attributes.
        """

        test_expr = Expr(
            value=Call(
                func=Attribute(
                    value=Name(id='load_user_span', ctx=Load()),
                    attr='add_events',
                    ctx=Load()
                ),
                args=[
                    List(
                        elts=[
                            Dict(
                                keys=[
                                    Constant(value='name'),
                                    Constant(value='timestamp'),
                                    Constant(value='description')
                                ],
                                values=[
                                    Constant(value='operation_started'),
                                    Call(
                                        func=Attribute(
                                            value=Name(id='time', ctx=Load()),
                                            attr='time',
                                            ctx=Load()
                                        ),
                                        args=[],
                                        keywords=[]
                                    ),
                                    Constant(value='Load User from DB')
                                ]
                            ),
                            Dict(
                                keys=[
                                    Constant(value='name'),
                                    Constant(value='timestamp'),
                                    Constant(value='description')
                                ],
                                values=[
                                    Constant(value='operation_completed'),
                                    Call(
                                        func=Attribute(
                                            value=Name(id='time', ctx=Load()),
                                            attr='time',
                                            ctx=Load()
                                        ),
                                        args=[],
                                        keywords=[]
                                    ),
                                    Constant(value='User loaded from DB')
                                ]
                            )
                        ],
                        ctx=Load()
                    )
                ],
                keywords=[]
            )
        )

        actual = ast_extractor(test_expr)
        expected = {
            'func': 'load_user_span.add_events',
            'args': [
                [
                    {
                        'name': 'operation_started', 
                        'timestamp': {
                            'func': 'time.time', 'args': [],
                        },
                        'description': 'Load User from DB'
                    },
                    {
                        'name': 'operation_completed', 
                        'timestamp': {
                            'func': 'time.time', 'args': [],
                        },
                        'description': 'User loaded from DB'
                    }
                ],
            ],
        }

        self.assertEqual(actual, expected)

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
            member="end",
            qualifier="span",
            arguments=[],
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
                "arguments": ["test_span"]
            },
            {
                "method": "setAttribute",
                "qualifier": "span",
                "arguments": ["test_key", "test_value"]
            },
            {
                "method": "end",
                "qualifier": "span",
                "arguments": []
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
                        "arguments": ["operation", "subtraction"]
                    },
                    {
                        "method": "put",
                        "qualifier": None,
                        "arguments": ["result", "123"]
                    },
                    {
                        "method": "build",
                        "qualifier": None,
                        "arguments": []
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
                        "arguments": ["span_name"]
                    }
                ]
            }
        )

        self.assertEqual(actual, expected)

    # def test_java_ast_extractor_assignment(self):
    #     """
    #     Description: check if the extractor is capable of parsing Assignment expressions.
    #     """

    #     test_assignment_1 = Assignment(
    #         expression=MemberReference(member="span"),
    #         value=MethodInvocation(
    #             member="spanBuilder",
    #             qualifier="tracer",
    #             arguments=[Literal(value="test")]
    #         ),
    #         type=Literal(value="=")
    #     )

    #     test_assignment_2 = Assignment(
    #         expression=MemberReference(member="span"),
    #         value=MethodInvocation(
    #             member="startSpan",
    #             qualifier=MethodInvocation(
    #                 member="spanBuilder",
    #                 qualifier="tracer",
    #                 arguments=[Literal(value="example_span")]
    #             ),
    #             arguments=[]
    #         ),
    #         type="="
    #     )

    #     actual = (
    #         java_ast_extractor(test_assignment_1),
    #         java_ast_extractor(test_assignment_2),
    #     )

    #     expected = (
    #         {
    #             "operator": "=",
    #             "expression": "span",
    #             "value": {
    #                 "method": "spanBuilder",
    #                 "qualifier": "tracer",
    #                 "arguments": ["test"]
    #             }
    #         },
    #         {
    #             "operator": "=",
    #             "expression": "span",
    #             "value": {
    #                 "method": "startSpan",
    #                 "qualifier": {
    #                     "method": "spanBuilder",
    #                     "qualifier": "tracer",
    #                     "arguments": ["example_span"]
    #                 },
    #                 "arguments": []
    #             }
    #         }
    #     )

    #     breakpoint()

    #     self.assertEqual(actual, expected)