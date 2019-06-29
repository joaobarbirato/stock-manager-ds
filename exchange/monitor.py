# -*- coding: utf-8 -*-

import zmq
import json
from exchange.stock import (Stock, create_stock_json, unmarshal)
from config import (ADDR, MONITOR_PORT)


class Monitor:
    """
        No momento, é basicamente um dict em python, mas criei a classe caso precise adicionar mais coisa
    """
    def __init__(self, stock_id_list):
        self._dict =  {}
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.SUB)
        self._socket.connect("tcp://%s:%s" % (ADDR, MONITOR_PORT))

        for id in stock_id_list:
            self._socket.setsockopt_string(zmq.SUBSCRIBE, id)
            self._dict[id] = {
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
                self._dict[obj.get_id()]['status'] = status

    def listen(self):
        print("Listening...")
        while True:
            [_id, d_stock] = self._socket.recv_multipart()
            stock = create_stock_json(unmarshal(d_stock))
            stock_id = _id.decode()
            self._update_stock(stock)
            print("[SUB] ID: %s, VAL: %s" % (stock.get_id(), stock.get_value()))

    def get_dict(self):
        return self._dict
