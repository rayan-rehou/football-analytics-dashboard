import sqlite3

import pandas as pd

SEASON = "2026/27"                                                  # LIVE season shown in the app 
CSV_URL = "https://www.football-data.co.uk/mmz4281/2627/E0.csv"     # link to the current season's CSV (2627 = 2026/27, E0 = Premier League)


def load_matches():                                                 #the whole job is now a function, so app.py can call it by itself
    matches = pd.read_csv(CSV_URL,                                  #were accessing the CSV file (now straight from the website) and only reading: Date, HomeTeam, AwayTeam, FTHG, FTAG
        usecols=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"],   #usecols tells panda which columns to load
    )

    matches = matches.dropna()                                      #removes empty rows (the live file can have blank lines at the end)
    matches[["FTHG", "FTAG"]] = matches[["FTHG", "FTAG"]].astype(int)   #makes sure goals are whole numbers (1, not 1.0)

    matches["Date"] = pd.to_datetime(                               # Change dates from DD/MM/YYYY to YYYY-MM-DD so they sort correctly in SQL
        matches["Date"], dayfirst=True                              # read the text as a real date (day/month/year)
    ).dt.strftime("%Y-%m-%d")                                       # write it back as text: year-month-day

    connection = sqlite3.connect("football.db")                     #opens the database file or creates it if its missing
    try:
        matches.to_sql("matches", connection, if_exists="replace", index=False)    #writes the Pandas table into SQLite database
    finally:
        connection.close()                                          #closes the connection whether the save succeeds or raises an error (making sure everything is stored after changing)


if __name__ == "__main__":                                          # only runs when you run main.py yourself (not when app.py uses it)
    load_matches()
