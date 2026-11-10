import sqlite3

import pandas as pd

matches = pd.read_csv("Data/premier_league_2024_25.csv",
    usecols=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"], #usecols tells panda which columns to load
)

matches["Date"] = pd.to_datetime(
    matches["Date"], format="%d/%m/%Y"
).dt.strftime("%Y-%m-%d")

connection = sqlite3.connect("football.db") #opens the database file or creates it if its missing
try:
    matches.to_sql("matches", connection, if_exists="replace", index=False) #writes the Pandas table into SQLite
finally:
    connection.close() #closes the connection whether the save succeeds or raises an error

print(f"Saved {len(matches)} matches to football.db.") #Prints a confirmation of 380 matches into the database