#!/usr/bin/env python
from bottle import route, run, Bottle, ServerAdapter
import os
import commands
import httplib


print('[*] xSystem Agent Version 1.0')
if os.path.isfile('installerdone.note') == False:
    print('[-] You need to run "installer.py" in the agent folder first.')
    exit()
else:
    pass
print('[*] This program was written for (OS Name)')


# --------- Configuration -------------

portnumber = 1237  #port that the program runs on. leave at 1237 if unsure.

debugapi = False   #useful if you are writing your own commands and functions

hostip = '0.0.0.0' #This allows you to make the server local only or make it accessible by a controller
                   #Keep on 0.0.0.0 to make it accessible by a controller
                   #Change to localhost if you want it to be local only

saltfile = 'salt.salt' #put path to your "salt" file here.  This should be generated when you run the install script.
                       #must be exactly 8 digits

tempsalt = '12345678'
# ------ Config Setup Code ---------



salt = tempsalt
#-------- Encryption -------------
from pyDes import *

def encrypt(data, password,):
    k = des(password, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5,)
    d = k.encrypt(data,)
    return d
def decrypt(data, password,):
    k = des(password, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5,)
    d = k.decrypt(data,)
    return d


#--------- Default Commands ----------
@route('/harddisks')
def harddisks():
    cmd = commands.getstatusoutput('df -h')
    cmdEnc = encrypt(cmd, salt)
    return cmdEnc

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

#Note about custom commands and functions:
#currently xsystem only supports a maximum of two arguments in a request
#so you cannot currently do something like @route('/somearg/somearg/somearg')
#you could do something like @route('/somearg/somearg')
#DO NOT PUT A FORWARD SLASH AT THE END OF A REQUEST!!! It will cause all sorts of errors and it is generally easier to sort through if you leave a / off of the end.


# -------- Server Initiation ----------
run(host=hostip, port=portnumber, debug=debugapi)

# ---------- Cleanup Stuff on quit -----------
print('[*] Quitting...')