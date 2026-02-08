import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import load_all_data, load_stat_dict, load_university_rankings
import pandas as pd

st.title("Draft Analytics & University Rankings")

_, _, df_draft, _ = load_all_data()
stat_dict = load_stat_dict()
top_univ, univ_by_range = load_university_rankings()

# Bar chart: Top 10 universities by total picks
num_univ = st.slider("Select number of top universities to display:", min_value=5, max_value=30, value=10)
years = st.slider("Select draft year range:", min_value=int(df_draft['season'].min()), max_value=int(df_draft['season'].max()), value=(int(df_draft['season'].min()), int(df_draft['season'].max())))

st.markdown(f"#### Top {num_univ} Universities by Total Draft Picks")
if top_univ is not None:
    filtered_draft = df_draft[(df_draft['season'] >= years[0]) & (df_draft['season'] <= years[1])]
    top_univ = filtered_draft['college'].value_counts().sort_values(ascending=False).head(num_univ)
    fig = px.bar(top_univ, x=top_univ.index, y=top_univ.values, labels={'x': 'University', 'y': 'Total Picks'}, title=f"Top {num_univ} Universities by Draft Picks")
    st.plotly_chart(fig, width='stretch')
else:
    st.warning("University ranking data not available.")

# Table: Universities by pick rank range
st.markdown("#### University Picks by Rank Range")
if univ_by_range is not None:
    univ_by_range["Total Picks"] = univ_by_range.sum(axis=1)
    univ_by_range = univ_by_range.sort_values("Total Picks", ascending=False)
    st.dataframe(univ_by_range)
    csv = univ_by_range.to_csv().encode('utf-8')
    st.download_button("Download Table as CSV", csv, "university_picks_by_rank_range.csv", "text/csv")
else:
    st.warning("University pick range data not available.")

# Year and round selection for draft 
st.markdown("#### Explore Draft Picks by Year and Round")
years = sorted(df_draft['season'].unique(), reverse=True)
rounds = sorted(df_draft['round'].dropna().unique())

year = st.selectbox("Select draft year:", years)
draft_round = st.selectbox("Select draft round:", rounds)

filtered = df_draft[(df_draft['season'] == year) & (df_draft['round'] == draft_round)].reset_index(drop=True)
if not filtered.empty:
    filtered_2 = filtered[['overall_pick', 'player', 'college']].rename(columns={'overall_pick': 'Overall Pick', 'player': 'Player', 'college': 'College'}).reset_index(drop=True)
    st.dataframe(filtered_2.reset_index(drop=True))
else:
    st.warning("No draft data for this year and round.")

st.markdown("### Column Definitions")
for col in df_draft.columns:
    desc = stat_dict.get(col, "No description available.")
    st.write(f"**{col}**: {desc}")
