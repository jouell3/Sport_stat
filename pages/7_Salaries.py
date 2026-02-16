import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from utils.data_loader import load_team_salaries
from utils.figure_constructor import salary_figure, total_salary_figure

df_salaries, df_team_salaries = load_team_salaries()

list_teams2 = df_salaries['full_team_name'].unique()
list_teams = list_teams2[pd.notna(list_teams2)]

st.title("NBA Salaries Analysis -- search by team or player")

st.subheader("Search by team")

st.markdown("##### Select a team to see the salary distribution of its players across seasons. Additionally, you can filter the data by a range of years to focus on specific seasons.")
selected_team = st.selectbox("Select a team:", np.sort(list_teams), key="team_select_1", label_visibility="collapsed")
years = st.slider("Select a year range (To only display the players within these years):", min_value=int(df_salaries['year'].min()), max_value=int(df_salaries['year'].max()), value=(int(df_salaries['year'].min()), int(df_salaries['year'].max())), label_visibility="collapsed")

players_from_team = df_salaries[df_salaries['full_team_name'] == selected_team]['player'].unique()
st.markdown(f"#### You can  select a specific player from that team to highlight its salary history.")
players_years = df_salaries[df_salaries['player'].isin(players_from_team) & df_salaries['year'].between(years[0], years[1])]['player'].unique()
#refine the search from player of that team

search_team = st.selectbox("Select a player from the team:", np.sort(players_years), label_visibility="collapsed")


if selected_team:
    team_salaries = df_salaries[df_salaries['full_team_name'] == selected_team].sort_values('year')
    total_salaries = team_salaries.groupby('year')['sum_salary'].sum().reset_index()
    mean_salaries = team_salaries.groupby('year')['sum_salary'].mean().reset_index()
    median_salaries = team_salaries.groupby('year')['sum_salary'].median().reset_index()
    player_salary = team_salaries[team_salaries['player'] == search_team].sort_values('year')
    
    figure_1 = salary_figure(team_salaries, selected_team, search_team)
    st.plotly_chart(figure_1, width='stretch')
    
    st.subheader("Description")
    st.text(f"The graph above shows the salary of each player in {selected_team} for each season (markers) and the mean salary for the team (line). Hover over the markers to see the player's name. Below is a graph showing the total salary for the team by season.")
    
    grouped_team = df_salaries.groupby(['full_team_name', "year"])['sum_salary'].sum().reset_index()
    selected_team_data = grouped_team[grouped_team['full_team_name'] == selected_team]

    figure_2 = total_salary_figure(grouped_team, selected_team_data, selected_team)
    
    st.plotly_chart(figure_2, width='stretch')
    


st.subheader("It is also possible to search for a player directly and see their salary history across all teams they played for.")

search = st.text_input("Enter player name (partial match, case-insensitive):")

if search: 
    list_players = df_salaries['player'].unique()
    matches = list_players[pd.Series(list_players).str.contains(search, case=False, na=False)]
    if len(matches) == 0:
        st.warning("No players found. Please refine your search.")
    elif len(matches) == 1:
        player = matches[0]
        st.success(f"Found: {player}")
        player_salaries = df_salaries[df_salaries['player'] == player].sort_values('year')
        # --- produce a graph with all the season where data are available ---
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=player_salaries['year'], y=player_salaries['sum_salary'], mode='lines+markers', name=player))
        fig.update_layout(title=f"{player} - Salary by Season", xaxis_title="Season", yaxis_title="Salary (USD)", height=500)
        st.plotly_chart(fig, width='stretch')
  
    else:
        st.info(f"{len(matches)} players found. Please refine your search or select:")
        player = st.selectbox("Select a player:", matches)
        if player:
            player_salaries = df_salaries[df_salaries['player'] == player].sort_values('year')
        # --- produce a graph with all the season where data are available ---
        
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=player_salaries['year'], y=player_salaries['sum_salary'], mode='lines+markers', name=player))
            fig.update_layout(title=f"{player} - Salary by Season", xaxis_title="Season", yaxis_title="Salary (USD)", height=500)
            st.plotly_chart(fig, width='stretch')
            
