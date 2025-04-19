# F1 Pit Stop Strategy Optimizer using ML

**Author:** Pranav Vats  
**Repo:** [github.com/pranavvats32/F1-PitStop-Strategy-Optimizer-using-ML](https://github.com/pranavvats32/F1-PitStop-Strategy-Optimizer-using-ML)

---

## 🏎️ Overview
This project is a predictive race strategy engine for Formula 1, built using 5 years of FastF1 telemetry and Ergast data. It models lap-by-lap performance based on tyre degradation and simulates pit stop strategies to recommend the fastest options.

Inspired by PitGenius, but with custom features, driver-focused modeling, and strategy simulation logic.

---

## 📦 Features

### Data Sources:
- FastF1 (Lap times, compounds, stints, telemetry)
- Ergast API (Race results, weather, podium detection)

### Key Modules:
- `data/`: Ingest FastF1 and Ergast data
- `features/`: Extract lap-level and race-level features
- `models/`: Train baseline and advanced models (Linear, RF, XGB, LSTM, AutoML)
- `simulator/`: Simulate strategies lap-by-lap
- `visuals/`: Plot real vs simulated race timelines

### Strategy Features:
- 📈 Tyre pace (`LapTime_sec`)
- 🧊 Warmup effect (`IsFreshTyre`)
- 🔻 Degradation rate (`DegradationPerLap`)
- ⏱️ Performance and wear life
- 🕓 Pit stop duration

---

## 🧪 Example: Predict Strategy for 2024 Bahrain GP

```python
from simulator.recommender import recommend_strategies
from visuals.plots import plot_strategy_laps

# Load trained model
model = joblib.load("models/saved/RandomForest.pkl")

# Recommend top 3 strategies
top_strats = recommend_strategies(model, top_n=3, race_laps=57)

# Visualize them
plot_strategy_laps(top_strats)
```

---

## 🔧 Setup
```bash
git clone https://github.com/pranavvats32/F1-PitStop-Strategy-Optimizer-using-ML.git
cd F1-PitStop-Strategy-Optimizer-using-ML

pip install -r requirements.txt
```

Make sure to run:
```python
import fastf1
fastf1.Cache.enable_cache('cache')
```

---

## 🧠 Models Included
- `LinearRegression`
- `RandomForestRegressor`
- `XGBoostRegressor`
- `LSTM (Keras)`
- `FLAML AutoML`

All models predict lap time based on compound, tyre age, stint length, and degradation.

---

## 📊 Strategy Simulator
Simulates any given strategy like:
```python
[('SOFT', 17), ('HARD', 20), ('SOFT', 20)]
```
And returns:
- Total predicted race time
- Lap-by-lap prediction
- Visual strategy comparison

---

## 📈 Visual Output
![Example Plot](path/to/example_plot.png)  
_Compare lap-by-lap lap times across strategies_

---

## 📋 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💬 Want to Contribute?
Open an issue or drop a PR! Contributions for strategy optimization logic, race weather models, or circuit-specific tuning are welcome.

---

## 🏁 Future Roadmap
- [ ] Streamlit app for race selection and strategy comparison
- [ ] Circuit-specific model tuning
- [ ] Reinforcement learning-based pit timing
- [ ] Include track temperature and fuel load in modeling

---

Built with ❤️ and race fuel by [@pranavvats32](https://github.com/pranavvats32)

