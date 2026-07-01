#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from shadowshell.chat.core.model.chat_business_scenario import ChatBusinessScenario
from shadowshell.chat.core.service.chat_business_scenario_service import ChatBusinessScenarioService


class ChatBusinessScenarioServiceImpl(ChatBusinessScenarioService):
    """
    Default implementation of ChatBusinessScenarioService.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    def find_by_code(self, code: str) -> ChatBusinessScenario | None:
        """Query a ChatBusinessScenario by its code. (empty implementation)"""
        pass
