import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
import pickle
from sklearn.metrics import mean_squared_error
import catboost
import matplotlib.pyplot as pl
import shap
from st_aggrid import AgGrid

# model_path="../020_code/model/"
model_path="./model/"

pca_file=model_path+"pca.pkl"
cat_file=model_path+"model.pkl"

# data_path="../010_data/"

data_path="./010_data/"
train_data=data_path+"train_after_treatment.csv"


# define categorical values
cat_values={
    'MSZoning': ['None','A','C','FV','I','RH','RL', 'RP' , 'RM'],
    'Street': ['None', 'Pave', 'Grvl'],
    'LandContour': ['None', 'Lvl', 'Bnk', 'HLS', 'Low'],
    'Utilities': ['None', 'AllPub', 'NoSewr', 'NoSeWa', 'ELO'],
    'LotConfig': ['None', 'Inside', 'Corner', 'CulDSac', 'FR2', 'FR3'],
    'LandSlope': ['None', 'Gtl', 'Mod', 'Sev'],
    'Neighborhood': ['None',"Blmngtn","Bluestem","BrDale","BrkSide",
                     "ClearCr","CollgCr","Crawfor","Edwards",
                     "Gilbert","IDOTRR","MeadowV","Mitchel",
                     "Names","NoRidge","NPkVill","NridgHt",
                     "NWAmes","OldTown","SWISU","Sawyer",
                     "SawyerW","Somerst","StoneBr","Timber","Veenker"],
    'Condition1': ['None',  'Artery', 'Feedr',  'Norm',
                   'RRNn',  'RRAn', 'PosN', 'PosA',
                   'RRNe',  'RRAe'],
    'Condition2':  ['None',  'Artery', 'Feedr',  'Norm',
                    'RRNn',  'RRAn', 'PosN', 'PosA',
                    'RRNe',  'RRAe'],
    'BldgType': ['None', '1Fam', '2fmCon', 'Duplex', 'TwnhsE', 'TwnhsI'],
    'HouseStyle': ['None',  '1Story',  '1.5Fin',  '1.5Unf', 
                   '2Story',  '2.5Fin',  '2.5Unf',  'SFoyer',  'SLvl'],
    'RoofStyle': ['None', 'Gable', 'Hip', 'Gambrel', 
                  'Mansard', 'Flat', 'Shed'],
    'RoofMatl': ['None',  'ClyTile', 'CompShg',  'Membran',  
                 'Metal',  'Roll', 'Tar&Grv',  'WdShake',  'WdShngl'],
    'Exterior1st': ['None',  'AsbShng',  'AsphShn',  'BrkComm',  
                    'BrkFace',  'CBlock',  'CemntBd',  'HdBoard',
                    'ImStucc', 'MetalSd',  'Other',  
                    'Plywood',  'PreCast',  'Stone',  
                    'Stucco', 'VinylSd', 'Wd Sdng',  'WdShing'],
    'Exterior2nd': ['None',  'AsbShng',  'AsphShn',  'BrkComm',  
                    'BrkFace',  'CBlock',  'CemntBd',  'HdBoard',
                    'ImStucc', 'MetalSd',  'Other',  
                    'Plywood',  'PreCast',  'Stone',  
                    'Stucco', 'VinylSd', 'Wd Sdng',  'WdShing'],
    'MasVnrType': ['None', 'BrkFace', 'Stone', 'BrkCmn'],
    'Foundation': ['None', 'PConc', 'CBlock', 'BrkTil', 
                   'Wood', 'Slab', 'Stone'],
    'Heating': ['None', 'GasA', 'GasW', 'Grav', 'Wall', 'OthW', 'Floor'],
    'CentralAir': ['None', 'Y', 'N'],
    'Electrical': ['None', 'SBrkr', 'FuseF', 'FuseA', 'FuseP', 'Mix'],
    'GarageType': ['None', 'Attchd', 'Detchd', 'BuiltIn', 
                   'CarPort', 'Basment', '2Types'],
    'SaleType': ['None', 'WD','CWD', 'VWD', 'New', 'COD',
                'ConLD',  'ConLI',  'ConLw',  'Con',  'Oth'],
    'SaleCondition': ['None',  'Normal',  'Abnorml',  'Partial',  'AdjLand',  'Alloca',  'Family'], 
    'MSSubClass':['None',20,30,40,45,50,60,70,75,80,85,90,120,150,160,180,190],
    'ExterQual':['None','Po','Fa','TA','Gd','Ex'],
    'LotShape':['None','Reg','IR1' ,'IR2','IR3'],
    'ExterCond':['None','Po','Fa','TA','Gd','Ex'],
    'BsmtQual':['None','Fa','TA','Gd','Ex'],
    'BsmtCond':['None','Po','Fa','TA','Gd','Ex'],
    'BsmtExposure':['None','No','Mn','Av','Gd'],
    'BsmtFinType1':['None','Unf','LwQ', 'Rec','BLQ','ALQ' , 'GLQ' ],
    'BsmtFinType2':['None','Unf','LwQ', 'Rec','BLQ','ALQ' , 'GLQ' ],
    'HeatingQC':['None','Po','Fa','TA','Gd','Ex'],
    'Functional':['None','Sev','Maj2','Maj1','Mod','Min2','Min1','Typ'],
    'KitchenQual':['None','Fa','TA','Gd','Ex'],
    'GarageFinish':['None','Unf','RFn','Fin'],
    'GarageQual':['None','Po','Fa','TA','Gd','Ex'],
    'GarageCond':['None','Po','Fa','TA','Gd','Ex'],
    'PavedDrive':['None','N','P',  'Y'],
    'PoolQC':['None','Po','Fa','TA','Gd','Ex'],
    'MiscFeature':['None','Elev','Gar2','Othr','Shed','TenC'],
    'Alley':['None','Grvl','Pave'],
    'Fence':['None','MnWw','GdWo','MnPrv','GdPrv'],
    'FireplaceQu':['None','Po','Fa','TA','Gd','Ex'],
}

