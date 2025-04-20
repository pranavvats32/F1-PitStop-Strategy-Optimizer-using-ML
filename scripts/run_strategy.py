import argparse
import joblib

from data.race_filter import load_race_lap_data, filter_dry_podium_races
from features.lap_features import extract_lap_features
from models.regressors import train_regressors
from simulator.recommender import recommend_strategies
from visuals.plots import plot_strategy_laps

def main(race_id, top_n=3, model_path="models/saved/RandomForest.pkl"):
    print(f"\n🏁 Running strategy simulation for: {race_id}\n")

    # Load and prepare race data
    race_laps = load_race_lap_data()
    podium_df = pd.read_csv("data/podiums.csv")  # or use fetch_all_race_results()

    filtered = filter_dry_podium_races(race_laps, podium_df, top_n=3)
    df = filtered.get(race_id)

    if df is None:
        print(f"❌ Race '{race_id}' not found or not valid.")
        return

    df = extract_lap_features(df)

    # Load model
    model = joblib.load(model_path)

    # Simulate & recommend
    top_strategies = recommend_strategies(model, top_n=top_n)
    plot_strategy_laps(top_strategies)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="F1 Pit Stop Strategy Optimizer")
    parser.add_argument('--race', type=str, required=True, help="Race ID, e.g., 2024_Bahrain_Grand_Prix")
    parser.add_argument('--model', type=str, default="models/saved/RandomForest.pkl", help="Path to trained model")
    parser.add_argument('--topn', type=int, default=3, help="Number of top strategies to return")
    args = parser.parse_args()

    main(race_id=args.race, top_n=args.topn, model_path=args.model)


#example terminal usage
#python run_strategy.py --race 2024_Bahrain_Grand_Prix --topn 3
