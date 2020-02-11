"""Test the features."""

from umldotcs.features import Access, Field, MetaEntity, Method, Modifier, attrs_to_dot


def test_attrs_to_dot():
    """Test the attrs_to_dot method."""
    assert attrs_to_dot(None) == ""
    assert attrs_to_dot([]) == ""
    attrs = ["One", "Two", "Three"]
    assert attrs_to_dot(attrs) == "[One]<BR/>[Two]<BR/>[Three]"


def test_access_to_str():
    """Test the __str__ method of the Access class."""
    assert f"{Access.INTERNAL}" == "~"
    assert f"{Access.PRIVATE}" == "-"
    assert f"{Access.PRIVATEPROTECTED}" == "-#"
    assert f"{Access.PROTECTED}" == "#"
    assert f"{Access.PROTECTEDINTERNAL}" == "#~"
    assert f"{Access.PUBLIC}" == "+"


def test_parse_access():
    """Test Access.parse_access(tokens)."""
    tail = ["bool", "IsValid()"]
    assert Access.parse_access(tail) == (Access.INTERNAL, tail)
    assert Access.parse_access(["internal"] + tail) == (Access.INTERNAL, tail)
    assert Access.parse_access(["private"] + tail) == (Access.PRIVATE, tail)
    assert Access.parse_access(["private", "protected"] + tail) == (
        Access.PRIVATEPROTECTED,
        tail,
    )
    assert Access.parse_access(["protected"] + tail) == (Access.PROTECTED, tail)
    assert Access.parse_access(["protected", "internal"] + tail) == (
        Access.PROTECTEDINTERNAL,
        tail,
    )
    assert Access.parse_access(["public"] + tail) == (Access.PUBLIC, tail)


def test_field_to_dot_with_one_attr():
    """Test Field.to_dot() with a single attribute."""
    field = Field(["XmlText"], Access.PUBLIC, None, "string", "Content")
    dot = field.to_dot()
    assert dot == '                    <TR><TD>+Content : string</TD><TD ALIGN="RIGHT">[XmlText]</TD></TR>'


def test_field_to_dot_with_more_than_one_attr():
    """Test Field.to_dot() with more than one attribute."""
    field = Field(
        ["One", "Two"], Access.INTERNAL, [Modifier.STATIC], "string", "Content"
    )
    dot = field.to_dot()
    assert dot == '                    <TR><TD><U>~Content : string</U></TD><TD ALIGN="RIGHT">[One]<BR/>[Two]</TD></TR>'


def test_field_to_dot_without_attrs():
    """Test Field.to_dot() without attributes."""
    field = Field([], Access.PRIVATE, [Modifier.STATIC], "bool", "Boolean")
    dot = field.to_dot()
    assert dot == '                    <TR><TD COLSPAN="2"><U>-Boolean : bool</U></TD></TR>'


def test_meta_entity_as_str_list():
    """Test MetaEntity.as_str_list()."""
    assert list(MetaEntity.as_str_list()) == ["class", "enum", "interface", "struct"]


def test_method_to_dot_with_one_attr():
    """Test Method.to_dot() with a single attribute."""
    method = Method(["XmlElement"], Access.PUBLIC, [], "bool", "Equals(object o)")
    dot = method.to_dot()
    assert dot == '                    <TR><TD>+Equals(object o) : bool</TD><TD ALIGN="RIGHT">[XmlElement]</TD></TR>'


def test_method_to_dot_without_attrs():
    """Test Method.to_dot() without attributes."""
    method = Method([], Access.PUBLIC, [Modifier.STATIC], "string", "«cast»(Measure m)")
    dot = method.to_dot()
    assert dot == '                    <TR><TD COLSPAN="2"><U>+«cast»(Measure m) : string</U></TD></TR>'


def test_modifier_class_modifiers():
    """Test Modifier.class_modifiers()."""
    assert list(Modifier.class_modifiers()) == [
        Modifier.ABSTRACT,
        Modifier.NEW,
        Modifier.PARTIAL,
        Modifier.SEALED,
        Modifier.STATIC,
    ]


def test_parse_modifiers():
    """Test Modifier.parse_modifiers(tokens)."""
    tokens = [
        "abstract",
        "const",
        "extern",
        "new",
        "override",
        "partial",
        "readonly",
        "sealed",
        "unsafe",
        "static",
        "virtual",
        "volatile",
        "int",
        "RandInt()",
    ]
    assert Modifier.parse_modifiers(tokens) == (
        [
            Modifier.ABSTRACT,
            Modifier.CONST,
            Modifier.EXTERN,
            Modifier.NEW,
            Modifier.OVERRIDE,
            Modifier.PARTIAL,
            Modifier.READONLY,
            Modifier.SEALED,
            Modifier.UNSAFE,
            Modifier.STATIC,
            Modifier.VIRTUAL,
            Modifier.VOLATILE,
        ],
        ["int", "RandInt()"],
    )
