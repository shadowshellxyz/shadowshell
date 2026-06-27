#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.monitor import function_monitor
from shadowshell.boot.starter import Starter

class_mame = 'TestStarter'

class TestStarter(Starter):
    
  def __init__(self, work_dir = None):
    super().__init__(work_dir)
   
  def test(self):
    self.test0()

  def test0(self):
    self.get_logger().info('test0')

