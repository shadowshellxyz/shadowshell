#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.config import Configurator
from shadowshell.logging import LoggerFactory
from shadowshell.serialize import SerializerFactory
from shadowshell.file import FileUtil


class Starter:
    """
    Base class providing app_dir, logging, config, serialization, and file utilities.

    Each instance holds its own app_dir — no shared class-level state.

    @author: shadowshell<shadowshell@foxmail.com>
    """

    def __init__(self, app_dir=None):
        self.app_dir = app_dir
        self._init_logging()
        self._init_configs()

    def _init_logging(self):
        conf_path = self.get_logging_config_file_path()
        LoggerFactory.init(conf_path)

    def get_logging_config_file_path(self):
        return f'{self.app_dir}/config/logging.conf'

    def _init_configs(self):
        config_file_path = self.get_config_file_path()
        if config_file_path is not None:
            self.configurator = Configurator(config_file_path)

    def get_config_file_path(self):
        return f'{self.app_dir}/config/app.ini'

    def get_file_content(self, file_name):
        return FileUtil.get_all(file_name)

    def serialize(self, object):
        return SerializerFactory.get_instance().serialize(object)

    def deserialize(self, text):
        return SerializerFactory.get_instance().deserialize(text)

    def get_logger(self, logger_name='root'):
        return LoggerFactory.get_logger(logger_name)
