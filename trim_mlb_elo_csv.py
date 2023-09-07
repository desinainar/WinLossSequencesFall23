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
data = pd.read_csv('data/raw_data/mlb_elo.csv')

# remove all games that haven't been played yet
trimmed_data = data[data['rating1_post'].notnull()]

# remove all playoff games
trimmed_data = trimmed_data[trimmed_data['playoff'].isnull()]

# convert 'neutral' to string (this is done to avoid a FutureWarning with Pandas regarding type incompatibilities)
trimmed_data['neutral'] = trimmed_data['neutral'].astype(str)

# populate 'neutral' column with proper values
trimmed_data.loc[trimmed_data['neutral'] == '0', 'neutral'] = 'H'
trimmed_data.loc[trimmed_data['neutral'] == '1', 'neutral'] = 'N'

# use difference of scores and helper function to determine result column
trimmed_data['result'] = trimmed_data['score1'] - trimmed_data['score2']
trimmed_data['result'] = trimmed_data['result'].apply(interpret_score_difference)

# remove all unneeded columns
trimmed_data = trimmed_data.drop(columns=['playoff', 'elo1_pre', 'elo2_pre', 'elo1_post', 'elo2_post', 
                                          'rating1_pre','rating2_pre','pitcher1','pitcher2','pitcher1_rgs',
                                          'pitcher2_rgs','pitcher1_adj','pitcher2_adj','rating_prob1',
                                          'rating_prob2','rating1_post','rating2_post','score1','score2'], axis = 1)

# output to 'trimmed_mlb_elo.csv'
trimmed_data.to_csv('data/trimmed_data/trimmed_mlb_elo.csv', index=False)


