import numpy as np
import pandas as pd

data = pd.read_csv('data/processed_data/epl_current_trimmed.csv')
teams = data['Result']
print(teams)