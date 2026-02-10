import streamlit as st
from streamlit_extras.let_it_rain import rain
from utils.data_loader import load_all_data, load_university_rankings

st.set_page_config(page_title="NBA Stats Explorer", layout="wide")
st.title("NBA Stats Explorer")

# Load all data once and cache
df_players, df_teams, df_draft, df_all_star = load_all_data()

#load university rankings (cached)
top_univ, univ_by_range = load_university_rankings()

rain(
    emoji="🏀",
    font_size=54,
    falling_speed=5,
    animation_length="infinite"
)

st.markdown("""
Welcome to the NBA Stats Explorer! Use the sidebar to navigate between pages:

- **Intro**: Learn about the app and its features
- **Player Search**: Find and analyze player stats
- **Team Stats**: Explore team statistics by year
- **Draft Analytics**: Discover draft pick trends and university rankings
- **All Star Games**: View All Star Game selections by year
""")
