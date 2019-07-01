from exchange.user import Subscriber
from sys import argv

def main(stock=None):
    _stock="IBV"
    list_stock = []
    if len(stock) > 1:
        for i in range(1,len(stock)):
            list_stock.append(stock[i])
        
    m = Subscriber(stock_id_list=list_stock)
    m.listen()

if __name__ == "__main__":
    main(argv)