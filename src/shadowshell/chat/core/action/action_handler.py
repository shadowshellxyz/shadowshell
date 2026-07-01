#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any

from shadowshell.chat.core.model.chat_base_model import ChatBaseModel


class ActionHandler(ChatBaseModel, ABC):
    """
    Dialogue action handler interface (design layer).

    Responsibility: accept a recognized intent, execute the corresponding dialogue
    action, and generate a response. Different implementation strategies (LLM,
    rule engine, hybrid, etc.) all inherit from this interface.

    Inherits id, description, ext_info from ChatBaseModel.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    def __init__(self, name: str = "", code: str = "", type: str = "",
                 id: str = "", description: str = "", ext_info: dict = None):
        super().__init__(id=id, description=description, ext_info=ext_info or {})
        self.name = name
        self.code = code
        self.type = type

    @abstractmethod
    def execute(self, intent_code: str, context: dict[str, Any]) -> str:
        """
        Execute a dialogue action based on the intent code and context.

        Args:
            intent_code: Intent code (out_code from the XoT tree).
            context:     Context information (user input, history messages, xot node, etc.).

        Returns:
            Generated dialogue/response content.
        """
        ...

    @abstractmethod
    def handler_type(self) -> str:
        """
        Return the implementation type identifier for this handler.

        Returns:
            Type name, e.g. "llm", "rule", "hybrid".
        """
        ...
