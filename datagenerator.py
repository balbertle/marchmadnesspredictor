import csv

def get_team_points(team, filename="team_data.csv"):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Team Name"].lower() == team.lower():
                return int(row["Points For"]), int(row["Points Against"])
    return None, None  # Return None if team is not found

def pythagoreanExpectation(team, filename="team_data.csv"):
    ptsFor, ptsAgainst = get_team_points(team, filename)
    if ptsFor is None or ptsAgainst is None:
        raise ValueError(f"Team '{team}' not found in the data.")
    
    percentage = ptsFor**11.5 / (ptsFor**11.5 + ptsAgainst**11.5)
    return percentage