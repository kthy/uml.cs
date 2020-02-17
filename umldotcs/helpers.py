# -*- coding: utf-8 -*-
"""Generic helper methods."""

from re import match


def attrs_to_dot(attrs):
    """Convert list of attributes to a dot string."""
    return "<BR/>".join([f"[{attr}]" for attr in attrs]) if attrs else ""


def clean_generics(token):
    """Convert a string like IAmGeneric<Foo,Bar> into IAmGeneric_T_U_."""
    token = token.strip(",")
    parts = match(r"([^<]+)<([^>]+)>", token)
    if parts:
        generics = list("TUVWXYZ"[: len(parts.group(2).split(","))])
        token = f"{parts.group(1)}_{'_'.join(generics)}_"
    return token


def encode_generics(token):
    """Convert a string like IAmGeneric<Foo,Bar> into IAmGeneric&lt;Foo,Bar&gt;."""
    return token.strip(",").replace("<", "&lt;").replace(">", "&gt;")
