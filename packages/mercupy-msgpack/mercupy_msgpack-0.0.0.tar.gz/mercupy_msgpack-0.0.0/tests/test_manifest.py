# boilerplate
import sys
import unittest
from pathlib import Path

from mercupy import manifest_elements as ma
from mercupy import tags

sys.path.append(str(Path(__file__).absolute().resolve().parent.parent))

import msgpack

from src.mercupy_msgpack import serialize_manifest_element, deserialize_manifest_element


class TestStringElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.StringElement('test')

        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestBoolElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.BoolElement(True)

        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestIntElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.IntElement(5)

        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestFloatElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.FloatElement(5.5)

        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestDictElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.DictElement({'a': ma.StringElement('test')})
        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestListElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.ListElement([ma.StringElement('test1'), ma.IntElement(1)])

        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestTagCollectionElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.TagCollectionElement([
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) + tags.TagNameComponent.LOCALLY_DEPLOYED
            )
        ])

        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestTypeDeclarationElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.TypeDeclarationElement(ma.TypeStringElement())

        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestTypeStringElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.TypeStringElement()

        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestTypeBoolElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.TypeBoolElement()

        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestTypeIntElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.TypeIntElement()

        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestTypeFloatElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.TypeFloatElement()

        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestTypeTensorElement(unittest.TestCase):

    def test_pytree_conversion(self):
        shapes = [
            (),
            (1,),
            (2, 3),
            (3, 3, 3)
        ]

        for shape in shapes:
            var1 = ma.TypeTensorElement(shape)
            self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestTypeNamedValueCollectionElement(unittest.TestCase):

    def test_pytree_conversion(self):
        test_data = {
            'type-named-value-collection': {
                "value1": {
                    'type-tensor': [2, 3]
                }
            }
        }

        var1 = ma.TypeNamedValueCollectionElement({'value1': ma.TypeTensorElement((2, 3))})
        serialized = serialize_manifest_element(var1)
        self.assertEqual(msgpack.unpackb(serialized), test_data)

        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestTypeListElement(unittest.TestCase):

    def test_pytree_conversion(self):
        test_data = {'type-list': {'type-tensor': [2, 3]}}

        var1 = ma.TypeListElement(ma.TypeTensorElement((2, 3)))
        serialized = serialize_manifest_element(var1)
        self.assertEqual(msgpack.unpackb(serialized), test_data)

        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestTypeTupleElement(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.TypeTupleElement((ma.TypeStringElement(), ma.TypeIntElement()))
        self.assertEqual(deserialize_manifest_element(serialize_manifest_element(var1)), var1)


class TestIntegration(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = ma.DictElement({
            'key1': ma.StringElement('cute'),
            'key2': ma.ListElement([
                ma.DictElement({
                    'declaration': ma.TypeDeclarationElement(ma.TypeIntElement()),
                    'data': ma.IntElement(1)
                })
            ])
        })

        tree = {
            'dict': {
                'key1': {
                    'string': 'cute'
                },
                'key2': {
                    'list': [
                        {
                            'dict': {
                                'declaration': {
                                    'type-declaration': {
                                        'type-int': None
                                    }
                                },
                                'data': {
                                    'int': 1
                                }
                            }
                        }
                    ]
                }
            }
        }

        serialized = serialize_manifest_element(var1)
        self.assertEqual(msgpack.unpackb(serialized), tree)

        self.assertEqual(deserialize_manifest_element(serialized), var1)


if __name__ == '__main__':
    unittest.main()