# Drop the columns with more than 10% missing values
col_drop=['Id']

# Name categorical variables
col_cat=['MSSubClass', #building class
         'MSZoning', #general zoning classification
         'Street', #road access
         'LandContour', #flatness of property
         'Utilities', #type of utilities avail
         'LotConfig', #lot configuration
         'LandSlope', #slope of property
         'Neighborhood', #physical neighborhoods within Ames
         'Condition1', #proximity to certain landmarks
         'Condition2', #proximity to certain landmarks (if more than one present)
         'BldgType', #type of dwelling
         'HouseStyle', #how many floors/type of dwelling
         'RoofStyle', #type of roof
         'RoofMatl', #roof material
         'Exterior1st', #exterior covering on the house
         'Exterior2nd', #exterior covering on the house (if more than one present)
         'MasVnrType', #masonry veneer type
         'Foundation', #type of foundation
         'Heating', #type of heating
         'CentralAir', #boolean if central air is avail
         'Electrical', #type of electrical system
         'GarageType', #garage location
         'SaleType', #type of sale
         'SaleCondition', #condition of sale
         'MiscFeature', #Miscellaneous feature not covered in other categories

        ]

# Name ordinal variables -- these are string value ordinals
col_order=['ExterQual', #Evaluates the quality of the material on the exterior 
           'LotShape', #general shape of the property
           'ExterCond', #evaluate present condition of material on exterior
           'BsmtQual', #evaluate height of basement
           'BsmtCond', #evaluate present condition of the basement
           'BsmtExposure', #evaluate ability to walkout or garden level walls
           'BsmtFinType1', #rating of basement finished area
           'BsmtFinType2', #rating of basement finished area (if multiple)
           'HeatingQC', #heating quality & condition
           'Functional', #home functionality (assume typical unless deductions warranted)
           'KitchenQual', #kitchen quality
           'GarageQual', #garage quality
           'GarageFinish', #evaluate interior finish of garage
           'GarageCond', #evaluate garage condition
           'PavedDrive', #evaluate type of driveway based on pavement
           'PoolQC',  # Pool quality
           'Fence', # Fence quality
           'FireplaceQu', # Fireplace quality   
           'Alley', #Type of alley access      
          ]

