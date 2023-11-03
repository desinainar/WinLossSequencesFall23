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

team_abbr = {'Kansas City Chiefs' : 'KC', 'Los Angeles Chargers' : 'LAC', 'Denver Broncos' : 'DEN', 'Las Vegas Raiders' : 'LV',
'Baltimore Ravens' : 'BAL', 'Cincinnati Bengals' : 'CIN', 'Cleveland Browns' : 'CLE', 'Pittsburgh Steelers' : 'PIT',
'Houston Texans' : 'HOU', 'Indianapolis Colts' : 'IND', 'Jacksonville Jaguars' : 'JAX', 'Tennessee Titans' : 'TEN',
'New England Patriots' : 'NE', 'New York Jets' : 'NYJ', 'Miami Dolphins' : 'MIA', 'Buffalo Bills' : 'BUF',
'Detroit Lions' : 'DET', 'Green Bay Packers' : 'GB', 'Chicago Bears' : 'CHI', 'Minnesota Vikings' : 'MIN',
'Dallas Cowboys' : 'DAL', 'New York Giants' : 'NYG', 'Philadelphia Eagles' : 'PHI', 'Washington Commanders' : 'WAS',
'Atlanta Falcons' : 'ATL', 'New Orleans Saints' : 'NO', 'Carolina Panthers' : 'CAR', 'Tampa Bay Buccaneers' : 'TB',
'Arizona Cardinals' : 'ARI', 'San Francisco 49ers' : 'SF', 'Seattle Seahawks' : 'SEA', 'Los Angeles Rams' : 'LAR'}

nfl_df = pd.read_csv('data/processed_data/nfl_live/nfl_current_trimmed.csv')
data = pd.read_csv('data/raw_data/nfl-2023-raw.csv')

cumulative = pd.DataFrame(columns=['date', 'season', 'location', 'team1', 'team2', 'team1winrate', 'team2winrate', 'result', 'prediction'])


teams = nfl_df['team1'].to_list()
teams = list(set(teams))

def weekly_winrate_prediction_accuracy (week_num):
    next_dates = data.loc[data['Round Number'] == week_num + 1]
    next_dates[['Date', 'Time']] = next_dates['Date'].str.split(' ', expand=True)
    next_dates[['Day', 'Month', 'Year']] = next_dates['Date'].str.split('/', expand=True)
    next_dates['Date'] = next_dates[['Year', 'Month', 'Day']].apply(lambda x: '-'.join(str(value) for value in x), axis=1)
    next_max_date = max(next_dates['Date'])

    winrates = {}
    for team in teams:
        nfl_winrate_sequence = get_cumulative_winrate_sequence(nfl_df, 2023, team, next_max_date)
        curr_winrate = nfl_winrate_sequence['winrate'].iloc[-1]
        winrates[team] = round(curr_winrate, 3)

    curr_dates = data.loc[data['Round Number'] == week_num]
    curr_dates[['Date', 'Time']] = curr_dates['Date'].str.split(' ', expand=True)
    curr_dates[['Day', 'Month', 'Year']] = curr_dates['Date'].str.split('/', expand=True)
    curr_dates['Date'] = curr_dates[['Year', 'Month', 'Day']].apply(lambda x: '-'.join(str(value) for value in x), axis=1)

    min_date = min(curr_dates['Date'])
    max_date = max(curr_dates['Date'])

    week = nfl_df.loc[nfl_df['date'] <= max_date]
    week = week.loc[week['date'] >= min_date]

    week['team1winrate'] = week['team1']
    week.replace({"team1winrate": winrates}, inplace = True)
    week['team2winrate'] = week['team2']
    week.replace({"team2winrate": winrates}, inplace = True)

    week['prediction'] = week['team1winrate']/(week['team1winrate'] + week['team2winrate'])
    week = week[['date', 'season', 'location', 'team1', 'team2', 'team1winrate', 'team2winrate', 'result', 'prediction']]
    week = get_prediction_metric_accuracy(week, prob_column_name='prediction')

    return week

for i in range(1, 8, 1):
    week = weekly_winrate_prediction_accuracy(i)
    cumulative = pd.concat([cumulative, week] , axis=0)

cumulative.to_csv('data/processed_data/nfl_live/nfl_cumulative_testing.csv', index=False)





