#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shadowshell<shadowshell@foxmail.com>
"""

import copy
from shadowshell.monitor import function_monitor

from .llm_starter import LLMStarter

class_name = 'GenChatAction'

class GenChatAction2(LLMStarter):

    def __init__(self, work_dir, base_url, api_key, model):
        super().__init__(work_dir)
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.init_messages()
        self.init_client()

    @function_monitor(class_name)
    def init_messages(self):
        """ 初始化一个 messages 数组 """
        self.messages = self.deserialize(
            self.get_file_content(f'{self.work_dir}/historyMessages/1000.json')
        )

    @function_monitor(class_name)
    def get_prompts(self):
        return self.get_file_content(f'{self.work_dir}/prompts/global_ic_prompt.md')
    
    @function_monitor(class_name)
    def action(self, user_input = None):

        messages_size = len(self.messages)
        if messages_size <= 2:
            history_messages = []
            if user_input is None:
                user_input = self.messages[1]['content']
        else:
            history_messages = self.messages[0: messages_size - 1]
            if user_input is None:
                user_input = self.messages[messages_size - 1]['content']

        intent_code = self.action0(history_messages, user_input)

        return intent_code

    @function_monitor(class_name)
    def action0(self, messages, user_input):
        return self.action_for_llm(self.append_prompt(messages), self.rewrite_user_input(user_input))

    @function_monitor(class_name)
    def append_prompt(self, messages):
        messages = copy.deepcopy(messages)
        messages.insert(0,
            {
                "role": "system",
                "content": self.get_prompts()
            }
        )
        return messages
    
    @function_monitor(class_name)
    def rewrite_user_input(self, user_input):
        return self.userinput_rewrite_tmpl.replace('{{user.query}}', user_input)
        
    @function_monitor(class_name)
    def action_for_llm(self, messages, user_input):
        """recognize_for_llm"""
        self.init_client()
        copied_messages = copy.deepcopy(messages)
        copied_messages.append({"role": "user", "content": user_input})
        return self.call_model(copied_messages).choices[0].message.content
    