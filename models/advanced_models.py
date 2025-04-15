import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

from flaml import AutoML

# Sequence model: LSTM
def train_lstm_sequence_model(df: pd.DataFrame, timesteps: int = 5):
    df = df.copy()
    df = df.sort_values(by=['Driver', 'LapNumber'])

    # Filter clean laps
    df = df[
        (~df['IsInlap']) & (~df['IsOutlap']) & (~df['Deleted']) & (df['LapTime_sec'].notna())
    ]

    # Encode compound as numeric
    df['CompoundCode'] = df['Compound'].astype('category').cat.codes

    features = ['TyreLife', 'StintLength', 'IsFreshTyre', 'DegradationPerLap', 'CompoundCode']
    scaler = MinMaxScaler()
    df[features] = scaler.fit_transform(df[features])

    X, y = [], []
    for i in range(len(df) - timesteps):
        X.append(df[features].iloc[i:i+timesteps].values)
        y.append(df['LapTime_sec'].iloc[i+timesteps])
    
    X, y = np.array(X), np.array(y)

    model = Sequential([
        LSTM(64, input_shape=(X.shape[1], X.shape[2]), return_sequences=False),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1)
    ])

    model.compile(loss='mse', optimizer='adam')
    model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2, verbose=1)

    return model, scaler

# AutoML model with FLAML
def train_automl_model(df: pd.DataFrame, time_budget=60):
    df = df[
        (~df['IsInlap']) & (~df['IsOutlap']) & (~df['Deleted']) & (df['LapTime_sec'].notna())
    ]

    features = ['TyreLife', 'StintLength', 'DegradationPerLap', 'IsFreshTyre', 'Compound']
    X = df[features]
    y = df['LapTime_sec']

    transformer = ColumnTransformer([
        ('cat', OneHotEncoder(), ['Compound']),
        ('num', 'passthrough', ['TyreLife', 'StintLength', 'DegradationPerLap', 'IsFreshTyre'])
    ])

    X = transformer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    automl = AutoML()
    automl.fit(X_train=X_train, y_train=y_train, task="regression", time_budget=time_budget)

    return automl, transformer