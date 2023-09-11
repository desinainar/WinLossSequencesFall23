# various utilities to be used throughout the repository 
import pandas as pd
# takes a dataframe with columns [location, team1, team2, score1, score2, result]
# and returns a dataframe with the teams & scores flipped and locations & results switched
def return_flipped_data(df):
    
    flipped_data = df.copy()

    # reassign who is team1
    flipped_data.rename(columns={'team1': 'team2', 'team2': 'team1', 'score1': 'score2', 'score2': 'score1'}, inplace=True)

    # these lambda functions simply change location and result as expected (home becomes away, loss becomes win, etc.)
    flipped_data['location'] = flipped_data['location'].apply(lambda x: 'A' if x == 'H' else 'H' if x == 'A' else 'N')
    flipped_data['result'] = flipped_data['result'].apply(lambda x: 1.0 if x == 0.0 else 0.0 if x == 1.0 else 0.5)

    # order them as desired
    flipped_data = flipped_data[['date', 'season', 'location', 'team1', 'team2', 'score1', 'score2', 'result']]

    return flipped_data



