import unittest

# boilerplate
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().resolve().parent.parent))

import src.mercupy.filter_elements as fe
from src.mercupy import tags


class TestStringElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.StringElement(fe.FilterOperationType.ALL, 'test')
        var2 = fe.StringElement(fe.FilterOperationType.ALL, 'test')
        var3 = fe.StringElement(fe.FilterOperationType.ALL, 'tester')
        var4 = fe.IntElement(fe.FilterOperationType.EQ, 5)
        var5 = 'a'
        var6 = fe.StringElement(fe.FilterOperationType.NONE, 'test')

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)
        self.assertNotEqual(var1, var6)

    def test_data_getter(self):
        var1 = fe.StringElement(fe.FilterOperationType.EQ, 'test')
        self.assertEqual(var1.operation, fe.FilterOperationType.EQ)
        self.assertEqual(var1.value, 'test')


class TestBoolElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.BoolElement(fe.FilterOperationType.EQ, True)
        var2 = fe.BoolElement(fe.FilterOperationType.EQ, True)
        var3 = fe.BoolElement(fe.FilterOperationType.EQ, False)
        var4 = fe.IntElement(fe.FilterOperationType.EQ, 1)
        var5 = 'a'
        var6 = fe.BoolElement(fe.FilterOperationType.ALL, False)

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)
        self.assertNotEqual(var1, var6)

    def test_data_getter(self):
        var1 = fe.BoolElement(fe.FilterOperationType.EQ, True)
        self.assertEqual(var1.operation, fe.FilterOperationType.EQ)
        self.assertEqual(var1.value, True)


class TestIntElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.IntElement(fe.FilterOperationType.EQ, 5)
        var2 = fe.IntElement(fe.FilterOperationType.EQ, 5)
        var3 = fe.IntElement(fe.FilterOperationType.EQ, 7)
        var4 = fe.FloatElement(fe.FilterOperationType.EQ, 5.0)
        var5 = '5'
        var6 = fe.IntElement(fe.FilterOperationType.GT, 5)

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)
        self.assertNotEqual(var1, var6)

    def test_data_getter(self):
        var1 = fe.IntElement(fe.FilterOperationType.LT, 5)
        self.assertEqual(var1.operation, fe.FilterOperationType.LT)
        self.assertEqual(var1.value, 5)


class TestFloatElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.FloatElement(fe.FilterOperationType.GE, 5.5)
        var2 = fe.FloatElement(fe.FilterOperationType.GE, 5.5)
        var3 = fe.FloatElement(fe.FilterOperationType.GE, 7.5)
        var4 = fe.IntElement(fe.FilterOperationType.GE, 5)
        var5 = '5.5'
        var6 = fe.FloatElement(fe.FilterOperationType.EQ, 5.5)

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)
        self.assertNotEqual(var1, var6)

    def test_data_getter(self):
        var1 = fe.FloatElement(fe.FilterOperationType.GE, 5.5)
        self.assertEqual(var1.operation, fe.FilterOperationType.GE)
        self.assertEqual(var1.value, 5.5)


class TestDictElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.DictElement(fe.FilterOperationType.ALL, {
            'a': fe.StringElement(fe.FilterOperationType.EQ, 'test'),
            'b': fe.IntElement(fe.FilterOperationType.EQ, 1)
        })

        var2 = fe.DictElement(fe.FilterOperationType.ALL, {
            'a': fe.StringElement(fe.FilterOperationType.EQ, 'test'),
            'b': fe.IntElement(fe.FilterOperationType.EQ, 1)
        })

        var3 = fe.DictElement(fe.FilterOperationType.ALL, {
            'a': fe.StringElement(fe.FilterOperationType.EQ, 'test'),
            'b': fe.IntElement(fe.FilterOperationType.EQ, 2)
        })

        var4 = fe.DictElement(fe.FilterOperationType.ALL, {
            'a': fe.StringElement(fe.FilterOperationType.EQ, 'test'),
            'b': fe.FloatElement(fe.FilterOperationType.EQ, 1)
        })

        var5 = fe.DictElement(fe.FilterOperationType.NONE, {
            'a': fe.StringElement(fe.FilterOperationType.EQ, 'test'),
            'b': fe.IntElement(fe.FilterOperationType.EQ, 1)
        })

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, 'test')
        self.assertNotEqual(var1, var5)

    def test_data_getter(self):
        data = {'a': fe.StringElement(fe.FilterOperationType.EQ, 'test')}
        var1 = fe.DictElement(fe.FilterOperationType.ALL, data)
        self.assertEqual(var1.operation, fe.FilterOperationType.ALL)
        self.assertEqual(var1.elements, data)


class TestListElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.ListElement(fe.FilterOperationType.ALL, [
            fe.StringElement(fe.FilterOperationType.EQ, 'test1'),
            fe.IntElement(fe.FilterOperationType.EQ, 1)
        ])

        var2 = fe.ListElement(fe.FilterOperationType.ALL, [
            fe.StringElement(fe.FilterOperationType.EQ, 'test1'),
            fe.IntElement(fe.FilterOperationType.EQ, 1)
        ])

        var3 = fe.ListElement(fe.FilterOperationType.ALL, [
            fe.StringElement(fe.FilterOperationType.EQ, 'test1'),
            fe.IntElement(fe.FilterOperationType.EQ, 2)
        ])

        var4 = fe.ListElement(fe.FilterOperationType.ALL, [
            fe.StringElement(fe.FilterOperationType.EQ, 'test1'),
            fe.FloatElement(fe.FilterOperationType.EQ, 1.0)
        ])

        var5 = fe.ListElement(fe.FilterOperationType.NONE, [
            fe.StringElement(fe.FilterOperationType.EQ, 'test1'),
            fe.IntElement(fe.FilterOperationType.EQ, 1)
        ])

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)
        self.assertNotEqual(var1, ['test1', 1])

    def test_data_getter(self):
        data = [fe.StringElement(fe.FilterOperationType.EQ, 'test1')]
        var1 = fe.ListElement(fe.FilterOperationType.ALL, data)
        self.assertEqual(var1.operation, fe.FilterOperationType.ALL)
        self.assertEqual(var1.elements, data)


# TODO: sample data that actually makes sense?
class TestLogicalElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.LogicalElement(fe.FilterOperationType.AND, [
            fe.StringElement(fe.FilterOperationType.EQ, 'test1'),
            fe.IntElement(fe.FilterOperationType.EQ, 1)
        ])

        var2 = fe.LogicalElement(fe.FilterOperationType.AND, [
            fe.StringElement(fe.FilterOperationType.EQ, 'test1'),
            fe.IntElement(fe.FilterOperationType.EQ, 1)
        ])

        var3 = fe.LogicalElement(fe.FilterOperationType.AND, [
            fe.StringElement(fe.FilterOperationType.EQ, 'test1'),
            fe.IntElement(fe.FilterOperationType.EQ, 2)
        ])

        var4 = fe.LogicalElement(fe.FilterOperationType.AND, [
            fe.StringElement(fe.FilterOperationType.EQ, 'test1'),
            fe.FloatElement(fe.FilterOperationType.EQ, 1.0)
        ])

        var5 = fe.LogicalElement(fe.FilterOperationType.OR, [
            fe.StringElement(fe.FilterOperationType.EQ, 'test1'),
            fe.IntElement(fe.FilterOperationType.EQ, 1)
        ])

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)
        self.assertNotEqual(var1, ['test1', 1])

    def test_data_getter(self):
        data = [fe.StringElement(fe.FilterOperationType.EQ, 'test1')]
        var1 = fe.LogicalElement(fe.FilterOperationType.NOT, data)
        self.assertEqual(var1.operation, fe.FilterOperationType.NOT)
        self.assertEqual(var1.predicates, data)


class TestTagCollectionElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.TagCollectionElement(fe.FilterOperationType.IMPLICIT_TAG_MATCH, [
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) + tags.TagNameComponent.LOCALLY_DEPLOYED
            ),
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.LOCALLY_DEPLOYED) + tags.TagNameComponent.CLOUD_DEPLOYED
            )
        ])

        var2 = fe.TagCollectionElement(fe.FilterOperationType.IMPLICIT_TAG_MATCH, [
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) + tags.TagNameComponent.LOCALLY_DEPLOYED
            ),
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.LOCALLY_DEPLOYED) + tags.TagNameComponent.CLOUD_DEPLOYED
            )
        ])

        var3 = fe.TagCollectionElement(fe.FilterOperationType.IMPLICIT_TAG_MATCH, [
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) + tags.TagNameComponent.LOCALLY_DEPLOYED
            ),
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) + tags.TagNameComponent.LOCALLY_DEPLOYED
            )
        ])

        var4 = fe.StringElement(fe.FilterOperationType.EQ, 'test')

        var5 = fe.TagCollectionElement(fe.FilterOperationType.EXPLICIT_TAG_MATCH, [
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) + tags.TagNameComponent.LOCALLY_DEPLOYED
            ),
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.LOCALLY_DEPLOYED) + tags.TagNameComponent.CLOUD_DEPLOYED
            )
        ])

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)

    def test_data_getter(self):
        data = [
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) + tags.TagNameComponent.LOCALLY_DEPLOYED
            ),
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.LOCALLY_DEPLOYED) + tags.TagNameComponent.CLOUD_DEPLOYED
            )
        ]

        var1 = fe.TagCollectionElement(fe.FilterOperationType.EXPLICIT_TAG_MATCH, data)

        self.assertEqual(var1.operation, fe.FilterOperationType.EXPLICIT_TAG_MATCH)
        self.assertEqual(var1.condensed_tags, data)


class TestTypeDeclarationElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.TypeDeclarationElement(fe.FilterOperationType.TYPE_MATCH,
                                         fe.TypeStringElement(fe.FilterOperationType.NONE))
        var2 = fe.TypeDeclarationElement(fe.FilterOperationType.TYPE_MATCH,
                                         fe.TypeStringElement(fe.FilterOperationType.NONE))
        var3 = fe.TypeDeclarationElement(fe.FilterOperationType.TYPE_MATCH,
                                         fe.TypeFloatElement(fe.FilterOperationType.NONE))
        var4 = fe.TypeDeclarationElement(fe.FilterOperationType.NONE, fe.TypeStringElement(fe.FilterOperationType.NONE))

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, ['test1', 1])
        self.assertNotEqual(var1, var4)

    def test_data_getter(self):
        data = fe.TypeStringElement(fe.FilterOperationType.NONE)
        var1 = fe.TypeDeclarationElement(fe.FilterOperationType.NONE, data)
        self.assertEqual(var1.operation, fe.FilterOperationType.NONE)
        self.assertEqual(var1.type_declaration, data)


class TestTypeStringElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.TypeStringElement(fe.FilterOperationType.NONE)
        var2 = fe.TypeStringElement(fe.FilterOperationType.NONE)
        var3 = fe.TypeFloatElement(fe.FilterOperationType.NONE)

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, ['test1', 1])

    def test_data_getter(self):
        var1 = fe.TypeStringElement(fe.FilterOperationType.NONE)
        self.assertEqual(var1.operation, fe.FilterOperationType.NONE)


class TestTypeBoolElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.TypeBoolElement(fe.FilterOperationType.NONE)
        var2 = fe.TypeBoolElement(fe.FilterOperationType.NONE)
        var3 = fe.TypeIntElement(fe.FilterOperationType.NONE)

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, ['test2', 2])

    def test_data_getter(self):
        var1 = fe.TypeBoolElement(fe.FilterOperationType.NONE)
        self.assertEqual(var1.operation, fe.FilterOperationType.NONE)


class TestTypeIntElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.TypeIntElement(fe.FilterOperationType.NONE)
        var2 = fe.TypeIntElement(fe.FilterOperationType.NONE)
        var3 = fe.TypeFloatElement(fe.FilterOperationType.NONE)

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, ['test3', 3])

    def test_data_getter(self):
        var1 = fe.TypeIntElement(fe.FilterOperationType.NONE)
        self.assertEqual(var1.operation, fe.FilterOperationType.NONE)


class TestTypeFloatElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.TypeFloatElement(fe.FilterOperationType.NONE)
        var2 = fe.TypeFloatElement(fe.FilterOperationType.NONE)
        var3 = fe.TypeBoolElement(fe.FilterOperationType.NONE)

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, ['test4', 4])

    def test_data_getter(self):
        var1 = fe.TypeFloatElement(fe.FilterOperationType.NONE)
        self.assertEqual(var1.operation, fe.FilterOperationType.NONE)


class TestDimElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.DimElement(fe.FilterOperationType.GE, 5)
        var2 = fe.DimElement(fe.FilterOperationType.GE, 5)
        var3 = fe.DimElement(fe.FilterOperationType.LE, 5)
        var4 = fe.DimElement(fe.FilterOperationType.GE, 6)
        var5 = fe.TypeIntElement(fe.FilterOperationType.NONE)

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)

    def test_data_getter(self):
        var1 = fe.DimElement(fe.FilterOperationType.EQ, 5)
        self.assertEqual(var1.operation, fe.FilterOperationType.EQ)
        self.assertEqual(var1.size, 5)


class TestTypeTensorElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.TypeTensorElement(fe.FilterOperationType.ALL, [fe.DimElement(fe.FilterOperationType.EQ, 2),
                                                                 fe.DimElement(fe.FilterOperationType.EQ, 3)])
        var2 = fe.TypeTensorElement(fe.FilterOperationType.ALL, [fe.DimElement(fe.FilterOperationType.EQ, 2),
                                                                 fe.DimElement(fe.FilterOperationType.EQ, 3)])
        var3 = fe.TypeTensorElement(fe.FilterOperationType.ALL, [fe.DimElement(fe.FilterOperationType.EQ, 3),
                                                                 fe.DimElement(fe.FilterOperationType.EQ, 2)])
        var4 = fe.TypeTensorElement(fe.FilterOperationType.NONE, [fe.DimElement(fe.FilterOperationType.EQ, 2),
                                                                  fe.DimElement(fe.FilterOperationType.EQ, 3)])
        var5 = fe.TypeTensorElement(fe.FilterOperationType.ALL, [fe.DimElement(fe.FilterOperationType.EQ, 2),
                                                                 fe.DimElement(fe.FilterOperationType.EQ, 3),
                                                                 fe.DimElement(fe.FilterOperationType.EQ, 6)])
        var6 = fe.TypeTensorElement(fe.FilterOperationType.ALL, [fe.DimElement(fe.FilterOperationType.GT, 2),
                                                                 fe.DimElement(fe.FilterOperationType.EQ, 3)])

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)
        self.assertNotEqual(var1, var6)
        self.assertNotEqual(var1, fe.TypeStringElement(fe.FilterOperationType.NONE))
        self.assertNotEqual(var1, 1)

    def test_data_getter(self):
        shape = [
            fe.LogicalElement(fe.FilterOperationType.AND, [
                fe.DimElement(fe.FilterOperationType.GE, 5),
                fe.DimElement(fe.FilterOperationType.LT, 10)
            ]),
            fe.DimElement(fe.FilterOperationType.GT, 6)
        ]
        var1 = fe.TypeTensorElement(fe.FilterOperationType.ALL, shape)
        self.assertEqual(var1.operation, fe.FilterOperationType.ALL)
        self.assertEqual(var1.dimensions, shape)


class TestTypeNamedValueCollectionElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.TypeNamedValueCollectionElement(fe.FilterOperationType.ALL,
                                                  {"key": fe.TypeStringElement(fe.FilterOperationType.NONE)})
        var2 = fe.TypeNamedValueCollectionElement(fe.FilterOperationType.ALL,
                                                  {"key": fe.TypeStringElement(fe.FilterOperationType.NONE)})
        var3 = fe.TypeNamedValueCollectionElement(fe.FilterOperationType.ALL,
                                                  {"key": fe.TypeIntElement(fe.FilterOperationType.NONE)})
        var4 = fe.TypeNamedValueCollectionElement(fe.FilterOperationType.ALL,
                                                  {"key1": fe.TypeStringElement(fe.FilterOperationType.NONE)})
        var5 = fe.TypeNamedValueCollectionElement(fe.FilterOperationType.NONE,
                                                  {"key": fe.TypeStringElement(fe.FilterOperationType.NONE)})
        var6 = fe.TypeNamedValueCollectionElement(fe.FilterOperationType.ALL,
                                                  {"key": fe.TypeStringElement(fe.FilterOperationType.NONE),
                                                   "key1": fe.TypeStringElement(fe.FilterOperationType.NONE)})

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)
        self.assertNotEqual(var1, var6)
        self.assertNotEqual(var1, fe.TypeTensorElement(fe.FilterOperationType.ALL,
                                                       [fe.DimElement(fe.FilterOperationType.GE, 2),
                                                        fe.DimElement(fe.FilterOperationType.GT, 2)]))
        self.assertNotEqual(var1, {"key": fe.TypeStringElement(fe.FilterOperationType.NONE)})

    def test_data_getters(self):
        data = {'value1': fe.TypeTensorElement(fe.FilterOperationType.ALL, [fe.DimElement(fe.FilterOperationType.GE, 5),
                                                                            fe.DimElement(fe.FilterOperationType.GT,
                                                                                          6)])}
        var1 = fe.TypeNamedValueCollectionElement(fe.FilterOperationType.ALL, data)
        self.assertEqual(var1.operation, fe.FilterOperationType.ALL)
        self.assertEqual(var1.elements, data)


class TestTypeListElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.TypeListElement(fe.FilterOperationType.ALL, fe.TypeStringElement(fe.FilterOperationType.NONE))
        var2 = fe.TypeListElement(fe.FilterOperationType.ALL, fe.TypeStringElement(fe.FilterOperationType.NONE))
        var3 = fe.TypeListElement(fe.FilterOperationType.ALL, fe.TypeIntElement(fe.FilterOperationType.NONE))
        var4 = fe.TypeListElement(fe.FilterOperationType.NONE, fe.TypeStringElement(fe.FilterOperationType.NONE))

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, fe.TypeStringElement(fe.FilterOperationType.NONE))
        self.assertNotEqual(var1, fe.TypeListElement(fe.FilterOperationType.ALL,
                                                     fe.TypeListElement(fe.FilterOperationType.ALL,
                                                                        fe.TypeStringElement(
                                                                            fe.FilterOperationType.NONE))))

    def test_data_getter(self):
        data = fe.TypeTensorElement(fe.FilterOperationType.ALL, [fe.DimElement(fe.FilterOperationType.GE, 2),
                                                                 fe.DimElement(fe.FilterOperationType.GE, 3)])
        var1 = fe.TypeListElement(fe.FilterOperationType.ALL, data)
        self.assertEqual(var1.operation, fe.FilterOperationType.ALL)
        self.assertEqual(var1.element_type_declaration, data)


class TestTypeTupleElement(unittest.TestCase):

    def test_eq(self):
        var1 = fe.TypeTupleElement(fe.FilterOperationType.ALL, [fe.TypeStringElement(fe.FilterOperationType.NONE),
                                                                fe.TypeIntElement(fe.FilterOperationType.NONE)])
        var2 = fe.TypeTupleElement(fe.FilterOperationType.ALL, [fe.TypeStringElement(fe.FilterOperationType.NONE),
                                                                fe.TypeIntElement(fe.FilterOperationType.NONE)])
        var3 = fe.TypeTupleElement(fe.FilterOperationType.ALL, [fe.TypeIntElement(fe.FilterOperationType.NONE)])
        var4 = fe.TypeTupleElement(fe.FilterOperationType.ALL, [fe.TypeIntElement(fe.FilterOperationType.NONE),
                                                                fe.TypeStringElement(fe.FilterOperationType.NONE)])
        var5 = fe.TypeTupleElement(fe.FilterOperationType.ALL, [fe.TypeStringElement(fe.FilterOperationType.NONE),
                                                                fe.TypeIntElement(fe.FilterOperationType.NONE),
                                                                fe.TypeFloatElement(fe.FilterOperationType.NONE)])
        var6 = fe.TypeTupleElement(fe.FilterOperationType.NONE, [fe.TypeStringElement(fe.FilterOperationType.NONE),
                                                                 fe.TypeIntElement(fe.FilterOperationType.NONE)])

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)
        self.assertNotEqual(var1, var6)
        self.assertNotEqual(var1, (fe.TypeStringElement(fe.FilterOperationType.NONE),))
        self.assertNotEqual(var1, fe.TypeListElement(fe.FilterOperationType.ALL,
                                                     fe.TypeStringElement(fe.FilterOperationType.NONE)))

    def test_data_getter(self):
        elements = [fe.TypeStringElement(fe.FilterOperationType.NONE), fe.TypeIntElement(fe.FilterOperationType.NONE)]
        var1 = fe.TypeTupleElement(fe.FilterOperationType.ALL, elements)
        self.assertEqual(var1.operation, fe.FilterOperationType.ALL)
        self.assertEqual(var1.elements, elements)


