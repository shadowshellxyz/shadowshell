#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tree-based ActionHandlerFactory implementation.

@author: shadowshell<shadowshell@foxmail.com>
"""

import importlib.util
import os
import sys

from shadowshell.model import Tree
from shadowshell.boot import Starter
from shadowshell.chat.common.llm_client import LlmClient

from shadowshell.chat.core.action.action_handler import ActionHandler
from shadowshell.chat.core.action.model import ActionHandlerMeta
from shadowshell.chat.core.action.factory.action_handler_factory import ActionHandlerFactory

class_name = 'LocalTreeActionHandlerFactory'


class LocalTreeActionHandlerFactory(Starter, ActionHandlerFactory):
    """
    Everything of Thoughts — tree-based ActionHandlerFactory.

    Builds a tree from an SOP path for intent routing, and implements
    the ActionHandlerFactory interface for handler lifecycle management.

    Infrastructure dependencies (app_dir, llm_config) are injected at
    construction time.  llm_config is optional — set it before calling
    methods that require LLM access (_before_execute, _after_execute, create).

    Usage:
        factory = LocalTreeActionHandlerFactory(app_dir, llm_config)
        factory.build(action_handlers_dir)
        factory.register("echo", EchoHandler)
        handlers = factory.create(metas)

    @author: shadowshell<shadowshell@foxmail.com>
    """

    def __init__(self, app_dir: str, llm_config=None):
        """
        Args:
            app_dir:    Working directory for file operations.
            llm_config: Optional LlmConfig instance (can be set later).
        """
        super().__init__(app_dir)
        self._llm_config = llm_config
        self._registry = {}

    # ── Tree operations ─────────────────────────────────────────────────

    def build(self, action_handlers_dir=None):
        """
        Build the action handler tree from the action handlers directory.

        Args:
            action_handlers_dir: Path to the action handlers directory structure.
                                 Defaults to config.action_handlers_dir if omitted.
        """
        if action_handlers_dir is None:
            raise ValueError("action_handlers_dir is required")
        self._action_handlers_dir = action_handlers_dir
        self._tree = Tree(action_handlers_dir)
        self._tree.build([(lambda node: self._parse_out_code(node))])
        self.root = self._tree.root

    def _parse_out_code(self, node):
        """Extract out_code from node name (format: code@description)."""
        if node is None or node.name is None or node.name.find("@") == -1:
            return None

        node.out_code = node.name.split("@")[0]

    def find(self, code):
        """
        Find a tree node by its out_code.

        Args:
            code: The out_code to search for.

        Returns:
            The matching tree node, or None if not found.
        """
        return self._tree.find_by_out_code(code)

    def get_content(self, node, file_name):
        """
        Get file content relative to a tree node, falling back to root.

        Args:
            node:      Tree node to resolve the path against.
            file_name: File name (relative to node.code).

        Returns:
            File content string, or None if not found.
        """
        if node is None:
            return None
        final_file_name = f'{node.code}/{file_name}'
        content = self.get_file_content(final_file_name)

        if (content is None or content == '') and node is not self._tree.root:
            content = self.get_content(self._tree.root, final_file_name)

        return content

    # ── ActionHandlerFactory interface ──────────────────────────────────

    def create(self, metas: list[ActionHandlerMeta]) -> list[ActionHandler]:
        """
        Create ActionHandler instances for the given metadata entries.

        Resolution order for each meta:
        1. find(meta.code) → tree node (structural context).
        2. Registry lookup by meta.type.
        3. If not registered, try to auto-load handler.py from the node's
           directory, register it, and retry.

        Args:
            metas:  List of ActionHandlerMeta objects parsed from actions.json.

        Returns:
            List of instantiated ActionHandler objects.

        Raises:
            RuntimeError: If the tree has not been built (call build() first).
            ValueError:   If a handler type cannot be resolved after trying
                          all resolution strategies.
        """
        if not hasattr(self, '_tree'):
            raise RuntimeError(
                "Tree has not been built — call build(action_handlers_dir) before create()"
            )

        handlers = []
        for meta in metas:
            node = self.find(meta.code)
            handler_class = self._registry.get(meta.type)

            # Auto-load handler.py from the tree node when not yet registered
            if handler_class is None and node is not None:
                handler_class = self._load_handler_from_node(node)
                if handler_class is not None:
                    self.register(meta.type, handler_class)
                    self.get_logger().info(
                        f"Auto-registered handler '{meta.type}' from "
                        f"'{node.code}/handler.py'"
                    )

            if handler_class is None:
                raise ValueError(
                    f"Unknown handler type: '{meta.type}'. "
                    f"Registered types: {list(self._registry.keys())}"
                )

            if node is not None:
                self.get_logger().info(
                    f"Resolved action '{meta.code}' to tree node '{node.name}'"
                )
            handlers.append(handler_class(self.app_dir, self._llm_config, meta))
        return handlers

    def _load_handler_from_node(self, node) -> type | None:
        """
        Dynamically load an ActionHandler subclass from {node.code}/handler.py.

        Args:
            node:  Tree node whose directory may contain handler.py.

        Returns:
            An ActionHandler subclass found in the module, or None if the
            file does not exist or contains no valid handler class.
        """
        handler_path = os.path.join(self._action_handlers_dir, node.code, 'handler.py')
        if not os.path.isfile(handler_path):
            return None

        module_name = f"_dynamic_handler_{node.out_code}"
        try:
            spec = importlib.util.spec_from_file_location(module_name, handler_path)
            if spec is None or spec.loader is None:
                return None
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
        except Exception as e:
            self.get_logger().warning(
                f"Failed to load handler.py for node '{node.code}': {e}"
            )
            return None

        # Find the first ActionHandler subclass in the loaded module
        for obj in vars(module).values():
            if (
                isinstance(obj, type)
                and issubclass(obj, ActionHandler)
                and obj is not ActionHandler
            ):
                return obj

        self.get_logger().warning(
            f"No ActionHandler subclass found in '{node.code}/handler.py'"
        )
        return None

    def register(self, handler_type: str, handler_class: type) -> None:
        """
        Register a new handler type.

        Args:
            handler_type:  Handler type identifier string.
            handler_class: ActionHandler subclass.

        Raises:
            TypeError: If handler_class does not implement ActionHandler.
        """
        if not issubclass(handler_class, ActionHandler):
            raise TypeError(
                f"Handler class '{handler_class.__name__}' must implement ActionHandler"
            )
        self._registry[handler_type] = handler_class

    # ── Lifecycle hooks ─────────────────────────────────────────────────

    def _before_execute(
        self, meta: ActionHandlerMeta, intent_code: str, context: dict
    ) -> dict | None:
        """
        Process before.md from the tree node as pre-execution context.

        When the action's tree node contains a before.md file its content is
        sent to the LLM for processing.  The LLM response is merged into the
        handler's execution context as ``_before_result``.

        Args:
            meta:        ActionHandlerMeta for the current handler.
            intent_code: The resolved intent code.
            context:     Current execution context (must contain 'user_input').

        Returns:
            Dict with key '_before_result' to merge into context, or None if
            no before.md exists or processing fails.
        """
        if self._llm_config is None:
            return None

        node = self.find(meta.code)
        if node is None:
            return None

        before_content = self.get_content(node, 'before.md')
        if before_content is None:
            return None

        try:
            llm = LlmClient(self._llm_config)
            messages = [{'role': 'system', 'content': before_content + '\n/no_think'}]
            user_input = context.get('user_input', '')
            processed = llm.chat_completion(messages, user_input)
            if processed:
                self.get_logger().info(
                    f"before.md processed for '{meta.code}' → "
                    f"'{processed[:80]}...'"
                )
                return {'_before_result': processed}
        except Exception as e:
            self.get_logger().warning(
                f"before.md processing failed for '{meta.code}': {e}"
            )

        return None

    def _after_execute(
        self,
        meta: ActionHandlerMeta,
        intent_code: str,
        result: str,
        context: dict,
    ) -> str | None:
        """
        Post-process the handler result with after.md from the tree node.

        When the action's tree node contains an after.md file the handler
        result is sent to the LLM together with the after.md instructions
        for refinement.

        Args:
            meta:        ActionHandlerMeta for the current handler.
            intent_code: The resolved intent code.
            result:      Raw result from handler.execute().
            context:     Execution context (may contain '_before_result').

        Returns:
            LLM-refined result, or the original result if no after.md
            exists or processing fails.
        """
        if self._llm_config is None:
            return result

        node = self.find(meta.code)
        if node is None:
            return result

        after_content = self.get_content(node, 'after.md')
        if after_content is None:
            return result

        try:
            llm = LlmClient(self._llm_config)
            messages = [{'role': 'system', 'content': after_content + '\n/no_think'}]
            processed = llm.chat_completion(messages, result)
            if processed:
                self.get_logger().info(
                    f"after.md processed for '{meta.code}' → "
                    f"'{processed[:80]}...'"
                )
                return processed
        except Exception as e:
            self.get_logger().warning(
                f"after.md processing failed for '{meta.code}': {e}"
            )

        return result

    def __repr__(self):
        return self.__class__.__name__
