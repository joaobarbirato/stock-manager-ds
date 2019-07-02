# -*- coding: utf-8 -*-

import zmq
import time
from config import (ADDR, BROKER_IN_PORT, SYSTEM_EXISTS_MONITOR)
from exchange.monitor import Monitor
from exchange.stock import Stock
from exchange.worker import Worker


class Subscriber:
    """
        Client that monitors stocks
        Every subscriber has one monitor and one only
    """
    def __init__(self, username=None, stock_id_list=None):
        """
            :param stock_id_list: list of stock IDs that this client wants to subscribe for
        """
        self._id_list = stock_id_list
        self._username = username
        self._context = zmq.Context()

        # Verify if a monitor exists
        _socket_exists_monitor = self._context.socket(zmq.REQ)
        _socket_exists_monitor.connect("tcp://%s:%s" % (ADDR, SYSTEM_EXISTS_MONITOR))
        stock_id_list.sort()

        _key = "_".join(stock_id_list)
        _socket_exists_monitor.send_string(_key)
        response_json = _socket_exists_monitor.recv_json()

        if not "error" in response_json:
            print("[SUB] Monitor exists")
            response_stock_id_list = list(response_json.keys())[0].split("_")
            self._monitor = Monitor(stock_id_list=response_stock_id_list, port_list=response_json[_key], username=self._username)
        else:
            print("[SUB] Creating monitor")
            self._monitor = Monitor(stock_id_list=stock_id_list, username=self._username)

    def listen(self):
        """
            Start monitor visualization
        """
        self._monitor.listen()


class Manager:
    """
        Stock manager.
        Every stock manager manages one stock and one only
    """
    def __init__(self, stock_name, stock_id, stock_val):
        """
            :param stock_val: Current value of a stock in dollars
        """
        self._my_stock = Stock(name=stock_name, id_stock=stock_id, val=stock_val)
        self._context = zmq.Context()

        # Pipeline connection to broker's input side (backend)
        self._socket = self._context.socket(zmq.PUSH)
        self._socket.connect("tcp://%s:%s" % (ADDR, BROKER_IN_PORT))

    def update_value(self, stock_value):
        """
            Update the current value of this manager's stock
            :param stock_value: new value for a stock
        """
        self._my_stock.set_value(stock_value)

    def get_curr_value(self):
        """
            Get stock's current value
        """
        return self._my_stock.get_value()

    def send_stock(self):
        """
            Send stock to broker
        """
        self._socket.send_multipart(
            [str(self._my_stock.get_id()).encode(), self._my_stock.marshal()]
            )
