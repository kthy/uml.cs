# -*- coding: utf-8 -*-
"""Definition of UML entities."""

from abc import ABC, abstractmethod
from os import linesep
from re import match, sub

from umldotcs.features import Access, Field, MetaEntity, Method, Modifier
from umldotcs.helpers import clean_generics

ARROW = "=>"
CURLY = "{"

EXTENDS = "[arrowhead = normal, style = solid]"
IMPLEMENTS = "[arrowhead = empty, style = dotted]"
AGGREGATES = "[arrowhead = odiamond, style = solid]"
COMPOSITES = "[arrowhead = diamond, style = solid]"
HAS_A = "[arrowhead = vee, style = solid]"
# TODO: autodetection of aggregation, composition, uses


class UmlEntity(ABC):
    """An abstract UML entity."""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, tokens, **kwargs):
        self.__tokens = tokens.copy()
        self.__kwargs = kwargs
        self.fields = []
        self.methods = []
        self.name = tokens[0].replace("<", "_").replace(">", "_")
        del tokens[0]

        self.namespace = kwargs.get("nsp", "No Namespace Defined")
        self.access = kwargs.get("access", Access.INTERNAL)
        self.attrs = kwargs.get("attrs", [])
        self.bgcolor = kwargs.get("bgcolor", "gray99")
        self.color = kwargs.get("color", "gray10")
        self.format_href(kwargs.get("repo_url", None))
        self.modifiers = kwargs.get("modifiers", [])

        self.implements = [clean_generics(t) for t in tokens[1:] if t != "{"] if tokens else []

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, UmlEntity):
            return False
        # We are sure that we have a UmlEntity now, so it's okay to pick through its guts:
        # pylint: disable=protected-access
        return self.__tokens == other.__tokens and self.__kwargs == other.__kwargs

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__tokens}, **{self.__kwargs})"

    def __str__(self):
        mods = " " * bool(self.modifiers) + " ".join([m.value for m in self.modifiers])
        typ = self.__class__.__name__[3:].lower()
        return f"{self.access.value}{mods} {typ} {self.name}"

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

    def is_abstract(self):
        """Return True if this entity is abstract."""
        return any([m is Modifier.ABSTRACT for m in self.modifiers])

    def is_static(self):
        """Return True if this entity is static."""
        return any([m is Modifier.STATIC for m in self.modifiers])

    @staticmethod
    def parse_entity(tokens):
        """Parse tokens. Return entity and leftover tokens."""
        entity = MetaEntity(tokens[0])
        del tokens[0]
        return entity, tokens

    def parse_return_type(self, tokens):
        """Parse tokens. Return return type and leftover tokens."""
        if tokens[0] == "async":
            del tokens[0]
        return_type = tokens[0]
        if return_type.startswith(self.name.partition("_")[0] + "("):
            return_type = ""
            tokens = ["«Create»"] + tokens
        elif return_type in ["explicit", "implicit"]:
            del tokens[:2]
            return_type = tokens[0].split("(", 1)[0]
            tokens[0] = tokens[0].replace(return_type, "«Cast»")
        else:
            while return_type.endswith(","):
                del tokens[0]
                return_type = f"{return_type} {tokens[0]}"
            if return_type == "void":
                return_type = ""
            del tokens[0]
        return return_type, tokens

    def parse_tokens(self, tokens, attrs):
        """Parse line for fields and methods."""
        # Parse access level - NB: if some dolt used implicit
        # internal access we won't catch the method / field
        try:
            access = Access(tokens[0])
            del tokens[0]
        except ValueError:
            return attrs

        # Parse modifiers
        modifiers, tokens = Modifier.parse_modifiers(tokens)

        # Parse return type
        return_type, tokens = self.parse_return_type(tokens)

        # Throw away implementation if present
        if ARROW in tokens:
            tokens = tokens[: tokens.index(ARROW)]
        if CURLY in tokens:
            tokens = tokens[: tokens.index(CURLY)]
        if len(tokens) > 1 and tokens[1] == "=":
            tokens = [tokens[0]]

        # Remove default parameter values
        while "=" in tokens:
            idx = tokens.index("=")
            if tokens[idx + 1].endswith(","):
                tokens[idx - 1] = tokens[idx - 1] + ","
            elif tokens[idx + 1].endswith(")"):
                tokens[idx - 1] = tokens[idx - 1] + ")"
            del tokens[idx : idx + 2]

        # Remove parameter names
        tokens = ["," if t[-1] == "," and "<" not in t else t for t in tokens]
        tokens = [")" if t[-1] == ")" and t[-2] != "(" else t for t in tokens]

        # Rejoin method / field signature
        signature = " ".join(tokens).replace(" ,", ",").replace(" )", ")")
        if signature and signature[-1] == ";":
            signature = signature[:-1]

        # Create Method or Field and add to list
        if "(" in signature:
            self.methods.append(Method(attrs, access, modifiers, return_type, signature))
        else:
            self.fields.append(Field(attrs, access, modifiers, return_type, signature))
        return []

    def relations_to_dot(self):
        """Convert the objects relations to GraphViz/dot code."""
        rels = []
        for rel in self.implements:
            style = IMPLEMENTS if rel.startswith("I") else EXTENDS
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
        dname = sub(r"_([^_]+)_", "&lt;\\1&gt;", self.name)
        if self.is_abstract():
            dname = f"<I>{dname}</I>"
        if self.is_static():
            dname = f"<U>{dname}</U>"
        return dname


class UmlEnum(UmlEntity):
    """An enumeration."""

    def __init__(self, tokens, **kwargs):
        kwargs["bgcolor"] = "gold"
        super().__init__(tokens, **kwargs)

    def display_name(self):
        return f"«enumeration»<BR/><I>{self.name}</I>"


class UmlStruct(UmlClass):
    """A struct."""
