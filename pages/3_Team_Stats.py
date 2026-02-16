import random
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_loader import load_all_data, load_nba_stat_definitions
from utils.figure_constructor import create_metric_subplots

st.title("Team Statistics")

_, df_teams, _, _ = load_all_data()
stat_dict = load_nba_stat_definitions()



teams = df_teams['team'].unique()
years = sorted(df_teams['season'].unique())

st.markdown(f"##### Use the dropdowns below to select a team, year range, and metrics to visualize. The data will update accordingly.")
team = st.selectbox("Select a team:", teams, label_visibility="collapsed")
year_range = st.slider("Select year range:", min_value=int(min(years)), max_value=int(max(years)), value=(int(min(years)), int(max(years))), step=1, label_visibility="collapsed")

    # --- Metric selection ---
numeric_cols2 = [col for col in df_teams.columns if df_teams[col].dtype != 'O' and col not in ['season', 'full_team_name']]
numeric_cols = [value for key, value in stat_dict.items() if key in numeric_cols2]
st.markdown(f"##### Select the metrics you want to display in the plot. You can choose multiple metrics to compare them side by side.")
metrics2 = st.multiselect("Select metrics to display:", numeric_cols, default=numeric_cols[1], label_visibility="collapsed")

metrics = [key for key, value in stat_dict.items() if value in metrics2]

if metrics:
    
    metrics3 = [key for key, value in stat_dict.items() if value in metrics2]
    
    filtered = df_teams[(df_teams['team'] == team) & (df_teams['season'] >= year_range[0]) & (df_teams['season'] <= year_range[1])].reset_index(drop=True)

    fig = create_metric_subplots(filtered, metrics2, metrics, team)
    st.plotly_chart(fig, width='stretch')


if not filtered.empty:
    st.dataframe(filtered[['season', 'team'] + metrics], hide_index=True)
else:
    st.warning("No data for this team and year range.")