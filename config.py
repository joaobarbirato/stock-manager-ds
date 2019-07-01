# -*- coding: utf-8 -*-

import json
from exchange.stock import Stock

"""
    MANAGER -> BROKER -> WORKERS -> MONITOR -> SUBSCRIBER
"""

NUM_WORKERS = 0
ADDR = '127.0.0.1'

BROKER_PORT = '9000'

BROKER_IN_PORT  =   '9630'
BROKER_OUT_PORT =   '9031'

MONITOR_PORT =   '9100'

SYSTEM_EXISTS_MONITOR = '9896'
SYSTEM_CREATE_MONITOR = '9897'
SYSTEM_UPDATE_PORT = '9898'
SYSTEM_LISTEN_PORT = '9899'
