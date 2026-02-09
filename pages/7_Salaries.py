import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from utils.data_loader import load_team_salaries

df_salaries, df_team_salaries = load_team_salaries()

