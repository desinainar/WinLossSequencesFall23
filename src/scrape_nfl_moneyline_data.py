from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from io import StringIO

data = pd.read_csv('testing.csv')

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1200")
#driver = webdriver.Chrome(options=options)

for index in data.index:
    home_team = data['home'][index]
    away_team = data['away'][index]
    date = data['date'][index]
    url_date = ""

    for element in date.split("-"):
        url_date += element
    
    print("https://www.cbssports.com/nfl/gametracker/boxscore/NFL_" + url_date + "_" + away_team + "@" + home_team)

#odds = driver.find_elements(By.CLASS_NAME, 'hud-odds')

# name-changes to be done
# cbs_name -> 538_name
# WSH -> WAS
