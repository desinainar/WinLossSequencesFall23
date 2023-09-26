import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
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

    # note that the returned dataframe still uses the column name 'team1'
    return filtered_df



# GET_WINRATE
# takes a dataframe with columns [season, team1] and returns a dataframe with
# columns [season, team, winrate] which act as youd expect
#
# optional adjusted boolean if you desire a adjusted winrate
def get_winrate(df, seasons=None, teams=None, adjusted=True):
    
    to_return = pd.DataFrame(columns=['season', 'team', 'winrate'])
    years = get_filtered_data(df, seasons, teams)['season'].unique()
    seasonal_dataframes = {}

    # i dont like this loop - matthew
    for year in years:
        # the unique() function returns a numpy int, perhaps adjust get_filtered_data
        # to account for this, to avoid casting here and elsewhere
        seasonal_dataframes[year] = get_filtered_data(df, seasons=int(year), teams=teams)

    to_append = []

    for year in years:
        team_to_wins = {}
        team_to_losses = {}

        for index, row in seasonal_dataframes[year].iterrows():
            if(row['result'] == 0):
                team_to_losses[row['team1']] = team_to_losses.get(row['team1'], 0) + 1
            if(row['result'] == 1):
                team_to_wins[row['team1']] = team_to_wins.get(row['team1'], 0) + 1
        
        teams = set(team_to_wins.keys()).union(set(team_to_losses.keys()))
        for team in teams:
            to_append = {'season': year, 'team': team, 
                         'winrate': (team_to_wins.get(team, 0) + int(adjusted)) / 
                         (team_to_losses.get(team, 0) + team_to_wins.get(team, 0) + (2 * int(adjusted)))}
            to_return = to_return.append(to_append, ignore_index=True)

    return to_return

