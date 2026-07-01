#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Default implementation of ActionHandlerFactory.

@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.chat.common.llm_client import LlmConfig
from shadowshell.chat.core.action.action_handler import ActionHandler
from shadowshell.chat.core.action.model import ActionHandlerMeta
from shadowshell.chat.core.action.factory.action_handler_factory import ActionHandlerFactory


class DefaultActionHandlerFactory(ActionHandlerFactory):
    """
    Default concrete implementation of ActionHandlerFactory.

    Maintains an empty registry at construction time.  All handler types
    must be explicitly registered via register() before calling create().

    Infrastructure dependencies (app_dir, llm_config) are injected at construction
    time rather than passed to each method call.

    Usage:
        factory = DefaultActionHandlerFactory(app_dir, llm_config)
        factory.register("script-generation", ScriptGenerationHandler)
        metas = [ActionHandlerMeta(name="script-gen", code="sg-001", type="script-generation")]
        handlers = factory.create(metas)

    @author: shadowshell<shadowshell@foxmail.com>
    """

    def __init__(self, app_dir: str, llm_config: LlmConfig):
        """
        Args:
            app_dir:    Working directory for file operations.
            llm_config: LlmConfig instance with base_url, api_key, model.
        """
        self._app_dir = app_dir
        self._llm_config = llm_config
        self._registry = {}

    def create(self, metas: list[ActionHandlerMeta]) -> list[ActionHandler]:
        """
        Create ActionHandler instances for the given metadata entries.

        Args:
            metas:  List of ActionHandlerMeta objects parsed from actions.json.

        Returns:
            List of instantiated ActionHandler objects.

        Raises:
            ValueError: If a handler type is not registered.
        """
        handlers = []
        for meta in metas:
            handler_class = self._registry.get(meta.type)
            if handler_class is None:
                raise ValueError(
                    f"Unknown handler type: '{meta.type}'. "
                    f"Registered types: {list(self._registry.keys())}"
                )
            handlers.append(handler_class(self._app_dir, self._llm_config, meta))
        return handlers

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
