from typing import List, Dict, Union
from typeguard import typechecked

from mercupy.tags import TagTokenTree, TagNameComponent, TagTokenType

_PyTree = Union[List, Dict, tuple, str, float, bool, int]


_tag_name_components_enum_name_mapping = {
    TagNameComponent.CLOUD_DEPLOYED: 'cloud-deployed',
    TagNameComponent.LOCALLY_DEPLOYED: 'locally-deployed'
}

assert set(_tag_name_components_enum_name_mapping.keys()) == set(TagNameComponent)

_tag_name_components_name_enum_mapping = {value: key for key, value in _tag_name_components_enum_name_mapping.items()}


_token_type_enum_name_mapping: Dict[TagTokenType, str] = {
    TagTokenType.NAMESPACE_OPERATOR: 'namespace',
    TagTokenType.CONCATENATION_OPERATOR: 'concatenation',
    TagTokenType.COMPONENT_NAME: 'component-name',
    TagTokenType.COLLECTION: 'collection'
}

assert set(_token_type_enum_name_mapping.keys()) == set(TagTokenType)

_token_type_name_enum_mapping: Dict[str, TagTokenType] = {
    value: key for key, value in _token_type_enum_name_mapping.items()}


@typechecked
def to_pytree(condensed_tags: TagTokenTree) -> _PyTree:
    if condensed_tags.token_type == TagTokenType.COLLECTION:
        return {
            _token_type_enum_name_mapping[TagTokenType.COLLECTION]:
                [to_pytree(child) for child in condensed_tags.children]
        }
    elif condensed_tags.token_type == TagTokenType.NAMESPACE_OPERATOR or \
            condensed_tags.token_type == TagTokenType.CONCATENATION_OPERATOR:
        # :: / . both have next field
        return {
            _token_type_enum_name_mapping[condensed_tags.token_type]:
                to_pytree(condensed_tags.next_token) if condensed_tags.next_token is not None else None
        }

    else:
        # name component
        return {
            _token_type_enum_name_mapping[condensed_tags.token_type]:
                [_tag_name_components_enum_name_mapping[condensed_tags.name_component],
                 to_pytree(condensed_tags.next_token) if condensed_tags.next_token is not None else None]
        }


@typechecked
def from_pytree(pytree: Dict[str, _PyTree]):
    assert len(pytree) == 1
    token_type = _token_type_name_enum_mapping[next(iter(pytree.keys()))]

    if token_type == TagTokenType.COLLECTION:
        children = [from_pytree(child) for child in next(iter(pytree.values()))]
        return TagTokenTree(token_type, children=children)
    elif token_type == TagTokenType.NAMESPACE_OPERATOR or token_type == TagTokenType.CONCATENATION_OPERATOR:
        # :: / . both have next field
        next_tree_raw = next(iter(pytree.values()))
        if next_tree_raw is None:
            next_tree = None
        else:
            next_tree = from_pytree(next_tree_raw)

        return TagTokenTree(token_type, next_token=next_tree)
    else:
        # name component
        name, next_tree_raw = next(iter(pytree.values()))
        name_enum = _tag_name_components_name_enum_mapping[name]

        if next_tree_raw is None:
            next_tree = None
        else:
            next_tree = from_pytree(next_tree_raw)

        return TagTokenTree(token_type, name_component=name_enum, next_token=next_tree)
