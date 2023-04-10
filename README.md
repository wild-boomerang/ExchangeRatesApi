# Exchange Rates API

This project is an API that retrieves and displays exchange rates from the [API](https://www.nbrb.by/apihelp/exrates) 
of the National Bank of the Republic of Belarus.

The project is written with [FastAPI](https://fastapi.tiangolo.com/) and [SQLAlchemy](https://www.sqlalchemy.org/) in a
fully asynchronous manner. [AIOHTTP](https://docs.aiohttp.org/en/stable/) is used for requests.

## Prerequisites

1. `docker compose`

## Local launch

1. Create `.env` from `.example.env`.
1. Launch the project with `docker compose` from the project root:
```shell script
docker compose up -d
```

The project is now available via these links: 
1. [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
1. Interactive API documentation is available [here](http://127.0.0.1:8000/docs) and an alternative 
[here](http://127.0.0.1:8000/redoc).
1. The raw OpenAPI schema can be found [here](http://127.0.0.1:8000/openapi.json).

## Usage notes

1. If you don't specify a date for the endpoints, today's date will be used.
1. To get a rate, you need to specify the internal currency code of nbrb api.
