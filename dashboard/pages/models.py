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
from dash import dash_table
import base64
# Navbar
from pages.navbar import Navbar

nav = Navbar()

# model accuracy summary
acc_df = pd.read_csv(
    r'data/Accuracy_Summary.csv').drop(columns=['SN', 'Metric Kaggle'])

# assets
# home price image
RF_img_filename = 'dashboard\\assets\\imgs\\RF.png'
RF_encoded_image = base64.b64encode(open(RF_img_filename, 'rb').read())

KNN_img_filename = 'dashboard\\assets\\imgs\\knn.png'
KNN_encoded_image = base64.b64encode(open(KNN_img_filename, 'rb').read())

CB_img_filename = 'dashboard\\assets\\imgs\\catboost.png'
CB_encoded_image = base64.b64encode(open(CB_img_filename, 'rb').read())

XG_img_filename = 'dashboard\\assets\\imgs\\xgboost.png'
XG_encoded_image = base64.b64encode(open(XG_img_filename, 'rb').read())

opt_img_filename = 'dashboard\\assets\\imgs\\optuna.gif'
opt_encoded_image = base64.b64encode(open(opt_img_filename, 'rb').read())

tree_imag_filename= 'dashboard\\assets\\imgs\\tree_history.png'
tree_encoded_image = base64.b64encode(open(tree_imag_filename, 'rb').read())

def create_img_div(encoded_img, img_type):
    if img_type == 'png':
        img_div = html.Div(
            [
                html.Img(
                    src='data:image/png;base64,{}'.format(
                        encoded_img.decode()),
                    style={
                        'height': '80%',
                        'width': '80%'}
                ),
            ]
        )
    else:
        img_div = html.Div(
            [
                html.Img(
                    src='data:image/gif;base64,{}'.format(
                        encoded_img.decode()),
                    style={
                        'height': '80%',
                        'width': '80%'}
                ),
            ]
        )

    return img_div


rf_img = create_img_div(RF_encoded_image, 'png')
knn_img = create_img_div(KNN_encoded_image, 'png')
xg_img = create_img_div(XG_encoded_image, 'png')
cb_img = create_img_div(CB_encoded_image, 'png')
optuna_gif = create_img_div(opt_encoded_image, 'gif')
tree_hist_img = create_img_div(tree_encoded_image, 'png')

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


def create_base_tab(info, rmse, vars, img_div):
    body = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        img_div
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                [info],
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
                        ],
                        md=8
                    ),
                ],
                className='model-tab-content'
            )
        ],

    )
    return body


base_model1_desc = dcc.Markdown(
    '''
    We used a Random Forest model as our initial baseline model.

    There were 79 features trained in this model from the cleaned and processed dataset.

    ** OVERVIEW: **
    * Grows a forest of decision trees
    * Data from these trees are then merged together to ensure the most accurate predictions
    * Forest assures a more accurate result with a larger number of groups and decisions rather than the narrowness of a single tree
    * Benefit of adding randomness
    * Finds the best feature among a random subset of features
    '''
)
base_model1_info = create_base_info('Random Forest', base_model1_desc)
base_model1_rmse = create_rmse_info(29433)
base_model1_vars = create_var_info(73)
base_model1_tab = create_base_tab(
    base_model1_info, base_model1_rmse, base_model1_vars, rf_img)

base_model2_desc = dcc.Markdown(
    '''
    We used a k-Nearest Neighbors Model as a comparison to the baseline model.

    There were 129 features trained in this model from the cleaned and processed dataset.

    ** OVERVIEW: **
    * Assumes that similar things exist in close proximity
    * Captures idea of similarity in distance, proximity, or closeness
    * Euclidean distance is the popular and familiar choice to calculate distance

    '''
)
base_model2_info = create_base_info('KNN', base_model2_desc)
base_model2_rmse = create_rmse_info(32175)
base_model2_vars = create_var_info(129)
base_model2_tab = create_base_tab(
    base_model2_info, base_model2_rmse, base_model2_vars, knn_img)

base_model3_desc = dcc.Markdown(
    '''
    As we used a Random Forest model for our baseline model, we wanted to compare the results to a model that contained all engineered features.

    There were 129 features trained in this model from the cleaned and processed dataset.
    '''
)
base_model3_info = create_base_info('Random Forest', base_model3_desc)
base_model3_rmse = create_rmse_info(24520)
base_model3_vars = create_var_info(129)
base_model3_tab = create_base_tab(
    base_model3_info, base_model3_rmse, base_model3_vars, rf_img)

