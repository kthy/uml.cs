# -*- coding: utf-8 -*-
"""Definition of UML entities."""

from abc import ABC, abstractmethod
from os import linesep
from re import match, sub

try:
    from features import Access, Field, MetaEntity, Method, Modifier
except (ImportError, ModuleNotFoundError):  # pragma: no cover
    from umldotcs.features import Access, Field, MetaEntity, Method, Modifier


ARROW = "=>"
CURLY = "{"


class UmlEntity(ABC):
    """An abstract UML entity."""

    def __init__(self, tokens, **kwargs):
        self.fields = []
        self.methods = []
        self.name = tokens[0]
        del tokens[0]

        self.namespace = kwargs.get("nsp", "No Namespace Defined")
        self.access = kwargs.get("access", Access.INTERNAL)
        self.attrs = kwargs.get("attrs", [])
        self.bgcolor = kwargs.get("bgcolor", "gray99")
        self.color = kwargs.get("color", "gray10")
        self.format_href(kwargs.get("repo_url", None))
        self.modifiers = kwargs.get("modifiers", [])

        self.implements = [t.strip(", ") for t in tokens[1:]] if tokens else []
        self.implements = [sub("<(.*)>$", r"&lt;\1&gt;", i) for i in self.implements]

    def __repr__(self):
        """A representation of the entity."""
        mods = " " * bool(self.modifiers) + " ".join([m.value for m in self.modifiers])
        typ = self.__class__.__name__[3:].lower()
        return f"{self.access.value}{mods} {typ} {self.name}"

    def __str__(self):
        """A string representation of the entity suitable for printing."""
        return self.to_dot().partition("\n")[0]

    @abstractmethod
    def display_name(self):
        """Return dot code for the display name of the object."""

    def format_href(self, url):
        """Format dot code for a link to the source repo."""
        if url is None:
            self.repo_link = ""
            return
        base_url = match(r"https?://([^/]+)", url).group(1)
        href = f'HREF="{url}/{self.namespace}/{self.name}.cs"'
        target = 'TARGET="_blank"'
        title = f'TITLE="{self.name}.cs @ {base_url}"'
        self.repo_link = " ".join([href, target, title])

    @staticmethod
    def parse_entity(tokens):
        """Parse tokens. Return entity and leftover tokens."""
        entity = MetaEntity(tokens[0])
        del tokens[0]
        return entity, tokens

    def parse_tokens(self, tokens, attrs):
        """Parse line for fields and methods."""
        try:
            access = Access(tokens[0])
            del tokens[0]
        except ValueError:
            return attrs
        modifiers, tokens = Modifier.parse_modifiers(tokens)
        return_type = tokens[0]
        if return_type.startswith(self.name + "("):
            return_type = "«Create»"
        else:
            del tokens[0]
        if CURLY in tokens:
            tokens = tokens[: tokens.index(CURLY)]
        elif ARROW in tokens:
            tokens = tokens[: tokens.index(ARROW)]
        signature = " ".join(tokens)
        if "(" in signature:
            self.methods.append(Method(attrs, access, modifiers, return_type, signature))
        else:
            self.fields.append(Field(attrs, access, modifiers, return_type, signature))
        return []

    def relations_to_dot(self):
        """Convert the objects relations to GraphViz/dot code."""
        rels = []
        for rel in self.implements:
            style = (
                "[arrowhead = empty, style = dotted]"
                if rel.startswith("I")
                else "[arrowhead = normal, style = solid]"
            )
            rels.append(f"    {self.name} -> {rel} {style}")
        return rels

    def to_dot(self):
        """Convert the object to GraphViz/dot code."""
        indent = " " * 16
        empty_row = f'{indent}    <TR><TD COLSPAN="2"></TD></TR>'
        dot = f"""    {self.name} [
        color = {self.color},
        label = <<TABLE {self.repo_link}BGCOLOR="{self.bgcolor}" BORDER="1" CELLBORDER="0" CELLSPACING="0">
                    <TR><TD PORT="name" COLSPAN="2">{self.display_name()}</TD></TR>\n"""
        if self.fields or self.methods:
            fields = linesep.join([f.to_dot() for f in self.fields]) or empty_row
            dot += f"{indent}    <HR/>\n{fields}\n"
            methods = linesep.join([m.to_dot() for m in self.methods]) or empty_row
            dot += f"{indent}    <HR/>\n{methods}\n"
        dot += f"""{indent}</TABLE>>\n    ]\n"""
        return dot


class UmlInterface(UmlEntity):
    """An interface."""

    def __init__(self, tokens, **kwargs):
        kwargs["bgcolor"] = "darkolivegreen1"
        kwargs["color"] = "darkolivegreen"
        super().__init__(tokens, **kwargs)

    def display_name(self):
        return f"«interface»<BR/>{self.name}"


class UmlClass(UmlEntity):
    """A class."""

    def display_name(self):
        dname = self.name
        if self.is_abstract():
            dname = f"<I>{dname}</I>"
        if self.is_static():
            dname = f"<U>{dname}</U>"
        return dname

    def is_abstract(self):
        """Return True if this Class is abstract."""
        return Modifier.ABSTRACT in self.modifiers

    def is_static(self):
        """Return True if this Class is abstract."""
        return Modifier.STATIC in self.modifiers


class UmlEnum(UmlEntity):
    """An enumeration."""

    def display_name(self):
        return f"«enumeration»<BR/><I>{self.name}</I>"


class UmlStruct(UmlClass):
    """A struct."""
