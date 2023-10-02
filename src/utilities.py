import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) # fix usage of _append before we can remove this
import pandas as pd

def get_flipped_data(df):
    """
    get_flipped_data takes a dataframe and returns a dataframe with ONLY 'flipped' entries

    Params:
    df: a pandas dataframe with columns [location, team1, team2, score1, score2, result]

    Returns: a pandas dataframe with flipped entries  
    """
    flipped_data = df.copy()

    # reassign who is team1 
    flipped_data.rename(columns={'team1': 'team2', 'team2': 'team1', 'score1': 'score2', 'score2': 'score1'}, inplace=True)

    # these lambda functions simply change location and result as expected (home becomes away, loss becomes win, etc.)
    flipped_data['location'] = flipped_data['location'].apply(lambda x: 'A' if x == 'H' else 'H' if x == 'A' else 'N')
    flipped_data['result'] = flipped_data['result'].apply(lambda x: 1.0 if x == 0.0 else 0.0 if x == 1.0 else 0.5)

    # order them as desired
    flipped_data = flipped_data[['date', 'season', 'location', 'team1', 'team2', 'score1', 'score2', 'result']]

    return flipped_data


def get_flipped_data_appended(df):
    """
    get_flipped_data_appended takes a dataframe and returns a dataframe with BOTH original and flipped entries

    Params:
    df: a pandas dataframe with columns [location, team1, team2, score1, score2, result]
    
    Returns: a pandas dataframe with both original and flipped entries 
    """
    return pd.concat([df, get_flipped_data(df)])


def get_filtered_data(df, seasons=None, teams=None):
    """
    get_filtered_data is a function to filter data by season(s) and team(s)

    Params:
    df: a pandas dataframe with columns [season, team1]
    seasons: None (all seasons), an int representing a single season, or a list of ints for multiple seasons
    teams: None (all teams), a string representing a single team abbreviation, or a list of strings for multiple teams

    Returns: a pandas dataframe filtered as desired
    """
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


def get_season_winrate(df, seasons=None, teams=None, adjusted=True):
    """
    get_season_winrate calculates season-long winrates from a dataframe

    Params:
    df: a pandas dataframe with columns [season, team1, result]
    seasons: None (all seasons), an int representing a single season, or a list of ints for multiple seasons
    teams: None (all teams), a string representing a single team abbreviation, or a list of strings for multiple teams
    adjusted: a boolean for changing between adjusted (True) and raw (False) winrate

    Returns: a pandas dataframe with columns [season, team, winrate] 
    """
    
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

        # there are weird edge cases in the NFL where teams exist that have only ever DRAWN. this fixes that
        teams_who_tied = set()

        for index, row in seasonal_dataframes[year].iterrows():
            if(row['result'] == 0):
                team_to_losses[row['team1']] = team_to_losses.get(row['team1'], 0) + 1
            if(row['result'] == 1):
                team_to_wins[row['team1']] = team_to_wins.get(row['team1'], 0) + 1
            if(row['result'] == 0.5):
                teams_who_tied.add(row['team1'])
        
        teams = (set(team_to_wins.keys()).union(set(team_to_losses.keys()))).union(teams_who_tied)
        for team in teams:
            to_append = {'season': year, 'team': team, 
                         'winrate': (team_to_wins.get(team, 0) + int(adjusted)) / 
                         (team_to_losses.get(team, 0) + team_to_wins.get(team, 0) + (2 * int(adjusted)))}
            to_return = to_return._append(to_append, ignore_index=True)

    return to_return


def get_cumulative_winrate(df, season, team, date):
    """
    get_cumulative_winrate calculates winrates within a season up to a specified date

    TODO: account for double headers

    Params:
    df: a pandas dataframe containing columns [date, season, team1, result]
    season: an int representing the desired season
    team: a string with the desired team's abbreviation
    date: a string in "YYYY-MM-DD" format which you want to calculate the cumulative winrate up to

    Returns: a pandas dataframe with columns [season, team, winrate, date] and only one entry
    """
    filtered_data = get_filtered_data(df, seasons=season, teams=team)
    filtered_data = filtered_data.loc[filtered_data['date'] <= date]
    filtered_data = get_season_winrate(filtered_data)
    date_column = [date]
    filtered_data['date'] = date_column
    return filtered_data


def get_cumulative_winrate_sequence(df, season, team, date=None):
    """
    get_cumulative_winrate_sequence calculates a sequence of cumulative winrates up to a specified date

    TODO: account for double headers

    Params:
    df: a pandas dataframe containing columns [date, season, team1, result]
    season: an int representing the desired season
    team: a string with the desired team's abbreviation
    date: a string in "YYYY-MM-DD" format which you want to calculate the cumulative winrate sequence up to

    Returns: a pandas dataframe with columns [season, team, winrate, date] with entries for played game up to date
    """
    if(date == None):
        # this is a bit of a hack but its foolproof for about 8000 more years
        date = '9999-12-31'

    filtered_data = get_filtered_data(df, seasons=season, teams=team)
    #redundant line copied over from get_cumulative_winrate, maybe can be changed for effeciency
    filtered_data = filtered_data.loc[filtered_data['date'] <= date]

    date_to_rate = {}

    for d in filtered_data['date'].unique():
        date_to_rate[str(d)] = float(get_cumulative_winrate(df, season, team, d)['winrate'])

    to_return = pd.DataFrame(columns=['date', 'winrate'])

    #wildly inefficient reiteration over the data but it works
    for k in date_to_rate.keys():
        to_dataframe = {}
        to_dataframe['date'] = k
        to_dataframe['winrate'] = date_to_rate[k]
        to_return = to_return._append(to_dataframe, ignore_index=True)

    return to_return.sort_values(by=['date']).reset_index().drop(columns=['index'])


def get_prediction_metric_accuracy(df, prob_column_name=None):
    """
    get_prediction_metric_accuracy evaluates the accuracy of predictions in predicting results in data

    Params:
    df: a pandas dataframe containing column [results] AND an arbitraily named column with prediction probabilities
    prob_column_name: a string with the name of the column in df where prediction probabilties are, or None (rightmost df column)

    Returns: a dataframe with the same entries as df, with an extra "accuracy" column calculated and appended
    """
    # if no column name specified, assume it is last column
    if prob_column_name == None:
        prob_column = df.iloc[:,-1:]
    else:
        prob_column = df[prob_column_name]

    correctness = []

    for index in df.index:
        if(prob_column.iloc[:,0][index] > 0.5):
            correctness.append(df['result'][index])
        elif(prob_column.iloc[:,0][index] < 0.5):
            correctness.append(abs(df['result'][index] - 1))
        else:
            correctness.append(0.5)

    to_return = df.copy()
    to_return['accuracy'] = correctness
    return to_return


#nhl_data = pd.read_csv('../data/processed_data/nhl/generic_nhl_data_flipped.csv')
#nba_data = pd.read_csv('../data/processed_data/nba/generic_nba_data_flipped.csv')
#nfl_data = pd.read_csv('../data/processed_data/nfl_historical/generic_nfl_data_flipped.csv')

#get_season_winrate(nhl_data).to_csv('nhl.csv', index=False)
#get_season_winrate(nba_data).to_csv('nba.csv', index=False)
#get_season_winrate(nfl_data).to_csv('nfl.csv', index=False)