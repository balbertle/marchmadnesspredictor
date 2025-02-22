import requests
from bs4 import BeautifulSoup
import csv

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
        writer.writerow(["Team Name", "Third Data Sort"])  # Header
        writer.writerows(data)

    print(f"Data successfully saved to {csv_filename}")

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



