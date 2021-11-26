# python-pdf2png-render [WIP]
Python PDF to PNG distributed rendering web app

## Stack
 - django
 - django-restframework
 - celery
 - postgresql
 - rabbitmq

See `Makefile` and `environment` folder for bigger picture .

## Prerequisites
```bash
sudo apt-get -y install make docker-compose
```

## Build the app
```bash
cd ./python-pdf2png-render
make build
```

## Run the app
```bash
make up
```

as daemon:
```bash
make upd
```

## Run tests
```bash
make test
```
