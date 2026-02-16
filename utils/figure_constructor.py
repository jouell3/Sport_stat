import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_loader import load_nba_stat_definitions, load_team_id_name_dict
import random

stat_dict = load_nba_stat_definitions()
dict_teamID = load_team_id_name_dict()

home_label_colors = {
    "West - First Round": "#56B4E9",
    "East - First Round": "#009E73",
    "East - Conf. Semifinals": "#F0E442",
    "West - Conf. Semifinals": "#E69F00",
    "East - Conf. Finals": "#CC79A7",
    "West - Conf. Finals": "#0072B2",
    "NBA Finals": "#D55E00"
}

away_label_colors = {
    "West - First Round": "#BDE9FF",
    "East - First Round": "#66E0B3",
    "East - Conf. Semifinals": "#FFF3A1",
    "West - Conf. Semifinals": "#FFC97A",
    "East - Conf. Finals": "#F2B6D9",
    "West - Conf. Finals": "#66B6FF",
    "NBA Finals": "#FF9A7A",
} 
default_color = "#D5F49C" 

def final_figure(games_final, team_final, team_final_names):
    
    game_final_team1_score = [games_final.loc[row, 'homeScore'] if games_final.loc[row, 'hometeamId'] == team_final[0] else games_final.loc[row, 'awayScore'] for row in games_final.index]
    
    games_final['score_team1'] = game_final_team1_score
    
    game_final_team2_score = [games_final.loc[row, 'homeScore'] if games_final.loc[row, 'hometeamId'] == team_final[1] else games_final.loc[row, 'awayScore'] for row in games_final.index]
    games_final['score_team2'] = game_final_team2_score
    
    fig = make_subplots(rows=1, cols=1, 
                        subplot_titles=[f"{team_final_names[0]} vs {team_final_names[1]} in the NBA Finals of the {selected_year} season"],  
                        specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(x=games_final["gameDateTimeEst"].str.split(" ").str[0], y=games_final['score_team1'], name=f'{team_final_names[0]}', legend="legend",
               marker=dict(color="#56B4E9")),
        row=1, col=1, secondary_y=False)
    fig.add_trace(
        go.Bar(x=games_final["gameDateTimeEst"].str.split(" ").str[0], y=games_final['score_team2'], name=f'{team_final_names[1]}', legend="legend",
               marker=dict(color="#FF9A7A")),
        row=1, col=1, secondary_y=False)

    fig.add_trace(
        go.Scatter(x=games_final["gameDateTimeEst"].str.split(" ").str[0], y=games_final['score_team1'] - games_final['score_team2'], name='Game Score Difference', legend="legend",
               mode='lines+markers', line=dict(color='red', width=2)),
        row=1, col=1, secondary_y=True)

    fig.update_layout(
        height=600,
        width=800,
        barmode="group",
        title_text="Number of points scored in each games in the NBA Finals",
        title_font_size=28,
        legend=dict(x=0.99, y=1, xanchor="right", yanchor="top"))
    fig.update_xaxes(title_font=dict(size=28, family='Gravitas One', color='deepskyblue'), 
                     title_text="Date", row=1, col=1)

    fig.update_yaxes(title_font=dict(size=22, family='Gravitas One', color='deepskyblue'),
                     title_text="Number of points", range=(70, 150), row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_font=dict(size=22, family='Gravitas One', color='deepskyblue'),
                     title_text="Difference in Points", range=(-60, 60), secondary_y=True, row=1, col=1)
    
    # Add a horizontal line at y=110 for reference
    fig.add_hline(y=110, line_color="green", line_dash="dash", row=1, col=1)

    return fig

def label_color_home(series):
    return series.map(home_label_colors).fillna(default_color)

def label_color_away(series):
    return series.map(away_label_colors).fillna(default_color)

def create_roster_metric_subplots(roster_stats, metrics2, metrics, player_names):   #figure for page 2 - team roster
    """Create subplots for each metric selected with players on X axis"""
    list_colors = ['steelblue', 'indianred', 'seagreen', 'mediumpurple', 'darkorange', 'teal', 'crimson', 'navy', 'darkcyan', 'goldenrod', 'slateblue', 'coral']
    
    fig = make_subplots(
        rows=len(metrics),
        cols=1,
        subplot_titles=metrics2,
        #vertical_spacing=0.005 * len(metrics)  # Adjust spacing based on number of metrics
    )
    
    for i, metric in enumerate(metrics, 1):
        fig.add_trace(
            go.Bar(
                x=player_names,
                y=roster_stats[metric],
                name=metric,
                marker=dict(color=random.choice(list_colors))
            ),
            row=i,
            col=1
        )
    
    fig.update_xaxes(title_text="Players", 
                     title_font=dict(size=18, family='Gravitas One', color='palegreen'),
                        tickfont=dict(size=12, color='white'), tickangle=-45,
                     row=len(metrics), col=1)
    fig.update_yaxes(title_text="Value", col=1)
    fig.update_layout(height=500 * len(metrics), title_text="Team Roster - Statistics by Metric", 
                      title_font=dict(size=24, family='Gravitas One', color='white'), showlegend=False)
    fig.update_annotations(font=dict(size=22, color="lightblue", family='Gravitas One'))
    
    return fig

