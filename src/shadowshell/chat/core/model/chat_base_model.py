#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class ChatBaseModel:
    """
    Base model for all chat domain classes.

    Provides common attributes: id, description, and extensible metadata (ext_info).

    @author: shadowshell<shadowshell@foxmail.com>
    """

    id: str
    """Unique identifier."""

    description: str = ""
    """Human-readable description."""

    ext_info: dict = field(default_factory=dict)
    """Extension information (Map type) for arbitrary metadata."""
