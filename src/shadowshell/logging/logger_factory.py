#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LoggerFactory
@author: shadowshell<shadowshell@foxmail.com>
"""

import ast
import logging
import logging.config
import os
from configparser import RawConfigParser

from .logging_logger import LoggingLogger
from .logging_constants import LoggingConstants

class LoggerFactory:

    @staticmethod
    def init():
        cp = RawConfigParser()
        cp.read(LoggingConstants.logging_conf_dir, encoding='utf-8')
        home = os.path.expanduser('~')
        for section in cp.sections():
            if cp.has_option(section, 'args'):
                args = cp.get(section, 'args')
                args = args.replace('~/', home + os.sep)
                cp.set(section, 'args', args)
                LoggerFactory._ensure_log_dir(args)
        logging.config.fileConfig(cp)
        LoggerFactory._initialized = True

    @staticmethod
    def _ensure_log_dir(args):
        try:
            parsed = ast.literal_eval(args)
            if isinstance(parsed, tuple) and len(parsed) > 0:
                log_path = parsed[0]
                if isinstance(log_path, str):
                    log_dir = os.path.dirname(log_path)
                    if log_dir:
                        os.makedirs(log_dir, exist_ok=True)
        except (ValueError, SyntaxError):
            pass

    @staticmethod
    def get_logger(name = 'root'):
        return LoggingLogger(logging.getLogger(name))
    
