import abc
import struct

class RTCPPacket(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, data=None):
        if data is None:
            self.data = None
        else:
            self.decode(data)

    @abc.abstractmethod
    def decode(self, data):
        pass

    @abc.abstractmethod
    def encode(self):
        pass

class SDESPacket(RTCPPacket):
    def decode(self, data):
        self.data = data

    def encode(self):
        self.data = "encoded data"
