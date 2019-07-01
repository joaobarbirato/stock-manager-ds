# -*- coding: utf-8 -*-

from exchange.user import Manager
from sys import argv

def main(item):
    manager = Manager("IBOVESPA", "IBV", 30.00)
    if len(item) > 1:
        if item[1] == "1":
            manager = Manager("IBOVESPA", "IBV", 30.00)
        elif item[1] == "2":
            manager = Manager("PERALTA", "PRT", 0.01)

    manager.send_stock()

if __name__ == "__main__":
    main(argv)
