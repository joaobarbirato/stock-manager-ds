#-*- coding: utf-8 -*-
from exchange.worker import Worker
from threading import Thread

def main():

    worker_IBV = Worker("IBV")
    worker_DWJ = Worker("DWJ")
    worker_NDC = Worker("NDC")
    worker_FTS = Worker("FTS")
    worker_DXI = Worker("DXI")

    thread_IBV = Thread(target=worker_IBV.work)
    thread_DWJ = Thread(target=worker_DWJ.work)
    thread_NDC = Thread(target=worker_NDC.work)
    thread_FTS = Thread(target=worker_FTS.work)
    thread_DXI = Thread(target=worker_DXI.work)

    thread_IBV.start()
    thread_DWJ.start()
    thread_NDC.start()
    thread_FTS.start()
    thread_DXI.start()

    thread_IBV.join()
    thread_DWJ.join()
    thread_NDC.join()
    thread_FTS.join()
    thread_DXI.join()


    thr = Thread(target=worker2.work)
    thr.start()

    worker1.work()
    thr.join()

if __name__ == "__main__":
    main()