def figure_playoff(games_team_year, wins_losses_by_year, team):  
    
    selected_games = games_team_year[(games_team_year["seriesGameNumber"] == 1)]
    opponents = []
    for index, row in selected_games.iterrows():
        opponent_id = row['awayteamId']
        opponent_name = dict_teamID.get(opponent_id, "Unknown")
        opponents.append(opponent_name)
    
    fig = make_subplots(rows=2, cols=1, 
                        subplot_titles=[f"Playoff games for the {team}", f"Wins vs Losses per season in the playoff for the {team}"], 
                        vertical_spacing=0.18, 
                        specs=[[{"secondary_y": True}], [{"secondary_y": True}],])

    fig.add_trace(go.Bar(x=games_team_year.index, y=games_team_year['selected_team_score'], name=f'{team}', legend="legend",
                marker=dict(color=label_color_home(games_team_year["gameLabel"]))),
                row=1, col=1, secondary_y=False)
    
    fig.add_trace(go.Bar(x=games_team_year.index, y=games_team_year['opponent_score'], name='Opponent team', legend="legend",
                marker=dict(color=label_color_away(games_team_year["gameLabel"]))),
                row=1, col=1, secondary_y=False)

    fig.add_trace(go.Scatter(x=games_team_year.index, y=games_team_year['selected_team_score']-games_team_year['opponent_score'], name='Home Game Difference', legend="legend",
                mode='lines+markers', line=dict(color='red', width=2)),
                row=1, col=1, secondary_y=True)
    
    fig.update_xaxes(title_text="Date of the game",
                        title_font=dict(size=18, family='Gravitas One', color='palegreen'),
    tickvals=list(range(0, len(games_team_year)+1)),
    ticktext=games_team_year['gameDate'].tolist(),
    tickfont=dict(size=12, color='palegreen'),
    tickangle=-45,
    row=1, col=1)

    
    fig.add_trace(go.Bar(x=wins_losses_by_year["year"], y=wins_losses_by_year["team_win"], 
                         name="Wins", legend="legend3",
                         marker=dict(color='#56B4E9')), row=2, col=1, secondary_y=False)
    fig.add_trace(go.Bar(x=wins_losses_by_year["year"], y=wins_losses_by_year["team_loss"], 
                         name="Losses", legend="legend3",
                         marker=dict(color='#E69F00')), row=2, col=1, secondary_y=False)
    fig.add_trace(
    go.Scatter(x=wins_losses_by_year["year"], y=wins_losses_by_year["delta"], name='Wins-Losses Difference', 
               mode='lines+markers', legend="legend3", line=dict(color='red', width=2)),
    row=2, col=1, secondary_y=True)
    
    fig.update_layout(
        height=1000,
        width=800,
        barmode="group",
        title_text=f"Number of points scored in playoff games for the {team}",
        title_font_size=32,
        margin=dict(t=150, b=80), 
        legend=dict(x=0.92, y=1, xanchor="right", yanchor="top"),
        legend3=dict(x=0.92, y=0.28, xanchor="right", yanchor="bottom"))
    fig.update_xaxes(title_text="Season", row=2, col=1)
    

    fig.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='deepskyblue'),title_text="Number of points", range=(70, 150), row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='lightsalmon'),title_text="Difference in Points", range=(-40, 40), secondary_y=True, row=1, col=1)

    
    fig.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='deepskyblue'),title_text="Number of games", range=(0, 20), row=2, col=1, secondary_y=False)
    fig.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='lightsalmon'),title_text="Difference in Wins-Losses", range=(-10, 30), secondary_y=True, row=2, col=1)
    
    # Add a horizontal line at y=110 for reference
    fig.add_hline(y=110, line_color="green", line_dash="dash", row=1, col=1)

    fig.add_hline(y=5, line_color="green", line_dash="dash", row=2, col=1)
    fig.update_annotations(font=dict(size=26, color="lightblue"))

    return fig

def create_metric_subplots(team_stats, metrics2, metrics, team_name):
    """Create subplots for each metric selected"""
    list_colors=['steelblue', 'indianred', 'seagreen', 'mediumpurple', 'darkorange', 'teal', 'crimson', 'navy', 'darkcyan', 'goldenrod', 'slateblue', 'coral']
    metrics3 = [key for key, value in stat_dict.items() if value in metrics2]
    
    fig = make_subplots(
        rows=int(len(metrics)/2) + len(metrics)%2,
        cols=2,
        subplot_titles=[stat_dict.get(metric, "No description available.") for metric in metrics3]
        #vertical_spacing=0.05,
    )
    j =1
    k = 0
    for i, metric in enumerate(metrics3, 1):
        if i% 2 == 1:
            k += 1
            j = 1
        else:
            j = 2   
        
        fig.add_trace(
            go.Bar(
                x=team_stats['season'],
                y=team_stats[metric],
                name=metric,
                marker=dict(color=random.choice(list_colors))
            ),
            row=k,
            col=j
        )
    
    fig.update_xaxes(title_text="Season", title_font=dict(size=18, family='Gravitas One', color='white'), tickfont=dict(size=12, color='white'), tickangle=-45)
    fig.update_yaxes(title_text="Value", col=1)
    fig.update_layout(height=400 * (int(len(metrics)/2) + len(metrics)%2), 
                      title_text=f"{team_name} - Statistics by Metric", title_font=dict(size=26, family='Gravitas One', color='white'), showlegend=False)
    fig.update_annotations(font=dict(size=18, color="lightblue", family='Gravitas One'))
    
    return fig

