# -*- coding: utf-8 -*-
"""
Main dash app
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly
import random
import plotly.graph_objs as go
from collections import deque

X = deque(maxlen=1500)
X.append(1)
Y = deque(maxlen=1500)
Y.append(1)

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])

def update_graph_scatter(input_data):
    
    for x in range(0, 50):
        X.append(X[-1]+1)
        Y.append(Y[-1]+Y[-1]*random.uniform(-0.01,0.01))
        
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            fill='tozeroy',
            mode= 'lines'
            )

    return {'data': [data],'layout' : go.Layout(paper_bgcolor= "#000", 
                                                colorway= ["#fff"],
                                                plot_bgcolor= "#000",
                                                xaxis=dict(title='ms',range=[min(X),max(X)], visible = True, color = "#fff"),
                                                yaxis=dict(color = "#fff", range=[min(Y),max(Y)]),)}


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
# -*- coding: utf-8 -*-
"""
Main dash app
"""

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

app.layout = html.Div(
    children=[
        html.H1(children="Hello!"),
        html.Div(
            children="""
        Dash: A web application framework for Python.
    """
        ),
        dcc.Graph(
            id="example-graph",
            figure={
                "data": [
                    {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
                    {
                        "x": [1, 2, 3],
                        "y": [2, 4, 5],
                        "type": "bar",
                        "name": u"Montréal",
                    },
                ],
                "layout": {"title": "Dash Data Visualization"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
