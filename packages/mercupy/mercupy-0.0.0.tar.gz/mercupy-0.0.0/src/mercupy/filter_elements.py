# TODO: check for argument validity in constructors & PyTree parsing methods?
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List, Dict, Self

from typeguard import typechecked

from .tags import TagTokenTree


class FilterElementType(Enum):
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

    # Filter only
    LOGICAL = auto()
    DIM = auto()


class FilterOperationType(Enum):
    # Universal
    ALL = auto()
    NONE = auto()

    # Numerical Comparisons
    EQ = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()

    # Type Declarations
    TYPE_MATCH = auto()

    # Logical Operations
    AND = auto()
    OR = auto()
    NOT = auto()

    # Tag Matching
    IMPLICIT_TAG_MATCH = auto()
    EXPLICIT_TAG_MATCH = auto()


class FilterElement(ABC):

    @typechecked
    def __init__(self, element_type: FilterElementType):
        self._element_type = element_type

    @abstractmethod
    def _eq(self, other: Self) -> bool:
        """
        Should evaluate to True if and only if both the operation type and data are the same.

        :param other:
        :return:
        """
        raise NotImplementedError()

    @typechecked
    def __eq__(self, other) -> bool:
        if not isinstance(other, FilterElement):
            return False

        if other._element_type != self._element_type:
            return False

        return self._eq(other)

    @property
    @typechecked
    def element_type(self) -> FilterElementType:
        return self._element_type


class StringElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, string: str | None):
        super().__init__(FilterElementType.STRING)

        self._operation = operation
        self._string = string

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @property
    @typechecked
    def value(self) -> str | None:
        return self._string

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._string == other._string


class BoolElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, value: bool | None):
        super().__init__(FilterElementType.BOOL)
        self._operation = operation
        self._value = value

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @property
    @typechecked
    def value(self) -> bool | None:
        return self._value

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._value == other._value


class IntElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, value: int | None):
        super().__init__(FilterElementType.INT)
        self._operation = operation
        self._value = value

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @property
    @typechecked
    def value(self) -> int | None:
        return self._value

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._value == other._value


class FloatElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, value: float | None):
        super().__init__(FilterElementType.FLOAT)
        self._operation = operation
        self._value = value

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @property
    @typechecked
    def value(self) -> float | None:
        return self._value

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._value == other._value


class ListElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, elements: List[FilterElement] | None):
        super().__init__(FilterElementType.LIST)
        self._operation = operation
        self._elements = elements

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @property
    @typechecked
    def elements(self) -> List[FilterElement] | None:
        return self._elements

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._elements == other._elements


class DictElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, elements: Dict[str, FilterElement] | None):
        super().__init__(FilterElementType.DICT)
        self._operation = operation
        self._elements = elements

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @property
    @typechecked
    def elements(self) -> Dict[str, FilterElement] | None:
        return self._elements

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._elements == other._elements


class TypeDeclarationElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, type_declaration: FilterElement | None):
        super().__init__(FilterElementType.TYPE_DECLARATION)
        self._operation = operation
        self._type_declaration = type_declaration

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @property
    @typechecked
    def type_declaration(self) -> FilterElement | None:
        return self._type_declaration

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._type_declaration == other._type_declaration


class TypeNamedValueCollectionElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, elements: Dict[str, FilterElement] | None):
        super().__init__(FilterElementType.TYPE_NAMED_VALUE_COLLECTION)
        self._operation = operation
        self._elements = elements

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @property
    @typechecked
    def elements(self) -> Dict[str, FilterElement] | None:
        return self._elements

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._elements == other._elements


class TypeListElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, element_type_declaration: FilterElement | None):
        super().__init__(FilterElementType.TYPE_LIST)
        self._operation = operation
        self._element_type_declaration = element_type_declaration

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @property
    @typechecked
    def element_type_declaration(self) -> FilterElement | None:
        return self._element_type_declaration

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._element_type_declaration == other._element_type_declaration


class TypeTupleElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, elements: List[FilterElement] | None):
        super().__init__(FilterElementType.TYPE_TUPLE)
        self._operation = operation
        self._elements = elements

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @property
    @typechecked
    def elements(self) -> List[FilterElement] | None:
        return self._elements

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._elements == other._elements


class DimElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, size: int | None):
        super().__init__(FilterElementType.DIM)

        self._operation = operation
        self._size = size

    @property
    @typechecked
    def size(self) -> int | None:
        return self._size

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._size == other._size

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation


class TypeTensorElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, dimensions: List[FilterElement] | None):
        super().__init__(FilterElementType.TYPE_TENSOR)
        self._operation = operation
        self._dimensions = dimensions

    @property
    @typechecked
    def dimensions(self) -> List[FilterElement] | None:
        return self._dimensions

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._dimensions == other._dimensions

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation


class TypeStringElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType):
        super().__init__(FilterElementType.TYPE_STRING)

        self._operation = operation

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation


class TypeBoolElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType):
        super().__init__(FilterElementType.TYPE_BOOL)

        self._operation = operation

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation


class TypeIntElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType):
        super().__init__(FilterElementType.TYPE_INT)

        self._operation = operation

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation


class TypeFloatElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType):
        super().__init__(FilterElementType.TYPE_FLOAT)

        self._operation = operation

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation


# "none" is not available on logical elements
class LogicalElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, predicates: List[FilterElement]):
        super().__init__(FilterElementType.LOGICAL)
        self._operation = operation
        self._predicates = predicates

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @property
    @typechecked
    def predicates(self) -> List[FilterElement]:
        return self._predicates

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._predicates == other._predicates


class TagCollectionElement(FilterElement):

    @typechecked
    def __init__(self, operation: FilterOperationType, condensed_tags: List[TagTokenTree] | None):
        super().__init__(FilterElementType.TAG_COLLECTION)
        self._operation = operation
        self._condensed_tags = condensed_tags

    @property
    @typechecked
    def operation(self) -> FilterOperationType:
        return self._operation

    @property
    @typechecked
    def condensed_tags(self) -> List[TagTokenTree] | None:
        return self._condensed_tags

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._operation == other._operation and self._condensed_tags == other._condensed_tags
