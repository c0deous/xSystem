#!/usr/bin/env python
from bottle import route, run
import os
import commands
import httplib

print('[*] xSystem Controller Version 1.0')
print('[*] This program was written for (OS Name)')
#configuration

portnumber = 1238  #port that the program runs on. leave at 1237 if unsure.

debugapi = False   #useful if you are writing your own commands and functions

hostip = '0.0.0.0' #This allows you to make the server local only or make it accessible by a controller
				   #Keep on 0.0.0.0 to make it accessible by a controller
				   #Change to localhost if you want it to be local only

#hostnames ----- put hostnames and their ip addresses here
hostNames = {'mac-pro' : 'jessewallacemacpro.local', 'imac' : 'imac.local'}




#default commands
@route('/<hostname>/')
def hostnameinfo(hostname="localhost"):
    connection = httplib.HTTPConnection(hostname + ':1237')
    connection.request('GET', '/info')
    r1 = connection.getresponse()
    hostnameinfo = r1.read()
    return hostnameinfo
    connection.close()
    
@route('/<hostname>/<command>/<command1>')
def runhostcommand(hostname="localhost", command="/info", command1=""):
    connection = httplib.HTTPConnection(hostname + ':1237')
    connection.request('GET', '/' + command + '/' + command1)   
    r1 = connection.getresponse()
    agentreturn = r1.read()
    return agentreturn
    connection.close()

@route('/<hostname>/<command>')
def runhostcommand(hostname="localhost", command="/info"):
	connection = httplib.HTTPConnection(hostname + ':1237')
	connection.request('GET', '/' + command)   
	r1 = connection.getresponse()
	agentreturn = r1.read()
	return agentreturn
	connection.close()
	
run(host=hostip, port=portnumber, debug=debugapi)
