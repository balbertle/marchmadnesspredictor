import csv

def data(team):
    with open("team_data.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Team Name"].lower() == team.lower():
                return (
                    row["Team Name"],
                    float(row["Field Goal Percentage"]),
                    int(row["2P Made"]),
                    int(row["2P Attempted"]),
                    float(row["2P Percentage"]),
                    int(row["3P Made"]),
                    int(row["3P Attempted"]),
                    float(row["3P Percentage"]),
                    int(row["Free Throws Made"]),
                    int(row["Free Throws Attempted"]),
                    float(row["Free Throw Percentage"]),
                    int(row["Offensive Rebounds"]),
                    int(row["Defensive Rebounds"]),
                    int(row["Total Rebounds"]),
                    int(row["Assists"]),
                    int(row["Steals"]),
                    int(row["Blocks"]),
                    int(row["Turnovers"]),
                    int(row["Personal Fouls"]),
                    int(row["Total Points"])
                )
    return None

def getTeams():
    return ["auburn", "alabama", "florida", "duke", 
        "tennessee", "houston", "purdue", "texas-am", 
        "st-johns-ny", "iowa-state", "texas-tech", "arizona", "memphis", "kentucky", 
        "wisconsin", "michigan", "michigan-state", "missouri", 
        "marquette", "clemson", "maryland", "mississippi-state", 
        "kansas", "mississippi", "louisville"]