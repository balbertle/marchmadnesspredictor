import numpy as np
import sys
import ast
import csv

sys.path.append(r'C:\Users\alber\Documents\marchmadness')
from helpers import getTeams, data
from models import TeamStats

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

def simulate_game(team1_matrix, team2_matrix, points_per_state, num_possessions, show_progress=False):
    states = list(points_per_state.keys())
    state_index = {state: i for i, state in enumerate(states)}
    
    team1_points = 0
    team2_points = 0
    current_team = 1 
    current_state = 'Start'
    num_possessions = int(num_possessions)
    for possession in range(num_possessions):
        if show_progress:
            print(f"\rPossession {possession + 1}/{num_possessions}", end="")
        
        # Use the appropriate transition matrix based on which team has possession
        transition_matrix = team1_matrix if current_team == 1 else team2_matrix
        
        while current_state != 'End':
            # Get probabilities for current state
            probs = transition_matrix[state_index[current_state]].copy()
            
            # Ensure all probabilities are non-negative and sum to 1
            probs = np.maximum(probs, 0)
            probs_sum = np.sum(probs)
            if probs_sum > 0:
                probs = probs / probs_sum
            
            # Choose next state based on probabilities
            next_state = np.random.choice(states, p=probs)
            points = points_per_state[next_state]
            
            # Add points to the appropriate team
            if current_team == 1:
                team1_points += points
            else:
                team2_points += points
                
            current_state = next_state
            
        # Switch possession
        current_team = 2 if current_team == 1 else 1
        current_state = 'Start'

    if show_progress:
        print()
    return team1_points, team2_points

def calculate_balanced_probabilities(team_stats, opp_stats, possessions):
    """Calculate probabilities that balance team's offense and opponent's defense"""
    
    # Calculate team's offensive probabilities per possession
    team_2p_made = max(0, min(1, team_stats.fg2 / max(1, team_stats.possessions * team_stats.games)))
    team_3p_made = max(0, min(1, team_stats.fg3 / max(1, team_stats.possessions * team_stats.games)))
    team_missed = max(0, min(1, ((team_stats.fg2a - team_stats.fg2) + (team_stats.fg3a - team_stats.fg3)) / max(1, team_stats.possessions * team_stats.games)))
    team_turnovers = max(0, min(1, team_stats.tov / max(1, team_stats.possessions * team_stats.games)))
    team_free_throws = max(0, min(1, team_stats.fta / max(1, team_stats.possessions * team_stats.games)))
    team_off_rebounds = max(0, min(1, team_stats.orb / max(1, team_stats.possessions * team_stats.games)))

    # Calculate opponent's defensive probabilities per possession
    opp_2p_allowed = max(0, min(1, opp_stats.opp_fg2 / max(1, opp_stats.possessions * opp_stats.games)))
    opp_3p_allowed = max(0, min(1, opp_stats.opp_fg3 / max(1, opp_stats.possessions * opp_stats.games)))
    opp_missed_forced = max(0, min(1, ((opp_stats.opp_fg2a - opp_stats.opp_fg2) + (opp_stats.opp_fg3a - opp_stats.opp_fg3)) / max(1, opp_stats.possessions * opp_stats.games)))
    opp_turnovers_forced = max(0, min(1, opp_stats.opp_tov / max(1, opp_stats.possessions * opp_stats.games)))
    opp_free_throws_allowed = max(0, min(1, opp_stats.opp_fta / max(1, opp_stats.possessions * opp_stats.games)))
    opp_off_rebounds_allowed = max(0, min(1, opp_stats.opp_orb / max(1, opp_stats.possessions * opp_stats.games)))

    # Print raw probabilities
    print("\nRaw probabilities per possession:")
    print(f"Team 2P: {team_2p_made:.3f} ({team_stats.fg2}/{team_stats.possessions * team_stats.games}), 3P: {team_3p_made:.3f} ({team_stats.fg3}/{team_stats.possessions * team_stats.games})")
    print(f"Team Miss: {team_missed:.3f}, TO: {team_turnovers:.3f} ({team_stats.tov}/{team_stats.possessions * team_stats.games})")
    print(f"Team FT: {team_free_throws:.3f} ({team_stats.fta}/{team_stats.possessions * team_stats.games}), ORB: {team_off_rebounds:.3f} ({team_stats.orb}/{team_stats.possessions * team_stats.games})")
    print(f"Opp 2P: {opp_2p_allowed:.3f} ({opp_stats.opp_fg2}/{opp_stats.possessions * opp_stats.games}), 3P: {opp_3p_allowed:.3f} ({opp_stats.opp_fg3}/{opp_stats.possessions * opp_stats.games})")
    print(f"Opp Miss: {opp_missed_forced:.3f}, TO: {opp_turnovers_forced:.3f} ({opp_stats.opp_tov}/{opp_stats.possessions * opp_stats.games })")
    print(f"Opp FT: {opp_free_throws_allowed:.3f} ({opp_stats.opp_fta}/{opp_stats.possessions * opp_stats.games}), ORB: {opp_off_rebounds_allowed:.3f} ({opp_stats.opp_orb}/{opp_stats.possessions * opp_stats.games})")

    # Calculate balanced probabilities (median between team and opponent)
    twoPointersMade = (team_2p_made + (1 - opp_2p_allowed)) / 2
    threePointersMade = (team_3p_made + (1 - opp_3p_allowed)) / 2
    missedShots = (team_missed + opp_missed_forced) / 2
    turnovers = (team_turnovers + opp_turnovers_forced) / 2
    freeThrows = team_free_throws  # Less affected by defense
    offensiveRebounds = (team_off_rebounds + (1 - opp_off_rebounds_allowed)) / 2

    # Print balanced probabilities before normalization
    print("\nBalanced probabilities (before normalization):")
    print(f"2P: {twoPointersMade:.3f}, 3P: {threePointersMade:.3f}, Miss: {missedShots:.3f}")
    print(f"TO: {turnovers:.3f}, FT: {freeThrows:.3f}, ORB: {offensiveRebounds:.3f}")

    # Normalize to sum to 1
    total = twoPointersMade + threePointersMade + missedShots + turnovers + freeThrows + offensiveRebounds
    if total > 0:
        twoPointersMade /= total
        threePointersMade /= total
        missedShots /= total
        turnovers /= total
        freeThrows /= total
        offensiveRebounds /= total

    # Print final normalized probabilities
    print("\nFinal normalized probabilities:")
    print(f"2P: {twoPointersMade:.3f}, 3P: {threePointersMade:.3f}, Miss: {missedShots:.3f}")
    print(f"TO: {turnovers:.3f}, FT: {freeThrows:.3f}, ORB: {offensiveRebounds:.3f}")
    print(f"Sum: {twoPointersMade + threePointersMade + missedShots + turnovers + freeThrows + offensiveRebounds:.3f}")

    return {
        'twoPointersMade': twoPointersMade,
        'threePointersMade': threePointersMade,
        'missedShots': missedShots,
        'turnovers': turnovers,
        'freeThrows': freeThrows,
        'offensiveRebounds': offensiveRebounds,
        'ft_pct': team_stats.ft_pct  # Pass through actual FT percentage
    }

