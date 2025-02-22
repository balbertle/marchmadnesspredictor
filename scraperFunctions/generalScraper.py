import sys
sys.path.append(r'C:\Users\alber\Documents\marchmadness')
from helpers import getTeams, data
import requests
from bs4 import BeautifulSoup
import csv


def scrape_team_data(team_name):
    # Construct the URL with the team name
    url = f"https://www.sports-reference.com/cbb/schools/{team_name}/men/2025.html"
    
    # Send a GET request to the website
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (e.g., 404, 429)
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve data for {team_name}. Error: {e}")
        return None
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data for {team_name}. Status code: {response.status_code}")
        return None
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    

    # Scraping data
    games_element = soup.find("td", {"data-stat": "games"})
    mp_element = soup.find("td", {"data-stat": "mp"})
    fg_element = soup.find("td", {"data-stat": "fg"})
    fga_element = soup.find("td", {"data-stat": "fga"})
    fg_pct_element = soup.find("td", {"data-stat": "fg_pct"})
    fg2_element = soup.find("td", {"data-stat": "fg2"})
    fg2a_element = soup.find("td", {"data-stat": "fg2a"})
    fg2_pct_element = soup.find("td", {"data-stat": "fg2_pct"})
    fg3_element = soup.find("td", {"data-stat": "fg3"})
    fg3a_element = soup.find("td", {"data-stat": "fg3a"})
    fg3_pct_element = soup.find("td", {"data-stat": "fg3_pct"})
    ft_element = soup.find("td", {"data-stat": "ft"})
    fta_element = soup.find("td", {"data-stat": "fta"})
    ft_pct_element = soup.find("td", {"data-stat": "ft_pct"})
    orb_element = soup.find("td", {"data-stat": "orb"})
    drb_element = soup.find("td", {"data-stat": "drb"})
    trb_element = soup.find("td", {"data-stat": "trb"})
    ast_element = soup.find("td", {"data-stat": "ast"})
    stl_element = soup.find("td", {"data-stat": "stl"})
    blk_element = soup.find("td", {"data-stat": "blk"})
    tov_element = soup.find("td", {"data-stat": "tov"})
    pf_element = soup.find("td", {"data-stat": "pf"})
    pts_element = soup.find("td", {"data-stat": "pts"})
    

    try:
        games_element = int(games_element.get_text(strip=True))
        mp_element = int(mp_element.get_text(strip=True))
        fg_element = int(fg_element.get_text(strip=True))
        fga_element = int(fga_element.get_text(strip=True))
        fg_pct_element = float(fg_pct_element.get_text(strip=True))
        fg2_element = int(fg2_element.get_text(strip=True))
        fg2a_element = int(fg2a_element.get_text(strip=True))
        fg2_pct_element = float(fg2_pct_element.get_text(strip=True))
        fg3_element = int(fg3_element.get_text(strip=True))
        fg3a_element = int(fg3a_element.get_text(strip=True))
        fg3_pct_element = float(fg3_pct_element.get_text(strip=True))
        ft_element = int(ft_element.get_text(strip=True))
        fta_element = int(fta_element.get_text(strip=True))
        ft_pct_element = float(ft_pct_element.get_text(strip=True))
        orb_element = int(orb_element.get_text(strip=True))
        drb_element = int(drb_element.get_text(strip=True))
        trb_element = int(trb_element.get_text(strip=True))
        ast_element = int(ast_element.get_text(strip=True))
        stl_element = int(stl_element.get_text(strip=True))
        blk_element = int(blk_element.get_text(strip=True))
        tov_element = int(tov_element.get_text(strip=True))
        pf_element = int(pf_element.get_text(strip=True))
        pts_element = int(pts_element.get_text(strip=True))
    except ValueError as e:
        print(f"Failed to convert points to integers for {team_name}. Error: {e}")
        return None

    
    print("finished scrape_team_data")
    print(mp_element)
    print(fg_element)
    return (
    team_name, mp_element, fg_element, fga_element, fg_pct_element, fg2_element, fg2a_element, fg2_pct_element, fg3_element,
    fg3a_element, fg3_pct_element, ft_element, fta_element, ft_pct_element, orb_element, drb_element,
    trb_element, ast_element, stl_element, blk_element, tov_element, pf_element, pts_element,
)

def write_to_csv(data, filename="team_data.csv"):
    # Define the headers if they are not already present in the CSV
    headers = [
        "Team Name", "Minutes Played", "Field Goals Made", "Field Goals Attempted", 
        "Field Goal Percentage", "2P Made", "2P Attempted", 
        "2P Percentage", "3P Made", "3P Attempted", "3P Percentage",
        "Free Throws Made", "Free Throws Attempted", "Free Throw Percentage",
        "Offensive Rebounds", "Defensive Rebounds", "Total Rebounds",
        "Assists", "Steals", "Blocks", "Turnovers", "Personal Fouls", "Total Points", "Effective Field Goal %"
    ]

    # Open file in append mode to keep existing content
    try:
        with open(filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Check if the file is empty or does not exist to write the header
            if file.tell() == 0:
                writer.writerow(headers)  # Write the headers if the file is empty
            writer.writerows(data)  # Write the data rows
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

