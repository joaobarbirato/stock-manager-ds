#-*- coding: utf-8 -*-
from exchange.worker import Worker

def main():
    worker = Worker()
    worker.work()

if __name__ == "__main__":
    main()