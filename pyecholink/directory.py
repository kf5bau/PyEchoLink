import socket
import time

class StationType:
    Node, Link, Repeater, Conference = range(1, 5)

class Station:
    def read(self, reader):
        self.callsign = reader.readline().strip()
        self.data = reader.readline().strip()
        self.node_id = reader.readline().strip()
        self.ip_address = reader.readline().strip()
        if self.callsign.endswith("-L"):
            self.station_type = StationType.Link
        elif self.callsign.endswith("-R"):
            self.station_type = StationType.Repeater
        elif self.callsign.startswith("*") and self.callsign.endswith("*"):
            self.station_type = StationType.Conference
        else:
            self.station_type = StationType.Node

class Directory(object):
    HOST = "servers.echolink.org"
    PORT = 5200

    def __init__(self, callsign, password):
        self.callsign = callsign
        self.password = password

    def online(self, description):
        self.__set_status("ONLINE3.38", description)

    def busy(self, description):
        self.__set_status("BUSY3.40", description)

    def offline(self):
        self.__set_status("OFF-V3.40", "Offline")

    def __set_status(self, status, description):
        localTime = time.strftime("%H:%M", time.localtime())
        self.__connect()
        self.socket.sendall(
                "l" + self.callsign + "\254\254" + self.password + "\r" + 
                status + 
                "(" + localTime + ")\n" + 
                description + 
                "\r")
        assert self.socket_file.readline().startswith("OK")
        self.__disconnect()

    def listing(self):
        self.__connect()
        self.socket.sendall("s\r")
        stations = []
        motd = ""
        assert self.socket_file.readline().startswith("@@@")
        count = int(self.socket_file.readline())
        for index in range(count):
            station = Station()
            station.read(self.socket_file)
            if not station.node_id:
                motd += station.data + "\n"
            else:
                stations.append(station)
        assert self.socket_file.readline().startswith("+++")
        self.__disconnect()
        return (motd, stations)

    def __connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        self.socket_file = self.socket.makefile()

    def __disconnect(self):
        self.socket.close()
