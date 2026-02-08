import streamlit as st
from utils.data_loader import load_all_data, load_stat_dict

st.title("Team Statistics")

_, df_teams, _, _ = load_all_data()
stat_dict = load_stat_dict()

teams = df_teams['team'].unique()
years = sorted(df_teams['season'].unique())

team = st.selectbox("Select a team:", teams)
year_range = st.slider("Select year range:", min_value=int(min(years)), max_value=int(max(years)), value=(int(min(years)), int(max(years))))

filtered = df_teams[(df_teams['team'] == team) & (df_teams['season'] >= year_range[0]) & (df_teams['season'] <= year_range[1])].reset_index(drop=True)

if not filtered.empty:
    st.dataframe(filtered, hide_index=True)
else:
    st.warning("No data for this team and year range.")

st.markdown("### Column Definitions")
for col in filtered.columns:
    desc = stat_dict.get(col, "No description available.")
    st.write(f"**{col}**: {desc}")