# Already numerical values -- these may contain numerical ordinal values
col_num_continuous=[
         'LotArea', #Lot size in square feet
         'MasVnrArea', #Masonry veneer area in square feet
         'BsmtFinSF1', #Type 1 finished square feet
         'BsmtFinSF2', #Type 2 finished square feet
         'BsmtUnfSF', #Unfinished square feet of basement area
         'TotalBsmtSF', #Total square feet of basement area
         '1stFlrSF', #First Floor square feet
         '2ndFlrSF', #Second floor square feet
         'LowQualFinSF', #Low quality finished square feet (all floors)
         'GrLivArea', #Above grade (ground) living area square feet
         'GarageArea', #Size of garage in square feet
         'WoodDeckSF', #Wood deck area in square feet
         'OpenPorchSF', #Open porch area in square feet
         'EnclosedPorch', #Enclosed porch area in square feet
         '3SsnPorch', #Three season porch area in square feet
         'ScreenPorch', #Screen porch area in square feet
         'PoolArea', #Pool area in square feet
         'MiscVal', #Value of miscellaneous feature
         'LotFrontage',#Linear feet of street connected to property
        ]

col_num_int=['OverallQual', #evaluate the overall material and finish of the house
         'OverallCond', #evaluate Overall condition rating
         'BsmtFullBath', #Basement full bathrooms
         'BsmtHalfBath', #Basement half bathrooms
         'FullBath', #Full bathrooms above grade
         'HalfBath', #Half baths above grade
         'BedroomAbvGr', #Number of bedrooms above basement level
         'KitchenAbvGr', #Number of kitchens
         'TotRmsAbvGrd', #Total rooms above grade (does not include bathrooms)
         'Fireplaces', #Number of fireplaces
         'GarageCars', #Size of garage in car capacity
         'YearBuilt', #year built
         'YearRemodAdd', #year remodels were added
         'MoSold', #month sold
         'YrSold', #year sold
         'GarageYrBlt' #year garage was built
            ]

missmatch_correction={"MSZoning":{'C (all)':'C'}, 
                      "Neighborhood": {'NAmes':'Names', 'Blueste':'Bluestem'},
                      # assumption:  that Twnhs is a misstypping for TwnhsI
                      "BldgType":{'Twnhs':'TwnhsI'},
                      "Exterior2nd":{'Wd Shng':'Wd Sdng', 'CmentBd':'CemntBd', 'Brk Cmn':'BrkComm'}
                     }


orders_encoding_result={}
for ord_feat in col_order:
    ord_vals=cat_values[ord_feat]
    orders_encoding_result[ord_feat]={}
    for i in range(len(ord_vals)):
        orders_encoding_result[ord_feat][ord_vals[i]]=i

def ImputerConverter(df,col_num,col_order,col_cat,orders_encoding_result):
    df=df.drop(col_drop,axis=1).copy()
    df=df.replace(missmatch_correction)   
    df[col_num_continuous+col_num_int]=df[col_num].fillna(0)
    df[col_num_int]=df[col_num_int].astype(int)
    df[col_order+col_cat]=df[col_order+col_cat].fillna('None')
    df[col_cat]=df[col_cat].astype(str)
    for i in col_order:
        df[i]=df[i].map(orders_encoding_result[i])
    return df
    
def FeatureEngineering(df,pca=None):
    
    df_study=df.copy()
    
    # Create a new variable called FE_SalesPrice_Per_GrLivArea
    # Which stands for sales price per square foot
    df_study['FEN_IndoorArea']=df_study['GrLivArea']+df_study['TotalBsmtSF']+0.01
    # df_study['FE_SalePrice_Per_IndoorArea']=df_study['SalePrice']/df_study['FEN_IndoorArea']

