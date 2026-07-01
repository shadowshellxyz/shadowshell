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
from shadowshell.chat.core.action.impl import ScriptGenerationHandler
from shadowshell.chat.core.action.factory.impl import LocalTreeActionHandlerFactory
from shadowshell.test import Testee, Tester, CartesianProductTestCaseBuilder

current_dir = Path(__file__).parent.resolve()

app_dir = f'{current_dir.parent}/demo'
assets_dir = f'{current_dir.parent.parent}/roomie-assets'
action_handlers_dir = f'{assets_dir}/mcps/0000@shared'
sop_path = f'{assets_dir}/sops/aicaller/0000@root'

class ChatTest:

    def __init__(self, app_dir=None):
        self._app_dir = app_dir

    def chat(self, question):
        configurator = Configurator(f'{app_dir}/config/app.ini')
        llm_config = LlmConfig().build(configurator, "llm_chatbot")

        action_handler_factory = LocalTreeActionHandlerFactory(app_dir, llm_config)
        action_handler_factory.build(action_handlers_dir)

        action_handler_factory.register("script-generation", ScriptGenerationHandler)

        chat_starter = ChatStarter(action_handler_factory, app_dir=app_dir,
                                   llm_config=llm_config, sop_path=sop_path)
        chat_starter.chat(question)

ChatTest(app_dir).chat('我不出租啦')

