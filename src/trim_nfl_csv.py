import pandas as pd
import numpy as np

from utilities import *
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
data = pd.read_csv('../data/raw_data/nfl-2023-raw.csv')

# remove all games that haven't been played yet
trimmed_data = data[data['Result'].notnull()]

#save original game scores in separate columns
trimmed_data[['score1', 'dash', 'score2']] = trimmed_data['Result'].str.split(' ', expand=True)

# use difference of scores and helper function to determine result column
trimmed_data['Result'] = trimmed_data['Result'].apply(interpret_score_difference)

# populate 'location' column with proper values
trimmed_data.loc[trimmed_data['Location'] != '0', 'Location'] = 'H'

# split date and time
trimmed_data[['Date', 'Time']] = trimmed_data['Date'].str.split(' ', expand=True)
trimmed_data[['Day', 'Month', 'Year']] = trimmed_data['Date'].str.split('/', expand=True)
trimmed_data['Date'] = trimmed_data[['Year', 'Month', 'Day']].apply(lambda x: '-'.join(str(value) for value in x), axis=1)




# rename teams to abbreviations
team_abbr = {'Kansas City Chiefs' : 'KC', 'Los Angeles Chargers' : 'LAC', 'Denver Broncos' : 'DEN', 'Las Vegas Raiders' : 'LV',
'Baltimore Ravens' : 'BAL', 'Cincinnati Bengals' : 'CIN', 'Cleveland Browns' : 'CLE', 'Pittsburgh Steelers' : 'PIT',
'Houston Texans' : 'HOU', 'Indianapolis Colts' : 'IND', 'Jacksonville Jaguars' : 'JAX', 'Tennessee Titans' : 'TEN',
'New England Patriots' : 'NE', 'New York Jets' : 'NYJ', 'Miami Dolphins' : 'MIA', 'Buffalo Bills' : 'BUF',
'Detroit Lions' : 'DET', 'Green Bay Packers' : 'GB', 'Chicago Bears' : 'CHI', 'Minnesota Vikings' : 'MIN',
'Dallas Cowboys' : 'DAL', 'New York Giants' : 'NYG', 'Philadelphia Eagles' : 'PHI', 'Washington Commanders' : 'WAS',
'Atlanta Falcons' : 'ATL', 'New Orleans Saints' : 'NO', 'Carolina Panthers' : 'CAR', 'Tampa Bay Buccaneers' : 'TB',
'Arizona Cardinals' : 'ARI', 'San Francisco 49ers' : 'SF', 'Seattle Seahawks' : 'SEA', 'Los Angeles Rams' : 'LAR'}
trimmed_data.replace({"Home Team": team_abbr}, inplace = True)
trimmed_data.replace({"Away Team": team_abbr}, inplace = True)

# remove all unneeded columns
trimmed_data = trimmed_data.drop(columns=['Match Number', 'Round Number', 'Time', 'dash', 'Month', 'Day'], axis = 1)

# rename colunms to match template
trimmed_data.rename(columns={'Home Team': 'team1', 'Away Team': 'team2', 'Year': 'season'}, inplace = True)

#arrange columns in proper order
trimmed_data = trimmed_data[['Date', 'season', 'Location', 'team1', 'team2', 'score1', 'score2', 'Result']]
trimmed_data.columns = trimmed_data.columns.str.lower()

#add flipped results
trimmed_data = get_flipped_data_appended(trimmed_data)

# output to trimmed folder
trimmed_data.to_csv('output.csv', index=False)