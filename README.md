# Instrutions
Distributed Systems Project 2

## Authors
- João Gabriel Melo Barbirato [joaobarbirato](https://github.com/joaobarbirato)
- Renata Sarmet Smiderle Mendes [renatasarmet](https://github.com/renatasarmet)

## Before you begin,
adjust the server addr in `config.py`.

#### IMPORTANT: Files inside the `exchange` folder should not be run directly.

## Running

- On bash 1:
```bash
python world.py
```

- On bash 2:
```bash
python start_workers.py
```

- On bash 3:
```bash
python manager.py
```

- On bash > 4 
```bash
python subscriber.py username [stock_id]+
```

#### You can run as many subscribers as you want, you just need to specify in its parameters a username and which stocks you want to monitor
