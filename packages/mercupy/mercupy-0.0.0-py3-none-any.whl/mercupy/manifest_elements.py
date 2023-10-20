from abc import ABC, abstractmethod
# TODO: change to better base classes; don't use deprecated ones
from typing import List, Dict, Self, Set, override
from enum import Enum, auto
from typeguard import typechecked

from .tags import TagTokenTree


class ManifestElementType(Enum):
    # Primitives
    STRING = auto()
    BOOL = auto()
    INT = auto()
    FLOAT = auto()

    # Compositors
    DICT = auto()
    LIST = auto()

    # Special
    TYPE_DECLARATION = auto()
    TAG_COLLECTION = auto()

    # Type declaration (primitive)
    TYPE_STRING = auto()
    TYPE_INT = auto()
    TYPE_FLOAT = auto()
    TYPE_BOOL = auto()
    TYPE_TENSOR = auto()

    # Type declaration (primitive)
    TYPE_NAMED_VALUE_COLLECTION = auto()
    TYPE_LIST = auto()
    TYPE_TUPLE = auto()


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


def _is_type_declaration_element(element_type: ManifestElementType) -> bool:
    return element_type in _type_declaration_elements


class ManifestElement(ABC):

    @typechecked
    def __init__(self, element_type: ManifestElementType):
        self._element_type = element_type

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, ManifestElement):
            return False

        if not self.element_type == other.element_type:
            return False

        return self._eq(other)

    @typechecked
    @abstractmethod
    def _eq(self, other: Self) -> bool:
        raise NotImplementedError()

    @property
    @typechecked
    def element_type(self) -> ManifestElementType:
        return self._element_type


class StringElement(ManifestElement):

    @typechecked
    def __init__(self, value: str):
        super().__init__(ManifestElementType.STRING)

        self._value = value

    @property
    @typechecked
    def value(self) -> str:
        return self._value

    @typechecked
    @override
    def _eq(self, other: Self) -> bool:
        return self._value == other._value


class BoolElement(ManifestElement):

    @typechecked
    def __init__(self, value: bool):
        super().__init__(ManifestElementType.BOOL)
        self._value = value

    @property
    @typechecked
    def value(self) -> bool:
        return self._value

    @typechecked
    @override
    def _eq(self, other: Self) -> bool:
        return self._value == other._value


class IntElement(ManifestElement):

    @typechecked
    def __init__(self, value: int):
        super().__init__(ManifestElementType.INT)
        self._value = value

    @property
    @typechecked
    def value(self) -> int:
        return self._value

    @typechecked
    @override
    def _eq(self, other: Self) -> bool:
        return self._value == other._value


class FloatElement(ManifestElement):

    @typechecked
    def __init__(self, value: float):
        super().__init__(ManifestElementType.FLOAT)
        self._value = value

    @property
    @typechecked
    def value(self) -> float:
        return self._value

    @typechecked
    @override
    def _eq(self, other: Self) -> bool:
        return self._value == other._value


class DictElement(ManifestElement):

    @typechecked
    def __init__(self, data: Dict[str, ManifestElement]):
        super().__init__(ManifestElementType.DICT)
        self._data = data

    @property
    @typechecked
    def data(self) -> Dict[str, ManifestElement]:
        return self._data

    @typechecked
    @override
    def _eq(self, other: Self) -> bool:
        if set(self._data.keys()) != set(other._data.keys()):
            return False

        return all(self._data[key] == other._data[key] for key in self._data.keys())


class ListElement(ManifestElement):

    @typechecked
    def __init__(self, data: List[ManifestElement]):
        super().__init__(ManifestElementType.LIST)
        self._data = data

    @property
    @typechecked
    def data(self) -> List[ManifestElement]:
        return self._data

    @typechecked
    @override
    def _eq(self, other: Self) -> bool:
        if len(self._data) != len(other._data):
            return False

        return all(item1 == item2 for item1, item2 in zip(self._data, other._data))


class TagCollectionElement(ManifestElement):

    @typechecked
    def __init__(self, tags: List[TagTokenTree]):
        super().__init__(ManifestElementType.TAG_COLLECTION)

        self._tags = tags

    @property
    @typechecked
    def tags(self) -> List[TagTokenTree]:
        return self._tags

    @typechecked
    @override
    def _eq(self, other: Self) -> bool:
        return all(tags_1 == tags_2 for tags_1, tags_2 in zip(self._tags, other._tags))


