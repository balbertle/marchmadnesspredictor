import requests
from bs4 import BeautifulSoup
from helpers import getTeams
from scraperFunctions.generalScraper import scrape_team_data, write_to_csv
from scraperFunctions.possessionsScraper import update_team_stats_with_possessions

def main():
    print("\n===== STARTING SCRAPER =====")
    print("Getting list of teams...")
    teams = getTeams()
    print(f"Found {len(teams)} teams to scrape")
    
    scraped_data = []
    for i, team_name in enumerate(teams, 1):
        print(f"\n[{i}/{len(teams)}] Scraping data for {team_name}...")
        team_data = scrape_team_data(team_name)
        if team_data:
            print(f"✓ Successfully scraped data for {team_name}")
            scraped_data.append(team_data)
        else:
            print(f"✗ Failed to scrape data for {team_name}")
    
    print(f"\nSuccessfully scraped data for {len(scraped_data)} out of {len(teams)} teams")
    
    # Write the scraped data to a CSV file
    print("\nWriting data to CSV file...")
    write_to_csv(scraped_data)
    print("CSV file updated successfully")
    
    # Check BPM values
    print("\n===== CHECKING BPM VALUES =====")
    bpm_missing = False
    bpm_zero_count = 0
    bpm_valid_count = 0
    
    for team_data in scraped_data:
        team_name = team_data.get("Team Name", "Unknown")
        bpm = team_data.get("Box Plus/Minus", 0.0)
        
        if bpm == 0.0:
            print(f"⚠️ BPM value is 0.0 for {team_name}")
            bpm_missing = True
            bpm_zero_count += 1
        else:
            print(f"✅ BPM value for {team_name}: {bpm}")
            bpm_valid_count += 1
    
    print(f"\nBPM Summary:")
    print(f"- Valid BPM values: {bpm_valid_count}")
    print(f"- Zero BPM values: {bpm_zero_count}")
    
    if bpm_missing:
        print("\n⚠️ Some teams have missing or zero BPM values. This may affect prediction accuracy.")
        print("Consider manually checking the sports-reference.com website for these teams.")
    else:
        print("\n✅ All teams have valid BPM values.")
    
    print("\nUpdating team stats with possessions...")
    update_team_stats_with_possessions()
    print("Team stats updated successfully")
    
    print("\n===== SCRAPER COMPLETED =====")

if __name__ == "__main__":
    main()