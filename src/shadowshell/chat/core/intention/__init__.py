#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The intention subpackage has circular import risks (impl.llm_intention_recognizer → model.chat_xot → model.chat_intention_example).
__init__.py is kept minimal and does not re-export at this level. Upper layers import from module paths directly.

@author: shadowshell<shadowshell@foxmail.com>
"""
