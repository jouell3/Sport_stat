import streamlit as st
from utils.data_loader import load_all_data, load_stat_dict, load_university_rankings, compute_university_rankings, save_university_rankings

st.set_page_config(page_title="NBA Stats Explorer", layout="wide")
st.title("NBA Stats Explorer")

# Load all data once and cache
df_players, df_teams, df_draft, df_all_star = load_all_data()
stat_dict = load_stat_dict()

# University rankings pickle (compute and save if not present)
top_univ, univ_by_range = load_university_rankings()
if top_univ is None or univ_by_range is None:
    top_univ, univ_by_range = compute_university_rankings(df_draft)
    save_university_rankings(top_univ, univ_by_range)

st.markdown("""
Welcome to the NBA Stats Explorer! Use the sidebar to navigate between pages:

- **Intro**: Learn about the app and its features
- **Player Search**: Find and analyze player stats
- **Team Stats**: Explore team statistics by year
- **Draft Analytics**: Discover draft pick trends and university rankings
- **All Star Games**: View All Star Game selections by year
""")