# Will add the below code about feature engineering on final submission

    for e in col_num_continuous:
      if e not in ['MiscVal','LotFrontage'] :
        FE_name='FEN_'+e+'_Per_IndoorArea'
        df_study[FE_name]=df_study[e]/df_study['FEN_IndoorArea']

    for e in col_order+col_num_int+col_num_continuous:
      df_study['FEC_'+e+"_dual"]=np.where(df_study[e]!=0, 1, 0)
    
    df_study['FEN_YearAfterRemode']=df_study['YrSold']-df_study['YearRemodAdd']
    
    df_study['FEN_YearAfterbuilt']=df_study['YrSold']-df_study['YearBuilt']

    # temp=df_study['1stFlrSF']+df_study['2ndFlrSF']+df_study['BsmtFinSF1']
    
    # df_study['FEN_1stFlrSF_Plus_2ndFlrSF_Plus_BsmtFinSF1_per_GrLivArea']=temp/(df_study['GrLivArea']+0.001)
    
    # df_study['FEN_1stFlrSF_Plus_2ndFlrSF_Plus_per_GrLivArea']=(df_study['1stFlrSF']+df_study['2ndFlrSF'])/(df_study['GrLivArea']+0.001)
    
    
    # df_study['FEN_BsmtUnfSF_Per_GrLivArea']=df_study['BsmtUnfSF']/(df_study['GrLivArea']+0.001)
        
    # df_study['FEN_1stFlrSF_Plus_2ndFlrSF_Plus_BsmtFinSF1_plus_BsmtFinSF2_per_GrLivArea']=(df_study['1stFlrSF']+df_study['2ndFlrSF']+df_study['BsmtFinSF1']+df_study['BsmtFinSF2'])/(df_study['GrLivArea']+0.001)
        
    df_study['FEN_TotRmsAbvGrd_Per_GrLivArea']=df_study['TotRmsAbvGrd']/(df_study['GrLivArea']+0.001)
            
    df_study['FEN_BsmtTotalbath']=df_study['BsmtFullBath']+df_study['BsmtHalfBath']
    df_study['FEN_GrLivTotalbath']=df_study['FullBath']+df_study['HalfBath']

    if pca==None:
      pass
    else:
      df_study=pca_transform(df_study,pca)
#     col_FE=[i for i in df_study.columns if (('FE' in i) and ('FE_SalePrice_Per_IndoorArea' not in i))]
    
#     print(col_FE)
    # df_study_norm=df_study.drop(['FE_SalePrice_Per_IndoorArea','SalePrice'],axis=1).groupby('Neighborhood').transform(lambda x: (x - x.mean()) / x.std())
        
    # df_study_norm.columns=['nrm_Neighborhood_'+i for i in df_study_norm.columns]

    # # df_study_norm.,inplace=True)
    
    # return  pd.concat([df_study,df_study_norm],axis=1)

    col_FE_num=[i for i in df_study.columns if ('FEN_' in i)& ('nrm_' not in i) ]
    col_FE_cat=[i for i in df_study.columns if ('FEC_' in i)& ('nrm_' not in i) ]

    return df_study,col_FE_num,col_FE_cat


pca = pickle.load(open(pca_file,'rb'))

def pca_transform(df_input,pca_model):
  
  Area_factors=['FEN_LotArea_Per_IndoorArea',
 'FEN_MasVnrArea_Per_IndoorArea',
 'FEN_BsmtFinSF1_Per_IndoorArea',
 'FEN_BsmtFinSF2_Per_IndoorArea',
 'FEN_BsmtUnfSF_Per_IndoorArea',
 'FEN_TotalBsmtSF_Per_IndoorArea',
 'FEN_1stFlrSF_Per_IndoorArea',
 'FEN_2ndFlrSF_Per_IndoorArea',
 'FEN_LowQualFinSF_Per_IndoorArea',
 'FEN_GrLivArea_Per_IndoorArea',
 'FEN_GarageArea_Per_IndoorArea',
 'FEN_WoodDeckSF_Per_IndoorArea',
 'FEN_OpenPorchSF_Per_IndoorArea',
 'FEN_EnclosedPorch_Per_IndoorArea',
 'FEN_3SsnPorch_Per_IndoorArea',
 'FEN_ScreenPorch_Per_IndoorArea',
 'FEN_PoolArea_Per_IndoorArea',]

  df=pca_model.transform(df_input[Area_factors])
  df = pd.DataFrame(df,columns=['FEN_Area_comp0','FEN_Area_comp1','FEN_Area_comp2','FEN_Area_comp3','FEN_Area_comp4','FEN_Area_comp5','FEN_Area_comp7'],index=df_input.index)
  # display(df_original)
  return pd.concat([df_input.drop(Area_factors,axis=1) ,df],axis=1)

# pca_transform(df_study,pca)

