import requests
from bs4 import BeautifulSoup
from helpers import getTeams
from scraperFunctions.possessionsScraper import scrape_possessions_data, merge_csvs
from scraperFunctions.generalScraper import scrape_team_data, write_to_csv


def main():
    teams = getTeams()
    scraped_data = []
    for team_name in teams:
        print(f"Scraping data for {team_name}...")
        team_data = scrape_team_data(team_name)
        if team_data:
            scraped_data.append(team_data)
    
    # Write the scraped data to a CSV file
    write_to_csv(scraped_data)
    scrape_possessions_data()
    merge_csvs("team_data.csv", "team_possessions.csv", "stats.csv")

if __name__ == "__main__":
    main()