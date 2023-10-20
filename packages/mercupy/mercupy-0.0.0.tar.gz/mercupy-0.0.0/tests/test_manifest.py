# boilerplate
import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().resolve().parent.parent))

from src.mercupy import manifest_elements as ma
from src.mercupy import tags


class TestManifestElement(unittest.TestCase):

    def test_eq(self):
        var1 = ma.DictElement({
            'a': ma.IntElement(1),
            'b': ma.ListElement([
                ma.DictElement({
                    'c': ma.StringElement('cute')
                })
            ])
        })

        var2 = ma.DictElement({
            'a': ma.IntElement(1),
            'b': ma.ListElement([
                ma.DictElement({
                    'c': ma.StringElement('cute')
                })
            ])
        })

        var3 = ma.DictElement({
            'a': ma.IntElement(1),
            'b': ma.ListElement([
                ma.DictElement({
                    'c': ma.StringElement('cuta')
                })
            ])
        })

        var4 = ma.StringElement('cute')

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, 'a')
        self.assertNotEqual(var1, var4)


class TestStringElement(unittest.TestCase):

    def test_eq(self):
        var1 = ma.StringElement('test')
        var2 = ma.StringElement('test')
        var3 = ma.StringElement('tester')
        var4 = ma.IntElement(1)
        var5 = 'a'

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)

    def test_invalid_argument(self):
        with self.assertRaises(Exception):
            ma.StringElement(1)

    def test_data_getter(self):
        var1 = ma.StringElement('test')
        self.assertEqual(var1.value, 'test')


class TestBoolElement(unittest.TestCase):

    def test_eq(self):
        var1 = ma.BoolElement(True)
        var2 = ma.BoolElement(True)
        var3 = ma.BoolElement(False)
        var4 = ma.IntElement(1)
        var5 = 'a'

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)

    def test_invalid_argument(self):
        with self.assertRaises(Exception):
            ma.BoolElement(1)

    def test_data_getter(self):
        var1 = ma.BoolElement(True)
        self.assertEqual(var1.value, True)


class TestIntElement(unittest.TestCase):

    def test_eq(self):
        var1 = ma.IntElement(5)
        var2 = ma.IntElement(5)
        var3 = ma.IntElement(7)
        var4 = ma.FloatElement(5.0)
        var5 = '5'

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)

    def test_invalid_argument(self):
        with self.assertRaises(Exception):
            ma.IntElement(5.0)

    def test_data_getter(self):
        var1 = ma.IntElement(5)
        self.assertEqual(var1.value, 5)


class TestFloatElement(unittest.TestCase):

    def test_eq(self):
        var1 = ma.FloatElement(5.5)
        var2 = ma.FloatElement(5.5)
        var3 = ma.FloatElement(7.5)
        var4 = ma.IntElement(5)
        var5 = '5.5'

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)

    def test_data_getter(self):
        var1 = ma.FloatElement(5.5)
        self.assertEqual(var1.value, 5.5)

    def test_invalid_argument(self):
        with self.assertRaises(Exception):
            ma.FloatElement('a')


class TestDictElement(unittest.TestCase):

    def test_eq(self):
        var1 = ma.DictElement({
            'a': ma.StringElement('test'),
            'b': ma.IntElement(1)
        })

        var2 = ma.DictElement({
            'a': ma.StringElement('test'),
            'b': ma.IntElement(1)
        })

        var3 = ma.DictElement({
            'a': ma.StringElement('test'),
            'b': ma.IntElement(2)
        })

        var4 = ma.DictElement({
            'a': ma.StringElement('test'),
            'b': ma.FloatElement(1)
        })

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, 'test')

    def test_data_getter(self):
        data = {'a': ma.StringElement('test')}
        var1 = ma.DictElement(data)
        self.assertEqual(var1.data, data)

    def test_invalid_arguments(self):
        with self.assertRaises(Exception):
            ma.DictElement(1)


class TestListElement(unittest.TestCase):

    def test_eq(self):
        var1 = ma.ListElement([
            ma.StringElement('test1'),
            ma.IntElement(1)
        ])

        var2 = ma.ListElement([
            ma.StringElement('test1'),
            ma.IntElement(1)
        ])

        var3 = ma.ListElement([
            ma.StringElement('test1'),
            ma.IntElement(2)
        ])

        var4 = ma.ListElement([
            ma.StringElement('test1'),
            ma.FloatElement(1.0)
        ])

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, ['test1', 1])

    def test_data_getter(self):
        data = [ma.StringElement('test1')]
        var1 = ma.ListElement(data)
        self.assertEqual(var1.data, data)

    def test_invalid_arguments(self):
        with self.assertRaises(Exception):
            ma.ListElement('test1')


