# -*- coding: utf-8 -*-
"""
Main dash app
"""
# pylint: disable=unused-argument
import logging
import os
import dash
from datetime import datetime, timezone, timedelta
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from typing import Iterable, Any
from influx import Influx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))


INFLUXDB_HOST = os.environ.get("INFLUXDB_HOST", "influxdb")
INFLUXDB_PORT = int(os.environ.get("INFLUXDB_PORT", 8086))
UPDATE_INTERVAL = float(os.environ.get("GRAPH_UPDATE_INTERVAL_SECONDS", 1))
INFLUXDB_DATABASE = os.environ.get("INFLUXDB_DATABASE", "default")


influx = Influx(INFLUXDB_HOST, INFLUXDB_DATABASE, INFLUXDB_PORT)
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id="live-graph-pressure", animate=True),
        dcc.Graph(id="live-graph-flow", animate=True),
        dcc.Graph(id="live-graph-volume", animate=True),
        dcc.Interval(id="graph-update", interval=UPDATE_INTERVAL * 1000),
        dcc.Store(id="in-memory-storage", storage_type="memory"),
    ],
)


@app.callback(
    Output("in-memory-storage", "data"), [Input("graph-update", "n_intervals")],
)
def fetch_data(intervals):
    """
    called by graph-update timer
    uses influx client to fetch new data for all available measurements
    """
    measurements_data = {}
    for measurement in influx.get_measurements():
        data = list(influx.get_data(measurement, duration="30s"))

        x_data = [d["time"] for d in data]
        y_data = [d["value"] for d in data]

        # replace y-data with relative time
        # fixme, move this to influx-connector
        now = datetime.now(timezone.utc)
        x_data = [(ts - now).total_seconds() for ts in x_data]

        measurements_data[measurement] = {"x": x_data, "y": y_data}
    return measurements_data


@app.callback(
    Output("live-graph-pressure", "figure"), [Input("in-memory-storage", "data")],
)
def scatter_graph(data):
    """
    Returns scatter graph for measurement whenever stored data changes
    """
    measurement = "pressure"
    plot_data = make_scatter_data(
        measurement, data[measurement]["x"], data[measurement]["y"]
    )
    plot_layout = make_scatter_layout(
        measurement, data[measurement]["x"], data[measurement]["y"]
    )
    return {"data": plot_data, "layout": plot_layout}


@app.callback(
    Output("live-graph-flow", "figure"), [Input("in-memory-storage", "data")],
)
def scatter_graph(data):
    """
    Returns scatter graph for measurement whenever stored data changes
    """
    measurement = "flow"
    plot_data = make_scatter_data(
        measurement, data[measurement]["x"], data[measurement]["y"]
    )
    plot_layout = make_scatter_layout(
        measurement, data[measurement]["x"], data[measurement]["y"]
    )
    return {"data": plot_data, "layout": plot_layout}


@app.callback(
    Output("live-graph-volume", "figure"), [Input("in-memory-storage", "data")],
)
def scatter_graph(data):
    """
    Returns scatter graph for measurement whenever stored data changes
    """
    measurement = "volume"
    plot_data = make_scatter_data(
        measurement, data[measurement]["x"], data[measurement]["y"]
    )
    plot_layout = make_scatter_layout(
        measurement, data[measurement]["x"], data[measurement]["y"]
    )
    return {"data": plot_data, "layout": plot_layout}


def make_scatter_data(measurement_name, data_x, data_y):
    """
    Helper to generate consistent plots
    """
    return [
        go.Scatter(
            x=data_x, y=data_y, name=measurement_name, fill="tozeroy", mode="lines"
        )
    ]


def make_scatter_layout(
    measurement_name: str, data_x: Iterable[Any], data_y: Iterable[Any]
):
    """
    Helper to generate consistent layouts for scatter plots with adaptive x and y
    axis ranges
    """
    return dict(
        title=measurement_name.upper(),
        paper_bgcolor="#000",
        plot_bgcolor="#000",
        # colorway=["#fff"],
        xaxis=dict(
            title="relative time [s]",
            range=[min(data_x), max(data_x)],
            visible=True,
            color="#fff",
        ),
        yaxis=dict(
            color="#fff",
            title=f"{measurement_name} [-unit-]",
            range=[min(data_y), max(data_y)],
        ),
    )


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
