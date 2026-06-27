#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.monitor import function_monitor
from openai import OpenAI
from .chat_starter import ChatStarter


def callback(request, response):
    
    # logger = LoggerFactory.get_logger()  
    # logger.info(f"[CALLBACK][Request]{__serialize(request)}[Response]{__serialize(response)}")
    
    pass

def __serialize(obj):
    # return orjson.dumps(obj, default=lambda obj: obj.__dict__)
    # return orjson.dumps(obj)
    return obj

class_name = "LLMStarter"

class LLMStarter(ChatStarter):

    # @function_monitor(class_name)
    def __init__(self, work_dir, llm_config):
        super().__init__(work_dir)
        self.__llm_config = llm_config

    # @function_monitor(class_name)
    def init_messages(self):
        """ 初始化一个 messages 数组 """
        self.messages = [
            
        ]

    # @function_monitor(class_name)
    def get_prompts(self):
        return None
        
    # @function_monitor(class_name)
    def init_client(self):
        self.client = OpenAI(
            api_key = self.__llm_config.api_key,
            base_url = self.__llm_config.base_url,
        )

    @function_monitor(class_name)
    def call_model(self, messages):
        
        completion = self.client.chat.completions.create(
            model = self.__llm_config.model,
            messages = messages,
            extra_body = {"enable_thinking": False},
            temperature = 0.3,
            top_p = 0.7
        )

        return completion