class TestTagCollectionElement(unittest.TestCase):

    def test_eq(self):
        var1 = ma.TagCollectionElement([
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) + tags.TagNameComponent.LOCALLY_DEPLOYED
            ),
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.LOCALLY_DEPLOYED) + tags.TagNameComponent.CLOUD_DEPLOYED
            )
        ])

        var2 = ma.TagCollectionElement([
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) + tags.TagNameComponent.LOCALLY_DEPLOYED
            ),
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.LOCALLY_DEPLOYED) + tags.TagNameComponent.CLOUD_DEPLOYED
            )
        ])

        var3 = ma.TagCollectionElement([
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) + tags.TagNameComponent.LOCALLY_DEPLOYED
            ),
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) + tags.TagNameComponent.LOCALLY_DEPLOYED
            )
        ])

        var4 = ma.StringElement('test')

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)

    def test_data_getter(self):
        data = [
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) + tags.TagNameComponent.LOCALLY_DEPLOYED
            ),
            tags.CondensedTags(tags.TagNameComponent.CLOUD_DEPLOYED) / (
                    tags.CondensedTags(tags.TagNameComponent.LOCALLY_DEPLOYED) + tags.TagNameComponent.CLOUD_DEPLOYED
            )
        ]

        retrieved = ma.TagCollectionElement(data).tags

        self.assertEqual(data[0], retrieved[0])
        self.assertEqual(data[1], retrieved[1])

    def test_invalid_arguments(self):
        with self.assertRaises(Exception):
            ma.TagCollectionElement('test1')


class TestTypeDeclarationElement(unittest.TestCase):

    def test_eq(self):
        var1 = ma.TypeDeclarationElement(ma.TypeStringElement())

        var2 = ma.TypeDeclarationElement(ma.TypeStringElement())

        var3 = ma.TypeDeclarationElement(ma.TypeFloatElement())

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, ['test1', 1])

    def test_data_getter(self):
        data = ma.TypeStringElement()
        var1 = ma.TypeDeclarationElement(data)
        self.assertEqual(var1.type_declaration, data)

    def test_invalid_arguments(self):
        with self.assertRaises(Exception):
            ma.TypeDeclarationElement(ma.StringElement('test'))


class TestTypeStringElement(unittest.TestCase):

    def test_eq(self):
        var1 = ma.TypeStringElement()
        var2 = ma.TypeStringElement()
        var3 = ma.TypeFloatElement()

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, ['test1', 1])

    def test_invalid_arguments(self):
        with self.assertRaises(Exception):
            ma.TypeStringElement('test')


class TestTypeBoolElement(unittest.TestCase):

    def test_eq(self):
        var1 = ma.TypeBoolElement()
        var2 = ma.TypeBoolElement()
        var3 = ma.TypeIntElement()

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, ['test2', 2])

    def test_invalid_arguments(self):
        with self.assertRaises(Exception):
            ma.TypeBoolElement('test')


class TestTypeIntElement(unittest.TestCase):

    def test_eq(self):
        var1 = ma.TypeIntElement()
        var2 = ma.TypeIntElement()
        var3 = ma.TypeFloatElement()

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, ['test3', 3])

    def test_invalid_arguments(self):
        with self.assertRaises(Exception):
            ma.TypeIntElement(1)


class TestTypeFloatElement(unittest.TestCase):

    def test_eq(self):
        var1 = ma.TypeFloatElement()
        var2 = ma.TypeFloatElement()
        var3 = ma.TypeBoolElement()

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, ['test4', 4])

    def test_invalid_arguments(self):
        with self.assertRaises(Exception):
            ma.TypeFloatElement(1.0)


class TestTypeTensorElement(unittest.TestCase):

    def test_creation(self):
        valid_shapes = [
            (1,),
            (2, 3),
            (3, 3, 3)
        ]

        for shape in valid_shapes:
            tensor_elem = ma.TypeTensorElement(shape)
            self.assertEqual(tensor_elem.shape, shape)

    def test_eq(self):
        var1 = ma.TypeTensorElement((2, 3))
        var2 = ma.TypeTensorElement((2, 3))
        var3 = ma.TypeTensorElement((3, 2))

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, ma.TypeStringElement())
        self.assertNotEqual(var1, 1)

    def test_invalid_shapes(self):
        invalid_shapes = [
            (-1,),
            (2, -3),
            (0, 3),
        ]

        for shape in invalid_shapes:
            with self.assertRaises(Exception):
                ma.TypeTensorElement(shape)

        with self.assertRaises(Exception):
            ma.TypeTensorElement('cute')

        with self.assertRaises(Exception):
            ma.TypeTensorElement([1, 2, 3])


