# TODO: check for argument validity in constructors & PyTree parsing methods?
from typing import List, Dict, Union
from dataclasses import dataclass
from collections.abc import Callable

from typeguard import typechecked

from mercupy.filter_elements import (
    FilterElementType, FilterOperationType, FilterElement,
    IntElement, BoolElement, FloatElement, StringElement, ListElement, DictElement,
    TypeDeclarationElement, TypeTupleElement, TypeNamedValueCollectionElement, TypeListElement,
    TypeIntElement, TypeFloatElement, TypeStringElement, TypeBoolElement, TypeTensorElement, DimElement,
    TagCollectionElement, LogicalElement
)

from mercupy.tags import TagTokenTree

from . import _tags

_PyTree = Union[List, Dict, tuple, str, float, bool, int, None]

_element_type_name_enum_map: Dict[str, FilterElementType] = {
    "string": FilterElementType.STRING,
    "bool": FilterElementType.BOOL,
    "int": FilterElementType.INT,
    "float": FilterElementType.FLOAT,
    "dict": FilterElementType.DICT,
    "list": FilterElementType.LIST,
    "tag-collection": FilterElementType.TAG_COLLECTION,
    "type-declaration": FilterElementType.TYPE_DECLARATION,
    "type-string": FilterElementType.TYPE_STRING,
    "type-int": FilterElementType.TYPE_INT,
    "type-float": FilterElementType.TYPE_FLOAT,
    "type-bool": FilterElementType.TYPE_BOOL,
    "type-tensor": FilterElementType.TYPE_TENSOR,
    "type-named-value-collection": FilterElementType.TYPE_NAMED_VALUE_COLLECTION,
    "type-list": FilterElementType.TYPE_LIST,
    "type-tuple": FilterElementType.TYPE_TUPLE,
    "logical": FilterElementType.LOGICAL,
    "dim": FilterElementType.DIM
}

assert set(_element_type_name_enum_map.values()) == set(FilterElementType)

_element_type_enum_name_map: Dict[FilterElementType, str] = {
    value: key for key, value in _element_type_name_enum_map.items()}

_operation_type_name_enum_map: Dict[str, FilterOperationType] = {
    "all": FilterOperationType.ALL,
    "none": FilterOperationType.NONE,
    "eq": FilterOperationType.EQ,
    "lt": FilterOperationType.LT,
    "le": FilterOperationType.LE,
    "gt": FilterOperationType.GT,
    "ge": FilterOperationType.GE,
    "type-match": FilterOperationType.TYPE_MATCH,
    "and": FilterOperationType.AND,
    "or": FilterOperationType.OR,
    "not": FilterOperationType.NOT,
    "implicit-tag-match": FilterOperationType.IMPLICIT_TAG_MATCH,
    "explicit-tag-match": FilterOperationType.EXPLICIT_TAG_MATCH
}

assert set(_operation_type_name_enum_map.values()) == set(FilterOperationType)


def to_pytree(element: FilterElement) -> _PyTree:
    return {_element_type_enum_name_map[element.element_type]: _element_type_serializer_map[element.element_type](element)}


_operation_type_enum_name_map: Dict[FilterOperationType, str] = {
    value: key for key, value in _operation_type_name_enum_map.items()}

_element_type_serializer_map: Dict[FilterElementType, Callable[[FilterElement], _PyTree]] = {}
_element_type_deserializer_map: Dict[FilterElementType, Callable[[_PyTree], FilterElement]] = {}


def from_pytree(pytree: _PyTree) -> FilterElement:
    element_type, data = _decompose_element_pytree(pytree)
    return _element_type_deserializer_map[element_type](data)


@dataclass
class _InvalidPyTreeError(Exception):
    pytree: _PyTree
    message: str | None = None


def _decompose_element_pytree(pytree: Dict[str, _PyTree]) \
        -> tuple[FilterElementType, _PyTree]:
    # TODO: error handling?
    assert len(pytree) == 1
    type_name, data = next(iter(pytree.items()))

    return _element_type_name_enum_map[type_name], data


@typechecked
def _string_to_data_only_pytree(element: StringElement) -> _PyTree:
    return [_operation_type_enum_name_map[element.operation], element.value]


@typechecked
def _string_from_data_only_pytree(data_only_pytree: _PyTree) -> StringElement:
    operation_name, string = data_only_pytree
    return StringElement(
        operation=_operation_type_name_enum_map[operation_name],
        string=string
    )


