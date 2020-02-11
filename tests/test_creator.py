"""Test the Creator module."""

from umldotcs.creator import UmlCreator


def test_extract_attribute():
    """Test UmlCreator.extract_attribute()."""
    assert UmlCreator.extract_attribute("    public bool IsValid()") is None
    assert UmlCreator.extract_attribute("    [XmlText]") == "XmlText"
