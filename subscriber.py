from exchange.user import Subscriber
from sys import argv

def main(stock=None):
    user = "Guest"
    if stock is None:
        list_stock = ["IBV"]
    else:
        list_stock = []

    if len(stock) > 1:
        user = stock[1]

    if len(stock) > 2:
        for i in range(2,len(stock)):
            list_stock.append(stock[i])
        
    m = Subscriber(stock_id_list=list_stock, username=user)
    m.listen()

if __name__ == "__main__":
    main(argv)