# -*- coding: utf-8 -*-

import zmq
import json
from exchange.stock import (Stock, create_stock_json, unmarshal)
from config import (ADDR, MONITOR_PORT, SYSTEM_LISTEN_PORT, SYSTEM_CREATE_MONITOR)
import random
import os
import signal

class Monitor:
    """
        No momento, é basicamente um dict em python, mas criei a classe caso precise adicionar mais coisa
    """
    def __init__(self, stock_id_list, port_list=None):
        self._id = -1
        self._dict =  {}
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.SUB)
        
        if port_list is None:
            _socket_register_monitor = self._context.socket(zmq.REQ)
            _socket_register_monitor.connect("tcp://%s:%s" % (ADDR, SYSTEM_CREATE_MONITOR))

            _socket_world = self._context.socket(zmq.REQ)
            _socket_world.connect("tcp://%s:%s" % (ADDR, SYSTEM_LISTEN_PORT))

            _socket_world.send_multipart([sid.encode() for sid in stock_id_list])
            self._ports = _socket_world.recv_json()

            if 'error' not in self._ports:
                print(self._ports)
                ordered_ids = list(self._ports.keys())
                ordered_ids.sort()
                self._monitor_id = "_".join(ordered_ids)
                _socket_register_monitor.send_string(self._monitor_id)
                
                for _, port in self._ports.items():
                    self._socket.connect("tcp://%s:%s" % (ADDR, port))

                for stock_id in stock_id_list:
                    self._socket.setsockopt_string(zmq.SUBSCRIBE, stock_id)
                    self._dict[stock_id] = {
                        "data": None,
                        "old": None,
                        "status": None
                    }
            else:
                print("Stocks don't exist :(")

        else:
            self._ports = port_list
            print(port_list)
            for port in port_list:
                print(port)
                self._socket.connect("tcp://%s:%s" % (ADDR, port))

            for stock_id in stock_id_list:
                self._socket.setsockopt_string(zmq.SUBSCRIBE, stock_id)
                self._dict[stock_id] = {
                    "data": None,
                    "old": None,
                    "status": None
                }

    def _update_stock(self, obj):
        if isinstance(obj, list):
            for stock in obj:
                self._update_stock(stock)

        if isinstance(obj, Stock):
            if self._dict[obj.get_id()]['data'] is None:
                self._dict[obj.get_id()]['data'] = obj
            else:
                old_val = self._dict[obj.get_id()]['data'].get_value()
                status = (obj.get_value() - old_val)*100 / old_val
                self._dict[obj.get_id()]['data'] = obj
                self._dict[obj.get_id()]['old'] = old_val
                if status != 0:
                    self._dict[obj.get_id()]['status'] = status

    def listen(self):
        if self._dict:
            print("Listening...")
            while True:
                [_id, d_stock] = self._socket.recv_multipart()
                stock = create_stock_json(unmarshal(d_stock))
                stock_id = _id.decode()
                self._update_stock(stock)
                self.show_in_terminal()

    def show_in_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("NAME\t\tVALUE\t\tVAR")
        print("------------------------------------")
        for key, value in self._dict.items():
            if value['data'] and value['status'] is not None:
                print("%s\t\t%.2f\t\t%.2f" % (key, value['data'].get_value(), value['status']))
        print()

    def get_dict(self):
        return self._dict
