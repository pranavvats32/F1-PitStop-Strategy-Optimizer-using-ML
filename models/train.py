

# the script to tie them all together for training and saving models

import os
import joblib
from models.regressors import train_regressors
from models.advanced_models import train_lstm_sequence_model, train_automl_model

def run_training_pipeline(df, save_path='models/saved/', train_advanced=False):
    os.makedirs(save_path, exist_ok=True)

    print("🎯 Training baseline regressors...")
    regressors, metrics = train_regressors(df)

    for name, model in regressors.items():
        model_path = os.path.join(save_path, f"{name}.pkl")
        joblib.dump(model, model_path)
        print(f"✅ Saved {name} to {model_path}")
        print(f"  MAE: {metrics[name]['MAE']:.3f} sec | R²: {metrics[name]['R2']:.3f}")

    if train_advanced:
        print("\n🧠 Training sequence model (LSTM)...")
        lstm_model, scaler = train_lstm_sequence_model(df)
        lstm_model.save(os.path.join(save_path, "LSTM_Model.h5"))
        joblib.dump(scaler, os.path.join(save_path, "LSTM_Scaler.pkl"))
        print("✅ LSTM model saved")

        print("\n🤖 Training AutoML model (FLAML)...")
        automl_model, transformer = train_automl_model(df, time_budget=120)
        joblib.dump(automl_model, os.path.join(save_path, "FLAML_Model.pkl"))
        joblib.dump(transformer, os.path.join(save_path, "FLAML_Transformer.pkl"))
        print("✅ AutoML model saved")

    print("\n🏁 Training complete.")

# example usage
#from models.train import run_training_pipeline

# Assuming `df` is your fully enriched, clean race DataFrame
#run_training_pipeline(df, train_advanced=True)

