#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from shadowshell.chat.core.model.chat_intention_node import ChatIntentionNode
from shadowshell.chat.core.service.chat_intention_node_service import ChatIntentionNodeService


class ChatIntentionNodeServiceImpl(ChatIntentionNodeService):
    """
    Default implementation of ChatIntentionNodeService.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    def list_children_by_code(self, code: str) -> list[ChatIntentionNode]:
        """Query child nodes by parent code. (empty implementation)"""
        pass
