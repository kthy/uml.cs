"""Test the features."""

from umldotcs.features import Access, Field, MetaEntity, Method, Modifier, attrs_to_dot

S20 = 20 * " "


def test_attrs_to_dot():
    """Test the attrs_to_dot method."""
    assert attrs_to_dot(None) == ""
    assert attrs_to_dot([]) == ""
    attrs = ["One", "Two", "Three"]
    assert attrs_to_dot(attrs) == "[One]<BR/>[Two]<BR/>[Three]"


def test_access___repr__():
    """Test the __repr__ method of the Access class."""
    access = Access.PRIVATE
    lazarus = eval(repr(access))  # pylint: disable=eval-used
    assert lazarus is Access.PRIVATE


def test_access_to_dot():
    """Test Access.to_dot()."""
    assert Access.INTERNAL.to_dot() == "~"
    assert Access.PRIVATE.to_dot() == "-"
    assert Access.PRIVATEPROTECTED.to_dot() == "-#"
    assert Access.PROTECTED.to_dot() == "#"
    assert Access.PROTECTEDINTERNAL.to_dot() == "#~"
    assert Access.PUBLIC.to_dot() == "+"


def test_parse_access():
    """Test Access.parse_access(tokens)."""
    tail = ["bool", "IsValid()"]
    assert Access.parse_access(tail) == (Access.INTERNAL, tail)
    assert Access.parse_access(["internal"] + tail) == (Access.INTERNAL, tail)
    assert Access.parse_access(["private"] + tail) == (Access.PRIVATE, tail)
    assert Access.parse_access(["private", "protected"] + tail) == (Access.PRIVATEPROTECTED, tail,)
    assert Access.parse_access(["protected"] + tail) == (Access.PROTECTED, tail)
    assert Access.parse_access(["protected", "internal"] + tail) == (
        Access.PROTECTEDINTERNAL,
        tail,
    )
    assert Access.parse_access(["public"] + tail) == (Access.PUBLIC, tail)


def test_field_or_method_is_static():
    """Test FieldOrMethod.is_static()."""
    assert not Field(["XmlText"], Access.PUBLIC, None, "string", "Content").is_static()
    assert Field(["XmlText"], Access.PUBLIC, [Modifier.STATIC], "string", "Content").is_static()
    assert not Method([], Access.PUBLIC, None, "string", "GetContent()").is_static()
    assert Method([], Access.PUBLIC, [Modifier.STATIC], "string", "GetContent()").is_static()


def test_field___eq__():
    """Test the __eq__ method of the Field class."""
    field1 = Field(["XmlText"], Access.PUBLIC, [Modifier.STATIC], "string", "Content")
    field2 = Field(["XmlText"], Access.PUBLIC, [Modifier.STATIC], "string", "Content")
    field3 = "Foo"
    field4 = None
    assert field1 == field2
    assert field1 != field3
    assert field1 != field4


def test_field___repr__():
    """Test the __repr__ method of the Field class."""
    field = Field(["One", "Two"], Access.INTERNAL, [Modifier.STATIC], "string", "Content")
    lazarus = eval(repr(field))  # pylint: disable=eval-used
    assert lazarus == field


def test_field_to_dot_with_one_attr():
    """Test Field.to_dot() with a single attribute."""
    field = Field(["XmlText"], Access.PUBLIC, None, "string", "Content")
    dot = field.to_dot()
    assert dot == f'{S20}<TR><TD>+Content : string</TD><TD ALIGN="RIGHT">[XmlText]</TD></TR>'


def test_field_to_dot_with_more_than_one_attr():
    """Test Field.to_dot() with more than one attribute."""
    field = Field(["One", "Two"], Access.INTERNAL, [Modifier.STATIC], "string", "Content")
    dot = field.to_dot()
    assert (
        dot
        == f'{S20}<TR><TD><U>~Content : string</U></TD><TD ALIGN="RIGHT">[One]<BR/>[Two]</TD></TR>'
    )


def test_field_to_dot_without_attrs():
    """Test Field.to_dot() without attributes."""
    field = Field([], Access.PRIVATE, [Modifier.STATIC], "bool", "Boolean")
    dot = field.to_dot()
    assert dot == f'{S20}<TR><TD COLSPAN="2"><U>-Boolean : bool</U></TD></TR>'


def test_meta_entity___repr__():
    """Test the __repr__ method of the MetaEntity class."""
    ment = MetaEntity.INTERFACE
    lazarus = eval(repr(ment))  # pylint: disable=eval-used
    assert lazarus is MetaEntity.INTERFACE


def test_meta_entity_as_str_list():
    """Test MetaEntity.as_str_list()."""
    assert list(MetaEntity.as_str_list()) == ["class", "enum", "interface", "struct"]


def test_method___eq__():
    """Test the __eq__ method of the Method class."""
    method1 = Method([], Access.PUBLIC, None, "string", "GetContent()")
    method2 = Method([], Access.PUBLIC, None, "string", "GetContent()")
    method3 = "Foo"
    method4 = None
    assert method1 == method2
    assert method1 != method3
    assert method1 != method4


def test_method___repr__():
    """Test the __repr__ method of the Method class."""
    method = Method([], Access.PUBLIC, None, "string", "GetContent()")
    lazarus = eval(repr(method))  # pylint: disable=eval-used
    assert lazarus == method


def test_method_is_abstract():
    """Test Method.is_abstract()."""
    assert not Method([], Access.PUBLIC, None, "string", "GetContent()").is_abstract()
    assert Method([], Access.PUBLIC, [Modifier.ABSTRACT], "string", "GetContent()").is_abstract()


def test_method_to_dot_with_one_attr():
    """Test Method.to_dot() with a single attribute."""
    method = Method(["XmlElement"], Access.PUBLIC, [], "bool", "Equals(object)")
    dot = method.to_dot()
    assert (
        dot == f'{S20}<TR><TD>+Equals(object) : bool</TD><TD ALIGN="RIGHT">[XmlElement]</TD></TR>'
    )


def test_method_to_dot_without_attrs():
    """Test Method.to_dot() without attributes."""
    method = Method([], Access.PUBLIC, [Modifier.STATIC], "string", "«Cast»(Klass)")
    dot = method.to_dot()
    assert dot == f'{S20}<TR><TD COLSPAN="2"><U>+«Cast»(Klass) : string</U></TD></TR>'

    method = Method(None, Access.PRIVATE, None, "", "Parse(string)")
    dot = method.to_dot()
    assert dot == f'{S20}<TR><TD COLSPAN="2">-Parse(string)</TD></TR>'


def test_modifier___repr__():
    """Test the __repr__ method of the Modifier class."""
    mod = Modifier.VOLATILE
    lazarus = eval(repr(mod))  # pylint: disable=eval-used
    assert lazarus is Modifier.VOLATILE


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
