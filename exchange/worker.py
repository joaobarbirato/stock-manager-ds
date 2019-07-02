# -*- coding: utf-8 -*-
import json
import time
import zmq
import random
import sys
from threading import Thread
from exchange.stock import (marshal, unmarshal, create_stock_json)
from config import (ADDR, BROKER_OUT_PORT, SYSTEM_UPDATE_PORT)

class Worker:
    """
        Worker object
        Every worker has one stock and one only
    """
    def __init__(self, stock_id=None):
        """
            :param stock_id: stock id to be responsible with
        """
        self._worker_id = random.randrange(1,10005)

        # BROKER -> WORKER
        self._context = zmq.Context()

        # Subscribe to a stock
        self._socket_in = self._context.socket(zmq.SUB)
        self._socket_in.connect("tcp://%s:%s" % (ADDR, BROKER_OUT_PORT))
        self._socket_in.setsockopt_string(zmq.SUBSCRIBE, stock_id)
        
        # Request-reply to give this worker a port
        _socket_world = self._context.socket(zmq.REQ)
        _socket_world.connect("tcp://%s:%s" % (ADDR, SYSTEM_UPDATE_PORT))

        _socket_world.send_string(stock_id)
        self._my_port = _socket_world.recv_string()

        # Publishes a stock for monitors
        self._socket_out = self._context.socket(zmq.PUB)
        self._socket_out.bind("tcp://%s:%s" % (ADDR, self._my_port))

        self._stock = None

    def _listen(self):
        """
            Receive stock updates
        """
        while True:
            [_, raw_data] = self._socket_in.recv_multipart()
            data = unmarshal(raw_data.decode())

            print("[WKR] Worker %s received %r" % (self._worker_id, data))
            self._stock = create_stock_json(data)

    def _update(self):
        """
            Send stock current state each at second
        """
        while True:
            if self._stock is not None:
                self._socket_out.send_multipart(
                    [str(self._stock.get_id()).encode(), marshal(self._stock)]
                )
            time.sleep(1)

    def work(self):
        """
            Main loop for running this worker
        """
        update_thr = Thread(target=self._update)

        update_thr.start()
        self._listen()

        update_thr.join()

        

        

        
      
