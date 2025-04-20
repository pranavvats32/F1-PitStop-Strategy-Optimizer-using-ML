import os
import sys
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# Optional: Try importing XGBoost
try:
    from xgboost import XGBRegressor
    xgb_installed = True
except ImportError:
    xgb_installed = False

# Setup import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load data
df = pd.read_pickle("data/model_input/bahrain_top5_laps_2019_2024.pkl")

# Drop in/out laps and missing times
df = df[df['LapTime'].notnull()]
df = df[~df['PitInTime'].notnull()]
df = df[~df['PitOutTime'].notnull()]

# Convert to seconds safely
df = df.copy()
df.loc[:, 'LapTime_sec'] = df['LapTime'].dt.total_seconds()

# 📉 Remove lap time outliers
df = df[(df['LapTime_sec'] >= 80) & (df['LapTime_sec'] <= 105)]

# 💡 Optional: View distribution summary in CLI
print("\n📊 LapTime_sec summary after filtering:")
print(df['LapTime_sec'].describe())

# Feature engineering
df['IsFreshTyre'] = df['FreshTyre'].fillna(False).astype(int)
df['TyreAge'] = df['TyreLife']
df['CompoundEncoded'] = df['Compound'].astype('category').cat.codes

# Define model features
features = ['Stint', 'TyreAge', 'IsFreshTyre', 'CompoundEncoded', 'Position']
target = 'LapTime_sec'

X = df[features]
y = df[target]

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models
models = {
    'LinearRegression': LinearRegression(),
    'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42)
}
if xgb_installed:
    models['XGBoost'] = XGBRegressor(n_estimators=100, random_state=42)

# Train + Evaluate
results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    results[name] = {
        'MAE': mean_absolute_error(y_test, y_pred),
        'R2': r2_score(y_test, y_pred)
    }

    print(f"\n📈 {name}")
    print(f"  MAE: {results[name]['MAE']:.3f}")
    print(f"  R²:  {results[name]['R2']:.3f}")

# Save predictions
df_preds = X_test.copy()
df_preds['Actual'] = y_test
df_preds['Predicted_RF'] = models['RandomForest'].predict(X_test)

os.makedirs("outputs", exist_ok=True)
df_preds.to_csv("outputs/rf_predictions.csv", index=False)
print("\n✅ Saved predictions to: outputs/rf_predictions.csv")
