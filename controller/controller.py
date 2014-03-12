#!/usr/bin/env python
from bottle import route, run
import os
import commands
import httplib

print ('[*] xSystem Controller Version 1.0')

@route('/<hostname>/')
def hostnameinfo(hostname="localhost"):
    connection = httplib.HTTPConnection(hostname + ':1237')
    connection.request('GET', '/info/')
    r1 = connection.getresponse()
    hostnameinfo = r1.read()
    return hostnameinfo
    connection.close()
    
@route('/<hostname>/<command>/<command1>')
def runhostcommand(hostname="localhost", command="/info/"):
    connection = httplib.HTTPConnection(hostname + ':1237')
    
    if command2 == "":
        connection.request('GET', '/' + command + '/')
    else:
        connection.request('GET', '/' + command + '/' + command1)
        
    r1 = connection.getresponse()
    agentreturn = r1.read()
    return agentreturn
    connection.close()

run(host='0.0.0.0', port=1238, debug=False)
