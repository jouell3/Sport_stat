import os
import pandas as pd
import numpy as np
import pickle
import streamlit as st

# Paths to data
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
CACHE_DIR = os.path.join(os.path.dirname(__file__), '../cache')

PLAYER_TOTALS = os.path.join(DATA_DIR, 'Player Totals.csv')
TEAM_TOTALS = os.path.join(DATA_DIR, 'Team Totals.csv')
DRAFT_HISTORY = os.path.join(DATA_DIR, 'Draft Pick History.csv')
ALL_STAR = os.path.join(DATA_DIR, 'All-Star Selections.csv')
STAT_DICT = os.path.join(DATA_DIR, 'nba_stat_dict.npy')
UNIV_RANK_PICKLE = os.path.join(CACHE_DIR, 'university_rankings.pkl')

@st.cache_data(show_spinner=False)
def load_all_data():
    df_players = pd.read_csv(PLAYER_TOTALS)
    df_teams = pd.read_csv(TEAM_TOTALS)
    df_draft = pd.read_csv(DRAFT_HISTORY)
    df_all_star = pd.read_csv(ALL_STAR)
    return df_players, df_teams, df_draft, df_all_star

@st.cache_data(show_spinner=False)
def load_stat_dict():
    # Loads the column definitions from the .npy file
    return np.load(STAT_DICT, allow_pickle=True).item()

@st.cache_data(show_spinner=False)
def compute_university_rankings(df_draft):
    # Top 10 universities by total picks
    top_univ = df_draft['college'].value_counts().sort_values(ascending=False)
    # Picks by rank range (1-5, 6-10, ...)
    bins = list(range(1, 61, 5))
    labels = [f"{i}-{i+4}" for i in bins]
    df_draft = df_draft.copy()
    df_draft['rank_range'] = pd.cut(df_draft['overall_pick'], bins=bins+[np.inf], labels=labels, right=False)
    univ_by_range = df_draft.groupby(['college', 'rank_range']).size().unstack(fill_value=0)
    return top_univ, univ_by_range

def save_university_rankings(top_univ, univ_by_range):
    with open(UNIV_RANK_PICKLE, 'wb') as f:
        pickle.dump({'top_univ': top_univ, 'univ_by_range': univ_by_range}, f)

def load_university_rankings():
    if os.path.exists(UNIV_RANK_PICKLE):
        with open(UNIV_RANK_PICKLE, 'rb') as f:
            data = pickle.load(f)
        return data['top_univ'], data['univ_by_range']
    return None, None
