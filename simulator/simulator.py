import pandas as pd
import numpy as np

def simulate_stint(model, compound, stint_length):
    """
    Predict lap times for a single stint.
    """
    laps = []
    for lap in range(1, stint_length + 1):
        laps.append({
            'TyreLife': lap,
            'StintLength': stint_length,
            'IsFreshTyre': lap == 1,
            'DegradationPerLap': 0,  # optional: leave or compute
            'Compound': compound
        })
    stint_df = pd.DataFrame(laps)
    lap_times = model.predict(stint_df)
    return lap_times

def simulate_strategy(model, strategy, pit_time_loss=23):
    """
    Simulate total race time for a pit strategy.
    Strategy = list of (compound, stint_length)
    """
    total_lap_times = []
    for compound, laps in strategy:
        stint_times = simulate_stint(model, compound, laps)
        total_lap_times.extend(stint_times)

    # Add pit time loss (for each stop after first)
    total_time = sum(total_lap_times) + (len(strategy) - 1) * pit_time_loss

    return total_time, total_lap_times

#example usage
#from simulator.simulator import simulate_strategy

#strategy = [('SOFT', 17), ('HARD', 20), ('SOFT', 20)]
#total_time, lap_times = simulate_strategy(trained_model, strategy)

#print(f"Total Race Time: {total_time:.2f} sec ({total_time/60:.2f} min)")
