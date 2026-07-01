#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from shadowshell.chat.core.model.chat_business_scenario import ChatBusinessScenario


class ChatBusinessScenarioService(ABC):
    """
    Service interface for ChatBusinessScenario operations.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    @abstractmethod
    def find_by_code(self, code: str) -> ChatBusinessScenario | None:
        """
        Query a ChatBusinessScenario by its code.

        Args:
            code: Scenario code used in tree routing.

        Returns:
            ChatBusinessScenario instance, or None if not found.
        """
        ...
