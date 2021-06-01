import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
from parser_agent.sql_create_query import CreateQuery
from style import DECATHLON_LOGO, LOGO_BAR_STYLE, SIDEBAR_STYLE, CONTENT_STYLE,\
    NODE_STYLE, EDGE_STYLE, INPUT_STYLE, INTERMEDIATE_STYLE, TEMPORARY_STYLE, PERMANENT_STYLE

query="""CREATE TEMPORARY TABLE t_output
AS WITH t_intermediate AS
(
SELECT *
FROM t_input
)
SELECT *
FROM t_intermediate
"""

q = CreateQuery(
    query=query
).mine()

data = q.to_dash_with_parent()

dialog = dcc.ConfirmDialog(
        id='confirm',
        message='Welcome !',
    )

external_stylesheets = [dbc.themes.SIMPLEX]

logo_bar = html.Div(
    [
        html.Img(src=DECATHLON_LOGO, height="45px", style=LOGO_BAR_STYLE),
        html.Hr()
    ],
    style={"class":"d-flex justify-content-center"}
)

textarea = html.Div(
    [
        dbc.Textarea(id="input_text_", className="mb-3", placeholder=query, value=query, style={"height":"300px"}),
    ]
)

graph = cyto.Cytoscape(
    id='cytoscape',
    elements=data,
    layout={'name': 'concentric'},
    style={'width': '950px', 'height': '550px'},
    minZoom=0.2,
    maxZoom=2,
    stylesheet=[
        {
            'selector': 'node',
            'style': NODE_STYLE,
        },
        {
            'selector': 'edge',
            'style': EDGE_STYLE
        },
        {
            'selector': '.INPUT',
            'style': INPUT_STYLE
        },
        {
            'selector': '.INTERMEDIATE',
            'style': INTERMEDIATE_STYLE
        },
        {
            'selector': '.TEMPORARY',
            'style': TEMPORARY_STYLE
        },
        {
            'selector': '.PERMANENT',
            'style': PERMANENT_STYLE
        }
    ]
)

button = html.Div(dbc.Button('Plot !', color="success", id='button', className="mr-1 col text-center"))

title = html.Div(
    [
        html.H2("Rétro-lineage", className="display-4", style={"font-size": "2rem"}),
        html.Hr()
    ]
)
dropdown = html.Div(
    [
        dcc.Dropdown(
            id='dropdown-update-layout',
            value='concentric',
            clearable=False,
            options=[
                {'label': name.capitalize(), 'value': name}
                for name in ['circle', 'concentric', 'preset', 'breadthfirst', 'grid', 'random', 'cose']
            ]
        ),
        html.Hr()
    ]
)

sidebar = html.Div([
    dialog,
    logo_bar,
    title,
    dropdown,
    textarea,
    button

], style=SIDEBAR_STYLE)

content = html.Div([graph], id="page-content", style=CONTENT_STYLE)

