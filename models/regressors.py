#required libraries
#pip install scikit-learn xgboost

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import xgboost as xgb

def get_feature_pipeline(model):
    numeric = ['TyreLife', 'StintLength', 'DegradationPerLap', 'IsFreshTyre']
    categorical = ['Compound']

    transformer = ColumnTransformer([
        ('num', 'passthrough', numeric),
        ('cat', OneHotEncoder(), categorical)
    ])

    return Pipeline([
        ('preprocess', transformer),
        ('model', model)
    ])

def train_regressors(df: pd.DataFrame, target_col='LapTime_sec'):
    df = df[
        df[target_col].notna() &
        (~df['IsInlap']) &
        (~df['IsOutlap']) &
        (~df['Deleted'])
    ].copy()

    features = ['TyreLife', 'StintLength', 'DegradationPerLap', 'IsFreshTyre', 'Compound']
    X = df[features]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        'LinearRegression': LinearRegression(),
        'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
        'XGBoost': xgb.XGBRegressor(n_estimators=100, random_state=42)
    }

    trained = {}
    metrics = {}

    for name, model in models.items():
        pipeline = get_feature_pipeline(model)
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)

        trained[name] = pipeline
        metrics[name] = {
            'MAE': mean_absolute_error(y_test, preds),
            'R2': r2_score(y_test, preds)
        }

    return trained, metrics


#example usage
#from models.regressors import train_regressors

# Use one race or combine multiple
#df = enriched_races['2024_Bahrain_Grand_Prix']

#models, metrics = train_regressors(df)

#for name, res in metrics.items():
    #print(f"{name} - MAE: {res['MAE']:.3f}, R²: {res['R2']:.3f}")
