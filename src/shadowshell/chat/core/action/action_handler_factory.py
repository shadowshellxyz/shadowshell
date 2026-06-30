#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ActionHandlerFactory interface.

@author: shadowshell<shadowshell@foxmail.com>
"""

from abc import ABC, abstractmethod
from typing import Any

from shadowshell.chat.core.action.action_handler import ActionHandler
from shadowshell.chat.core.action.model import ActionHandlerMeta


class ActionHandlerFactory(ABC):
    """
    Interface for creating and dispatching ActionHandler instances.

    Infrastructure dependencies (app_dir, llm_config) are injected at
    construction time by concrete implementations.  The factory methods
    only accept domain parameters (handler metadata, intent, context).

    Usage:
        factory = DefaultActionHandlerFactory(app_dir, llm_config)
        factory.register("custom", CustomHandler)
        result = factory.dispatch(metas, intent_code, context)

    @author: shadowshell<shadowshell@foxmail.com>
    """

    @abstractmethod
    def create(self, metas: list[ActionHandlerMeta]) -> list[ActionHandler]:
        """
        Create ActionHandler instances for the given metadata entries.

        Infrastructure dependencies (app_dir, llm_config) are held by the
        concrete factory instance.

        Args:
            metas:  List of ActionHandlerMeta objects parsed from actions.json.

        Returns:
            List of instantiated ActionHandler objects.

        Raises:
            ValueError: If a handler type is not registered.
        """
        ...

    @abstractmethod
    def register(self, handler_type: str, handler_class: type) -> None:
        """
        Register a new handler type.

        Args:
            handler_type:  Handler type identifier string.
            handler_class: ActionHandler subclass.

        Raises:
            TypeError: If handler_class does not implement ActionHandler.
        """
        ...

    # ── Lifecycle hooks (override in subclasses) ────────────────────────

    def _before_execute(
        self, meta: ActionHandlerMeta, intent_code: str, context: dict[str, Any]
    ) -> dict[str, Any] | None:
        """
        Hook called before each handler executes.

        Subclasses override this to inject additional context (e.g. from
        tree-node resources such as before.md).

        Args:
            meta:        ActionHandlerMeta for the current handler.
            intent_code: The resolved intent code.
            context:     Current execution context.

        Returns:
            Dict to merge into context, or None to leave context unchanged.
        """
        return None

    def _after_execute(
        self,
        meta: ActionHandlerMeta,
        intent_code: str,
        result: str,
        context: dict[str, Any],
    ) -> str | None:
        """
        Hook called after a handler produces a result.

        Subclasses override this to post-process the result (e.g. with
        tree-node resources such as after.md).

        Args:
            meta:        ActionHandlerMeta for the current handler.
            intent_code: The resolved intent code.
            result:      The raw result from handler.execute().
            context:     Execution context (including any _before_execute data).

        Returns:
            Post-processed result string, or None to discard.
        """
        return result

    # ── Template method ──────────────────────────────────────────────────

    def dispatch(
        self,
        metas: list[ActionHandlerMeta],
        intent_code: str,
        context: dict[str, Any],
    ) -> str | None:
        """
        Create handlers and execute them in order for the given intent.

        Execution pipeline per handler:
        1. _before_execute(meta, intent_code, context) → enrich context
        2. handler.execute(intent_code, enriched_context) → raw result
        3. _after_execute(meta, intent_code, raw_result, context) → final result

        Template method: create() is abstract; _before_execute / _after_execute
        are hooks with default no-op / pass-through implementations.

        Args:
            metas:       List of ActionHandlerMeta objects from actions.json.
            intent_code: The resolved intent code (out_code from the XoT tree).
            context:     Context dict forwarded to each handler (e.g. node, user_input).

        Returns:
            Concatenated final results joined by newlines, or None if no
            handler produced output.
        """
        handlers = self.create(metas)
        results = []
        for i, handler in enumerate(handlers):
            meta = metas[i]

            # 1. Before hook — may enrich context
            before_ctx = self._before_execute(meta, intent_code, context)
            exec_context = context
            if before_ctx:
                exec_context = {**context, **before_ctx}

            # 2. Execute handler
            result = handler.execute(intent_code, exec_context)

            # 3. After hook — may transform or discard result
            if result:
                final_result = self._after_execute(meta, intent_code, result, exec_context)
                if final_result:
                    results.append(final_result)

        return '\n'.join(results) if results else None
