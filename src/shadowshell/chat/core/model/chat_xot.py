#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from shadowshell.file import FileUtil
from shadowshell.model import Tree

from .chat_base_model import ChatBaseModel
from .chat_intention_example import ChatIntentionExampleCategory, ChatIntentionExample

class_name = 'ChatXoT'


class ChatXoT(ChatBaseModel):

    """
    Everything of Thoughts — tree-based intent hierarchy.

    Zero-arg construction; build() initializes the tree from an SOP path.
    No dependency on Starter — only FileUtil and Tree.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    def __init__(self, tenant_code: str = None, biz_code: str = None,
                 id: str = "", description: str = "", ext_info: dict = None):
        super().__init__(id=id, description=description, ext_info=ext_info or {})
        self.tenant_code = tenant_code
        self.biz_code = biz_code

    def build(self, sop_path, root_name=None):
        """Build the XoT tree.  root_name defaults to the last segment of sop_path."""
        if root_name is None:
            root_name = os.path.basename(sop_path)
        self._tree = Tree(sop_path, root_name)
        self._tree.build([(lambda node: self._parse_out_code(node))])
        self.root = self._tree.root

    def _parse_out_code(self, node):
        if node is None or node.name is None or node.name.find("@") == -1:
            return None
        node.out_code = node.name.split("@")[0]

    def find(self, code):
        return self._tree.find_by_out_code(code)

    def recall_examples(self, node):
        if node is None or node.leaf == True or node.children is None:
            return None
        examples = []
        for child in node.children:
            if child is None:
                continue
            file_name = f'{child.code}/fewshots.md'
            example_category = ChatIntentionExampleCategory(child.out_code, child.name)
            examples.append(ChatIntentionExample(example_category, self._read_file(file_name)))
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
        content = self._read_file(final_file_name)
        if content is None or content == '':
            content = self.get_content(self._tree.root, final_file_name)
        return content

    def get_actions(self, node):
        if node is None:
            return None
        final_file_name = f'{node.code}/actions.md'
        return self._read_file(final_file_name)

    # ── internal helpers ──────────────────────────────────────────────

    @staticmethod
    def _read_file(file_path):
        """Read file content via FileUtil."""
        return FileUtil.get_all(file_path)

    def __repr__(self):
        return self.__class__.__name__
