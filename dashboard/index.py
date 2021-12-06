import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from pages.homepage import Homepage
from pages.variables import Variables, build_count
from pages.models import Models
from pages.eda import EDA
import base64


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

image_filename = 'dashboard\\assets\\imgs\\bg.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

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


@app.callback(
    Output('var_output', 'children'),
    [Input('orig_var_dropdown', 'value')]
)
def update_graph(variable):
    plot_row = build_count(variable)
    return plot_row


if __name__ == '__main__':
    app.run_server(debug=True, use_debugger=False, use_reloader=False)