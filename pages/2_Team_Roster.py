import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import random
from utils.data_loader import load_all_data, load_nba_stat_definitions
from utils.figure_constructor import create_roster_metric_subplots

st.title("Team Roster Statistics")

df_players, _, _, _ = load_all_data()
stat_dict = load_nba_stat_definitions()

# --- Team and Year selection ---
teams = df_players['full_team_name'].unique()
st.markdown("### Select a team and a year to view roster statistics:")
team = st.selectbox("Select a team:", teams, label_visibility="collapsed")

years = sorted(df_players[df_players['full_team_name'] == team]['season'].unique(), reverse=True)
year = st.selectbox("Select a year:", years, label_visibility="collapsed")

# Filter players for the selected team and year
roster = df_players[(df_players['full_team_name'] == team) & (df_players['season'] == year)].sort_values(by="player", key=lambda x: x.str.split().str[-1])  # Sort by last name
if len(roster) == 0:
    st.warning(f"No players found for {team} in {year}.")
else:
    st.success(f"Found {len(roster)} players for {team} in {year}.")
    
    # --- Metric selection ---
    numeric_cols2 = [col for col in roster.columns if roster[col].dtype != 'O' and col not in ['season', 'full_team_name']]
    numeric_cols = [value for key, value in stat_dict.items() if key in numeric_cols2]
    metrics2 = st.multiselect("Select metrics to display:", numeric_cols, default=numeric_cols[1])
    
    if metrics2:
        metrics = [key for key, value in stat_dict.items() if value in metrics2]
        player_names = roster['player'].values
        roster_stats = roster[metrics]
        
        fig = create_roster_metric_subplots(roster_stats, metrics2, metrics, player_names)
        st.plotly_chart(fig, width='stretch')
    
    # --- Stats table ---
    st.markdown("### Roster Statistics Table")
    display_columns = ['player'] + metrics
    table = roster[display_columns].set_index('player')
    table = table.rename(columns={m: stat_dict.get(m, m) for m in metrics})
    
    def highlight_summary(row):
        return [''] * len(row)
    
    st.dataframe(table.style.apply(highlight_summary, axis=1))