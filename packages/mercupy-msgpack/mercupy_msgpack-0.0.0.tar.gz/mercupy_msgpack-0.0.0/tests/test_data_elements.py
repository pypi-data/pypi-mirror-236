# Authored by GPT-4-backed ChatGPT and adapted by Trent Fellbootman
import unittest
import msgpack
import numpy as np

from mercupy import data_elements as da

# boilerplate
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().resolve().parent.parent))

from src.mercupy_msgpack import serialize_data_element, deserialize_data_element


class TestStringElement(unittest.TestCase):

    def test_serde(self):
        var1 = da.StringElement("sample")
        serialized = serialize_data_element(var1)
        self.assertEqual(msgpack.unpackb(serialized), {'string': 'sample'})
        deserialized = deserialize_data_element(serialized)
        self.assertEqual(deserialized, var1)


class TestBoolElement(unittest.TestCase):

    def test_serde(self):
        var1 = da.BoolElement(True)
        serialized = serialize_data_element(var1)
        self.assertEqual(msgpack.unpackb(serialized), {'bool': True})
        deserialized = deserialize_data_element(serialized)
        self.assertEqual(deserialized, var1)


class TestIntElement(unittest.TestCase):

    def test_serde(self):
        var1 = da.IntElement(10)
        serialized = serialize_data_element(var1)
        self.assertEqual(msgpack.unpackb(serialized), {'int': 10})
        deserialized = deserialize_data_element(serialized)
        self.assertEqual(deserialized, var1)


class TestFloatElement(unittest.TestCase):

    def test_serde(self):
        var1 = da.FloatElement(10.5)
        serialized = serialize_data_element(var1)
        self.assertEqual(msgpack.unpackb(serialized), {'float': 10.5})
        deserialized = deserialize_data_element(serialized)
        self.assertEqual(deserialized, var1)


class TestListElement(unittest.TestCase):

    def test_serde(self):
        var1 = da.ListElement([da.IntElement(1), da.StringElement("two")])
        serialized = serialize_data_element(var1)
        self.assertEqual(msgpack.unpackb(serialized), {'list': [{'int': 1}, {'string': 'two'}]})
        deserialized = deserialize_data_element(serialized)
        self.assertEqual(deserialized, var1)


class TestNamedValueCollectionElement(unittest.TestCase):

    def test_serde(self):
        var1 = da.NamedValueCollectionElement({'a': da.IntElement(1), 'b': da.StringElement("two")})
        serialized = serialize_data_element(var1)
        self.assertEqual(msgpack.unpackb(serialized), {'named-value-collection': {'a': {'int': 1}, 'b': {'string': 'two'}}})
        deserialized = deserialize_data_element(serialized)
        self.assertEqual(deserialized, var1)


class TestTensorElement(unittest.TestCase):

    def test_serde(self):
        np_arr = np.array([[1, 2, 3], [4, 5, 6]])
        var1 = da.TensorElement(np_arr)
        serialized = serialize_data_element(var1)
        self.assertEqual(msgpack.unpackb(serialized), {'tensor': [[2, 3], [1, 2, 3, 4, 5, 6]]})
        deserialized = deserialize_data_element(serialized)
        self.assertEqual(deserialized, var1)


class TestDataIntegration(unittest.TestCase):

    def test_serde(self):
        var1 = da.NamedValueCollectionElement({
            'key1': da.StringElement('cute'),
            'key2': da.ListElement([
                da.NamedValueCollectionElement({
                    'tensor': da.TensorElement(np.array([1, 2, 3])),
                    'status': da.BoolElement(True)
                })
            ])
        })

        tree = {
            'named-value-collection': {
                'key1': {
                    'string': 'cute'
                },
                'key2': {
                    'list': [
                        {
                            'named-value-collection': {
                                'tensor': {
                                    'tensor': [[3], [1, 2, 3]]
                                },
                                'status': {
                                    'bool': True
                                }
                            }
                        }
                    ]
                }
            }
        }

        self.assertEqual(msgpack.unpackb(serialize_data_element(var1)), tree)
        self.assertEqual(deserialize_data_element(serialize_data_element(var1)), var1)


if __name__ == '__main__':
    unittest.main()
