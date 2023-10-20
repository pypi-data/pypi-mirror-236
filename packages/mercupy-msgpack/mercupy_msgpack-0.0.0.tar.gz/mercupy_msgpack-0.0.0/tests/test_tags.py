import unittest

import msgpack

from mercupy.tags import CondensedTags, TagNameComponent

# boilerplate
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().resolve().parent.parent))

from src.mercupy_msgpack import serialize_condensed_tags, deserialize_condensed_tags


class TestTagTokenTree(unittest.TestCase):

    def test_pytree_conversion(self):
        var1 = CondensedTags(TagNameComponent.CLOUD_DEPLOYED) / (
                CondensedTags(TagNameComponent.CLOUD_DEPLOYED) +
                CondensedTags(TagNameComponent.LOCALLY_DEPLOYED) / (
                        CondensedTags(TagNameComponent.CLOUD_DEPLOYED) + TagNameComponent.LOCALLY_DEPLOYED
                )
        )

        expected = {
            'component-name': [
                'cloud-deployed',
                {
                    'namespace': {
                        'collection': [
                            {'component-name': ['cloud-deployed', None]},
                            {
                                'component-name': [
                                    'locally-deployed',
                                    {
                                        'namespace': {
                                            'collection': [
                                                {'component-name': ['cloud-deployed', None]},
                                                {'component-name': ['locally-deployed', None]}]}}]}]}}]}

        serialized = serialize_condensed_tags(var1)
        self.assertEqual(msgpack.unpackb(serialized), expected)

        reconstructed = deserialize_condensed_tags(serialized)
        self.assertEqual(reconstructed, var1)


if __name__ == '__main__':
    unittest.main()
