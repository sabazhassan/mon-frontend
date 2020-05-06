# mon-frontend

[![Build Status](https://travis-ci.org/HDventilator/mon-frontend.svg?branch=master)](https://travis-ci.org/HDventilator/mon-frontend)

## Developing

start containers:
`docker-compose up`
(add `-d` to start and detach)

The dash app will be automatically started and can be accessed at [http://localhost:8050](http://localhost:8050)

### Test Data Writer

Test data is written continuously into influxdb. The writer is configured with the following docker-compose environment variables:

```
- INFLUXDB_HOST=influxdb  # inxflux host (do not use localhost)
- INFLUXDB_PORT=8086      # influx port
- DATABASE_NAME=testdata  # database to write test data to
- WRITE_INTERVAL=1.0      # data write interval
```

WARNING: The writer will drop the test database on restart to prevent issues with already existing series -> do not point it at a "production" database!

## InfluxDB

external URL: `http://localhost:8086`

## Grafana

WebUI: [http://localhost:3000](http://localhost:3000)

default login credentials:

- username: `admin`
- password: `admin`

The first time you start grafana (or if you delete the docker volume `grafana-data`) you will need to set up the influxdb data source.

- URL: `http://influxdb:8086`
- Database: This can be the test database, or real data once we have one. The datawriter container uses `testdata` by default.
