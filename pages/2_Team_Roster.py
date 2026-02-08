import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import random
from utils.data_loader import load_all_data, load_stat_dict

st.title("Team Roster Statistics")

df_players, _, _, _ = load_all_data()
stat_dict = load_stat_dict()

def create_roster_metric_subplots(roster_stats, metrics2, metrics, player_names):
    """Create subplots for each metric selected with players on X axis"""
    list_colors = ['steelblue', 'indianred', 'seagreen', 'mediumpurple', 'darkorange', 'teal', 'crimson', 'navy', 'darkcyan', 'goldenrod', 'slateblue', 'coral']
    
    fig = make_subplots(
        rows=len(metrics),
        cols=1,
        subplot_titles=metrics2,
        #vertical_spacing=0.005 * len(metrics)  # Adjust spacing based on number of metrics
    )
    
    for i, metric in enumerate(metrics, 1):
        fig.add_trace(
            go.Bar(
                x=player_names,
                y=roster_stats[metric],
                name=metric,
                marker=dict(color=random.choice(list_colors))
            ),
            row=i,
            col=1
        )
    
    fig.update_xaxes(title_text="Players", row=len(metrics), col=1)
    fig.update_yaxes(title_text="Value", col=1)
    fig.update_layout(height=400 * len(metrics), title_text="Team Roster - Statistics by Metric", showlegend=False)
    
    return fig

# --- Team and Year selection ---
teams = df_players['full_team_name'].unique()
team = st.selectbox("Select a team:", teams)

years = sorted(df_players[df_players['full_team_name'] == team]['season'].unique(), reverse=True)
year = st.selectbox("Select a year:", years)

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