#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Literal

from .chat_base_model import ChatBaseModel


@dataclass(kw_only=True)
class ChatIntentionTrigger(ChatBaseModel):
    """
    Represents a trigger rule for intent matching.

    A trigger is associated with an intention node and defines how
    user input is matched — by keyword, rule engine, or few-shot examples.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    name: str
    """Trigger name."""

    code: str
    """Unique trigger code."""

    type: Literal["关键字", "规则引擎", "fewshots"]
    """Trigger type: 关键字 (keyword), 规则引擎 (rule engine), or fewshots."""

