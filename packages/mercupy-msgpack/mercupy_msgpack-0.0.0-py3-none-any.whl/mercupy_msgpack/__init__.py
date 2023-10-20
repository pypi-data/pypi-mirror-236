from mercupy.data_elements import DataElement
from mercupy.filter_elements import FilterElement
from mercupy.manifest_elements import ManifestElement
from mercupy.tags import TagTokenTree

import msgpack

from . import _data_elements, _tags, _filter_elements, _manifest_elements


def serialize_data_element(data_element: DataElement) -> bytes:
    return msgpack.packb(_data_elements.to_pytree(data_element))


def deserialize_data_element(msgpack_bytes: bytes) -> DataElement:
    return _data_elements.from_pytree(msgpack.unpackb(msgpack_bytes))


def serialize_condensed_tags(condensed_tags: TagTokenTree) -> bytes:
    return msgpack.packb(_tags.to_pytree(condensed_tags))


def deserialize_condensed_tags(msgpack_bytes: bytes) -> bytes:
    return _tags.from_pytree(msgpack.unpackb(msgpack_bytes))


def serialize_filter_element(filter_element: FilterElement) -> bytes:
    return msgpack.packb(_filter_elements.to_pytree(filter_element))


def deserialize_filter_element(msgpack_bytes: bytes) -> FilterElement:
    return _filter_elements.from_pytree(msgpack.unpackb(msgpack_bytes))


def serialize_manifest_element(manifest_element: ManifestElement) -> bytes:
    return msgpack.packb(_manifest_elements.to_pytree(manifest_element))


def deserialize_manifest_element(msgpack_bytes: bytes) -> ManifestElement:
    return _manifest_elements.from_pytree(msgpack.unpackb(msgpack_bytes))
