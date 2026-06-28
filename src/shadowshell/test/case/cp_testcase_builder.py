#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.monitor import function_monitor
from shadowshell.file import FileUtil
from shadowshell.test import TestCaseTree

from .testcase_builder import TestCaseBuilder

import itertools

class_mame = 'CartesianProductTestCaseBuilder'

class CartesianProductTestCaseBuilder(TestCaseBuilder):
  
  def __init__(self, app_dir = None):
    super().__init__(app_dir)
    self.data_file_name = self.configurator.get('test', 'data_file_name')

    # 解析测试用例要素
    script_paths = self.configurator.get('test', 'script_paths')
    if script_paths is None or len(script_paths) <= 0:
      return
        
    script_path_list = script_paths.split(',')
    if len(script_path_list) <= 0:
        return    
    items_all = []
    for script_path in script_path_list:
      part_items = self.__extract_items(f'{self.app_dir}/{script_path}')
      items_all.append(part_items)
    self.arrays = items_all

  @function_monitor(class_mame)
  def build(self):
    if self.arrays is None or len(self.arrays) <= 0:
      return []
    
    testcases = []
    for combined in itertools.product(*self.arrays):
      # print(f'combined -->> {combined}')
      l1 = []
      for item in combined:
          for item1 in item:
              l1.append(item1)
      for testcase in itertools.product(*tuple(l1)):
          testcases.append(testcase)
    return testcases
     
  @function_monitor(class_mame)
  def __extract_items(self, node_code):
    
    tree = TestCaseTree(node_code).build()
    leaves = tree.list_leaves()
    if len(leaves) == 0:
      return None
    
    result_list = []

    for leaf in leaves:
      arrays = []
      grand_nodes = leaf.get_grand_nodes()
      grand_nodes.insert(0, leaf)
      
      for index in range(len(grand_nodes) - 1, -1, -1):
        file_path = f'{grand_nodes[index].code}/{self.data_file_name}'
        items = FileUtil.read_csv_to_list(file_path)
        if len(items) > 0:
          arrays.append(items)

      print(f'--->>> {arrays}')

      result_list.append(arrays)

    return result_list
