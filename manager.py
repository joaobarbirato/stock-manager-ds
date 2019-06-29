# -*- coding: utf-8 -*-

from exchange.user import Manager

def main():
    manager = Manager("IBOVESPA", "IBV", 30.00)
    manager.send_stock()

if __name__ == "__main__":
    main()
