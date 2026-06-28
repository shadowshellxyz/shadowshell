"""
@author: shadowshell<shadowshell@foxmail.com>
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathlib import Path
from shadowshell.chat.core.chat_starter import ChatStarter
from shadowshell.chat.core.action import ActionHandler, ActionHandlerMeta, ActionHandlerFactory

user_home = Path.home()
base_dir = f'{user_home}/shadowshell'

app_dir = f'{base_dir}/roomie-assets/chat/aicaller'
sop_path = f'{base_dir}/roomie-assets/sops/aicaller/0000@留存线索录房示例'


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

    action_handler_factory = ActionHandlerFactory()
    action_handler_factory.register("echo", EchoHandler)
    chat_starter = ChatStarter(app_dir=app_dir, sop_path=sop_path, action_handler_factory=action_handler_factory)
    chat_starter.chat('我不出租了')
    print()
