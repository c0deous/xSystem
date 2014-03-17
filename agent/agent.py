#!/usr/bin/env python
from bottle import route, run
import os
import commands
import httplib

print('[*] xSystem Agent Version 1.0')
print('[*] This program was written for (OS Name)')

#configuration

portnumber = 1237  #port that the program runs on. leave at 1237 if unsure.

debugapi = False   #useful if you are writing your own commands and functions

hostip = '0.0.0.0' #This allows you to make the server local only or make it accessible by a controller
				   #Keep on 0.0.0.0 to make it accessible by a controller
				   #Change to localhost if you want it to be local only







#default commands
@route('/harddisks')
def harddisks():
    cmd = commands.getstatusoutput('df -h')
    return cmd

@route('/info')
def info():
    cmd = commands.getstatusoutput('uptime')
    return cmd

@route('/interfaces')
def ifconfig():
    cmd = commands.getstatusoutput('ifconfig')
    return cmd

@route('/interface/<interface>')
def ifconfig2(interface=""):
    cmd = commands.getstatusoutput('ifconfig ' + interface)
    return cmd

#Custom functions and commands go below this line




run(host=hostip, port=portnumber, debug=debugapi)
print('[*] Quitting...')