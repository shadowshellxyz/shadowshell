#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shadowshell<shadowshell@foxmail.com>
"""
from shadowshell.monitor import function_monitor
from .intention_recognizer import IntentionRecognizer
from .chat_starter import ChatStarter
from .tts import Tts
from .llm_config import LLMConfig


class_name = 'ChatBot'

class ChatBot(ChatStarter):

    def __init__(self, work_dir, conf_path, sop_path, sop_name):
        self.conf_path = conf_path
        self.__work_dir = work_dir
        super().__init__(work_dir)
        self.__sop_path = sop_path
        self.__sop_name = sop_name
        llm_config = self.__init_llm_config()

        self.intention_recognizer = IntentionRecognizer(self.__work_dir, llm_config, self.__sop_path, self.__sop_name)
        self.tts = Tts(self.__work_dir, llm_config, self.intention_recognizer.xot)

    def __init_llm_config(self):
        llm_conf_group = 'llm_chatbot'
        base_url = self.configurator.get(llm_conf_group, 'base_url')
        api_key = self.configurator.get(llm_conf_group, 'api_key')
        model = self.configurator.get(llm_conf_group, 'model')
        return LLMConfig(base_url, api_key, model)

    def get_config_file_path(self):
        return self.conf_path

    @function_monitor(class_name)
    def chat(self, user_input):
        intent_code = self.intention_recognizer.recognize(user_input)
        intent_node = self.intention_recognizer.xot.find(intent_code)
        return self.tts.action(intent_node, '')        
        
        