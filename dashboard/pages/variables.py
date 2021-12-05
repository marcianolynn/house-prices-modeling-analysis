### Import Packages ###
from assets.data_dictionary import *
from pages.navbar import Navbar
import pandas as pd
import numpy as np
import dash
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import base64
sns.set_theme(style="darkgrid")

### NAVBAR ###

### DATA DICT ###

nav = Navbar()

# dataset
df = pd.read_csv(r'data/W207_original_IC.csv')
df_FEN = pd.read_csv(r'data/W207_original_IC_FEN.csv')

# data descriptions
data_descriptions_file = r'data/data_description.txt'
data_descriptions = pd.read_csv(data_descriptions_file, error_bad_lines=False, sep='\t', header=None,
                                names=['var_varEx', 'val']).dropna(how='all')
data_descriptions = data_descriptions.replace(
    r'^\s*$', np.nan, regex=True).dropna(how='all')  # remove blank cells
data_descriptions = data_descriptions.reset_index(drop=True)

# we will assume any adjacent col that is nan will be the variable description col
var_idxs = data_descriptions.loc[pd.isna(data_descriptions["val"]), :].index

# get the number of data observations
num_obs = len(df)

# get the number of different variables
num_vars = len(df.columns)

# explain the dataset and the cleaning process
data_overview = dbc.Card(
    dbc.CardBody(
        dcc.Markdown('''
                        # The Data
                        The *Ames Housing Dataset* was compiled by Dead De Cock for the use in data science education
                        to describe and perform analysis on different features of residential homes in Ames, Iowa and their house prices.
                        
                        There is a total of 79 explanatory variables representing the features of these homes.
                        ''')
    )
)

preprocessing_overview = dbc.Card(
    dbc.CardBody(
        dcc.Markdown('''
                        # Data Pre-Processing
                        Throughout our analysis, we perform data cleansing and ordinal encoding to pre-process the data.
                        
                        We perform data cleansing by handling missing values by:
                        * Filling in for missing or "NaN" values
                        * Validate the correspondence between the dataset values and data dictionary
                        * Fill in for boolean blank values
                        
                        We perform ordinal encoding by changing our ordinal features from string representation to numerical representation. 
                        ''')
    )
)

obs_card = dbc.Card(
    dbc.CardBody(
        [
            html.H1(str(num_obs), className="card-title"),
            html.P(
                "Cleaned Observations",
                className="card-text",
            )
        ]
    ),
    style={"width": "20rem"},
    color="rgb(217,175,107)",
    inverse=True
)

vars_card = dbc.Card(
    dbc.CardBody(
        [
            html.H1(str(num_vars-1), className="card-title"),
            html.P(
                "Explanatory Variables",
                className="card-text",
            )
        ]
    ),
    style={"width": "20rem"},
    color="rgb(172,174,161)",
    inverse=True
)


def get_var_features(var_vals):
    features = []
    for val in var_vals:
        features.append(str(val[0].strip() + ': ' + val[1]))
    features_string = "\n".join(features)
    return features_string


def get_variable_datatable():
    var_desc = {}
    # grab the var and its data description and values
    for i in range(0, len(var_idxs)):

        key, description = data_descriptions.loc[var_idxs[i]].str.split(': ')[
            0]
        var_desc[key] = {}
        var_desc[key]['Description'] = description

        # get the variable values
        if i < len(var_idxs)-1:
            var_df = data_descriptions[var_idxs[i]:var_idxs[i+1]]
        else:
            var_df = data_descriptions.loc[var_idxs[i]:]

        # if the variable has features, get those
        if len(var_df) > 1:
            var_elements = list(var_df.values)
            features_string = get_var_features(var_elements[1:])
            var_desc[key]['Values'] = features_string

    var_df = pd.DataFrame.from_dict(var_desc, orient='index').fillna(
        '').reset_index().rename(columns={'index': 'Variable'})
    return var_df


# variable data table
var_df = get_variable_datatable()


# create the datatable to display the variables
table = dash_table.DataTable(
    id='var_table',
    columns=[{"name": i, "id": i} for i in var_df.columns],
    data=var_df.to_dict('records'),
    style_data={
        'whiteSpace': 'pre-line',
        'height': '20px',
        'backgroundColor': 'white'
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }
    ],
    fixed_rows={'headers': True},
    page_action='none',
    style_table={
        'height': '400px',
        'width': '1300px'},
    style_cell={
        'textAlign': 'left',
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
        'height': '50px'},
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    },
    sort_mode="multi",
    filter_action="native"
)


all_vars = col_order + col_cat + col_num_continuous + col_num_int
options = [{'label': var_str, 'value': var_str} for var_str in all_vars]

# show the datavisualtion of the variables with the target variable
dropdown = html.Div(dcc.Dropdown(
    id='orig_var_dropdown',
    options=options,
    value=col_order[0]
))

output = html.Div(id='var_output',
                  children=[],
                  )

# build variable plots


def build_count(variable):
    if variable in all_vars:
        title_text = var_df.loc[var_df['Variable'] ==
                                variable]['Description'].values[0]

        # variable histogram
        hist = dcc.Graph(
            id='variable_hist',
            figure=px.histogram(
                df[variable],
                x=variable,
                color=variable,
                color_discrete_sequence=px.colors.qualitative.Antique,
            ).update_layout(
                yaxis_title="Count"
            )
        )

        box = dcc.Graph(
            id='variable_box',
            figure=px.box(
                df[variable],
                x=variable,
                y=df_FEN['FE_SalePrice_Per_IndoorArea'],
                points='all',
                color=variable,
                color_discrete_sequence=px.colors.qualitative.Antique,
            ).update_layout(
                showlegend=False,
                yaxis_title="Sale Price per Square Foot"
            )
        )

        plot_row = dbc.Row(
            [
                html.B(title_text),
                dbc.Col(
                    hist
                ),
                dbc.Col(
                    box
                )
            ]
        )

        return plot_row


# replace with your own image
image_filename = 'dashboard\\assets\\preprocessing.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

### BODY ###
body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    data_overview,
                    md=3
                ),
                dbc.Col(
                    preprocessing_overview,
                    md=5
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.Img(
                                src='data:image/png;base64,{}'.format(
                                    encoded_image.decode()),
                                style={
                                    'width': '90%'}
                            ),
                        ]
                    ),
                    md=4
                )
            ],
            style={
                'width': 'auto'
            },
            className="var_overview_row",
            justify="center"
        ),
        dbc.Row(
            [
                dbc.Col(
                    obs_card,
                    md=4,
                ),
                dbc.Col(
                    vars_card,
                    md=4,
                ),

            ],
            className=["variables-row", "justify-content-center"],
            justify="center"
        ),

        dbc.Row(
            [
                dropdown,
                output
            ],
            className="variables-row",
            justify="center"

        ),
        dbc.Row(
            [
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [table],
                            title="View the Data Dictionary",
                        )
                    ],
                    start_collapsed=True,
                    flush=True,
                    className="data_dict_accor"

                ),
            ],
            justify="center"
        ),
    ]

)


def Variables():
    layout = html.Div([
        nav,
        body
    ])
    return layout
