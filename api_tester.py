#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#Copyright 2015 Dell.Inc

import urllib.request
import ssl
import json

# This restores the same behavior as before.


BASE_PATH = 'https://10.103.240.219'

START_LOGON = BASE_PATH + "/__api__/v1/logon"

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
            print(e)

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

if __name__ == '__main__':
    resp = HTTPSender.send(START_LOGON, values = {'method': 144}, method = 'POST')
    # print(resp.method)
    logon_result = json.loads(resp.body)
    print(logon_result)

    resp = HTTPSender.send(BASE_PATH + logon_result['location'] + '/agentinfo', method = 'GET')
    # print(resp.method)
    result = json.loads(resp.body)
    print(result)

    resp = HTTPSender.send(BASE_PATH + logon_result['location'] + '/agentinfo',
                                values = {'win': True}, method = 'POST')
    print(resp.body)

    resp = HTTPSender.send(BASE_PATH + logon_result['location'] + '/authenticate',
                                values = {}, method = 'POST')
    print(resp.body)

    resp = HTTPSender.send(BASE_PATH + logon_result['location'] + '/authenticate',
                                values = {'button' : 'ok', 'replies' : ['local','password']}, 
                                method = 'POST')
    print(resp.body)

    resp = HTTPSender.send(BASE_PATH + logon_result['location'] + '/interrogation',
                                method = 'GET')
    print(resp.body)
    val =  {    
        "client_info" :{  
                    'user': 1,
                    'user_home_directory':'C:\\Users\\shgao\\AppData',
                    'system_directory' : 'C:\\Windows\\system32',
                    'x64' : False,
                    'client_type':'CT'
        },
        'interrogation_info' :{
                    'AV1444922987988AFJ': True,
                    'AV1444922987988AFK' : True,
                    'AV1444922987988AFI' : False
        }
    }

    resp = HTTPSender.send(BASE_PATH + logon_result['location'] + '/interrogation',
                                values = val, 
                                method = 'POST', header={'User-Agent':'SONICWALL'})
    print(resp.body)