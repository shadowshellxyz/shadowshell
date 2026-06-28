

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# 确保路径添加在所有导入语句之前！

from src.shadowshell.logging.logger_factory import LoggerFactory
from src.shadowshell.logging.logging_constants import LoggingConstants

LoggingConstants.logging_conf_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/logging.conf'))
LoggerFactory.init()

class BaseTest():

    def __init__(self):
        pass
