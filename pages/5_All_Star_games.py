import streamlit as st
from plotly.subplots import make_subplots
import pandas as pd
import random
from utils.data_loader import load_all_data, load_stat_dict

st.title("All Star Games Selection")

_, _, _, df_all_star = load_all_data()  # Load the All Star Games data
stat_dict = load_stat_dict()

#Year selection
years = sorted(df_all_star['season'].unique(), reverse=True)
year = st.selectbox("Select a year:", years)

east = df_all_star[df_all_star['season'] == year][df_all_star['team'] == 'East'].reset_index(drop=True)   
west = df_all_star[df_all_star['season'] == year][df_all_star['team'] == 'West'].reset_index(drop=True)

east_all = df_all_star[df_all_star['team'] == 'East']["full_team_name"].reset_index(drop=True)   
west_all = df_all_star[df_all_star['team'] == 'West']["full_team_name"].reset_index(drop=True)

table_data = pd.concat([east[["player", "full_team_name"]], west[["player", "full_team_name"]]], axis=1, ignore_index=True)
table_data.columns = ['Eastern conference players', 'Original Team 1', 'Western conference players', 'Original Team 2']
st.markdown(f"### All Star Game Players - {year} Season")
st.table(table_data)    

teams_count_east = east_all.value_counts()[:20] # Get the top 20 teams by All Star selections in the East
teams_count_west = west_all.value_counts()[:20] # Get the top 20 teams by All Star selections in the West

#graph_east = px.bar(x=teams_count_east.index, y=teams_count_east.values, labels={'x': 'Team', 'y': 'Number of Selections'}, title='East All Star Selections by Team')   
#graph_west = px.bar(x=teams_count_west.index, y=teams_count_west.values, labels={'x': 'Team', 'y': 'Number of Selections'}, title='West All Star Selections by Team')
fig = make_subplots(rows=1, cols=2, subplot_titles=["East All Star Selections by Team", "West All Star Selections by Team"])
fig.add_trace(go.Bar(x=teams_count_east.index, y=teams_count_east.values, name='East'), row=1, col=1)
fig.add_trace(go.Bar(x=teams_count_west.index, y=teams_count_west.values, name='West'), row=1, col=2)
fig.update_layout(height=500, showlegend=False)
st.plotly_chart(fig, width='stretch')  