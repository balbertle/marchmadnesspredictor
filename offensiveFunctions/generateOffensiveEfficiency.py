import sys
sys.path.append(r'C:\Users\alber\Documents\marchmadness')
from helpers import getTeams, data
from models import TeamStats

def calculate_offensive_efficiency(team_stats):
    if not team_stats:
        return None
    
    # Calculate possessions
    possessions = team_stats.tov + team_stats.fg2a + team_stats.fg3a + team_stats.ft // 2.15
    
    if possessions <= 0:
        return None
    
    # Calculate offensive efficiency (points per 100 possessions)
    offensive_efficiency = (team_stats.pts / possessions) * 100
    
    return offensive_efficiency

def main():
    teams = getTeams()
    efficiencies = []
    
    for team in teams:
        team_stats = data(team)
        if team_stats:
            efficiency = calculate_offensive_efficiency(team_stats)
            if efficiency:
                efficiencies.append((team_stats.team_name, efficiency))
    
    # Sort by efficiency (highest first)
    efficiencies.sort(key=lambda x: x[1], reverse=True)
    
    # Print results
    print("\nOffensive Efficiency Rankings (points per 100 possessions):")
    print("-" * 50)
    for team_name, efficiency in efficiencies:
        print(f"{team_name}: {efficiency:.2f}")

if __name__ == "__main__":
    main()
