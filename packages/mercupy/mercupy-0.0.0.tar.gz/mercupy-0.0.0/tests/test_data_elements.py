# Authored by GPT-4-backed ChatGPT and adapted by Trent Fellbootman
import unittest
import numpy as np

# boilerplate
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().resolve().parent.parent))

import src.mercupy.data_elements as da


class TestStringElement(unittest.TestCase):

    def test_eq(self):
        var1 = da.StringElement("sample")
        var2 = da.StringElement("sample")
        var3 = da.StringElement("different")
        var4 = da.FloatElement(True)

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, "sample")

    def test_invalid_argument(self):
        with self.assertRaises(Exception):
            da.StringElement(123)

    def test_data_getter(self):
        var1 = da.StringElement("sample")
        self.assertEqual(var1.element_type, da.DataElementType.STRING)
        self.assertEqual(var1.value, "sample")


class TestBoolElement(unittest.TestCase):

    def test_eq(self):
        var1 = da.BoolElement(True)
        var2 = da.BoolElement(True)
        var3 = da.BoolElement(False)
        var4 = da.StringElement('test')

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, da.StringElement('True'))
        self.assertNotEqual(var1, 1)

    def test_invalid_argument(self):
        with self.assertRaises(Exception):
            da.BoolElement('True')

    def test_data_getter(self):
        var1 = da.BoolElement(True)
        self.assertEqual(var1.element_type, da.DataElementType.BOOL)
        self.assertEqual(var1.value, True)


class TestIntElement(unittest.TestCase):

    def test_eq(self):
        var1 = da.IntElement(10)
        var2 = da.IntElement(10)
        var3 = da.IntElement(15)
        var4 = da.StringElement('test')

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, da.StringElement('10'))
        self.assertNotEqual(var1, '10')

    def test_invalid_argument(self):
        with self.assertRaises(Exception):
            da.IntElement('10')

    def test_data_getter(self):
        var1 = da.IntElement(10)
        self.assertEqual(var1.element_type, da.DataElementType.INT)
        self.assertEqual(var1.value, 10)


class TestFloatElement(unittest.TestCase):

    def test_eq(self):
        var1 = da.FloatElement(10.5)
        var2 = da.FloatElement(10.5)
        var3 = da.FloatElement(15.5)
        var4 = da.StringElement('test')

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, da.StringElement('10.5'))
        self.assertNotEqual(var1, '10.5')

    def test_invalid_argument(self):
        with self.assertRaises(Exception):
            da.FloatElement('10.5')

    def test_data_getter(self):
        var1 = da.FloatElement(10.5)
        self.assertEqual(var1.element_type, da.DataElementType.FLOAT)
        self.assertEqual(var1.value, 10.5)


class TestListElement(unittest.TestCase):

    def test_eq(self):
        var1 = da.ListElement([da.IntElement(1), da.StringElement("two")])
        var2 = da.ListElement([da.IntElement(1), da.StringElement("two")])
        var3 = da.ListElement([da.IntElement(1)])
        var4 = da.FloatElement(1.0)

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, [da.IntElement(1), da.StringElement("two")])

    def test_invalid_argument(self):
        with self.assertRaises(Exception):
            da.ListElement([1, "two"])

    def test_data_getter(self):
        var1 = da.ListElement([da.IntElement(1), da.StringElement("two")])
        self.assertEqual(var1.element_type, da.DataElementType.LIST)
        self.assertEqual(var1.data, [da.IntElement(1), da.StringElement("two")])


class TestNamedValueCollectionElement(unittest.TestCase):

    def test_eq(self):
        var1 = da.NamedValueCollectionElement({'a': da.IntElement(1), 'b': da.StringElement("two")})
        var2 = da.NamedValueCollectionElement({'a': da.IntElement(1), 'b': da.StringElement("two")})
        var3 = da.NamedValueCollectionElement({'a': da.IntElement(1)})
        var4 = da.FloatElement(1.0)

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, {'a': da.IntElement(1), 'b': da.StringElement("two")})

    def test_invalid_argument(self):
        with self.assertRaises(Exception):
            da.NamedValueCollectionElement({'a': 1, 'b': "two"})

    def test_data_getter(self):
        var1 = da.NamedValueCollectionElement({'a': da.IntElement(1), 'b': da.StringElement("two")})
        self.assertEqual(var1.element_type, da.DataElementType.NAMED_VALUE_COLLECTION)
        self.assertEqual(var1.data, {'a': da.IntElement(1), 'b': da.StringElement("two")})


class TestTensorElement(unittest.TestCase):

    def test_eq(self):
        np_arr = np.array([1, 2, 3])
        var1 = da.TensorElement(np_arr)
        var2 = da.TensorElement(np_arr.copy())
        var3 = da.TensorElement(np.array([1, 2, 4]))
        var4 = da.FloatElement(1.0)
        var5 = da.TensorElement(np.array([[1, 2, 3], [4, 5, 6]]))

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)
        self.assertNotEqual(var1, np_arr)

    def test_invalid_argument(self):
        with self.assertRaises(Exception):
            da.TensorElement([1, 2, 3])

    def test_data_getter(self):
        np_arr = np.array([1, 2, 3])
        var1 = da.TensorElement(np_arr)
        self.assertEqual(var1.element_type, da.DataElementType.TENSOR)
        self.assertTrue(np.array_equal(var1.data, np_arr))


class TestDataIntegration(unittest.TestCase):

    def test_eq(self):
        var1 = da.NamedValueCollectionElement({
            'key1': da.StringElement('cute'),
            'key2': da.ListElement([
                da.NamedValueCollectionElement({
                    'tensor': da.TensorElement(np.array([1, 2, 3])),
                    'status': da.BoolElement(True)
                })
            ])
        })

        var2 = da.NamedValueCollectionElement({
            'key1': da.StringElement('cute'),
            'key2': da.ListElement([
                da.NamedValueCollectionElement({
                    'tensor': da.TensorElement(np.array([1, 2, 3])),
                    'status': da.BoolElement(True)
                })
            ])
        })

        var3 = da.NamedValueCollectionElement({
            'key1': da.StringElement('cute'),
            'key2': da.ListElement([
                da.NamedValueCollectionElement({
                    'tensor': da.TensorElement(np.array([1, 2, 3])),
                    'status': da.BoolElement(False)
                })
            ])
        })

        var4 = da.NamedValueCollectionElement({
            'key1': da.StringElement('cute'),
            'key2': da.FloatElement(3.14)
        })

        var5 = da.NamedValueCollectionElement({
            'key1': da.StringElement('cute'),
            'key2': da.ListElement([
                da.NamedValueCollectionElement({
                    'tensor': da.TensorElement(np.array([[1, 2, 3]])),
                    'status': da.BoolElement(True)
                })
            ])
        })

        self.assertEqual(var1, var2)
        self.assertNotEqual(var1, var3)
        self.assertNotEqual(var1, var4)
        self.assertNotEqual(var1, var5)


if __name__ == '__main__':
    unittest.main()
