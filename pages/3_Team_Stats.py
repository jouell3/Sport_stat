import random
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_loader import load_all_data, load_nba_stat_definitions

st.title("Team Statistics")

_, df_teams, _, _ = load_all_data()
stat_dict = load_nba_stat_definitions()

def create_metric_subplots(team_stats, metrics2, metrics, team_name):
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
                x=team_stats['season'],
                y=team_stats[metric],
                name=metric,
                marker=dict(color=random.choice(list_colors))
            ),
            row=k,
            col=j
        )
    
    fig.update_xaxes(title_text="Season")
    fig.update_yaxes(title_text="Value", col=1)
    fig.update_layout(height=400 * (int(len(metrics)/2) + len(metrics)%2), title_text=f"{team_name} - Statistics by Metric", showlegend=False)
    
    return fig

teams = df_teams['team'].unique()
years = sorted(df_teams['season'].unique())

team = st.selectbox("Select a team:", teams)
year_range = st.slider("Select year range:", min_value=int(min(years)), max_value=int(max(years)), value=(int(min(years)), int(max(years))))

    # --- Metric selection ---
numeric_cols2 = [col for col in df_teams.columns if df_teams[col].dtype != 'O' and col not in ['season', 'full_team_name']]
numeric_cols = [value for key, value in stat_dict.items() if key in numeric_cols2]
metrics2 = st.multiselect("Select metrics to display:", numeric_cols, default=numeric_cols[1])
metrics = [key for key, value in stat_dict.items() if value in metrics2]

filtered = df_teams[(df_teams['team'] == team) & (df_teams['season'] >= year_range[0]) & (df_teams['season'] <= year_range[1])].reset_index(drop=True)

fig = create_metric_subplots(filtered, metrics2, metrics, team)
st.plotly_chart(fig, width='stretch')


if not filtered.empty:
    st.dataframe(filtered[['season', 'team'] + metrics], hide_index=True)
else:
    st.warning("No data for this team and year range.")

st.markdown("### Column Definitions")
for col in filtered.columns:
    desc = stat_dict.get(col, "No description available.")
    st.write(f"**{col}**: {desc}")
