from datagenerator import offensiveEfficiency

teams = ["auburn", "alabama", "florida", "duke", 
        "tennessee", "houston", "purdue", "texas-am", 
        "st-johns-ny", "iowa-state", "texas-tech", "arizona", "memphis", "kentucky", 
        "wisconsin", "michigan", "michigan-state", "missouri", 
        "marquette", "clemson", "maryland", "mississippi-state", 
        "kansas", "mississippi", "louisville"]
for team in teams:
    print(f"{team} eFG: {offensiveEfficiency(team):.3f}")
