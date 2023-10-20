# TODO: change to better base classes; don't use deprecated ones
from typing import List, Dict, Union, Set
from collections.abc import Callable
from typeguard import typechecked
from dataclasses import dataclass

from mercupy.manifest_elements import (
    ManifestElement, ManifestElementType,
    StringElement, BoolElement, IntElement, FloatElement,
    DictElement, ListElement,
    TypeDeclarationElement, TypeFloatElement, TypeStringElement, TypeBoolElement, TypeIntElement,
    TypeListElement, TypeTupleElement, TypeTensorElement, TypeNamedValueCollectionElement,
    TagCollectionElement
)

from . import _tags

# TODO: recursive annotation?
_PyTree = Union[List, Dict, tuple, str, float, bool, int, None]

_element_type_name_enum_map: Dict[str, ManifestElementType] = {
    "string": ManifestElementType.STRING,
    "bool": ManifestElementType.BOOL,
    "int": ManifestElementType.INT,
    "float": ManifestElementType.FLOAT,
    "dict": ManifestElementType.DICT,
    "list": ManifestElementType.LIST,
    "tag-collection": ManifestElementType.TAG_COLLECTION,
    "type-declaration": ManifestElementType.TYPE_DECLARATION,
    "type-string": ManifestElementType.TYPE_STRING,
    "type-int": ManifestElementType.TYPE_INT,
    "type-float": ManifestElementType.TYPE_FLOAT,
    "type-bool": ManifestElementType.TYPE_BOOL,
    "type-tensor": ManifestElementType.TYPE_TENSOR,
    "type-named-value-collection": ManifestElementType.TYPE_NAMED_VALUE_COLLECTION,
    "type-list": ManifestElementType.TYPE_LIST,
    "type-tuple": ManifestElementType.TYPE_TUPLE
}

assert set(_element_type_name_enum_map.values()) == set(ManifestElementType)

_element_enum_name_map: Dict[ManifestElementType, str] = {
    value: key for key, value in _element_type_name_enum_map.items()}

_type_declaration_elements: Set[ManifestElementType] = {
    ManifestElementType.TYPE_STRING,
    ManifestElementType.TYPE_INT,
    ManifestElementType.TYPE_FLOAT,
    ManifestElementType.TYPE_BOOL,
    ManifestElementType.TYPE_TENSOR,
    ManifestElementType.TYPE_NAMED_VALUE_COLLECTION,
    ManifestElementType.TYPE_LIST,
    ManifestElementType.TYPE_TUPLE
}

_type_declaration_element_type_names: Set[str] = {
    _element_enum_name_map[elem_type] for elem_type in _type_declaration_elements}


_element_type_serializer_map: Dict[ManifestElementType, Callable[[ManifestElement], _PyTree]] = {}
_element_type_deserializer_map: Dict[ManifestElementType, Callable[[_PyTree], ManifestElement]] = {}


@dataclass
class _InvalidPyTreeError(Exception):
    pytree: _PyTree
    message: str | None = None


def _is_type_declaration_element(element_type: ManifestElementType) -> bool:
    return element_type in _type_declaration_elements


def _is_element_type_name_type_declaration(element_type_name: str) -> bool:
    return element_type_name in _type_declaration_element_type_names


def to_pytree(element: ManifestElement) -> _PyTree:
    return {_element_enum_name_map[element.element_type]: _element_type_serializer_map[element.element_type](element)}


def from_pytree(pytree: _PyTree) -> ManifestElement:
    elem_type, data = _decompose_element_pytree(pytree)
    return _element_type_deserializer_map[elem_type](data)


@typechecked
def _decompose_element_pytree(pytree: Dict[str, _PyTree] | str) -> tuple[ManifestElementType, _PyTree]:
    # TODO: error handling?
    """
    Decompose a manifest element pytree into its element type and its data.
    :param pytree:
    :return: element type, data
    """

    if isinstance(pytree, Dict):
        assert len(pytree) == 1
        type_name, data = next(iter(pytree.items()))
        return _element_type_name_enum_map[type_name], data
    else:
        return _element_type_name_enum_map[pytree], None


