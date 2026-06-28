#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.serialize import Serializable

class IntentionExampleCategory(Serializable):

    def __init__(self, code, name = None):
        self.code = code
        self.name = name
        if self.name is None:
            self.name = self.code

    def serialize(self):
        return self.__class__.__name__

    def __dict__(self):
        return {
            "code": self.code,
            "name": self.name
        }

    def __str__(self):
        return f"code={self.code}, name={self.name}"

    def __repr__(self):
        return self.__str__()

class IntentionExample(Serializable):

    def __init__(self, category = None, content = None):
        self.category = category
        self.content = content

    def serialize(self):
        return "xx"

    def __dict__(self):
        return {
            "category": self.category,
            "content": self.content
        }

    def __str__(self):
        return f"\n##{self.category}\n{self.content}\n"

    def __repr__(self):
        return self.__str__()

print(f'xx -> {isinstance(IntentionExample(), Serializable)}')