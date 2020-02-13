"""Test the entities."""

# Interesting lines to parse:
#   public class Measure : ICanBeXmlSerialized, IComparable, IEquatable<Measure>
#   internal Measure() => this.Blocked();
#   public static implicit operator string(Measure m) => m.ToString();
#   public static bool operator <(Measure a, Measure b)
#   public override bool Equals(object obj)

from umldotcs.entities import UmlClass, UmlInterface
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
    assert entity.access == Access.PUBLIC
    assert entity.attrs == []
    assert entity.modifiers == [Modifier.ABSTRACT, Modifier.SEALED]
    assert entity.implements == ["IFace", "IGeneric_T_"]


def test_uml_entity___repr__():
    """Test UmlEntity.__repr__()."""
    entity = UmlInterface(["ICanBeWhateverYouWant"])
    assert repr(entity) == "internal interface ICanBeWhateverYouWant"


def test_uml_entity_format_href():
    """Test UmlEntity.format_href()."""
    entity = UmlClass(["UmlCsDll"], **dict(nsp="Uml.Cs.Dll"))
    assert entity.repo_link == ""
    entity.format_href("https://github.com/kthy/uml.cs/blob/master/tests/sln")
    href = "https://github.com/kthy/uml.cs/blob/master/tests/sln/Uml.Cs.Dll/UmlCsDll.cs"
    assert entity.repo_link == f'HREF="{href}" TARGET="_blank" TITLE="UmlCsDll.cs @ github.com"'


def test_uml_interface_display_name():
    """Test UmlInterface.display_name()."""
    interface = UmlInterface(["ICanBeWhateverYouWant"])
    assert interface.display_name() == "«interface»<BR/>ICanBeWhateverYouWant"
