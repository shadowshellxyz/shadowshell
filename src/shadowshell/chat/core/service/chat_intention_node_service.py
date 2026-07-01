#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from shadowshell.chat.core.model.chat_intention_node import ChatIntentionNode


class ChatIntentionNodeService(ABC):
    """
    Service interface for ChatIntentionNode operations.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    @abstractmethod
    def list_children_by_code(self, code: str) -> list[ChatIntentionNode]:
        """
        Query child nodes by parent code.

        Args:
            code: Parent node code.

        Returns:
            List of child ChatIntentionNode instances.
        """
        ...
