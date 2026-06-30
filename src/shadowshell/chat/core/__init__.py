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
from shadowshell.chat.core.model import XoT
from shadowshell.chat.core.action import ScriptGenerationHandler
from shadowshell.chat.op import Sop

# intention: due to circular import risk, __init__.py is kept minimal; import directly from the module here
from shadowshell.chat.core.intention.intention_recognizer import IntentionRecognizer
from shadowshell.chat.core.intention.impl import LlmIntentionRecognizer
from shadowshell.chat.core.model.intention_example import IntentionExampleCategory, IntentionExample

__all__ = [
    'ChatStarter',
    'LlmClient',
    'LlmConfig',
    'XoT',
    'Sop',
    'ScriptGenerationHandler',
    'IntentionRecognizer',
    'LlmIntentionRecognizer',
    'IntentionExampleCategory',
    'IntentionExample',
]
