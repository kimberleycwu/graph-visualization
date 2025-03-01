# REVIEW: implement button that change csv file that generates graph (functionality in a callback)
# REVIEW: two more dropdown menus (under the 'update graph' button) that each let user select a node in the graph
# REVIEW: generate bar chart showing distance distributon between two selected nodes. (re: prev. task)
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
import plotly.express as px

# import necessary tools
from models.SequenceGraph import SequenceGraph
from models.SequenceNetwork import SequenceNetwork
from collections import deque
import os

# fetch .csv files from Project/data/
csv_files = [ {'label':f, 'value':f} for f in os.listdir('./data') if f.endswith('.csv') ]

# ===== APP ====================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='file-selector',
                options=csv_files,
                value=csv_files[0]['value'] if csv_files else None,
                style={'padding-bottom': '5px'}
            ),
            dbc.Button('Update Graph', id='update-button', n_clicks=0, color='primary'),
            dcc.Store(id="sequence-graph-player-states"),
            dbc.Alert(id='alert', children='', is_open=False, color='info', className='mt-2')
        ], width=3),
        dbc.Col([
            cyto.Cytoscape(
                id='cytoscape-graph',
                elements=[],
                style={ 'width': '100%', 'height': '500px', 'border': '2px solid black' },
                layout={
                    'name': 'cose',
                    'animate': False,
                    'randomize': False,
                    'nodeRepulsion': 900000,
                    'fit': True,
                    'padding': 10 },
                stylesheet=[
                    {   'selector': 'node',
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
                        }},
                    {   'selector': 'edge',
                        'style': {
                            'line-color': '#B3B3B3',
                            'width': '5px',
                            'target-arrow-shape': 'triangle',
                            'target-arrow-color': '#B3B3B3',
                            'arrow-scale': '1.5',
                            'curve-style': 'bezier'
                        }},
                    {   'selector': ':selected',
                        'style': {
                            'background-color': '#FF4136',
                            'line-color': '#FF4136',
                            'target-arrow-color': '#FF4136',
                            'border-width': '4px'
                        }}
                ]
            ),
        ], width=9)
    ], className="pt-1"),
    dbc.Row([
        dbc.Col([
             # node1 and node2 selectors
            dcc.Dropdown(
                id='node1-select', options=[], placeholder='node1', style={'padding-bottom': '5px'}
            ),
            dcc.Dropdown(
                id='node2-select', options=[], placeholder='node2', style={'padding-bottom': '5px'}
            ),
            dbc.Button('Generate Chart', id='chart-button', n_clicks=0, color='primary'),
        ]), 
        dbc.Col([
            dcc.Graph(id='bar-chart'),
        ], width=9, className="text-left")
    ], className="pt-1")
])

# ===== CALLBACKS ====================
# updates graph, node1, and node2 from csv
@app.callback(
    [Output('cytoscape-graph', 'elements'),
     Output('node1-select', 'options'),
     Output('node2-select', 'options'),
     Output("sequence-graph-player-states", "data"),
     Output("alert", "children", allow_duplicate=True),
     Output("alert", "color", allow_duplicate=True),
     Output("alert", "is_open", allow_duplicate=True),
    ],
    [Input('update-button', 'n_clicks')],
    [State('file-selector', 'value')],
    prevent_initial_call=True
)
def update_graph(n_clicks, selected_file):
    if n_clicks > 0 and selected_file:
        # network declaration
        our_network = SequenceNetwork()
        our_network.initFromCsv(os.path.join('./data', selected_file), 'example')
        # build graph from our_network
        our_graph = SequenceGraph()
        our_graph.initFromSequenceNetwork(our_network)
        our_graph.buildSequenceGraph()
        playerState = our_network.getCurUserStates()
        # extract elements and declare nodes for dropdown
        elements = our_graph.getCurrentElements()
        node_options = [
            {'label': node['data']['id'],
             'value': node['data']['id'] } for node in elements if 'source' not in node['data']
        ]

        return elements, node_options, node_options, playerState, "Load Successfully!", "success", True
    return [], [], [], {}, "Something wrong when load graph!", "danger", True

# updates bar chart
@app.callback(
    [Output('bar-chart', 'figure'),
     Output("alert", "children"),
     Output("alert", "color"),
     Output("alert", "is_open")
    ],
    [Input('chart-button', 'n_clicks')],
    [State("sequence-graph-player-states", "data"),
     State('cytoscape-graph', 'elements'),
     State('node1-select', 'value'),
     State('node2-select', 'value')
    ],
    prevent_initial_call=True
)
# == WITHOUT pandas ==
def generate_chart(n_clicks, playerState, elements, node1, node2):
    if n_clicks > 0 and node1 and node2:
        # try:
            paths = find_all_paths(elements, node1, node2)
            if len(paths) == 0:
                return px.bar(), "No path found for these two selected nodes", "danger", True
            lengths = [len(path) - 1 for path in paths]  # -1 to count edges only
            length_counts = {length: lengths.count(length) for length in set(lengths)}
            # convert dictionary keys & values into lists for Plotly
            x_values = list(length_counts.keys())
            y_values = list(length_counts.values())
            # == DEBUG (re: bars not visible) ==
            print('length counts:', length_counts)
            print('x_values:', x_values)
            print('y_values:', y_values)
            # ====
            chart = px.bar(x=x_values, y=y_values, labels={'x': 'Sequence Length', 'y': 'Number of Paths'}, title="Sequence Length Distribution")
            return chart, "Chart Calculation Success!", "success", True
        # except Exception as e:
        #     return px.bar(), f"Error happens: {e}", "danger", True
    return px.bar()
# ====
# {"player1":[{"Activity":"action", "Starttime":0, "EndTime":1, "Image":"None", "actionAttribute":"test"}, {"Activity":"action2", ...}, ...], "player2":[]}
# helper function
def find_all_paths(elements, start, end):
    queue = deque([ (start, [start]) ]) # stores (current_node, path_so_far)
    all_paths = []
    while queue:
        current, path = queue.popleft()
        # print(current, path)
        if current == end:
            all_paths.append(path)
            # == DEBUG (re: bars not visible) ==
            # print('found path: ', path)
            # ====
            continue
        for edge in elements:
            if 'source' in edge['data'] and edge['data']['source'] == current:
                next_node = edge['data']['target']
                if next_node not in path:  # prevent cycles
                    queue.append((next_node, path + [next_node]))
    # == DEBUG (re: bars not visible) ==
    print("All paths found:", all_paths)
    # ====
    return all_paths

if __name__ == '__main__':
    app.run_server(debug=True)