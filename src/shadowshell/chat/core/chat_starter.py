#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.boot import Starter
from shadowshell.chat.common.llm_client import LlmConfig
from shadowshell.monitor import function_monitor


class_name = "ChatStarter"


class ChatStarter(Starter):
    """
    Chat starter — chatbot orchestration with file operations.

    When used with sop_path, initializes IntentionRecognizer and Tts
    for full chat capability. sop_name is derived from the last segment
    of sop_path. Config is read from the default location
    ({app_dir}/config/app.ini) using the given config_group.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    def __init__(self, app_dir=None, sop_path=None, config_group="llm_chatbot", action_handler_factory=None):
        super().__init__(app_dir)
        self._config_group = config_group
        self._handler_factory = action_handler_factory
        if sop_path:
            self._init_chat(sop_path)

    def __repr__(self):
        return self.__class__.__name__

    # ── chat orchestration ──────────────────────────────────────────────

    def _init_chat(self, sop_path):
        """Initialize chat components (IntentionRecognizer + Tts)."""
        llm_config = LlmConfig().build(self.configurator, self._config_group)
        from .intention.impl import LlmIntentionRecognizer
        from .backup.tts import Tts
        self.intention_recognizer = LlmIntentionRecognizer(app_dir=self.app_dir, llm_config=llm_config,
                                                            sop_path=sop_path)
        self.tts = Tts(self.app_dir, llm_config, self.intention_recognizer.xot)

    @function_monitor(class_name)
    def chat(self, user_input):
        intent_node = self._recognize_intention(user_input)
        return self._handle_action(intent_node, user_input)

    @function_monitor(class_name)
    def _recognize_intention(self, user_input):
        intent_code = self.intention_recognizer.recognize(user_input)
        return self.intention_recognizer.xot.find(intent_code)

    @function_monitor(class_name)
    def _handle_action(self, intent_node, user_input):
        actions_config = self._load_actions_config(intent_node)
        if actions_config:
            return self._dispatch_handlers(actions_config, intent_node, user_input)
        return self.tts.action(intent_node, user_input)

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
        from .action.action_handler_factory import ActionHandlerFactory
        from .action.action_handler_meta import ActionHandlerMeta
        from shadowshell.serialize import SerializerFactory
        llm_config = LlmConfig().build(self.configurator, self._config_group)
        serializer = SerializerFactory.get_instance()
        metas = [ActionHandlerMeta(**serializer.deserialize(serializer.serialize(item))) for item in actions_config]
        factory = self._handler_factory if self._handler_factory is not None else ActionHandlerFactory()
        handlers = factory.create(metas, self.app_dir, llm_config)
        results = []
        context = {'node': intent_node, 'user_input': user_input}
        for handler in handlers:
            result = handler.execute(intent_node.out_code, context)
            if result:
                results.append(result)
        return '\n'.join(results) if results else None
