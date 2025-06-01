# Unitary tests to the Python Hunter

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

from spanalyzer.python.hunters import ast_extractor


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
