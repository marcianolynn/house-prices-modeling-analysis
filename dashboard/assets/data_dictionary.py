col_cat = [
    'MSSubClass',  # building class
    'MSZoning',  # general zoning classification
    'Street',  # road access
    'LandContour',  # flatness of property
    'Utilities',  # type of utilities avail
    'LotConfig',  # lot configuration
    'LandSlope',  # slope of property
    'Neighborhood',  # physical neighborhoods within Ames
    'Condition1',  # proximity to certain landmarks
    'Condition2',  # proximity to certain landmarks (if more than one present)
    'BldgType',  # type of dwelling
    'HouseStyle',  # how many floors/type of dwelling
    'RoofStyle',  # type of roof
    'RoofMatl',  # roof material
    'Exterior1st',  # exterior covering on the house
    'Exterior2nd',  # exterior covering on the house (if more than one present)
    'MasVnrType',  # masonry veneer type
    'Foundation',  # type of foundation
    'Heating',  # type of heating
    'CentralAir',  # boolean if central air is avail
    'Electrical',  # type of electrical system
    'GarageType',  # garage location
    'SaleType',  # type of sale
    'SaleCondition',  # condition of sale
    'MiscFeature',  # Miscellaneous feature not covered in other categories
]

col_order = [
    'ExterQual',  # Evaluates the quality of the material on the exterior
    'LotShape',  # general shape of the property
    'ExterCond',  # evaluate present condition of material on exterior
    'BsmtQual',  # evaluate height of basement
    'BsmtCond',  # evaluate present condition of the basement
    'BsmtExposure',  # evaluate ability to walkout or garden level walls
    'BsmtFinType1',  # rating of basement finished area
    'BsmtFinType2',  # rating of basement finished area (if multiple)
    'HeatingQC',  # heating quality & condition
    # home functionality (assume typical unless deductions warranted)
    'Functional',
    'KitchenQual',  # kitchen quality
    'GarageQual',  # garage quality
    'GarageFinish',  # evaluate interior finish of garage
    'GarageCond',  # evaluate garage condition
    'PavedDrive',  # evaluate type of driveway based on pavement
    'PoolQC',  # Pool quality
    'Fence',  # Fence quality
    'FireplaceQu',  # Fireplace quality
    'Alley',  # Type of alley access
]

col_num_continuous = [
    'LotArea',  # Lot size in square feet
    'MasVnrArea',  # Masonry veneer area in square feet
    'BsmtFinSF1',  # Type 1 finished square feet
    'BsmtFinSF2',  # Type 2 finished square feet
    'BsmtUnfSF',  # Unfinished square feet of basement area
    'TotalBsmtSF',  # Total square feet of basement area
    '1stFlrSF',  # First Floor square feet
    '2ndFlrSF',  # Second floor square feet
    'LowQualFinSF',  # Low quality finished square feet (all floors)
    'GrLivArea',  # Above grade (ground) living area square feet
    'GarageArea',  # Size of garage in square feet
    'WoodDeckSF',  # Wood deck area in square feet
    'OpenPorchSF',  # Open porch area in square feet
    'EnclosedPorch',  # Enclosed porch area in square feet
    '3SsnPorch',  # Three season porch area in square feet
    'ScreenPorch',  # Screen porch area in square feet
    'PoolArea',  # Pool area in square feet
    'MiscVal',  # Value of miscellaneous feature
    'LotFrontage',  # Linear feet of street connected to property
]

col_num_int = [
    'OverallQual',  # evaluate the overall material and finish of the house
    'OverallCond',  # evaluate Overall condition rating
    'BsmtFullBath',  # Basement full bathrooms
    'BsmtHalfBath',  # Basement half bathrooms
    'FullBath',  # Full bathrooms above grade
    'HalfBath',  # Half baths above grade
    'BedroomAbvGr',  # Number of bedrooms above basement level
    'KitchenAbvGr',  # Number of kitchens
    'TotRmsAbvGrd',  # Total rooms above grade (does not include bathrooms)
    'Fireplaces',  # Number of fireplaces
    'GarageCars',  # Size of garage in car capacity
    'YearBuilt',  # year built
    'YearRemodAdd',  # year remodels were added
    'MoSold',  # month sold
    'YrSold',  # year sold
    'GarageYrBlt'  # year garage was built
]

