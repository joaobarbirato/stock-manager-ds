# -*- coding: utf-8 -*-

import zmq
import json
from exchange.stock import (Stock, create_stock_json, unmarshal)
from config import (ADDR, SYSTEM_LISTEN_PORT, SYSTEM_CREATE_MONITOR)
import random
import os
import signal

class Monitor:
    """
        Stock monitor
    """
    def __init__(self, stock_id_list, port_list=None, username='Guest'):
        """
            :param stock_id_list: list of stock identifiers the monitor wants to keep track
            :param port_list: (optional) list of ports for an existing monitor
            :param username: (optional) subscriber's username
        """
        self._id = -1

        self._dict =  {}    # Contains all subscribed stocks informations
        self._context = zmq.Context()

        # Monitor subscribing to broker's backend
        self._socket = self._context.socket(zmq.SUB)
        self._username = username
        
        if port_list is None:
            # Routine for creating a monitor

            # Request-reply for creating a monitor
            _socket_register_monitor = self._context.socket(zmq.REQ)
            _socket_register_monitor.connect("tcp://%s:%s" % (ADDR, SYSTEM_CREATE_MONITOR))

            # Request-reply for getting all stock-worker port relations
            _socket_world = self._context.socket(zmq.REQ)
            _socket_world.connect("tcp://%s:%s" % (ADDR, SYSTEM_LISTEN_PORT))

            _socket_world.send_multipart([sid.encode() for sid in stock_id_list])
            self._ports = _socket_world.recv_json()

            if 'error' not in self._ports:
                # At least one subscribed port exists
                ordered_ids = list(self._ports.keys())
                ordered_ids.sort()
                self._monitor_id = "_".join(ordered_ids)

                # Register a monitor to system
                _socket_register_monitor.send_string(self._monitor_id)
                
                for _, port in self._ports.items():
                    self._socket.connect("tcp://%s:%s" % (ADDR, port))

                # Subscribe to all stock IDs
                for stock_id in ordered_ids:
                    self._socket.setsockopt_string(zmq.SUBSCRIBE, stock_id)
                    self._dict[stock_id] = {
                        "data": None,           # Stock object
                        "old": None,            # Old value
                        "variation": None          # Variation in %
                    }
            else:
                # Neither of the subscribed ports exists
                print("[MNT] Stocks don't exist :(")

        else:
            # Routine for reusing an existing monitor
            # (uses the same stock-worker port relation)

            self._ports = port_list
            for port in port_list:
                self._socket.connect("tcp://%s:%s" % (ADDR, port))
            
            # Subscribe to all stock IDs
            for stock_id in stock_id_list:
                self._socket.setsockopt_string(zmq.SUBSCRIBE, stock_id)
                self._dict[stock_id] = {
                    "data": None,
                    "old": None,
                    "variation": None
                }

    def _update_stock(self, obj):
        """
            Create/Updates an existing stock
            :param obj: Stock object (or a list of stocks)
        """
        if isinstance(obj, list):
            for stock in obj:
                self._update_stock(stock)

        if isinstance(obj, Stock):
            if self._dict[obj.get_id()]['data'] is None:
                self._dict[obj.get_id()]['data'] = obj
            else:
                old_val = self._dict[obj.get_id()]['data'].get_value()
                variation = (obj.get_value() - old_val)*100 / old_val
                self._dict[obj.get_id()]['data'] = obj
                self._dict[obj.get_id()]['old'] = old_val
                if variation != 0:
                    self._dict[obj.get_id()]['variation'] = variation

    def listen(self):
        """
            Main loop of listening stocks updates
        """
        if self._dict:
            print("Listening...")
            while True:
                [_id, d_stock] = self._socket.recv_multipart()
                stock = create_stock_json(unmarshal(d_stock))
                stock_id = _id.decode()
                self._update_stock(stock)
                
                # Visualize updates
                self.show_in_terminal()

    def show_in_terminal(self):
        """
            Visualize updates on console
        """
        no_dash = 36
        os.system('cls' if os.name == 'nt' else 'clear')
        print("USERNAME: %s" % (self._username))
        print("Monitoring: %s;" % (", ".join(list(self._dict.keys()))))
        print("-"*no_dash)
        print("NAME\t\tVALUE\t\tVAR")
        print("-"*no_dash)
        for key, value in self._dict.items():
            if value['data'] and value['variation'] is not None:
                l1 = len("$ %.2f" %  value['data'].get_value())
                if value['variation'] < 0:
                    l2 = len("%.2f%%" % value['variation'])
                    _white_space = no_dash - l1 - len(key) - 13 - l2
                    print("%s\t\t$ %.2f%s%2.2f%%" % (key, value['data'].get_value(), " "*_white_space, value['variation']))
                else:
                    l2 = len("+%.2f%%" % value['variation'])
                    _white_space = no_dash - l1 - len(key) - 13 - l2
                    print("%s\t\t$ %.2f%s+%2.2f%%" % (key, value['data'].get_value(), " "*_white_space, value['variation']))
        print()

    def get_dict(self):
        return self._dict
