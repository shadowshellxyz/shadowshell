#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.monitor import function_monitor

from ..testee.testee import Testee
from ..case.testcase_builder import TestCaseBuilder
from ..test_starter import TestStarter

class_mame = 'Tester'

class Tester(TestStarter):

    def __init__(self, app_dir=None):
        super().__init__(app_dir)
        self.__testee = Testee()
        self.__testcase_builder = TestCaseBuilder(app_dir)

    @function_monitor(class_mame)
    def test(self):
        testcases = self.get_testcase_builder().build()
        self.get_testee().tests(testcases)

    def get_testee(self):
        return self.__testee
    
    def get_testcase_builder(self):
        return self.__testcase_builder
    
class DefaultTester(Tester):

    def __init__(self, testee, testcase_builder, app_dir = None):
        super().__init__(app_dir)
        self.__testee = testee
        self.__testcase_builder = testcase_builder
    
    def get_testee(self):
        return self.__testee
    
    def get_testcase_builder(self):
        return self.__testcase_builder

    

    