def salary_figure(team_salaries, selected_team, search_team):
    
    mean_salaries = team_salaries.groupby('year')['sum_salary'].mean().reset_index()
    median_salaries = team_salaries.groupby('year')['sum_salary'].median().reset_index()
    player_salary = team_salaries[team_salaries['player'] == search_team].sort_values('year')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=team_salaries['year'], y=team_salaries['sum_salary'], mode='markers', name="Salary per player", hovertext=team_salaries['player'], legendgroup="legend"))
    fig.add_trace(go.Scatter(x=mean_salaries['year'], y=mean_salaries['sum_salary'], mode='lines', name=f"{selected_team} - Mean Salary", legendgroup="legend"))
    fig.add_trace(go.Scatter(x=median_salaries['year'], y=median_salaries['sum_salary'], mode='lines', name=f"{selected_team} - Median Salary", legendgroup="legend"))
    fig.add_trace(go.Scatter(x=player_salary['year'], y=player_salary['sum_salary'], mode='lines+markers', name=search_team, legendgroup="legend"))
    fig.update_layout(title=f"{selected_team} - Salary by player for each Season", title_font=dict(size=26), 
                      xaxis_title="Season", 
                      yaxis_title="Total Salary (USD)", 
                      legend=dict(x=0.02, y=0.98, xanchor="left", yanchor="top"),
                      
                      height=500)
    return fig

def regular_season_figure(home_games, away_games, wins_losses_by_year, team2):
    fig = make_subplots(rows=3, cols=1, 
                        subplot_titles=["Home games", "Away games", "Wins vs Losses per season"], 
                        vertical_spacing=0.1, 
                        specs=[[{"secondary_y": True}], [{"secondary_y": True}], [{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(x=home_games.index, y=home_games['homeScore'], name=f'{team2}', legend="legend",
               marker=dict(color='#56B4E9')),
        row=1, col=1, secondary_y=False)
    fig.add_trace(
        go.Bar(x=home_games.index, y=home_games['awayScore'], name='Visitor team', legend="legend",
               marker=dict(color='#E69F00')),
        row=1, col=1, secondary_y=False)
    fig.add_trace(
    go.Scatter(x=home_games.index, y=home_games['delta'], name='Home Game Difference', legend="legend",
               mode='lines+markers', line=dict(color='red', width=2)),
    row=1, col=1, secondary_y=True)
    
    fig.update_xaxes(title_text="Date",
                        title_font=dict(size=18, family='Gravitas One', color='palegreen'), 
                     tickvals=list(range(0, len(home_games)+1)),
    ticktext=home_games['gameDate'].tolist(),
    tickfont=dict(size=12, color='palegreen'),
    tickangle=-45, row=1, col=1)

    fig.add_trace(
        go.Bar(x=away_games.index, y=away_games['awayScore'], name='Home team', legend="legend2",
               marker=dict(color='#E69F00')),
        row=2, col=1, secondary_y=False)
    fig.add_trace(
        go.Bar(x=away_games.index, y=away_games['homeScore'], name=f'{team2}', legend="legend2",
               marker=dict(color='#56B4E9')),
        row=2, col=1, secondary_y=False)
    
    fig.add_trace(
    go.Scatter(x=away_games.index, y=away_games["delta"], name='Away Game Difference', legend="legend2",
               mode='lines+markers', line=dict(color='red', width=2)),
    row=2, col=1, secondary_y=True)
    
    fig.update_xaxes(title_text="Date",
                     title_font=dict(size=18, family='Gravitas One', color='palegreen'), 
                     tickvals=list(range(0, len(away_games))),
    ticktext=away_games['gameDate'].tolist(),
    tickfont=dict(size=12, color='palegreen'),
    tickangle=-45, row=2, col=1)
    
    fig.add_trace(go.Bar(x=wins_losses_by_year["year"], y=wins_losses_by_year["team_win"], 
                         name="Wins", legend="legend3",
                         marker=dict(color='#56B4E9')), row=3, col=1, secondary_y=False)
    fig.add_trace(go.Bar(x=wins_losses_by_year["year"], y=wins_losses_by_year["team_loss"], 
                         name="Losses", legend="legend3",
                         marker=dict(color='#E69F00')), row=3, col=1, secondary_y=False)
    fig.add_trace(
    go.Scatter(x=wins_losses_by_year["year"], y=wins_losses_by_year["delta"], name='Wins-Losses Difference', 
               mode='lines+markers', legend="legend3", line=dict(color='red', width=2)),
    row=3, col=1, secondary_y=True)
    
    fig.update_xaxes(title_text="Season", title_font=dict(size=18, family='Gravitas One', color='palegreen'), row=3, col=1)
    
    fig.update_layout(
        height=1500,
        width=800,
        barmode="group",
        title_text="Number of points scored in home vs away games",
        title_font_size=26,
        legend=dict(x=0.92, y=1, xanchor="right", yanchor="top"),
        legend2=dict(x=0.92, y=0.6, xanchor="right", yanchor="bottom"),
        legend3=dict(x=0.92, y=0.23, xanchor="right", yanchor="bottom"))

    fig.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='deepskyblue'),title_text="Number of points", range=(80, 180), row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='lightsalmon'),title_text="Difference in Points", range=(-50, 50), secondary_y=True, row=1, col=1)
    
    fig.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='deepskyblue'),title_text="Number of points", range=(80, 180), row=2, col=1, secondary_y=False)
    fig.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='lightsalmon'),title_text="Difference in Points", range=(-50, 50), secondary_y=True, row=2, col=1)
    
    fig.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='deepskyblue'),title_text="Number of games", range=(0, 100), row=3, col=1, secondary_y=False)
    fig.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='lightsalmon'),title_text="Difference in Wins-Losses", range=(-50, 50), secondary_y=True, row=3, col=1)
    
    fig.update_annotations(font=dict(size=22, color="lightblue", family='Gravitas One'))
    
    # Add a horizontal line at y=110 for reference
    fig.add_hline(y=130, line_color="green", line_dash="dash", row=1, col=1)
    fig.add_hline(y=130, line_color="green", line_dash="dash", row=2, col=1)
    fig.add_hline(y=50, line_color="green", line_dash="dash", row=3, col=1)
    
    return fig

