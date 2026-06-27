#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SerializerFactory

@author: shadowshell<shadowshell@foxmail.com>
"""

from .serializer_json import SerializerJson

class SerializerFactory():

    def __init__(self):
        pass
    
    @staticmethod
    def get_instance():
        return SerializerJson()
    

