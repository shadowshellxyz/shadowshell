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
import threading
from configparser import RawConfigParser

from .logging_logger import LoggingLogger

_LOCK = threading.Lock()
_INITIALIZED = False


class LoggerFactory:

    @staticmethod
    def init(conf_path=None):
        """
        Initialize logging from a configuration file. Thread-safe; only the
        first call takes effect — subsequent calls are ignored.

        Args:
            conf_path: Path to the logging.conf file. If None, no-op.
        """
        global _INITIALIZED
        if conf_path is None:
            return
        with _LOCK:
            if _INITIALIZED:
                return
            _INITIALIZED = True

        cp = RawConfigParser()
        cp.read(conf_path, encoding='utf-8')
        home = os.path.expanduser('~')
        for section in cp.sections():
            if cp.has_option(section, 'args'):
                args = cp.get(section, 'args')
                args = args.replace('~/', home + os.sep)
                cp.set(section, 'args', args)
                LoggerFactory._ensure_log_dir(args)
        logging.config.fileConfig(cp)

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
    def get_logger(name='root'):
        return LoggingLogger(logging.getLogger(name))
