import csv

def get_team_fg(team, filename="team_data.csv"):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Team Name"].lower() == team.lower():
                return int(row["Field Goals Made"]), int(row["Field Goals Attempted"]), int(row["Three Pointer's Made"])
    return None, None, None

def efg_pct_cenerator(team, filename="team_data.csv"):
    fg, fga, fg3 = get_team_fg(team, filename)
    efg_pct = (fg + 0.5 * fg3) / fga
    return efg_pct

