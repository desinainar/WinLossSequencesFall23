import pandas as pd
import numpy as np
# helper function used when computing 'result' column
def interpret_score_difference(diff):
    if(diff > 0):
        return 1
    if(diff < 0):
        return 0
    return 0.5

# -----------------
#  FIELDS IN DATA
# -----------------
# date: date when game was played
# season: year when season began
# neutral: H if team1 is home, A if team1 is away, N if neutral site (NOTE: the fivethirtyeight data is surely inaccurate regarding neutral sites)
# team1: who the league designated as the home team
# team2: who the league designated as the away team
# elo_prob1: team1 winning probability as determined by ELO
# elo_prob2: team2 winning probability as determined by ELO
# result: 1 if team1 wins, 0 if team2 wins, 0.5 if tie

# open .csv into 'data' variable
data = pd.read_csv('../../data/raw_data/nhl_elo_original.csv')

# remove all games that haven't been played yet
trimmed_data = data[data['home_team_postgame_rating'].notnull()]

print(len(trimmed_data))

# remove all playoff games
trimmed_data = trimmed_data[trimmed_data['playoff'] == 0]

print(len(trimmed_data))

# convert 'neutral' to string (this is done to avoid a FutureWarning with Pandas regarding type incompatibilities)
trimmed_data['neutral'] = trimmed_data['neutral'].astype(str)

print(len(trimmed_data))

# populate 'neutral' column with proper values
trimmed_data.loc[trimmed_data['neutral'] == '0', 'neutral'] = 'H'
trimmed_data.loc[trimmed_data['neutral'] == '1', 'neutral'] = 'N'

print(len(trimmed_data))

# rename 'neutral' to 'location'
trimmed_data = trimmed_data.rename(columns={'neutral': 'location'})

print(len(trimmed_data))

# use difference of scores and helper function to determine result column
trimmed_data['result'] = trimmed_data['home_team_score'] - trimmed_data['away_team_score']
trimmed_data['result'] = trimmed_data['result'].apply(interpret_score_difference)

# remove all unneeded columns

# arrange columns in proper order
trimmed_data = trimmed_data[['date', 'season', 'location', 'home_team', 'away_team', 'home_team_score', 'away_team_score', 'result', 'home_team_winprob']]
print(len(trimmed_data))


trimmed_data = trimmed_data.rename(columns={'home_team': 'team1', 'away_team': 'team2', 'home_team_score': 'score1', 'away_team_score': 'score2', 'home_team_winprob': 'elo_prob1'})

# output to 'trimmed_nhl.csv'
trimmed_data.to_csv('../../data/processed_data/nhl/nhl_elo.csv', index=False)

# drop elo_prob1
trimmed_data = trimmed_data.drop(columns=['elo_prob1'], axis = 1)

trimmed_data.to_csv('../../data/processed_data/generic_nhl_data.csv', index=False)


