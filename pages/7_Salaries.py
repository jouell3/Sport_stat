import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from utils.data_loader import load_team_salaries

df_salaries, df_team_salaries = load_team_salaries()

list_teams = df_salaries['full_team_name'].unique()

st.title("NBA Salaries Analysis -- search by team or player")

st.subheader("Search by team")
selected_team = st.selectbox("Select a team:", list_teams)
years = st.slider("Select a year range (To only display the players within these years):", min_value=int(df_salaries['year'].min()), max_value=int(df_salaries['year'].max()), value=(int(df_salaries['year'].min()), int(df_salaries['year'].max())))

players_from_team = df_salaries[df_salaries['full_team_name'] == selected_team]['player'].unique()
players_years = df_salaries[df_salaries['player'].isin(players_from_team) & df_salaries['year'].between(years[0], years[1])]['player'].unique()
#refine the search from player of that team

search_team = st.selectbox("Select a player from the team:", players_years)


if selected_team:
    team_salaries = df_salaries[df_salaries['full_team_name'] == selected_team].sort_values('year')
    total_salaries = team_salaries.groupby('year')['sum_salary'].sum().reset_index()
    mean_salaries = team_salaries.groupby('year')['sum_salary'].mean().reset_index()
    player_salary = team_salaries[team_salaries['player'] == search_team].sort_values('year')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=team_salaries['year'], y=team_salaries['sum_salary'], mode='markers', name="Salary per player", hovertext=team_salaries['player']))
    fig.add_trace(go.Scatter(x=mean_salaries['year'], y=mean_salaries['sum_salary'], mode='lines', name=f"{selected_team} - Mean Salary"))
    fig.add_trace(go.Scatter(x=player_salary['year'], y=player_salary['sum_salary'], mode='lines+markers', name=search_team))
    fig.update_layout(title=f"{selected_team} - Salary by player for each Season", xaxis_title="Season", yaxis_title="Total Salary (USD)", height=500)
    st.plotly_chart(fig, width='stretch')
    
    st.subheader("Description")
    st.text(f"The graph above shows the salary of each player in {selected_team} for each season (markers) and the mean salary for the team (line). Hover over the markers to see the player's name. Below is a graph showing the total salary for the team by season.")
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=total_salaries['year'], y=total_salaries['sum_salary'], mode='lines', name=f"{selected_team} - Total Salary", showlegend=True))
    fig2.update_layout(title=f"{selected_team} - Total Salary by Season", xaxis_title="Season", yaxis_title="Total Salary (USD)", height=500)
    st.plotly_chart(fig2, width='stretch')
    st.subheader("Description")
    st.text(f"The graph above shows the total salary for {selected_team} by season. This can be used to analyze the team's salary trends over time and compare it with their performance in those seasons.")


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