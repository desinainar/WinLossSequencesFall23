import penaltyblog as pb
import numpy as np
import pandas as pd

nfl_df = pd.read_csv('data/processed_data/nfl_live/nfl_current_trimmed.csv')
colley = pb.ratings.Colley(nfl_df["score1"], nfl_df["score2"], nfl_df["team1"], nfl_df["team2"])
ratings = colley.get_ratings() 
print(ratings)


