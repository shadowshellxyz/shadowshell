#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.monitor import function_monitor

from shadowshell.chat.common.llm_client import LlmClient
from shadowshell.boot import Starter

class_name = 'GenChatAction'

class GenChatAction2(Starter):

    @function_monitor(class_name)
    def __init__(self, app_dir, llm_config):
        super().__init__(app_dir)
        self.llm = LlmClient(llm_config)
        self.init_messages()
        self.userinput_rewrite_tmpl = self.get_file_content(f'{self.app_dir}/templates/global_userinput_tmpl.md')

    @function_monitor(class_name)
    def init_messages(self):
        """Initialize the messages array from history file."""
        self.messages = self.deserialize(
            self.get_file_content(f'{self.app_dir}/historyMessages/1000.json')
        )

    @function_monitor(class_name)
    def get_prompts(self):
        return self.get_file_content(f'{self.app_dir}/prompts/global_ic_prompt.md')

    @function_monitor(class_name)
    def action(self, user_input = None):
        history_messages, user_input = self.llm.prepare_messages(self.messages, user_input)
        return self.action0(history_messages, user_input)

    @function_monitor(class_name)
    def action0(self, messages, user_input):
        prompt = self.get_prompts()
        messages_with_prompt = self.llm.prepend_system_prompt(messages, prompt)
        return self.llm.chat_completion(messages_with_prompt, self.rewrite_user_input(user_input))

    @function_monitor(class_name)
    def rewrite_user_input(self, user_input):
        return self.userinput_rewrite_tmpl.replace('{{user.query}}', user_input)
