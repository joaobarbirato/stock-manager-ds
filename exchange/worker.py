# -*- coding: utf-8 -*-

# from queue import Queue
import time
import zmq
from config import ADDR, BROKER_OUT_PORT

class Worker:
    def __init__(self):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PULL)
        self._socket.connect("tcp://%s:%s" % (ADDR, BROKER_OUT_PORT))
        
    def work(self):
        message = self._socket.recv()
        print("Worker #%s got message! %s oi :)" % (work_num, message))
        time.sleep(1)
      
