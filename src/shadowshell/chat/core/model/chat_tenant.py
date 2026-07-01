#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass

from .chat_base_model import ChatBaseModel


@dataclass(kw_only=True)
class ChatTenant(ChatBaseModel):
    """
    Represents a chat tenant (multi-tenant isolation unit).

    Each tenant owns independent conversation contexts, intent trees,
    and action configurations.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    name: str
    """Tenant display name."""

    code: str
    """Tenant code used in routing and lookup."""