feature_list=['MiscVal',
 'LotFrontage',
 'FEN_IndoorArea',
 'FEN_YearAfterRemode',
 'FEN_YearAfterbuilt',
 'FEN_TotRmsAbvGrd_Per_GrLivArea',
 'FEN_BsmtTotalbath',
 'FEN_GrLivTotalbath',
 'FEN_Area_comp0',
 'FEN_Area_comp1',
 'FEN_Area_comp2',
 'FEN_Area_comp3',
 'FEN_Area_comp4',
 'FEN_Area_comp5',
 'FEN_Area_comp7',
 'MSSubClass',
 'MSZoning',
 'Street',
 'LandContour',
 'Utilities',
 'LotConfig',
 'LandSlope',
 'Neighborhood',
 'Condition1',
 'Condition2',
 'BldgType',
 'HouseStyle',
 'RoofStyle',
 'RoofMatl',
 'Exterior1st',
 'Exterior2nd',
 'MasVnrType',
 'Foundation',
 'Heating',
 'CentralAir',
 'Electrical',
 'GarageType',
 'SaleType',
 'SaleCondition',
 'MiscFeature',
 'ExterQual',
 'LotShape',
 'ExterCond',
 'BsmtQual',
 'BsmtCond',
 'BsmtExposure',
 'BsmtFinType1',
 'BsmtFinType2',
 'HeatingQC',
 'Functional',
 'KitchenQual',
 'GarageQual',
 'GarageFinish',
 'GarageCond',
 'PavedDrive',
 'PoolQC',
 'Fence',
 'FireplaceQu',
 'Alley',
 'OverallQual',
 'OverallCond',
 'BsmtFullBath',
 'BsmtHalfBath',
 'FullBath',
 'HalfBath',
 'BedroomAbvGr',
 'KitchenAbvGr',
 'TotRmsAbvGrd',
 'Fireplaces',
 'GarageCars',
 'YearBuilt',
 'YearRemodAdd',
 'MoSold',
 'YrSold',
 'GarageYrBlt',
 'FEC_ExterQual_dual',
 'FEC_LotShape_dual',
 'FEC_ExterCond_dual',
 'FEC_BsmtQual_dual',
 'FEC_BsmtCond_dual',
 'FEC_BsmtExposure_dual',
 'FEC_BsmtFinType1_dual',
 'FEC_BsmtFinType2_dual',
 'FEC_HeatingQC_dual',
 'FEC_Functional_dual',
 'FEC_KitchenQual_dual',
 'FEC_GarageQual_dual',
 'FEC_GarageFinish_dual',
 'FEC_GarageCond_dual',
 'FEC_PavedDrive_dual',
 'FEC_PoolQC_dual',
 'FEC_Fence_dual',
 'FEC_FireplaceQu_dual',
 'FEC_Alley_dual',
 'FEC_OverallQual_dual',
 'FEC_OverallCond_dual',
 'FEC_BsmtFullBath_dual',
 'FEC_BsmtHalfBath_dual',
 'FEC_FullBath_dual',
 'FEC_HalfBath_dual',
 'FEC_BedroomAbvGr_dual',
 'FEC_KitchenAbvGr_dual',
 'FEC_TotRmsAbvGrd_dual',
 'FEC_Fireplaces_dual',
 'FEC_GarageCars_dual',
 'FEC_YearBuilt_dual',
 'FEC_YearRemodAdd_dual',
 'FEC_MoSold_dual',
 'FEC_YrSold_dual',
 'FEC_GarageYrBlt_dual',
 'FEC_LotArea_dual',
 'FEC_MasVnrArea_dual',
 'FEC_BsmtFinSF1_dual',
 'FEC_BsmtFinSF2_dual',
 'FEC_BsmtUnfSF_dual',
 'FEC_TotalBsmtSF_dual',
 'FEC_1stFlrSF_dual',
 'FEC_2ndFlrSF_dual',
 'FEC_LowQualFinSF_dual',
 'FEC_GrLivArea_dual',
 'FEC_GarageArea_dual',
 'FEC_WoodDeckSF_dual',
 'FEC_OpenPorchSF_dual',
 'FEC_EnclosedPorch_dual',
 'FEC_3SsnPorch_dual',
 'FEC_ScreenPorch_dual',
 'FEC_PoolArea_dual',
 'FEC_MiscVal_dual',
 'FEC_LotFrontage_dual']


