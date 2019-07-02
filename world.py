# -*- coding: utf-8 -*-
from exchange.broker import Broker
from config import (ADDR, SYSTEM_LISTEN_PORT, SYSTEM_UPDATE_PORT, SYSTEM_CREATE_MONITOR, SYSTEM_EXISTS_MONITOR)
from threading import Thread
import zmq, json

class StockSystem:
    def __init__(self):
        self._bkr = Broker()
        self._stk_port = {}
        self._monitors = {}

        self._context = zmq.Context()
        self._socket_update = self._context.socket(zmq.REP)
        self._socket_update.bind("tcp://%s:%s" % (ADDR, SYSTEM_UPDATE_PORT))
        
        self._socket_listen = self._context.socket(zmq.REP)
        self._socket_listen.bind("tcp://%s:%s" % (ADDR, SYSTEM_LISTEN_PORT))

        self._worker_ports = range(9100, 9120)
        self._worker_index = 0

        self._socket_create_monitor = self._context.socket(zmq.REP)
        self._socket_create_monitor.bind("tcp://%s:%s" % (ADDR, SYSTEM_CREATE_MONITOR))

        self._socket_exists_monitor = self._context.socket(zmq.REP)
        self._socket_exists_monitor.bind("tcp://%s:%s" % (ADDR, SYSTEM_EXISTS_MONITOR))

    def _exists_monitor(self):
        while True:
            monitor_id = self._socket_exists_monitor.recv_string()
            print(self._monitors)
            print(monitor_id)
            if monitor_id in self._monitors:
                self._socket_exists_monitor.send_json({monitor_id: self._monitors[monitor_id]})
            else:
                self._socket_exists_monitor.send_json({"error": "Monitor does not exists"})

    def _create_monitor(self):
        while True:
            monitor_id = self._socket_create_monitor.recv_string()
            workers_port = []
            stock_id_list = monitor_id.split("_")
            if monitor_id not in self._monitors:
                for key in stock_id_list:
                    workers_port.append(self._stk_port[key])
                self._monitors[monitor_id] = workers_port
                self._socket_create_monitor.send_json({"success": "Monitor Created"})
            else:
                print("errei")
            #     self._socket_create_monitor.send_json({monitor_id: self._monitors[monitor_id]})


    def _update(self):
        while True:
            stock_id = self._socket_update.recv_string()
            new_port = self._worker_ports[self._worker_index]
            self._worker_index += 1
            self._stk_port[stock_id] = new_port

            print("[UPD]", self._stk_port)

            self._socket_update.send_string(str(new_port))
            
    def _listen(self):
        while True:
            raw_data = self._socket_listen.recv_multipart()
            ports = {}
            for stock_id in raw_data:
                if stock_id.decode() in self._stk_port:
                    ports[stock_id.decode()] = self._stk_port[stock_id.decode()]

            print("[LST]", self._stk_port)
            # raw_ports = [str(port).encode() for port in ports]
            print(ports)
            if ports:
                self._socket_listen.send_json(ports)
            else:
                self._socket_listen.send_json({'error': 'stock not found'})


    def start(self):
        thr_update_port = Thread(target=self._update)
        thr_listen_port = Thread(target=self._listen)

        thr_create_monitor = Thread(target=self._create_monitor)
        thr_exists_monitor = Thread(target=self._exists_monitor)

        thr_update_port.start()
        thr_listen_port.start()

        thr_create_monitor.start()
        thr_exists_monitor.start()

        self._bkr.start()

        thr_update_port.join()
        thr_listen_port.join()

def main():
    system = StockSystem()
    system.start()

if __name__ == "__main__":
    main()
