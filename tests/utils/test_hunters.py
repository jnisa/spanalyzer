# Unitary tests to the multiple hunters

from unittest import TestCase

from ast import Dict
from ast import Name
from ast import Call
from ast import Expr
from ast import keyword
from ast import Constant
from ast import Attribute

from spanalyzer.utils.hunters import add_events_hunter
from spanalyzer.utils.hunters import set_attributes_hunter
from spanalyzer.utils.hunters import value_extractor
from spanalyzer.utils.hunters import counter_hunter

class TestHunters(TestCase):

    def test_value_extractor_basic(self):
        """
        Description: check if the extractor is capable of dealing with ast constant values.
        """

        test_constant = Constant(value="test")

        actual = value_extractor(test_constant)
        expected = "test"

        self.assertEqual(actual, expected)

    def test_value_extractor_name(self):
        """
        Description: check if the extractor is capable of dealing with ast name values.
        """

        test_name = Name(id="test")

        actual = value_extractor(test_name)
        expected = "test"

        self.assertEqual(actual, expected)

    def test_value_extractor_dict(self):
        """
        Description: check if the extractor is capable of dealing with ast dict values.
        """

        test_dict = Dict(keys=[Constant(value="key1"), Constant(value="key2")], values=[Constant(value="value1"), Constant(value="value2")])

        actual = value_extractor(test_dict)
        expected = {"key1": "value1", "key2": "value2"}

        self.assertEqual(actual, expected)

    def test_set_attributes_hunter_basic(self):
        """
        Description: check if the we can capture the set_attribute operator from a code sample containing one
        attribute only.
        """

        test_attrs = [
            Constant(value="key1"),
            Constant(value="value1")
        ]

        actual = set_attributes_hunter(test_attrs)
        expected = {'key1': 'value1'}

        self.assertEqual(actual, expected)

    def test_set_attributes_hunter_complex(self):
        """
        Description: check if we can capture all the set_attribute operators from a sample code containing 
        multiple set_attribute operators.
        """
        
        test_attrs = [
            Dict(
                keys=[Constant(value="key1"), Constant(value="key2")],
                values=[Name(id="Paul"), Name(id="Bruno")]
            )
        ]

        actual = set_attributes_hunter(test_attrs)
        expected = {
            'key1': 'Paul',
            'key2': 'Bruno'
        }

        self.assertEqual(actual, expected)

    def test_set_attributes_hunter_exception(self):
        """
        Description: check if we can capture the set_attribute operators from a sample code containing 
        no set_attribute operators.
        """

        test_attrs = []

        actual = set_attributes_hunter(test_attrs)
        expected = None

        self.assertEqual(actual, expected)

    def test_add_events_hunter_basic(self):
        """
        Description: check if we can capture the add_event operator from a code sample containing one
        add_event operator.
        """

        test_event = [
            Constant(value="event1"),
            Dict(
                keys=[Constant(value="key1")],
                values=[Constant(value="value1")]
            )
        ]

        actual = add_events_hunter(test_event)
        expected = ['event1', {'key1': 'value1'}]

        self.assertEqual(actual, expected)

    def test_add_events_hunter_complex(self):
        """
        Description: check if we can capture the add_event operator from a code sample containing 
        multiple add_event operators.
        """

        test_event = [
            Name(id="event1"),
            Dict(
                keys=[Constant(value="key1"), Constant(value="key2")],
                values=[Constant(value="value1"), Constant(value="value2")]
            )
        ]

        actual = add_events_hunter(test_event)
        expected = ['event1', {'key1': 'value1', 'key2': 'value2'}]

        self.assertEqual(actual, expected)

    def test_add_events_hunter_exception(self):
        """
        Description: check if we can capture the add_event operator from a code sample containing 
        no add_event operators.
        """

        test_event = []

        actual = add_events_hunter(test_event)
        expected = None

        self.assertEqual(actual, expected)

    def test_counter_hunter_basic(self):
        """
        Description: check if we can capture the counter operator from a code sample containing one
        counter operator.
        """

        test_counter = Expr(
            value=Call(
                func=Attribute(
                    value=Name(id='test_counter'),
                    attr='add'
                ),
                args=[
                    Constant(value=1)
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

        actual = counter_hunter(test_counter)
        expected = ['test_counter', [1], [{'key1': 'value1'}]]

        self.assertEqual(actual, expected)

    def test_counter_hunter_complex(self):
        """
        Description: check if we can capture the counter operator from a code sample containing a new
        increment is created with no attributes.
        """

        test_counter = Expr(
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

        actual = counter_hunter(test_counter)
        expected = ['test_counter', [2, {'key1': 'value1'}], None]

        self.assertEqual(actual, expected)
