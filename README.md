# F1-PitStop-Strategy-Optimizer-using-ML

Data Acquired from [FastF1](https://docs.fastf1.dev/) api as well as [Ergast](https://ergast.com/mrd/) API

Attempted Data exploration for Monaco 2023, to search for features which influence pitspot, monaco 2023 data is complex and skewed, the model is not confident (MLP).

(Early rain in the race leading to tyre compound switch  to wets or inters and early pitstops)

(The time difference between the dry compounds is negligible as the track is shorter with many curves and smaller straights )

Moving to a different race data to make specific model for optimised pitstop prediction.

The project in its completion should be able to give optimized pitspot strategy for each track, based on the historial data present.

Feature selection seems of the utmost importance here as alot of features are invovled.

FastF1 is the best dataset for this project, it is also used by the F1 teams aswell.

Will update the readme as i keep working.

f1_strategy_optimizer/
├── data/                        # Pull + clean race data
│   ├── fetch_fastf1.py          # Uses FastF1 to pull telemetry, laps
│   ├── fetch_ergast.py          # Uses Ergast API for race results, temps
│   ├── race_filter.py           # Filter dry races, top finishers only
│   └── cache_manager.py         # Cache control (optional)
│
├── features/
│   ├── lap_features.py          # Extract per-lap features (pace, tyre life)
│   ├── race_features.py         # Aggregate race-level features
│   └── utils.py                 # Shared feature logic
│
├── models/
│   ├── regressors.py            # LapTime predictors (Linear, RF, XGB)
│   ├── advanced_models.py       # Sequence models, RL, AutoML, etc.
│   ├── train.py                 # Model training pipeline
│   └── evaluation.py            # MAE, R2, strategy accuracy
│
├── simulator/
│   ├── simulator.py             # Lap-by-lap simulation using model
│   ├── strategy_generator.py    # Create valid strategy sets
│   └── recommender.py           # Return top-k strategies
│
├── visuals/
│   └── plots.py                 # Lap trends, strategy comparison
│
├── notebooks/                  # Dev & EDA notebooks
│   ├── StrategyExploration.ipynb
│   └── ModelTesting.ipynb
│
├── config/
│   └── settings.yaml            # Constants like race years, compounds, thresholds
│
├── cli/ (optional)             # For running it from terminal or scripts
├── README.md
├── requirements.txt
└── setup.py


References:

https://docs.fastf1.dev/

https://ergast.com/mrd/

https://motorsportengineer.net/how-pit-stop-strategy-leads-to-victories-in-formula-1/

https://motorsportengineer.net/how-race-strategy-works-in-formula-1/#:~:text=The%20decision%20of%20when%20to,on%20opportunities%20or%20mitigate%20risks.

https://www.youtube.com/watch?v=2PUz2EvbHRw