def total_salary_figure(grouped_team, selected_team_data, selected_team):
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=grouped_team['year'], y=grouped_team['sum_salary'],hovertext=grouped_team["full_team_name"], mode='markers', name="Total Salary", showlegend=True))
    fig2.add_trace(go.Scatter(x=selected_team_data['year'], y=selected_team_data['sum_salary'], mode='lines+markers', name=f"{selected_team} - Total Salary", showlegend=True))
    fig2.update_layout(title=f"Evolution of the total salary for {selected_team} vs All Teams and per season", xaxis_title="Season", yaxis_title="Total Salary (USD)", height=500)
    
    return fig2

def final_figure(games_final, team_final, team_final_names, selected_year):
    
    game_final_team1_score = [games_final.loc[row, 'homeScore'] if games_final.loc[row, 'hometeamId'] == team_final[0] else games_final.loc[row, 'awayScore'] for row in games_final.index]
    
    games_final['score_team1'] = game_final_team1_score
    
    game_final_team2_score = [games_final.loc[row, 'homeScore'] if games_final.loc[row, 'hometeamId'] == team_final[1] else games_final.loc[row, 'awayScore'] for row in games_final.index]
    games_final['score_team2'] = game_final_team2_score
    team_final_names2 = team_final_names.split(", ")
    
    fig = make_subplots(rows=1, cols=1, 
                        subplot_titles=[f"{team_final_names2[0]} vs {team_final_names2[1]} in the NBA Finals of the {selected_year} season"],  
                        specs=[[{"secondary_y": True}]],
                        vertical_spacing=0.1)
    
    fig.add_trace(
        go.Bar(x=games_final.index, y=games_final['score_team1'], 
               name=f'{team_final_names2[0]}', legend="legend",
               marker=dict(color="#56B4E9")),
        row=1, col=1, secondary_y=False)
    fig.add_trace(
        go.Bar(x=games_final.index, y=games_final['score_team2'], name=f'{team_final_names2[1]}', legend="legend",
               marker=dict(color="#FF9A7A")),
        row=1, col=1, secondary_y=False)

    fig.add_trace(
        go.Scatter(x=games_final.index, y=games_final['score_team1'] - games_final['score_team2'], name='Game Score Difference', legend="legend",
               mode='lines+markers', line=dict(color='red', width=2)),
        row=1, col=1, secondary_y=True)

    fig.update_layout(
        height=600,
        width=800,
        barmode="group",
        title_text="Number of points scored in each games in the NBA Finals",
        title_font_size=28,
        margin=dict(t=130),  # increases top margin
        legend=dict(x=0.93, y=1, xanchor="right", yanchor="top"))
    fig.update_xaxes(tickvals=list(range(0, len(games_final))),
                     title_font=dict(size=18, family='Gravitas One', color='palegreen'),
            ticktext=games_final['gameDate'].tolist(),
            title_text="Date of the game", 
            tickfont=dict(size=12, color='palegreen'),
            tickangle=-45, row=1, col=1)
    #fig.update_xaxes(title_font=dict(size=28, family='Gravitas One', color='deepskyblue'), 
    #                 title_text="Date", row=1, col=1)

    fig.update_yaxes(title_font=dict(size=22, family='Gravitas One', color='deepskyblue'),
                     title_text="Number of points", range=(70, 150), row=1, col=1, secondary_y=False)
    fig.update_yaxes(title_font=dict(size=22, family='Gravitas One', color='lightsalmon'),
                     title_text="Difference in Points", range=(-60, 60), secondary_y=True, row=1, col=1)
    
    # Add a horizontal line at y=110 for reference
    fig.add_hline(y=110, line_color="green", line_dash="dash", row=1, col=1)
    fig.update_annotations(font=dict(size=26, color="lightblue"))

    return fig


