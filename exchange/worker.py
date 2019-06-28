# -*- coding: utf-8 -*-
import json
import time
import zmq
import random
import sys
from config import (ADDR, BROKER_OUT_PORT, MONITOR_PORT, marshal, unmarshal)

class Worker:
    def __init__(self):
        self._worker_id = random.randrange(1,10005)

        self._context_in = zmq.Context()
        self._socket_in = self._context_in.socket(zmq.PULL)
        self._socket_in.connect("tcp://%s:%s" % (ADDR, BROKER_OUT_PORT))
        
        self._context_out = zmq.Context()
        self._socket_out = self._context_out.socket(zmq.PUB)
        self._socket_out.bind("tcp://%s:%s" % (ADDR, MONITOR_PORT))

    def work(self):
        print ("I am consumer #%s" % (self._consumer_id))
        while True:
            # work = self._socket_in.recv()
            # data = work['num']
            # result = { 'consumer' : self._consumer_id, 'num' : data}
            # # self._socket_out.send_string("consumer %d %d" % (self._consumer_id, data))
            # self._socket_out.send_multipart([b'consumer', json.dumps(result).encode()])
            # print (result)
            data = unmarshal(self._socket_in.recv())
            topic = data['id']
            print("[WKR] Worker %s received %r" % (self._worker_id, data))
            self._socket_out.send_multipart([topic.encode(), marshal(data)])

        
      
