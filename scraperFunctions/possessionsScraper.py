import requests
from bs4 import BeautifulSoup
import csv
import sys
sys.path.append(r'C:\Users\alber\Documents\marchmadness')
from helpers import getTeams, data

def scrape_possessions_data():
    url = 'https://www.teamrankings.com/ncaa-basketball/stat/possessions-per-game'

    # Send a GET request to the webpage
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the data
    table = soup.find('table', {'class': 'datatable'})

    # Initialize a list to store the extracted data
    data = []

    # Iterate over each row in the table body
    for row in table.tbody.find_all('tr'):
        # Find all 'td' elements in the row
        cells = row.find_all('td')
        if len(cells) >= 3:
            # Extract the team name (second 'td' element)
            team_name = cells[1].get('data-sort')
            
            # Extract the third 'data-sort' value
            third_data_sort = cells[2].get('data-sort')
            
            # Append to data list
            data.append([team_name, third_data_sort])

    # Save the extracted data to a CSV file
    csv_filename = "team_possessions.csv"

    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Team Name", "Possessions Per Game"])  # Header
        writer.writerows(data)

    print(f"Data successfully saved to {csv_filename}")
    return data

def merge_csvs(full_stats_file, possessions_file, output_file):
    def normalize_team_name(name):
        """Normalize team names to match across both datasets."""
        name = name.lower().replace(" ", "-")
        replacements = {
            "st-johns": "st-johns-ny",
            "texas-a&m": "texas-am",
            "s-mississippi": "mississippi-state",
            "michigan-st" : "michigan-state",
            "iowa-st" : "iowa-state"
        }
        return replacements.get(name, name)

    # Load full stats data
    full_stats = {}
    with open(full_stats_file, mode="r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)  # Read header
        for row in reader:
            team_name = normalize_team_name(row[0])
            full_stats[team_name] = row

    # Load possessions data
    possessions = {}
    with open(possessions_file, mode="r", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            team_name = normalize_team_name(row[0])
            possessions[team_name] = row[1]

    # Merge data
    merged_data = []
    new_header = header + ["Possessions Per Game"]

    for team, stats in full_stats.items():
        pos_per_game = possessions.get(team, "N/A")
        merged_data.append(stats + [pos_per_game])

    # Save merged data
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(new_header)
        writer.writerows(merged_data)

    print(f"Merged data saved to {output_file}")

def update_team_stats_with_possessions(csv_file_path="stats.csv"):
    """Update the CSV file with possessions data from the scraping"""
    # First scrape the possessions data
    possessions_data = scrape_possessions_data()
    
    # Create a dictionary of team names to possessions
    possessions_dict = {}
    for team_name, possessions in possessions_data:
        normalized_name = team_name.lower().replace(" ", "-")
        possessions_dict[normalized_name] = float(possessions)
    
    # Read the existing CSV file
    rows = []
    with open(csv_file_path, mode="r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)  # Read header
        
        # Check if "Possessions" column already exists
        if "Possessions" not in header:
            header.append("Possessions")
            possession_index = len(header) - 1
        else:
            possession_index = header.index("Possessions")
        
        # Read all rows
        for row in reader:
            team_name = row[0].lower().replace(" ", "-")
            if team_name in possessions_dict:
                # Ensure row has enough columns
                while len(row) <= possession_index:
                    row.append("")
                # Update possessions value
                row[possession_index] = str(possessions_dict[team_name])
                print(f"Updated {team_name} with {possessions_dict[team_name]} possessions per game")
            rows.append(row)
    
    # Write back to the CSV file
    with open(csv_file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)
    
    print(f"Successfully updated {csv_file_path} with possessions data")

def calculate_expected_possessions(team_stats):
    """
    Calculate expected possessions manually based on team statistics.
    This is an alternative to scraping possessions data.
    
    Formula: Possessions = FGA + 0.44 * FTA - ORB + TOV
    
    Args:
        team_stats: TeamStats object containing team statistics
        
    Returns:
        float: Estimated possessions per game
    """
    # Calculate total field goal attempts
    fga = team_stats.fg2a + team_stats.fg3a
    
    # Calculate estimated possessions
    # Formula: Possessions = FGA + 0.44 * FTA - ORB + TOV
    estimated_possessions = fga + 0.44 * team_stats.fta - team_stats.orb + team_stats.tov
    
    # Divide by number of games to get per game average
    
    return estimated_possessions

def update_team_stats_with_calculated_possessions(csv_file_path="stats.csv"):
    """Update the CSV file with manually calculated possessions data in a new column"""
    # Read the existing CSV file
    rows = []
    with open(csv_file_path, mode="r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)  # Read header
        
        # Add "Expected Possessions" column if it doesn't exist
        if "Expected Possessions" not in header:
            header.append("Expected Possessions")
            expected_possession_index = len(header) - 1
        else:
            expected_possession_index = header.index("Expected Possessions")
        
        # Get column indices for required stats
        team_name_index = 0
        fg2a_index = header.index("2P Attempted") if "2P Attempted" in header else None
        fg3a_index = header.index("3P Attempted") if "3P Attempted" in header else None
        fta_index = header.index("Free Throws Attempted") if "Free Throws Attempted" in header else None
        orb_index = header.index("Offensive Rebounds") if "Offensive Rebounds" in header else None
        tov_index = header.index("Turnovers") if "Turnovers" in header else None
        games_index = header.index("Games") if "Games" in header else None
        
        # Check if all required columns exist
        if None in [fg2a_index, fg3a_index, fta_index, orb_index, tov_index, games_index]:
            print("Error: Missing required columns in CSV file")
            return
        
        # Read all rows
        for row in reader:
            # Skip any rows that match the header (duplicate headers in the file)
            if row[0] == "Team Name":
                continue
                
            team_name = row[team_name_index]
            
            try:
                # Extract required stats
                fg2a = int(row[fg2a_index])
                fg3a = int(row[fg3a_index])
                fta = int(row[fta_index])
                orb = int(row[orb_index])
                tov = int(row[tov_index])
                games = int(row[games_index])
                
                # Calculate possessions
                fga = fg2a + fg3a
                estimated_possessions = fga + 0.44 * fta - orb + tov
                possessions_per_game = estimated_possessions / max(1, games)
                
                # Ensure row has enough columns
                while len(row) <= expected_possession_index:
                    row.append("")
                
                # Update expected possessions value
                row[expected_possession_index] = str(round(possessions_per_game, 2))
                print(f"Updated {team_name} with {possessions_per_game:.2f} expected possessions per game")
            except ValueError as e:
                print(f"Warning: Could not process row for {team_name}: {e}")
                continue
                
            rows.append(row)
    
    # Write back to the CSV file
    with open(csv_file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)
    
    print(f"Successfully updated {csv_file_path} with calculated expected possessions data")

def main():
    # Example usage
    # update_team_stats_with_possessions()  # Use scraper
    update_team_stats_with_calculated_possessions()  # Use manual calculation

# Update the default stats.csv file with expected possessions
update_team_stats_with_calculated_possessions()


