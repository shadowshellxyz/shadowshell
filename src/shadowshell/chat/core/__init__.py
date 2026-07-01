#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

# direct modules (api layer)
from shadowshell.chat.core.chat_starter import ChatStarter
from shadowshell.chat.common.llm_client import LlmClient, LlmConfig

# direct modules (implementation)
# subpackages
from shadowshell.chat.core.model import ChatXoT
from shadowshell.chat.core.action import ScriptGenerationHandler
from shadowshell.chat.op import Sop

# intention: due to circular import risk, __init__.py is kept minimal; import directly from the module here
from shadowshell.chat.core.intention.intention_recognizer import IntentionRecognizer
from shadowshell.chat.core.intention.impl import LlmIntentionRecognizer
from shadowshell.chat.core.model.chat_intention_example import ChatIntentionExampleCategory, ChatIntentionExample

__all__ = [
    'ChatStarter',
    'LlmClient',
    'LlmConfig',
    'ChatXoT',
    'Sop',
    'ScriptGenerationHandler',
    'IntentionRecognizer',
    'LlmIntentionRecognizer',
    'ChatIntentionExampleCategory',
    'ChatIntentionExample',
]
