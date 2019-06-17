# -*- coding: utf-8 -*-

import zmq
import time
from config import (ADDR, BROKER_IN_PORT)


class Subscriber:
    """
        ????
    """
    def __init__(self):
        pass

    def buy(self):
        pass

    def sell(self):
        pass
    pass

class Manager:
    def __init__(self):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUSH)
        self._socket.connect("tcp://%s:%s" % (ADDR, BROKER_IN_PORT))


    def request_stock_update(self, stock_id, stock_value):
        
        # Start your result manager and workers before you start your producers
        for num in range(20000):
            work_message = { 'num' : num }
            self._socket.send_json(work_message)
            time.sleep(1)
