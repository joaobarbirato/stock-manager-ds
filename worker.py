#-*- coding: utf-8 -*-
from exchange.worker import Worker
from threading import Thread

def main():
    worker1 = Worker("IBV")
    worker2 = Worker("PRT")

    thr = Thread(target=worker2.work)
    thr.start()

    worker1.work()
    thr.join()

if __name__ == "__main__":
    main()