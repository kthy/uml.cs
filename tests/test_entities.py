"""Test the entities."""

# Interesting lines to parse:
#   public class Klass : ICanBeImplemented, IComparable, IEquatable<Klass>
#   internal Klass() => this.Blocked();
#   public static implicit operator string(Klass m) => m.ToString();
#   public static bool operator <(Klass a, Klass b)
#   public override bool Equals(object obj)

import pytest

from umldotcs.entities import (
    EXTENDS,
    IMPLEMENTS,
    MetaEntity,
    UmlClass,
    UmlEntity,
    UmlEnum,
    UmlInterface,
)
from umldotcs.features import Access, Modifier


def test_uml_entity___init__():
    """Test UmlEntity.__init__()."""
    kwargs = dict(
        nsp="Name.Space",
        access=Access.PUBLIC,
        attrs=[],
        repo_url="https://example.com",
        modifiers=[Modifier.ABSTRACT, Modifier.SEALED],
    )
    entity = UmlClass(["Foo", ":", "IFace", "IGeneric<Foo>"], **kwargs)
    assert entity.namespace == "Name.Space"
    assert entity.name == "Foo"
    assert entity.access is Access.PUBLIC
    assert entity.attrs == []
    assert entity.modifiers == [Modifier.ABSTRACT, Modifier.SEALED]
    assert entity.implements == ["IFace", "IGeneric_T_"]


def test_uml_entity___eq__():
    """Test UmlEntity.__eq__()."""
    kwargs = dict(
        nsp="Name.Space",
        access=Access.PUBLIC,
        attrs=[],
        repo_url="https://example.com",
        modifiers=[Modifier.ABSTRACT, Modifier.SEALED],
    )
    entity1 = UmlClass(["Foo", ":", "IFace", "IGeneric<Foo>"], **kwargs)
    entity2 = UmlClass(["Foo", ":", "IFace", "IGeneric<Foo>"], **kwargs)
    entity3 = None
    entity4 = "str"
    assert entity1 == entity2
    assert entity1 != entity3
    assert entity1 != entity4


def test_uml_entity___repr__():
    """Test UmlEntity.__repr__()."""
    kwargs = dict(
        nsp="Name.Space",
        access=Access.PUBLIC,
        attrs=[],
        repo_url="https://example.com",
        modifiers=[Modifier.ABSTRACT, Modifier.SEALED],
    )
    entity = UmlClass(["Foo", ":", "IFace", "IGeneric<Foo>"], **kwargs)
    lazarus = eval(repr(entity))  # pylint: disable=eval-used
    assert lazarus == entity


def test_uml_entity___str__():
    """Test UmlEntity.__str__()."""
    entity = UmlInterface(["ICanBeWhateverYouWant"])
    assert f"{entity}" == "internal interface ICanBeWhateverYouWant"


def test_uml_entity_format_href():
    """Test UmlEntity.format_href()."""
    entity = UmlClass(["UmlCsDll"], **dict(nsp="Uml.Cs.Dll"))
    assert entity.repo_link == ""
    entity.format_href("https://github.com/kthy/uml.cs/blob/master/tests/sln")
    href = "https://github.com/kthy/uml.cs/blob/master/tests/sln/Uml.Cs.Dll/UmlCsDll.cs"
    assert entity.repo_link == f'HREF="{href}" TARGET="_blank" TITLE="UmlCsDll.cs @ github.com"'


def test_uml_entity_relations_to_dot():
    """Test UmlEntity.relations_to_dot()."""
    klass = UmlClass(["Classy"])
    klass.implements = ["Extends", "Interface"]
    assert klass.relations_to_dot() == [
        f"    Classy -> Extends {EXTENDS}",
        f"    Classy -> Interface {IMPLEMENTS}",
    ]


def test_uml_entity_parse_entity():
    """Test UmlEntity.parse_entity(tokens)."""
    with pytest.raises(IndexError):
        UmlEntity.parse_entity([])
    with pytest.raises(ValueError):
        UmlEntity.parse_entity(["foo", "bar"])
    inputs = [
        ("class", MetaEntity.CLASS),
        ("enum", MetaEntity.ENUM),
        ("interface", MetaEntity.INTERFACE),
        ("struct", MetaEntity.STRUCT),
    ]
    for i in inputs:
        ent, toks = UmlEntity.parse_entity([i[0], "foo"])
        assert ent == i[1]
        assert toks == ["foo"]


def test_uml_class_display_name():
    """Test UmlClass.display_name()."""
    klass = UmlClass(["Classy"])
    assert klass.display_name() == "Classy"
    abstract_klass = UmlClass(["Classy"], modifiers=[Modifier.ABSTRACT])
    assert abstract_klass.display_name() == "<I>Classy</I>"
    static_klass = UmlClass(["Classy"], modifiers=[Modifier.STATIC])
    assert static_klass.display_name() == "<U>Classy</U>"


def test_uml_enum_display_name():
    """Test UmlEnum.display_name()."""
    enum = UmlEnum(["Flags"])
    assert enum.display_name() == "«enumeration»<BR/><I>Flags</I>"


def test_uml_interface_display_name():
    """Test UmlInterface.display_name()."""
    interface = UmlInterface(["ICanBeWhateverYouWant"])
    assert interface.display_name() == "«interface»<BR/>ICanBeWhateverYouWant"