#1461,20,RH,80,11622,Pave,NA,Reg,Lvl,AllPub,Inside,Gtl,NAmes,Feedr,Norm,1Fam,1Story,5,6,1961,1961,Gable,CompShg,VinylSd,VinylSd,None,0,TA,TA,CBlock,TA,TA,No,Rec,468,LwQ,144,270,882,GasA,TA,Y,SBrkr,896,0,0,896,0,0,1,0,2,1,TA,5,Typ,0,NA,Attchd,1961,Unf,1,730,TA,TA,Y,140,0,0,0,120,0,NA,MnPrv,NA,0,6,2010,WD,Normal
#1461,20,RH,80,11622,Pave,NA,Reg,Lvl,AllPub,Inside,Gtl,NAmes,Feedr,Norm,1Fam,1Story,7,7,1961,2010,Gable,CompShg,VinylSd,VinylSd,None,0,TA,TA,CBlock,Ex,Gd,No,Rec,468,LwQ,144,270,882,GasA,TA,Y,SBrkr,896,0,0,896,0,0,1,0,2,1,TA,5,Typ,0,NA,Attchd,1961,Unf,1,730,TA,TA,Y,140,0,0,0,120,0,NA,MnPrv,NA,0,6,2010,WD,Normal
#1461,20,RH,80,11622,Pave,NA,Reg,Lvl,AllPub,Inside,Gtl,NAmes,Feedr,Norm,1Fam,1Story,7,7,1961,2010,Gable,CompShg,VinylSd,VinylSd,None,0,TA,TA,CBlock,Ex,Gd,No,GLQ,468,LwQ,144,270,882,GasA,TA,Y,SBrkr,896,0,0,896,0,0,1,0,2,1,TA,5,Typ,0,NA,Attchd,1961,Unf,1,730,TA,TA,Y,140,0,0,0,120,0,NA,MnPrv,NA,0,6,2010,WD,Normal



image = Image.open('./image/header.png')

st.image(image,use_column_width=True)

st.write ("""

# Welcome to our House Pricing App! 

> Kind reminder:

> All models are wrong but some models are useful. 

>by George EP Box

""")

# Id,MSSubClass,MSZoning,LotFrontage,LotArea,Street,Alley,LotShape,LandContour,Utilities,LotConfig,LandSlope,Neighborhood,Condition1,Condition2,BldgType,HouseStyle,OverallQual,OverallCond,YearBuilt,YearRemodAdd,RoofStyle,RoofMatl,Exterior1st,Exterior2nd,MasVnrType,MasVnrArea,ExterQual,ExterCond,Foundation,BsmtQual,BsmtCond,BsmtExposure,BsmtFinType1,BsmtFinSF1,BsmtFinType2,BsmtFinSF2,BsmtUnfSF,TotalBsmtSF,Heating,HeatingQC,CentralAir,Electrical,1stFlrSF,2ndFlrSF,LowQualFinSF,GrLivArea,BsmtFullBath,BsmtHalfBath,FullBath,HalfBath,BedroomAbvGr,KitchenAbvGr,KitchenQual,TotRmsAbvGrd,Functional,Fireplaces,FireplaceQu,GarageType,GarageYrBlt,GarageFinish,GarageCars,GarageArea,GarageQual,GarageCond,PavedDrive,WoodDeckSF,OpenPorchSF,EnclosedPorch,3SsnPorch,ScreenPorch,PoolArea,PoolQC,Fence,MiscFeature,MiscVal,MoSold,YrSold,SaleType,SaleCondition\n
# 1461,20,RH,80,11622,Pave,NA,Reg,Lvl,AllPub,Inside,Gtl,NAmes,Feedr,Norm,1Fam,1Story,5,6,1961,1961,Gable,CompShg,VinylSd,VinylSd,None,0,TA,TA,CBlock,TA,TA,No,Rec,468,LwQ,144,270,882,GasA,TA,Y,SBrkr,896,0,0,896,0,0,1,0,2,1,TA,5,Typ,0,NA,Attchd,1961,Unf,1,730,TA,TA,Y,140,0,0,0,120,0,NA,MnPrv,NA,0,6,2010,WD,Normal


df_train_after_treatment=pd.read_csv(train_data)

st.sidebar.header('Select to filter the data')

# Sidebar - Neighborhood selection
sorted_unique_Neighborhood = sorted(df_train_after_treatment.Neighborhood.unique())
sorted_Neighborhood = st.sidebar.multiselect('Neighborhood', sorted_unique_Neighborhood, sorted_unique_Neighborhood)

# Sidebar - Buildyear Selection
a=float(df_train_after_treatment.YearBuilt.max())
b=float(df_train_after_treatment.YearBuilt.min())
selected_year = st.sidebar.slider('Build Year', a,b,(a,b),step =1.0)
selected_year=range(int(selected_year[0]),int(selected_year[1]+1))

