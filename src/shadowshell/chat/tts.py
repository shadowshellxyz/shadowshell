#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy

from .llm_starter import LLMStarter
from shadowshell.monitor import function_monitor
from shadowshell.serialize import SerializerFactory
from shadowshell.logging import LoggerFactory

class_name = "Tts"
   
def serialize(req):
    return SerializerFactory.get_instance().serialize(req[1: len(req)])

def serialize2(req):
    return SerializerFactory.get_instance().serialize(req[2: len(req)])

class Tts(LLMStarter):
    """
    TTS
    @author: shadowshell<shadowshell@foxmail.com>
    """ 

    @function_monitor(class_name)
    def __init__(self, work_dir, llm_config, xot):
        super().__init__(work_dir)
        self.__llm_config = llm_config
        self.init_messages()
        self.xot = xot
        self.userinput_rewrite_tmpl = self.get_file_content(f'{self.work_dir}/templates/tts_userinput_tmpl.md')

    @function_monitor(class_name)
    def init_messages(self):
        """ 初始化一个 messages 数组 """
        self.messages = self.deserialize(
            self.get_file_content(f'{self.work_dir}/historyMessages/tts.json')
        )

    @function_monitor(class_name)
    def get_prompts(self):
        return self.get_file_content(f'{self.work_dir}/prompts/tts_prompt.md')
    
    @function_monitor(class_name)
    def action(self, node, user_input):
        messages_size = len(self.messages)
        if messages_size <= 2:
            history_messages = []
            if user_input is None:
                user_input = self.messages[1]['content']
        else:
            history_messages = self.messages[0: messages_size - 1]
            if user_input is None:
                user_input = self.messages[messages_size - 1]['content']

        return self.action0(node, history_messages, user_input)

    @function_monitor(class_name)
    def action0(self, node, messages, user_input = None):

        if node is None:
            return None
        
        examples = self.xot.get_actions(node)
        return self.tts_for_llm(self.append_prompt(messages), self.rewrite_user_input(user_input, examples))

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
    def rewrite_user_input(self, user_input, examples):
        return self.userinput_rewrite_tmpl.replace('{{user.query}}', user_input).replace('{{context}}', examples)
        
    @function_monitor(class_name)
    def tts_for_llm(self, messages, user_input):
        """recognize_for_llm"""
        self.init_client()
        copied_messages = copy.deepcopy(messages)
        copied_messages.append({"role": "user", "content": user_input})
        return self.call_model(copied_messages).choices[0].message.content


