#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from collections import deque
import os
from shadowshell.monitor import function_monitor

"""
树节点
"""
class TreeNode():

    def __init__(self, code, name = None):
        self.code = code
        if name is None:
            name = code
        self.name = name
        self.children = []
        self.parent = None
        self.out_code = None
        self.type = None
        self.out_code = None
        self.full_name = None
        self.leaf = False
        self.content  = None
        self.ext_info = None
        pass

    def add_child(self, child):
        self.children.append(child)
        child.parent = self
    
    def get_grand_nodes(self):
        grand_nodes = []
        node = self
        while node.parent is not None:
            grand_nodes.append(node.parent)
            node = node.parent
        return grand_nodes

    def only_has_leaf_child(self):
        if self.children is None:
            return True

        for child in self.children:
            if child.leaf is False:
                return False
        
        return True
    
    def __repr__(self):
        return f'\ncode:{self.code},\nout_code:{self.out_code},\nname:{self.name}\n'

class Tree():

    def __init__(self, code, name = None):
        if name is None:
            name = code
        self.root = TreeNode(code, name)

    def build(self, funcs = None):
        self.__build0(self.root, funcs)
        return self

    # @function_monitor("Tree")
    def __build0(self, node, funcs = None):

        if node is None:
            return self
        
        if funcs is not None:
            for func in funcs:
                func(node)

        children = self.list_children(node.code)

        if len(children) == 0:
            node.leaf = True
            return self
        
        for child in children:
            node.add_child(child)
            self.__build0(child, funcs)
        
        return self

    def list_children(self, parent_code):
        
        if parent_code is None:
            return None
        
        if os.path.isdir(parent_code) == False:
            return None
        
        children = []
        for item in os.listdir(parent_code):
            child_code = os.path.join(parent_code, item)
            
            if os.path.isdir(child_code) == True:
                child = TreeNode(child_code, item)
                children.append(child)
            
        return children
    
    def bfs_traverse(self, root, funcs = None):
        if root is None:
            return
        
        queue = deque()
        queue.append(root)

        while queue:
            node = queue.popleft()
            if funcs is not None:
                for func in funcs:
                    func(node)
            queue.extend(node.children)

    def dfs_traverse(self, root, funcs = None):
        if root is None:
            return

        stack = [root]

        while stack:
            node = stack.pop()
            if funcs is not None:
                for func in funcs:
                    func(node)
            stack.extend(reversed(node.children))

    def list_leaves(self):
        leaves = []
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node.leaf == True:
                leaves.append(node)
            queue.extend(node.children)
        return leaves
    
    def find_by_code(self, target_code):
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node.code == target_code:
                return node
            queue.extend(node.children)
        return None
    
    def find_by_out_code(self, target_out_code):
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node.out_code == target_out_code:
                return node
            queue.extend(node.children)
        return None
    
    def get_root(self):
        return self.root


