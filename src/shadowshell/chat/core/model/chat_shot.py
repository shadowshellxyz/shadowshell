#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass

from .chat_base_model import ChatBaseModel


@dataclass(kw_only=True)
class ChatShot(ChatBaseModel):
    """
    Represents a single chat interaction record (one-shot example).

    Used for few-shot prompting, evaluation, and conversation logging.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    name: str
    """Chat shot name."""

    content: str
    """Chat shot content (e.g. dialogue text, prompt template)."""
