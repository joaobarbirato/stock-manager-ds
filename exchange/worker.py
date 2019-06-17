# -*- coding: utf-8 -*-

# from queue import Queue
import time
import zmq
import random
import sys
from config import ADDR, BROKER_OUT_PORT

class Worker:
    def __init__(self):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PULL)
        self._socket.connect("tcp://%s:%s" % (ADDR, BROKER_OUT_PORT))
        self._consumer_id = random.randrange(1,10005)

    def work(self):
        print ("I am consumer #%s" % (self._consumer_id))
        while True:
            work = self._socket.recv_json()
            data = work['num']
            result = { 'consumer' : self._consumer_id, 'num' : data}
            print (result)
        
      