base_model4_desc = dcc.Markdown(
    '''
    We use an XGBoost model to investigate different boosting techniques as a comparison to the baseline model.

    There were 129 features trained in this model from the cleaned and processed dataset.

    ** OVERVIEW: **
    * Implementation of the Gradient Boosting method
    * Uses more accurate approximations to find the best tree model
    * Computes second-order gradients, i.e. second partial derivatives of the loss function
    * Advanced regularization (L1 & L2), which improves model generalization
    * Training is very fast and can be parallelized / distributed across clusters
    '''
)
base_model4_info = create_base_info('XGB Boost', base_model4_desc)
base_model4_rmse = create_rmse_info(21362)
base_model4_vars = create_var_info(129)
base_model4_tab = create_base_tab(
    base_model4_info, base_model4_rmse, base_model4_vars, xg_img)

# load summary of model accuracies
acc_table = dash_table.DataTable(
    id='var_table',
    columns=[{"name": i, "id": i} for i in acc_df.columns],
    data=acc_df.to_dict('records'),
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
        'width': '1200px'},
    style_cell={
        'textAlign': 'left',
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
        'height': '50px'},
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold'
    }
)


# get final model info
def make_final_cards(title, description, color_val):
    feat_card = dbc.Col(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H1(title, className="card-title"),
                        html.P(
                            description,
                            className="card-text",
                        )
                    ]
                ),
                style={"width": "17rem"},
                color=color_val,
                inverse=True
            ),
        ],
    )
    return feat_card


feat_card = make_final_cards(str(129), 'Features', "rgb(104,133,92)")
rmse_card = make_final_cards(str(19901), 'RMSE', "rgb(124,124,124)")
dev_acc_card = make_final_cards(
    str(1.01), 'Dev (Training) Accuracy', "rgb(175,100,88)")
test_acc_card = make_final_cards(
    str(1.29), 'Kaggle (Test) Accuracy', "rgb(217,175,107)")

# catboost overview
catboost_info = dbc.Card(
    [
        dbc.CardHeader(html.B("Catboost Overview"),
                       style={'background-color': 'rgb(229,236,246)'}),
        dbc.CardBody(
            dcc.Markdown('''
                        Catboosting builds decision tree sequentially to predict residuals from the previous tress.

                        We chose catboost as our final model due to:
                        * User friendly categorical handling
                            * Target handling is applied if specified
                        * Faster than XGBoost
                            * Minimal Variance Sampling Technique
                        * More stable than lightGBM
                            * Full rank tree structure
                        ''')
        )
    ]
)

# optuna info
optuna_info = dbc.Card(
    [
        dbc.CardHeader(html.B("Optuna Overview"),
                       style={'background-color': 'rgb(229,236,246)'}),
        dbc.CardBody(
            dcc.Markdown('''
                        Optuna allowed us to enhance our modeling training to achieve optimal results

                        * Utilizes a traditional searchCV brute force method
                        * Hyperparameter optimization coiciding with the gradient descent algorithm
                        ''')
        )
    ]
)

final_body = dbc.Container(
    [
        dbc.Row(
            cb_img,
            className="variables-row",
            justify="center"),
        dbc.Row(
            [
                feat_card,
                rmse_card,
                dev_acc_card,
                test_acc_card
            ],
            className=["final-models-row"]
        ),
        dbc.Row(
            [
                dbc.Col(
                    catboost_info,
                    md=4,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            optuna_info
                        ),
                        dbc.Row(
                            dbc.Button(
                                "View our Streamlit Final Model Implementation",
                                href="https://share.streamlit.io/stjokerli/stream_lite_showcase/main/main.py",
                                external_link=True,
                                color="secondary",
                                size='lg'),
                            className="variables-row",
                            justify="center"
                        ),

                    ],
                    md=5
                )
            ],
            className="eda-row",
            justify="center"
        ),
        dbc.Row(
            optuna_gif,
            className="variables-row",
            justify="center"
        )

    ]
)

tabs = dbc.Tabs(
    [
        dbc.Tab(base_model1_tab, label="Baseline Model - Random Forest"),
        dbc.Tab(base_model2_tab, label="Comparing Model 1 - KNN"),
        dbc.Tab(base_model3_tab, label="Comparing Model 2 - Random Forest"),
        dbc.Tab(base_model4_tab, label="Comparing Model 3 - XGBoost"),
        dbc.Tab(
            dbc.Container(
                dbc.Row(
                    acc_table,
                    className='model-summary')
            ),
            label="Model Summary")
    ]
)

body = dbc.Container(
    [   dbc.Row(dbc.Card(
                [
                    dbc.CardHeader(
                        html.H1("Tree Algorithm Timeline")
                    ),
                    dbc.CardBody(
                        tree_hist_img
                    )
                ]
            ),
            className='tree history'
        ),
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
            ),
            className='model-tabs'
        ),
        dbc.Row(
            [final_body]
        )
    ]
)


def Models():
    layout = html.Div([
        nav,
        body
    ])
    return layout
