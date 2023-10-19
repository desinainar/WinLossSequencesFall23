import utilities
import pandas as pd

mlb_winrate_dataframe = pd.read_csv('..\data\processed_data\mlb\mlb_adjusted_winrates.csv').rename(columns={'team': 'team1'})
nhl_winrate_dataframe = pd.read_csv('..\data\processed_data/nhl/nhl_adjusted_winrates.csv').rename(columns={'team': 'team1'})
nfl_winrate_dataframe = pd.read_csv('..\data\processed_data/nfl_historical/nfl_adjusted_winrates.csv').rename(columns={'team': 'team1'})
nba_winrate_dataframe = pd.read_csv('..\data\processed_data/nba/nba_adjusted_winrates.csv').rename(columns={'team': 'team1'})


mlb_df = pd.read_csv('../data/processed_data/mlb/generic_mlb_data_flipped.csv')
nhl_df = pd.read_csv('../data/processed_data/nhl/generic_nhl_data_flipped.csv')
nfl_df = pd.read_csv('../data/processed_data/nfl_historical/generic_nfl_data_flipped.csv')
nba_df = pd.read_csv('../data/processed_data/nba/generic_nba_data_flipped.csv')

team_season_pair_to_winrate = {}

def initialize_dictionary(df, dictionary):
    for index in df.index:
        dictionary[ (df['team1'][index], df['season'][index]) ] = df['winrate'][index]
    
def map_row_to_probability_hindsight(row):
     return team_season_pair_to_winrate[(row['team1'], row['season'])] / (team_season_pair_to_winrate[(row['team1'], row['season'])] + team_season_pair_to_winrate[(row['team2'], row['season'])] )
    
def map_row_to_probability_foresight(row):
     return team_season_pair_to_winrate[(row['team1'], row['season'] - 1)] / (team_season_pair_to_winrate[(row['team1'], row['season'] - 1)] + team_season_pair_to_winrate[(row['team2'], row['season'] - 1)] )

def get_hindsight_prediction(df):
    """
    the clairvoyant method 
    """
    df['implied_probability'] = df.apply(map_row_to_probability_hindsight, axis = 1)

    return df
    
def get_foresight_prediction(df):
    """
    the past-season method
    """
    filtered_df = df.copy()
    for index, row in filtered_df.iterrows():
       print(index)
       try:
           map_row_to_probability_foresight(row)
       except:
           filtered_df = filtered_df.drop(index = index)
    
    filtered_df['implied_probability'] = filtered_df.apply(map_row_to_probability_foresight, axis = 1)

    return filtered_df


def get_running_winrate_prediction(data, season):
    """
    uses running tally of winrate
    """

    df = data.copy()

    prob_list = []

    for ind in df.index:
        team1_winrate = utilities.get_cumulative_winrate(df, season, df['team1'][ind], str(pd.to_datetime(df['date'][ind]) + pd.Timedelta(days = -1)))
        team2_winrate = utilities.get_cumulative_winrate(df, season, df['team2'][ind], str(pd.to_datetime(df['date'][ind]) + pd.Timedelta(days = -1)))
        if not (team1_winrate.empty or team2_winrate.empty):
            probability = team1_winrate['winrate'] / (team1_winrate['winrate'] + team2_winrate['winrate'])
            prob_list.append(float(probability))
        else:
            prob_list.append(-1)

    df['prob'] = prob_list
    indexDrop = df[ (df['prob'] < 0)].index
    df.drop(indexDrop , inplace=True)
    accuracy_df = utilities.get_prediction_metric_accuracy(df)
    print(accuracy_df['accuracy'].sum() / len(accuracy_df))


# evaluate hindsight for MLB
# team_season_pair_to_winrate = {}
# initialize_dictionary(mlb_winrate_dataframe, team_season_pair_to_winrate)
# winrate_df = get_hindsight_prediction(mlb_df)
# prediction_df = utilities.get_prediction_metric_accuracy(winrate_df)
# utilities.get_filtered_data(prediction_df, seasons=list(range(1800, 2023))).to_csv('mlb_output.csv', index=False)

# evaluate hindsight for NHL
# team_season_pair_to_winrate = {}
# initialize_dictionary(nhl_winrate_dataframe, team_season_pair_to_winrate)
# winrate_df = get_hindsight_prediction(nhl_df)
# prediction_df = utilities.get_prediction_metric_accuracy(winrate_df)
# utilities.get_filtered_data(prediction_df, seasons=list(range(1800, 2023))).to_csv('nhl_output.csv', index=False)

