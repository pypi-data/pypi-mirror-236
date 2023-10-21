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

#standings bot post body
def post_body_standings():
    r = requests.get("https://statsapi.web.nhl.com/api/v1/standings")
    teams = r.json().get("records")[0].get("teamRecords")
    i = 0
    j = len(teams)
    body = "# Eastern Conference \n\n ## Metropolitan Division \n"
    body = body + "| Team | W | L | OT | Pts | Clinched Playoffs | \n"
    body = body + "|----- | ---- | ---- | ---- | ---- | ----- | \n"
    while(i < j):
        team = r.json().get("records")[0].get("teamRecords")[i].get("team").get("name")
        records = [0,0,0,0]
        records[0] = r.json().get("records")[0].get("teamRecords")[i].get("leagueRecord").get("wins")
        records[1] = r.json().get("records")[0].get("teamRecords")[i].get("leagueRecord").get("losses")
        records[2] = r.json().get("records")[0].get("teamRecords")[i].get("leagueRecord").get("ot")
        records[3] = r.json().get("records")[0].get("teamRecords")[i].get("points")
        Clinched = r.json().get("records")[0].get("teamRecords")[i].get("clinchIndicator")
        if(Clinched == None):
               Clinched = ""
        body = body + "| " + team + " | " + str(records[0]) + " | " + str(records[1]) + " | " + str(records[2]) + " | "
        body = body + str(records[3]) + " | " + str(Clinched) + " | \n"
        i = i + 1
    teams = r.json().get("records")[1].get("teamRecords")
    i = 0
    j = len(teams)
    body = body + "## Atlantic Division \n"
    body = body + "| Team | W | L | OT | Pts | Clinched Playoffs |\n"
    body = body + "|----- | ---- | ---- | ---- | ---- | ----- |\n"
    while(i < j):
        team = r.json().get("records")[1].get("teamRecords")[i].get("team").get("name")
        records = [0,0,0,0]
        records[0] = r.json().get("records")[1].get("teamRecords")[i].get("leagueRecord").get("wins")
        records[1] = r.json().get("records")[1].get("teamRecords")[i].get("leagueRecord").get("losses")
        records[2] = r.json().get("records")[1].get("teamRecords")[i].get("leagueRecord").get("ot")
        records[3] = r.json().get("records")[1].get("teamRecords")[i].get("points")
        Clinched = r.json().get("records")[1].get("teamRecords")[i].get("clinchIndicator")
        if(Clinched == None):
               Clinched = ""
        body = body + "| " + team + " | " + str(records[0]) + " | " + str(records[1]) + " | " + str(records[2]) + " | "
        body = body + str(records[3]) + " | " + str(Clinched) + " | \n"
        i = i + 1
    #3rd
    teams = r.json().get("records")[2].get("teamRecords")
    i = 0
    j = len(teams)
    body = body + "# Western Conference \n\n ## Central Division \n"
    body = body + "| Team | W | L | OT | Pts | Clinched Playoffs |\n"
    body = body + "|----- | ---- | ---- | ---- | ---- | ----- |\n"
    while(i < j):
        team = r.json().get("records")[2].get("teamRecords")[i].get("team").get("name")
        records = [0,0,0,0]
        records[0] = r.json().get("records")[2].get("teamRecords")[i].get("leagueRecord").get("wins")
        records[1] = r.json().get("records")[2].get("teamRecords")[i].get("leagueRecord").get("losses")
        records[2] = r.json().get("records")[2].get("teamRecords")[i].get("leagueRecord").get("ot")
        records[3] = r.json().get("records")[2].get("teamRecords")[i].get("points")
        Clinched = r.json().get("records")[2].get("teamRecords")[i].get("clinchIndicator")
        if(Clinched == None):
               Clinched = ""
        body = body + "| " + team + " | " + str(records[0]) + " | " + str(records[1]) + " | " + str(records[2]) + " | "
        body = body + str(records[3]) + " | " + str(Clinched) + " | \n"
        i = i + 1
    #4th
    teams = r.json().get("records")[3].get("teamRecords")
    i = 0
    j = len(teams)
    body = body + "## Pacific Division \n"
    body = body + "| Team | W | L | OT | Pts | Clinched Playoffs |\n"
    body = body + "|----- | ---- | ---- | ---- | ---- | ----- |\n"
    while(i < j):
        team = r.json().get("records")[3].get("teamRecords")[i].get("team").get("name")
        records = [0,0,0,0]
        records[0] = r.json().get("records")[3].get("teamRecords")[i].get("leagueRecord").get("wins")
        records[1] = r.json().get("records")[3].get("teamRecords")[i].get("leagueRecord").get("losses")
        records[2] = r.json().get("records")[3].get("teamRecords")[i].get("leagueRecord").get("ot")
        records[3] = r.json().get("records")[3].get("teamRecords")[i].get("points")
        Clinched = r.json().get("records")[3].get("teamRecords")[i].get("clinchIndicator")
        if(Clinched == None):
               Clinched = ""
        body = body + "| " + team + " | " + str(records[0]) + " | " + str(records[1]) + " | " + str(records[2]) + " | "
        body = body + str(records[3]) + " | " + str(Clinched) + " | \n"
        i = i + 1
    return body

