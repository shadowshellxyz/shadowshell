#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.monitor import function_monitor
from shadowshell.boot.starter import Starter

class_mame = 'TestCaseBuilder'

class TestCaseBuilder(Starter):
  
  def __init__(self, work_dir = None):
    super().__init__(work_dir)

  @function_monitor(class_mame)
  def build(self):
    pass