@typechecked
def _bool_to_data_only_pytree(element: BoolElement) -> _PyTree:
    return [_operation_type_enum_name_map[element.operation], element.value]


@typechecked
def _bool_from_data_only_pytree(data_only_pytree: _PyTree) -> BoolElement:
    operation_name, value = data_only_pytree
    return BoolElement(
        operation=_operation_type_name_enum_map[operation_name],
        value=value
    )


@typechecked
def _int_to_data_only_pytree(element: IntElement) -> _PyTree:
    return [_operation_type_enum_name_map[element.operation], element.value]


@typechecked
def _int_from_data_only_pytree(data_only_pytree: _PyTree) -> IntElement:
    operation_name, value = data_only_pytree
    return IntElement(
        operation=_operation_type_name_enum_map[operation_name],
        value=value
    )


@typechecked
def _float_to_data_only_pytree(element: FloatElement) -> _PyTree:
    return [_operation_type_enum_name_map[element.operation], element.value]


@typechecked
def _float_from_data_only_pytree(data_only_pytree: _PyTree) -> FloatElement:
    operation_name, value = data_only_pytree
    return FloatElement(
        operation=_operation_type_name_enum_map[operation_name],
        value=value
    )


@typechecked
def _list_to_data_only_pytree(element: ListElement) -> _PyTree:
    elements_pytree = [to_pytree(element) for element in element.elements] if element.elements is not None else None
    return [_operation_type_enum_name_map[element.operation], elements_pytree]


@typechecked
def _list_from_data_only_pytree(data_only_pytree: _PyTree) -> ListElement:
    operation_name, elements_pytree = data_only_pytree
    if elements_pytree is not None:
        elements = []

        for element in elements_pytree:
            elem_type, data = _decompose_element_pytree(element)
            new_element = _element_type_deserializer_map[elem_type](data)
            elements.append(new_element)
    else:
        elements = None

    return ListElement(
        operation=_operation_type_name_enum_map[operation_name],
        elements=elements
    )


@typechecked
def _dict_to_data_only_pytree(element: DictElement) -> _PyTree:
    elements_pytree = {key: to_pytree(element) for key, element in
                       element.elements.items()} if element.elements is not None else None
    return [_operation_type_enum_name_map[element.operation], elements_pytree]


@typechecked
def _dict_from_data_only_pytree(data_only_pytree: _PyTree) -> DictElement:
    operation_name, elements_pytree = data_only_pytree
    if elements_pytree is not None:
        elements = {}

        for key, element in elements_pytree.items():
            elem_type, data = _decompose_element_pytree(element)
            new_element = _element_type_deserializer_map[elem_type](data)
            elements[key] = new_element
    else:
        elements = None

    return DictElement(
        operation=_operation_type_name_enum_map[operation_name],
        elements=elements
    )


@typechecked
def _type_declaration_to_data_only_pytree(element: TypeDeclarationElement) -> _PyTree:
    return [_operation_type_enum_name_map[element.operation],
            to_pytree(element.type_declaration) if element.type_declaration is not None else None]


@typechecked
def _type_declaration_from_data_only_pytree(data_only_pytree: _PyTree) -> TypeDeclarationElement:
    operation_name, type_declaration = data_only_pytree
    if type_declaration is not None:
        element_type, data = _decompose_element_pytree(type_declaration)
        declaration_element = _element_type_deserializer_map[element_type](data)
    else:
        declaration_element = None

    return TypeDeclarationElement(
        operation=_operation_type_name_enum_map[operation_name],
        type_declaration=declaration_element
    )


@typechecked
def _type_named_value_collection_to_data_only_pytree(element: TypeNamedValueCollectionElement) -> _PyTree:
    elements_pytree = {key: to_pytree(element) for key, element in
                       element.elements.items()} if element.elements is not None else None
    return [_operation_type_enum_name_map[element.operation], elements_pytree]


@typechecked
def _type_named_value_collection_from_data_only_pytree(data_only_pytree: _PyTree) -> TypeNamedValueCollectionElement:
    operation_name, elements_pytree = data_only_pytree

    if elements_pytree is not None:
        elements = {}

        for key, element in elements_pytree.items():
            elem_type, data = _decompose_element_pytree(element)
            new_element = _element_type_deserializer_map[elem_type](data)
            elements[key] = new_element
    else:
        elements = None

    return TypeNamedValueCollectionElement(
        operation=_operation_type_name_enum_map[operation_name],
        elements=elements
    )


