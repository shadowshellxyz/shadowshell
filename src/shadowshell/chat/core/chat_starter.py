#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.boot import Starter
from shadowshell.chat.common.llm_client import LlmConfig
from shadowshell.monitor import function_monitor

from .action.model import ActionHandlerMeta
from .intention.impl import LlmIntentionRecognizer

class_name = "ChatStarter"

class ChatStarter(Starter):
    """
    Chat starter — chatbot orchestration with file operations.

    Receives app_dir, LlmConfig, and sop_path directly in the constructor.
    Each ChatStarter instance holds its own state for full multi-instance isolation.

    Usage:
        chat = ChatStarter(action_handler_factory, app_dir="/path",
                           llm_config=llm_config, sop_path="/sop")

    @author: shadowshell<shadowshell@foxmail.com>
    """

    def __init__(self, action_handler_factory, app_dir=None, llm_config=None, sop_path=None):
        super().__init__(app_dir)
        self._handler_factory = action_handler_factory
        self._llm_config = llm_config
        if sop_path:
            self._init_chat(sop_path)

    def __repr__(self):
        return self.__class__.__name__

    # ── chat orchestration ──────────────────────────────────────────────

    def _init_chat(self, sop_path):
        """Initialize chat components."""
        self.intention_recognizer = LlmIntentionRecognizer(
            self.app_dir, self._llm_config, sop_path
        )

    @function_monitor(class_name)
    def chat(self, user_input):
        intent_node = self.recognize_intention(user_input)
        return self.dispatch_actions(intent_node, user_input)

    @function_monitor(class_name)
    def recognize_intention(self, user_input):
        intent_code = self.intention_recognizer.recognize(user_input)
        return self.intention_recognizer.xot.find(intent_code)

    @function_monitor(class_name)
    def dispatch_actions(self, intent_node, user_input):
        actions_config = self._load_actions_config(intent_node)
        if actions_config is not None:
            return self._dispatch_handlers(actions_config, intent_node, user_input)

    def _load_actions_config(self, node):
        """Load actions.json from the node directory, or None if not found."""
        if node is None or node.code is None:
            return None
        content = self.get_file_content(f'{node.code}/actions.json')
        if content is None:
            return None
        return self.deserialize(content)

    def _dispatch_handlers(self, actions_config, intent_node, user_input):
        """Instantiate handlers from actions.json config and execute them in order."""
        metas = [ActionHandlerMeta(**item) for item in actions_config]
        context = {'node': intent_node, 'user_input': user_input}
        return self._handler_factory.dispatch(metas, intent_node.out_code, context)
