# -*- coding: utf-8 -*-
"""Methods for globbing .cs files and building a UML class hierarchy."""

import re

try:
    from entities import UmlClass, UmlEntity, UmlEnum, UmlInterface, UmlStruct
    from features import Access, MetaEntity, Modifier
except (ImportError, ModuleNotFoundError):
    from umldotcs.entities import UmlClass, UmlEntity, UmlEnum, UmlInterface, UmlStruct
    from umldotcs.features import Access, MetaEntity, Modifier

BOM = "\ufeff"
AZAZ = "A-Za-z"

ATTRIB = f"^\\s\\[([{AZAZ}]+)"
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
        self.repo_url = repo_url

    def extract_attribute(self, line):
        """Extract an attribute from a line."""
        match = self.re_attribute.search(line)
        return None if match is None else match.group(1)

    def extract_namespace(self, line):
        """Extract the namespace from a line.
        Return None if no namespace found."""
        match = self.re_namespace.match(line)
        return None if match is None else match.group(1)

    def extract_object(self, nsp, tokens):
        """Extract a class or interface name from a line."""
        attrs = self.cur_attrs
        access, tokens = Access.parse_access(tokens)
        modifiers, tokens = Modifier.parse_modifiers(tokens)
        entity, tokens = UmlEntity.parse_entity(tokens)

        kwargs = dict(
            nsp=nsp,
            access=access,
            attrs=attrs,
            modifiers=modifiers,
            repo_url=self.repo_url,
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
        nsp, ent = None, None
        try:
            with open(self.path, "r") as file_:
                for _, line in enumerate(file_):
                    if "///" in line:
                        continue

                    if nsp is None:
                        nsp = self.extract_namespace(line)
                        continue

                    attr = self.extract_attribute(line)
                    if attr:
                        self.cur_attrs.append(attr)
                        continue

                    tokens = line.strip().split()
                    if not tokens:
                        continue

                    if ent is None and self.re_entity.search(line):
                        ent = self.extract_object(nsp, tokens)
                    elif ent:
                        self.cur_attrs = ent.parse_tokens(tokens, self.cur_attrs)
        except IsADirectoryError:
            return dict(), list()
        if nsp is None:
            raise RuntimeError(f"No namespace found in {self.path}")
        if ent is None:
            raise RuntimeError(
                f"No class, enum, struct or interface found in {self.path}"
            )
        return {nsp: [ent]}, ent.relations_to_dot()

    @staticmethod
    def write_gv(output_gv, namespaces, relations):
        """Write entities to a .gv file."""
        with open(output_gv, "w") as out:
            # TODO: configure title, fonts, label
            out.write(
                """digraph AutoLER2UML {

    graph [fontname = "Bahnschrift SemiBold", fontsize = 8]
    edge  [fontname = "Bahnschrift", fontsize = 8]
    node  [fontname = "Bahnschrift", fontsize = 8, shape = none, width=0, height=0, margin=0]

    label    = "LE34.AutoLER2 UML diagram"
    labelloc = "t"\n"""
            )
            for nsp, classes in namespaces.items():
                out.write(f"\n    // {nsp}\n\n")
                out.write("\n\n".join([ent.to_dot() for ent in classes]))
            out.write("\n\n")
            out.write("\n".join(relations))
            out.write("\n}\n")
            out.flush()
