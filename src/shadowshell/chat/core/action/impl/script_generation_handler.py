#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from shadowshell.chat.common.llm_client import LlmClient, LlmConfig
from shadowshell.chat.core.action.action_handler import ActionHandler
from shadowshell.chat.core.action.model import ActionHandlerMeta
from shadowshell.file import FileUtil
from shadowshell.logging import LoggerFactory
from shadowshell.serialize import SerializerFactory
from shadowshell.monitor import function_monitor

def serialize(req):
    return req

class_name = "ScriptGenerationHandler"

class ScriptGenerationHandler(ActionHandler):
    """
    Script generation action handler — generates dialogue scripts via LLM.

    Reads script-generation.md from the XoT leaf node directory as scenario
    context, then calls the LLM to produce a dialogue response.

    Uses LlmClient via composition for LLM operations.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    @function_monitor(class_name)
    def __init__(self, app_dir, llm_config: LlmConfig, meta: ActionHandlerMeta = None):
        self.app_dir = app_dir
        self.meta = meta
        self.llm = LlmClient(llm_config)
        self.init_messages()
        self.userinput_rewrite_tmpl = FileUtil.get_all(
            f'{self.app_dir}/templates/script_generation_userinput_tmpl.md'
        )

    @function_monitor(class_name, serialize)
    def handler_type(self) -> str:
        return "script-generation"

    @function_monitor(class_name, serialize)
    def init_messages(self):
        """Initialize the messages array from history file."""
        content = FileUtil.get_all(f'{self.app_dir}/historyMessages/script_generation.json')
        self.messages = SerializerFactory.get_instance().deserialize(content) if content else []

    @function_monitor(class_name, serialize)
    def get_prompts(self):
        """Load the system prompt for script generation."""
        return FileUtil.get_all(f'{self.app_dir}/prompts/script_generation_prompt.md')

    @function_monitor(class_name, serialize)
    def execute(self, intent_code: str, context: dict) -> str:
        """
        Execute script generation for the given intent.

        Args:
            intent_code: Intent code (out_code from XoT leaf node).
            context:     Dict with keys:
                         - node:       XoT leaf node (has .code for directory path)
                         - user_input: Current user input text

        Returns:
            Generated dialogue text.
        """
        node = context.get("node")
        user_input = context.get("user_input")

        if node is None:
            return None

        history_messages, user_input = self.llm.prepare_messages(self.messages, user_input)
        return self._execute(node, history_messages, user_input)

    @function_monitor(class_name, serialize)
    def _execute(self, node, messages, user_input=None):
        scenario_context = FileUtil.get_all(f'{node.code}/{self.meta.code}.md')
        prompt = self.get_prompts()
        if prompt:
            messages = self.llm.prepend_system_prompt(messages, prompt)
        return self.llm.chat_completion(messages, self.rewrite_user_input(user_input, scenario_context))

    @function_monitor(class_name, serialize)
    def rewrite_user_input(self, user_input, scenario_context):
        """Rewrite the user input with scenario context."""
        if not self.userinput_rewrite_tmpl:
            return user_input
        return (self.userinput_rewrite_tmpl
                .replace('{{user.query}}', user_input or '')
                .replace('{{context}}', scenario_context or ''))

    def get_logger(self, logger_name='root'):
        """Minimal logger access for @function_monitor compatibility."""
        return LoggerFactory.get_logger(logger_name)