#stat bot post body
def post_body_stats(teamID):
    link = "https://statsapi.web.nhl.com/api/v1/teams/" + str(teamID) + "/stats"
    r = requests.get(link)
    team = r.json().get("stats")[1].get("splits")[0].get("team").get("name")
    stats = []
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("ptPctg"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("goalsPerGame"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("goalsAgainstPerGame"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("powerPlayPercentage"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("penaltyKillPercentage"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("shotsPerGame"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("shotsAllowed"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("faceOffWinPercentage"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("shootingPctg"))
    stats.append(r.json().get("stats")[0].get("splits")[0].get("stat").get("savePctg"))
    i = len(stats)
    j = 0
    body = "| Pnt Pctge | Goals Per Game | Goals Against Per Game | Power Play % | Penalty Kill % | Shots Per Game | Shots Allowed | "
    body = body + "Face Off Win % | Shooting % | Save % |\n"
    body = body + "| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | \n"
    body = body + "| " + str(stats[0]) + " | " + str(stats[1]) + " | " + str(stats[2]) + " | " + str(stats[3]) + " | "
    body = body + str(stats[4]) + " | " + str(stats[5]) + " | " + str(stats[6]) + " | " + str(stats[7]) + " | "
    body = body + str(stats[8]) + " | " + str(stats[9]) + " | \n"
    return body

def post_body_linescore(gamePK):
    homeOtShots = 0
    awayOtShots = 0
    gameOver = False
    game_today = "https://statsapi.web.nhl.com/api/v1/game/" + str(gamePK) + "/linescore"
    r = requests.get(game_today)
    home_name = r.json().get("teams").get("home").get("team").get("name")
    home_goals = r.json().get("teams").get("home").get("goals")
    home_power = r.json().get("teams").get("home").get("powerPlay")
    home_shots = r.json().get("teams").get("home").get("shotsOnGoal")
    away_name = r.json().get("teams").get("away").get("team").get("name")
    away_goals = r.json().get("teams").get("away").get("goals")
    away_power = r.json().get("teams").get("away").get("powerPlay")
    away_shots = r.json().get("teams").get("away").get("shotsOnGoal")
    currentPeriod = r.json().get("currentPeriod")
    timeLeft = r.json().get("currentPeriodTimeRemaining")
    period = r.json().get("periods")
    temp = r.json().get("currentPeriodTimeRemaining")
    if(temp == "Final" and currentPeriod >= 3 and away_goals != home_goals):
        gameOver = True
    #overtime handler for current Period stat
    if(currentPeriod >= 4):
        currentPeriod = "OT " + str(currentPeriod - 3)
    numPeriods = len(period) - 1
    #main body
    body = "# " + away_name + " vs " + home_name + " \n"
    body = body + "| Period | Time Remaining | \n"
    body = body + "| ------- | ------------- | \n"
    body = body + "| " + str(currentPeriod) + " | " + timeLeft + " | \n"
    body = body + "## Scores: \n"
    if(numPeriods <= 0):
        body = body + "| Team | Period 1: | Period 2:  | Period 3: | Totals | \n"
        body = body + "| ----- | -------- | ---------- | ----------- | ------| \n"
        body = body + "| " + away_name + " | " +  str(period[0].get("away").get("goals")) + " | "
        body = body +  " " + " | " +  " " + " | "
        body = body + str(away_goals) + " | \n"
        body = body + "| " + home_name + " | " +  str(period[0].get("home").get("goals")) + " | "
        body = body + " " + " | " + " " + " | "
        body = body + str(home_goals) + " | \n"
    elif(numPeriods == 1):
        body = body + "| Team | Period 1: | Period 2:  | Period 3: | Totals | \n"
        body = body + "| ----- | -------- | ---------- | ----------- | ------| \n"
        body = body + "| " + away_name + " | " +  str(period[0].get("away").get("goals")) + " | "
        body = body +  str(period[1].get("away").get("goals")) + " | " +  " " + " | "
        body = body + str(away_goals) + " | \n"
        body = body + "| " + home_name + " | " +  str(period[0].get("home").get("goals")) + " | "
        body = body + str(period[1].get("home").get("goals")) + " | " + " " + " | "
        body = body + str(home_goals) + " | \n"
    elif(numPeriods == 2):
        body = body + "| Team | Period 1: | Period 2:  | Period 3: | Totals | \n"
        body = body + "| ----- | -------- | ---------- | ----------- | ------| \n"
        body = body + "| " + away_name + " | " +  str(period[0].get("away").get("goals")) + " | "
        body = body +  str(period[1].get("away").get("goals")) + " | " +  str(period[2].get("away").get("goals")) + " | "
        body = body + str(away_goals) + " | \n"
        body = body + "| " + home_name + " | " +  str(period[0].get("home").get("goals")) + " | "
        body = body + str(period[1].get("home").get("goals")) + " | " + str(period[2].get("home").get("goals")) + " | "
        body = body + str(home_goals) + " | \n"
    else:
        body = body + "| Team | Period 1: | Period 2:  | Period 3: | OT | Totals | \n"
        body = body + "| ----- | -------- | ---------- | --------- | ------| ----- | \n"
        body = body + "| " + away_name + " | " +  str(period[0].get("away").get("goals")) + " | "
        body = body +  str(period[1].get("away").get("goals")) + " | " +  str(period[2].get("away").get("goals")) + " | "
        body = body + str(period[numPeriods].get("away").get("goals")) + " | " + str(away_goals) + " | \n"
        body = body + "| " + home_name + " | " +  str(period[0].get("home").get("goals")) + " | "
        body = body + str(period[1].get("home").get("goals")) + " | " + str(period[2].get("home").get("goals")) + " | "
        body = body + str(period[numPeriods].get("home").get("goals")) + " | " + str(home_goals) + " | \n"
    body = body + "## Shots on Goal: \n"
    if(numPeriods <= 0):
        body = body + "| Team | Period 1 | Period 2 | Period 3 | Total Shots | \n"
        body = body + "| ----- | ------- | -------- | -------- | ----------- | \n"
        body = body + "| " + away_name + " | " + str(period[0].get("away").get("shotsOnGoal")) + " | "
        body = body + " " + " | " + " " + " | "
        body = body + str(away_shots) + " | \n"
        body = body + "| " + home_name + " | " + str(period[0].get("home").get("shotsOnGoal")) + " | "
        body = body + " " + " | " + " " + " | "
        body = body + str(home_shots) + " | \n"
    elif(numPeriods == 1):
        body = body + "| Team | Period 1 | Period 2 | Period 3 | Total Shots | \n"
        body = body + "| ----- | ------- | -------- | -------- | ----------- | \n"
        body = body + "| " + away_name + " | " + str(period[0].get("away").get("shotsOnGoal")) + " | "
        body = body + str(period[1].get("away").get("shotsOnGoal")) + " | " + " " + " | "
        body = body + str(away_shots) + " | \n"
        body = body + "| " + home_name + " | " + str(period[0].get("home").get("shotsOnGoal")) + " | "
        body = body + str(period[1].get("home").get("shotsOnGoal")) + " | " + " " + " | "
        body = body + str(home_shots) + " | \n"
    elif(numPeriods == 2):
        body = body + "| Team | Period 1 | Period 2 | Period 3 | Total Shots | \n"
        body = body + "| ----- | ------- | -------- | -------- | ----------- | \n"
        body = body + "| " + away_name + " | " + str(period[0].get("away").get("shotsOnGoal")) + " | "
        body = body + str(period[1].get("away").get("shotsOnGoal")) + " | " + str(period[2].get("away").get("shotsOnGoal")) + " | "
        body = body + str(away_shots) + " | \n"
        body = body + "| " + home_name + " | " + str(period[0].get("home").get("shotsOnGoal")) + " | "
        body = body + str(period[1].get("home").get("shotsOnGoal")) + " | " + str(period[2].get("home").get("shotsOnGoal")) + " | "
        body = body + str(home_shots) + " | \n"
    else:
        if(numPeriods - 3 == 0):
            homeOtShots = period[3].get("home").get("shotsOnGoal")
            awayOtShots = period[3].get("away").get("shotsOnGoal")
        else:
            for x in range(3, numPeriods):
                homeOtShots = homeOtShots + period[x].get("home").get("shotsOnGoal")
                awayOtShots = awayOtShots + period[x].get("away").get("shotsOnGoal")
        body = body + "| Team | Period 1 | Period 2 | Period 3 | OT | Total Shots | \n"
        body = body + "| ----- | ------- | -------- | -------- | ---- | ----------- | \n"
        body = body + "| " + away_name + " | " + str(period[0].get("away").get("shotsOnGoal")) + " | "
        body = body + str(period[1].get("away").get("shotsOnGoal")) + " | " + str(period[2].get("away").get("shotsOnGoal")) + " | "
        body = body + str(awayOtShots) + " | " + str(away_shots) + " | \n"
        body = body + "| " + home_name + " | " + str(period[0].get("home").get("shotsOnGoal")) + " | "
        body = body + str(period[1].get("home").get("shotsOnGoal")) + " | " + str(period[2].get("home").get("shotsOnGoal")) + " | "
        body = body + str(homeOtShots) + " | " + str(home_shots) + " | \n"
    #Power Play status
    body = body + "## Power Play \n"
    body = body + "| Team | On PowerPlay | \n"
    body = body + "| ----- | ------------ | \n"
    body = body + "| " + away_name + " | " + str(away_power) + " | \n"
    body = body + "| " + home_name + " | " + str(home_power) + " | \n"
    # game highlights
    r = requests.get("https://statsapi.web.nhl.com/api/v1/game/" + str(gamePK) + "/content")
    body = body + "# Game Highlights \n"
    try:
        for x in range(len(r.json().get("highlights").get("scoreboard").get("items"))):
            body = body + "\n" + "[" + r.json().get("highlights").get("scoreboard").get("items")[x].get("description") + "]("
            body = body + r.json().get("highlights").get("scoreboard").get("items")[x].get("playbacks")[3].get("url") + ") \n"
        return body, gameOver
    except:
        return body, GameOver
