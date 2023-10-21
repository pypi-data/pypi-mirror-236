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

#basic config, will save the token key for future logins, team, community name
import getpass
from plemmy import LemmyHttp
import sqlite3
import requests
import time
import os.path
import sys

def newToken():
    dbLocation = os.path.expanduser("~/.cache/lnhl.db")
    server = input("server address (make sure to include the https://): ")
    username = input("Username: ")
    password = getpass.getpass('Password: ')
    srv = LemmyHttp(server)
    r = srv.login(username, password)
    token = r.json().get("jwt")
    con = sqlite3.connect(dbLocation)
    cur = con.cursor()
    r = cur.execute("SELECT token FROM user")
    temp = r.fetchall()
    oldToken = str(temp[0])
    oldToken = token.lstrip("('")
    oldToken = token.rstrip("',)")
    cur.execute("UPDATE user SET token = ? , WHERE token = ?", (token, oldToken))
    con.commit()
    print("New Token saved.")
    sys.exit()

def config():
    dbLocation = os.path.expanduser("~/.cache/lnhl.db")
    print("Basic Setup, This will store your auth token in an unencrypted database. Username/password itself are not saved.")
    print("If database already exists all data will be overwritten!")
    justToken = input("Do you just need to update your token? y/n ")
    justToken = newToken
    if(justToken == "y" or justToken == "Y"):
        newToken()
    server = input("server address (make sure to include the https://): ")
    username = input("Username: ")
    password = getpass.getpass('Password: ')
    isMod = input("Is this account a mod of the community? (needed to pin posts) (y/n): ")
    isMod = isMod.lower()
    defaults = input("Would you like to enable all services, or choose individually (stats, standings, schedule, linescore) y/n: ")
    defaults = defaults.lower()
    bots = ["n", "n", "n", "n"]
    if(defaults == "y"):
        print("Excellent choice, setting up services and scraping the schedule now.")
        for x in range(len(bots)):
            bots[x] = "y"
    elif(defaults == "n"):
        bots[0]= input("Would you like to enable the stat bot? (y/n): ")
        bots[0] = bots[0].lower()
        bots[1] = input("Would you like to enable the standings bot? (y/n): ")
        bots[1] = bots[1].lower()
        bots[2] = input("Would you like to enable the side-bar schedule bot? (y/n): ")
        bots[2] = bots[2].lower()
        bots[3] = input("Would you like to enable the live game thread bot? (y/n): ")
        bots[3] = bots[3].lower()
    else:
        print("You selected an invalid response. Assuming you want all the bots")
        for x in range(len(bots)):
            bots[x] = "y"

    t = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
    teams = t.json().get("teams")
    print("Select team Number from the following:")

    for x in range(0, len(teams)):
        print(teams[x].get("name") + ": " + str(teams[x].get("id")))
    teamID = input("Team ID NUM: ")
    communityName = input("Name of the local community: ")

    srv = LemmyHttp(server)
    r = srv.login(username, password)
    token = r.json().get("jwt")

    con = sqlite3.connect(dbLocation)
    cur = con.cursor()
    try:
        cur.execute("CREATE TABLE user(token, teamID, communityName, server, isMod)")
        cur.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?);", (token, teamID, communityName, server, isMod))
        con.commit()
    except:
        cur.execute("DELETE FROM user")
        cur.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?);", (token, teamID, communityName, server, isMod))
        con.commit()
    try:
        cur.execute("CREATE TABLE schedule(gamePK, date, time)")
        con.commit()
    except:
        cur.execute("DELETE FROM schedule")
        con.commit()
    try:
        cur.execute("CREATE TABLE bots(stats, standings, schedule, linescore)")
        cur.execute("INSERT INTO bots VALUES (?, ?, ?, ?);", (bots[0], bots[1], bots[2], bots[3]))
        con.commit()
    except:
        cur.execute("DELETE FROM bots")
        cur.execute("INSERT INTO bots VALUES (?, ?, ?, ?);", (bots[0], bots[1], bots[2], bots[3]))
        con.commit()

    #scrape schedule and times, output to database under schedule table
    today = time.strftime("%Y")
    year = int(today) + 1
    t = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?teamId=" + str(teamID) + "&season=" + str(today) + str(year))
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
    print("Configuration done!")
