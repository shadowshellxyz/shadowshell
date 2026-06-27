#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: shadowshell<shadowshell@foxmail.com>
"""

import requests

class Request():

    def __init__(self):
        pass

    def post(self, url, headers, data):
        response = requests.request('POST', url, headers = headers, data = data)
        return response
        
