#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ...model.xot import XoT
from shadowshell.chat.common.llm_client import LlmClient, LlmConfig
from shadowshell.chat.core.intention.intention_recognizer import IntentionRecognizer
from shadowshell.file import FileUtil
from shadowshell.logging import LoggerFactory
from shadowshell.monitor import function_monitor
from shadowshell.serialize import SerializerFactory

class_name = "LlmIntentionRecognizer"

def serialize(req):
    return SerializerFactory.get_instance().serialize(req[1: len(req)])

def serialize2(req):
    return SerializerFactory.get_instance().serialize(req[2: len(req)])

class LlmIntentionRecognizer(IntentionRecognizer):
    """
    LLM-based intention recognizer — classifies user input into intent codes
    by walking the XoT tree.  Receives app_dir, LlmConfig, and sop_path
    directly in the constructor.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    @function_monitor(class_name)
    def __init__(self, app_dir: str, llm_config: LlmConfig, sop_path: str):
        self.app_dir = app_dir
        self.llm = LlmClient(llm_config)
        self.init_messages()
        self.xot = XoT()
        self.xot.build(sop_path)
        self.userinput_rewrite_tmpl = FileUtil.get_all(f'{self.app_dir}/templates/global_userinput_tmpl.md')

    @function_monitor(class_name)
    def init_messages(self):
        """Initialize the messages array from history file."""
        content = FileUtil.get_all(f'{self.app_dir}/historyMessages/1000.json')
        self.messages = SerializerFactory.get_instance().deserialize(content) if content else []

    @function_monitor(class_name)
    def get_prompts(self):
        return FileUtil.get_all(f'{self.app_dir}/prompts/global_ic_prompt.md')

    @function_monitor(class_name)
    def recognize(self, user_input=None):
        history_messages, user_input = self.llm.prepare_messages(self.messages, user_input)
        return self.recognize0(self.xot.root, history_messages, user_input)

    @function_monitor(class_name)
    def recognize0(self, node, messages, user_input=None):

        if node is None:
            return None

        if not node.children:
            return node.out_code

        examples = self.xot.recall_examples(node)
        prompt = self.get_prompts()
        messages_with_prompt = self.llm.prepend_system_prompt(messages, prompt)
        intent_code = self.llm.chat_completion(messages_with_prompt, self.rewrite_user_input(user_input, examples))

        if intent_code is None or intent_code == '-1':
            return node.out_code

        intent_node = self.xot.find(intent_code)

        if intent_node is None:
            return node.out_code

        return self.recognize0(intent_node, messages, user_input)

    @function_monitor(class_name)
    def rewrite_user_input(self, user_input, examples):
        context = '' if not examples else ''.join(
            f'场景编码:{e.category.code},场景名称:{e.category.name}\n{e.content}' for e in examples
        )
        return self.userinput_rewrite_tmpl.replace('{{user.query}}', user_input).replace('{{context}}', context)

    def get_logger(self, logger_name='root'):
        """Minimal logger access for @function_monitor compatibility."""
        return LoggerFactory.get_logger(logger_name)
