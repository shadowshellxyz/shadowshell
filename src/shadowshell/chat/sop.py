#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
from shadowshell.serialize import SerializerFactory
from shadowshell.model import Tree
from shadowshell.monitor import function_monitor
from shadowshell.chat import ChatStarter

class Sop(ChatStarter):

    def __init__(self):
        super().__init__()
            
    def build(self, sop_path, root_name):
        """
        构建
        @author: shadowshell<shadowshell@foxmail.com>
        """
        self.__tree = Tree(sop_path, root_name)
        self.__tree.build([(lambda node: self.__parse_out_code(node))])
        self.root = self.__tree.root
    
    def __parse_out_code(self, node):
        if node is None or node.name is None:
            return None
        node.out_code = node.name
    
    def dfs_traverse(self, output_path):
        """
        DFS 遍历树并输出为 CSV 文件

        Args:
            csv_output: CSV 输出文件路径，默认为 sop_traverse.csv
        """
       
        self.__rows = []
        self.__tree.dfs_traverse(self.root, [(lambda node: self.dd(node))])

        # 写入 CSV 文件
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['一级场景', '描述及示例', '二级场景', '描述及示例', '三级场景', '描述及示例', '四级场景（可选）', '描述及示例', '五级场景（可选）', '描述及示例', '对话动作', '备注'])
            for row in self.__rows:
                writer.writerow(row)

        print(f'CSV output written to: {output_path}')

    def dd(self, node):
        if node is None:
            return
        grand_nodes = node.get_grand_nodes()
        all_nodes = grand_nodes[::-1] + [node]

        result = []
        for n in all_nodes[1:]:  # skip root
            name = n.name.split('-', 1)[-1] if '-' in n.name else n.name
            result.append(name)
            # merge fewshots.md content if exists
            fewshots_path = os.path.join(n.code, 'fewshots.md')
            content =  self.get_file_content(fewshots_path)
            result.append(content)

        # pad to 10 columns (5 pairs of scene + fewshot)
        while len(result) < 10:
            result.append('')

        # read actions.md from leaf node for 对话动作 column
        actions_path = os.path.join(node.code, 'actions.md')
        actions_content = self.get_file_content(actions_path)
        result.append(actions_content)

        # 备注 column
        result.append('')

        self.__rows.append(result)
    
