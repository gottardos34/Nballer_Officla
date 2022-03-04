#Create db joueur

from urllib.request import urlopen
import json
import pandas as pd
import datetime as dt
import sqlite3

def get_draft_score_match(id_match, id_day):
    url_boxscore = "http://data.nba.net/prod/v1/" + str(id_day) + "/" + str(id_match) + "_boxscore.json"
    res = urlopen(url_boxscore)
    data = json.loads(res.read())
    try:
        a = len(data["stats"]["activePlayers"])
    except:
        return(None)
        
    
    for num_player in range (len(data["stats"]["activePlayers"])):
        try:
            player = data["stats"]["activePlayers"][num_player]
        except:
            print("no player")
        name = get_info(player,"firstName") + " " + get_info(player,"lastName")
        player_ = get_info(player,"personId")
        pts =  get_info(player,"points")
        reb = get_info(player,"totReb")
        assist = get_info(player,"assists")
        block = get_info(player,"blocks")
        steal = get_info(player,"steals")
        TO = get_info(player,"turnovers")
        PM = get_info(player,"plusMinus")
        In = get_info(player,"fgm")
        time = get_info(player,"min")
        fga = get_info(player, "fga")
        fgm = get_info(player, "fgm")
        Out = str(int(float(fga)) - int(float(fgm)))
        score = int(pts) + int(reb) + int(assist) + int(block) + int(steal)
        score = score + int(PM) + int(In) - int(TO) - int(Out)
        db.execute("INSERT INTO store_score_nbl VALUES (?, ?, ?, ?, ?)", (int(player_ + "_" + id_day), int(player_), int(id_match), int(score), time))
    
def get_info(player, stat):
    try:
        res = player[stat]
        if(res == ""):
            res = "0"
        return res
    except:
        player = data["stats"]["activePlayers"][num_player]
        name = player["firstName"] + " " + player["lastName"]
        print("Problème pour: " + name + "Probleme res :" + stat)
        
db = sqlite3.connect("data_bank.db")
A = db.execute('SELECT DISTINCT id_match FROM store_score_nbl')
already = []
for a in A:
    already = already + [a[0]]

all_score = []
for row in db.execute('SELECT id_match, date FROM store_match ORDER BY date DESC'):
    try:
        if(row[0] in already):
            print("On a déja ce match :" + str(row[1]))
        else:
            print("Calcul de " + str(row[1]))
            get_draft_score_match(row[0], row[1])
    except:
        print("Pas de match le " + str(row[1]))
        break
db.commit()
db.close()