def create_transition_matrix(probs):
    """Create a transition matrix from the given probabilities"""
    twoPointersMade = probs['twoPointersMade']
    threePointersMade = probs['threePointersMade']
    missedShots = probs['missedShots']
    turnovers = probs['turnovers']
    freeThrows = probs['freeThrows']
    offensiveRebounds = probs['offensiveRebounds']
    
    # Use actual free throw percentage from stats
    ft_pct = 0.7  # Default if not available
    makingBothFreeThrows = ft_pct * ft_pct
    makingAndOne = ft_pct * 0.33
    missedShotAfterFreeThrow = 1 - ft_pct

    # Create transition matrix with proper normalization
    matrix = np.array([
        [0, twoPointersMade, threePointersMade, missedShots, turnovers, freeThrows, offensiveRebounds, 0], 
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, offensiveRebounds, max(0, 1 - offensiveRebounds)],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, makingBothFreeThrows, makingAndOne, missedShotAfterFreeThrow, turnovers, freeThrows, offensiveRebounds, 0],
        [0, twoPointersMade, threePointersMade, missedShots, turnovers, freeThrows, offensiveRebounds, 0],
        [0, 0, 0, 0, 0, 0, 0, 1]
    ])

    # Normalize each row to ensure probabilities sum to 1
    for i in range(len(matrix)):
        row_sum = np.sum(matrix[i])
        if row_sum > 0:
            matrix[i] = matrix[i] / row_sum

    return matrix

def simulate_matchup(team1_name, team2_name, num_simulations=1000):
    """Simulate a game between two teams"""
    print(f"\nSimulating matchup: {team1_name} vs {team2_name}")
    
    # Get team stats
    team1_stats = data(team1_name)
    team2_stats = data(team2_name)
    
    if not team1_stats or not team2_stats:
        print("Could not get stats for one or both teams")
        return None
    
    possessions = ((float(team1_stats.possessions) + float(team2_stats.possessions)) // 2)  # Average possessions played per game between two teams
    print(f"Team 1 possessions: {team1_stats.possessions}")
    print(f"Team 2 possessions: {team2_stats.possessions}")
    print(f"Possessions: {possessions}")
    
    print(f"\nCalculating probabilities for {team1_name}:")
    team1_probs = calculate_balanced_probabilities(team1_stats, team2_stats, possessions)
    
    print(f"\nCalculating probabilities for {team2_name}:")
    team2_probs = calculate_balanced_probabilities(team2_stats, team1_stats, possessions)
    
    # Create transition matrices
    team1_matrix = create_transition_matrix(team1_probs)
    team2_matrix = create_transition_matrix(team2_probs)
    
    # Run simulations
    print(f"\nRunning {num_simulations} simulations...")
    team1_scores = []
    team2_scores = []
    
    for i in range(num_simulations):
        print(f"\rSimulation {i + 1}/{num_simulations}", end="")
        # Only show possession progress for the first simulation
        show_progress = (i == 0)
        score1, score2 = simulate_game(team1_matrix, team2_matrix, points_per_state, possessions, show_progress)
        team1_scores.append(score1)
        team2_scores.append(score2)
    
    print() 
    
    # Calculate statistics
    team1_avg = np.mean(team1_scores)
    team2_avg = np.mean(team2_scores)
    team1_std = np.std(team1_scores)
    team2_std = np.std(team2_scores)
    
    # Print results
    print(f"\n{team1_name}: {team1_avg:.1f} ± {team1_std:.1f} points")
    print(f"{team2_name}: {team2_avg:.1f} ± {team2_std:.1f} points")
    print(f"Predicted winner: {team1_name if team1_avg > team2_avg else team2_name}")
    
    # Return the simulation results
    return team1_avg, team1_std, team2_avg, team2_std

def main():
    # Example
    team1 = "auburn"
    team2 = "duke"
    results = simulate_matchup(team1, team2)
    
    return results

if __name__ == "__main__":
    main()