import socket
import time

class StationType:
    Node, Link, Repeater, Conference = range(1, 5)

class Station:
    def read(self, reader):
        self.callsign = reader.readline()[:-1]
        self.data = reader.readline()[:-1]
        self.node_id = reader.readline()[:-1]
        self.ip_address = reader.readline()[:-1]
        if self.callsign.endswith("-L"):
            self.station_type = StationType.Link
        elif self.callsign.endswith("-R"):
            self.station_type = StationType.Repeater
        elif self.callsign.startswith("*") and self.callsign.endswith("*"):
            self.station_type = StationType.Conference
        else:
            self.station_type = StationType.Node

class StationList:
    stations = []

    def append(self, station):
        self.stations.append(station)

    def nodes(self):
        return self.__filter(StationType.Node)

    def links(self):
        return self.__filter(StationType.Link)

    def repeaters(self):
        return self.__filter(StationType.Repeater)

    def conferences(self):
        return self.__filter(StationType.Conference)

    def __filter(self, station_type):
        return [station for station in self.stations if station.station_type == station_type]

class Directory(object):
    HOST = "servers.echolink.org"
    PORT = 5200

    def __init__(self, callsign, password):
        self.callsign = callsign
        self.password = password

    def online(self, description="Online"):
        """Register the station 'online' with the directory server.

        Keyword arguments:
        description -- the 'comment' to show to other stations (default 'Online')

        """
        self.__set_status("ONLINE3.38", description)

    def busy(self, description="Busy"):
        """Register the station as 'busy' with the directory server.

        Keyword arguments:
        description -- the 'comment' to show to other stations (default 'Busy')

        """
        self.__set_status("BUSY3.40", description)

    def offline(self):
        """Tell the directory server the station is 'offline'"""
        self.__set_status("OFF-V3.40", "Offline")

    def __set_status(self, status, description):
        localTime = time.strftime("%H:%M", time.localtime())
        self.__connect()
        self.socket.sendall(
                "l" + self.callsign + "\254\254" + self.password + "\r" + 
                status + 
                "(" + localTime + ")\n" + 
                description + 
                "\r"
        )
        assert self.__socket_file.readline().startswith("OK")
        self.__disconnect()

    def listing(self):
        """List all stations registered with the directory server.
        
        Returns a tuple of ('motd', 'station_list')
        
        """
        self.__connect()
        self.socket.sendall("s\r")
        stations = StationList()
        motd = ""
        assert self.__socket_file.readline().startswith("@@@")
        count = int(self.__socket_file.readline())
        for index in range(count):
            station = Station()
            station.read(self.__socket_file)
            if station.ip_address == "127.0.0.1":
                motd += station.data + "\n"
            else:
                stations.append(station)
        assert self.__socket_file.readline().startswith("+++")
        self.__disconnect()
        return (motd, stations)

    def __connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))
        self.__socket_file = self.socket.makefile()

    def __disconnect(self):
        self.socket.close()
