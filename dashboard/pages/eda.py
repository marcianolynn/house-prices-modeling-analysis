# Data
import pandas as pd
import numpy as np
import pickle
from pandas.io.formats import style
# Graphing
import plotly.graph_objects as go
import plotly.express as px
# Dash
import dash
import dash_table
from dash_table.Format import Format, Scheme
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import base64
# Navbar
from pages.navbar import Navbar

nav = Navbar()

header = html.H3(
    'Place EDA HERE'
)

# dataset
df = pd.read_csv(r'data/W207_original_IC.csv')

df_FEN = pd.read_csv(r'data/W207_original_IC_FEN.csv')

# assets
# home price image
# replace with your own image
image_filename = 'dashboard\\assets\\house_dollar.jpg'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# determine absolute correlation of features with our target variable
corr_table = df.corr()
corr_table['abs_SalePrice'] = abs(corr_table['SalePrice'])
corr_table.sort_values(by='abs_SalePrice', ascending=False)[
    ['SalePrice', 'abs_SalePrice']]

# explain the EDA and feature engineering overview
eda_overview = dbc.Card(
    dbc.CardBody([
        dcc.Markdown('''
                        # Exploratory Data Analysis
                        We perform EDA by observing the intial distribution of our target variable. Some of the things we notice were:
                        * Distribution for "SalePrice" is not normally distributed
                        * House features can cause a high price tag
                        '''),
        dbc.Col(
                 html.Div(
                     [
                         html.Img(
                             src='data:image/jpg;base64,{}'.format(
                                 encoded_image.decode()),
                             style={
                                 'height': '50%',
                                 'width': '50%'}
                         ),
                     ]
                 ), style={'textAlign': 'center'})
    ]
    ),
    style={
        'width': 'auto'
    }
)

fg_overview = dbc.Card(
    dbc.CardBody(
        dcc.Markdown('''
                        # Price Per Square Foot
                        **Intuition**:

                        Price per square foot can show you a trend if the homes are similar in square footage.
                        It is meant to give individual's an idea of the home's market value.
                        Although our dataset is confined to the Ames, Iowa location,
                        the square footage in our dataset varies and is similarly skewed to our initial target variable.
                        However, we decided transform our target variable (Sales Price) with the combined indoor square footage of a home
                        to see if this would create a normally distributed variable.

                        When *feature engineering* a new "target" variable in order to assist us in the modeling of our true target variable,
                        we notice that the distribution is more normal and will be helpful in creating more robust results from our models since
                        the RMSE will not be biased by the outlier prices or square footage.

                        We then investigate the absolute correlation of our features with the target variable, sales price.
                        ''')
    ),
    style={
        'width': 'auto'
    }
)

# explain observations from correlation table
correlation_info = dbc.Card([
    dbc.CardHeader(html.B("Absolute Correlation with Target Variables"),
                   style={'background-color': 'rgb(229,236,246)'}),
    dbc.CardBody(
        dcc.Markdown('''
                        Based on our observations, we determine that these variables are most correlated with our target variables:

                        ### **SalesPrice**
                        - OverallQual
                        - GrLivArea
                        - ExterQual
                        - KitchenQual
                        - GarageCars

                        ### **Price per Square Foot**
                        - YearBuilt
                        - OverallQual
                        - KitchenQual
                        - ExterQual
                        - YearRemodAdd
                        ''')
    )
]

)

# create histogram plots of the target variables
init_target_hist = px.histogram(
    df['SalePrice'],
    x="SalePrice"
)

init_target_hist.update_layout(
    xaxis_title="Sale Price",
    yaxis_title="Count",
    font=dict(
        size=18,
        color="RebeccaPurple"
    )
)

fen_target_hist = px.histogram(
    df_FEN['FE_SalePrice_Per_IndoorArea'],
    x="FE_SalePrice_Per_IndoorArea"
)

fen_target_hist.update_layout(
    xaxis_title="Sale Price per Square Foot",
    yaxis_title="Count",
    font=dict(
        size=18,
        color="RebeccaPurple"
    )
)

# find the correlation of variables with the target variables
pd.options.display.float_format = '{:.2f}'.format
corr_table = df_FEN.corr().reset_index().rename(columns={
    'index': 'Variable',
    'FE_SalePrice_Per_IndoorArea': 'PricePerSqFoot'}).head(30)
corr_table = corr_table.sort_values(
    by='PricePerSqFoot', ascending=False)[
        ['Variable', 'SalePrice', 'PricePerSqFoot']]


corr_dash_table = dash_table.DataTable(
    id='corr_table',
    columns=[{"name": i, "id": i} for i in corr_table.columns],
    data=corr_table.to_dict('records'),
    style_data={
        'height': '20px',
        'backgroundColor': 'white'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(229,236,246)',
        }
    ],
    fixed_rows={'headers': True},
    style_header={
        'backgroundColor': 'rgb(229,236,246)',
        'color': 'black',
        'fontWeight': 'bold'
    },
    style_table={
        'height': '600px'},
    style_cell_conditional=[
        {'if': {'column_id': 'Variable'},
         'width': '20%'}
    ],
    page_action='none',
)

# define layout
body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [eda_overview],
                    md=4
                ),
                dbc.Col(
                    [fg_overview],
                    md=6
                )
            ],
            className="eda-row",
            justify="center"
        ),
        dbc.Row(
            [
                # provide a side by side histogram of the original target variable and our FEN one
                dbc.Col(
                    dcc.Graph(
                        id='init_target',
                        figure=init_target_hist
                    ),
                    md=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='fen_target',
                        figure=fen_target_hist
                    ),
                    md=6
                )
            ],
            className="variables-row",
            justify="center"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [correlation_info],
                    md=4
                ),
                dbc.Col(
                    [corr_dash_table],
                    md=6
                )
            ],
            className=["corr-row"],
            justify="center"
        )
    ]
)


def EDA():
    layout = html.Div([
        nav,
        body
    ])
    return layout
