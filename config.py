# -*- coding: utf-8 -*-

import json
from exchange.stock import Stock

"""
    MANAGER -> BROKER -> WORKERS -> MONITOR -> SUBSCRIBER
"""

NUM_WORKERS = 0
ADDR = '127.0.0.1'
BROKER_IN_PORT  =   '9010'
BROKER_OUT_PORT =   '9030'

MONITOR_PORT =   '9110'
# MONITOR_OUT_PORT =  '9130'

# def marshal(stock):
#     if isinstance(stock, Stock):
#         return json.dumps({
#             "id": stock.get_id(),
#             "name": stock.get_name(),
#             "value": stock.get_value(),
#             "old_value": stock.get_old_value()
#         }).encode()

# def unmarshal(d_json):
#     if isinstance(d_json, dict):
#         return json.loads(d_json)

