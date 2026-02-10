import pandas as pd

# Load data
df_sal = pd.read_csv('../data/salaries.csv')
df_players = pd.read_csv('../data/NBA_stats/Player Totals.csv')

print(f"Salaries: {len(df_sal)} rows, {df_sal['full_team_name'].isna().sum()} missing team names")
print(f"Player Totals: {len(df_players)} rows")

# Create a lookup dictionary: (player_name, season) -> team
player_team_lookup = {}
for _, row in df_players.iterrows():
    key = (row['player'], row['season'])
    if key not in player_team_lookup:
        player_team_lookup[key] = row['team']

# Fill missing team names
filled_count = 0
for idx, row in df_sal[df_sal['full_team_name'].isna()].iterrows():
    key = (row['Players'], row['year'])
    if key in player_team_lookup:
        df_sal.at[idx, 'full_team_name'] = player_team_lookup[key]
        filled_count += 1

print(f"\nFilled {filled_count} missing team names")
print(f"Remaining missing: {df_sal['full_team_name'].isna().sum()}")

# Save the updated file
df_sal.to_csv('data/salaries.csv', index=False)
print("\nSaved updated salaries.csv")
