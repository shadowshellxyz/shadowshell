#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class ActionHandlerMeta:
    """
    Metadata for an action handler entry in actions.json.

    Each entry describes a handler to be instantiated and executed
    for a given intent node.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    name: str
    """Handler name."""

    code: str
    """Unique code for this action instance."""

    type: str
    """Handler type identifier, e.g. 'script-generation'."""

    description: str = ""
    """Human-readable description of this action."""

    ext_info: str | None = None
    """Optional extension information (extra context, metadata, etc.)."""
