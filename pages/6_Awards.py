import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from utils.data_loader import load_awards_data, load_nba_stat_definitions

st.title("Player Awards & Honors")

df_awards = load_awards_data()
stat_dict = load_nba_stat_definitions()

# --- Award search ---
award_options = df_awards['award'].unique()
award_options = [award for award in award_options if "nba" in award]
award_options2 = [stat_dict.get(award, award) for award in award_options]
selected_award2 = st.selectbox("Select an award to explore:", award_options2) 
selected_award = award_options[award_options2.index(selected_award2)]

years = sorted(df_awards['season'].unique(), reverse=True)
year = st.selectbox("Select a year:", years)

if selected_award and year:
    award_data = df_awards[(df_awards['award'] == selected_award) & (df_awards['season'] == year)]
    if len(award_data) == 0:
        st.warning(f"No data found for {selected_award2} in {year}.")
    else:
        st.success(f"Found {len(award_data)} recipients for {selected_award2} in {year}.")
        fig = go.Figure(data=[go.Bar(x=award_data['player'], y=award_data['share'], marker_color='gold')])
        fig.update_layout(title=f"{selected_award2} Recipients in {year}", xaxis_title="Player", yaxis_title="Award Share", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
if selected_award == "nba mvp":
    st.subheader(f"**{selected_award2} definition**")
    st.markdown("""
    The NBA Most Valuable Player (MVP) award is given annually to the player deemed the most valuable in the regular season. 
    The award is voted on by a panel of sportswriters and broadcasters, and the player with the highest point total wins. 
    The MVP is often considered the most prestigious individual award in the NBA, recognizing outstanding performance, leadership, and impact on their team's success throughout the season.
    """)
elif selected_award == "nba dpoy":
    st.subheader(f"**{selected_award2} definition**")
    st.markdown("""
    The NBA Defensive Player of the Year (DPOY) award is given annually to the player who is considered the best defensive player in the regular season. The award is voted on by a panel of sportswriters and broadcasters, and the player with the highest point total wins. The DPOY recognizes players who excel in defensive skills such as shot-blocking, stealing, and overall defensive presence on the court.
    """)
elif selected_award == "nba roy":
    st.subheader(f"**{selected_award2} definition**")
    st.markdown("""
    The NBA Rookie of the Year (ROY) award is given annually to the most outstanding rookie player in the regular season. The award is voted on by a panel of sportswriters and broadcasters, and the player with the highest point total wins. The ROY recognizes the best first-year player who has made a significant impact on their team and the league during their debut season.
    """)
elif selected_award == "nba mip":
    st.subheader(f"**{selected_award2} definition**")
    st.markdown("""
    The NBA Most Improved Player (MIP) award is given annually to the player who has shown the most significant improvement in their performance from the previous season. The award is voted on by a panel of sportswriters and broadcasters, and the player with the highest point total wins. The MIP recognizes players who have made substantial strides in their skills, statistics, and overall impact on their team.
    """)
elif selected_award == "nba smoy":
    st.subheader(f"**{selected_award2} definition**")
    st.markdown("""
    The NBA Sixth Man of the Year (SMOY) award is given annually to the best player who comes off the bench as a substitute during the regular season. The award is voted on by a panel of sportswriters and broadcasters, and the player with the highest point total wins. The SMOY recognizes players who provide significant contributions to their team in a reserve role, often changing the momentum of games and providing valuable scoring, defense, or playmaking.
    """)
elif selected_award == "nba clutch_poy":
    st.subheader(f"**{selected_award2} definition**")
    st.markdown("""
    The NBA Clutch Player of the Year (Clutch POY) award is given annually to the player who performs exceptionally well in high-pressure situations, such as close games in the final minutes or overtime. The award is voted on by a panel of sportswriters and broadcasters, and the player with the highest point total wins. The Clutch POY recognizes players who consistently deliver game-winning plays, crucial baskets, or defensive stops when it matters most.
    """)
    
df_winners = df_awards[df_awards["winner"] == True].groupby(["player", "award"]).size().reset_index(name="wins")
df_winners["award"] = df_winners["award"].apply(lambda x: stat_dict.get(x, x))
df_winners = df_winners.sort_values("wins", ascending=False).reset_index(drop=True)
st.subheader("Top Award Winners")
st.dataframe(df_winners, hide_index=True)