#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass

from .chat_base_model import ChatBaseModel
from .chat_tenant import ChatTenant


@dataclass(kw_only=True)
class ChatBusinessScenario(ChatBaseModel):
    """
    Represents a business scenario for intent routing.

    Each scenario maps to a domain-specific conversation context,
    used to scope intent recognition and action dispatching.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    name: str
    """Scenario name."""

    code: str
    """Scenario code used in tree routing."""

    tenant: ChatTenant | None = None
    """Associated tenant for multi-tenant isolation."""
