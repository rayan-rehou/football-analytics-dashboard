# Live Premier League Analytics Dashboard

A live dashboard for the current 2026/27 Premier League season. It downloads the latest results every 6 hours, so the stats keep up as the season goes on. Built by Rayan Rehou as an independent portfolio project.

**[Open the live dashboard](https://rayan-rehou-football-analytics.streamlit.app/)** · **[Watch the demo](https://rayan-rehou.github.io/#football)**

![Dashboard showing the 2026/27 season, matches played so far, and the top 3 teams by goals per match](https://rayan-rehou.github.io/premier-league-live-poster.webp)

## What you can explore

- See how many matches have been played so far this season.
- See the three clubs with the highest goals per match.
- Compare any two clubs' overall, home, and away scoring averages.
- View their head-to-head scores and match dates, or a message if they haven't played each other yet.
- Follow each club's scoring form with a rolling average over its latest five matches.

## How it works

- `main.py` downloads the current season's CSV straight from Football-Data.co.uk, cleans it with Pandas (removes empty rows, makes goals whole numbers, changes dates to YYYY-MM-DD) and saves it to a SQLite database.
- `app.py` runs that download on each visit, but a 6-hour cache (`st.cache_data(ttl=6 * 60 * 60)`) means the data is only really downloaded every 6 hours.
- SQL calculates the rankings, the home and away averages, and the rolling scoring averages, and Streamlit displays the results.

## Run locally

From the project folder on Windows, run these commands in PowerShell.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL printed in the terminal. The app downloads the latest data by itself. To rebuild `football.db` without opening the app, run `main.py`.

## Data source

Match results come from [Football-Data.co.uk](https://www.football-data.co.uk/).
