from re import S
from parser_agent.sql_create_query import CreateQuery
import dash
import json
import dash_html_components as html
from dash.dependencies import Input, Output, State

from viz_components import external_stylesheets, sidebar, content, dialog

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([   
    html.Div([sidebar, content]),
])

@app.callback(
    Output("cytoscape", "elements"),
    [Input('button', 'n_clicks')],
    state=[State(component_id='input_text_', component_property='value')]
)
def plot(n_clicks, input_text):

    _data = CreateQuery(query=input_text, query_group_name="group").mine().to_dash(with_parent=True)
    
    return _data


@app.callback(Output('confirm', 'displayed'),
              Output('confirm', 'message'),
              Input('cytoscape', 'selectedNodeData'))

def display_confirm(value):

    if not value:

        return False, ""
    
    return True, value[0]['query']

if __name__ == "__main__":
    
    app.run_server(host="0.0.0.0", port=8050, debug=False)