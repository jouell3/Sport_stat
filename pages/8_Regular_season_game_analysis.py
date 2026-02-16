import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from utils.data_loader import load_games, load_team_id_name_dict
from utils.figure_constructor import regular_season_figure


df_games_regular = load_games()
dict_teamID = load_team_id_name_dict()
df_games = df_games_regular[(df_games_regular["gameType"] == "Regular Season")]

st.title("Games Analysis")

teams = sorted(df_games['hometeamCity'].unique())

st.markdown(f"##### Select a team and a season to see the results of the regular season games for that team in that season.")
team2 = st.selectbox("Select a team (by the town of the team):", sorted(dict_teamID.values()), index=0, label_visibility="collapsed")
team = [key for key, value in dict_teamID.items() if value == team2][0]

years = sorted(df_games['year'].unique(), reverse=True)[1:]
selected_year = st.selectbox("Select a season (From 1946 to 2025):", years, label_visibility="collapsed")

if selected_year:
    # Filter games for the selected year
    games_year = df_games[df_games['year'] == selected_year]
    games_team_year = games_year[(games_year['hometeamId'] == team) | (games_year['awayteamId'] == team)].reset_index(drop=True)
    home_games = games_team_year[games_team_year['hometeamId'] == team].reset_index()
    away_games = games_team_year[games_team_year['awayteamId'] == team].reset_index()
    
    wins = ((home_games['homeScore'] > home_games['awayScore']).sum() + (away_games['awayScore'] > away_games['homeScore']).sum())
    wins_home = (home_games['homeScore'] > home_games['awayScore']).sum()
    wins_away = (away_games['awayScore'] > away_games['homeScore']).sum()
    loose_home = (home_games['homeScore'] < home_games['awayScore']).sum()
    loose_away = (away_games['awayScore'] < away_games['homeScore']).sum()
    losses = ((home_games['homeScore'] < home_games['awayScore']).sum() + (away_games['awayScore'] < away_games['homeScore']).sum())
    
    team_games = df_games[(df_games['hometeamId'] == team) | (df_games['awayteamId'] == team)].copy()
    team_games["team_win"] = np.where(
        (team_games["hometeamId"] == team) & (team_games["homeScore"] > team_games["awayScore"]),
        1,
        np.where(
            (team_games["awayteamId"] == team) & (team_games["awayScore"] > team_games["homeScore"]),
            1,
            0,
        ),
    )
    team_games["team_loss"] = 1 - team_games["team_win"]

    wins_losses_by_year = (
        team_games.groupby("year")[["team_win", "team_loss"]].sum().reset_index())
    
    home_games["delta"] = home_games['homeScore'] - home_games['awayScore']  # Add a constant to shift the difference for better visualization
    away_games["delta"] = away_games['awayScore'] - away_games['homeScore']  # Add a constant to shift the difference for better visualization
    wins_losses_by_year["delta"] = wins_losses_by_year['team_win'] - wins_losses_by_year['team_loss']  # Add a constant to shift the difference for better visualization
    wins_losses_by_year["reference"] = 25  # Add a reference line at 25 for better visualization    

    
    st.subheader(f"{team2} had {wins} wins and {losses} losses in the {selected_year} season.")
    st.write(f"Among the home games: {team2} had {wins_home} wins, {loose_home} losses.")
    st.write(f"Among the away games: {team2} had {wins_away} wins, {loose_away} losses.")
    
    figure_1 = regular_season_figure(home_games, away_games, wins_losses_by_year, team2)
    
    st.plotly_chart(figure_1, width='stretch')
    
    