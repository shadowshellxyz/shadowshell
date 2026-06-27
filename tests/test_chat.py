
"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from pathlib import Path
user_home = Path.home()

from base_test import BaseTest
from src.shadowshell.chat.chatbot import ChatBot

work_dir = f'{user_home}/shadowshellxyz/roomie-assets/chat/aicaller'
conf_path = f'{user_home}/shadowshellxyz/.shadowshell/config/app.ini'
sop_path = f'{user_home}/shadowshellxyz/roomie-assets/sops/aicaller/0000@留存线索录房示例'
sop_name = '0000@留存线索录房示例'

chatbot = ChatBot(work_dir, conf_path, sop_path, sop_name)
chatbot.chat('我不出租了')

