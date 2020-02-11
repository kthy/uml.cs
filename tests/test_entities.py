"""Test the entities."""

# Interesting lines to parse:
#   public class Measure : ICanBeXmlSerialized, IComparable, IEquatable<Measure>
#   internal Measure() => this.Blocked();
#   public static implicit operator string(Measure m) => m.ToString();
#   public static bool operator <(Measure a, Measure b)
#   public override bool Equals(object obj)

from umldotcs.entities import UmlInterface


def test_uml_entity___repr__():
    """Test UmlEntity.__repr__()."""
    entity = UmlInterface(["ICanBeWhateverYouWant"])
    assert repr(entity) == "internal interface ICanBeWhateverYouWant"


def test_uml_interface_display_name():
    """Test UmlInterface.display_name()."""
    interface = UmlInterface(["ICanBeWhateverYouWant"])
    assert interface.display_name() == "«interface»<BR/>ICanBeWhateverYouWant"
