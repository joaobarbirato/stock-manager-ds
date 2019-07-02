from exchange.user import Subscriber
from sys import argv

"""
To run this code use:

python3 subscriber.py username [stock1] [stock2] .. [stockN]

"""

def main(stock=None):
    # Setting default values
    user = "Guest"
    if stock is None:
        list_stock = ["IBV"]
    else:
        list_stock = []

    # Getting the username
    if len(stock) > 1:
        user = stock[1]

    # Getting which stocks it wants to monitor
    if len(stock) > 2:
        for i in range(2,len(stock)):
            list_stock.append(stock[i])
    
    # Creating the subscriber and start listening to this monitor
    m = Subscriber(stock_id_list=list_stock, username=user)
    m.listen()

if __name__ == "__main__":
    main(argv)