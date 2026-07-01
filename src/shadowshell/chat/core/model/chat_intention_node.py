#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from .chat_base_model import ChatBaseModel
from .chat_business_scenario import ChatBusinessScenario
from .chat_intention_trigger import ChatIntentionTrigger
from .chat_shot import ChatShot
from ..action.action_handler import ActionHandler


@dataclass(kw_only=True)
class ChatIntentionNode(ChatBaseModel):
    """
    Represents a node in the intention recognition tree.

    Each node corresponds to a directory entry in the SOP tree,
    carrying routing metadata for intent classification.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    name: str
    """Node name."""

    code: str
    """Unique code identifying this node."""

    parent_code: str
    """Code of the parent node (empty string for root)."""

    type: str
    """Node type identifier."""

    business_scenario: ChatBusinessScenario | None = None
    """Associated business scenario for domain-scoped routing."""

    triggers: list[ChatIntentionTrigger] = field(default_factory=list)
    """Triggers associated with this intention node."""

    shots: list[ChatShot] = field(default_factory=list)
    """Chat shots (few-shot examples) associated with this intention node."""

    action_handlers: list[ActionHandler] = field(default_factory=list)
    """Action handlers associated with this intention node."""
