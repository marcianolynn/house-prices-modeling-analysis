import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import base64

from navbar import Navbar

#navbar
nav = Navbar()

#dataset
df = pd.read_csv(r'house-prices-analytics\data\train.csv',
                 index_col=0, parse_dates=True)

# provide a write up of the overview of the dashboard
overview = dcc.Markdown('''
                        This interactive analysis dashboard provides insight on the [Ames Housing Dataset](http://jse.amstat.org/v19n3/decock.pdf)
                        that contains 2930 observations and 79 explanatory variables involved in assessing the home values in Ames, Iowa.
                        
                        The goal of the analysis is to create a model to predict the final price of each home in the dataset.
                        
                        With the dataset, we perform exploratory data analysis and practice *feature engineering, RFs, and gradient boosing* in order to develop our model.
                        ''')

#homepage image
image_filename = 'house-prices-analytics\\assets\\ames.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("Overview"),
                        overview,
                        dbc.Button("View Kaggle Competition Details", color="secondary", 
                                   href="https://www.kaggle.com/c/house-prices-advanced-regression-techniques/overview"),
                    ],
                    md=4,
                ),
                dbc.Col(
                    [
                        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                 style={'height':'70%', 'width':'70%'}),
                    ],
                    style={'textAlign': 'center'}
                )
            ],
            align="center"
        )
    ],
    className="overview-border",
)


def Homepage():
    layout = html.Div([
        nav,
        body
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Homepage()
if __name__ == "__main__":
    app.run_server()