# evaluate hindsight for NFL
# team_season_pair_to_winrate = {}
# initialize_dictionary(nfl_winrate_dataframe, team_season_pair_to_winrate)
# winrate_df = get_hindsight_prediction(nfl_df)
# prediction_df = utilities.get_prediction_metric_accuracy(winrate_df)
# utilities.get_filtered_data(prediction_df, seasons=list(range(1800, 2023))).to_csv('nfl_output.csv', index=False)

# evaluate hindsight for NBA
# team_season_pair_to_winrate = {}
# initialize_dictionary(nba_winrate_dataframe, team_season_pair_to_winrate)
# winrate_df = get_hindsight_prediction(nba_df)
# prediction_df = utilities.get_prediction_metric_accuracy(winrate_df)
# utilities.get_filtered_data(prediction_df, seasons=list(range(1800, 2023))).to_csv('nba_output.csv', index=False)

# evaluate hindsight for MLB
# team_season_pair_to_winrate = {}
# initialize_dictionary(mlb_winrate_dataframe, team_season_pair_to_winrate)
# winrate_df = get_foresight_prediction(mlb_df)
# prediction_df = utilities.get_prediction_metric_accuracy(winrate_df)
# utilities.get_filtered_data(prediction_df, seasons=list(range(1800, 2023))).to_csv('mlb_output.csv', index=False)

# # evaluate hindsight for NHL
# team_season_pair_to_winrate = {}
# initialize_dictionary(nhl_winrate_dataframe, team_season_pair_to_winrate)
# winrate_df = get_foresight_prediction(nhl_df)
# prediction_df = utilities.get_prediction_metric_accuracy(winrate_df)
# utilities.get_filtered_data(prediction_df, seasons=list(range(1800, 2023))).to_csv('nhl_output.csv', index=False)

# # evaluate foresight for NFL
# team_season_pair_to_winrate = {}
# initialize_dictionary(nfl_winrate_dataframe, team_season_pair_to_winrate)
# winrate_df = get_foresight_prediction(nfl_df)
# prediction_df = utilities.get_prediction_metric_accuracy(winrate_df)
# utilities.get_filtered_data(prediction_df, seasons=list(range(1800, 2023))).to_csv('nfl_output.csv', index=False)

# # evaluate hindsight for NBA
# team_season_pair_to_winrate = {}
# initialize_dictionary(nba_winrate_dataframe, team_season_pair_to_winrate)
# winrate_df = get_foresight_prediction(nba_df)
# prediction_df = utilities.get_prediction_metric_accuracy(winrate_df)
# utilities.get_filtered_data(prediction_df, seasons=list(range(1800, 2023))).to_csv('nba_output.csv', index=False)

# mlb_hindsight_accuracies = pd.read_csv('..\data\processed_data\mlb\mlb_hindsight_accuracy.csv')
# nba_hindsight_accuracies = pd.read_csv('..\data\processed_data/nba/nba_hindsight_accuracy.csv')
# nhl_hindsight_accuracies = pd.read_csv('..\data\processed_data/nhl/nhl_hindsight_accuracy.csv')
# nfl_hindsight_accuracies = pd.read_csv('..\data\processed_data/nfl_historical/nfl_hindsight_accuracy.csv')

# nfl_foresight_accuracies = pd.read_csv('..\data\processed_data/nfl_historical/nfl_foresight_accuracy.csv')
# nba_foresight_accuracies = pd.read_csv('..\data\processed_data/nba/nba_foresight_accuracy.csv')
# nhl_foresight_accuracies = pd.read_csv('..\data\processed_data/nhl/nhl_foresight_accuracy.csv')
# mlb_foresight_accuracies = pd.read_csv('..\data\processed_data/mlb/mlb_foresight_accuracy.csv')


# print()
# print("MLB hindsight Accuracy")
# print(mlb_foresight_accuracies['accuracy'].sum()/len(mlb_foresight_accuracies))
# print()
# print("NBA hindsight Accuracy")
# print(nba_foresight_accuracies['accuracy'].sum()/len(nba_foresight_accuracies))
# print()
# print("NHL hindsight Accuracy")
# print(nhl_foresight_accuracies['accuracy'].sum()/len(nhl_foresight_accuracies))
# print()
# print("NFL hindsight Accuracy")
# print(nfl_foresight_accuracies['accuracy'].sum()/len(nfl_foresight_accuracies))
# print()

#get_running_winrate_prediction(nfl_df, 2022)