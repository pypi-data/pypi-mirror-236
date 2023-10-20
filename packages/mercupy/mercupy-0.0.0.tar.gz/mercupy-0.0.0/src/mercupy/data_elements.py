# Authored by GPT-4-backed ChatGPT and adapted by Trent Fellbootman
"""Data element definitions. Abstractions for data that will be passed to and received from model server processes."""

from abc import ABC, abstractmethod
from typing import List, Dict, Self
from typeguard import typechecked
import numpy as np
from enum import Enum, auto


class DataElementType(Enum):
    STRING = auto()
    BOOL = auto()
    INT = auto()
    FLOAT = auto()
    NAMED_VALUE_COLLECTION = auto()
    LIST = auto()
    TENSOR = auto()


class DataElement(ABC):

    @typechecked
    def __init__(self, element_type: DataElementType):
        self._element_type = element_type

    @property
    @typechecked
    def element_type(self) -> DataElementType:
        return self._element_type

    @abstractmethod
    def _eq(self, other: Self) -> bool:
        raise NotImplementedError()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, DataElement):
            return False
        
        if other._element_type != self._element_type:
            return False
        
        return self._eq(other)


class StringElement(DataElement):

    @typechecked
    def __init__(self, value: str):
        super().__init__(DataElementType.STRING)
        self._value = value

    @property
    @typechecked
    def value(self) -> str:
        return self._value

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._value == other._value


class BoolElement(DataElement):

    @typechecked
    def __init__(self, value: bool):
        super().__init__(DataElementType.BOOL)
        self._value = value

    @property
    @typechecked
    def value(self) -> bool:
        return self._value

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._value == other._value


class IntElement(DataElement):

    @typechecked
    def __init__(self, value: int):
        super().__init__(DataElementType.INT)
        self._value = value

    @property
    @typechecked
    def value(self) -> int:
        return self._value

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._value == other._value


class FloatElement(DataElement):

    @typechecked
    def __init__(self, value: float):
        super().__init__(DataElementType.FLOAT)
        self._value = value

    @property
    @typechecked
    def value(self) -> float:
        return self._value

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._value == other._value


class NamedValueCollectionElement(DataElement):

    @typechecked
    def __init__(self, data: Dict[str, DataElement]):
        super().__init__(DataElementType.NAMED_VALUE_COLLECTION)
        self._data = data

    @property
    @typechecked
    def data(self) -> Dict[str, DataElement]:
        return self._data

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._data == other._data


class ListElement(DataElement):

    @typechecked
    def __init__(self, data: List[DataElement]):
        super().__init__(DataElementType.LIST)
        self._data = data

    @property
    @typechecked
    def data(self) -> List[DataElement]:
        return self._data

    @typechecked
    def _eq(self, other: Self) -> bool:
        return self._data == other._data


class TensorElement(DataElement):

    @typechecked
    def __init__(self, data: np.ndarray):
        super().__init__(DataElementType.TENSOR)
        self._data = data

    @property
    @typechecked
    def data(self) -> np.ndarray:
        return self._data

    @typechecked
    def _eq(self, other: Self) -> bool:
        return np.array_equal(self._data, other._data)