@typechecked
def _string_to_data_only_pytree(element: StringElement) -> str:
    return element.value


@typechecked
def _string_from_data_only_pytree(pytree: str) -> StringElement:
    return StringElement(pytree)


@typechecked
def _bool_to_data_only_pytree(element: BoolElement) -> bool:
    return element.value


@typechecked
def _bool_from_data_only_pytree(pytree: bool) -> BoolElement:
    return BoolElement(pytree)


@typechecked
def _int_to_data_only_pytree(element: IntElement) -> int:
    return element.value


@typechecked
def _int_from_data_only_pytree(pytree: int) -> IntElement:
    return IntElement(pytree)


@typechecked
def _float_to_data_only_pytree(element: FloatElement) -> float:
    return element.value


@typechecked
def _float_from_data_only_pytree(pytree: float) -> FloatElement:
    return FloatElement(pytree)


@typechecked
def _dict_to_data_only_pytree(element: DictElement) -> Dict[str, _PyTree]:
    return {key: to_pytree(value) for key, value in element.data.items()}


@typechecked
def _dict_from_data_only_pytree(pytree: Dict[str, _PyTree]) -> DictElement:
    child_dict = {}

    for key, value in pytree.items():
        child_type, child_data = _decompose_element_pytree(value)
        child_dict[key] = _element_type_deserializer_map[child_type](child_data)

    return DictElement(child_dict)


@typechecked
def _list_to_data_only_pytree(element: ListElement) -> List[_PyTree]:
    return [to_pytree(item) for item in element.data]


@typechecked
def _list_from_data_only_pytree(pytree: List[_PyTree]) -> ListElement:
    children = []

    for item in pytree:
        child_type, child_data = _decompose_element_pytree(item)
        children.append(_element_type_deserializer_map[child_type](child_data))

    return ListElement(children)


@typechecked
def _tag_collection_to_data_only_pytree(element: TagCollectionElement) -> _PyTree:
    return [_tags.to_pytree(tag_set) for tag_set in element.tags]


@typechecked
def _tag_collection_from_data_only_pytree(pytree: List[_PyTree]) -> TagCollectionElement:
    tag_sets = [_tags.from_pytree(subtree) for subtree in pytree]
    return TagCollectionElement(tag_sets)


@typechecked
def _type_declaration_to_data_only_pytree(element: TypeDeclarationElement) -> _PyTree:
    return to_pytree(element.type_declaration)


@typechecked
def _type_declaration_from_data_only_pytree(pytree: _PyTree) -> TypeDeclarationElement:
    element_type, data = _decompose_element_pytree(pytree)

    if not _is_type_declaration_element(element_type):
        raise _InvalidPyTreeError(pytree, f'Expected type declaration element, got {element_type}!')

    return TypeDeclarationElement(_element_type_deserializer_map[element_type](data))


@typechecked
def _type_int_to_data_only_pytree(element: TypeIntElement) -> _PyTree:
    return None


@typechecked
def _type_int_from_data_only_pytree(pytree: _PyTree) -> TypeIntElement:
    return TypeIntElement()


@typechecked
def _type_float_to_data_only_pytree(element: TypeFloatElement) -> _PyTree:
    return None


@typechecked
def _type_float_from_data_only_pytree(pytree: _PyTree) -> TypeFloatElement:
    return TypeFloatElement()


@typechecked
def _type_string_to_data_only_pytree(element: TypeStringElement) -> _PyTree:
    return None


@typechecked
def _type_string_from_data_only_pytree(pytree: _PyTree) -> TypeStringElement:
    return TypeStringElement()


@typechecked
def _type_bool_to_data_only_pytree(element: TypeBoolElement) -> _PyTree:
    return None


@typechecked
def _type_bool_from_data_only_pytree(pytree: _PyTree) -> TypeBoolElement:
    return TypeBoolElement()


@typechecked
def _type_tensor_to_data_only_pytree(element) -> tuple[int, ...]:
    return element.shape


