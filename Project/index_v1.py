# TODO: implement button that change csv file that generates graph (functionality in a callback)
# TODO: two more dropdown menus (under the 'update graph' button) that each let user select a node in the graph
# TODO: generate bar chart showing distance distributon between two selected nodes. (re: prev. TODO)
    # remember button to generate chart
    # calc length of all sequences between two nodes
    # bar chart should show distribution of lengths (x: length, y: num players that took this sequence length)
    # length should always be calculated as node1 - node2

## try to avoid global variables, put functions in source files ##

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto

# import necessary tools
from models.SequenceGraph import SequenceGraph
from models.SequenceNetwork import SequenceNetwork
import os
# network declaration
our_network = SequenceNetwork()
our_network.initFromCsv('Project/data/completedAndIncompletePlayers.csv', 'example')
# build graph from our_network
our_graph = SequenceGraph()
our_graph.initFromSequenceNetwork(our_network)
our_graph.buildSequenceGraph()
#
graph_elements = our_graph.getCurrentElements()
graph_styles = our_graph.getCurrentStyle()

# =========================
# app v2
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Dropdown(
                    id='dropdown-file-selection',
                    value='all_players'
                )
            ], id="div-file-selection-dropdown"
            ),
            dbc.Button('Update Graph', id='update-button', n_clicks=0, color='primary', className='mt-3'),
            dbc.Alert(id='alert', children='', is_open=False, color='info', className='mt-2'),
            html.Div(id='node-info', style={'marginTop': '20px'})
        ], width=3),

        dbc.Col([
            cyto.Cytoscape(
                id='cytoscape-graph',
                elements=graph_elements,
                style={
                    'width': '100%',
                    'height': '700px',
                    'border': '2px solid black'
                },
                layout={
                    'name': 'cose',
                    'animate': False,
                    'randomize': False,
                    'nodeRepulsion': 900000,
                    'fit': True,
                    'padding': 10
                },
                # stylesheet=graph_styles
                stylesheet=[
                    {
                        'selector': 'node',
                        'style': {
                            'label': 'data(label)',
                            'background-color': '#0074D9',
                            'color': 'black',
                            'font-size': '12px',
                            'width': 'data(size)',
                            'height': 'data(size)',
                            'border-width': '2px',
                            'border-color': 'black',
                            'text-wrap': 'wrap'
                        }
                    },
                    {
                        'selector': 'edge',
                        'style': {
                            'line-color': '#B3B3B3',
                            'width': '5px',
                            'target-arrow-shape': 'triangle',
                            'target-arrow-color': '#B3B3B3',
                            'arrow-scale': '1.5',
                            'curve-style': 'bezier'
                        }
                    },
                    {
                        'selector': ':selected',
                        'style': {
                            'background-color': '#FF4136',
                            'line-color': '#FF4136',
                            'target-arrow-color': '#FF4136',
                            'border-width': '4px'
                        }
                    }
                ]
            )
        ], width=9)
    ])
])
# =========================

if __name__ == '__main__':
    app.run_server(debug=True)
