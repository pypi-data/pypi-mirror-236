from typing import List, Dict, Self, Union
from typeguard import typechecked
from dataclasses import dataclass
from enum import Enum, auto

_PyTree = Union[List, Dict, tuple, str, float, bool, int]


class TagNameComponent(Enum):
    CLOUD_DEPLOYED = auto()
    LOCALLY_DEPLOYED = auto()


class TagTokenType(Enum):
    NAMESPACE_OPERATOR = auto()
    CONCATENATION_OPERATOR = auto()
    COMPONENT_NAME = auto()
    COLLECTION = auto()


# TODO: add error handling?
@dataclass
class TagTokenTree:

    def __init__(self,
                 token_type: TagTokenType,
                 name_component: TagNameComponent | None = None,
                 children: List[Self] | None = None,
                 next_token: Self | None = None):
        self.token_type = token_type
        self.name_component = name_component
        self.children = children
        self.next_token = next_token

    def __eq__(self, other: Self):
        if not isinstance(other, TagTokenTree):
            return False

        return self.token_type == other.token_type and \
            self.name_component == other.name_component and \
            self.children == other.children and \
            self.next_token == other.next_token

    @typechecked
    def __mul__(self, other: Self | TagNameComponent) -> Self:
        if isinstance(other, TagTokenTree):
            return TagTokenTree(
                token_type=TagTokenType.COMPONENT_NAME,
                name_component=self.name_component,
                next_token=TagTokenTree(
                    token_type=TagTokenType.CONCATENATION_OPERATOR,
                    next_token=other
                )
            )
        elif isinstance(other, TagNameComponent):
            return TagTokenTree(
                token_type=TagTokenType.COMPONENT_NAME,
                name_component=self.name_component,
                next_token=TagTokenTree(
                    token_type=TagTokenType.CONCATENATION_OPERATOR,
                    next_token=TagTokenTree(token_type=TagTokenType.COMPONENT_NAME, name_component=other)
                )
            )
        else:
            raise ValueError('other must be of Self or component name enum type!')

    @typechecked
    def __truediv__(self, other: Self | TagNameComponent) -> Self:
        if isinstance(other, TagTokenTree):
            return TagTokenTree(
                token_type=TagTokenType.COMPONENT_NAME,
                name_component=self.name_component,
                next_token=TagTokenTree(
                    token_type=TagTokenType.NAMESPACE_OPERATOR,
                    next_token=other
                )
            )
        elif isinstance(other, TagNameComponent):
            return TagTokenTree(
                token_type=TagTokenType.COMPONENT_NAME,
                name_component=self.name_component,
                next_token=TagTokenTree(
                    token_type=TagTokenType.NAMESPACE_OPERATOR,
                    next_token=TagTokenTree(token_type=TagTokenType.COMPONENT_NAME, name_component=other)
                )
            )
        else:
            raise ValueError('other must be of Self or component name enum type!')

    @typechecked
    def __add__(self, other: Self | TagNameComponent):
        # '+' will always return a collection
        if isinstance(other, TagTokenTree):
            if self.token_type == TagTokenType.COLLECTION:
                if other.token_type == TagTokenType.COLLECTION:
                    # both are collections
                    children = self.children + other.children
                else:
                    # convert other to a collection
                    children = self.children + [other]
            else:
                if other.token_type == TagTokenType.COLLECTION:
                    children = [self] + other.children
                else:
                    children = [self, other]
        elif isinstance(other, TagNameComponent):
            if self.token_type == TagTokenType.COLLECTION:
                children = self.children + [TagTokenTree(
                    token_type=TagTokenType.COMPONENT_NAME,
                    name_component=other
                )]
            else:
                children = [self, TagTokenTree(
                    token_type=TagTokenType.COMPONENT_NAME,
                    name_component=other
                )]
        else:
            raise ValueError('other must be of Self or component name enum type!')

        return TagTokenTree(
            token_type=TagTokenType.COLLECTION,
            children=children
        )


def CondensedTags(name_component: TagNameComponent) -> TagTokenTree:
    return TagTokenTree(
        token_type=TagTokenType.COMPONENT_NAME,
        name_component=name_component
    )
