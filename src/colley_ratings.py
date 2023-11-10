import penaltyblog as pb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from utilities import *

nfl_df = pd.read_csv('data/processed_data/nfl_live/nfl_current_trimmed.csv')
nfl_raw_data = pd.read_csv('data/raw_data/nfl-2023-raw.csv')

def colley_predictions (week_num, data, df):
    colley = pb.ratings.Colley(df["score1"], df["score2"], df["team1"], df["team2"])
    ratings = colley.get_ratings() 
    ratings = ratings.set_index('team').to_dict()['rating']

    curr_dates = data.loc[data['Round Number'] == week_num]
    curr_dates[['Date', 'Time']] = curr_dates['Date'].str.split(' ', expand=True)
    curr_dates[['Day', 'Month', 'Year']] = curr_dates['Date'].str.split('/', expand=True)
    curr_dates['Date'] = curr_dates[['Year', 'Month', 'Day']].apply(lambda x: '-'.join(str(value) for value in x), axis=1)

    min_date = min(curr_dates['Date'])
    max_date = max(curr_dates['Date'])

    week = df.loc[df['date'] <= max_date]
    week = week.loc[week['date'] >= min_date]

    week['team1_colleyrating'] = week['team1']
    week.replace({"team1_colleyrating": ratings}, inplace = True)
    week['team2_colleyrating'] = week['team2']
    week.replace({"team2_colleyrating": ratings}, inplace = True)

    week['prediction'] = np.where((week['team1_colleyrating'] > week['team2_colleyrating']), 1, 0)
    week = week[['date', 'season', 'location', 'team1', 'team2', 'team1_colleyrating', 'team2_colleyrating', 'result', 'prediction']]
    week = get_prediction_metric_accuracy(week, prob_column_name='prediction')

    return week

nfl_cumulative = pd.DataFrame(columns=['date', 'season', 'location', 'team1', 'team2', 'team1_colleyrating', 'team2_colleyrating', 'result', 'prediction'])
nfl_correct_prediction = []

for i in range(1, 9, 1):
    week = colley_predictions(i, nfl_raw_data, nfl_df)
    nfl_correct_prediction.append(sum(week['accuracy']) / len(week['accuracy']))
    nfl_cumulative = pd.concat([nfl_cumulative, week] , axis=0)

nfl_cumulative.to_csv('data/processed_data/nfl_live/nfl_colley.csv', index=False)

colley = pb.ratings.Colley(nfl_df["score1"], nfl_df["score2"], nfl_df["team1"], nfl_df["team2"])
ratings = colley.get_ratings() 	
print(ratings)


x = np.array([1, 2, 3, 4, 5, 6, 7, 8]) 
y = nfl_correct_prediction
plt.plot(x, y, label = "NFL")
plt.xlabel("Week")  # add X-axis label 
plt.ylabel("Prediction Accuracy")  # add Y-axis label 
plt.title("Weekly Accuracy")  # add title
plt.ylim(0, 1) 
plt.legend()
plt.show()
