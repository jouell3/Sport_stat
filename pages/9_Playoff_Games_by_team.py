import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from utils.data_loader import load_games, load_team_id_name_dict
from utils.figure_constructor import figure_playoff

df_games_playoff = load_games()
df_games = df_games_playoff[(df_games_playoff["gameType"] == "Playoffs")]
dict_teamID = load_team_id_name_dict()

home_label_colors = {
    "West - First Round": "#56B4E9",
    "East - First Round": "#009E73",
    "East - Conf. Semifinals": "#F0E442",
    "West - Conf. Semifinals": "#E69F00",
    "East - Conf. Finals": "#CC79A7",
    "West - Conf. Finals": "#0072B2",
    "NBA Finals": "#D55E00"
}

away_label_colors = {
    "West - First Round": "#BDE9FF",
    "East - First Round": "#66E0B3",
    "East - Conf. Semifinals": "#FFF3A1",
    "West - Conf. Semifinals": "#FFC97A",
    "East - Conf. Finals": "#F2B6D9",
    "West - Conf. Finals": "#66B6FF",
    "NBA Finals": "#FF9A7A",
} 
default_color = "#D5F49C" 


st.title("Games Analysis")

teams = sorted(df_games['hometeamCity'].unique())
team2 = st.selectbox("Select a team (by the town of the team):", sorted(dict_teamID.values()), index=0)
team = [key for key, value in dict_teamID.items() if value == team2][0]


playoff_team_year = df_games[(df_games['hometeamId'] == team) | (df_games['awayteamId'] == team)].reset_index(drop=True)
   
years = sorted(playoff_team_year['year'].unique(), reverse=True)[1:]

st.markdown(f"### {team2} had playoff games in the following seasons: " )
st.markdown(f":orange[{', '.join(map(str, years))}].")
st.markdown("### Select a season to see the details of the playoff games for that season.")
selected_year = st.selectbox("Select a season to see the details of the playoff games for that season.", years, label_visibility="collapsed")

if selected_year:
    # Filter games for the selected year
    games_year = df_games[df_games['year'] == selected_year]
    games_team_year = games_year[(games_year['hometeamId'] == team) | (games_year['awayteamId'] == team)].reset_index(drop=True)
    #games_team_year = games_team_year.iloc[::-1]
    games_team_year["selected_team_score"] = np.where(games_team_year["hometeamId"] == team, games_team_year["homeScore"], games_team_year["awayScore"])
    games_team_year["opponent_score"] = np.where(games_team_year["hometeamId"] == team, games_team_year["awayScore"], games_team_year["homeScore"])
    home_games = games_team_year[games_team_year['hometeamId'] == team].sort_index().reset_index()
    away_games = games_team_year[games_team_year['awayteamId'] == team].sort_index().reset_index()
    
    team_games = df_games[(df_games['hometeamId'] == team) | (df_games['awayteamId'] == team)].copy()
    
    selected_games = games_team_year[(games_team_year["seriesGameNumber"] == 1)]
    opponents = []
    for index, row in selected_games.iterrows():
        opponent_id = row['awayteamId']
        opponent_id2 = row['hometeamId']
        opponents.append(dict_teamID.get(opponent_id, "Unknown") if opponent_id != team else dict_teamID.get(opponent_id2, "Unknown"))
        
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
    

    wins_losses_by_year["delta"] = wins_losses_by_year['team_win'] - wins_losses_by_year['team_loss']  
    
    st.write("### :orange[Legend for Game Labels]") # Home Colors home_colors_html = "" st.write("#### Home Colors") for label, color in home_label_colors.items(): home_colors_html += f"<div style='display: flex; align-items: center;'><div style='width: 20px; height: 20px; background-color: {color}; margin-right: 10px;'></div><span>{label}</span></div>" st.markdown(home_colors_html, unsafe_allow_html=True)

    # Home Colors
    st.write(f"#### :blue[{team2}]")
    list_playoff_labels = games_team_year['gameLabel'].unique()[::-1]
    home_colors_html = ""
    for label in list_playoff_labels:
        color = home_label_colors.get(label, default_color)
        home_colors_html += f"<div style='display: inline-block; align-items: center; margin-right: 10px;'><div style='width: 20px; height: 20px; background-color: {color}; display: inline-block; margin-right: 5px;'></div><span style='display: inline-block;'>{label}</span></div>"

    st.markdown(home_colors_html, unsafe_allow_html=True)

    # Away Colors
    st.write("#### :blue[Opponents]")
    st.markdown(f'{", ".join(opponents)}', unsafe_allow_html=True)
    away_colors_html = ""
    for label in list_playoff_labels:
        color = away_label_colors.get(label, default_color)
        away_colors_html += f"<div style='display: inline-block; align-items: center; margin-right: 10px;'><div style='width: 20px; height: 20px; background-color: {color}; display: inline-block; margin-right: 5px;'></div><span style='display: inline-block;'>{label}</span></div>"

    st.markdown(away_colors_html, unsafe_allow_html=True)
     
    custom_order = [
    "West - First Round",
    "East - First Round",
    "West - Conf. Semifinals",
    "East - Conf. Semifinals",
    "West - Conf. Finals",
    "East - Conf. Finals",
    "NBA Finals"
]

    # Create a mapping for the order
    order_mapping = {label: i for i, label in enumerate(custom_order)}

    # Sort home_games and away_games based on the custom order
    home_games['order'] = home_games['gameLabel'].map(order_mapping)
    away_games['order'] = away_games['gameLabel'].map(order_mapping)
    
    home_games = home_games.sort_values('order').reset_index()
    away_games = away_games.sort_values('order').reset_index()
    
    figure_1 = figure_playoff(games_team_year, wins_losses_by_year, team2)

    st.plotly_chart(figure_1, width='stretch')


#st.write(f"{team} had {wins} wins and {losses} losses in the {selected_year} season.")
#st.write(f"Among the home games: {team} had {wins_home} wins, {loose_home} losses.")
#st.write(f"Among the away games: {team} had {wins_away} wins, {loose_away} losses.")
