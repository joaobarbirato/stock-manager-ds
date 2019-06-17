# -*- coding: utf-8 -*-

import time
import zmq
import pdb
from zmq.devices.basedevice import ProcessDevice
from multiprocessing import Process
from config import (BROKER_IN_PORT, BROKER_OUT_PORT, ADDR)

class Broker:
    """
        'device' em https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/pyzmqdevices/streamer.html
    """
    def __init__(self):
        # pdb.set_trace()
        # self.streamerdevice  = ProcessDevice(zmq.STREAMER, zmq.PULL, zmq.PUSH)
        # self.streamerdevice.bind_in("tcp://%s:%s" % (ADDR, BROKER_IN_PORT))
        # self.streamerdevice.bind_out("tcp://%s:%s" % (ADDR, BROKER_OUT_PORT))
        # self.streamerdevice.setsockopt_in(zmq.IDENTITY, "PULL")
        # self.streamerdevice.setsockopt_out(zmq.IDENTITY, "PUSH")
        try:
            self._context = zmq.Context(1)
            # Socket facing clients
            self._frontend = self._context.socket(zmq.PULL)
            self._frontend.bind("tcp://%s:%s" % (ADDR, BROKER_IN_PORT))
            
            # Socket facing services
            self._backend = self._context.socket(zmq.PUSH)
            self._backend.bind("tcp://%s:%s" % (ADDR, BROKER_OUT_PORT))


        except Exception as e:
            print (e)
            print ("bringing down zmq device")
        

    def start(self):
        zmq.device(zmq.STREAMER, self._frontend, self._backend)
        # self.streamerdevice
        # time.sleep(20)
    
    def __del__(self):
        self._frontend.close()
        self._backend.close()
        self._context.term()

