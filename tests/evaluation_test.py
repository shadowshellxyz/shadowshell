"""
@author: shadowshell<shadowshell@foxmail.com>
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathlib import Path
from shadowshell.config import Configurator

from shadowshell.test import Testee, Tester, CartesianProductTestCaseBuilder

current_dir = Path(__file__).parent.resolve()

app_dir = f'{current_dir.parent}/demo'


class DefaultTestee(Testee):

    def __init__(self, app_dir=None):
        super().__init__(app_dir)
        # self._test_chat = TestChat(app_dir)


    def test(self, testcase):
        self.get_logger().info(f'执行 testcase -> {testcase}')
        # self._test_chat.chat(testcase)
        pass

class DefaultTestCaseBuilder(CartesianProductTestCaseBuilder):

    def __init__(self, app_dir=None):
        super().__init__(app_dir)
        

class DefaultTester(Tester):

    def __init__(self, app_dir=None):
        super().__init__(app_dir)
        self.__testee = DefaultTestee(app_dir)
        self.__testcase_builder = DefaultTestCaseBuilder(app_dir)

    def get_testee(self):
        return self.__testee
    
    def get_testcase_builder(self):
        return self.__testcase_builder

DefaultTester(app_dir).test()

