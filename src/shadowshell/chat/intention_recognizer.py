#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy

from .xot import XoT
from .llm_starter import LLMStarter
from .llm_config import LLMConfig
from shadowshell.monitor import function_monitor
from shadowshell.serialize import SerializerFactory
from shadowshell.logging import LoggerFactory

class_name = "IntentionRecognizer"
   
def serialize(req):
    return SerializerFactory.get_instance().serialize(req[1: len(req)])

def serialize2(req):
    return SerializerFactory.get_instance().serialize(req[2: len(req)])

class IntentionRecognizer(LLMStarter):
    """
    意图识别
    @author: shadowshell<shadowshell@foxmail.com>
    """ 

    @function_monitor(class_name)
    def __init__(self, work_dir, llm_config, sop_path, sop_name):
        super().__init__(work_dir)
        self.__llm_config = llm_config
        self.init_messages()
        self.xot = XoT(work_dir)
        self.xot.build(sop_path, sop_name)
        self.userinput_rewrite_tmpl = self.get_file_content(f'{self.work_dir}/templates/global_userinput_tmpl.md')

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
    def recognize(self, user_input = None):

        messages_size = len(self.messages)
        if messages_size <= 2:
            history_messages = []
            if user_input is None:
                user_input = self.messages[1]['content']
        else:
            history_messages = self.messages[0: messages_size - 1]
            if user_input is None:
                user_input = self.messages[messages_size - 1]['content']

        intent_code = self.recognize0(self.xot.root, history_messages, user_input)

        return intent_code

    @function_monitor(class_name)
    def recognize0(self, node, messages, user_input = None):

        if node is None:
            return None

        if not node.children:
            return node.out_code
        
        examples = self.xot.recall_examples(node)
        intent_code = self.recognize_for_llm(self.append_prompt(messages), self.rewrite_user_input(user_input, examples))

        if intent_code is None or intent_code == '-1':
            return node.out_code
        
        intent_node = self.xot.find(intent_code)
                
        if intent_node is None:
            return node.out_code
        
        return self.recognize0(intent_node, messages, user_input)

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
        context = '' if not examples else ''.join(f'场景编码:{e.category.code},场景名称:{e.category.name}\n{e.content}' for e in examples)
        return self.userinput_rewrite_tmpl.replace('{{user.query}}', user_input).replace('{{context}}', context)
        
    @function_monitor(class_name)
    def recognize_for_llm(self, messages, user_input):
        """recognize_for_llm"""
        self.init_client()
        copied_messages = copy.deepcopy(messages)
        copied_messages.append({"role": "user", "content": user_input})
        return self.call_model(copied_messages).choices[0].message.content

# IntentionRecognizer().recognize()

