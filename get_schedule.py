from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time, unicodedata
import pandas as pd

from utilities import *

# download chrome driver here: https://chromedriver.chromium.org/
# put it in the same folder as the scripts

url = 'https://www.dota2.com/esports/winter21/schedule'

# open the DPC schedule page
opt = Options()
opt.headless = True
opt.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options = opt)
driver.get(url)

# wait an extra 2 seconds after page loads
time.sleep(2)

# click the button containing "Skip"
# change this according to your language
btn_text = 'Skip'
btn = driver.find_element('xpath', '//div[contains(text(), "{}")]'.format(btn_text))
btn.click()

# wait for schedule to load
schd_cls = 'schedulepage_DPCScheduleList'
schedule = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.XPATH,
        '//div[contains(@class, "{}")]'.format(schd_cls))))

# wait an extra 2 seconds after schedule loads
time.sleep(2)

# reconstruct schedule
days_cls = 'schedulepage_DaySection'
date_cls = 'schedulepage_DayHeader'
game_cls = 'schedulepage_DPCScheduleEntry'

days = schedule.find_elements('xpath', './/div[contains(@class, "{}")]'.format(days_cls))

data = []
for day in days:
    date = day.find_element('xpath', './/div[contains(@class, "{}")]'.format(date_cls)).text
    games = day.find_elements('xpath', './/div[contains(@class, "{}")]'.format(game_cls))
    for game in games:
        d = game.text.split('\n')
        vs = d[4:].index('vs')
        t1, t2 = d[4:][:vs][0], d[4:][vs + 1:][0]

        # fix weird characters
        t1 = unicodedata.normalize('NFKD', t1)
        t2 = unicodedata.normalize('NFKD', t2)

        data += [[date, *d[:4], t1, t2]]

data = pd.DataFrame(data, columns = ['date', 'region', 'division', 'time', 'timezone', 'team_1', 'team_2'])
driver.quit()

# extra: get team IDs
teams = pd.unique(data[['team_1', 'team_2']].values.ravel())
team_ids = {t: D2_get_team_id(t) for t in teams}

data['id_1'] = data['team_1'].map(team_ids)
data['id_2'] = data['team_2'].map(team_ids)
data.to_csv('DPC_schedule.csv')
