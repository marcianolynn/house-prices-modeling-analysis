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
import base64
from sklearn.decomposition import PCA
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
house_img_filename = 'dashboard\\assets\\imgs\\house_dollar.jpg'
house_encoded_image = base64.b64encode(open(house_img_filename, 'rb').read())

fg_img_filename = 'dashboard\\assets\\imgs\\fg_calc.png'
fg_encoded_image = base64.b64encode(open(fg_img_filename, 'rb').read())

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
                                 house_encoded_image.decode()),
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

fg_target_overview = dbc.Card(
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

# brief overview of the feature engineering
fg_overview = dbc.Card(
    dbc.CardBody(
        [
            dcc.Markdown('''
                        # Feature Engineering
                        
                        Due to the observations that our initial target variable, "SalePrice" did not have a normal distribution,
                        we created a new target variable, **Sale Price per Square Foot**, for our observations.
                        
                        With our new target variable, we applied the same logic to the other variables.
                        
                        **Value:**
                        
                        * Identifying a normally distributed variable allows for easier observations during statistical testing
                        * Creating new engineered variables will bring more value to our dataset to improve our models
                        '''),
            dbc.Col(
                html.Div(
                    [
                        html.Img(
                            src='data:image/png;base64,{}'.format(
                                fg_encoded_image.decode()),
                            style={
                                'height': '90%',
                                'width': '90%'}
                        ),
                    ]
                ), style={'textAlign': 'center'})
        ]
    ),
    style={
        'width': 'auto'
    }
)

# overview of other engineered variables
fg_other_info = dbc.Card(
    [
        dbc.CardHeader(html.B("Engineered Variables"),
                       style={'background-color': 'rgb(229,236,246)'}),
        dbc.CardBody(
            dcc.Markdown('''
                        As mentioned, we combined our variables with the same logic with our new target variable\
                        and created other new variables based on similar expected features
                        
                        * **Indoor Area** = Ground Living Area + Total Basement sq. ft.
                        * **Sale Price per Indoor Area** = Sale Price / Indoor Area
                        * **Year after Remodel** = Year Sold – Year Remodel Add
                        * **Year after Built** = Year Sold – Year Built
                        * **Total Rooms above Ground per Ground Living Area** = Total Rooms above Ground / Ground Living Area
                        * **Total Bathrooms in Basement** = No. of Full Bathrooms in Basement + No. of Half Bathrooms in Basement
                        * **Total Bathrooms above Ground** = No. of Full Bathrooms above Ground + No. of Half Bathrooms above Ground.
                        
                        70 other variables by dividing the original variables in the dataset by Indoor Area,\
                            and recoding variables into binary on whether or not they have a valid value.
                        ''')
        )
    ]
)

#overview of PCA we did for reducing models
pca_overview = dbc.Card(
    dbc.CardBody(
        [
            dcc.Markdown('''
                        # Principal Component Analysis
                        We observe the PCA for our newly engineered variables.
                        
                        Since there are 17 variables related to the area of the house, they could be highly correlated and
                        be considered to demonstrate multiollinearity.
                        
                        For example, houses with a large above ground area will almost certainly also have a large first floor area.
                         
                        Therefore, we decided to put these 17 variables through PCA and aimed to retain at least 99.9% of the variability.  
                        As a result, we were able to reduce the number of variables from 17 to 7, with a 60% reduction and still able to maintain 99.9% of the cumulative variance.
                        '''),
        ]
    ),
    style={
        'width': 'auto'
    }
)

# create histogram plots of the target variables
init_target_hist = px.histogram(
    df['SalePrice'],
    x="SalePrice",
    color_discrete_sequence=["rgb(98,83,119)"]
)

init_target_hist.update_layout(
    xaxis_title="Sale Price",
    yaxis_title="Count",
    font=dict(
        size=18,
        color="rgb(98,83,119)"
    )
)

fen_target_hist = px.histogram(
    df_FEN['FE_SalePrice_Per_IndoorArea'],
    x="FE_SalePrice_Per_IndoorArea",
    color_discrete_sequence=["rgb(175,100,88)"]
)

fen_target_hist.update_layout(
    xaxis_title="Sale Price per Square Foot",
    yaxis_title="Count",
    font=dict(
        size=18,
        color="rgb(175,100,88)"
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

# get the PCA results
def get_PCA():
    pca_results = pd.read_csv(r'data\\PCA results.csv')
    pca_features = list(pca_results['Area Factors'])

    exp_var_cumul = list(pca_results['Cumulative Sum of Explained Variance Ratio'])

    pca_plot = px.area(
        x=range(1, len(exp_var_cumul) + 1),
        y=exp_var_cumul,
        labels={"x": "# Components", "y": "Explained Variance"},
        color_discrete_sequence=["rgb(82,106,131)"]
    ).update_layout(
        yaxis_range=[0.98,1]
    )
    
    return pca_plot


# make the EDA tab
eda_tab = dbc.Tab(
    [
        dbc.Row(
            [
                dbc.Col(
                    [eda_overview],
                    md=4
                ),
                dbc.Col(
                    [fg_target_overview],
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
    ],
    label="Initial Exploratory Data Analysis"
)

fg_tab = dbc.Tab(
    [
        dbc.Row(
            [
                dbc.Col(
                    [fg_overview],
                    md=6
                ),
                dbc.Col(
                    [fg_other_info],
                    md=6
                )
            ],
            className="eda-row",
            justify="center"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [pca_overview],
                    md=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='fen_target',
                        figure=get_PCA()
                    ),
                    md=6
                )
            ],
            className="eda-row",
            justify="center"
        )
    ],
    label="Feature Engineering"
)


# define layout
body = dbc.Container(
    [
        dbc.Tabs(
            [
                eda_tab,
                fg_tab
            ],
            className='eda_tabs'

        )
    ]
)


def EDA():
    layout = html.Div([
        nav,
        body
    ])
    return layout
