#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

from shadowshell.logging import LoggerFactory

class Xyz():

    def __init__(self):
        LoggerFactory.get_logger().info("xx24")
