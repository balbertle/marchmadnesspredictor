import csv
import sys
sys.path.append(r'C:\Users\alber\Documents\marchmadness')

from helpers import getTeams, data

def get_team_fg(team, filename="stats.csv"):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Team Name"].lower() == team.lower():
                return int(row[""]), int(row["Field Goals Attempted"]), int(row["Three Pointer's Made"])
    return None, None, None

def efg_pct_generator(team, filename="stats.csv"):
    fg, fga, fg3 = get_team_fg(team, filename)
    efg_pct = (fg + 0.5 * fg3) / fga
    return efg_pct

# Assuming `getTeams()` and `efg_pct_generator(team)` are defined elsewhere
teams = getTeams()

# Initialize list for the merged data
merged_data = []

# Define the new header with the "Effective Field Goal %" column
new_header = []

# Read the existing file and add EFG to the header
with open("stats.csv", mode="r", newline="") as file:
    reader = csv.reader(file)
    header = next(reader)  # Read header
    new_header = header + ["Effective Field Goal %"]  # Add new header column

    # Iterate over each team, get their EFG, and append to merged data
    rows = list(reader)  # Read all rows
    for team in teams:
        efg_pct = efg_pct_generator(team)
        
        for row in rows:
            if row[0] == team:  # Assuming the team name is in the first column
                row.append(efg_pct)  # Append the EFG value
                merged_data.append(row)
                break  # Move on to the next team

# Write the new data, including the EFG column, directly to stats.csv
with open("stats.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(new_header)  # Write the new header
    writer.writerows(merged_data)  # Write the data

print(f"Merged data saved to stats.csv")

    
