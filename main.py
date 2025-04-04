import sys
sys.path.append(r'C:\Users\alber\Documents\marchmadness')
from offensiveFunctions.expectedPoints import simulate_matchup
from datagenerator import pythagoreanExpectation, calculate_team_efficiency, calculate_team_defensive_efficiency, get_team_bpm

import argparse

def predict_winner(team1_name, team2_name, num_simulations=1000):
    """
    Predict the winner of a game between two teams using a weighted approach:
    - 60% weight on the simulation results
    - 35% weight on the Pythagorean expectation
    - 5% weight on offensive efficiency comparison
    
    Args:
        team1_name: Name of the first team
        team2_name: Name of the second team
        num_simulations: Number of simulations to run
        
    Returns:
        tuple: (winner_name, win_probability)
    """
    print(f"\nPredicting winner for {team1_name} vs {team2_name}")
    print("=" * 50)
    
    # Run the simulation
    simulation_result = simulate_matchup(team1_name, team2_name, num_simulations)
    
    if not simulation_result:
        print("Simulation failed. Using only Pythagorean expectation and offensive efficiency.")
        # If simulation fails, use only Pythagorean expectation and offensive efficiency
        team1_pyth = pythagoreanExpectation(team1_name)
        team2_pyth = pythagoreanExpectation(team2_name)
        team1_eff = calculate_team_efficiency(team1_name)
        team2_eff = calculate_team_efficiency(team2_name)
        
        # Calculate weighted probability
        if team1_eff and team2_eff:
            eff_weight = 0.125  # Increase weight when simulation fails
            pyth_weight = 0.875
            
            # Convert offensive efficiencies to win probability
            total_eff = team1_eff + team2_eff
            team1_eff_prob = team1_eff / total_eff if total_eff > 0 else 0.5
            
            # Combine probabilities
            team1_prob = pyth_weight * team1_pyth + eff_weight * team1_eff_prob
            team2_prob = pyth_weight * team2_pyth + eff_weight * (1 - team1_eff_prob)
            
            if team1_prob > team2_prob:
                return team1_name, team1_prob
            else:
                return team2_name, team2_prob
        else:
            # If efficiency calculation fails, use only Pythagorean expectation
            if team1_pyth > team2_pyth:
                return team1_name, team1_pyth
            else:
                return team2_name, team2_pyth
    
    # Extract simulation results
    team1_avg, team1_std = simulation_result[0], simulation_result[1]
    team2_avg, team2_std = simulation_result[2], simulation_result[3]
    
    # Calculate win probability from simulation
    if team1_avg > team2_avg:
        sim_winner = team1_name
        sim_prob = 0.5 + (team1_avg - team2_avg) / (2 * max(team1_std, team2_std))
        sim_prob = max(0.5, min(0.95, sim_prob))  # Clamp between 0.5 and 0.95
    else:
        sim_winner = team2_name
        sim_prob = 0.5 + (team2_avg - team1_avg) / (2 * max(team1_std, team2_std))
        sim_prob = max(0.5, min(0.95, sim_prob))  # Clamp between 0.5 and 0.95
    
    # Get Pythagorean expectation
    team1_pyth = pythagoreanExpectation(team1_name)
    team2_pyth = pythagoreanExpectation(team2_name)
    
    # Get offensive efficiencies
    team1_eff = calculate_team_efficiency(team1_name)
    team2_eff = calculate_team_efficiency(team2_name)

    team1_deff = calculate_team_defensive_efficiency(team1_name)
    team2_deff = calculate_team_defensive_efficiency(team2_name)
    
    # Get BPM values
    team1_bpm = get_team_bpm(team1_name)
    team2_bpm = get_team_bpm(team2_name)

    # Convert offensive efficiencies to win probability
    if team1_deff is not None and team2_deff is not None:
        total_deff = team1_deff + team2_deff
        team1_deff_prob = team1_deff / total_deff if total_deff > 0 else 0.5
        deff_winner = team1_name if team1_deff > team2_deff else team2_name
        deff_prob = max(team1_deff_prob, 1 - team1_deff_prob)
    else:
        deff_winner = sim_winner  # Default to simulation winner if efficiency calculation fails
        deff_prob = 0.5
        print("Warning: Could not calculate defensive efficiency for one or both teams")
    
    # Convert BPM to win probability
    if team1_bpm is not None and team2_bpm is not None:
        # Normalize BPM values to create a probability
        total_bpm = team1_bpm + team2_bpm
        team1_bpm_prob = team1_bpm / total_bpm if total_bpm > 0 else 0.5
        bpm_winner = team1_name if team1_bpm > team2_bpm else team2_name
        bpm_prob = max(team1_bpm_prob, 1 - team1_bpm_prob)
    else:
        bpm_winner = sim_winner  # Default to simulation winner if BPM calculation fails
        bpm_prob = 0.5
        print("Warning: Could not get BPM for one or both teams")
    
    # Convert offensive efficiencies to win probability
    if team1_eff is not None and team2_eff is not None:
        total_eff = team1_eff + team2_eff
        team1_eff_prob = team1_eff / total_eff if total_eff > 0 else 0.5
        eff_winner = team1_name if team1_eff > team2_eff else team2_name
        eff_prob = max(team1_eff_prob, 1 - team1_eff_prob)
    else:
        eff_winner = sim_winner  # Default to simulation winner if efficiency calculation fails
        eff_prob = 0.5
        print("Warning: Could not calculate offensive efficiency for one or both teams")
    
    # Determine Pythagorean winner
    if team1_pyth > team2_pyth:
        pyth_winner = team1_name
        pyth_prob = team1_pyth
    else:
        pyth_winner = team2_name
        pyth_prob = team2_pyth
    
    # Combine predictions with weights (60% simulation, 20% Pythagorean, 10% offensive efficiency, 10% defensive efficiency, 5% BPM)
    sim_weight = 0.60
    pyth_weight = 0.20
    eff_weight = 0.10
    deff_weight = 0.10
    bpm_weight = 0.05

    # Calculate final probability based on which team is predicted to win
    if sim_winner == team1_name:
        team1_prob = sim_weight * sim_prob + pyth_weight * team1_pyth + eff_weight * team1_eff_prob + deff_weight * team1_deff_prob + bpm_weight * team1_bpm_prob
    else:
        team1_prob = sim_weight * (1 - sim_prob) + pyth_weight * team1_pyth + eff_weight * team1_eff_prob + deff_weight * team1_deff_prob + bpm_weight * team1_bpm_prob
    
    final_winner = team1_name if team1_prob > 0.5 else team2_name
    final_prob = max(team1_prob, 1 - team1_prob)
    
    # Print detailed results
    print("\nDetailed Prediction Results:")
    print(f"Simulation: {sim_winner} wins with {sim_prob:.2%} probability")
    print(f"Pythagorean: {pyth_winner} wins with {pyth_prob:.2%} probability")
    print(f"Offensive Efficiency: {eff_winner} wins with {eff_prob:.2%} probability")
    print(f"Defensive Efficiency: {deff_winner} wins with {deff_prob:.2%} probability")
    print(f"Box Plus/Minus: {bpm_winner} wins with {bpm_prob:.2%} probability")
    print(f"Final Prediction: {final_winner} wins with {final_prob:.2%} probability")
    
    return final_winner, final_prob

def main():
    parser = argparse.ArgumentParser(description='Predict the winner of a basketball game')
    parser.add_argument('team1', help='Name of the first team')
    parser.add_argument('team2', help='Name of the second team')
    parser.add_argument('--simulations', type=int, default=1000, help='Number of simulations to run (default: 1000)')
    
    args = parser.parse_args()
    
    winner, probability = predict_winner(args.team1, args.team2, args.simulations)
    
    print("\nFinal Result:")
    print(f"{winner} is predicted to win with {probability:.2%} probability")

if __name__ == "__main__":
    main() 