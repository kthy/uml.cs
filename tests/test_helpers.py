"""Test the helpers."""

import pytest

from umldotcs.helpers import attrs_to_dot, clean_generics, encode_generics


def test_attrs_to_dot():
    """Test attrs_to_dot()."""
    assert attrs_to_dot(None) == ""
    assert attrs_to_dot([]) == ""
    assert attrs_to_dot(["Foo"]) == "[Foo]"
    assert attrs_to_dot(["Foo", "Bar"]) == "[Foo]<BR/>[Bar]"
    assert attrs_to_dot(["Foo", "Bar", "Baz"]) == "[Foo]<BR/>[Bar]<BR/>[Baz]"


def test_clean_generics():
    """Test clean_generics()."""
    with pytest.raises(AttributeError):
        clean_generics(None)
    assert clean_generics("") == ""
    assert clean_generics("Foo") == "Foo"
    assert clean_generics("IGeneric<Foo>") == "IGeneric_T_"
    assert clean_generics("IGeneric<Foo,Bar>") == "IGeneric_T_U_"
    assert clean_generics("IGeneric<Foo, Bar>") == "IGeneric_T_U_"
    assert clean_generics("IGeneric<Foo, Bar,Baz>") == "IGeneric_T_U_V_"
    assert clean_generics("IGeneric<Foo, Bar,Baz, Quux>") == "IGeneric_T_U_V_W_"


def test_encode_generics():
    """Test encode_generics()."""
    with pytest.raises(AttributeError):
        encode_generics(None)
    assert encode_generics("") == ""
    assert encode_generics("Foo") == "Foo"
    assert encode_generics("IGeneric<Foo>") == "IGeneric&lt;Foo&gt;"
    assert encode_generics("List<List<int>> Foo") == "List&lt;List&lt;int&gt;&gt; Foo"
    assert encode_generics("IGeneric<Foo>, bool)") == "IGeneric&lt;Foo&gt;, bool)"
    assert encode_generics("IGeneric<Foo,Bar>") == "IGeneric&lt;Foo,Bar&gt;"
    assert encode_generics("IGeneric<Foo, Bar>") == "IGeneric&lt;Foo,Bar&gt;"
    assert encode_generics("IGeneric<Foo, Bar,Baz>") == "IGeneric&lt;Foo,Bar,Baz&gt;"
    assert encode_generics("IGeneric<Foo, Bar,Baz, Quux>") == "IGeneric&lt;Foo,Bar,Baz,Quux&gt;"
