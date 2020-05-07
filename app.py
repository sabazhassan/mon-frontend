# -*- coding: utf-8 -*-
"""
Main dash app
"""
# pylint: disable=unused-argument
import logging
import os
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

##
import json
import base64
import datetime
import requests
import pathlib
import math
import flask
import dash

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
# app.layout = html.Div(
#     [
#         dcc.Graph(id="live-graph", animate=True),
#         dcc.Interval(id="graph-update", interval=UPDATE_INTERVAL * 1000),
#     ]
# )
app.layout = html.Div(
    className="row",
    children=[
        html.Div(
            className="nine columns div-right-panel",
            children=[
                # Top Bar Div - Displays Balance, Equity, ... , Open P/L
                html.Div(
                    children=[
                        dcc.Graph(id="live-graph", animate=True),
                        dcc.Interval(
                            id="graph-update", interval=UPDATE_INTERVAL * 1000
                        ),
                    ]
                ),
            ],
        ),
        html.Div(
            className="three columns div-left-panel",
            children=[
                # Top Bar Div - Displays Balance, Equity, ... , Open P/L
                html.Div(
                    className="div-info",
                    children=[
                        # html.Img(
                        #     className="logo", src=app.get_asset_url("dash-logo-new.png")
                        # ),
                        html.H6(className="title-header", children="FOREX TRADER"),
                        html.P(
                            """
                            Current values of parameters
                            """
                        ),
                    ],
                ),
                # Ask Bid Currency Div
                html.Div(
                    className="box-left",
                    children=[
                        # dcc.Interval(id="pressure-update", interval=UPDATE_INTERVAL * 1000),
                        html.Div(className="box-header", children=["Pressure"],),
                        html.Div(
                            className="box-body",
                            children=[
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="six columns",
                                            children=["Current Value"],
                                        ),
                                        html.Div(
                                            className="six columns",
                                            children=["0.26"],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="six columns", children=["Unit"],
                                        ),
                                        html.Div(
                                            className="six columns", children=["mbar"],
                                        ),
                                    ],
                                ),
                                # html.Div(
                                #     className="row",
                                #     children=[
                                #         html.Div(
                                #             className="six columns", children=["Mean"],
                                #         ),
                                #         html.Div(
                                #             className="six columns", children=["0.25"],
                                #         ),
                                #     ],
                                # ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="box-left",
                    children=[
                        html.Div(className="box-header", children=["Flow"],),
                        html.Div(
                            className="box-body",
                            children=[
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="six columns",
                                            children=["Current Value"],
                                        ),
                                        html.Div(
                                            className="six columns", children=["0.26"],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="six columns", children=["Unit"],
                                        ),
                                        html.Div(
                                            className="six columns", children=["mL"],
                                        ),
                                    ],
                                ),
                                # html.Div(
                                #     className="row",
                                #     children=[
                                #         html.Div(
                                #             className="six columns", children=["Mean"],
                                #         ),
                                #         html.Div(
                                #             className="six columns", children=["0.25"],
                                #         ),
                                #     ],
                                # ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="box-left",
                    children=[
                        html.Div(className="box-header", children=["Volume"],),
                        html.Div(
                            className="box-body",
                            children=[
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="six columns",
                                            children=["Current Value"],
                                        ),
                                        html.Div(
                                            className="six columns", children=["0.26"],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(
                                            className="six columns", children=["Unit"],
                                        ),
                                        html.Div(
                                            className="six columns", children=["cubic mL"],
                                        ),
                                    ],
                                ),
                                # html.Div(
                                #     className="row",
                                #     children=[
                                #         html.Div(
                                #             className="six columns", children=["Mean"],
                                #         ),
                                #         html.Div(
                                #             className="six columns", children=["0.25"],
                                #         ),
                                #     ],
                                # ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
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

#@app.callback(Output("live-pressure", "figure"), [Input("pressure-update", "n_intervals")])
def update_pressure():
    data = list(influx.get_data("pressure"))
    last_record = data[-1]
    return last_record["value"]


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
