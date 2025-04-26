# F1 Pit Stop Strategy Optimizer using ML

**Author:** Pranav Vats  
**Repo:** [github.com/pranavvats32/F1-PitStop-Strategy-Optimizer-using-ML](https://github.com/pranavvats32/F1-PitStop-Strategy-Optimizer-using-ML)

---

## 🏎️ Overview
A predictive F1 race strategy simulator that models lap-by-lap tyre performance and simulates pit stop strategies.  
Built using FastF1 telemetry data and Ergast API race results for Bahrain GP (2019–2024).

---

## 📦 Project Structure

| Folder | Purpose |
|:------|:--------|
| `data/` | Fetch FastF1 + Ergast data |
| `models/` | Trained ML models (Linear, Random Forest, XGBoost) |
| `outputs/` | Simulation outputs and plots |
| `scripts/` | Runnable Python scripts for full pipeline |

---

## 🔧 Setup

```bash
git clone https://github.com/pranavvats32/F1-PitStop-Strategy-Optimizer-using-ML.git
cd F1-PitStop-Strategy-Optimizer-using-ML

conda create -n f1-strategy python=3.10
conda activate f1-strategy
pip install -r requirements.txt
```

Initialize FastF1 cache (important!):

```python
import fastf1
fastf1.Cache.enable_cache('cache')
```

---

## 🚀 Quickstart Pipeline

1. **Fetch race lap data**  
   (FastF1 telemetry for Bahrain GPs)
   ```bash
   python scripts/fetch_races.py
   ```

2. **Fetch Ergast race results**  
   (Top 5 finishers)
   ```bash
   python scripts/fetch_ergast_results.py
   ```

3. **Build the model dataset**  
   (Match laps with podium drivers)
   ```bash
   python scripts/build_model_dataset.py
   ```

4. **Train machine learning models**  
   (Linear, RandomForest, XGBoost)
   ```bash
   python scripts/train_model.py
   ```

5. **Simulate pit stop strategies**  
   (Lap-by-lap race simulation)
   ```bash
   python scripts/strategy_simulator.py --model randomforest
   ```

---

## 🧠 Models Included
- Linear Regression
- Random Forest
- XGBoost

Each predicts **lap time** based on:
- Tyre compound
- Tyre age
- Stint number
- Tyre freshness
- Track position

---

## 🏎️ Strategy Simulator
Simulates strategies like:

```
Soft → Hard
Hard → Soft
Soft → Hard → Soft
```

and outputs:
- Total race time prediction
- Lap-by-lap predicted lap times
- Best strategy recommendation

---

## 📊 Visuals
- Lap-by-lap strategy plot (`outputs/strategy_plot.png`)
- CSVs with full lap predictions and best strategy times

Example Plot:  
(You can update with your own generated plot later!)

---

## 📋 License
Licensed under the MIT License.

---

## 🛠️ Future Enhancements
- Circuit-specific degradation modeling
- Track temperature integration
- Streamlit app for live race simulations
- Reinforcement learning for pit timing
- Optional pit stop penalty scoring (planned)

---

🏁 Built with ❤️ and race data by [@pranavvats32](https://github.com/pranavvats32)
