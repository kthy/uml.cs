"""Test the entities."""

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
from umldotcs.features import Access, Field, Method, Modifier


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


def test_uml_entity_parse_tokens():
    """Test UmlEntity.parse_tokens(tokens, attr)."""
    klass = UmlClass(["Klass"])
    attrs = klass.parse_tokens(["}"], ["Attr"])
    assert klass.methods == []
    assert attrs == ["Attr"]

    tokens = "public Guid Id { get; set; }".split()
    klass.parse_tokens(tokens, None)
    assert klass.fields[0] == Field(None, Access.PUBLIC, [], "Guid", "Id")

    tokens = "private static readonly string CrLf = Environment.NewLine;".split()
    klass.parse_tokens(tokens, None)
    assert klass.fields[1] == Field(
        None, Access.PRIVATE, [Modifier.STATIC, Modifier.READONLY], "string", "CrLf"
    )

    tokens = "private readonly List<List<int>> IntMatrix = new List<List<int>>();".split()
    klass.parse_tokens(tokens, None)
    assert klass.fields[2] == Field(
        None, Access.PRIVATE, [Modifier.READONLY], "List&lt;List&lt;int&gt;&gt;", "IntMatrix"
    )

    line_vs_expected = [
        (
            "protected async Task<int> Do(string sql, IEnumerable<object> subs, bool prep = true)",
            None,
            Method(
                None,
                Access.PROTECTED,
                [],
                "Task&lt;int&gt;",
                "Do(string, IEnumerable&lt;object&gt;, bool)",
            ),
        ),
        ("public void Do()", None, Method(None, Access.PUBLIC, [], "", "Do()")),
        (
            "internal Klass() => this.Blocked();",
            None,
            Method(None, Access.INTERNAL, [], "", "«Create» Klass()"),
        ),
        (
            "public override bool Equals(object obj)",
            None,
            Method(None, Access.PUBLIC, [Modifier.OVERRIDE], "bool", "Equals(object)"),
        ),
        (
            "public string Concat(string first, string second)",
            ["Attr"],
            Method(["Attr"], Access.PUBLIC, [], "string", "Concat(string, string)"),
        ),
        (
            "public static bool operator <(Klass a, Klass b)",
            None,
            Method(None, Access.PUBLIC, [Modifier.STATIC], "bool", "operator <(Klass, Klass)"),
        ),
        (
            "public static implicit operator string(Klass m) => m.ToString();",
            None,
            Method(None, Access.PUBLIC, [Modifier.STATIC], "string", "«Cast»(Klass)"),
        ),
    ]
    for lve in line_vs_expected:
        klass = UmlClass(["Klass"])
        klass.parse_tokens(lve[0].split(), lve[1])
        assert klass.methods == [lve[2]]


def test_uml_entity_relations_to_dot():
    """Test UmlEntity.relations_to_dot()."""
    klass = UmlClass(["Classy"])
    klass.implements = ["Extends", "Interface"]
    assert klass.relations_to_dot() == [
        f"    Classy -> Extends {EXTENDS}",
        f"    Classy -> Interface {IMPLEMENTS}",
    ]


def test_uml_entity_to_dot():
    """Test UmlEntity.to_dot()."""
    klass = UmlClass(["Klass"])
    klass.methods.append(Method(None, Access.PROTECTED, [], "", "«Create» Klass()"))
    klass.methods.append(Method(None, Access.PUBLIC, [], "int", "GetCount()"))
    klass.methods.append(Method(["XmlAttr"], Access.INTERNAL, [], "", "Do(string, byte[])"))
    klass.fields.append(Field(None, Access.PUBLIC, [], "Guid", "Id"))
    klass.fields.append(Field(["XmlText"], Access.PUBLIC, [], "string", "Name"))
    klass.fields.append(Field(None, Access.PRIVATE, [Modifier.STATIC], "int", "Count"))
    assert (
        klass.to_dot()
        == """    Klass [
        color = gray10,
        label = <<TABLE BGCOLOR="gray99" BORDER="1" CELLBORDER="0" CELLSPACING="0">
                    <TR><TD PORT="name" COLSPAN="2">Klass</TD></TR>
                    <HR/>
                    <TR><TD ALIGN="LEFT" COLSPAN="2">+Id : Guid</TD></TR>
                    <TR><TD ALIGN="LEFT">+Name : string</TD><TD ALIGN="RIGHT">[XmlText]</TD></TR>
                    <TR><TD ALIGN="LEFT" COLSPAN="2"><U>-Count : int</U></TD></TR>
                    <HR/>
                    <TR><TD ALIGN="LEFT" COLSPAN="2">#«Create» Klass()</TD></TR>
                    <TR><TD ALIGN="LEFT" COLSPAN="2">+GetCount() : int</TD></TR>
                    <TR><TD ALIGN="LEFT">~Do(string, byte[])</TD><TD ALIGN="RIGHT">[XmlAttr]</TD></TR>
                </TABLE>>
    ]
"""
    )

    iface = UmlInterface(["IComparable"])
    assert (
        iface.to_dot()
        == """    IComparable [
        color = darkolivegreen,
        label = <<TABLE BGCOLOR="darkolivegreen1" BORDER="1" CELLBORDER="0" CELLSPACING="0">
                    <TR><TD PORT="name" COLSPAN="2">«interface»<BR/>IComparable</TD></TR>
                </TABLE>>
    ]
"""
    )


def test_uml_class_display_name():
    """Test UmlClass.display_name()."""
    klass = UmlClass(["Classy"])
    assert klass.display_name() == "Classy"
    abstract_klass = UmlClass(["Classy"], modifiers=[Modifier.ABSTRACT])
    assert abstract_klass.is_abstract()
    assert abstract_klass.display_name() == "<I>Classy</I>"
    static_klass = UmlClass(["Classy"], modifiers=[Modifier.STATIC])
    assert static_klass.is_static()
    assert static_klass.display_name() == "<U>Classy</U>"


def test_uml_enum_display_name():
    """Test UmlEnum.display_name()."""
    enum = UmlEnum(["Flags"])
    assert enum.display_name() == "«enumeration»<BR/><I>Flags</I>"


def test_uml_interface_display_name():
    """Test UmlInterface.display_name()."""
    interface = UmlInterface(["ICanBeWhateverYouWant"])
    assert interface.display_name() == "«interface»<BR/>ICanBeWhateverYouWant"
