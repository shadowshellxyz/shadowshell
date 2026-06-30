#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import os

from openai import OpenAI
from shadowshell.monitor import function_monitor

class_name = "LlmClient"


class LlmConfig:
    """
    LLM configuration — reads base_url, api_key, model from a configurator group.

    Supports two api_key sources, controlled by [app] llm_apikey_source:
      - config_file (default): read api_key from the config file
      - env:                   read api_key from environment variable

    Usage:
        config = LlmConfig().build(configurator, 'llm_chatbot')

    @author: shadowshell<shadowshell@foxmail.com>
    """

    ENV_LLM_API_KEY = "SHADOWSHELL_CHAT_LLM_API_KEY"

    def __init__(self):
        pass

    @function_monitor(class_name)
    def build(self, configurator, config_group):
        self.base_url = configurator.get(config_group, 'base_url')
        self.model = configurator.get(config_group, 'model')
        self.api_key = self._resolve_api_key(configurator, config_group)
        return self

    def _resolve_api_key(self, configurator, config_group):
        source = configurator.get('app', 'llm_apikey_source') or 'config_file'
        if source == 'env':
            return os.environ.get(self.ENV_LLM_API_KEY)
        return configurator.get(config_group, 'api_key')


class LlmClient:
    """
    Standalone LLM client — composable, not inherited.

    Encapsulates OpenAI client initialization, chat completion, message preparation,
    and system prompt management. Designed to be instantiated by classes that need
    LLM functionality (LlmIntentionRecognizer, ScriptGenerationHandler, etc.).

    @author: shadowshell<shadowshell@foxmail.com>
    """

    def __init__(self, llm_config):
        """
        Args:
            llm_config: LlmConfig instance with base_url, api_key, and model.
        """
        self._llm_config = llm_config

    def init_client(self):
        """Initialize the OpenAI client."""
        self.client = OpenAI(
            api_key=self._llm_config.api_key,
            base_url=self._llm_config.base_url,
        )

    @function_monitor(class_name)
    def call_model(self, messages):
        """Call the chat completions API and return the completion."""
        completion = self.client.chat.completions.create(
            model=self._llm_config.model,
            messages=messages,
            extra_body={"enable_thinking": False},
            temperature=0.3,
            top_p=0.7,
        )
        return completion

    @function_monitor(class_name)
    def prepare_messages(self, messages, user_input=None):
        """
        Extract history messages and current user input from a message list.

        Uses the last message as current input (if user_input is None),
        and the rest as history. Treats messages with length <= 2 as having no history.

        Args:
            messages:   Full message list.
            user_input: Current user input; if None, extracted from the tail of messages.

        Returns:
            (history_messages, user_input) tuple
        """
        messages_size = len(messages)
        if messages_size <= 2:
            history_messages = []
            if user_input is None:
                user_input = messages[1]['content']
        else:
            history_messages = messages[0: messages_size - 1]
            if user_input is None:
                user_input = messages[messages_size - 1]['content']
        return history_messages, user_input

    @function_monitor(class_name)
    def chat_completion(self, messages, user_input):
        """
        Append a user message, call the LLM, and return the response text.

        Args:
            messages:    History message list.
            user_input:  Current user input.

        Returns:
            Text content returned by the LLM, or None on failure.
        """
        self.init_client()
        copied_messages = copy.deepcopy(messages)
        copied_messages.append({"role": "user", "content": user_input})
        completion = self.call_model(copied_messages)
        if completion is None:
            return None
        return completion.choices[0].message.content

    @function_monitor(class_name)
    def prepend_system_prompt(self, messages, system_prompt):
        """
        Prepend a system prompt to the message list.

        Args:
            messages:      History message list.
            system_prompt: System prompt content.

        Returns:
            New list with the system prompt inserted at index 0.
        """
        messages = copy.deepcopy(messages)
        messages.insert(0, {
            "role": "system",
            "content": system_prompt,
        })
        return messages
