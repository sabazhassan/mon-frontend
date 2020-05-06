# -*- coding: utf-8 -*-
"""
Main dash app
"""
# pylint: disable=unused-argument
import logging
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

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
        dcc.Graph(id="live-graph", animate=True),
        dcc.Interval(id="graph-update", interval=UPDATE_INTERVAL * 1000),
    ]
)


@app.callback(Output("live-graph", "figure"), [Input("graph-update", "n_intervals")])
def update_graph_scatter(input_data):
    """
    Returns scatter graph containing all measurements from influxdb.
    """
    plot_data = []

    for measurement in influx.get_measurements():
        data = list(influx.get_data(measurement, duration="30s"))

        x_data = [d["time"] for d in data]
        y_data = [d["value"] for d in data]

        plot_data.append(
            go.Scatter(
                x=x_data, y=y_data, name=measurement, fill="tozeroy", mode="lines"
            )
        )

    return {
        "data": plot_data,
        "layout": dict(
            paper_bgcolor="#000",
            # colorway=["#fff"],
            plot_bgcolor="#000",
            xaxis=dict(
                title="time",
                range=[min(x_data), max(x_data)],
                visible=True,
                color="#fff",
            ),
            yaxis=dict(color="#fff", range=[min(y_data), max(y_data)]),
        ),
    }


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
