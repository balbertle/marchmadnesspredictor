import sys
sys.path.append(r'C:\Users\alber\Documents\marchmadness')
from helpers import getTeams, data
from models import TeamStats

def calculate_defensive_efficiency(team_stats):
    if not team_stats:
        return None
    
    # Calculate possessions
    possessions = team_stats.opp_tov + team_stats.opp_fg2a + team_stats.opp_fg3a + team_stats.opp_ft // 2.15
    
    if possessions <= 0:
        return None
    
    # Calculate defensive efficiency (points per 100 possessions)
    defensive_efficiency = (team_stats.opp_pts / possessions) * 100
    
    return defensive_efficiency

def main():
    teams = getTeams()
    efficiencies = []
    
    for team in teams:
        team_stats = data(team)
        if team_stats:
            efficiency = calculate_defensive_efficiency(team_stats)
            if efficiency:
                efficiencies.append((team_stats.team_name, efficiency))
    
    # Sort by efficiency (highest first)
    efficiencies.sort(key=lambda x: x[1], reverse=True)
    
    # Print results
    print("\ndefensive Efficiency Rankings (points per 100 possessions):")
    print("-" * 50)
    for team_name, efficiency in efficiencies:
        print(f"{team_name}: {efficiency:.2f}")

if __name__ == "__main__":
    main()
