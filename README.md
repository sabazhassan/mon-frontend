# mon-frontend

## Developing

start containers:
`docker-compose up`
(add `-d` to start and detach)

The dash app will be automatically started and can be accessed at [http://localhost:8050](http://localhost:8050)

### test data

Test data is written continuously into the following influxdb database:

- database: FIXME
- user: FIXME
- password: FIXME

## InfluxDB

URL: `http://localhost:8086`

## Grafana

WebUI: [http://localhost:3000](http://localhost:3000)

default login credentials:

- username: `admin`
- password: `admin`

The first time you start grafana (or if you delete the docker volume `grafana-data`) you will need to set up the influxdb data source. This can be the test database, or real data once we have one. See details above.
