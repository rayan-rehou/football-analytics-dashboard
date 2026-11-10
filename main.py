import sqlite3

import pandas as pd

DATASET_URL = "https://www.football-data.co.uk/mmz4281/2425/E0.csv"


def build_database(source, database):
    matches = pd.read_csv(
        source,
        usecols=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"],
    )
    matches["Date"] = pd.to_datetime(
        matches["Date"], format="%d/%m/%Y"
    ).dt.strftime("%Y-%m-%d")

    connection = sqlite3.connect(database)
    try:
        matches.to_sql("matches", connection, if_exists="replace", index=False)
    finally:
        connection.close()

    return len(matches)


if __name__ == "__main__":
    count = build_database("Data/premier_league_2024_25.csv", "football.db")
    print(f"Saved {count} matches to football.db.")
