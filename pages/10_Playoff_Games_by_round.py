import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from utils.data_loader import load_games, load_team_id_name_dict
from utils.figure_constructor import final_figure, first_round_figure, semi_round_figure, conf_round_figure

df_games_playoff = load_games()
df_games = df_games_playoff[(df_games_playoff["gameType"] == "Playoffs")]
dict_teamID = load_team_id_name_dict()

def label_color_home(series):
    return series.map(home_label_colors).fillna(default_color)

def label_color_away(series):
    return series.map(away_label_colors).fillna(default_color)

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



st.title("Playoff Games Analysis by rounds")

st.markdown(f"##### Select a round and a season to see the teams that participated in that round and the results of the games.")
round = st.selectbox("Select a round:", ["First Round", "Conference Semi-finals", "Conference Finals", "NBA Finals"], label_visibility="collapsed")

round_dict = {
    "First Round": ["West - First Round", "East - First Round"],
    "Conference Semi-finals": ["West - Conf. Semifinals", "East - Conf. Semifinals"],
    "Conference Finals": ["West - Conf. Finals", "East - Conf. Finals"],
    "NBA Finals": ["NBA Finals"]}
   
years = sorted(df_games['year'].unique(), reverse=True)[1:]
selected_year = st.selectbox("Select a season:", years, label_visibility="collapsed")



if selected_year:
    # Filter games for the selected year
    if round == "NBA Finals":
        games_final = df_games[(df_games['year'] == selected_year) & (df_games['gameLabel'] == round_dict[round][0])].sort_values("day", ascending=True).reset_index(drop=True)    
        team_final = games_final['hometeamId'].unique() if not games_final.empty else "Unknown"
        team_final_names = ', '.join([dict_teamID.get(team_id, "Unknown") for team_id in team_final])

        st.subheader(f"Teams in the {round} of the {selected_year} season:")
        st.markdown(f"#### :orange[{team_final_names}]")
        
        st.plotly_chart(final_figure(games_final, team_final, team_final_names, selected_year), width='stretch')
    
    elif round == "First Round":
        games_west = df_games[(df_games['year'] == selected_year) & (df_games['gameLabel'] == round_dict[round][0])]
        team_west = games_west['hometeamId'].unique() if not games_west.empty else "Unknown"
        team_west_names = [dict_teamID.get(team_id, "Unknown") for team_id in team_west]
        games_east = df_games[(df_games['year'] == selected_year) & (df_games['gameLabel'] == round_dict[round][1])]
        team_east = games_east['hometeamId'].unique() if not games_east.empty else "Unknown"
        team_east_names = [dict_teamID.get(team_id, "Unknown") for team_id in team_east]
        
        st.subheader(f"Teams in the {round} of the {selected_year} season:")
        st.markdown(f"#### :orange[Western Conference:] \n:orange[{', '.join(team_west_names)}]")
        st.markdown(f"#### :blue[Eastern Conference:] \n:blue[{', '.join(team_east_names)}]")    
        
        figure2 = first_round_figure(games_west, games_east, round, selected_year)
        st.plotly_chart(figure2, width='stretch')
        
    elif round == "Conference Semi-finals":
        games_west = df_games[(df_games['year'] == selected_year) & (df_games['gameLabel'] == round_dict[round][0])]
        team_west = games_west['hometeamId'].unique() if not games_west.empty else "Unknown"
        team_west_names = [dict_teamID.get(team_id, "Unknown") for team_id in team_west]
        games_east = df_games[(df_games['year'] == selected_year) & (df_games['gameLabel'] == round_dict[round][1])]
        team_east = games_east['hometeamId'].unique() if not games_east.empty else "Unknown"
        team_east_names = [dict_teamID.get(team_id, "Unknown") for team_id in team_east]
        
        st.subheader(f"Teams in the {round} of the {selected_year} season:")
        st.markdown(f"#### :orange[Western Conference:] \n:orange[{', '.join(team_west_names)}]")
        st.markdown(f"#### :blue[Eastern Conference:] \n:blue[{', '.join(team_east_names)}]")
        
        figure2 = semi_round_figure(games_west, games_east, round, selected_year)
        st.plotly_chart(figure2, width='stretch')
        
    elif round == "Conference Finals":
        games_west = df_games[(df_games['year'] == selected_year) & (df_games['gameLabel'] == round_dict[round][0])]
        team_west = games_west['hometeamId'].unique() if not games_west.empty else "Unknown"
        team_west_names = [dict_teamID.get(team_id, "Unknown") for team_id in team_west]
        games_east = df_games[(df_games['year'] == selected_year) & (df_games['gameLabel'] == round_dict[round][1])]
        team_east = games_east['hometeamId'].unique() if not games_east.empty else "Unknown"
        team_east_names = [dict_teamID.get(team_id, "Unknown") for team_id in team_east]
        
        st.subheader(f"Teams in the {round} of the {selected_year} season:")
        st.markdown(f"#### :orange[Western Conference:] \n:orange[{', '.join(team_west_names)}]")
        st.markdown(f"#### :blue[Eastern Conference:] \n:blue[{', '.join(team_east_names)}]")

        figure2 = conf_round_figure(games_west, games_east, round, selected_year)
        st.plotly_chart(figure2, width='stretch')


    

    


#st.write(f"{team} had {wins} wins and {losses} losses in the {selected_year} season.")
#st.write(f"Among the home games: {team} had {wins_home} wins, {loose_home} losses.")
#st.write(f"Among the away games: {team} had {wins_away} wins, {loose_away} losses.")