"""Test the helpers."""

import pytest

from umldotcs.helpers import attrs_to_dot, clean_generics


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
