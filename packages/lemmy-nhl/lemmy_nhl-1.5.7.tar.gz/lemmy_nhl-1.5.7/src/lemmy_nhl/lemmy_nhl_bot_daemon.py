"""Copyright [2023] [socphoenix]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

import requests
import sqlite3
from plemmy import LemmyHttp
import os.path
import time
import datetime
import sys
from lemmy_nhl import post_body
from plemmy.responses import GetCommunityResponse
import datetime

teamID = 0
CID = 0
isMod = "n"
gameOver = False
standings = False
stats = False
postID = 0
teamID = 0
newSchedule = False
srv = ""
inSeason = False
scheduled = False
recap_timeout = 0
# create time based services
# check for game today:


def seasonStart():
    global games, inSeason
    date = datetime.datetime.now()
    today = date.strftime("%Y, %m, %d").split(", ")
    lastGame = games[len(games)-1][1]
    lastGame = lastGame.split("-")
    firstGame = games[0][1]
    firstGame = firstGame.split("-")
    if(inSeason == False and int(today[1]) > 10):
        inSeason = True
    elif(inSeason == False and int(today[1]) == 10 and int(today[2]) > int(firstGame[2])):
        inSeason = True
    elif(int(today[1] == int(lastGame[1])) and int(today[2]) > int(lastGame[2])):
        inSeason = False
    elif(inSeason == True and int(today[1]) > int(lastGame[1])):
        inSeason = False

#add side bar schedule task
def scheduler():
    global games, srv, communityName
    date = datetime.datetime.now()
    today = date.strftime("%Y, %m, %d").split(", ")
    scheduleBody = "*** Upcoming Games: \n | Opponent | Time | \n | ---- | ---- | \n"
    for y in range(7):
        pm = ""
        for x in range(len(games)):
            gameToday = games[x][1]
            gameToday = gameToday.split("-")
            if(today[0] == gameToday[0] and today[1] == gameToday[1] and today[2] == gameToday[2]):
                r = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + str(games[x][0]) + "/linescore")
                team = int(r.json().get("teams").get("home").get("team").get("id"))
                if(team == teamID):
                    team = int(r.json().get("teams").get("away").get("team").get("id"))
                teamName = r.json().get("teams").get("home").get("team").get("name")
                timeStart = games[x][2]
                timeStart = timeStart.split(":")
                times = [int(timeStart[0]) - 4, int(timeStart[0]) - 5]
                if(times[0] > 12):
                    times[0] = times[0] - 12
                    pm = "p.m."
                if(times[1] > 12):
                    times[1] = times[1] - 12
                    pm = "p.m."
                times[0] = str(times[0]) + ":" + str(timeStart[1])
                times[1] = str(times[1]) + ":" + str(timeStart[1])
                scheduleBody = scheduleBody + "| " + teamName + " | " + times[0] + pm + " Est/" + times[1] + " Cst + | \n"
        date += datetime.timedelta(days=1)
        today = date.strftime("%Y, %m, %d").split(", ")
    try:
        temp = GetCommunityResponse(srv.get_community(name=communityName)).community_view.community.description
        temp = temp.split("*** ")
        body = temp[0] + scheduleBody
        posted = False
        while(posted == False):
            try:
                srv.edit_community(CID, description = body)
                posted = True
            except:
                print("failed to post standings, trying again.")
    except:
        print("Failed to contact server, sidebar not updated")

#is game
def isGame():
    global gameOver, games, gamePK, srv, postID
    today = time.strftime("%Y, %m, %d")
    today = str(today)
    today = today.split(", ")
    for x in range(len(games)):
        gameToday = games[x][1]
        gameToday = gameToday.split("-")
        gamePK = games[x][0]
        if(today[0] == gameToday[0] and today[1] == gameToday[1] and today[2] == gameToday[2]):
            timeStart = games[x][2]
            curTime = time.strftime("%H:%M", time.gmtime())
            timeStart = timeStart.split(":")
            curTime = curTime.split(":")
            #compare 0, 1 on these if hour and minute >= to then start game
            if(int(curTime[0]) >= int(timeStart[0]) and int(curTime[1]) >= int(timeStart[1]) and gameOver == False):
                create_post_linescore()
                while(gameOver == False):
                    gameTime()
                time.sleep(360)
                r = srv.get_post(postID)
                posted = False
                while(posted == False):
                    try:
                        recap = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + str(gamePK) + "/content")
                        recap = recap.json()
                        body2 = r.json().get("post_view").get("post").get("body") + "\n\n "
                        body2 = body2 + "# [recap]("
                        body2 = body2 + str(recap.get("media").get("epg")[2].get("items")[0].get("playbacks")[3].get("url")) + ")"
                        srv.edit_post(postID, body=body2)
                        posted = True
                    except:
                        print("Failed to get recap, waiting 60 seconds.")
                        time.sleep(60)
                        recap_timeout = recap_timeout + 1
                        if(recap_timeout > 4):
                            print("Could not get recap ending attempts")
                            posted = True
                srv.feature_post("Community", False, postID)

#create post for linescore
def create_post_linescore():
    global teamID, gamePK, isMod, srv, postID
    #get team Names/date/regular Season
    game_today = "https://statsapi.web.nhl.com/api/v1/game/" + str(gamePK) + "/linescore"
    game_today2 = "https://statsapi.web.nhl.com/api/v1/schedule?teamId="
    game_today2 = game_today2 + str(teamID)
    r = requests.get(game_today)
    t = requests.get(game_today2)
    home_name = r.json().get("teams").get("home").get("team").get("name")
    away_name = r.json().get("teams").get("away").get("team").get("name")
    date = t.json().get("dates")[0].get("date")
    gameType = t.json().get("dates")[0].get("games")[0].get("gameType")
    if(gameType == "R"):
        gameType = "Regular Season"
    elif(gameType == "PR"):
        gameType = "Pre-Season"
    else:
        gameType = "Playoffs"
    postName = away_name + " vs. " + home_name + " " + gameType + " " + str(date)
    global CID, postID
    temp = CID
    posted = False
    while(posted == False):
        try:
            post = srv.create_post(temp, postName, body="")
            postID = post.json().get("post_view")
            postID = postID["post"].get("id")
            posted = True
        except:
            print("failed to post, trying again in 30 seconds")
            time.sleep(30)
    if(isMod == "y"):
        feature = False
        while(feature == False):
            try:
                srv.feature_post("Community", True, postID)
                feature = True
            except:
                print("Failed to feature post, trying again in 30 seconds.")
                time.sleep(30)


#Linescore for game
def gameTime():
    global gameOver, postID, gamePK, srv
    body2, gameOver = post_body.post_body_linescore(gamePK)
    try:
        test = srv.edit_post(postID, body=body2)
    except:
        print("failed to contact server. Adding extra 60 seconds before retrying")
        time.sleep(60)
    time.sleep(5)


#get community ID

def create_post_stats():
    global CID, teamID, srv
    today = time.strftime("%m-%d-%Y")
    title = "Team Stats for the Season as of " + today
    body = post_body.post_body_stats(teamID)
    posted = False
    while(posted == False):
        try:
            srv.create_post(CID, title, body=body)
            posted = True
        except:
            print("failed to post, trying again in 30 seconds.")
            time.sleep(30)

def create_post_standings():
    today = time.strftime("%m-%d-%Y")
    global CID
    postName = "NHL Standings as of " + today
    body = post_body.post_body_standings()
    posted = False
    while(posted == False):
        try:
            post = srv.create_post(CID, postName, body=body)
            posted = True
        except:
            print("failed to post, trying again in 30 seconds.")
            time.sleep(30)

#main loop segment
def daemon():
    global token, communityName, server, teamID, isMod, games, standings, stats, post, CID, newSchedule, gameOver, srv, inSeason
    dbLocation = os.path.expanduser("~/.cache/lnhl.db")
    if(os.path.exists(dbLocation) == False):
        print("Please run config.py first!")
        sys.exit()

    #sql database connection/data grabbing
    con = sqlite3.connect(dbLocation)
    cur = con.cursor()
    #get login token
    r = cur.execute("SELECT token FROM user")
    temp = r.fetchall()
    token = str(temp[0])
    token = token.lstrip("('")
    token = token.rstrip("',)")
    #get community Name
    r = cur.execute("SELECT communityName FROM user")
    temp = r.fetchall()
    communityName = str(temp[0])
    communityName = communityName.lstrip("('")
    communityName = communityName.rstrip("',)")
    # get server name
    r = cur.execute("SELECT server FROM user")
    temp = r.fetchall()
    server = str(temp[0])
    server = server.lstrip("('")
    server = server.rstrip("',)")
    #get teamID
    r = cur.execute("SELECT teamID FROM user")
    temp = r.fetchall()
    teamID = str(temp[0])
    teamID = teamID.lstrip("('")
    teamID = teamID.rstrip("',)")

    #get mod status
    r = cur.execute("SELECT isMod FROM user")
    temp = r.fetchall()
    isMod = str(temp[0])
    isMod = isMod.lstrip("('")
    isMod = isMod.rstrip("',)")

    #get games
    r = cur.execute("SELECT * FROM schedule")
    games = r.fetchall()

    #get info on which bots to use
    try:
        r = cur.execute("SELECT * FROM bots")
        bots = r.fetchall()
    except:
        print("missing granular bot info, please consider running the config script again!")
        print("App will assume you want to run all bots")
        bots = [["y", "y", "y", "y"]]

    #use login token, check for game, get community id, create post, then loop
    srv = LemmyHttp(server)
    srv.key = token
    global CID
    CID = GetCommunityResponse(srv.get_community(name=communityName)).community_view.community.id

    #main loop
    while(True):
        # check for in Season for team:
        seasonStart()
        # bots(stats, standings, schedule, linescore)")
        if(bots[0][3] == "y"):
            isGame()


        today = time.strftime("%a")
        #run scheduler weekly no matter what
        if(str(today == "Sun" and scheduled == False)):
            if(isMod == "y" and bots[0][2] == "y"):
                scheduler()
                scheduled = True
        if(str(today) == "Sun" and standings == False and inSeason == True):
            if(bots[0][1] == "y"):
                create_post_standings()
            if(bots[0][0] == "y"):
                create_post_stats()
            standings = True
            stats = True
        elif(str(today) == "Sun" and newSchedule == False):
            newSchedule = True
            # get new schedule weekly to catch playoffs
            cur.execute("DELETE FROM schedule")
            con.commit()
            year = int(time.strftime("%Y"))
            t = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?teamId=" + str(teamID) + "&season=" + str(year) + str(year + 1))
            games = t.json().get("dates")
            i = len(games)
            j = 0
            while(j < i):
                gamePK = games[j].get("games")[0].get("gamePk")
                date = games[j].get("games")[0].get("gameDate")
                date = date.split("T")
                date[1] = date[1].rstrip("Z")
                cur.execute("INSERT INTO schedule VALUES (?, ?, ?);", (gamePK, date[0], date[1]))
                con.commit()
                j = j + 1
            r = cur.execute("SELECT * FROM schedule")
            games = r.fetchall()
        elif(str(today) == "Tue" and standings == True):
            standings = False
            stats = False
            newSchedule = False
            scheduled = False
        time.sleep(300)
