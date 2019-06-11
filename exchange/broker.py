import time
import zmq
from zmq.devices.basedevice import ProcessDevice
from multiprocessing import Process
from config import (BROKER_IN_PORT, BROKER_OUT_PORT, ADDR)

class Broker:
    """
        'device' em https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/pyzmqdevices/streamer.html
    """
    def __init__(self):
        self.streamerdevice  = ProcessDevice(zmq.STREAMER, zmq.PULL, zmq.PUSH)
        self.streamerdevice.bind_in("tcp://%s:%s" % (ADDR, BROKER_IN_PORT))
        self.streamerdevice.bind_out("tcp://%s:%s" % (ADDR, BROKER_OUT_PORT))
        self.streamerdevice.setsockopt_in(zmq.IDENTITY, 'PULL')
        self.streamerdevice.setsockopt_out(zmq.IDENTITY, 'PUSH')

    def start(self):
        self.streamerdevice.start()

