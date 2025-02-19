import requests
from bs4 import BeautifulSoup
import time
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
    
    # Extract "Points For" (pts)
    pts_element = soup.find("td", {"data-stat": "pts"})
    if pts_element:
        pts = pts_element.get_text(strip=True)
        print(f"Points For: {pts}")
    else:
        print(f"Points For data not found for {team_name}.")
        return None
    
    # Extract "Points Against" (opp_pts)
    opp_pts_element = soup.find("td", {"data-stat": "opp_pts"})
    if opp_pts_element:
        opp_pts = opp_pts_element.get_text(strip=True)
        print(f"Points Against: {opp_pts}")
    else:
        print(f"Points Against data not found for {team_name}.")
        return None
    
    # Convert points to integers
    try:
        pts = int(pts)
        opp_pts = int(opp_pts)
    except ValueError as e:
        print(f"Failed to convert points to integers for {team_name}. Error: {e}")
        return None
    
    # Add a delay to avoid rate limiting
    time.sleep(1)  # Adjust the delay as needed
    
    return (team_name, pts, opp_pts)

def write_to_csv(data, filename="team_data.csv"):
    # Define the CSV column headers
    headers = ["Team Name", "Points For", "Points Against"]
    
    # Write data to the CSV file
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write the headers
        writer.writerows(data)  # Write the data rows

def main():
    # List of team names to scrape
    
    oneSeed = "auburn"
    twoSeed = "alabama"
    threeSeed = "florida"
    fourSeed = "duke"
    fiveSeed = "tennessee"
    sixSeed = "houston"
    sevenSeed = "purdue"
    eightSeed = "texas-am"
    nineSeed = "st-johns-ny"
    tenSeed = "iowa-state"
    elevenSeed = "michigan-state"
    twelveSeed = "texas-tech"
    thirteenSeed = "arizona"
    fourteenSeed = "memphis"
    fifteenSeed = "kentucky"
    sixteenSeed = "wisconsin"
    team_names = [oneSeed, twoSeed, threeSeed, fourSeed, fiveSeed, sixSeed, sevenSeed, eightSeed, nineSeed, tenSeed, elevenSeed, twelveSeed, thirteenSeed, fourteenSeed, fifteenSeed, sixteenSeed]  # Add more teams as needed
    # Scrape data for each team
    scraped_data = []
    for team_name in team_names:
        print(f"Scraping data for {team_name}...")
        team_data = scrape_team_data(team_name)
        if team_data:
            scraped_data.append(team_data)
    
    # Write the scraped data to a CSV file
    write_to_csv(scraped_data)
    print("Data written to team_data.csv")

if __name__ == "__main__":
    main()