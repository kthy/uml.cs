"""Test the CLI."""

from umldotcs.cli import (
    NAMESPACES,
    RELATIONS,
    exclude,
    glob_files,
    write_output,
    zip_namespaces,
    zip_relations,
)


def test_glob_files():
    """Test cli.glob_files(dir)."""
    base_path = "./tests/sln/"
    assert glob_files(".") == [
        base_path + f
        for f in [
            "Uml.Cs.App/Program.cs",
            "Uml.Cs.Dll/ICanBeImplemented.cs",
            "Uml.Cs.Dll/SubUmlCsDll.cs",
            "Uml.Cs.Dll/UmlCsDll.cs",
            "Uml.Cs.Dll/UmlEnum.cs",
        ]
    ]


def test_exclude():
    """Test cli.exclude()."""
    should_be_excluded = [
        "./tests/sln/Uml.Cs.Dll/bin/Debug/netcoreapp2.1/UmlCsDll.cs",
        "./tests/sln/Uml.Cs.Dll/obj/Debug/netcoreapp2.1/UmlCsDll.cs",
        "./tests/sln/Uml.Cs.Dll/bin/Release/netcoreapp2.1/UmlCsDll.cs",
        "./tests/sln/Uml.Cs.Dll/obj/Release/netcoreapp2.1/UmlCsDll.cs",
        "./tests/sln/Uml.Cs.App/Properties/AssemblyInfo.cs",
        "./tests/sln/Uml.Cs.Dll.Test/UmlCsDllTest.cs",
    ]
    should_be_included = [
        "./tests/sln/Uml.Cs.App/Program.cs",
        "./tests/sln/Uml.Cs.Dll/ICanBeImplemented.cs",
        "./tests/sln/Uml.Cs.Dll/SubUmlCsDll.cs",
        "./tests/sln/Uml.Cs.Dll/UmlCsDll.cs",
        "./tests/sln/Uml.Cs.Dll/UmlEnum.cs",
    ]
    assert any([exclude(p) for p in should_be_excluded])
    assert not any([exclude(p) for p in should_be_included])


def test_write_output():
    """Test cli.write_output()."""
    assert NAMESPACES == {}
    assert write_output(None, None, None, None) == 0


def test_zip_namespaces():
    """Test cli.zip_namespaces()."""
    assert NAMESPACES == {}
    nsp_inner = {"Inner.Space": [1, 2, 3]}
    zip_namespaces(nsp_inner)
    assert NAMESPACES == nsp_inner
    nsp_outer1 = {"Outer.Space": [4, 5, 6]}
    nsp_outer2 = {"Outer.Space": [7, 8, 9]}
    zip_namespaces(nsp_outer1)
    zip_namespaces(nsp_outer2)
    nsp_merged = {"Inner.Space": [1, 2, 3], "Outer.Space": [4, 5, 6, 7, 8, 9]}
    assert NAMESPACES == nsp_merged
    NAMESPACES == {}  # pylint: disable=pointless-statement


def test_zip_relations():
    """Test cli.zip_relations()."""
    assert RELATIONS == []
    zip_relations(["foo"])
    assert RELATIONS == ["foo"]
