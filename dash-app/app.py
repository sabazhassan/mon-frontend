"Value Unit"
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

from plotly.subplots import make_subplots

# Create test data
X = deque(maxlen=1500)
X.append(1)
Y = deque(maxlen=1500)
Y.append(1)

# App layout
app = dash.Dash(__name__)
app.layout = html.Div(
    [   
        html.Div(
            [
                ## Top Bar
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4("MODE", className="top_bar_title"),
                            ],
                            className="one-third column top_bar_mode",
                        ),
                        html.Div(
                            [
                                html.H4("HDvent", className="top_bar_title"),
                            ],
                            className="two-thirds column top_bar_info",
                        ),
                    ],
                    className="top_bar",
                ),
                ## Main Display Area
                html.Div(
                    [
                        # Live Plots
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(id='live-graph', style={"height": "80vh"},animate=False),
                                    ],
                                    className="live_plot",                            
                                ),
                                dcc.Interval(
                                    id='graph-update',
                                    interval=1*1000
                                ),
                            ],
                            className="two-thirds column live_plots",
                        ),
                        # Status Boxes
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H4("mbar", className="top_bar_title"),
                                    ],
                                    className="status_box",
                                ),
                                html.Div(
                                    [
                                        html.H4("mL", className="top_bar_title"),
                                    ],
                                    className="status_box",
                                ),
                                html.Div(
                                    [
                                        html.H4("mL", className="top_bar_title"),
                                    ],
                                    className="status_box",
                                ),
                            ],
                            className="one-third column status_boxes",
                        ),
                    ],
                    className="main_display",
                ),
                ## Bottom Bar
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4("MACHINE PARAMETERS", className="top_bar_title"),
                            ],
                            className="two-thirds column machine_parameters",
                        ),
                        html.Div(
                            [
                                html.H4("MACHINE STATUS", className="top_bar_title"),
                            ],
                            className="one-third column machine_status",
                        ),
                    ],
                    className="bottom_bar",
                ),
            ],
            className="app_content",
        )
    ],
    className="app_container",
)

@app.callback([Output('live-graph', 'figure')],               
              [Input('graph-update', 'n_intervals')])

def update_graph_scatter(input_data):
    
    for x in range(0, 50):
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
                                                title='PRESSURE',
                                                plot_bgcolor= "#000",
                                                xaxis=dict(title='ms',range=[min(X),max(X)], visible = True, color = "#fff"),
                                                yaxis=dict(color = "#fff", range=[min(Y),max(Y)]),)}
                                                
                                                
    return [RESULT]
                                                           


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050 ,debug=True)
