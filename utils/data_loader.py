import os
import pandas as pd
import streamlit as st

# Paths to data
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
CACHE_DIR = os.path.join(os.path.dirname(__file__), '../cache')

PLAYER_TOTALS = os.path.join(DATA_DIR, 'Player Totals.csv')
TEAM_TOTALS = os.path.join(DATA_DIR, 'Team Totals.csv')
DRAFT_HISTORY = os.path.join(DATA_DIR, 'Draft Pick History.csv')
ALL_STAR = os.path.join(DATA_DIR, 'All-Star Selections.csv')
STAT_DICT = os.path.join(DATA_DIR, 'nba_stat_dict.npy')
UNIV_RANK = os.path.join(DATA_DIR, 'University Rankings.csv')
UNIV_RANGE = os.path.join(DATA_DIR, 'University Rankings by Range.csv')
NBA_STAT_DEF = os.path.join(DATA_DIR, 'nba_stat_definitions.csv')
AWARDS = os.path.join(DATA_DIR, 'Player Award Shares.csv')
SALARIES = os.path.join(DATA_DIR, 'players_salary_updated2.csv')
TEAM_SALARY = os.path.join(DATA_DIR, 'team_salaries.csv')

@st.cache_data(show_spinner=False)
def load_all_data():
    df_players = pd.read_csv(PLAYER_TOTALS)
    df_teams = pd.read_csv(TEAM_TOTALS)
    df_draft = pd.read_csv(DRAFT_HISTORY)
    df_all_star = pd.read_csv(ALL_STAR)
    return df_players, df_teams, df_draft, df_all_star

@st.cache_data(show_spinner=False)
def load_university_rankings():
    df_rankings = pd.read_csv(UNIV_RANK, index_col=0)
    df_range = pd.read_csv(UNIV_RANGE, index_col=0)
    return df_rankings, df_range

@st.cache_data(show_spinner=False)
def load_nba_stat_definitions():
    df_nbsa_stat_def = pd.read_csv(NBA_STAT_DEF, index_col=0)
    nba_deff_dict = df_nbsa_stat_def[["abbreviation", "Description"]].set_index("abbreviation").to_dict()["Description"]
    return nba_deff_dict

@st.cache_data(show_spinner=False)
def load_awards_data():
    df_awards = pd.read_csv(AWARDS)
    return df_awards

@st.cache_data(show_spinner=False)
def load_team_salaries():
    df_salaries = pd.read_csv(SALARIES)
    df_team_salaries = pd.read_csv(TEAM_SALARY)
    return df_salaries, df_team_salaries