# Sidebar - Position selection
a=float(df_train_after_treatment.FEN_IndoorArea.max())
b=float(df_train_after_treatment.FEN_IndoorArea.min())
selected_IndoorArea = st.sidebar.slider('IndoorArea', a,b,(a,b),step =1.0)
st.sidebar.write(selected_IndoorArea)

# Filtering data
df_selected_train_after_treatment = df_train_after_treatment[(df_train_after_treatment.Neighborhood.isin(sorted_Neighborhood)) &
                                                               (df_train_after_treatment.YearBuilt.isin(selected_year)) &
                                                               (df_train_after_treatment.FEN_IndoorArea<=selected_IndoorArea[1]) &
                                                               (df_train_after_treatment.FEN_IndoorArea>=selected_IndoorArea[0])
                                                               ]

st.header('Display House Info filtered by selected criteria')
st.write('Data Dimension: ' + str(df_selected_train_after_treatment.shape[0]) + ' rows and ' + str(df_selected_train_after_treatment.shape[1]) + ' columns.')
st.dataframe(df_selected_train_after_treatment)




st.header("Input House Info")

st.write("""Id,MSSubClass,MSZoning,LotFrontage,LotArea,Street,Alley,LotShape,LandContour,
Utilities,LotConfig,LandSlope,Neighborhood,Condition1,Condition2,BldgType,HouseStyle,OverallQual,
OverallCond,YearBuilt,YearRemodAdd,RoofStyle,RoofMatl,Exterior1st,Exterior2nd,MasVnrType,MasVnrArea,
ExterQual,ExterCond,Foundation,BsmtQual,BsmtCond,BsmtExposure,BsmtFinType1,BsmtFinSF1,
BsmtFinType2,BsmtFinSF2, BsmtUnfSF,TotalBsmtSF,Heating,HeatingQC,CentralAir,Electrical,1stFlrSF, 
2ndFlrSF,LowQualFinSF,GrLivArea,BsmtFullBath,BsmtHalfBath,FullBath,HalfBath,BedroomAbvGr,KitchenAbvGr,
KitchenQual,TotRmsAbvGrd,Functional,Fireplaces,FireplaceQu,GarageType,GarageYrBlt,GarageFinish,
GarageCars,GarageArea,GarageQual,GarageCond,PavedDrive,WoodDeckSF,OpenPorchSF,EnclosedPorch,
3SsnPorch,ScreenPorch,PoolArea,PoolQC,Fence,MiscFeature,MiscVal,MoSold,YrSold,SaleType,SaleCondition""")

col_names=["Id",
  "MSSubClass",
  "MSZoning",
  "LotFrontage",
  "LotArea",
  "Street",
  "Alley",
  "LotShape",
  "LandContour",
  "Utilities",
  "LotConfig",
  "LandSlope",
  "Neighborhood",
  "Condition1",
  "Condition2",
  "BldgType",
  "HouseStyle",
  "OverallQual",
  "OverallCond",
  "YearBuilt",
  "YearRemodAdd",
  "RoofStyle",
  "RoofMatl",
  "Exterior1st",
  "Exterior2nd",
  "MasVnrType",
  "MasVnrArea",
  "ExterQual",
  "ExterCond",
  "Foundation",
  "BsmtQual",
  "BsmtCond",
  "BsmtExposure",
  "BsmtFinType1",
  "BsmtFinSF1",
  "BsmtFinType2",
  "BsmtFinSF2",
  "BsmtUnfSF",
  "TotalBsmtSF",
  "Heating",
  "HeatingQC",
  "CentralAir",
  "Electrical",
  "1stFlrSF",
  "2ndFlrSF",
  "LowQualFinSF",
  "GrLivArea",
  "BsmtFullBath",
  "BsmtHalfBath",
  "FullBath",
  "HalfBath",
  "BedroomAbvGr",
  "KitchenAbvGr",
  "KitchenQual",
  "TotRmsAbvGrd",
  "Functional",
  "Fireplaces",
  "FireplaceQu",
  "GarageType",
  "GarageYrBlt",
  "GarageFinish",
  "GarageCars",
  "GarageArea",
  "GarageQual",
  "GarageCond",
  "PavedDrive",
  "WoodDeckSF",
  "OpenPorchSF",
  "EnclosedPorch",
  "3SsnPorch",
  "ScreenPorch",
  "PoolArea",
  "PoolQC",
  "Fence",
  "MiscFeature",
  "MiscVal",
  "MoSold",
  "YrSold",
  "SaleType",  "SaleCondition",]

