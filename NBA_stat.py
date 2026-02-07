import streamlit as st
<<<<<<< HEAD
<<<<<<< HEAD
from utils.data_loader import load_all_data, load_stat_dict, load_university_rankings, compute_university_rankings, save_university_rankings

st.set_page_config(page_title="NBA Stats Explorer", layout="wide")
st.title("NBA Stats Explorer")

# Load all data once and cache
df_players, df_teams, df_draft = load_all_data()
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
""")
=======
import pandas as pd
import numpy as np
import plotly.express as px 
=======
from utils.data_loader import load_all_data, load_stat_dict, load_university_rankings, compute_university_rankings, save_university_rankings
>>>>>>> a79b580 (Frist commit NBA stat app)

st.set_page_config(page_title="NBA Stats Explorer", layout="wide")
st.title("NBA Stats Explorer")

# Load all data once and cache
df_players, df_teams, df_draft = load_all_data()
stat_dict = load_stat_dict()

# University rankings pickle (compute and save if not present)
top_univ, univ_by_range = load_university_rankings()
if top_univ is None or univ_by_range is None:
    top_univ, univ_by_range = compute_university_rankings(df_draft)
    save_university_rankings(top_univ, univ_by_range)

st.markdown("""
Welcome to the NBA Stats Explorer! Use the sidebar to navigate between pages:

<<<<<<< HEAD
st.title("Everything you want to know on NBA players")

df_players

df_players_mike = df_players_jordan = df_players[(df_players["player"] == "Michael Jordan")]

df_players_mike
>>>>>>> aacd865 (first draft of teh app)
=======
- **Intro**: Learn about the app and its features
- **Player Search**: Find and analyze player stats
- **Team Stats**: Explore team statistics by year
- **Draft Analytics**: Discover draft pick trends and university rankings
""")
>>>>>>> a79b580 (Frist commit NBA stat app)
