# -*- coding: utf-8 -*-
"""
Continously writes test data to the specified influxdb database
"""

import os
import random
import time
from datetime import datetime, timezone
from typing import Optional

from influxdb import InfluxDBClient

INFLUXDB_HOST = os.environ.get("INFLUXDB_HOST", "influxdb")
INFLUXDB_PORT = os.environ.get("INFLUXDB_PORT", 8086)

WRITE_INTERVAL = os.environ.get("WRITE_INTERVAL", 1.0)
DATABASE_NAME = os.environ.get("DATABASE_NAME", "testdata")

# test fields and range for random value generation
MEASUREMENTS = ["pressure", "flow", "volume"]
MEASUREMENT_RANGE = (-100.0, 100.0)


def writeloop(client):
    """
    Infinite loop to write data to influxdb
    """
    while True:
        time.sleep(float(WRITE_INTERVAL))
        data = []

        # timestamp is in milliseconds
        timestamp = datetime.now(timezone.utc).timestamp() * 1000

        for measurement_name in MEASUREMENTS:
            # randomly generate value in measurement range
            lower, upper = MEASUREMENT_RANGE
            measurement_value = ((upper - lower) * random.random()) + lower

            # add influxdb line protocol line to data
            data.append(
                f"{measurement_name},type=test value={measurement_value:.3f} {timestamp:.0f}"
            )

        client.write_points(
            data,
            database=DATABASE_NAME,
            time_precision="ms",
            batch_size=10,
            protocol="line",
        )
        print("ping...")


def connect_client(max_tries: int = 30) -> Optional[InfluxDBClient]:
    """
    Connect/retry logic. Returns a working InfluxDBClient if successfull.
    """
    client = None
    tries = 0
    while tries < max_tries:
        try:
            tries += 1
            print(f"Connecting... (attempt {tries}/{max_tries})")
            client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)
        except ConnectionError:
            print(
                f"Could not connect to influxdb database \
                {DATABASE_NAME} @ {INFLUXDB_HOST}:{INFLUXDB_PORT}..."
            )
            print("Retrying in one second...")
            time.sleep(1.0)
            continue
        break
    return client


if __name__ == "__main__":
    print("Starting...")
    iflx_client = connect_client()  # pylint: disable=invalid-name
    if iflx_client is not None:
        iflx_client.drop_database(DATABASE_NAME)
        iflx_client.create_database(DATABASE_NAME)
        writeloop(iflx_client)
    print("Exited.")
