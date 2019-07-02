# -*- coding: utf-8 -*-

from exchange.user import Manager
from sys import argv
from random import randint
from time import sleep
from threading import Thread

"""
To run this code use:

python3 manager.py

"""

# Function that update the manager's value randomly with a percentage (positive or negative)
def modify_value(manager):
    if isinstance(manager, Manager):
        while True:
            manager.send_stock()
            sleep(randint(1,5))
            manager.update_value(
                manager.get_curr_value()*(1. + (-1)**randint(1,2)*randint(1,20)/100)
            )


""" STOCK EXAMPLES

    Bovespa Index 
            101.339,68  +0,37%
    Dow Jones
            26.717,43   +0,44%
    Nasdaq Composite
            8.091,1624  +1,06%
    FTSE 100
            7.497,5 +0,97%
    DAX Index
            12.521,38   +0,99%
"""

def main(item):
    # Creating some examples of stocks
    manager_ibv = Manager("Bovespa Index", "IBV", 101339.68)
    manager_dwj = Manager("Dow Jones", "DWJ", 26717.43)
    manager_ndc = Manager("Nasdaq Composite", "NDC", 8091.1624)
    manager_fts = Manager("FTSE 100", "FTS", 7497.5)
    manager_dxi = Manager("DAX Index", "DXI", 12521.38)

    # Each stock will be constantly updated in a thread
    thread_ibv = Thread(target=modify_value, args=(manager_ibv,))
    thread_dwj = Thread(target=modify_value, args=(manager_dwj,))
    thread_ndc = Thread(target=modify_value, args=(manager_ndc,))
    thread_fts = Thread(target=modify_value, args=(manager_fts,))
    thread_dxi = Thread(target=modify_value, args=(manager_dxi,))

    thread_ibv.start()
    thread_dwj.start()
    thread_ndc.start()
    thread_fts.start()
    thread_dxi.start()

    thread_ibv.join()
    thread_dwj.join()
    thread_ndc.join()
    thread_fts.join()
    thread_dxi.join()

if __name__ == "__main__":
    main(argv)
