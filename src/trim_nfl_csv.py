import pandas as pd
import numpy as np

# helper function used when computing 'result' column
def interpret_score_difference(result):
    diff = eval(result)
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
data = pd.read_csv('data/raw_data/nfl-2023-raw.csv')

# remove all games that haven't been played yet
trimmed_data = data[data['Result'].notnull()]


trimmed_data[['score1', 'dash', 'score2']] = trimmed_data['Result'].str.split(' ', expand=True)

# use difference of scores and helper function to determine result column
trimmed_data['Result'] = trimmed_data['Result'].apply(interpret_score_difference)

# populate 'location' column with proper values
trimmed_data.loc[trimmed_data['Location'] != '0', 'Location'] = 'H'

# split date and time
trimmed_data[['Date', 'Time']] = trimmed_data['Date'].str.split(' ', expand=True)

# remove all unneeded columns
trimmed_data = trimmed_data.drop(columns=['Match Number', 'Round Number', 'Time', 'dash'], axis = 1)

#arrange columns in proper order
trimmed_data = trimmed_data[['Date', 'Location', 'Home Team', 'Away Team', 'score1', 'score2', 'Result']]

# output to trimmed folder
trimmed_data.to_csv('data/processed_data/nfl/nfl_current_trimmed.csv', index=False)