import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

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

nfl_cumulative = pd.DataFrame(columns=['date', 'season', 'location', 'team1', 'team2', 'team1winrate', 'team2winrate', 'result', 'prediction'])
epl_cumulative = pd.DataFrame(columns=['date', 'season', 'location', 'team1', 'team2', 'team1winrate', 'team2winrate', 'result', 'prediction'])


nfl_df = pd.read_csv('data/processed_data/nfl_live/nfl_current_trimmed.csv')
nfl_raw_data = pd.read_csv('data/raw_data/nfl-2023-raw.csv')
nfl_teams = nfl_df['team1'].to_list()
nfl_teams = list(set(nfl_teams))

epl_df = pd.read_csv('data/processed_data/epl_live/epl_current_trimmed.csv')
epl_raw_data = pd.read_csv('data/raw_data/epl_current.csv')
epl_teams = epl_df['team1'].to_list()
epl_teams = list(set(epl_teams))


def weekly_winrate_prediction_accuracy (week_num, data, df, teams):
    next_dates = data.loc[data['Round Number'] == week_num + 1]
    next_dates[['Date', 'Time']] = next_dates['Date'].str.split(' ', expand=True)
    next_dates[['Day', 'Month', 'Year']] = next_dates['Date'].str.split('/', expand=True)
    next_dates['Date'] = next_dates[['Year', 'Month', 'Day']].apply(lambda x: '-'.join(str(value) for value in x), axis=1)
    next_max_date = max(next_dates['Date'])

    winrates = {}
    for team in teams:
        winrate_sequence = get_cumulative_winrate_sequence(df, 2023, team, next_max_date)
        curr_winrate = winrate_sequence['winrate'].iloc[-1]
        winrates[team] = round(curr_winrate, 3)

    curr_dates = data.loc[data['Round Number'] == week_num]
    curr_dates[['Date', 'Time']] = curr_dates['Date'].str.split(' ', expand=True)
    curr_dates[['Day', 'Month', 'Year']] = curr_dates['Date'].str.split('/', expand=True)
    curr_dates['Date'] = curr_dates[['Year', 'Month', 'Day']].apply(lambda x: '-'.join(str(value) for value in x), axis=1)

    min_date = min(curr_dates['Date'])
    max_date = max(curr_dates['Date'])

    week = df.loc[df['date'] <= max_date]
    week = week.loc[week['date'] >= min_date]

    week['team1winrate'] = week['team1']
    week.replace({"team1winrate": winrates}, inplace = True)
    week['team2winrate'] = week['team2']
    week.replace({"team2winrate": winrates}, inplace = True)

    week['prediction'] = week['team1winrate']/(week['team1winrate'] + week['team2winrate'])
    week = week[['date', 'season', 'location', 'team1', 'team2', 'team1winrate', 'team2winrate', 'result', 'prediction']]
    week = get_prediction_metric_accuracy(week, prob_column_name='prediction')

    return week

nfl_correct_prediction = []
epl_correct_prediction = []
epl_no_draws = []

for i in range(1, 9, 1):
    week = weekly_winrate_prediction_accuracy(i, nfl_raw_data, nfl_df, nfl_teams)
    nfl_correct_prediction.append(sum(week['accuracy']) / len(week['accuracy']))
    nfl_cumulative = pd.concat([nfl_cumulative, week] , axis=0)

nfl_cumulative.to_csv('data/processed_data/nfl_live/nfl_cumulative_testing.csv', index=False)

for j in range(1, 11, 1):
    week = weekly_winrate_prediction_accuracy(j, epl_raw_data, epl_df, epl_teams)
    week_no_draws = week[week['accuracy'] != 0.5]
    epl_correct_prediction.append(sum(week['accuracy']) / len(week['accuracy']))
    epl_no_draws.append(sum(week_no_draws['accuracy']) / len(week_no_draws['accuracy']))
    epl_cumulative = pd.concat([epl_cumulative, week] , axis=0)

epl_cumulative.to_csv('data/processed_data/epl_live/epl_cumulative_testing.csv', index=False)
#print(epl_correct_prediction)
print(epl_no_draws)

  
# define data values 
x = np.array([1, 2, 3, 4, 5, 6, 7, 8])  # X-axis points 
y = nfl_correct_prediction  # Y-axis points

x2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
x3 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y2 = epl_correct_prediction
y3 = epl_no_draws
  
plt.plot(x, y, label = "NFL")
plt.plot(x2, y2, label = "EPL") 
plt.plot(x3, y3, label = "EPL (Draws Excluded)") 
plt.xlabel("Week")  # add X-axis label 
plt.ylabel("Prediction Accuracy")  # add Y-axis label 
plt.title("Weekly Accuracy")  # add title
plt.ylim(0, 1.1) 
plt.legend()
plt.show()







