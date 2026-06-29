"""
@author: shadowshell<shadowshell@foxmail.com>
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathlib import Path
from shadowshell.chat.core.chat_starter import ChatStarter
from shadowshell.chat.common.llm_client import LlmConfig
from shadowshell.chat.core.action import ActionHandler, ActionHandlerMeta, ActionHandlerFactory
from shadowshell.chat.core.action.impl import LocalTreeActionHandlerFactory, ScriptGenerationHandler

user_home = Path.home()
base_dir = f'{user_home}/shadowshell'

app_dir = f'{base_dir}/shadowshell/demo'
# sop_path = f'{base_dir}/roomie-assets/sops/aicaller/0000@留存线索录房示例'
mcp_path = f'{base_dir}/roomie-assets/mcps/0000@shared'

# app_dir = f'{base_dir}/roomie-assets/chat/assistant'
sop_path = f'{base_dir}/roomie-assets/sops/assistant/100@聊天工作台'

# ── Demo 1: Define and register a custom ActionHandler ─────────────────

class EchoHandler(ActionHandler):
    """
    A simple echo handler for demo purposes.

    In a real business scenario, this would be a domain-specific handler
    like "send-message", "book-appointment", "check-inventory", etc.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    def __init__(self, app_dir, llm_config, meta: ActionHandlerMeta = None):
        self.meta = meta

    def execute(self, intent_code: str, context: dict) -> str:
        user_input = context.get("user_input", "")
        return f"[Echo:{self.meta.code}] Received: {user_input}"

    def handler_type(self) -> str:
        return "echo"

if __name__ == "__main__":

    action_handler_factory = LocalTreeActionHandlerFactory(app_dir)
    action_handler_factory.build(mcp_path)
    llm_config = LlmConfig().build(action_handler_factory.configurator, "llm_chatbot")
    action_handler_factory._llm_config = llm_config

    chat_starter = ChatStarter(action_handler_factory, app_dir=app_dir, sop_path=sop_path)
    chat_starter.chat('值班查询')
    print()
