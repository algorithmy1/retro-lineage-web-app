from re import S
#from parser_agent.sql_create_query import CreateQuery
from parser_agent.sql_query import SqlQuery
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

    #_data = CreateQuery(query=input_text, query_group_name="-").mine().to_dash(with_parent=False)
    _data = SqlQuery(query=input_text, queries_group_name="-").mine().to_dash(with_parent=False)
    return _data


@app.callback(Output('confirm', 'displayed'),
              Output('confirm', 'message'),
              Input('cytoscape', 'selectedNodeData'))

def display_confirm(value):

    if not value:

        return False, ""
    
    return True, value[0]['query']

@app.callback(Output('cytoscape', 'layout'),
              Input('dropdown-update-layout', 'value'))
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }

@app.callback(
    Output("cytoscape", "generateImage"),
    [
        Input("btn-get-jpg", "n_clicks")
    ])
def get_image(get_jpg_clicks):

    # File type to output of 'svg, 'png', 'jpg', or 'jpeg' (alias of 'jpg')
    ftype = 'jpg'
    action = 'download'
    filename = "data-lineage"

    output = dict()

    ctx = dash.callback_context
    if ctx.triggered:
        output = {
            'type': ftype,
            'action': action,
            'filename': filename,
            'options': {
                'full':True,
                'scale':5,
                'quality':1
            }
        }

    return output 

if __name__ == "__main__":
    
    app.run_server(host="0.0.0.0", port=8050, debug=True)