def first_round_figure(games_west, games_east, round, selected_year):

    games_west_round1 = games_west[games_west["seriesGameNumber"] == 1]
    games_east_round1 = games_east[games_east["seriesGameNumber"] == 1]
    team_round1_west = [(row["hometeamId"], row["awayteamId"]) for index, row in games_west_round1.iterrows()]
    team_round1_east = [(row["hometeamId"], row["awayteamId"]) for index, row in games_east_round1.iterrows()]
    team_round1_west_names = [(dict_teamID.get(team_id[0], "Unknown"), dict_teamID.get(team_id[1], "Unknown")) for team_id in team_round1_west]
    team_round1_east_names = [(dict_teamID.get(team_id[0], "Unknown"), dict_teamID.get(team_id[1], "Unknown")) for team_id in team_round1_east]
    
    
    subtitles = []
    for teams in zip(team_round1_west_names, team_round1_east_names):
        subtitles.append(f"{teams[0][0]} vs {teams[0][1]}")
        subtitles.append(f"{teams[1][0]} vs {teams[1][1]}")
    
    fig2 = make_subplots(rows=len(team_round1_west), cols=2, 
                         subplot_titles=subtitles, 
                         horizontal_spacing=0.14,
                         vertical_spacing=0.08,
                         specs=[[{"secondary_y": True}, {"secondary_y": True}] for _ in range(len(team_round1_west))])
    
    for i, team_id in enumerate(team_round1_west):
        
        game_final_team1_score = [games_west.loc[row, 'homeScore'] if games_west.loc[row, 'hometeamId'] == team_id[0] else games_west.loc[row, 'awayScore'] for row in games_west.index]
        games_west['score_team1'] = game_final_team1_score
        game_final_team2_score = [games_west.loc[row, 'homeScore'] if games_west.loc[row, 'hometeamId'] == team_id[1] else games_west.loc[row, 'awayScore'] for row in games_west.index]
        games_west['score_team2'] = game_final_team2_score
        games_west.reset_index(drop=True, inplace=True)

        
        
        team_games = games_west[(games_west['hometeamId'] == team_id[0]) | (games_west['awayteamId'] == team_id[0])]

        fig2.add_trace(go.Bar(x=list(range(1, len(team_games)+1)), y=team_games['score_team1'], 
                              name=dict_teamID.get(team_id[0], "Unknown"), 
                              marker=dict(color="#56B4E9"), 
                              showlegend=True, legend=f"legend{i+1}"), row=i+1, col=1, secondary_y=False)
        fig2.add_trace(go.Bar(x=list(range(1, len(team_games)+1)), y=team_games['score_team2'], 
                              name=dict_teamID.get(team_id[1], "Unknown"), 
                              marker=dict(color="#E6A519"), 
                              showlegend=True, legend=f"legend{i+1}"), row=i+1, col=1, secondary_y=False)
        fig2.add_trace(go.Scatter(x=list(range(1, len(team_games)+1)), y=team_games['score_team1'] - team_games['score_team2'], mode='markers+lines', 
                                  name='Difference', marker=dict(color="#B12A31"), line=dict(color="#B12A31"), 
                                  showlegend=True, legend=f"legend{i+1}"), row=i+1, col=1, secondary_y=True)

        fig2.update_xaxes(title_text="Date of the game",
                          title_font=dict(size=18, family='Gravitas One', color='palegreen'),
            tickvals=list(range(1, len(team_games)+1)),
            ticktext=team_games['gameDate'].tolist(),
            tickfont=dict(size=12, color='palegreen'),
            tickangle=-45, 
            row=i+1, col=1)
        fig2.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='deepskyblue'),
                          title_text="Number of points", range=(60, 150), secondary_y=False)
        fig2.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='lightsalmon'),
                          title_text="Difference in Points", range=(-40, 50), secondary_y=True)

                          
        
    for j, team_id in enumerate(team_round1_east):
        game_final_team1_score = [games_east.loc[row, 'homeScore'] if games_east.loc[row, 'hometeamId'] == team_id[0] else games_east.loc[row, 'awayScore'] for row in games_east.index]
        games_east['score_team1'] = game_final_team1_score
        game_final_team2_score = [games_east.loc[row, 'homeScore'] if games_east.loc[row, 'hometeamId'] == team_id[1] else games_east.loc[row, 'awayScore'] for row in games_east.index]
        games_east['score_team2'] = game_final_team2_score
        games_east.reset_index(drop=True, inplace=True)
        
        team_games = games_east[(games_east['hometeamId'] == team_id[0]) | (games_east['awayteamId'] == team_id[0])]

        fig2.add_trace(go.Bar(x=list(range(1, len(team_games)+1)), y=team_games['score_team1'], 
                              name=dict_teamID.get(team_id[0], "Unknown"), 
                              marker=dict(color="#66E0B3"), 
                              showlegend=True, legend=f"legend2{j+1}"), row=j+1, col=2, secondary_y=False)
        fig2.add_trace(go.Bar(x=list(range(1, len(team_games)+1)), y=team_games['score_team2'], 
                              name=dict_teamID.get(team_id[1], "Unknown"), 
                              marker=dict(color="#3E3594"), 
                              showlegend=True, legend=f"legend2{j+1}"), row=j+1, col=2, secondary_y=False)
        fig2.add_trace(go.Scatter(x=list(range(1, len(team_games)+1)), y=team_games['score_team1'] - team_games['score_team2'], 
                                  mode='markers+lines', name='Difference', marker=dict(color="#B12A31"), line=dict(color="#B12A31"), 
                                  showlegend=True, legend=f"legend2{j+1}"), row=j+1, col=2, secondary_y=True)
        
        fig2.update_xaxes(title_text="Date of the game",
                          title_font=dict(size=18, family='Gravitas One', color='palegreen'),
            tickvals=list(range(1, len(team_games)+1)),
            ticktext=team_games['gameDate'].tolist(),
            tickfont=dict(size=12, color='palegreen'), 
            tickangle=-45, 
            row=j+1, col=2)
        fig2.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='deepskyblue'),
                          title_text="Number of points", range=(60, 150), secondary_y=False)
        fig2.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='lightsalmon'),
                          title_text="Difference in Points", range=(-40, 50), secondary_y=True)

    fig2.update_layout(
        height=600*len(team_round1_east),
        width=1000,
        title_text=f"Playoff Games in the {round} of the {selected_year} season",
        title_font_size=26,
        margin=dict(t=150, b=80),  # increases top margin
        legend1=dict(x=0.4, y=1.001, xanchor="right", yanchor="top"),
        legend2=dict(x=0.4, y=0.73, xanchor="right", yanchor="top"),
        legend3=dict(x=0.4, y=0.47, xanchor="right", yanchor="top"),
        legend4=dict(x=0.4, y=0.2, xanchor="right", yanchor="top"),
        legend21=dict(x=0.8, y=1, xanchor="left", yanchor="top"),
        legend22=dict(x=0.8, y=0.73, xanchor="left", yanchor="top"),
        legend23=dict(x=0.8, y=0.47, xanchor="left", yanchor="top"),
        legend24=dict(x=0.8, y=0.2, xanchor="left", yanchor="top"),
    )
    # Add a horizontal line at y=100 for reference
    fig2.add_hline(y=100, line_color="green", line_dash="dash")
    fig2.update_annotations(font=dict(size=22, color="lightblue"), yshift=20)  # increases top margin and bottom margin
    
    return fig2

