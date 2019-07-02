# -*- coding: utf-8 -*-

from json import (dumps, loads)

def create_stock_json(json):
    """
        Converts a JSON representation to a Stock object
    """
    return Stock(
        name=json["name"],
        id_stock=json["id"],
        val=json["value"]
    )

def marshal(stock):
    """
        Transforms an object into a byte JSON representation
        :param stock: Representation of a stock
    """
    if isinstance(stock, Stock):
        return marshal({
            "id": stock.get_id(),
            "name": stock.get_name(),
            "value": stock.get_value()
        })
    elif isinstance(stock, dict):
        return dumps(stock).encode()

def unmarshal(d_json):
    """
        Transforms an a byte JSON representation into a JSON representation
        :param stock: Representation of a stock
    """
    if isinstance(d_json, str):
        return loads(d_json)
    elif isinstance(d_json, bytes):
        return unmarshal(d_json.decode())

class Stock:
    def __init__(self, name, id_stock, val):
        """
            :param id_stock: Stock identifier
            :param name: Stock name
            :param val: Initial stock value
        """
        self._id = id_stock
        self._name = name
        self._val = val

    # Getters
    def get_name(self):
        return self._name

    def get_value(self):
        return self._val

    def set_value(self, new_value):
        self._val = new_value

    def get_id(self):
        return self._id

    def marshal(self):
        """
            Transforms this stock to to a byte JSON representation
        """
        return marshal(self)

    def __repr__(self):
        return "<Stock %r>" % self._name
