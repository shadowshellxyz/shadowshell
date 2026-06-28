#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from shadowshell.chat.common.llm_client import LlmClient
from shadowshell.boot import Starter
from shadowshell.monitor import function_monitor
from shadowshell.serialize import SerializerFactory
from shadowshell.logging import LoggerFactory

class_name = "Tts"

def serialize(req):
    return SerializerFactory.get_instance().serialize(req[1: len(req)])

def serialize2(req):
    return SerializerFactory.get_instance().serialize(req[2: len(req)])

class Tts(Starter):
    """
    Text-To-Speech action handler — generates dialog responses via LLM.
    @author: shadowshell<shadowshell@foxmail.com>
    """

    @function_monitor(class_name)
    def __init__(self, app_dir, llm_config, xot):
        super().__init__(app_dir)
        self.llm = LlmClient(llm_config)
        self.init_messages()
        self.xot = xot
        self.userinput_rewrite_tmpl = self.get_file_content(f'{self.app_dir}/templates/tts_userinput_tmpl.md')

    @function_monitor(class_name)
    def init_messages(self):
        """Initialize the messages array from history file."""
        content = self.get_file_content(f'{self.app_dir}/historyMessages/tts.json')
        self.messages = self.deserialize(content) if content else []

    @function_monitor(class_name)
    def get_prompts(self):
        return self.get_file_content(f'{self.app_dir}/prompts/tts_prompt.md')

    @function_monitor(class_name)
    def action(self, node, user_input):
        history_messages, user_input = self.llm.prepare_messages(self.messages, user_input)
        return self.action0(node, history_messages, user_input)

    @function_monitor(class_name)
    def action0(self, node, messages, user_input = None):

        if node is None:
            return None

        examples = self.xot.get_actions(node)
        prompt = self.get_prompts()
        messages_with_prompt = self.llm.prepend_system_prompt(messages, prompt)
        return self.llm.chat_completion(messages_with_prompt, self.rewrite_user_input(user_input, examples))

    @function_monitor(class_name)
    def rewrite_user_input(self, user_input, examples):
        return self.userinput_rewrite_tmpl.replace('{{user.query}}', user_input).replace('{{context}}', examples or '')