# define categorical values
cat_values = {
    'MSZoning': ['None', 'A', 'C', 'FV', 'I', 'RH', 'RL', 'RP', 'RM'],
    'Street': ['None', 'Pave', 'Grvl'],
    'LandContour': ['None', 'Lvl', 'Bnk', 'HLS', 'Low'],
    'Utilities': ['None', 'AllPub', 'NoSewr', 'NoSeWa', 'ELO'],
    'LotConfig': ['None', 'Inside', 'Corner', 'CulDSac', 'FR2', 'FR3'],
    'LandSlope': ['None', 'Gtl', 'Mod', 'Sev'],
    'Neighborhood': ['None', "Blmngtn", "Bluestem", "BrDale", "BrkSide",
                     "ClearCr", "CollgCr", "Crawfor", "Edwards",
                     "Gilbert", "IDOTRR", "MeadowV", "Mitchel",
                     "Names", "NoRidge", "NPkVill", "NridgHt",
                     "NWAmes", "OldTown", "SWISU", "Sawyer",
                     "SawyerW", "Somerst", "StoneBr", "Timber", "Veenker"],
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
    'SaleType': ['None', 'WD', 'CWD', 'VWD', 'New', 'COD',
                 'ConLD',  'ConLI',  'ConLw',  'Con',  'Oth'],
    'SaleCondition': ['None',  'Normal',  'Abnorml',  'Partial',  'AdjLand',  'Alloca',  'Family'],
    'MSSubClass': ['None', 20, 30, 40, 45, 50, 60, 70, 75, 80, 85, 90, 120, 150, 160, 180, 190],
    'ExterQual': ['None', 'Po', 'Fa', 'TA', 'Gd', 'Ex'],
    'LotShape': ['None', 'Reg', 'IR1', 'IR2', 'IR3'],
    'ExterCond': ['None', 'Po', 'Fa', 'TA', 'Gd', 'Ex'],
    'BsmtQual': ['None', 'Fa', 'TA', 'Gd', 'Ex'],
    'BsmtCond': ['None', 'Po', 'Fa', 'TA', 'Gd', 'Ex'],
    'BsmtExposure': ['None', 'No', 'Mn', 'Av', 'Gd'],
    'BsmtFinType1': ['None', 'Unf', 'LwQ', 'Rec', 'BLQ', 'ALQ', 'GLQ'],
    'BsmtFinType2': ['None', 'Unf', 'LwQ', 'Rec', 'BLQ', 'ALQ', 'GLQ'],
    'HeatingQC': ['None', 'Po', 'Fa', 'TA', 'Gd', 'Ex'],
    'Functional': ['None', 'Sev', 'Maj2', 'Maj1', 'Mod', 'Min2', 'Min1', 'Typ'],
    'KitchenQual': ['None', 'Fa', 'TA', 'Gd', 'Ex'],
    'GarageFinish': ['None', 'Unf', 'RFn', 'Fin'],
    'GarageQual': ['None', 'Po', 'Fa', 'TA', 'Gd', 'Ex'],
    'GarageCond': ['None', 'Po', 'Fa', 'TA', 'Gd', 'Ex'],
    'PavedDrive': ['None', 'N', 'P',  'Y'],
    'PoolQC': ['None', 'Po', 'Fa', 'TA', 'Gd', 'Ex'],
    'MiscFeature': ['None', 'Elev', 'Gar2', 'Othr', 'Shed', 'TenC'],
    'Alley': ['None', 'Grvl', 'Pave'],
    'Fence': ['None', 'MnWw', 'GdWo', 'MnPrv', 'GdPrv'],
    'FireplaceQu': ['None', 'Po', 'Fa', 'TA', 'Gd', 'Ex'],
}

# feature engineered cols
new_FEN = ['FEN_IndoorArea',
           'FEN_LotArea_Per_IndoorArea',
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
           'FEN_PoolArea_Per_IndoorArea',
           'FEN_YearAfterRemode',
           'FEN_YearAfterbuilt',
           'FEN_TotRmsAbvGrd_Per_GrLivArea',
           'FEN_BsmtTotalbath',
           'FEN_GrLivTotalbath',
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
