# -*- coding: utf-8 -*-

import zmq
import time
from config import (ADDR, BROKER_IN_PORT)
from exchange.monitor import Monitor
from exchange.stock import Stock


class Subscriber:
    """
        ????
    """
    def __init__(self, username, password, stock_id_list):
        self._id_list = stock_id_list
        self._monitor = Monitor(stock_id_list)

        self._username = username
        self._password = password
        self._online = False

    def login(self, username, password):
        if username == self._username and password == self._password and not self._online:
            self._online = True

    def logout(self):
        if self._online:
            self._online = False

    def buy(self):
        pass

    def sell(self):
        pass


class Manager:
    """
        Assuma que um acionista gerencia apenas uma ação
    """
    def __init__(self, stock_name, stock_id, stock_val):
        self._my_stock = Stock(name=stock_name, id_stock=stock_id, val=stock_val)
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUSH)
        self._socket.connect("tcp://%s:%s" % (ADDR, BROKER_IN_PORT))

    def update_value(self, stock_value):
        self._my_stock.set_value(stock_value)
        # Start your result manager and workers before you start your producers
        # for num in range(20000):
        #     work_message = {'num' : num}
        #     self._socket.send_json(work_message)
        #     time.sleep(1)

    def send_stock(self):
        self._socket.send(self._my_stock.marshal())
