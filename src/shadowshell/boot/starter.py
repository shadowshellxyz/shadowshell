#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.config import Configurator
from shadowshell.monitor import function_monitor
from shadowshell.logging import LoggerFactory
from shadowshell.serialize import SerializerFactory
from shadowshell.file import FileUtil

class_mame = "Starter"

class Starter:
    
    app_dir = None
    
    # @function_monitor(class_mame)
    def __init__(self, app_dir = None):
        if self.app_dir is None:
            if app_dir is not None:
                self.app_dir = app_dir
            else:
                self.app_dir = self.get_app_dir()
        self.__init_logging()
        self.get_logger().info(f"app_dir -->> {self.app_dir}")
        self.__init_configs()

    # @function_monitor(class_mame)
    def __init_logging(self):
        conf_path = self.get_logging_config_file_path()
        LoggerFactory.init(conf_path)
    
    # @function_monitor(class_mame)
    def get_logging_config_file_path(self):
        return f'{self.app_dir}/config/logging.conf'

    # @function_monitor(class_mame)
    def __init_configs(self):
        config_file_path = self.get_config_file_path()
        if config_file_path is not None: 
            self.configurator = Configurator(config_file_path)

    @function_monitor(class_mame)
    def get_app_dir(self):
        """获取工作目录"""
        return self.app_dir
    
    @function_monitor(class_mame)
    def get_config_file_path(self):
        """ 获取配置文件路径"""
        return f'{self.app_dir}/config/app.ini'
    
    # @function_monitor(class_mame)
    def get_file_content(self, file_name):
        return FileUtil.get_all(file_name)
    
    # @function_monitor(class_mame)
    def serialize(self, object):
        return SerializerFactory.get_instance().serialize(object)
    
    # @function_monitor(class_mame)
    def deserialize(self, text):
        return SerializerFactory.get_instance().deserialize(text)

    # @function_monitor(class_mame)
    def get_logger(self, logger_name = 'root'):
        return LoggerFactory.get_logger(logger_name)
    
    