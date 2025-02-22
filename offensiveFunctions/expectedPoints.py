import numpy as np
import sys

sys.path.append(r'C:\Users\alber\Documents\marchmadness')

from helpers import getTeams, data

def simulate_game(transition_matrix, points_per_state, num_possessions):
    states = list(points_per_state.keys())
    state_index = {state: i for i, state in enumerate(states)}
    
    current_state = 'Start'  
    total_points = 0
    possession_count = 1

    for _ in range(num_possessions):
        while current_state != 'End':
            next_state = np.random.choice(states, p=transition_matrix[state_index[current_state]])
            total_points += points_per_state[next_state]  
            current_state = next_state
        current_state = 'Start'
        possession_count += 1

    return total_points

points_per_state = {
    'Start': 0,
    'Make 2': 2,
    'Make 3': 3,
    'Missed Shot': 0,
    'Turnover': 0,
    'Free Throw': 1,
    'Offensive Rebound': 0,
    'End': 0
}

# game simulations
teams = getTeams()
num_simulations = 100
for team in teams:
    team_name, fg_pct_element, fg2_element, fg2a_element, fg2_pct_element, fg3_element, fg3a_element, fg3_pct_element, ft_element, fta_element, ft_pct_element, orb_element, drb_element, trb_element, ast_element, stl_element, blk_element, tov_element, pf_element, pts_element, ppg = data(team)
    possessions = tov_element + fg2a_element + fg3a_element + ft_element // 2.15
    twoPointersMade = fg2_element / possessions
    threePointersMade = fg3_element / possessions
    missedShots = ((fg2a_element - fg2_element) + (fg3a_element - fg3_element)) / possessions
    turnovers = tov_element / possessions
    freeThrows = (ft_element // 2.5) / possessions
    offensiveRebounds = orb_element / possessions
    makingBothFreeThrows = ft_pct_element * ft_pct_element
    makingAndOne = ft_pct_element * 0.33
    missedShotAfterFreeThrow = 1 - ft_pct_element
    # Fixed transition matrix (normalized and valid)
    transition_matrix = np.array([
        [0,  twoPointersMade,  threePointersMade,  missedShots,   turnovers,  freeThrows, offensiveRebounds,  0],  # Start
        [0,   0,     0,    0,      0,     0,   0,   1],    # Make 2 (end)
        [0,   0,     0,    0,      0,     0,   0,   1],    # Make 3 (end)
        [0,   0,     0,    0,      0,     0,   offensiveRebounds,  1-offensiveRebounds],  # Missed Shot
        [0,   0,     0,    0,      0,     0,   0,   1],    # Turnover (end)
        [0,   makingBothFreeThrows,  makingAndOne, missedShotAfterFreeThrow,   turnovers,  freeThrows, offensiveRebounds,   0],    # Free Throw
        [0,  twoPointersMade,  threePointersMade,  missedShots,   turnovers,  freeThrows, offensiveRebounds,  0],  # Offensive Rebound
        [0,   0,     0,    0,      0,     0,   0,   1]     # End (absorbing state)
    ])

    #normalization of values
    for i in range(len(transition_matrix)):
        row_sum = np.sum(transition_matrix[i])
        if row_sum > 0:
            transition_matrix[i] /= row_sum
    predicted_scores = [simulate_game(transition_matrix, points_per_state, round(ppg)) for _ in range(num_simulations)]
    expected_points = np.mean(predicted_scores)
    print(f'Predicted Score for {team}: {expected_points:.2f} points')
    percent_error = ((pts_element / 26  - expected_points) / expected_points) * 100
    print(f'Percent error {percent_error:.2f} %')
