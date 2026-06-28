#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class IntentionRecognizer(ABC):
    """
    Intention recognizer interface.

    Implementations classify user input into intent codes.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    @abstractmethod
    def recognize(self, user_input=None) -> str:
        """
        Recognize the intent from user input.

        Args:
            user_input: User input text.

        Returns:
            Intent code string.
        """
        ...
