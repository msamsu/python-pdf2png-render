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

or as a daemon:
```bash
make upd
```

- Access to API (and django-restframework devel GUI): http://0.0.0.0:8000/api/v1/
- Access to OpenAPI documentation: http://0.0.0.0:8000/
- Access to django admin: http://0.0.0.0:8000/admin/

There is only one endpoint: http://0.0.0.0:8000/api/v1/works/ . It supports GET and POST methods.
GET lists present works.
Each work then can be found on its own url  http://0.0.0.0:8000/api/v1/works/:work_id:/ .

Exemple output:
 ```json
{
    "id": 1,
    "pdf_file": "http://0.0.0.0:8000/media/works/pdf/98/982bdb5a-d6b3-4b9f-931d-eafead59f42f.pdf",
    "orig_pdf_name": "Curriculum vitae.pdf",
    "status": "done",
    "page_count": 2,
    "created_at": "2021-12-01T11:43:00.957088Z",
    "work_started_at": "2021-12-02T21:31:35.729884Z",
    "done_at": "2021-12-02T21:31:36.699599Z",
    "pages_rendered": [
        "http://0.0.0.0:8000/media/works/png/62/62e96a64-b73a-4161-ab9e-524fd4a79882.png",
        "http://0.0.0.0:8000/media/works/png/0b/0b089c62-b8c0-431d-af26-011d6de4becd.png"
    ],
    "pages_text": [
        "Curriculum vitae\nPython backend developer",
        "Preferences\npython / django"
    ]
}
```
Field `status` enumerates to three values:
- `create` when work gets uploaded
- `done` when it is processed by celery worker
- `error` when worker failed to process the work

## Run tests and coverage
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
python stress_test.py 1000  # for more api calls
```

 Eventually change concurrency of the celery worker:
 `SWARM_CONCURRENCY` variable in `environment/.env` file