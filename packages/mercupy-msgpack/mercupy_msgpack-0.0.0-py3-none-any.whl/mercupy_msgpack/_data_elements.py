# Authored by GPT-4-backed ChatGPT and adapted by Trent Fellbootman
"""Data element definitions. Abstractions for data that will be passed to and received from model server processes."""

from typing import List, Dict, Union, Tuple
from collections.abc import Callable
from typeguard import typechecked
import numpy as np

from mercupy.data_elements import (
    DataElement, DataElementType,
    ListElement, FloatElement, StringElement, IntElement, BoolElement, TensorElement, NamedValueCollectionElement
)


_PyTree = Union[List, Dict, str, float, bool, int, None]


_element_name_enum_map = {
    "string": DataElementType.STRING,
    "bool": DataElementType.BOOL,
    "int": DataElementType.INT,
    "float": DataElementType.FLOAT,
    "named-value-collection": DataElementType.NAMED_VALUE_COLLECTION,
    "list": DataElementType.LIST,
    "tensor": DataElementType.TENSOR
}

assert set(_element_name_enum_map.values()) == set(DataElementType)

_element_enum_name_map = {
    value: key for key, value in _element_name_enum_map.items()
}


@typechecked
def _decompose_element_pytree(pytree: Dict[str, _PyTree]) -> Tuple[DataElementType, _PyTree]:
    assert len(pytree) == 1
    type_name, data = next(iter(pytree.items()))
    return _element_name_enum_map[type_name], data


# to data only pytree
_element_type_serializer_map: Dict[DataElementType, Callable[[DataElement], _PyTree]] = {}
# from data only pytree
_element_type_deserializer_map: Dict[DataElementType, Callable[[_PyTree], DataElement]] = {}


def to_pytree(element: DataElement) -> _PyTree:
    data_tree = _element_type_serializer_map[element.element_type](element)
    return {_element_enum_name_map[element.element_type]: data_tree}


def from_pytree(pytree: _PyTree) -> DataElement:
    element_type, data = _decompose_element_pytree(pytree)
    return _element_type_deserializer_map[element_type](data)


def _string_to_data_only_pytree(self) -> str:
    return self._value


def _string_from_data_only_pytree(pytree: str) -> StringElement:
    return StringElement(pytree)


def _bool_to_data_only_pytree(self) -> bool:
    return self._value


def _bool_from_data_only_pytree(pytree: bool) -> BoolElement:
    return BoolElement(pytree)


def _int_to_data_only_pytree(self) -> int:
    return self._value


def _int_from_data_only_pytree(pytree: int) -> IntElement:
    return IntElement(pytree)


def _float_to_data_only_pytree(self) -> float:
    return self._value


def _float_from_data_only_pytree(pytree: float) -> FloatElement:
    return FloatElement(pytree)


def _named_value_collection_to_data_only_pytree(self) -> Dict[str, _PyTree]:
    return {key: to_pytree(value) for key, value in self._data.items()}


def _named_value_collection_from_data_only_pytree(pytree: Dict[str, _PyTree]) -> NamedValueCollectionElement:
    child_dict = {}
    for key, value in pytree.items():
        child_type, child_data = _decompose_element_pytree(value)
        child_dict[key] = _element_type_deserializer_map[child_type](child_data)
    return NamedValueCollectionElement(child_dict)


def _list_to_data_only_pytree(self) -> List[_PyTree]:
    return [to_pytree(item) for item in self._data]


def _list_from_data_only_pytree(pytree: List[_PyTree]) -> ListElement:
    children = []
    for item in pytree:
        child_type, child_data = _decompose_element_pytree(item)
        children.append(_element_type_deserializer_map[child_type](child_data))
    return ListElement(children)


def _tensor_element_to_data_only_pytree(self) -> _PyTree:
    return [self._data.shape, self._data.flatten().tolist()]


def _tensor_element_from_data_only_pytree(pytree: _PyTree) -> TensorElement:
    shape, data = pytree
    return TensorElement(np.array(data).reshape(tuple(shape)))


# Register classes
_element_type_serializer_map[DataElementType.STRING] = _string_to_data_only_pytree
_element_type_serializer_map[DataElementType.BOOL] = _bool_to_data_only_pytree
_element_type_serializer_map[DataElementType.INT] = _int_to_data_only_pytree
_element_type_serializer_map[DataElementType.FLOAT] = _float_to_data_only_pytree
_element_type_serializer_map[DataElementType.NAMED_VALUE_COLLECTION] = _named_value_collection_to_data_only_pytree
_element_type_serializer_map[DataElementType.LIST] = _list_to_data_only_pytree
_element_type_serializer_map[DataElementType.TENSOR] = _tensor_element_to_data_only_pytree

_element_type_deserializer_map[DataElementType.STRING] = _string_from_data_only_pytree
_element_type_deserializer_map[DataElementType.BOOL] = _bool_from_data_only_pytree
_element_type_deserializer_map[DataElementType.INT] = _int_from_data_only_pytree
_element_type_deserializer_map[DataElementType.FLOAT] = _float_from_data_only_pytree
_element_type_deserializer_map[DataElementType.NAMED_VALUE_COLLECTION] = _named_value_collection_from_data_only_pytree
_element_type_deserializer_map[DataElementType.LIST] = _list_from_data_only_pytree
_element_type_deserializer_map[DataElementType.TENSOR] = _tensor_element_from_data_only_pytree

assert set(_element_type_serializer_map.keys()) == set(DataElementType)
assert set(_element_type_deserializer_map.keys()) == set(DataElementType)
