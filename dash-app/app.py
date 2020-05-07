# -*- coding: utf-8 -*-
"""
Main dash app
"""
# pylint: disable=unused-argument
import logging
import os
from typing import Any, Iterable

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

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

server = app.server
# production: gunicorn -b 0.0.0.0:8050 app:server

app.layout = html.Div(
    [
        dcc.Graph(id="live-graphs", animate=True, style={"height": "100vh"}),
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

        measurements_data[measurement] = {
            "x": [d["time"] for d in data],
            "y": [d["value"] for d in data],
        }
    return measurements_data


@app.callback(
    Output("live-graphs", "figure"), [Input("in-memory-storage", "data"),],
)
def live_graphs(data):

    measurements = list(influx.get_measurements())
    nrows = len(measurements)
    fig = make_subplots(rows=nrows, cols=1, shared_xaxes=True, vertical_spacing=0.02,)

    # overall layout
    layout = dict(
        paper_bgcolor="#000",
        plot_bgcolor="#000",
        # colorway=["#fff"],
        xaxis3=dict(title="relative time [s]", color="#fff"),
        showlegend=False,
    )

    # add traces and setup axes for each measurement
    for n, measurement in enumerate(measurements):
        trace = go.Scatter(
            x=data[measurement]["x"],
            y=data[measurement]["y"],
            name=measurement,
            fill="tozeroy",
            mode="lines",
        )
        fig.add_trace(trace, row=n + 1, col=1)

        y_layout = dict(
            title=f"{measurement.upper()} [-]",
            color="#fff",
            range=[min(data[measurement]["y"]), max(data[measurement]["y"])],
            showgrid=False,
        )
        if n == 0:
            layout["yaxis"] = y_layout
        else:
            layout[f"yaxis{n+1}"] = y_layout

    # set layout and return figure
    fig.update_layout(layout)
    return fig


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
