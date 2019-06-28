# -*- coding: utf-8 -*-
from exchange.broker import Broker

class StockSystem:
    def __init__(self):
        self._bkr = Broker()

    def start(self):
        self._bkr.start()

def main():
    system = StockSystem()
    system.start()

if __name__ == "__main__":
    main()
    
    