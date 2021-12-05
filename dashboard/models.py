# Data
import pandas as pd
import pickle
# Graphing
import plotly.graph_objects as go
# Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
# Navbar
from navbar import Navbar

nav = Navbar()


# dropdown = html.Div(dcc.Dropdown(
#     id='pop_dropdown',
#     options=options,
#     value='Abingdon city, Illinois'
# ))

# output = html.Div(id='output',
#                   children=[],
#                   )


def create_base_info(model_name, model_info):
    content = dbc.Card(
        [
            dbc.CardHeader(
                html.H3(model_name)
            ),
            dbc.CardBody(
                [
                    html.P(model_info, className="card-text"),
                ]
            ),
        ],
        className="mt-3",
    )
    return content


def create_rmse_info(rmse):
    content = dbc.Card(
        [
            dbc.CardHeader(
                html.H3('RMSE')
            ),
            dbc.CardBody(
                [
                    html.P(rmse, className="card-text"),
                ]
            ),
        ],
        className="mt-3",
    )
    return content


def create_var_info(num_vars):
    content = dbc.Card(
        [
            dbc.CardHeader(
                html.H3('Features Used')
            ),
            dbc.CardBody(
                [
                    html.P(num_vars, className="card-text"),
                ]
            ),
        ],
        className="mt-3",
    )
    return content


def create_base_tab(info, rmse, vars):
    body = dbc.Container(
        [
            dbc.Row(
                [info],
                className="variables-row",
                justify="center"
            ),
            dbc.Row(
                [
                    dbc.Col(
                        rmse
                    ),
                    dbc.Col(
                        vars
                    )
                ],
                className="variables-row",
                justify="center"
            )
        ]
    )
    return body


base_model1_desc = dcc.Markdown(
    '''
    Awesome info about Random Forest
    '''
)
base_model1_info = create_base_info('Random Forest', base_model1_desc)
base_model1_rmse = create_rmse_info(0.000)
base_model1_vars = create_var_info(20)
base_model1_tab = create_base_tab(base_model1_info, base_model1_rmse, base_model1_vars)

base_model2_desc = dcc.Markdown(
    '''
    Awesome info about KNN
    '''
)
base_model2_info = create_base_info('KNN', base_model2_desc)
base_model2_rmse = create_rmse_info(0.000)
base_model2_vars = create_var_info(20)
base_model2_tab = create_base_tab(base_model2_info, base_model2_rmse, base_model2_vars)

base_model3_desc = dcc.Markdown(
    '''
    Awesome info about XGB Boost
    '''
)
base_model3_info = create_base_info('XGB Boost', base_model3_desc)
base_model3_rmse = create_rmse_info(0.000)
base_model3_vars = create_var_info(20)
base_model3_tab = create_base_tab(base_model3_info, base_model3_rmse, base_model3_vars)

tabs = dbc.Tabs(
    [
        dbc.Tab(base_model1_tab, label="Baseline Model 1"),
        dbc.Tab(base_model2_tab, label="Baseline Model 2"),
        dbc.Tab(base_model3_tab, label="Baseline Model 3"),
    ]
)

body = dbc.Container(
    [
        dbc.Row(
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.H1("Baseline Models")
                    ),
                    dbc.CardBody(
                        tabs
                    )
                ]
            )
            
        ),
        dbc.Row(
            [html.H1('ADD INFO ABOUT FINAL MODEL'),
             html.P('ADD CHART')],
            className="variables-row",
            justify="center"
        )
    ]
)


def Models():
    layout = html.Div([
        nav,
        body
    ])
    return layout


# def build_graph(city):
#     data = [go.Scatter(x=df.index,
#                        y=df[city],
#                        marker={'color': 'orange'})]
#     graph = dcc.Graph(
#         figure={
#             'data': data,
#             'layout': go.Layout(
#                 title='{} Population Change'.format(city),
#                 yaxis={'title': 'Population'},
#                 hovermode='closest'
#             )
#         }
#     )
#     return graph