sample_input="1461,20,RH,80,11622,Pave,NA,Reg,Lvl,AllPub,Inside,Gtl,NAmes,Feedr,Norm,1Fam,1Story,5,6,1961,1961,Gable,CompShg,VinylSd,VinylSd,None,0,TA,TA,CBlock,TA,TA,No,Rec,468,LwQ,144,270,882,GasA,TA,Y,SBrkr,896,0,0,896,0,0,1,0,2,1,TA,5,Typ,0,NA,Attchd,1961,Unf,1,730,TA,TA,Y,140,0,0,0,120,0,NA,MnPrv,NA,0,6,2010,WD,Normal\n\
"
#1461,20,RH,80,11622,Pave,NA,Reg,Lvl,AllPub,Inside,Gtl,NAmes,Feedr,Norm,1Fam,1Story,5,6,1961,2010,Gable,CompShg,VinylSd,VinylSd,None,0,TA,TA,CBlock,Gd,TA,No,Rec,468,LwQ,144,270,882,GasA,TA,Y,SBrkr,896,0,0,896,0,0,1,0,2,1,TA,5,Typ,0,NA,Attchd,1961,Unf,1,730,TA,TA,Y,140,0,0,0,120,0,NA,MnPrv,NA,0,6,2010,WD,Normal

text_input= st.text_area("""input your data below"""
,sample_input,height=200)

text_input=text_input.splitlines()

st.header("Confirm Input")

#text_input[0]
#st.write(len(text_input[0]),
#st.write(type(col_names),len(col_names)))
#st.write('here')


def text_into_df(input):
    l=[]
    for j in range(len(input)):
            if l == []:
                l=[input[j]]
            else:
                l.append(input[j])
    return {"input":l}
    
df_test=pd.DataFrame.from_dict(text_into_df(text_input))
df_test[col_names]=df_test['input'].str.split(',', expand=True)
del df_test['input']
df_test.columns=col_names
#st.dataframe(df_test)


df_test=AgGrid(df_test,editable=True,)

df_test['data'].to_csv("temp.csv",index=False)


df_test=pd.read_csv("temp.csv")




df_test_IC=ImputerConverter(df_test,col_num_continuous+col_num_int,col_order,col_cat,orders_encoding_result)

df_test_IC,col_FE_num,col_FE_cat=FeatureEngineering(df_test_IC,pca)

st.header("After Feature Engineering")

st.dataframe(df_test_IC[df_test_IC.columns[::-1]])

df_test_IC_selection=df_test_IC[feature_list]

model = pickle.load(open(cat_file,'rb'))


df_test_IC['Predicted_Unit_Price']=model.predict(df_test_IC_selection)
df_test_IC['Predicted_Total_Price']=df_test_IC['Predicted_Unit_Price']*df_test_IC['FEN_IndoorArea']
df_test_IC['Total_Price_Delta']=(df_test_IC['Predicted_Total_Price']-df_test_IC['Predicted_Total_Price'].shift(1)).fillna(0).astype(int)



st.header("Prediction Result")

st.dataframe(df_test_IC[df_test_IC.columns[::-1]])




explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(df_test_IC_selection)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.header("SHAP Analysis on Prediction Result")

for i in range(df_test_IC.shape[0]):
    st.write("Input Record: "+str(i))
    p=shap.force_plot(explainer.expected_value, shap_values[i,:], df_test_IC_selection.iloc[i,:],matplotlib=True,figsize=(20, 5),text_rotation=45,contribution_threshold=0.025)
    st.pyplot(fig=p, bbox_inches='tight',dpi=300,pad_inches=0)
    pl.clf()
    
#df_test=pd.read_csv("../010_data/train.csv")
#df_test_IC=ImputerConverter(df_test,col_num_continuous+col_num_int,col_order,col_cat,orders_encoding_result)
#df_test_IC,col_FE_num,col_FE_cat=FeatureEngineering(df_test_IC,pca)
#df_test_IC.to_csv("../010_data/train_after_treatment.csv",index=False)

st.write("Done")