from utilities import *
from colley_ratings import *
from cumulative_scripts import *
from massey_ratings import *

nfl_df = pd.read_csv('data/processed_data/nfl_live/nfl_current_trimmed.csv')
nfl_raw_data = pd.read_csv('data/raw_data/nfl-2023-raw.csv')
nfl_teams = nfl_df['team1'].to_list()
nfl_teams = list(set(nfl_teams))

epl_df = pd.read_csv('data/processed_data/epl_live/epl_current_trimmed.csv')
epl_raw_data = pd.read_csv('data/raw_data/epl_current.csv')
epl_teams = epl_df['team1'].to_list()
epl_teams = list(set(epl_teams))

nfl_colley_prediction = []
epl_colley_prediction = []
nfl_massey_prediction = []
epl_massey_prediction = []
nfl_winrate_prediction = []
epl_winrate_prediction = []

for i in range(1, 9, 1):
    week_c = colley_predictions(i, nfl_raw_data, nfl_df)
    week_m = massey_predictions(i, nfl_raw_data, nfl_df)
    week_w = weekly_winrate_prediction_accuracy(i, nfl_raw_data, nfl_df, nfl_teams)
    nfl_colley_prediction.append(sum(week_c['accuracy']) / len(week_c['accuracy']))
    nfl_massey_prediction.append(sum(week_m['accuracy']) / len(week_m['accuracy']))
    nfl_winrate_prediction.append(sum(week_w['accuracy']) / len(week_w['accuracy']))

for i in range(1, 11, 1):
    week_c = colley_predictions(i, epl_raw_data, epl_df)
    week_m = massey_predictions(i, epl_raw_data, epl_df)
    week_w = weekly_winrate_prediction_accuracy(i, epl_raw_data, epl_df, epl_teams)
    epl_colley_prediction.append(sum(week_c['accuracy']) / len(week_c['accuracy']))
    epl_massey_prediction.append(sum(week_m['accuracy']) / len(week_m['accuracy']))
    epl_winrate_prediction.append(sum(week_w['accuracy']) / len(week_w['accuracy']))


x1 = np.array([1, 2, 3, 4, 5, 6, 7, 8]) 
x2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) 
y1 = nfl_colley_prediction
y2 = nfl_massey_prediction
y3 = nfl_winrate_prediction
y4 = epl_colley_prediction
y5 = epl_massey_prediction
y6 = epl_winrate_prediction

plt.plot(x1, y1, label = "NFL (Colley)")
plt.plot(x1, y2, label = "NFL (Massey)") 
#plt.plot(x1, y3, label = "NFL (Adj. Winrate)") 
plt.plot(x2, y4, label = "EPL (Colley)")
plt.plot(x2, y5, label = "EPL (Massey)") 
#plt.plot(x2, y6, label = "EPL (Adj. Winrate)") 
plt.xlabel("Week")  # add X-axis label 
plt.ylabel("Prediction Accuracy")  # add Y-axis label 
plt.title("Weekly Accuracy")  # add title
plt.ylim(0, 1.1) 
plt.legend()
plt.show()