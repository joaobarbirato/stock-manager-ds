#-*- coding: utf-8 -*-
from exchange.worker import Worker
from threading import Thread

"""
To run this code use:

python3 start_workers.py

"""

def main():
    # Each stock has a worker 
    # Creating workers for our examples
    worker_IBV = Worker("IBV")
    worker_DWJ = Worker("DWJ")
    worker_NDC = Worker("NDC")
    worker_FTS = Worker("FTS")
    worker_DXI = Worker("DXI")

    # Each worker will be running in a thread
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


if __name__ == "__main__":
    main()