@typechecked
def _type_tensor_from_data_only_pytree(pytree: List[int]) -> TypeTensorElement:
    return TypeTensorElement(tuple(pytree))


@typechecked
def _type_named_value_collection_to_data_only_pytree(element: TypeNamedValueCollectionElement) -> Dict[str, _PyTree]:
    return {key: to_pytree(value) for key, value in element.data.items()}


@typechecked
def _type_named_value_collection_from_data_only_pytree(pytree: Dict[str, _PyTree]) -> TypeNamedValueCollectionElement:
    children = {}

    for key, value in pytree.items():
        element_type, data = _decompose_element_pytree(value)

        if not _is_type_declaration_element(element_type):
            raise _InvalidPyTreeError(value, f'Expected type declaration element, got {element_type}!')

        children[key] = _element_type_deserializer_map[element_type](data)

    return TypeNamedValueCollectionElement(children)


@typechecked
def _type_list_to_data_only_pytree(element: TypeListElement) -> _PyTree:
    return to_pytree(element.element_type_declaration)


@typechecked
def _type_list_from_data_only_pytree(pytree: _PyTree) -> TypeListElement:
    element_type, data = _decompose_element_pytree(pytree)

    if not _is_type_declaration_element(element_type):
        raise _InvalidPyTreeError(pytree, f'Expected type declaration element, got {element_type}!')

    return TypeListElement(_element_type_deserializer_map[element_type](data))


@typechecked
def _type_tuple_to_data_only_pytree(element: TypeTupleElement) -> tuple[_PyTree, ...]:
    return tuple(to_pytree(element) for element in element.element_type_declarations)


@typechecked
def _type_tuple_from_data_only_pytree(pytree: List[_PyTree]) -> TypeTupleElement:
    element_type_declarations = []

    for element in pytree:
        elem_type, data = _decompose_element_pytree(element)
        if not _is_type_declaration_element(elem_type):
            raise _InvalidPyTreeError(pytree, f'Expected type declaration element, got {elem_type}!')
        element_type_declarations.append(_element_type_deserializer_map[elem_type](data))

    return TypeTupleElement(tuple(element_type_declarations))


_element_type_serializer_map[ManifestElementType.STRING] = _string_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.BOOL] = _bool_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.INT] = _int_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.FLOAT] = _float_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.DICT] = _dict_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.LIST] = _list_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.TAG_COLLECTION] = _tag_collection_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.TYPE_DECLARATION] = _type_declaration_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.TYPE_STRING] = _type_string_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.TYPE_INT] = _type_int_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.TYPE_FLOAT] = _type_float_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.TYPE_BOOL] = _type_bool_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.TYPE_TENSOR] = _type_tensor_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.TYPE_NAMED_VALUE_COLLECTION] = _type_named_value_collection_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.TYPE_LIST] = _type_list_to_data_only_pytree
_element_type_serializer_map[ManifestElementType.TYPE_TUPLE] = _type_tuple_to_data_only_pytree

assert set(_element_type_serializer_map.keys()) == set(ManifestElementType)

_element_type_deserializer_map[ManifestElementType.STRING] = _string_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.BOOL] = _bool_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.INT] = _int_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.FLOAT] = _float_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.DICT] = _dict_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.LIST] = _list_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.TAG_COLLECTION] = _tag_collection_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.TYPE_DECLARATION] = _type_declaration_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.TYPE_STRING] = _type_string_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.TYPE_INT] = _type_int_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.TYPE_FLOAT] = _type_float_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.TYPE_BOOL] = _type_bool_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.TYPE_TENSOR] = _type_tensor_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.TYPE_NAMED_VALUE_COLLECTION] = _type_named_value_collection_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.TYPE_LIST] = _type_list_from_data_only_pytree
_element_type_deserializer_map[ManifestElementType.TYPE_TUPLE] = _type_tuple_from_data_only_pytree

assert set(_element_type_deserializer_map.keys()) == set(ManifestElementType)
