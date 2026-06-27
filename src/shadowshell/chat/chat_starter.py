#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.boot import Starter
from shadowshell.monitor import function_monitor
def callback(request, response):
    
    # logger = LoggerFactory.get_logger()  
    # logger.info(f"[CALLBACK][Request]{__serialize(request)}[Response]{__serialize(response)}")
    
    pass

def __serialize(obj):
    # return orjson.dumps(obj, default=lambda obj: obj.__dict__)
    # return orjson.dumps(obj)
    return obj

class_name = "ChatStarter"

class ChatStarter(Starter):

    def __init__(self, work_dir):
        super().__init__(work_dir)
 
    def __repr__(self):
        return self.__class__.__name__