import matplotlib.pyplot as plt

def plot_strategy_laps(strategies, title="Top Strategy Lap Comparisons"):
    """
    Plot lap-by-lap lap times for multiple strategies.
    Each strategy = dict with 'strategy' and 'lap_times'.
    """
    plt.figure(figsize=(14, 6))

    for i, strat in enumerate(strategies, 1):
        laps = list(range(1, len(strat['lap_times']) + 1))
        label = f"{i}. " + " → ".join(f"{c}({l})" for c, l in strat['strategy'])
        plt.plot(laps, strat['lap_times'], label=label)

    plt.title(title)
    plt.xlabel("Lap Number")
    plt.ylabel("Predicted Lap Time (s)")
    plt.legend(title="Strategy")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_real_vs_sim(real_laps, sim_laps, label="Simulated Strategy"):
    """
    Plot a comparison between real lap times and one simulated strategy.
    """
    laps = list(range(1, len(real_laps) + 1))
    plt.figure(figsize=(12, 5))
    plt.plot(laps, real_laps, label="Real Lap Times", marker='o')
    plt.plot(laps, sim_laps, label=label, marker='x')
    plt.title("Real vs Simulated Lap Time")
    plt.xlabel("Lap Number")
    plt.ylabel("Lap Time (s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# example usage
#from visuals.plots import plot_strategy_laps
#from simulator.recommender import recommend_strategies

# Get top 3 strategies
#top3 = recommend_strategies(trained_model, top_n=3)

# Visualize
#plot_strategy_laps(top3)
