#!/usr/bin/env python
from bottle import route, run
import os
import commands
import httplib

print('[*] xSystem Agent Version 1.0')

#import plugins
import xsystemplugins


#default commands
@route('/harddisks')
def harddisks():
    cmd = commands.getstatusoutput('df -h')
    return cmd

@route('/info/')
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

run(host='0.0.0.0', port=1237, debug=False)