from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

def evaluate_model(model, X_test, y_test):
    """Evaluate regression model on test set."""
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    return {'MAE': mae, 'R2': r2}

def compare_strategy_totals(real_laps, simulated_laps):
    """
    Compare real lap times vs simulated lap times over a full race.
    Input: both arrays or lists of lap times
    Output: total delta and per-lap breakdown
    """
    real_total = sum(real_laps)
    sim_total = sum(simulated_laps)
    delta = sim_total - real_total

    lap_diffs = [sim - real for sim, real in zip(simulated_laps, real_laps)]
    return {
        'RealTotal': real_total,
        'SimulatedTotal': sim_total,
        'Delta': delta,
        'LapDiffs': lap_diffs
    }

def plot_strategy_comparison(real_laps, simulated_laps, strategy_label='Simulated Strategy'):
    """Plot real vs simulated lap times for visual comparison."""
    laps = list(range(1, len(real_laps) + 1))
    plt.figure(figsize=(12, 5))
    plt.plot(laps, real_laps, label='Actual Lap Times', marker='o')
    plt.plot(laps, simulated_laps, label=strategy_label, marker='x')
    plt.xlabel("Lap Number")
    plt.ylabel("Lap Time (s)")
    plt.title("Real vs Simulated Strategy Lap Times")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#example uage
from models.evaluation import compare_strategy_totals, plot_strategy_comparison

# After simulating a strategy
#metrics = compare_strategy_totals(real_laps, simulated_laps)
#plot_strategy_comparison(real_laps, simulated_laps)

#print(f"Strategy Time Delta: {metrics['Delta']:.2f} seconds")
