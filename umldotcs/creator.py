# -*- coding: utf-8 -*-
"""Methods for globbing .cs files and building a UML class hierarchy."""

import re

from umldotcs.entities import UmlClass, UmlEntity, UmlEnum, UmlInterface, UmlStruct
from umldotcs.features import Access, MetaEntity, Modifier

BOM = "\ufeff"
AZAZ = "A-Za-z"

ATTRIB = f"^\\s*\\[([{AZAZ}]+)"
ENTITY = "|".join(MetaEntity.as_str_list())
IDENTI = f"[{AZAZ}_][{AZAZ}0-9._-]+"


class UmlCreator:
    """Utility class to keep shared state."""

    re_attribute = re.compile(ATTRIB)
    re_entity = re.compile(ENTITY)
    re_namespace = re.compile(f"{BOM}?namespace ({IDENTI})")

    def __init__(self, path, repo_url=None):
        self.cur_attrs = []
        self.path = path
        self.nsp = None
        self.repo_url = repo_url

    @classmethod
    def extract_attribute(cls, line):
        """Extract an attribute from a line."""
        match = cls.re_attribute.search(line)
        return None if match is None else match.group(1)

    def extract_namespace(self, line):
        """Extract the namespace from a line into self.nsp.
        Set self.nsp to None if no namespace found."""
        match = self.re_namespace.match(line)
        self.nsp = None if match is None else match.group(1)

    def extract_object(self, tokens):
        """Extract a class or interface name from a line."""
        attrs = self.cur_attrs
        access, tokens = Access.parse_access(tokens)
        modifiers, tokens = Modifier.parse_modifiers(tokens)
        entity, tokens = UmlEntity.parse_entity(tokens)

        kwargs = dict(
            nsp=self.nsp, access=access, attrs=attrs, modifiers=modifiers, repo_url=self.repo_url
        )

        self.cur_attrs = []

        return {
            MetaEntity.CLASS: UmlClass,
            MetaEntity.ENUM: UmlEnum,
            MetaEntity.INTERFACE: UmlInterface,
            MetaEntity.STRUCT: UmlStruct,
        }[entity](tokens, **kwargs)

    def process_file(self):
        """Process a .cs file and parse it into entities."""
        ent = None
        try:
            with open(self.path, "r") as file_:
                for _, line in enumerate(file_):
                    ent = self.process_line(line, ent)
        except IsADirectoryError:
            return dict(), list()
        if self.nsp is None:
            raise RuntimeError(f"No namespace found in {self.path}")
        if ent is None:
            raise RuntimeError(f"No class, enum, struct or interface found in {self.path}")
        # TODO: run through relations and create entities
        # for those not found already (mostly interfaces)
        return {self.nsp: [ent]}, ent.relations_to_dot()

    def process_line(self, line, ent):
        """Process a line of C# code and return an entity."""
        if "///" in line:
            return ent

        if self.nsp is None:
            self.extract_namespace(line)
            return ent

        attr = self.extract_attribute(line)
        if attr:
            self.cur_attrs.append(attr)
            return ent

        tokens = self.tokenize(line)
        if not tokens:
            return ent

        if ent is None and self.re_entity.search(line):
            return self.extract_object(tokens)

        if ent:
            self.cur_attrs = ent.parse_tokens(tokens, self.cur_attrs)

        return ent

    @staticmethod
    def tokenize(line):
        """Take a line of code, return a list of tokens."""
        return line.strip().split()

    @staticmethod
    def write_gv(output_gv, label, font, namespaces, relations):
        """Write entities to a .gv file."""
        with open(output_gv, "w") as out:
            out.write(
                f"""digraph UML {{

  graph [fontname = "{font} SemiBold", fontsize = 48]
  edge  [fontname = "{font}", fontsize = 12]
  node  [fontname = "{font}", fontsize = 12, shape = none, width=0, height=0, margin=0]

  label    = "{label}"
  labelloc = "t"\n"""
            )
            for nsp, classes in namespaces.items():
                cluster_name = nsp.replace(".", "_")
                out.write(
                    f"""\n  subgraph cluster_{cluster_name} {{
    style     = rounded
    label     = "{nsp}"
    color     = crimson\n\n"""
                )
                out.write("\n".join([ent.to_dot() for ent in classes]))
                out.write("\n  }\n")
            out.write("\n")
            out.write("\n".join(relations))
            out.write("\n}\n")
            out.flush()
