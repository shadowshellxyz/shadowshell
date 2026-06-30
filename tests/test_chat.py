"""
@author: shadowshell<shadowshell@foxmail.com>
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pathlib import Path
from shadowshell.config import Configurator
from shadowshell.chat.common.llm_client import LlmConfig
from shadowshell.chat.core.chat_starter import ChatStarter
from shadowshell.chat.core.action.impl import LocalTreeActionHandlerFactory

current_dir = Path(__file__).parent.resolve()

app_dir = f'{current_dir.parent}/demo'
assets_dir = f'{current_dir.parent.parent}/roomie-assets'
action_handlers_dir = f'{assets_dir}/mcps/0000@shared'
sop_path = f'{assets_dir}/sops/assistant/100@聊天工作台'

if __name__ == "__main__":

    configurator = Configurator(f'{app_dir}/config/app.ini')
    llm_config = LlmConfig().build(configurator, "llm_chatbot")

    action_handler_factory = LocalTreeActionHandlerFactory(app_dir, llm_config)
    action_handler_factory.build(action_handlers_dir)

    chat_starter = ChatStarter(action_handler_factory, app_dir=app_dir,
                               llm_config=llm_config, sop_path=sop_path)
    chat_starter.chat('值班查询')
