from simulator.strategy_generator import generate_candidate_strategies
from simulator.simulator import simulate_strategy

def recommend_strategies(model, top_n=3, race_laps=57, compounds=['SOFT', 'HARD'], pit_time_loss=23):
    """
    Generate and evaluate strategies. Return the top-N by predicted total race time.
    """
    strategies = generate_candidate_strategies(race_laps=race_laps, compounds=compounds)
    results = []

    for strat in strategies:
        try:
            total_time, lap_times = simulate_strategy(model, strat, pit_time_loss)
            results.append({
                'strategy': strat,
                'total_time': total_time,
                'lap_times': lap_times
            })
        except Exception as e:
            continue  # skip if model input is invalid

    # Sort by total time
    sorted_results = sorted(results, key=lambda x: x['total_time'])
    return sorted_results[:top_n]

#example usage
#from simulator.recommender import recommend_strategies

#top_strats = recommend_strategies(trained_model, top_n=3)

#for i, strat in enumerate(top_strats, 1):
    #label = " → ".join(f"{c}({l})" for c, l in strat['strategy'])
    #print(f"{i}. {label}: {strat['total_time']:.2f} sec ({strat['total_time']/60:.2f} min)")
