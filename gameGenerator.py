import random
import matplotlib.pyplot as plt
from datagenerator import pythagoreanExpectation
import csv
import datetime

#OUTDATED
def predict_random_winner(team1, team2):
    # Get the win percentages for both teams
    team1_percentage = pythagoreanExpectation(team1)
    team2_percentage = pythagoreanExpectation(team2)
    
    # Normalize the percentages to sum to 100
    total = team1_percentage + team2_percentage
    team1_normalized = team1_percentage / total
    team2_normalized = team2_percentage / total

    print(f"Normalized percentage for {team1} against {team2}: {team1_normalized:.4f}")
    print(f"Normalized percentage for {team2} against {team1}: {team2_normalized:.4f}")

    random_number = random.random()
    if random_number < team1_normalized:
        return team1
    else:
        return team2
    
def predict_probable_winner(team1, team2):
    # Get the win percentages for both teams
    team1_percentage = pythagoreanExpectation(team1)
    team2_percentage = pythagoreanExpectation(team2)
    
    # Normalize the percentages to sum to 100
    total = team1_percentage + team2_percentage
    team1_normalized = team1_percentage / total
    team2_normalized = team2_percentage / total

    print(f"Normalized percentage for {team1} against {team2}: {team1_normalized:.4f}")
    print(f"Normalized percentage for {team2} against {team1}: {team2_normalized:.4f}")

    # Initialize win counters
    team1_wins = 0
    team2_wins = 0

    # Simulate 1000 games
    for _ in range(1000):
        random_number = random.random()
        if random_number < team1_normalized:
            team1_wins += 1
        else:
            team2_wins += 1

    # Calculate winning percentages
    team1_win_percentage = (team1_wins / 1000) * 100
    team2_win_percentage = (team2_wins / 1000) * 100
    if team1_win_percentage > team2_win_percentage:
        return team1
    return team2

def simulate_tournament(teams, num_simulations=100):
    wins = {team: 0 for team in teams}
    championships = {team: 0 for team in teams}

    for _ in range(num_simulations):
        round_teams = teams[:]
        while len(round_teams) > 1:
            next_round = []
            for i in range(0, len(round_teams), 2):
                if i + 1 < len(round_teams):
                    winner = predict_random_winner(round_teams[i], round_teams[i+1])
                    wins[winner] += 1
                    next_round.append(winner)
                else:
                    next_round.append(round_teams[i])  # Odd team advances automatically
            round_teams = next_round
        
        # Last remaining team is the champion
        champion = round_teams[0]
        championships[champion] += 1

    return wins, championships

def save_results_to_csv(wins, championships):
    today = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"tournament_results_{today}.csv"

    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Team", "Games Won", "Championships Won"])

        for team in wins:
            writer.writerow([team, wins[team], championships[team]])

    print(f"Results saved to {filename}")
teams = ["auburn", "alabama", "florida", "duke", 
        "tennessee", "houston", "purdue", "texas-am", 
        "st-johns-ny", "iowa-state", "texas-tech", "arizona", "memphis", "kentucky", 
        "wisconsin", "michigan", "michigan-state", "missouri", 
        "marquette", "clemson", "maryland", "mississippi-state", 
        "kansas", "mississippi", "louisville"]
