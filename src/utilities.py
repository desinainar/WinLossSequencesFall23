import pandas as pd
# various utilities to be used throughout the repository 


# GET_FLIPPED_DATA
# takes a dataframe with columns [location, team1, team2, score1, score2, result]
# and returns a dataframe with the teams & scores flipped and locations & results switched
def get_flipped_data(df):
    
    flipped_data = df.copy()

    # reassign who is team1
    flipped_data.rename(columns={'team1': 'team2', 'team2': 'team1', 'score1': 'score2', 'score2': 'score1'}, inplace=True)

    # these lambda functions simply change location and result as expected (home becomes away, loss becomes win, etc.)
    flipped_data['location'] = flipped_data['location'].apply(lambda x: 'A' if x == 'H' else 'H' if x == 'A' else 'N')
    flipped_data['result'] = flipped_data['result'].apply(lambda x: 1.0 if x == 0.0 else 0.0 if x == 1.0 else 0.5)

    # order them as desired
    flipped_data = flipped_data[['date', 'season', 'location', 'team1', 'team2', 'score1', 'score2', 'result']]

    return flipped_data



# GET_FLIPPED_DATA_APPENDED
# takes a dataframe with columns [location, team1, team2, score1, score2, result]
# and returns a dataframe with the original data as well as 
# appended entries with the teams & scores flipped and locations & results switched
def get_flipped_data_appended(df):

    return pd.concat([df, get_flipped_data(df)])



# GET_FILTERED_DATA
# takes a dataframe with columns [season, team1] and returns
# a dataframe that is filtered by the team(s) and season(s)
#
# you may pass season as a single int or a list of int
# you may pass teams as a single str or a list of str
def get_filtered_data(df, seasons=None, teams=None):
    
    # filter the data
    filtered_df = df.copy()

    if(type(teams) == str):
        temp = []
        temp.append(teams)
        teams = temp

    if(type(seasons) == int):
        temp = []
        temp.append(seasons)
        seasons = temp

    if(type(seasons) == list):
        filtered_df = filtered_df[filtered_df['season'].isin(seasons)]

    if(type(teams) == list):
        filtered_df = filtered_df[filtered_df['team1'].isin(teams)]

    return filtered_df
    


    