def semi_round_figure(games_west, games_east, round, selected_year):

    games_west_round1 = games_west[games_west["seriesGameNumber"] == 1]
    games_east_round1 = games_east[games_east["seriesGameNumber"] == 1]
    team_round1_west = [(row["hometeamId"], row["awayteamId"]) for index, row in games_west_round1.iterrows()]
    team_round1_east = [(row["hometeamId"], row["awayteamId"]) for index, row in games_east_round1.iterrows()]
    team_round1_west_names = [(dict_teamID.get(team_id[0], "Unknown"), dict_teamID.get(team_id[1], "Unknown")) for team_id in team_round1_west]
    team_round1_east_names = [(dict_teamID.get(team_id[0], "Unknown"), dict_teamID.get(team_id[1], "Unknown")) for team_id in team_round1_east]
    
    
    subtitles = []
    for teams in zip(team_round1_west_names, team_round1_east_names):
        subtitles.append(f"{teams[0][0]} vs {teams[0][1]}")
        subtitles.append(f"{teams[1][0]} vs {teams[1][1]}")
    
    fig2 = make_subplots(rows=len(team_round1_west), cols=2, 
                         subplot_titles=subtitles, 
                         horizontal_spacing=0.14,
                         vertical_spacing=0.17,
                         specs=[[{"secondary_y": True}, {"secondary_y": True}] for _ in range(len(team_round1_west))])
    
    for i, team_id in enumerate(team_round1_west):
        
        game_final_team1_score = [games_west.loc[row, 'homeScore'] if games_west.loc[row, 'hometeamId'] == team_id[0] else games_west.loc[row, 'awayScore'] for row in games_west.index]
        games_west['score_team1'] = game_final_team1_score
        game_final_team2_score = [games_west.loc[row, 'homeScore'] if games_west.loc[row, 'hometeamId'] == team_id[1] else games_west.loc[row, 'awayScore'] for row in games_west.index]
        games_west['score_team2'] = game_final_team2_score
        games_west.reset_index(drop=True, inplace=True)

        
        
        team_games = games_west[(games_west['hometeamId'] == team_id[0]) | (games_west['awayteamId'] == team_id[0])]

        fig2.add_trace(go.Bar(x=list(range(1, len(team_games)+1)), y=team_games['score_team1'], 
                              name=dict_teamID.get(team_id[0], "Unknown"), 
                              marker=dict(color="#56B4E9"), 
                              showlegend=True, legend=f"legend{i+1}"), row=i+1, col=1, secondary_y=False)
        fig2.add_trace(go.Bar(x=list(range(1, len(team_games)+1)), y=team_games['score_team2'], 
                              name=dict_teamID.get(team_id[1], "Unknown"), 
                              marker=dict(color="#E6A519"), 
                              showlegend=True, legend=f"legend{i+1}"), row=i+1, col=1, secondary_y=False)
        fig2.add_trace(go.Scatter(x=list(range(1, len(team_games)+1)), y=team_games['score_team1'] - team_games['score_team2'], mode='markers+lines', 
                                  name='Difference', marker=dict(color="#B12A31"), line=dict(color="#B12A31"), 
                                  showlegend=True, legend=f"legend{i+1}"), row=i+1, col=1, secondary_y=True)

        fig2.update_xaxes(title_text="Date of the game",
                          title_font=dict(size=18, family='Gravitas One', color='palegreen'),
            tickvals=list(range(1, len(team_games)+1)),
            ticktext=team_games['gameDate'].tolist(),
            tickfont=dict(size=12, color='palegreen'), 
            tickangle=-45, row=i+1, col=1)
        fig2.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='deepskyblue'),
                          title_text="Number of points", range=(60, 150), secondary_y=False)
        fig2.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='lightsalmon'),
                          title_text="Difference in Points", range=(-40, 50), secondary_y=True)

                          
        
    for j, team_id in enumerate(team_round1_east):
        game_final_team1_score = [games_east.loc[row, 'homeScore'] if games_east.loc[row, 'hometeamId'] == team_id[0] else games_east.loc[row, 'awayScore'] for row in games_east.index]
        games_east['score_team1'] = game_final_team1_score
        game_final_team2_score = [games_east.loc[row, 'homeScore'] if games_east.loc[row, 'hometeamId'] == team_id[1] else games_east.loc[row, 'awayScore'] for row in games_east.index]
        games_east['score_team2'] = game_final_team2_score
        games_east.reset_index(drop=True, inplace=True)
        
        team_games = games_east[(games_east['hometeamId'] == team_id[0]) | (games_east['awayteamId'] == team_id[0])]

        fig2.add_trace(go.Bar(x=list(range(1, len(team_games)+1)), y=team_games['score_team1'], 
                              name=dict_teamID.get(team_id[0], "Unknown"), 
                              marker=dict(color="#66E0B3"), 
                              showlegend=True, legend=f"legend2{j+1}"), row=j+1, col=2, secondary_y=False)
        fig2.add_trace(go.Bar(x=list(range(1, len(team_games)+1)), y=team_games['score_team2'], 
                              name=dict_teamID.get(team_id[1], "Unknown"), 
                              marker=dict(color="#3E3594"), 
                              showlegend=True, legend=f"legend2{j+1}"), row=j+1, col=2, secondary_y=False)
        fig2.add_trace(go.Scatter(x=list(range(1, len(team_games)+1)), y=team_games['score_team1'] - team_games['score_team2'], 
                                  mode='markers+lines', name='Difference', marker=dict(color="#B12A31"), line=dict(color="#B12A31"), 
                                  showlegend=True, legend=f"legend2{j+1}"), row=j+1, col=2, secondary_y=True)
        
        fig2.update_xaxes(title_text="Date of the game",
                          title_font=dict(size=18, family='Gravitas One', color='palegreen'),
            tickvals=list(range(1, len(team_games)+1)),
            ticktext=team_games['gameDate'].tolist(),
            tickfont=dict(size=12, color='palegreen'), 
            tickangle=-45, 
            row=j+1, col=2)
        fig2.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='deepskyblue'),
                          title_text="Number of points", range=(60, 150), secondary_y=False)
        fig2.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='lightsalmon'),
                          title_text="Difference in Points", range=(-40, 50), secondary_y=True)

    fig2.update_layout(
        height=600*len(team_round1_east),
        width=1000,
        title_text=f"Playoff Games in the {round} of the {selected_year} season",
        title_font_size=26,
        margin=dict(t=150, b=80),  # increases top margin and bottom margin
        legend1=dict(x=0.4, y=0.99, xanchor="right", yanchor="top"),
        legend2=dict(x=0.4, y=0.40, xanchor="right", yanchor="top"),
        legend21=dict(x=0.8, y=0.99, xanchor="left", yanchor="top"),
        legend22=dict(x=0.8, y=0.4, xanchor="left", yanchor="top"),
        )
    # Add a horizontal line at y=100 for reference
    fig2.add_hline(y=100, line_color="green", line_dash="dash")
    fig2.update_annotations(font=dict(size=22, color="lightblue"), yshift=20)  # increases top margin and bottom margin
    
    return fig2

