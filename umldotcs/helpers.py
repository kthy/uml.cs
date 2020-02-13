# -*- coding: utf-8 -*-
"""Generic helper methods."""

from re import match


def clean_generics(token):
    """Convert a string like IAmGeneric<Foo,Bar> into IAmGeneric_T_U_."""
    token = token.strip(",")
    if "<" in token:
        parts = match(r"([^<]+)<([^>]+)>", token)
        generics = list("TUVWXYZ"[: len(parts.group(2).split(","))])
        token = f"{parts.group(1)}_{'_'.join(generics)}_"
    return token
