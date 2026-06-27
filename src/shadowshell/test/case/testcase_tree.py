#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.model import Tree

class_mame = 'TestCaseTree'

class TestCaseTree(Tree):

    def __init__(self, code, name = None):
        super().__init__(code, name)
        pass
