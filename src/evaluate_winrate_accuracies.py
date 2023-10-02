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

def initialize_dictionary(df, dictionary):
    for index in df.index:
        dictionary[ (df['team1'][index], df['season'][index]) ] = df['winrate'][index]
    
def map_row_to_probability(row):
     return team_season_pair_to_winrate[(row['team1'], row['season'])] / (team_season_pair_to_winrate[(row['team1'], row['season'])] + team_season_pair_to_winrate[(row['team2'], row['season'])] )
    
def get_foresight_prediction(df):
    """
    the clairvoyant method 
    """
    df['implied_probability'] = df.apply(map_row_to_probability, axis = 1)

    return df
    
def get_hindsight_prediction(df):
    """
    the past-season method
    """

def get_running_winrate_prediction():
    """
    averages past-season winrate and running tally current-season winrate
    """


# evaluate for MLB
# team_season_pair_to_winrate = {}
# initialize_dictionary(mlb_winrate_dataframe, team_season_pair_to_winrate)
# winrate_df = get_foresight_prediction(mlb_df)
# prediction_df = utilities.get_prediction_metric_accuracy(winrate_df)
# utilities.get_filtered_data(prediction_df, seasons=list(range(1800, 2023))).to_csv('mlb_output.csv', index=False)

# evaluate for NHL
# team_season_pair_to_winrate = {}
# initialize_dictionary(nhl_winrate_dataframe, team_season_pair_to_winrate)
# winrate_df = get_foresight_prediction(nhl_df)
# prediction_df = utilities.get_prediction_metric_accuracy(winrate_df)
# utilities.get_filtered_data(prediction_df, seasons=list(range(1800, 2023))).to_csv('nhl_output.csv', index=False)

# evaluate for NFL
# team_season_pair_to_winrate = {}
# initialize_dictionary(nfl_winrate_dataframe, team_season_pair_to_winrate)
# winrate_df = get_foresight_prediction(nfl_df)
# prediction_df = utilities.get_prediction_metric_accuracy(winrate_df)
# utilities.get_filtered_data(prediction_df, seasons=list(range(1800, 2023))).to_csv('nfl_output.csv', index=False)

# evaluate for NBA
# team_season_pair_to_winrate = {}
# initialize_dictionary(nba_winrate_dataframe, team_season_pair_to_winrate)
# winrate_df = get_foresight_prediction(nba_df)
# prediction_df = utilities.get_prediction_metric_accuracy(winrate_df)
# utilities.get_filtered_data(prediction_df, seasons=list(range(1800, 2023))).to_csv('nba_output.csv', index=False)


