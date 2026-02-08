import random
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from utils.data_loader import load_all_data, load_nba_stat_definitions

st.title("Player Search & Statistics")

df_players, _, _, _ = load_all_data()
stat_dict = load_nba_stat_definitions()

def create_metric_subplots(player_stats, metrics2, metrics, player_name):
    """Create subplots for each metric selected"""
    list_colors=['steelblue', 'indianred', 'seagreen', 'mediumpurple', 'darkorange', 'teal', 'crimson', 'navy', 'darkcyan', 'goldenrod', 'slateblue', 'coral']
    
    fig = make_subplots(
        rows=int(len(metrics)/2) + len(metrics)%2,
        cols=2,
        subplot_titles=metrics2,
        #vertical_spacing=0.05,
    )
    j =1
    k = 0
    for i, metric in enumerate(metrics, 1):
        if i% 2 == 1:
            k += 1
            j = 1
        else:
            j = 2   
        
        fig.add_trace(
            go.Bar(
                x=player_stats['season'],
                y=player_stats[metric],
                name=metric,
                marker=dict(color=random.choice(list_colors))
            ),
            row=k,
            col=j
        )
    
    fig.update_xaxes(title_text="Season")
    fig.update_yaxes(title_text="Value", col=1)
    fig.update_layout(height=400 * (int(len(metrics)/2) + len(metrics)%2), title_text=f"{player_name} - Statistics by Metric", showlegend=False)
    
    return fig

# --- Player search ---
search = st.text_input("Enter player name (partial match, case-insensitive):")
if search:
    list_players = df_players['player'].unique()
    matches = list_players[pd.Series(list_players).str.contains(search, case=False, na=False)]
    #matches = df_players[df_players['player'].str.contains(search, case=False, na=False)].unique()
    if len(matches) == 0:
        st.warning("No players found. Please refine your search.")
    elif len(matches) == 1:
        player = matches.iloc[0]['player']
        st.success(f"Found: {player}")
        player_stats = df_players[df_players['player'] == player].sort_values('season')
        # --- Metric selection ---
        numeric_cols = [col for col in player_stats.columns if player_stats[col].dtype != 'O' and col not in ['season']]
        metrics2 = st.multiselect("Select metrics to display (bar chart):", numeric_cols, default=numeric_cols[1])
        if metrics2:
            metrics = [key for key, value in stat_dict.items() if value in metrics2]
            fig = create_metric_subplots(player_stats, metrics2, metrics, player)
            st.plotly_chart(fig, width='stretch')
        # --- Stats table with sum and per-game avg ---
        table = player_stats.set_index('season')[metrics]
        sum_row = pd.DataFrame([table.sum()], index=['Total'])
        games_played = player_stats['g'].sum()
        if games_played:
            avg_row = pd.DataFrame([table.sum() / games_played], index=['Per Game Avg'])
            table = pd.concat([table, sum_row, avg_row])
        else:
            table = pd.concat([table, sum_row])
        # Style the summary rows
        def highlight_summary(row):
            if row.name in ['Total', 'Per Game Avg']:
                return ['background-color: #4CAF50; color: white; font-weight: bold'] * len(row)
            return [''] * len(row)
        st.dataframe(table.style.apply(highlight_summary, axis=1))
        # --- Column definitions ---

    else:
        st.info(f"{len(matches)} players found. Please refine your search or select:")
        player = st.selectbox("Select a player:", matches)
        if player:
            player_stats = df_players[df_players['player'] == player].sort_values('season')
            numeric_cols2 = [col for col in player_stats.columns if player_stats[col].dtype != 'O' and col not in ['season']]
            numeric_cols = [value for key, value in stat_dict.items() if key in numeric_cols2]
            metrics2 = st.multiselect("Select metrics to display (bar chart):", numeric_cols, default=numeric_cols[1])
            if metrics2:
                metrics = [key for key, value in stat_dict.items() if value in metrics2]
                fig = create_metric_subplots(player_stats, metrics2, metrics, player)
                st.plotly_chart(fig, width='stretch')
            table = player_stats.set_index('season')[metrics]
            sum_row = pd.DataFrame([table.sum()], index=['Total'])
            games_played = player_stats['g'].sum() if 'g' in player_stats.columns else None
            if games_played:
                avg_row = pd.DataFrame([table.sum() / games_played], index=['Per Game Avg'])
                table = pd.concat([table, sum_row, avg_row])
                table.rename_axis(index='Season', inplace=True)
                table.rename(columns={m: stat_dict.get(m, m) for m in metrics}, inplace=True)
            else:
                table = pd.concat([table, sum_row])
                table.rename_axis(index='Season', inplace=True)
                table.rename(columns={m: stat_dict.get(m, m) for m in metrics}, inplace=True)
            # Style the summary rows
            def highlight_summary(row):
                if row.name in ['Total', 'Per Game Avg']:
                    return ['background-color: lightgreen; color: black; font-weight: bold'] * len(row)
                return [''] * len(row)
            st.dataframe(table.style.apply(highlight_summary, axis=1))

else:
    st.info("Enter a player name to begin.")