class TestNoneFilterOperationWorks(unittest.TestCase):

    def test_construction_and_conversion_successful(self):
        # StringElement
        element = fe.StringElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)
        self.assertEqual(element.value, None)

        # BoolElement
        element = fe.BoolElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)
        self.assertEqual(element.value, None)

        # IntElement
        element = fe.IntElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)
        self.assertEqual(element.value, None)

        # FloatElement
        element = fe.FloatElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)
        self.assertEqual(element.value, None)

        # DictElement
        element = fe.DictElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)
        self.assertEqual(element.elements, None)

        # ListElement
        element = fe.ListElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)
        self.assertEqual(element.elements, None)

        # TypeDeclarationElement
        element = fe.TypeDeclarationElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)
        self.assertEqual(element.type_declaration, None)

        # TagCollectionElement
        element = fe.TagCollectionElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)
        self.assertEqual(element.condensed_tags, None)

        # ... [similar blocks for TYPE_STRING, TYPE_INT, etc.]

        # TypeStringElement
        element = fe.TypeStringElement(fe.FilterOperationType.NONE)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)

        # TypeIntElement
        element = fe.TypeIntElement(fe.FilterOperationType.NONE)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)

        # TypeFloatElement
        element = fe.TypeFloatElement(fe.FilterOperationType.NONE)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)

        # TypeBoolElement
        element = fe.TypeBoolElement(fe.FilterOperationType.NONE)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)

        # TypeTensorElement
        element = fe.TypeTensorElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)
        self.assertEqual(element.dimensions, None)

        # TypeNamedValueCollectionElement
        element = fe.TypeNamedValueCollectionElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)
        self.assertEqual(element.elements, None)

        # TypeListElement
        element = fe.TypeListElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)
        self.assertEqual(element.element_type_declaration, None)

        # TypeTupleElement
        element = fe.TypeTupleElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)
        self.assertEqual(element.elements, None)

        # DimElement
        element = fe.DimElement(fe.FilterOperationType.NONE, None)
        self.assertEqual(element.operation, fe.FilterOperationType.NONE)
        self.assertEqual(element.size, None)


class TestIntegration(unittest.TestCase):

    def test_eq(self):
        var1 = fe.DictElement(fe.FilterOperationType.ALL, {
            'key1': fe.StringElement(fe.FilterOperationType.EQ, 'cute'),
            'key2': fe.ListElement(fe.FilterOperationType.ALL, [
                fe.DictElement(fe.FilterOperationType.ALL, {
                    'declaration': fe.TypeDeclarationElement(fe.FilterOperationType.TYPE_MATCH,
                                                             fe.TypeIntElement(fe.FilterOperationType.NONE)),
                    'data': fe.IntElement(fe.FilterOperationType.EQ, 1)
                })
            ])
        })

        var2 = fe.DictElement(fe.FilterOperationType.ALL, {
            'key1': fe.StringElement(fe.FilterOperationType.EQ, 'cute'),
            'key2': fe.ListElement(fe.FilterOperationType.ALL, [
                fe.DictElement(fe.FilterOperationType.ALL, {
                    'declaration': fe.TypeDeclarationElement(fe.FilterOperationType.TYPE_MATCH,
                                                             fe.TypeIntElement(fe.FilterOperationType.NONE)),
                    'data': fe.IntElement(fe.FilterOperationType.EQ, 1)
                })
            ])
        })

        var3 = fe.DictElement(fe.FilterOperationType.ALL, {
            'key1': fe.StringElement(fe.FilterOperationType.EQ, 'cute'),
            'key2': fe.ListElement(fe.FilterOperationType.ALL, [
                fe.DictElement(fe.FilterOperationType.ALL, {
                    'declaration': fe.TypeDeclarationElement(fe.FilterOperationType.TYPE_MATCH,
                                                             fe.TypeIntElement(fe.FilterOperationType.NONE)),
                    'data': fe.IntElement(fe.FilterOperationType.EQ, 2)
                })
            ])
        })

        var4 = fe.DictElement(fe.FilterOperationType.ALL, {
            'key1': fe.StringElement(fe.FilterOperationType.EQ, 'cute'),
            'key2': fe.TypeIntElement(fe.FilterOperationType.NONE)
        })

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)


if __name__ == '__main__':
    unittest.main()
