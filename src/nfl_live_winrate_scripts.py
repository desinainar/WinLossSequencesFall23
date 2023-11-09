import pandas as pd
import numpy as np

from utilities import *

def interpret_score_difference(result):
    diff = eval(result)
    if(diff > 0):
        return 1
    if(diff < 0):
        return 0
    return 0.5



nfl_df = pd.read_csv('data/processed_data/nfl_live/nfl_current_trimmed.csv')
data = pd.read_csv('data/raw_data/nfl-2023-raw.csv')

#getting winrate for each team
teams = nfl_df['team1'].to_list()
teams = list(set(teams))
#print(teams)

winrates = {}
for team in teams:
    nfl_winrate_sequence = get_cumulative_winrate_sequence(nfl_df, 2023, team, '2023-11-02')
    curr_winrate = nfl_winrate_sequence['winrate'].iloc[-1]
    winrates[team] = round(curr_winrate, 3)
#print(winrates)

#get next week of unplayed games
next_week = data[data['Round Number'] == 9]

next_week.loc[next_week['Location'] != '0', 'Location'] = 'H'

next_week[['Date', 'Time']] = next_week['Date'].str.split(' ', expand=True)
next_week[['Day', 'Month', 'Year']] = next_week['Date'].str.split('/', expand=True)
next_week['Date'] = next_week[['Year', 'Month', 'Day']].apply(lambda x: '-'.join(str(value) for value in x), axis=1)

team_abbr = {'Kansas City Chiefs' : 'KC', 'Los Angeles Chargers' : 'LAC', 'Denver Broncos' : 'DEN', 'Las Vegas Raiders' : 'LV',
'Baltimore Ravens' : 'BAL', 'Cincinnati Bengals' : 'CIN', 'Cleveland Browns' : 'CLE', 'Pittsburgh Steelers' : 'PIT',
'Houston Texans' : 'HOU', 'Indianapolis Colts' : 'IND', 'Jacksonville Jaguars' : 'JAX', 'Tennessee Titans' : 'TEN',
'New England Patriots' : 'NE', 'New York Jets' : 'NYJ', 'Miami Dolphins' : 'MIA', 'Buffalo Bills' : 'BUF',
'Detroit Lions' : 'DET', 'Green Bay Packers' : 'GB', 'Chicago Bears' : 'CHI', 'Minnesota Vikings' : 'MIN',
'Dallas Cowboys' : 'DAL', 'New York Giants' : 'NYG', 'Philadelphia Eagles' : 'PHI', 'Washington Commanders' : 'WAS',
'Atlanta Falcons' : 'ATL', 'New Orleans Saints' : 'NO', 'Carolina Panthers' : 'CAR', 'Tampa Bay Buccaneers' : 'TB',
'Arizona Cardinals' : 'ARI', 'San Francisco 49ers' : 'SF', 'Seattle Seahawks' : 'SEA', 'Los Angeles Rams' : 'LAR'}
next_week.replace({"Home Team": team_abbr}, inplace = True)
next_week.replace({"Away Team": team_abbr}, inplace = True)

next_week = next_week.drop(columns=['Match Number', 'Round Number', 'Time', 'Month', 'Day'], axis = 1)
next_week.rename(columns={'Home Team': 'team1', 'Away Team': 'team2', 'Year': 'season'}, inplace = True)

next_week['team1winrate'] = next_week['team1']
next_week.replace({"team1winrate": winrates}, inplace = True)
next_week['team2winrate'] = next_week['team2']
next_week.replace({"team2winrate": winrates}, inplace = True)

next_week['Result'] = next_week['team1winrate']/(next_week['team1winrate'] + next_week['team2winrate'])

next_week = next_week[['Date', 'season', 'Location', 'team1', 'team2', 'team1winrate', 'team2winrate', 'Result']]
next_week.columns = next_week.columns.str.lower()



next_week.to_csv('data/processed_data/nfl_live/nfl_live_predictions.csv', index=False)

#prediction method accuracies for games that already happened
accuracy_df = nfl_df
accuracy_df['team1winrate'] = accuracy_df['team1']
accuracy_df.replace({"team1winrate": winrates}, inplace = True)
accuracy_df['team2winrate'] = accuracy_df['team2']
accuracy_df.replace({"team2winrate": winrates}, inplace = True)

accuracy_df['prediction'] = accuracy_df['team1winrate']/(accuracy_df['team1winrate'] + accuracy_df['team2winrate'])

accuracy_df = get_prediction_metric_accuracy(accuracy_df, prob_column_name='prediction')
accuracy_df.to_csv('data/processed_data/nfl_live/nfl_live_cumulative_accuracies.csv', index=False)





