import utilities
import pandas as pd

mlb_winrate_dataframe = pd.read_csv('..\data\processed_data\mlb_adjusted_winrates.csv').rename(columns={'team': 'team1'})

team_season_pair_to_winrate = {}

def initialize_dictionary(df, dictionary):
    for index in df.index:
        dictionary[ (df['team1'][index], df['season'][index]) ] = df['winrate'][index]
    
def map_row_to_probability(row):
     return team_season_pair_to_winrate[(row['team1'], row['season'])] / (team_season_pair_to_winrate[(row['team1'], row['season'])] + team_season_pair_to_winrate[(row['team2'], row['season'])] )
    

def get_foresight_prediction(df):
    """
    the clairvoyant method 
    """
    initialize_dictionary(mlb_winrate_dataframe, team_season_pair_to_winrate)

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

#df = pd.read_csv('../data/processed_data/generic_mlb_data_flipped.csv')
#winrate_df = get_foresight_prediction(df)
#prediction_df = utilities.get_prediction_metric_accuracy(winrate_df)
#utilities.get_filtered_data(prediction_df, seasons=list(range(1800, 2023))).to_csv('output.csv')

df = pd.read_csv('output.csv')
print("accuracy")
print(df['accuracy'].sum() / len(df))
