#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

import time

from shadowshell.monitor import function_monitor
from shadowshell.boot.starter import Starter

class_mame = 'Testee'

class Testee(Starter):

  def __init__(self, work_dir = None):
    super().__init__(work_dir)

  def tests(self, testcases):
    """ 批量执行测试用例 """
    if testcases is None:
      return
    
    testcases_count = len(testcases)
    counter = 1
    for testcase in testcases:
      print(f'\n')
      self.get_logger().info(f'[测试用例执行]总共[{testcases_count}]条，当前第[{counter}]条，用例内容：{testcase}')
      self.test(testcase)
      time.sleep(3)
      counter += 1

  @function_monitor(class_mame)
  def test(self, testcase):
    pass


