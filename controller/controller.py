#!/usr/bin/env python
from bottle import route, run, Bottle, ServerAdapter
import os
import commands
import httplib

print('[*] xSystem Controller Version 1.0')
if os.path.isfile('installerdone.note') == False:
    print('[-] You need to run "installer.py" in the agent folder first.')
    exit()
else:
    pass
print('[*] This program was written for (OS Name)')
#configuration

portnumber = 1238  #port that the program runs on. leave at 1238 if unsure.


hostip = '0.0.0.0' #This allows you to make the server local only or make it accessible by a controller
                   #Keep on 0.0.0.0 to make it accessible by a controller
                   #Change to localhost if you want it to be local only

authtype = 'controller' #Allows you to choose what kind of authentication to use
                        #Authentication Types: controller, none
                        #Controller [Normal Security] lets you have a single password to use to access any agent computer
                        #None [No Security] has no password for anything (not reccomended)
saltfile = 'salt.salt'

salt = '12345678'

#-------hostnames-------
#put hostnames and their ip addresses here
#Format: 'friendlyname' : 'ip',
hostNames = {

'localhost' : 'localhost', 
'mac-pro' : '192.168.0.108', 
'imac' : '192.168.0.106',
'osxserver' : '192.168.0.100',
'router' : '192.168.0.1'

}

#----- Config Setup Code -----
if authtype == 'controller':
    def xsystemAuth(password):
        if password == 'lamepass':
            print(True)
        else:
            print(False)
if authtype == 'none':
    def xsystemAuth():
        print(True)

#------ SSL Stuff ------
class SSLWSGIRefServer(ServerAdapter):
    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        import ssl
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        srv = make_server(self.host, self.port, handler, **self.options)
        srv.socket = ssl.wrap_socket (
            srv.socket,
            certfile='server.pem',  # path to certificate
            server_side=True)
        srv.serve_forever()

# ------- Encryption ---------
from pyDes import *

def encrypt(data, password):
    k = des(password, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    d = k.encrypt(data)
    return d
def decrypt(data, password):
    k = des(password, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
    d = k.decrypt(data)
    return d

#--------- Default Commands ------------
@route('/<hostname>/')
def hostnameinfo(hostname="localhost"):
    try:
        hostnameip = hostNames[hostname]
    except KeyError:
        return 'Hostname "' + hostname + '" is not in hostname list.'
    except:
        return 'Unexpected error with hostnames list'
    else:
        try:
            connection = httplib.HTTPConnection(hostnameip + ':1237')
            connection.request('GET', '/info')
        except:
            return 'unexpected internal server error 500'
        else:
            r1 = connection.getresponse()
            hostnameinfo = r1.read()
            hostnameinfoDec = decrypt(hostnameinfo, salt)
            return hostnameinfoDec
            connection.close()
    
@route('/<hostname>/<command>/<command1>')
def runhostcommand(hostname="localhost", command="/info", command1=""):
    try:
        hostnameip = hostNames[hostname]
    except KeyError:
        return 'Hostname "' + hostname + '" is not in hostname list.'
    except:
        return 'Unexpected error with hostnames list'
    else:
        try:
            connection = httplib.HTTPConnection(hostnameip + ':1237')
            connection.request('GET', '/' + command + '/' + command1)
        except:
            return 'Unexpected internal server error 500'
        else:
            r1 = connection.getresponse()
            agentreturn = r1.read()
            agentreturnDec = decrypt(agentreturn, salt)
            return agentreturnDec
            connection.close()

@route('/<hostname>/<command>')
def runhostcommand(hostname="localhost", command="/info"):
    try:
        hostnameip = hostNames[hostname]
    except KeyError:
        return 'Hostname "' + hostname + '" is not in hostname list.'
    except:
        return 'Unexpected error with hostnames list'
    else:
        try:
            connection = httplib.HTTPConnection(hostnameip + ':1237')
            connection.request('GET', '/' + command)
        except:
            return 'Unexpected internal server error 500'
        else:
            r1 = connection.getresponse()
            agentreturn = r1.read()
            agentreturnDec = decrypt(agentreturn, salt)
            return agentreturnDec
            connection.close()
#---------- Custom Commands and Functions -------------
#DO NOT PUT A FORWARD SLASH AT THE END OF A REQUEST!!! It will cause all sorts of errors and it is generally easier to sort through if you leave a / off of the end.


#------ Server Initiation ------    
srv = SSLWSGIRefServer(host=hostip, port=portnumber)
run(server=srv)

#------- Cleanup Stuff on quit ------
print('[*] Quitting...')