# Assignment

The HTTP-based API described in the task was developed in Python using
as little framework facilities as possible (whilst keeping viability) in 
order to show SQL and general coding knowledge.

# Initial setup

## Database

The Docker setup provided was used, so the same instructions apply
to fire up the PostgreSQL database.

Build the image:

```bash
docker build -t ratestask .
```

Create the container for image *ratestask*:

```bash
docker run -p 0.0.0.0:5432:5432 --name ratestask ratestask
```

## Web server

Python was used to create the server(as it is more familiar to Xeneta's team),
so first we need to install dependencies.

Activate venv:

```bash
$ python3 -m venv venv
$ . venv/bin/activate
```

Install dependencies:

```bash
$ pip install -r requirements.txt
```

Start server (debug-mode):
```bash
./start-debug-server.sh
```

# Task

## GET API's

* API: **HTTP GET /rates** and **HTTP GET /rates_null**
* Expects the query params:
    * **date_from**, **date_to** 'YYYY-MM-DD' format
    * **origin**, **destination** can be port code(5 digits) or region
* Returns an JSON [{ "day": "<YYYY-MM-DD>", "average_price": <number>}] or a error about the query params

Example `/rates`:
```bash
curl http://localhost:5000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main
```

Example `/rates_null`:
```bash
curl http://localhost:5000/rates_null?date_from=2016-01-01&date_to=2016-01-2&origin=CNSGH&destination=north_europe_main
```

## POST API

* API: **HTTP POST /prices**
* Accepts `application/json` or `application/x-www-form-urlencoded` in request body
* Expects the in body content:
    * **date_from**, **date_to** 'YYYY-MM-DD' format
    * **origin**, **destination** can be port code(5 digits) or region
    * **price** an integer
    * **currency**, is optional, 3 digits currency identifier, *default* = USD
* Returns { "message": "OK" } or a error about the body content

Example `x-www-form-urlencoded`:
```bash
curl -d "date_from=2019-01-01&date_to=2016-01-02&origin=CNSNZ&destination=baltic&price=1400" -X POST http://localhost:5000/prices -H "Content-Type: application/x-www-form-urlencoded"
```

Example `json`:
```bash
curl -d '{"date_from":"2019-01-01","date_to":"2019-01-02","origin":"northern_europe","destination":"china_main","price":2345, "currency":"BRL"}' -X POST http://localhost:5000/prices -H "Content-Type: application/json"
```

## Batch processing answer

The answer to Batch processing question is in `batch_processing.md`

# Considerations

* The development flow can be seen in git history, as it was tailored to facilitate revision

* The database was not modified to solve the problem. Although there is some considerations in the folowing section

* 2 days (weekend)  were spent on this problem.

* I have Java background, I am sorry if the code is not pythonic (It will get better).

* I tried to use as little as possible of a framework, so you guys can evaluate me. So there is some database connection handling, functional-like dependency injection, regex, exception handling, etc. In a real project I would prefer use the stantard framework and modules.

* I marked some enhancements, like  caching, that could be done easily, with a little more time.

* Tests are missing =/. It is a big problem for me, and I will update it as a separate branch to not cheat the deadline.

## Database considerations

### Regions table

Relational databases are not good with **self-reference/recursion**, so **regions** table can slow
down some queries, if there as a deep recursion (which is not the case with this simplified database).

Regions table (as any table which has recursion) would be easily defined in a graph-like database.

Another option would be flatten the database in a materialized view, as I think regions table does
not change that much.

### Partition prices table by period (month or year or week)

Prices has characteristc of growning with time (each day a "little") bigger, so its performance,
degrades in time. That problem should be easily solved by partitioning in months, example:

```sql
CREATE TABLE prices (
    orig_code       text not null,
    dest_code       text not null,
    price           int not null,
    day             date not null
) PARTITION BY RANGE (day);

CREATE TABLE prices_2016_02 PARTITION OF prices
    FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');

CREATE TABLE prices_2016_03 PARTITION OF prices
    FOR VALUES FROM ('2006-03-01') TO ('2006-04-01');
```

A scheduled job should create the partition tables as time passes.
Like this performance should be kept.