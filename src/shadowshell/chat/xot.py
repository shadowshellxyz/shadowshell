#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from shadowshell.serialize import SerializerFactory
from shadowshell.model import Tree
from shadowshell.monitor import function_monitor
from .chat_starter import ChatStarter

from .intention_example import IntentionExampleCategory, IntentionExample
class_name = 'XOT'

class XoT(ChatStarter):
    
    """
    Everything of Thoughts
    @author: shadowshell<shadowshell@foxmail.com>
    """

    def __init__(self, work_dir):
        super().__init__(work_dir)
            
    def build(self, sop_path, root_name):
        """
        构建
        """
        self.__tree = Tree(sop_path, root_name)
        self.__tree.build([(lambda node: self.__parse_out_code(node))])
        self.root = self.__tree.root

    def __parse_out_code(self, node):
        if node is None or node.name is None or node.name.find("@") == -1:
            return None
        
        node.out_code = node.name.split("@")[0]

    def find(self, code):
        return self.__tree.find_by_out_code(code)
    
    @function_monitor(class_name)
    def recall_examples(self, node):
        if node is None or node.leaf == True or node.children is None:
            return None
        
        examples = []
        for child in node.children:
            if child is None:
                continue
            file_name = f'{child.code}/fewshots.md'
            example_category = IntentionExampleCategory(child.out_code, child.name)
            examples.append(IntentionExample(example_category, self.get_file_content(file_name)))
            
        return examples
    
    def get_children_content(self, node):
        if node is None or node.leaf == True or node.children is None:
            return None
        
        content = []
        for child in node.children:
            if child is None:
                continue
            part_content = self.get_content(child, 'fewshots.md')
            content.append(f'\n场景编码:{child.out_code},场景名称:{child.name}\n{part_content}')
            
        return content
     
    def get_content(self, node, file_name):
        if node is None:
            return None
        final_file_name = f'{node.code}/{file_name}'
        content = self.get_file_content(final_file_name)

        if content is None or content == '':
            content = self.get_content(self.__tree.root, final_file_name)
        
        return content
    
    def get_actions(self, node):
        if node is None:
            return None
        final_file_name = f'{node.code}/actions.md'
        content = self.get_file_content(final_file_name)
        return content
    
    def __repr__(self):
        return self.__class__.__name__ 

# xot = XoT()
# print('xxx')
# print(f'dd -> {xot.root.name}')
# examples = xot.recall_examples(xot.root)
# print(examples)

