#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

import csv

from pathlib import Path
from shadowshell.logging import LoggerFactory
from shadowshell.monitor import function_monitor

class FileUtil:

    __logger = LoggerFactory.get_logger()

    @staticmethod
    def get_all(file_path, mode = 'r', encoding = 'utf-8'):
        path = Path(file_path)
        if path.is_file() == False:
            FileUtil.__logger.warn(f'File is not exists: {file_path}')
            return None
        with open(file_path, mode, encoding = encoding) as f:
            content = f.read()
        FileUtil.__logger.info(f'[{file_path}][All content]{content}')
        return content
    
    @staticmethod
    def read_csv_to_list(file_path, mode = 'r', encoding = 'utf-8'):
        """
        读取CSV文件，返回一个列表，每个元素是文件中的一行（也是一个列表）
        """
        data_array = []
        
        # 注意指定文件编码
        with open(file_path, mode = mode, encoding = encoding) as file:  
            # 创建csv读取器对象
            csv_reader = csv.reader(file)

            for row in csv_reader:
                data_array.append(row[0])
        
        return data_array