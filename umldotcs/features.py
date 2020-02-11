# -*- coding: utf-8 -*-
"""Definition of features for/on UML entities."""

from abc import ABC, abstractmethod
from enum import Enum


def attrs_to_dot(attrs):
    """Convert list of attributes to a dot string."""
    return "<BR/>".join([f"[{attr}]" for attr in attrs]) if attrs else ""


class Access(Enum):
    """A class, field or method access restriction keyword."""

    INTERNAL = "internal"
    PRIVATE = "private"
    PRIVATEPROTECTED = "private protected"
    PROTECTED = "protected"
    PROTECTEDINTERNAL = "protected internal"
    PUBLIC = "public"

    def __str__(self):
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

    def is_static(self):
        """Return True if this Field or Method is static."""
        return Modifier.STATIC in self.modifiers

    @abstractmethod
    def to_dot(self):
        """Convert the Field or Method to GraphViz/dot code."""


class Field(FieldOrMethod):
    """A property/field."""

    def __init__(self, attrs, access, modifiers, typ, name):
        self.type = typ
        self.name = name
        super().__init__(attrs, access, modifiers)

    def to_dot(self):
        """Convert the Field to GraphViz/dot code."""
        dot = "                    <TR><TD"
        if not self.attrs:
            dot += ' COLSPAN="2"'
        if self.is_static():
            dot += "><U"
        dot += f">{self.access}{self.name} : {self.type}"
        if self.is_static():
            dot += "</U>"
        if self.attrs:
            dot += '</TD><TD ALIGN="RIGHT">' + attrs_to_dot(self.attrs)
        dot += "</TD></TR>"
        return dot


class MetaEntity(Enum):
    """Entity type enumeration."""

    CLASS = "class"
    ENUM = "enum"
    INTERFACE = "interface"
    STRUCT = "struct"

    @classmethod
    def as_str_list(cls):
        """Return a list of all entity types as string values."""
        yield cls.CLASS.value
        yield cls.ENUM.value
        yield cls.INTERFACE.value
        yield cls.STRUCT.value


class Method(FieldOrMethod):
    """A method."""

    def __init__(self, attrs, access, modifiers, return_type, signature):
        self.return_type = return_type
        # TODO: replace actual type(s) with T (, U, V, etc.)
        self.signature = signature.replace("<", "&lt;").replace(">", "&gt;")
        super().__init__(attrs, access, modifiers)

    def is_abstract(self):
        """Return True if this Method is abstract."""
        return Modifier.ABSTRACT in self.modifiers

    def to_dot(self):
        """Convert the Field to GraphViz/dot code."""
        dot = "                    <TR><TD"
        if not self.attrs:
            dot += ' COLSPAN="2"'
        # TODO: proper wrapping -- static, etc. wrap =
        if self.is_static():
            dot += "><U"
        dot += f">{self.access}{self.signature} : {self.return_type}"
        if self.attrs:
            dot += '</TD><TD ALIGN="RIGHT">' + attrs_to_dot(self.attrs)
        if self.is_static():
            dot += "</U>"
        dot += "</TD></TR>"
        return dot


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
