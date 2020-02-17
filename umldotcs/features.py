# -*- coding: utf-8 -*-
"""Definition of features for/on UML entities."""

from abc import ABC, abstractmethod
from enum import Enum, unique
from functools import total_ordering

from umldotcs.helpers import attrs_to_dot, encode_generics


@total_ordering
@unique
class Access(Enum):
    """A class, field or method access restriction keyword."""

    INTERNAL = "internal"
    PRIVATE = "private"
    PRIVATEPROTECTED = "private protected"
    PROTECTED = "protected"
    PROTECTEDINTERNAL = "protected internal"
    PUBLIC = "public"

    def __lt__(self, other):
        if other is None:
            return False
        if not isinstance(other, Access):
            return False
        values = {
            "private": 0,
            "private protected": 1,
            "internal": 2,
            "protected internal": 3,
            "protected": 4,
            "public": 5,
        }
        return values[self.value] < values[other.value]

    def __repr__(self):
        return f'Access("{self.value}")'

    def to_dot(self):
        """Convert the Access value to GraphViz/dot code."""
        return {
            self.INTERNAL: "~",
            self.PRIVATE: "-",
            self.PRIVATEPROTECTED: "-#",
            self.PROTECTED: "#",
            self.PROTECTEDINTERNAL: "#~",
            self.PUBLIC: "+",
        }[self]

    @staticmethod
    def parse_access(tokens):
        """Parse tokens. Return access level and leftover tokens."""
        try:
            access = Access(tokens[0])
            del tokens[0]
        except ValueError:
            access = Access.INTERNAL
        try:
            if access == Access.PRIVATE and Access(tokens[0]) == Access.PROTECTED:
                access = Access.PRIVATEPROTECTED
                del tokens[0]
            elif access == Access.PROTECTED and Access(tokens[0]) == Access.INTERNAL:
                access = Access.PROTECTEDINTERNAL
                del tokens[0]
        except ValueError:
            pass
        return access, tokens


class FieldOrMethod(ABC):
    """An abstract Field or Method."""

    def __init__(self, attrs, access, modifiers):
        self.attrs = attrs
        self.access = access
        self.modifiers = modifiers or []

    def __eq__(self, other):
        return all(
            [
                self.attrs == other.attrs,
                self.access == other.access,
                self.modifiers == other.modifiers,
            ]
        )

    def __hash__(self):
        return hash(repr(self))

    def is_static(self):
        """Return True if this Field or Method is static."""
        return Modifier.STATIC in self.modifiers

    @abstractmethod
    def to_dot(self):
        """Convert the Field or Method to GraphViz/dot code."""


@total_ordering
class Field(FieldOrMethod):
    """A property/field."""

    def __init__(self, attrs, access, modifiers, typ, name):
        self.type = encode_generics(typ)
        self.name = encode_generics(name)
        super().__init__(attrs, access, modifiers)

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Field):
            return False
        return all([super().__eq__(other), self.type == other.type, self.name == other.name])

    def __lt__(self, other):
        if other is None:
            return False
        if not isinstance(other, Field):
            return False
        return (self.access, self.name) < (other.access, other.name)

    def __repr__(self):
        return f'Field({self.attrs}, {self.access}, {self.modifiers}, "{self.type}", "{self.name}")'

    def to_dot(self):
        """Convert the Field to GraphViz/dot code."""
        dot = '                    <TR><TD ALIGN="LEFT"'
        if not self.attrs:
            dot += ' COLSPAN="2"'
        if self.is_static():
            dot += "><U"
        dot += f">{self.access.to_dot()}{self.name} : {self.type}"
        if self.is_static():
            dot += "</U>"
        if self.attrs:
            dot += '</TD><TD ALIGN="RIGHT">' + attrs_to_dot(self.attrs)
        dot += "</TD></TR>"
        return dot


@unique
class MetaEntity(Enum):
    """Entity type enumeration."""

    CLASS = "class"
    ENUM = "enum"
    INTERFACE = "interface"
    STRUCT = "struct"

    def __repr__(self):
        return f'MetaEntity("{self.value}")'

    @classmethod
    def as_str_list(cls):
        """Return a list of all entity types as string values."""
        yield cls.CLASS.value
        yield cls.ENUM.value
        yield cls.INTERFACE.value
        yield cls.STRUCT.value


@total_ordering
class Method(FieldOrMethod):
    """A method."""

    def __init__(self, attrs, access, modifiers, return_type, signature):
        self.return_type = encode_generics(return_type)
        self.signature = encode_generics(signature)
        super().__init__(attrs, access, modifiers)

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, Method):
            return False
        return all(
            [
                super().__eq__(other),
                self.return_type == other.return_type,
                self.signature == other.signature,
            ]
        )

    def __lt__(self, other):
        if other is None:
            return False
        if not isinstance(other, Method):
            return False
        return (self.access, self.signature) < (other.access, other.signature)

    def __repr__(self):
        return f'Method({self.attrs}, {self.access}, {self.modifiers}, "{self.return_type}", "{self.signature}")'

    def is_abstract(self):
        """Return True if this Method is abstract."""
        return Modifier.ABSTRACT in self.modifiers

    def to_dot(self):
        """Convert the Method to GraphViz/dot code."""
        dot = '                    <TR><TD ALIGN="LEFT"'
        if not self.attrs:
            dot += ' COLSPAN="2"'
        # TODO: proper wrapping -- static, etc. wrap =
        if self.is_static():
            dot += "><U"
        dot += f">{self.access.to_dot()}{self.signature}"
        if self.return_type:
            dot += f" : {self.return_type}"
        if self.attrs:
            dot += '</TD><TD ALIGN="RIGHT">' + attrs_to_dot(self.attrs)
        if self.is_static():
            dot += "</U>"
        dot += "</TD></TR>"
        return dot


@unique
class Modifier(Enum):
    """A class, field or method modifier."""

    ABSTRACT = "abstract"
    CONST = "const"
    EXTERN = "extern"
    NEW = "new"
    OVERRIDE = "override"
    PARTIAL = "partial"
    READONLY = "readonly"
    SEALED = "sealed"
    STATIC = "static"
    UNSAFE = "unsafe"
    VIRTUAL = "virtual"
    VOLATILE = "volatile"

    def __repr__(self):
        return f'Modifier("{self.value}")'

    @staticmethod
    def class_modifiers():
        """Return a list of the modifiers applicable for classes."""
        yield Modifier.ABSTRACT
        yield Modifier.NEW
        yield Modifier.PARTIAL
        yield Modifier.SEALED
        yield Modifier.STATIC

    @staticmethod
    def parse_modifiers(tokens):
        """Parse tokens. Return modifiers and leftover tokens."""
        modifiers = []
        while True:
            try:
                # TODO: proper support for partial (urgh!)
                modifiers.append(Modifier(tokens[0]))
                del tokens[0]
            except ValueError:
                break
        return modifiers, tokens
