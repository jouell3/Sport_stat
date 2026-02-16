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
- **Team Roster**: Explore team rosters and player stats by season
- **Team Stats**: Explore team statistics by year
- **Draft Analytics**: Discover draft pick trends and university rankings
- **All Star Games**: View All Star Game selections by year
- **Player Awards**: Analyze player awards over time
- **Player Salaries**: Explore salary trends for individual players and teams
- **Regular season Games by Team**: Analyze regular season performance for selected teams
- **Playoff Games by Team**: Explore playoff performance for selected teams
- **Playoff Games by Round**: Analyze playoff performance by round and team
""")




st.markdown("<br>"*5, unsafe_allow_html=True)

st.markdown("""
**First release** of this application occurred on Sunday, February 8th, 2026. The app is built using Streamlit and Plotly, 
and all data is sourced from Basketball Reference (https://www.basketball-reference.com/) as well as Kaggle 
(https://www.kaggle.com/datasets/sumitrodatta/nba-aba-baa-stats).
""")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("**Version 1.0.0** - Initial release with player search, team stats, draft analytics, and All Star Game selections.")

st.markdown("**Version 1.1.0** - Added salary analysis for teams and players, including total salary trends and comparisons across seasons.") 
st.markdown("**Version 1.2.0** - Introduced regular season game analysis by team, allowing users to explore performance trends and key statistics for selected teams across different seasons.")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("This app is a work in progress, and I plan to add more features and data visualizations in the future. If you have any suggestions or feedback, please feel free to reach out to me. Enjoy exploring the world of NBA stats!")