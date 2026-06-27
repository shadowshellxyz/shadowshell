#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

import pandas as pd

class DataSet():

    def __init__(self):
        pass

    def iterate_excel(self, file_path, sheet_name = None, callbacks = None):
        if callbacks is None:
            return
        
        df = pd.read_excel(file_path, sheet_name)
        
        for row in df.iterrows():
            for callback in callbacks:
                callback(row)

    