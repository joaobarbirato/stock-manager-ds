from queue import Queue
from config import ADDR, MONITOR_OUT_PORT

class Worker:
    def __init__(self):
        self._context = zmq.Context()
        self._socket = context.socket(zmq.PULL)
        self._socket.connect("tcp://%s:%s" % (ADDR, MONITOR_OUT_PORT))

    def work(self):
        pass
