import unittest

import msgpack

# boilerplate
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().resolve().parent.parent))

from src.mercupy_msgpack import serialize_filter_element, deserialize_filter_element

from mercupy import tags
from mercupy import filter_elements as fe


class TestStringElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.StringElement(fe.FilterOperationType.EQ, 'test')

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestBoolElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.BoolElement(fe.FilterOperationType.EQ, False)

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestIntElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.IntElement(fe.FilterOperationType.EQ, 5)

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestFloatElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.FloatElement(fe.FilterOperationType.GE, 5.5)

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestDictElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.DictElement(fe.FilterOperationType.ALL,
                              {'a': fe.StringElement(fe.FilterOperationType.EQ, 'test')})

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestListElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.ListElement(fe.FilterOperationType.ALL, [
            fe.StringElement(fe.FilterOperationType.EQ, 'test1'),
            fe.IntElement(fe.FilterOperationType.EQ, 1)
        ])

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestLogicalElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.LogicalElement(fe.FilterOperationType.AND, [
            fe.StringElement(fe.FilterOperationType.EQ, 'test1'),
            fe.IntElement(fe.FilterOperationType.EQ, 1)
        ])

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestTagCollectionElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.TagCollectionElement(fe.FilterOperationType.EXPLICIT_TAG_MATCH, [
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) + tags.TagNameComponent.LOCALLY_DEPLOYED
            )
        ])

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestTypeDeclarationElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.TypeDeclarationElement(fe.FilterOperationType.TYPE_MATCH,
                                         fe.TypeStringElement(fe.FilterOperationType.NONE))

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestTypeStringElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.TypeStringElement(fe.FilterOperationType.NONE)

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestTypeBoolElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.TypeBoolElement(fe.FilterOperationType.NONE)

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestTypeIntElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.TypeIntElement(fe.FilterOperationType.NONE)

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestTypeFloatElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.TypeFloatElement(fe.FilterOperationType.NONE)

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestDimElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.DimElement(fe.FilterOperationType.NONE, 5)

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestTypeTensorElement(unittest.TestCase):

    def test_pytree_conversion(self):
        shape = [
            fe.LogicalElement(fe.FilterOperationType.AND, [
                fe.DimElement(fe.FilterOperationType.GE, 5),
                fe.DimElement(fe.FilterOperationType.LT, 10)
            ]),
            fe.DimElement(fe.FilterOperationType.GT, 6)
        ]
        var1 = fe.TypeTensorElement(fe.FilterOperationType.ALL, shape)

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestTypeNamedValueCollectionElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.TypeNamedValueCollectionElement(fe.FilterOperationType.ALL, {
            'value1': fe.TypeTensorElement(fe.FilterOperationType.ALL, [fe.DimElement(fe.FilterOperationType.GE, 5),
                                                                        fe.DimElement(fe.FilterOperationType.GT, 6)])})

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestTypeListElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.TypeListElement(fe.FilterOperationType.ALL, fe.TypeTensorElement(fe.FilterOperationType.ALL, [
            fe.DimElement(fe.FilterOperationType.GE, 2), fe.DimElement(fe.FilterOperationType.GE, 3)]))

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestTypeTupleElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.TypeTupleElement(fe.FilterOperationType.ALL, [fe.TypeStringElement(fe.FilterOperationType.NONE),
                                                                fe.TypeIntElement(fe.FilterOperationType.NONE)])

        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


class TestNoneFilterOperationWorks(unittest.TestCase):

    def test_construction_and_conversion_successful(self):
        # StringElement
        element = fe.StringElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # BoolElement
        element = fe.BoolElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # IntElement
        element = fe.IntElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # FloatElement
        element = fe.FloatElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # DictElement
        element = fe.DictElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # ListElement
        element = fe.ListElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # TypeDeclarationElement
        element = fe.TypeDeclarationElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # TagCollectionElement
        element = fe.TagCollectionElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # ... [similar blocks for TYPE_STRING, TYPE_INT, etc.]

        # TypeStringElement
        element = fe.TypeStringElement(fe.FilterOperationType.NONE)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # TypeIntElement
        element = fe.TypeIntElement(fe.FilterOperationType.NONE)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # TypeFloatElement
        element = fe.TypeFloatElement(fe.FilterOperationType.NONE)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # TypeBoolElement
        element = fe.TypeBoolElement(fe.FilterOperationType.NONE)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # TypeTensorElement
        element = fe.TypeTensorElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # TypeNamedValueCollectionElement
        element = fe.TypeNamedValueCollectionElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # TypeListElement
        element = fe.TypeListElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # TypeTupleElement
        element = fe.TypeTupleElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)

        # DimElement
        element = fe.DimElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(element)), element)


class TestIntegration(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = fe.DictElement(fe.FilterOperationType.ALL, {
            'key1': fe.StringElement(fe.FilterOperationType.EQ, 'cute'),
            'key2': fe.ListElement(fe.FilterOperationType.ALL, [
                fe.DictElement(fe.FilterOperationType.ALL, {
                    'declaration': fe.TypeDeclarationElement(fe.FilterOperationType.NONE, None),
                    'data': fe.IntElement(fe.FilterOperationType.NONE, None),
                    'tensor': fe.TypeTensorElement(fe.FilterOperationType.ALL, [
                        fe.LogicalElement(fe.FilterOperationType.AND, [
                            fe.DimElement(fe.FilterOperationType.GE, 5),
                            fe.DimElement(fe.FilterOperationType.LT, 10)
                        ]),
                        fe.DimElement(fe.FilterOperationType.NONE, None)
                    ])
                })
            ])
        })

        tree = {
            'dict': [
                'all',
                {
                    'key1': {'string': ['eq', 'cute']},
                    'key2': {
                        'list': [
                            'all',
                            [{'dict': [
                                'all',
                                {
                                    'declaration': {
                                        'type-declaration': [
                                            'none',
                                            None
                                        ]},
                                    'data': {'int': ['none', None]},
                                    'tensor': {
                                        'type-tensor': [
                                            'all',
                                            [
                                                {'logical': ['and', [{'dim': ['ge', 5]}, {'dim': ['lt', 10]}]]},
                                                {'dim': ['none', None]}
                                            ]
                                        ]
                                    }
                                }
                            ]}]
                        ]
                    }
                }
            ]
        }

        self.assertEqual(msgpack.unpackb(serialize_filter_element(var1)), tree)
        self.assertEqual(deserialize_filter_element(serialize_filter_element(var1)), var1)


if __name__ == '__main__':
    unittest.main()
