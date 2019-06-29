from exchange.monitor import Monitor

def main():
    m = Monitor(["IBV"])
    m.listen()

if __name__ == "__main__":
    main()