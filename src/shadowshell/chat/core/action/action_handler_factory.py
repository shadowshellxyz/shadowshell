#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from shadowshell.chat.core.action.action_handler import ActionHandler
from shadowshell.chat.core.action.action_handler_meta import ActionHandlerMeta
from shadowshell.chat.core.action.impl.script_generation_handler import ScriptGenerationHandler


class ActionHandlerFactory:
    """
    Factory for creating ActionHandler instances by type identifier.

    Maintains a registry mapping handler type strings to ActionHandler
    subclasses. Supports runtime registration of new handler types.

    Usage:
        factory = ActionHandlerFactory()
        metas = [ActionHandlerMeta(type="script-generation", code="sg-001")]
        handlers = factory.create(metas, app_dir, llm_config)

    @author: shadowshell<shadowshell@foxmail.com>
    """

    def __init__(self):
        self._registry = {
            "script-generation": ScriptGenerationHandler,
        }

    def create(self, metas: list[ActionHandlerMeta], app_dir: str, llm_config) -> list[ActionHandler]:
        """
        Create ActionHandler instances for the given metadata entries.

        Args:
            metas:      List of ActionHandlerMeta objects parsed from actions.json.
            app_dir:    Working directory for file operations.
            llm_config: LlmConfig instance with base_url, api_key, model.

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
            handlers.append(handler_class(app_dir, llm_config, meta))
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
