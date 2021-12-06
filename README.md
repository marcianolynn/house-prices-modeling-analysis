

<img src="https://github.com/marcianolynn/house-prices-modeling-analysis/blob/main/images/Readme%20Image.jpeg" alt="alt text" width="900" height="300">

# house-prices-modeling-analysis

This repo contains all the files for the final project submission of the W207 - Applied Machine Learning at UC Berkeley MIDS. 
This project was completed by Lynn Marciano, Wanyu Li and Jason Cheung.

The goal of this final project was to use the Ames Housing Dataset from [Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) that describes different aspects of residential homes in Ames, Iowa, to form a predictive model for house prices.  In our Jupiter notebook, you will see how we have used exploratory data analysis, feature engineering, PCA, and various models to arrive at our final model. 

In this repo, you will find the following subdirectories:

**dashboard** - a Dash dashboard for in-class presentation

**data** - containing all of the data files used in the Jupiter notebook.  The original dataset from Kaggle contains 79 explanatory variables describing nearly every aspect of residential homes in Ames, Iowa. We took it a step further and expanded the number of variables from 79 to 140+ variables. 

**notebook** - containing the Jupiter notebooks for our baseline submission, final submission and also saved models

**streamlit** - an interactive platform to test our model and get your home price prediction!

---
### Tools used
- Random Forest (RF)
- k-Nearest-Neighbors (kNN)
- eXtreme Gradient Boosting (XGB)
- Catboost
- Shap
- Optuna

- Dash <img src="https://github.com/marcianolynn/house-prices-modeling-analysis/blob/main/images/Dash_by_plotly.jpeg" alt="alt text" width="100" height="50">

- Streamlit <img src="https://github.com/marcianolynn/house-prices-modeling-analysis/blob/main/images/streamlit-logo-secondary-colormark-darktext.svg" alt="alt text" width="100" height="50">

---
### Sample screenshot of Dash visualization
<img src="https://github.com/marcianolynn/house-prices-modeling-analysis/blob/main/images/image.png" alt="alt text" width="1000" height="800">

---
### References
1. Data dictionary and raw data - https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data
2. Missing Values, Ordinal data and stories - https://www.kaggle.com/mitramir5/missing-values-ordinal-data-and-stories/notebook
3. House Price Feature Engineering using only XGB - https://www.kaggle.com/filterjoe/house-price-feature-engineering-using-only-xgboost#Step-2---Feature-Utility-Scores
