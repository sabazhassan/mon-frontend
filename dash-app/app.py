
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

# Create list for labels


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H4("HDvent", className="top_bar_title"),
                    ],
                    className="top_bar_entry",
                ),
            ],
            className="top_bar",
        ),
        dcc.Graph(id='live-graph', animate=False),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
        dcc.Graph(id='live-graph2', animate=False),
        dcc.Graph(id='live-graph3', animate=False),
        html.Div(
            [
                html.Div(
                    [
                        html.H4("HDvent", className="top_bar_title"),
                    ],
                    className="top_bar_entry",
                ),
            ],
            className="top_bar",
        ),
    ]
)

@app.callback([Output('live-graph', 'figure'), 
               Output('live-graph2', 'figure'), 
               Output('live-graph3', 'figure')],
              [Input('graph-update', 'n_intervals')])

def update_graph_scatter(input_data):
    
    for x in range(0, 25):
        X.append(X[-1]+1)
        Y.append(Y[-1]+Y[-1]*random.uniform(-0.01,0.01))
        
## Create Labels
# LAB = LABELS[len(LABELS)-len(Y):len(LABELS)] 
    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            fill='tozeroy',
            mode= 'lines'
            )

    RESULT = {'data': [data],'layout' : go.Layout(paper_bgcolor= "#000", 
                                                colorway= ["#fff"],
                                                plot_bgcolor= "#000",
                                                xaxis=dict(title='ms',range=[min(X),max(X)], visible = True, color = "#fff"),
                                                yaxis=dict(color = "#fff", range=[min(Y),max(Y)]),)}

    return [RESULT, RESULT, RESULT]
                                                           


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8050 ,debug=True)
