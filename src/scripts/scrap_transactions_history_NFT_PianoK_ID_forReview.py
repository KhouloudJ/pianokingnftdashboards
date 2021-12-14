# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 11:27:22 2021

@author: Administrator
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta
import re
import pandas as pd

chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_driver_path = "C:/01. DataIDraw/00. Venv/00. General/01. Ouverture Chrome/Chrome V96/chromedriver.exe"
driver = webdriver.Chrome(
                    executable_path = chrome_driver_path,
                    options = chrome_options
                    )

df_history = pd.DataFrame(columns=['Event', 'Price', 'From', 'To', 'DateFormat'])

for _id in range(1, 1001):
    driver.get(f'https://opensea.io/assets/0x725afa0c34bab44f5b1ef8f87c50438f934c1a85/{_id}')
    time.sleep(2)
    items_activity = driver.find_elements_by_xpath("//div[@class='Scrollbox--content']/div")
    for activity in items_activity[1:-1]:
        event = activity.find_element_by_xpath(".//div[contains(@class, 'EventHistory--event')]/span").text
        price = activity.find_element_by_xpath(".//div[contains(@class, 'EventHistory--price')]").text
        _from = activity.find_elements_by_xpath(".//div[@class='Row--cell Row--cellIsSpaced']")[0].text
        _to = activity.find_elements_by_xpath(".//div[@class='Row--cell Row--cellIsSpaced']")[1].text
        _date = activity.find_element_by_xpath(".//div[@data-testid='EventTimestamp']").text  
        # Retraitement de la date
        if re.findall("\d+", _date):
            jours_ecart = int(re.findall("\d+", _date)[0])
        elif _date == "a day ago":
            jours_ecart = 1
        else:
            jours_ecart = 0
        date_format = (datetime.now() - timedelta(days=jours_ecart)).strftime("%Y-%m-%d") 
        df_history = df_history.append(
            {
            "TokenID" : _id,
            "Event" : event,
            "Price" : price,
            "From" : _from,
            "To" : _to,
            "DateFormat" : date_format
             },
            ignore_index=True
        )
    time.sleep(0.5)

df_history.to_excel("C:/01. DataIDraw/11. Developpement cours/05. PianoKing NFT/transac_history_by_PK_NFT_ID.xlsx")
df_history.to_csv("C:/01. DataIDraw/11. Developpement cours/05. PianoKing NFT/transac_history_by_PK_NFT_ID.csv")