@typechecked
def _type_list_to_data_only_pytree(element: TypeListElement) -> _PyTree:
    return [_operation_type_enum_name_map[element.operation],
            to_pytree(element.element_type_declaration) if element.element_type_declaration is not None else None]


@typechecked
def _type_list_from_data_only_pytree(data_only_pytree: _PyTree) -> TypeListElement:
    operation_name, type_declaration = data_only_pytree
    if type_declaration is not None:
        element_type, data = _decompose_element_pytree(type_declaration)
        element_type_declaration = _element_type_deserializer_map[element_type](data)
    else:
        element_type_declaration = None

    return TypeListElement(
        operation=_operation_type_name_enum_map[operation_name],
        element_type_declaration=element_type_declaration
    )


@typechecked
def _type_tuple_to_data_only_pytree(element: TypeTupleElement) -> _PyTree:
    elements_pytree = [to_pytree(element) for element in element.elements] if element.elements is not None else None
    return [_operation_type_enum_name_map[element.operation], elements_pytree]


@typechecked
def _type_tuple_from_data_only_pytree(data_only_pytree: _PyTree) -> TypeTupleElement:
    operation_name, elements_pytree = data_only_pytree

    if elements_pytree is not None:
        elements = []

        for element in elements_pytree:
            elem_type, data = _decompose_element_pytree(element)
            new_element = _element_type_deserializer_map[elem_type](data)
            elements.append(new_element)
    else:
        elements = None

    return TypeTupleElement(
        operation=_operation_type_name_enum_map[operation_name],
        elements=elements
    )


@typechecked
def _dim_element_to_data_only_pytree(element: DimElement) -> _PyTree | None:
    return [_operation_type_enum_name_map[element.operation], element.size]


@typechecked
def _dim_element_from_data_only_pytree(data_only_pytree: _PyTree) -> DimElement:
    operation_name, size = data_only_pytree

    return DimElement(
        operation=_operation_type_name_enum_map[operation_name],
        size=size
    )


@typechecked
def _type_tensor_to_data_only_pytree(element: TypeTensorElement) -> _PyTree | None:
    return [
        _operation_type_enum_name_map[element.operation],
        [to_pytree(sub_element) for sub_element in element.dimensions] if element.dimensions is not None else None
    ]


@typechecked
def _type_tensor_from_data_only_pytree(data_only_pytree: _PyTree) -> TypeTensorElement:
    operation_name, dimensions = data_only_pytree
    if dimensions is not None:
        dim_elements = []

        for dim_tree in dimensions:
            elem_type, data = _decompose_element_pytree(dim_tree)
            dim_elements.append(_element_type_deserializer_map[elem_type](data))
    else:
        dim_elements = None

    return TypeTensorElement(
        operation=_operation_type_name_enum_map[operation_name],
        dimensions=dim_elements
    )


@typechecked
def _type_string_to_data_only_pytree(element: TypeStringElement) -> _PyTree:
    return [_operation_type_enum_name_map[element.operation]]


@typechecked
def _type_string_from_data_only_pytree(data_only_pytree: _PyTree) -> TypeStringElement:
    operation_name = data_only_pytree[0]
    return TypeStringElement(
        operation=_operation_type_name_enum_map[operation_name],
    )


@typechecked
def _type_bool_to_data_only_pytree(element: TypeBoolElement) -> _PyTree:
    return [_operation_type_enum_name_map[element.operation]]


@typechecked
def _type_bool_from_data_only_pytree(data_only_pytree: _PyTree) -> TypeBoolElement:
    operation_name = data_only_pytree[0]
    return TypeBoolElement(
        operation=_operation_type_name_enum_map[operation_name],
    )


@typechecked
def _type_int_to_data_only_pytree(element: TypeIntElement) -> _PyTree:
    return [_operation_type_enum_name_map[element.operation]]


@typechecked
def _type_int_from_data_only_pytree(data_only_pytree: _PyTree) -> TypeIntElement:
    operation_name = data_only_pytree[0]
    return TypeIntElement(
        operation=_operation_type_name_enum_map[operation_name],
    )


@typechecked
def _type_float_to_data_only_pytree(element: TypeFloatElement) -> _PyTree:
    return [_operation_type_enum_name_map[element.operation]]


@typechecked
def _type_float_from_data_only_pytree(data_only_pytree: _PyTree) -> TypeFloatElement:
    operation_name = data_only_pytree[0]
    return TypeFloatElement(
        operation=_operation_type_name_enum_map[operation_name],
    )


