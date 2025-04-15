def generate_candidate_strategies(race_laps=57, compounds=['SOFT', 'HARD', 'MEDIUM']):
    """
    Generate a set of plausible race strategies.
    Returns: list of strategies, each as a list of (compound, stint_length)
    """
    strategies = []

    # 1-stop strategies
    for s1 in range(10, 30):
        s2 = race_laps - s1
        if s2 > 0:
            strategies.append([('SOFT', s1), ('HARD', s2)])
            strategies.append([('HARD', s1), ('SOFT', s2)])
            strategies.append([('MEDIUM', s1), ('HARD', s2)])
            strategies.append([('HARD', s1), ('MEDIUM', s2)])

    # 2-stop strategies
    for s1 in range(10, 25):
        for s2 in range(10, 25):
            s3 = race_laps - s1 - s2
            if s3 > 0:
                for c1 in compounds:
                    for c2 in compounds:
                        for c3 in compounds:
                            strategies.append([(c1, s1), (c2, s2), (c3, s3)])

    return strategies

#example usage
#from simulator.strategy_generator import generate_candidate_strategies

#candidates = generate_candidate_strategies(race_laps=57, compounds=['SOFT', 'HARD'])
#for strat in candidates[:5]:
    #print(strat)
