import random
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from utils.data_loader import load_all_data, load_nba_stat_definitions
from utils.figure_constructor import create_metric_subplots

st.title("Player Search & Statistics")

df_players, _, _, _ = load_all_data()
stat_dict = load_nba_stat_definitions()

list_players = df_players['player'].unique()

# --- Player search ---
st.markdown(f"##### Enter player name partial match (Surname or name only) is possible, case-insensitive):")
search = st.text_input("Enter player name (partial match (Surname or name only) is possible, case-insensitive):", label_visibility="collapsed")
player = None
if search:

    if search.find(" ") >= 1:
        list_names = search.split(" ")
        matches2 = list_players[pd.Series(list_players).str.contains(list_names[0], case=False, na=False)]
        if len(matches2) == 0:
            st.warning("No players found. Please refine your search.")
        elif len(matches2) == 1:
            matches = matches2[0]
            st.success(f"Found: {search}")
        else:
            matches = matches2[pd.Series(matches2).str.contains(list_names[1], case=False, na=False)]
            player = matches[0]
    else:
        matches = list_players[pd.Series(list_players).str.contains(search, case=False, na=False)]
        if len(matches) == 0:
            st.warning("No players found. Please refine your search.")
        elif len(matches) == 1:
            player = matches[0]
            st.success(f"Found: {player}")
        else:
            st.info(f"{len(matches)} players found. Please refine your search or select:")
            player = st.selectbox("Select a player:", np.sort(matches))
else:
    st.info("Enter a player name to begin.")
            
        
if player is not None:

    player_stats = df_players[df_players['player'] == player].sort_values('season')
        
    # Aggregate stats by season (combine multiple teams in same year)
    numeric_cols_to_sum = [col for col in player_stats.columns if player_stats[col].dtype != 'O' and col not in ['season', 'player', 'player_id']]
    player_stats = player_stats.groupby('season', as_index=False)[numeric_cols_to_sum].sum()
    
    # --- Metric selection ---
    numeric_cols2 = [col for col in player_stats.columns if player_stats[col].dtype != 'O' and col not in ['season']]
    numeric_cols = [value for key, value in stat_dict.items() if key in numeric_cols2]
    metrics2 = st.multiselect("Select metrics to display (bar chart):", numeric_cols, default=numeric_cols[1])
    if metrics2:
        metrics = [key for key, value in stat_dict.items() if value in metrics2]
        fig = create_metric_subplots(player_stats, metrics2, metrics, player)
        st.plotly_chart(fig, width='stretch')
    # --- Stats table with sum and per-game avg ---
    table = player_stats.set_index('season')[metrics]
    sum_row = pd.DataFrame([table.sum()], index=['Total'])
    games_played = player_stats['g'].sum()
    if games_played > 1:
        avg_row = pd.DataFrame([table.sum() / games_played], index=['Per Game Avg'])
        table = pd.concat([table, sum_row, avg_row])
        table.rename_axis(index='Season', inplace=True)
        table.rename(columns={m: stat_dict.get(m, m) for m in metrics}, inplace=True)
    else:
        table = pd.concat([table, sum_row])
        table.rename_axis(index='Season', inplace=True)
        table.rename(columns={m: stat_dict.get(m, m) for m in metrics}, inplace=True)
    # Style the summary rows
    def highlight_summary(row):
        if row.name in ['Total', 'Per Game Avg']:
            return ['background-color: #4CAF50; color: white; font-weight: bold'] * len(row)
        return [''] * len(row)
    st.dataframe(table.style.apply(highlight_summary, axis=1))

