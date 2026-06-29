#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.chat.core.action.action_handler import ActionHandler
from shadowshell.chat.core.action.action_handler_meta import ActionHandlerMeta
from shadowshell.chat.core.action.impl import ScriptGenerationHandler
from shadowshell.chat.core.action.action_handler_factory import ActionHandlerFactory
from shadowshell.chat.core.action.impl.local_tree_action_handler_factory import LocalTreeActionHandlerFactory
from shadowshell.chat.core.action.impl.default_action_handler_factory import DefaultActionHandlerFactory

# Re-export legacy handlers from backup
from shadowshell.chat.core.backup import Tts, GenChatAction2

__all__ = [
    'ActionHandler',
    'ActionHandlerMeta',
    'Tts',
    'GenChatAction2',
    'ScriptGenerationHandler',
    'ActionHandlerFactory',
    'LocalTreeActionHandlerFactory',
    'DefaultActionHandlerFactory',
]
