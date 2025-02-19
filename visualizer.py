import numpy as np
import matplotlib.pyplot as plt
import csv


def plot_results(wins, championships):
    teams = list(wins.keys())
    games_won = list(wins.values())
    championships_won = list(championships.values())

    x = np.arange(len(teams))  # X-axis positions
    width = 0.4  # Width of the bars

    fig, ax = plt.subplots(figsize=(12, 6))

    # Bar chart for Games Won
    ax.bar(x + width/2, championships_won, width, label="Championships Won", color='orange')

    ax.set_xlabel("Teams")
    ax.set_ylabel("Count")
    ax.set_title("Tournament Results:Championships Won")
    ax.set_xticks(x)
    ax.set_xticklabels(teams, rotation=45, ha="right")
    ax.legend()

    plt.tight_layout()
    plt.show()

def read_results_from_csv(filename):
    wins = {}
    championships = {}

    with open(filename, mode="r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            team = row[0]
            games_won = int(row[1])
            championships_won = int(row[2])
            wins[team] = games_won
            championships[team] = championships_won

    return wins, championships

# Example usage:
filename = "tournament_results_2025-02-17.csv"  # Replace with actual date
wins, championships = read_results_from_csv(filename)
plot_results(wins, championships)
