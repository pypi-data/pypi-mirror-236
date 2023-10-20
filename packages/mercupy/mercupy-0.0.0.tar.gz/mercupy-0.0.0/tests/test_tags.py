import unittest

# boilerplate
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().resolve().parent.parent))

from src.mercupy.tags import TagNameComponent, CondensedTags


class TestTagTokenTree(unittest.TestCase):

    def test_eq(self):
        var1 = CondensedTags(TagNameComponent.CLOUD_DEPLOYED) / (
                CondensedTags(TagNameComponent.CLOUD_DEPLOYED) + TagNameComponent.LOCALLY_DEPLOYED
        )
        var2 = CondensedTags(TagNameComponent.CLOUD_DEPLOYED) / (
                CondensedTags(TagNameComponent.CLOUD_DEPLOYED) + CondensedTags(TagNameComponent.LOCALLY_DEPLOYED)
        )
        var3 = CondensedTags(TagNameComponent.CLOUD_DEPLOYED) / (
                CondensedTags(TagNameComponent.CLOUD_DEPLOYED) / TagNameComponent.CLOUD_DEPLOYED
        )
        var4 = CondensedTags(TagNameComponent.CLOUD_DEPLOYED) / TagNameComponent.CLOUD_DEPLOYED

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)


if __name__ == '__main__':
    unittest.main()
