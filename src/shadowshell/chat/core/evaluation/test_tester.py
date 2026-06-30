#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell
"""

from shadowshell.logging import LoggingConstants, LoggerFactory

from shadowshell.file import FileUtil
from shadowshell.request import Request
from shadowshell.test import Testee, Tester, CartesianProductTestCaseBuilder

class DefaultTestee(Testee):

    def __init__(selfs, app_dir=None):
        super().__init__(app_dir)
  
    # def __test(self, user_contents, messages):
    #     self.get_logger().info(f'{self.assistant_alias_name}: {self.__prologue}')
    #     for user_content in user_contents:
    #         self.__test0(user_content, messages)

    # def __test0(self, user_content, messages):
    #     assistant_content = self.__chat([user_content])
    
    # def __chat(self, content):
    #     pass

    def test(self, testcase):
        self.get_logger().info(f'执行 testcase -> {testcase}')
        pass

class DefaultTestCaseBuilder(CartesianProductTestCaseBuilder):

    def __init__(self, app_dir=None):
        super().__init__(app_dir)
        

class DefaultTester(Tester):

    def __init__(self, app_dir=None):
        super().__init__(app_dir)
        self.__testee = DefaultTestee()
        self.__testcase_builder = DefaultTestCaseBuilder()

    def get_testee(self):
        return self.__testee
    
    def get_testcase_builder(self):
        return self.__testcase_builder

