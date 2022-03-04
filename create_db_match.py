#Create db game
from urllib.request import urlopen
import json
import pandas as pd
import datetime as dt
import sqlite3

db = sqlite3.connect('data_bank.db')


def get_score(id_day):
    
    url_score = "http://data.nba.net/10s/prod/v1/"+ id_day + "/scoreboard.json"
    res = urlopen(url_score)
    data = json.loads(res.read())

    print("Il y a eu " + str(len(data['games'])) + " game le " + id_day)
    for numGame in range(len(data['games'])):
        id_match = data['games'][numGame]["gameId"]
        visitor = data['games'][numGame]["vTeam"]["teamId"]
        home = data['games'][numGame]["hTeam"]["teamId"]
        date = id_day
        db.execute("INSERT INTO store_match VALUES (?, ?, ?, ?, ?, ?)", (id_match,id_match, id_day, home, visitor, 0))

id_day = ""
date = dt.datetime.now() + dt.timedelta(days=7)
not_do = True
while (not_do):
    try:
        date = date - dt.timedelta(days=1)
        str_date = date.strftime("%Y%m%d")
        print(str_date)
        id_day = str_date
        test_db = db.execute("SELECT date FROM store_match WHERE date ="+ id_day)
        if(len(test_db.fetchall()) != 0 or id_day == "20211019"):
            not_do = False
        else:
            get_score(id_day)
    except:

        print("error pour le " + id_day)
    
        
db.commit()
db.close()
       