class TestTypeNamedValueCollectionElement(unittest.TestCase):

    def test_creation(self):
        valid_data = [
            {},
            {"value1": ma.TypeStringElement()},
            {
                "value4": ma.TypeNamedValueCollectionElement({"inner": ma.TypeStringElement()}),
                "value5": ma.TypeFloatElement()
            },
            {"value2": ma.TypeIntElement(), "value3": ma.TypeFloatElement()}
        ]

        for data in valid_data:
            collection_elem = ma.TypeNamedValueCollectionElement(data)
            self.assertEqual(collection_elem.data, data)

    def test_eq(self):
        var1 = ma.TypeNamedValueCollectionElement({"key": ma.TypeStringElement()})
        var2 = ma.TypeNamedValueCollectionElement({"key": ma.TypeStringElement()})
        var3 = ma.TypeNamedValueCollectionElement({"key": ma.TypeIntElement()})

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, ma.TypeTensorElement((2, 2)))
        self.assertNotEqual(var1, {"key": ma.TypeStringElement()})

    def test_invalid_data(self):
        invalid_data = [
            {"value1": 1},
            {"value2": "string"},
            {"value3": [1, 2, 3]},
            {'value5': ma.StringElement('cute')}
        ]

        for data in invalid_data:
            with self.assertRaises(Exception):
                ma.TypeNamedValueCollectionElement(data)


class TestTypeListElement(unittest.TestCase):

    def test_creation(self):
        valid_type_declarations = [
            ma.TypeStringElement(),
            ma.TypeTensorElement((2, 3)),
            ma.TypeNamedValueCollectionElement({"value": ma.TypeStringElement()}),
            ma.TypeListElement(ma.TypeFloatElement())
        ]

        for type_declaration in valid_type_declarations:
            list_elem = ma.TypeListElement(type_declaration)
            self.assertEqual(list_elem.element_type_declaration, type_declaration)

    def test_eq(self):
        var1 = ma.TypeListElement(ma.TypeStringElement())
        var2 = ma.TypeListElement(ma.TypeStringElement())
        var3 = ma.TypeListElement(ma.TypeIntElement())

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, ma.TypeStringElement())
        self.assertNotEqual(var1, ma.TypeListElement(ma.TypeListElement(ma.TypeStringElement())))

    def test_invalid_data(self):
        invalid_type_declarations = [
            1,
            "string",
            [1, 2, 3],
            ma.StringElement('cute')
        ]

        for type_declaration in invalid_type_declarations:
            with self.assertRaises(Exception):
                ma.TypeListElement(type_declaration)


class TestTypeTupleElement(unittest.TestCase):

    def test_creation(self):
        valid_type_declarations = [
            (),
            (ma.TypeStringElement(),),
            (ma.TypeIntElement(), ma.TypeStringElement()),
            (ma.TypeFloatElement(), ma.TypeTensorElement((2, 2)), ma.TypeStringElement())
        ]

        for type_declaration in valid_type_declarations:
            tuple_elem = ma.TypeTupleElement(type_declaration)
            self.assertEqual(tuple_elem.element_type_declarations, type_declaration)

    def test_eq(self):
        var1 = ma.TypeTupleElement((ma.TypeStringElement(), ma.TypeIntElement()))
        var2 = ma.TypeTupleElement((ma.TypeStringElement(), ma.TypeIntElement()))
        var3 = ma.TypeTupleElement((ma.TypeIntElement(),))
        var4 = ma.TypeTupleElement((ma.TypeIntElement(), ma.TypeStringElement()))
        var5 = ma.TypeTupleElement((ma.TypeStringElement(), ma.TypeIntElement(), ma.TypeFloatElement()))

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)
        self.assertNotEqual(var1, (ma.TypeStringElement(),))
        self.assertNotEqual(var1, ma.TypeListElement(ma.TypeStringElement()))

    def test_invalid_data(self):
        invalid_type_declarations = [
            (1,),
            ("string",),
            ([1, 2, 3],),
            (ma.StringElement('cute'),),
            (ma.TypeStringElement(), 1),
            [ma.TypeStringElement()],
            (ma.TypeStringElement(), ma.StringElement('hello'))
        ]

        for type_declaration in invalid_type_declarations:
            with self.assertRaises(Exception):
                ma.TypeTupleElement(type_declaration)


class TestIntegration(unittest.TestCase):

    def test_eq(self):
        var1 = ma.DictElement({
            'key1': ma.StringElement('cute'),
            'key2': ma.ListElement([
                ma.DictElement({
                    'declaration': ma.TypeDeclarationElement(ma.TypeIntElement()),
                    'data': ma.IntElement(1)
                })
            ])
        })

        var2 = ma.DictElement({
            'key1': ma.StringElement('cute'),
            'key2': ma.ListElement([
                ma.DictElement({
                    'declaration': ma.TypeDeclarationElement(ma.TypeIntElement()),
                    'data': ma.IntElement(1)
                })
            ])
        })

        var3 = ma.DictElement({
            'key1': ma.StringElement('cute'),
            'key2': ma.ListElement([
                ma.DictElement({
                    'declaration': ma.TypeDeclarationElement(ma.TypeIntElement()),
                    'data': ma.IntElement(2)
                })
            ])
        })

        var4 = ma.DictElement({
            'key1': ma.StringElement('cute'),
            'key2': ma.TypeIntElement()
        })

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)


if __name__ == '__main__':
    unittest.main()
