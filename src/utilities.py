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

    # note that the returned dataframe still calls has the column as 'team1'
    return filtered_df



# GET_WINRATE
# takes a dataframe with columns [season, team1] and returns a dataframe with
# columns [team, season, winrate] which act as youd expect. you likely want to run 
# get_flipped_data_appended before running this function, as that will yield
# full season winrate instead of home/away winrate
#
# optional modified boolean if you desire a modified winrate
def get_winrate(df, seasons, teams=None, modified=False):

    seasons_dataframes = []

    if(type(seasons) == int):
        seasons_dataframes.append(get_filtered_data(df, seasons=seasons, teams=teams))
    else:
        for season in seasons:
            seasons_dataframes.append(get_filtered_data(df, season, teams=teams))
    
    final_dataframe = pd.DataFrame(columns=['team', 'season', 'winrate'])
    
    for data in seasons_dataframes:
        team_to_wins = {}
        team_to_losses = {}
        season = data.iloc[0]['season']

        for ind in data.index:
            if(data['result'][ind] == 1):
                team_to_wins[data['team1'][ind]] = team_to_wins.get(data['team1'][ind], 0) + 1
            if(data['result'][ind] == 0):
                team_to_losses[data['team1'][ind]] = team_to_losses.get(data['team1'][ind], 0) + 1

        teams = set(team_to_wins.keys()).union(set(team_to_losses.keys()))
       
       
        for team in teams:
            new_row = {'team': team, 'season': season, 
                'winrate': (team_to_wins[team] + int(modified)) / (team_to_wins[team] + team_to_losses[team] + int(modified) * 2)}
            to_append = pd.DataFrame(new_row, index=[0])
            final_dataframe = pd.concat([final_dataframe, to_append],ignore_index=True)
            
    return final_dataframe

#data = pd.read_csv('../data/processed_data/generic_mlb_data.csv')
#print(get_winrate(data, 2021, modified=True).head())


    