class TypeDeclarationElement(ManifestElement):

    @typechecked
    def __init__(self, type_declaration: ManifestElement):
        if not _is_type_declaration_element(type_declaration.element_type):
            raise Exception("Invalid type declaration!")

        super().__init__(ManifestElementType.TYPE_DECLARATION)

        self._type_declaration = type_declaration

    @property
    @typechecked
    def type_declaration(self) -> ManifestElement:
        return self._type_declaration

    @typechecked
    @override
    def _eq(self, other: Self) -> bool:
        return self._type_declaration == other._type_declaration


class _DataLessElement(ManifestElement, ABC):

    @staticmethod
    @typechecked
    @abstractmethod
    def _element_type() -> ManifestElementType:
        raise NotImplementedError()

    @typechecked
    def __init__(self):
        super().__init__(self._element_type())

    @typechecked
    @override
    def _eq(self, other: Self) -> bool:
        # should evaluate to true as long as the element types are the same, since there is no data
        return True


class TypeStringElement(_DataLessElement):

    @staticmethod
    def _element_type() -> ManifestElementType:
        return ManifestElementType.TYPE_STRING


class TypeIntElement(_DataLessElement):

    @staticmethod
    def _element_type() -> ManifestElementType:
        return ManifestElementType.TYPE_INT


class TypeFloatElement(_DataLessElement):

    @staticmethod
    def _element_type() -> ManifestElementType:
        return ManifestElementType.TYPE_FLOAT


class TypeBoolElement(_DataLessElement):

    @staticmethod
    def _element_type() -> ManifestElementType:
        return ManifestElementType.TYPE_BOOL


class TypeTensorElement(ManifestElement):

    @typechecked
    def __init__(self, shape: tuple[int, ...]):
        assert all(dim > 0 for dim in shape), "All dimensions must be positive!"

        super().__init__(ManifestElementType.TYPE_TENSOR)

        self._shape = shape

    @property
    @typechecked
    def shape(self) -> tuple[int, ...]:
        return self._shape

    @typechecked
    @override
    def _eq(self, other: Self) -> bool:
        return self._shape == other._shape


class TypeNamedValueCollectionElement(ManifestElement):

    @typechecked
    def __init__(self, data: Dict[str, ManifestElement]):

        assert all(_is_type_declaration_element(value.element_type) for value in data.values()), \
            "All values must be type declaration elements!"

        super().__init__(ManifestElementType.TYPE_NAMED_VALUE_COLLECTION)

        self._data = data

    @property
    @typechecked
    def data(self) -> Dict[str, ManifestElement]:
        return self._data

    @typechecked
    @override
    def _eq(self, other: Self) -> bool:
        if set(self._data.keys()) != set(other._data.keys()):
            return False

        return all(self._data[key] == other._data[key] for key in self._data.keys())


class TypeListElement(ManifestElement):

    @typechecked
    def __init__(self, element_type_declaration: ManifestElement):
        assert _is_type_declaration_element(element_type_declaration.element_type), \
            "Element type must be a type declaration element!"

        super().__init__(ManifestElementType.TYPE_LIST)

        self._element_type_declaration = element_type_declaration

    @property
    @typechecked
    def element_type_declaration(self) -> ManifestElement:
        return self._element_type_declaration

    @typechecked
    @override
    def _eq(self, other: Self) -> bool:
        return self._element_type_declaration == other._element_type_declaration


class TypeTupleElement(ManifestElement):

    @typechecked
    def __init__(self, element_type_declarations: tuple[ManifestElement, ...]):
        assert all(_is_type_declaration_element(element.element_type) for element in element_type_declarations), \
            "All tuple elements must be type declaration elements!"

        super().__init__(ManifestElementType.TYPE_TUPLE)

        self._element_type_declarations = element_type_declarations

    @property
    @typechecked
    def element_type_declarations(self) -> tuple[ManifestElement, ...]:
        return self._element_type_declarations

    @typechecked
    @override
    def _eq(self, other: Self) -> bool:
        if len(self._element_type_declarations) != len(other._element_type_declarations):
            return False

        return all(
            item1 == item2 for item1, item2 in zip(self._element_type_declarations, other._element_type_declarations))
