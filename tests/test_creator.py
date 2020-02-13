"""Test the Creator module."""

import pytest

from umldotcs.creator import UmlCreator
from umldotcs.entities import UmlClass
from umldotcs.features import Access, Modifier


def test_extract_attribute():
    """Test UmlCreator.extract_attribute()."""
    assert UmlCreator.extract_attribute("    public bool IsValid()") is None
    assert UmlCreator.extract_attribute("    [XmlText]") == "XmlText"


def test_extract_namespace():
    """Test UmlCreator.extract_namespace()."""
    creator = UmlCreator(".")
    creator.extract_namespace("    public bool IsValid()")
    assert creator.nsp is None
    creator.extract_namespace("namespace Foo.Bar.Baz")
    assert creator.nsp == "Foo.Bar.Baz"
    creator.extract_namespace("\ufeffnamespace Quux")
    assert creator.nsp == "Quux"


def test_extract_object():
    """Test UmlCreator.extract_object()."""
    creator = UmlCreator(".")
    with pytest.raises(ValueError):
        creator.extract_object(["no", "klass", "included"])
    obj = creator.extract_object(
        [
            "public",
            "static",
            "class",
            "StaticKlass",
            ":",
            "ICanBeImplemented,",
            "IComparable,",
            "IEquatable<Klass>",
        ]
    )
    assert obj.__class__.__name__ == "UmlClass"
    assert obj.access == Access.PUBLIC
    assert obj.modifiers == [Modifier.STATIC]
    assert obj.name == "StaticKlass"
    assert obj.implements == ["ICanBeImplemented", "IComparable", "IEquatable_T_"]


def test_tokenize():
    """Test UmlCreator.tokenize()."""
    lines_vs_tokens = [
        ("    ", []),
        ("    }", ["}"]),
        (
            "public class Klass : ICanBeImplemented, IComparable, IEquatable<Klass>",
            [
                "public",
                "class",
                "Klass",
                ":",
                "ICanBeImplemented,",
                "IComparable,",
                "IEquatable<Klass>",
            ],
        ),
        ("internal Klass() => this.Blocked();", ["internal", "Klass()", "=>", "this.Blocked();"],),
        (
            "public static implicit operator string(Klass k) => k.ToString();",
            [
                "public",
                "static",
                "implicit",
                "operator",
                "string(Klass",
                "k)",
                "=>",
                "k.ToString();",
            ],
        ),
        (
            "public static bool operator <(Klass a, Klass b)",
            ["public", "static", "bool", "operator", "<(Klass", "a,", "Klass", "b)"],
        ),
        (
            "public override bool Equals(object obj)",
            ["public", "override", "bool", "Equals(object", "obj)"],
        ),
    ]
    for lvt in lines_vs_tokens:
        assert UmlCreator.tokenize(lvt[0]) == lvt[1]