@typechecked
def _logical_to_data_only_pytree(element: LogicalElement) -> _PyTree:
    elements_pytree = [to_pytree(element) for element in element.predicates]
    return [_operation_type_enum_name_map[element.operation], elements_pytree]


@typechecked
def _logical_from_data_only_pytree(data_only_pytree: _PyTree) -> LogicalElement:
    operation_name, elements_pytree = data_only_pytree
    elements = []

    for element in elements_pytree:
        elem_type, data = _decompose_element_pytree(element)
        new_element = _element_type_deserializer_map[elem_type](data)
        elements.append(new_element)

    return LogicalElement(
        operation=_operation_type_name_enum_map[operation_name],
        predicates=elements
    )


@typechecked
def _tag_collection_to_data_only_pytree(element: TagCollectionElement) -> _PyTree | None:
    return [
        _operation_type_enum_name_map[element.operation],
        [_tags.to_pytree(tag_set) for tag_set in element.condensed_tags] if element.condensed_tags is not None else None
    ]


@typechecked
def _tag_collection_from_data_only_pytree(data_only_pytree: _PyTree) -> TagCollectionElement:
    operation_name, tags_tree = data_only_pytree
    if tags_tree is not None:
        condensed_tags = []

        for tag_set_tree in tags_tree:
            condensed_tags.append(_tags.from_pytree(tag_set_tree))
    else:
        condensed_tags = None

    return TagCollectionElement(
        operation=_operation_type_name_enum_map[operation_name],
        condensed_tags=condensed_tags
    )


_element_type_deserializer_map[FilterElementType.STRING] = _string_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.BOOL] = _bool_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.INT] = _int_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.FLOAT] = _float_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.DICT] = _dict_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.LIST] = _list_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.TAG_COLLECTION] = _tag_collection_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.TYPE_DECLARATION] = _type_declaration_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.TYPE_STRING] = _type_string_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.TYPE_INT] = _type_int_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.TYPE_FLOAT] = _type_float_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.TYPE_BOOL] = _type_bool_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.TYPE_TENSOR] = _type_tensor_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.TYPE_NAMED_VALUE_COLLECTION] = _type_named_value_collection_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.TYPE_LIST] = _type_list_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.TYPE_TUPLE] = _type_tuple_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.DIM] = _dim_element_from_data_only_pytree
_element_type_deserializer_map[FilterElementType.LOGICAL] = _logical_from_data_only_pytree

_element_type_serializer_map[FilterElementType.STRING] = _string_to_data_only_pytree
_element_type_serializer_map[FilterElementType.BOOL] = _bool_to_data_only_pytree
_element_type_serializer_map[FilterElementType.INT] = _int_to_data_only_pytree
_element_type_serializer_map[FilterElementType.FLOAT] = _float_to_data_only_pytree
_element_type_serializer_map[FilterElementType.DICT] = _dict_to_data_only_pytree
_element_type_serializer_map[FilterElementType.LIST] = _list_to_data_only_pytree
_element_type_serializer_map[FilterElementType.TAG_COLLECTION] = _tag_collection_to_data_only_pytree
_element_type_serializer_map[FilterElementType.TYPE_DECLARATION] = _type_declaration_to_data_only_pytree
_element_type_serializer_map[FilterElementType.TYPE_STRING] = _type_string_to_data_only_pytree
_element_type_serializer_map[FilterElementType.TYPE_INT] = _type_int_to_data_only_pytree
_element_type_serializer_map[FilterElementType.TYPE_FLOAT] = _type_float_to_data_only_pytree
_element_type_serializer_map[FilterElementType.TYPE_BOOL] = _type_bool_to_data_only_pytree
_element_type_serializer_map[FilterElementType.TYPE_TENSOR] = _type_tensor_to_data_only_pytree
_element_type_serializer_map[FilterElementType.TYPE_NAMED_VALUE_COLLECTION] = _type_named_value_collection_to_data_only_pytree
_element_type_serializer_map[FilterElementType.TYPE_LIST] = _type_list_to_data_only_pytree
_element_type_serializer_map[FilterElementType.TYPE_TUPLE] = _type_tuple_to_data_only_pytree
_element_type_serializer_map[FilterElementType.DIM] = _dim_element_to_data_only_pytree
_element_type_serializer_map[FilterElementType.LOGICAL] = _logical_to_data_only_pytree

assert set(_element_type_deserializer_map.keys()) == set(FilterElementType)
assert set(_element_type_serializer_map.keys()) == set(FilterElementType)
