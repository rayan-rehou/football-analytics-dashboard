import sqlite3

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Premier League Analytics | 2024/25")

ranking_query = """
WITH team_games AS (
    SELECT HomeTeam AS team, FTHG AS goals_scored, 'home' AS venue
    FROM matches

    UNION ALL

    SELECT AwayTeam AS team, FTAG AS goals_scored, 'away' AS venue
    FROM matches
)
SELECT team,
       AVG(goals_scored) AS goals_per_match,
       AVG(CASE WHEN venue = 'home' THEN goals_scored END) AS home_average,
       AVG(CASE WHEN venue = 'away' THEN goals_scored END) AS away_average
FROM team_games
GROUP BY team
ORDER BY goals_per_match DESC;
"""

head_to_head_query = """
SELECT Date AS "Match date",
       HomeTeam AS "Home team",
       FTHG AS "Home goals",
       FTAG AS "Away goals",
       AwayTeam AS "Away team"
FROM matches
WHERE (HomeTeam = ? AND AwayTeam = ?)
   OR (HomeTeam = ? AND AwayTeam = ?)
ORDER BY Date;
"""

form_query = """
WITH team_games AS (
    SELECT Date AS match_date, HomeTeam AS team, FTHG AS goals
    FROM matches

    UNION ALL

    SELECT Date AS match_date, AwayTeam AS team, FTAG AS goals
    FROM matches
)
SELECT match_date AS "Match date",
       team AS "Team",
       AVG(goals) OVER (
           PARTITION BY team
           ORDER BY match_date
           ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
       ) AS "Goals per match"
FROM team_games
WHERE team IN (?, ?)
ORDER BY match_date;
"""

connection = sqlite3.connect("football.db")
try:
    summary = pd.read_sql_query(
        "SELECT COUNT(*) AS matches FROM matches",
        connection,
    )
    ranking = pd.read_sql_query(ranking_query, connection)
finally:
    connection.close()

ranking = ranking.rename(columns={
    "team": "Team",
    "goals_per_match": "Goals per match",
})

st.title("Premier League Analytics")
st.caption("2024/25 season")
st.write(
    "Compare clubs’ scoring at home and away, explore head-to-head results, "
    "and track scoring form across the season."
)
st.metric("Matches in the dataset", int(summary["matches"].iloc[0]))

st.subheader("Top 3 teams by goals per match")
top_three = ranking[["Team", "Goals per match"]].head(3)
st.dataframe(top_three.round(2), hide_index=True)

st.subheader("Compare two teams")
teams = sorted(ranking["Team"])
left, right = st.columns(2)

with left:
    first_team = st.selectbox("First team", teams)
    first_stats = ranking[ranking["Team"] == first_team].iloc[0]

    st.metric("Goals per match", f"{first_stats['Goals per match']:.2f}")
    st.metric("Home goals per match", f"{first_stats['home_average']:.2f}")
    st.metric("Away goals per match", f"{first_stats['away_average']:.2f}")

with right:
    second_team = st.selectbox("Second team", teams, index=1)
    second_stats = ranking[ranking["Team"] == second_team].iloc[0]

    st.metric("Goals per match", f"{second_stats['Goals per match']:.2f}")
    st.metric("Home goals per match", f"{second_stats['home_average']:.2f}")
    st.metric("Away goals per match", f"{second_stats['away_average']:.2f}")

st.subheader("Head-to-head results")

if first_team == second_team:
    st.write("Choose two different teams to compare.")
else:
    connection = sqlite3.connect("football.db")
    try:
        head_to_head = pd.read_sql_query(
            head_to_head_query,
            connection,
            params=(first_team, second_team, second_team, first_team),
        )
        form = pd.read_sql_query(
            form_query,
            connection,
            params=(first_team, second_team),
            parse_dates=["Match date"],
        )
    finally:
        connection.close()

    st.dataframe(head_to_head, hide_index=True)

    st.subheader("Scoring form over the season")
    st.write("Average goals over each team's last five matches.")
    st.line_chart(form, x="Match date", y="Goals per match", color="Team")

st.divider()
st.caption(
    "**Created by Rayan Rehou** · Independent football analytics project  \n"
    "Match data from [Football-Data.co.uk](https://www.football-data.co.uk/)"
)