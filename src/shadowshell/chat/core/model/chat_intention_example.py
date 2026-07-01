#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.serialize import Serializable

from .chat_base_model import ChatBaseModel


class ChatIntentionExampleCategory(ChatBaseModel, Serializable):

    def __init__(self, code, name=None, tenant_code: str = "", biz_code: str = "",
                 id: str = "", description: str = "", ext_info: dict = None):
        ChatBaseModel.__init__(self, id=id, description=description, ext_info=ext_info or {})
        self.code = code
        self.name = name
        self.tenant_code = tenant_code
        self.biz_code = biz_code
        if self.name is None:
            self.name = self.code

    def serialize(self):
        return self.__class__.__name__

    def __dict__(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "ext_info": self.ext_info,
            "tenant_code": self.tenant_code,
            "biz_code": self.biz_code,
        }

    def __str__(self):
        return f"code={self.code}, name={self.name}"

    def __repr__(self):
        return self.__str__()


class ChatIntentionExample(ChatBaseModel, Serializable):

    def __init__(self, category=None, content=None, tenant_code: str = "", biz_code: str = "",
                 id: str = "", description: str = "", ext_info: dict = None):
        ChatBaseModel.__init__(self, id=id, description=description, ext_info=ext_info or {})
        self.category = category
        self.content = content
        self.tenant_code = tenant_code
        self.biz_code = biz_code

    def serialize(self):
        return "xx"

    def __dict__(self):
        return {
            "id": self.id,
            "category": self.category,
            "content": self.content,
            "description": self.description,
            "ext_info": self.ext_info,
            "tenant_code": self.tenant_code,
            "biz_code": self.biz_code,
        }

    def __str__(self):
        return f"\n##{self.category}\n{self.content}\n"

    def __repr__(self):
        return self.__str__()
