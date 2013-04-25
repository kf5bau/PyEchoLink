import atexit
import socket
import threading
import SocketServer

class ControlHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        """
        hread-2: ('178.235.247.143', 5199) wrote:
        ???CALLSIGNKF5BAU         CarCALLSIG3F4F5590E1.20P519D0
        """
        data = self.request[0]
        socket = self.request[1]
        cur_thread = threading.current_thread()
        print "{}: {} wrote:".format(cur_thread.name, self.client_address)
        print data

class ControlServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass

class Dispatcher():
    def __init__(self):
        HOST, PORT = "0.0.0.0", 5199
        self.__server = ControlServer((HOST, PORT), ControlHandler)
        self.__server_thread = threading.Thread(target=self.__server.serve_forever)
        self.__server_thread.daemon = True
        self.__server_thread.start()
        atexit.register(self.__server.shutdown)
