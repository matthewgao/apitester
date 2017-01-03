#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#Copyright 2015 Dell.Inc

import urllib.request
import ssl
import json

# This restores the same behavior as before.
class HTTPSender:

    def __init__(self):
        self.response = None
        self.request = None

    @classmethod
    def send(cls, url, values = None, method = 'GET', header={}):
        c = cls()
        data = None
        context = ssl._create_unverified_context()
        if values is not None:
            # data = urllib.parse.urlencode(values)
            # data = data.encode('utf-8') # data should be bytes           
            data = json.dumps(values)
            data = data.encode('utf-8')
        
        if data is None:
            c.request = urllib.request.Request(url)
        else:
            c.request = urllib.request.Request(url, data)
            c.request.add_header('Content-Type', 'application/json')
        for key, value in header.items():
            c.request.add_header(key,value)

        c.request.method = method
        # print(c.request.get_header('Content-Type'))
        try:
            c.response = urllib.request.urlopen(c.request, context=context)
        except urllib.error.HTTPError as e:
            c.response = e
            # print(e)

        return c
    
    @property
    def body(self):
        if self.response is None:
            return None
        return self.response.read().decode()

    @property
    def raw_body(self):
        if self.response is None:
            return None
        return self.response.read()

    @property
    def method(self):
        if self.request is None:
            return None
        
        return self.request.get_method()