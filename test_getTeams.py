from helpers import getTeams

def test_getTeams():
    print("Testing getTeams() function...")
    teams = getTeams()
    
    if not teams:
        print("No teams found!")
        return
    
    print(f"\nFound {len(teams)} teams:")
    for i, team in enumerate(teams, 1):
        print(f"{i}. {team}")
    
    print("\nFirst few team stats:")
    for team in teams[:3]:  # Show details for first 3 teams
        print(f"\nTeam: {team}")
        team_stats = data(team)
        if team_stats:
            print(f"Points: {team_stats.pts}")
            print(f"Field Goal %: {team_stats.fg_pct:.3f}")
            print(f"3PT %: {team_stats.fg3_pct:.3f}")
            print(f"Effective FG %: {team_stats.efg:.3f}")
        else:
            print("Could not get team stats")

if __name__ == "__main__":
    test_getTeams() 