def conf_round_figure(games_west, games_east, round, selected_year):

    games_west_round1 = games_west[games_west["seriesGameNumber"] == 1]
    games_east_round1 = games_east[games_east["seriesGameNumber"] == 1]
    team_round1_west = [(row["hometeamId"], row["awayteamId"]) for index, row in games_west_round1.iterrows()]
    team_round1_east = [(row["hometeamId"], row["awayteamId"]) for index, row in games_east_round1.iterrows()]
    team_round1_west_names = [(dict_teamID.get(team_id[0], "Unknown"), dict_teamID.get(team_id[1], "Unknown")) for team_id in team_round1_west]
    team_round1_east_names = [(dict_teamID.get(team_id[0], "Unknown"), dict_teamID.get(team_id[1], "Unknown")) for team_id in team_round1_east]
    
    
    subtitles = []
    for teams in zip(team_round1_west_names, team_round1_east_names):
        subtitles.append(f"{teams[0][0]} vs {teams[0][1]}")
        subtitles.append(f"{teams[1][0]} vs {teams[1][1]}")
    
    fig2 = make_subplots(rows=len(team_round1_west), cols=2, 
                         subplot_titles=subtitles, 
                         horizontal_spacing=0.14,
                         vertical_spacing=0.1,
                         specs=[[{"secondary_y": True}, {"secondary_y": True}] for _ in range(len(team_round1_west))])
    
    for i, team_id in enumerate(team_round1_west):
        
        game_final_team1_score = [games_west.loc[row, 'homeScore'] if games_west.loc[row, 'hometeamId'] == team_id[0] else games_west.loc[row, 'awayScore'] for row in games_west.index]
        games_west['score_team1'] = game_final_team1_score
        game_final_team2_score = [games_west.loc[row, 'homeScore'] if games_west.loc[row, 'hometeamId'] == team_id[1] else games_west.loc[row, 'awayScore'] for row in games_west.index]
        games_west['score_team2'] = game_final_team2_score
        games_west.reset_index(drop=True, inplace=True)

        
        
        team_games = games_west[(games_west['hometeamId'] == team_id[0]) | (games_west['awayteamId'] == team_id[0])]

        fig2.add_trace(go.Bar(x=list(range(1, len(team_games)+1)), y=team_games['score_team1'], 
                              name=dict_teamID.get(team_id[0], "Unknown"), 
                              marker=dict(color="#56B4E9"), 
                              showlegend=True, legend=f"legend{i+1}"), row=i+1, col=1, secondary_y=False)
        fig2.add_trace(go.Bar(x=list(range(1, len(team_games)+1)), y=team_games['score_team2'], 
                              name=dict_teamID.get(team_id[1], "Unknown"), 
                              marker=dict(color="#E6A519"), 
                              showlegend=True, legend=f"legend{i+1}"), row=i+1, col=1, secondary_y=False)
        fig2.add_trace(go.Scatter(x=list(range(1, len(team_games)+1)), y=team_games['score_team1'] - team_games['score_team2'], mode='markers+lines', 
                                  name='Difference', marker=dict(color="#B12A31"), line=dict(color="#B12A31"), 
                                  showlegend=True, legend=f"legend{i+1}"), row=i+1, col=1, secondary_y=True)

        fig2.update_xaxes(title_text="Date of the game",
                          title_font=dict(size=18, family='Gravitas One', color='palegreen'),
            tickvals=list(range(1, len(team_games)+1)),
            ticktext=team_games['gameDate'].tolist(), 
            tickfont=dict(size=12, color='palegreen'), 
            tickangle=-45, row=i+1, col=1)
        fig2.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='deepskyblue'),
                          title_text="Number of points", range=(60, 150), secondary_y=False)
        fig2.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='lightsalmon'),
                          title_text="Difference in Points", range=(-40, 50), secondary_y=True)

                          
        
    for j, team_id in enumerate(team_round1_east):
        game_final_team1_score = [games_east.loc[row, 'homeScore'] if games_east.loc[row, 'hometeamId'] == team_id[0] else games_east.loc[row, 'awayScore'] for row in games_east.index]
        games_east['score_team1'] = game_final_team1_score
        game_final_team2_score = [games_east.loc[row, 'homeScore'] if games_east.loc[row, 'hometeamId'] == team_id[1] else games_east.loc[row, 'awayScore'] for row in games_east.index]
        games_east['score_team2'] = game_final_team2_score
        games_east.reset_index(drop=True, inplace=True)
        
        team_games = games_east[(games_east['hometeamId'] == team_id[0]) | (games_east['awayteamId'] == team_id[0])]

        fig2.add_trace(go.Bar(x=list(range(1, len(team_games)+1)), y=team_games['score_team1'], 
                              name=dict_teamID.get(team_id[0], "Unknown"), 
                              marker=dict(color="#66E0B3"), 
                              showlegend=True, legend=f"legend2{j+1}"), row=j+1, col=2, secondary_y=False)
        fig2.add_trace(go.Bar(x=list(range(1, len(team_games)+1)), y=team_games['score_team2'], 
                              name=dict_teamID.get(team_id[1], "Unknown"), 
                              marker=dict(color="#3E3594"), 
                              showlegend=True, legend=f"legend2{j+1}"), row=j+1, col=2, secondary_y=False)
        fig2.add_trace(go.Scatter(x=list(range(1, len(team_games)+1)), y=team_games['score_team1'] - team_games['score_team2'], 
                                  mode='markers+lines', name='Difference', marker=dict(color="#B12A31"), line=dict(color="#B12A31"), 
                                  showlegend=True, legend=f"legend2{j+1}"), row=j+1, col=2, secondary_y=True)
        
        fig2.update_xaxes(title_text="Date of the game",
                          title_font=dict(size=18, family='Gravitas One', color='palegreen'),
            tickvals=list(range(1, len(team_games)+1)),
            ticktext=team_games['gameDate'].tolist(), 
            tickfont=dict(size=12, color='palegreen'), 
            tickangle=-45,
            row=j+1, col=2)
        fig2.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='deepskyblue'),
                          title_text="Number of points", range=(60, 150), secondary_y=False)
        fig2.update_yaxes(title_font=dict(size=16, family='Gravitas One', color='lightsalmon'),
                          title_text="Difference in Points", range=(-40, 50), secondary_y=True)

    fig2.update_layout(
        height=600*len(team_round1_east),
        width=1000,
        title_text=f"Playoff Games in the {round} of the {selected_year} season",
        title_font_size=26,
        margin=dict(t=150, b=80),  # increases top margin and bottom margin
        legend1=dict(x=0.42, y=1, xanchor="right", yanchor="top"),
        legend21=dict(x=0.8, y=1, xanchor="left", yanchor="top"),
        )
    # Add a horizontal line at y=100 for reference
    fig2.add_hline(y=100, line_color="green", line_dash="dash")
    fig2.update_annotations(font=dict(size=22, color="lightblue"), yshift=20)  # increases top margin and bottom margin
    
    return fig2