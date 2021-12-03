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

 - Access to OpenApi documentation: http://0.0.0.0:8000/
 - Access to django-restframework GUI: http://0.0.0.0:8000/api/v1/
 - Access to django admin: http://0.0.0.0:8000/admin/

## Run tests
```bash
make test
```

## Run coding standards check
```bash
make pep8
```


## Run simple stress test
 - requires `requests`

When you have the app up and running run
 ```bash
python stress_test.py
```

 Eventually change concurrency of the celery worker:
 `SWARM_CONCURRENCY` variable in `environment/.env` file