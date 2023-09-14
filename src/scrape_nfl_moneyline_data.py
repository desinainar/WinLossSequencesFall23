from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from io import StringIO

# CBS considers Washington as "WAS" and Jacksonville as "JAC" which 538 disagree with
name_changes = {'WSH': 'WAS', 'JAX': 'JAC'}

data = pd.read_csv('testing.csv')

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome('C:/Users/leona/Documents/chromedriver/chromedriver', options=options)

for index in data.index:
    
    home_team = data['home'][index]
    if(home_team in name_changes.keys()):
        home_team = name_changes[home_team]

    away_team = data['away'][index]
    if(away_team in name_changes.keys()):
        away_team = name_changes[away_team]

    split_date = data['date'][index].split("-")
    
    # ACCOUNT FOR THE EVER-SO-FRUSTRATING RELOCATION OF THE RAIDERS AND 538'S IGNORANCE OF IT    
    if(int(split_date[0]) > 2020 or (int(split_date[0]) == 2020 and int(split_date[1]) > 8)):
        if(away_team == 'OAK'):
            away_team = 'LV'
        if(home_team == 'OAK'):
            home_team == 'LV'

    url_date = ""
    for element in split_date:
        url_date += element
    
    website = "https://www.cbssports.com/nfl/gametracker/boxscore/NFL_" + url_date + "_" + away_team + "@" + home_team
    
    driver.get(website)

    odds = driver.find_elements(By.CLASS_NAME, 'hud-odds')
    with open('output.txt', 'a') as f:
        f.write(url_date)
        f.write(home_team + ": " + odds[0].text)
        f.write(away_team + ": " + odds[2].text)
        f.write('\n')


