import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from homepage import Homepage
from variables import Variables
from models import Models
from eda import EDA


app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.UNITED],
    assets_folder = 'assets',
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0",
        }])

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/variables':
        return Variables()
    elif pathname == '/models':
        return Models()
    elif pathname == '/eda':
        return EDA()
    else:
        return Homepage()



# @app.callback(
#     Output('output', 'children'),
#     [Input('pop_dropdown', 'value')]
# )
# def update_graph(city):
#     graph = build_graph(city)
#     return graph


if __name__ == '__main__':
    app.run_server(debug=True, use_debugger=False, use_reloader=False)