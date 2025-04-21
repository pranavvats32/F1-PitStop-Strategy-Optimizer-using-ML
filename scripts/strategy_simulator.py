import os
import pickle
import pandas as pd
import numpy as np
import argparse
import sys
import matplotlib.pyplot as plt
import seaborn as sns

# CLI args
parser = argparse.ArgumentParser(description="Simulate F1 pit stop strategies")
parser.add_argument("--model", type=str, default="randomforest", help="Model to use (randomforest, linearregression, xgboost)")
args = parser.parse_args()

# Setup path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load model
model_name = args.model.lower()
model_path = f"models/{model_name}_model.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Model not found: {model_path}")
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Load lap data
df = pd.read_pickle("data/model_input/bahrain_top5_laps_2019_2024.pkl")

# Filter + clean
df = df[df['LapTime'].notnull()]
df = df[~df['PitInTime'].notnull()]
df = df[~df['PitOutTime'].notnull()]
df = df.copy()

# Feature engineering
df.loc[:, 'LapTime_sec'] = df['LapTime'].dt.total_seconds()
df.loc[:, 'IsFreshTyre'] = df['FreshTyre'].fillna(False).astype(int)
df.loc[:, 'TyreAge'] = df['TyreLife']
df.loc[:, 'CompoundEncoded'] = df['Compound'].astype('category').cat.codes

# Feature columns
features = ['Stint', 'TyreAge', 'IsFreshTyre', 'CompoundEncoded', 'Position']

# Define strategies
strategies = {
    "Soft → Hard": [('SOFT', 17), ('HARD', 40)],
    "Hard → Soft": [('HARD', 35), ('SOFT', 22)],
    "Soft → Hard → Soft": [('SOFT', 15), ('HARD', 27), ('SOFT', 15)],
}

compound_map = {'SOFT': 0, 'MEDIUM': 1, 'HARD': 2}

compound_colors = {
    'SOFT': '#FF3333',
    'MEDIUM': '#FFD700',
    'HARD': '#A9A9A9',
    'PIT': '#000000'
}

def simulate_strategy(strategy_name, base_position=1):
    strategy = strategies[strategy_name]
    lap_predictions = []
    total_time = 0
    tyre_age = 0
    stint_num = 0
    lap_number = 1

    for compound, length in strategy:
        for _ in range(length):
            row = {
                'Stint': stint_num,
                'TyreAge': tyre_age,
                'IsFreshTyre': int(tyre_age == 0),
                'CompoundEncoded': compound_map.get(compound, -1),
                'Position': base_position
            }
            base_time = model.predict(pd.DataFrame([row]))[0]

            degradation_factor = 1 + (0.003 * tyre_age)
            pred_time = base_time * degradation_factor
            total_time += pred_time

            lap_predictions.append({
                'Strategy': strategy_name,
                'Lap': lap_number,
                'Stint': stint_num,
                'Compound': compound,
                'TyreAge': tyre_age,
                'PredictedTime_sec': round(pred_time, 3)
            })

            tyre_age += 1
            lap_number += 1

        # Pit stop (adds time to race, but not to scoring anymore)
        total_time += 20
        lap_predictions.append({
            'Strategy': strategy_name,
            'Lap': lap_number,
            'Stint': stint_num,
            'Compound': 'PIT',
            'TyreAge': 0,
            'PredictedTime_sec': 20.0
        })
        lap_number += 1
        tyre_age = 0
        stint_num += 1

    return round(total_time, 2), lap_predictions

# Run simulations
print(f"\n🏎️ Strategy Simulation using model: {model_name.capitalize()}\n")
all_laps = []
results = []

best_strategy = None
best_time = float("inf")

for strat in strategies:
    total_time, laps = simulate_strategy(strat)

    print(f"→ {strat}: {total_time:.2f} sec")
    all_laps.extend(laps)
    results.append((strat, total_time))

    if total_time < best_time:
        best_time = total_time
        best_strategy = strat
        best_laps = laps

print(f"\n🏁 Best strategy: {best_strategy} ({best_time:.2f} sec)")

# Save output
os.makedirs("outputs", exist_ok=True)
pd.DataFrame(all_laps).to_csv("outputs/strategy_lap_predictions.csv", index=False)
pd.DataFrame(best_laps).to_csv("outputs/best_strategy_lap_times.csv", index=False)
print("✅ Saved lap-by-lap predictions.")

# Plot
lap_df = pd.DataFrame(all_laps)
plt.figure(figsize=(12, 6))
sns.lineplot(data=lap_df[lap_df['Compound'] != 'PIT'], x='Lap', y='PredictedTime_sec', hue='Compound', palette=compound_colors)
plt.title(f"Lap-by-Lap Predicted Time by Compound ({model_name})")
plt.ylabel("Lap Time (sec)")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/strategy_plot.png")
plt.close()
print("📊 Lap time plot saved to outputs/strategy_plot.png")
