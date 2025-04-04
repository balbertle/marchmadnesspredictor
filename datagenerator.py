import csv
from helpers import data

def get_team_points(team, filename="stats.csv"):
    """Get points for and against from the stats.csv file"""
    team_stats = data(team)
    if team_stats:
        points_for = team_stats.pts
        points_against = team_stats.opp_pts
        return points_for, points_against
    return None, None

def pythagoreanExpectation(team, filename="stats.csv"):
    """Calculate Pythagorean expectation using points for and against"""
    ptsFor, ptsAgainst = get_team_points(team, filename)
    if ptsFor is None or ptsAgainst is None:
        print(f"Warning: Team '{team}' not found in the data. Using default probability of 0.5")
        return 0.5
    
    percentage = ptsFor**11.5 / (ptsFor**11.5 + ptsAgainst**11.5)
    return percentage

# For expected points
from offensiveFunctions.expectedPoints import simulate_matchup

# For offensive efficiency
from offensiveFunctions.generateOffensiveEfficiency import calculate_offensive_efficiency
from offensiveFunctions.generateDefensiveEfficiency import calculate_defensive_efficiency

# Calculate offensive efficiency
def calculate_team_efficiency(team_name):
    team_stats = data(team_name)
    if team_stats:
        return calculate_offensive_efficiency(team_stats)
    return None

def calculate_team_defensive_efficiency(team_name):
    team_stats = data(team_name)
    if team_stats:
        return calculate_defensive_efficiency(team_stats)
    return None

def get_team_bpm(team_name):
    """Get the Box Plus/Minus value for a team"""
    team_stats = data(team_name)
    if team_stats:
        return team_stats.bpm
    return None