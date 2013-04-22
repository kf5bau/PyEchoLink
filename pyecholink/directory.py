import socket
import time

class Directory(object):
    HOST = "servers.echolink.org"
    PORT = 5200

    def __init__(self, callsign, password):
        self.callsign = callsign
        self.password = password

    def online(self):
        print ("going online")
        self.__set_status("ONLINE3.38", "Online")

    def busy(self):
        print ("going busy")
        self.__set_status("BUSY3.40", "Busy")

    def offline(self):
        print ("going offline")
        self.__set_status("OFF-V3.40", "Offline")

    def __set_status(self, status, description):
        localTime = time.strftime("%H:%M", time.localtime())
        self.__connect()
        self.socket.sendall("l" + self.callsign + "\254\254" + self.password + "\r" + status + "(" + localTime + ")\n" + description + "\r")
        print ("Status Response: " + self.socketFile.readline())
        self.__disconnect()

    def listing(self):
        print ("listing stations")
        self.__connect()
        self.socket.sendall("s\r")
        while 1:
            line = self.socketFile.readline()
            if not line:
                break
            else:
                print (line)
        self.__disconnect()

    def __connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        self.socketFile = self.socket.makefile()

    def __disconnect(self):
        self.socket.close()
