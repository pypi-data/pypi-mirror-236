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
import sys
import time
from plemmy import LemmyHttp
from plemmy.responses import GetCommunityResponse
from datetime import datetime
import os.path
import sqlite3

def draft():
    finished = False
    finishedR1 = False
    draftYear = datetime.now().year
    # talk to sqlite database
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

    #begin main program
    round1 = input("Is this the first Round? (y/n) ")
    round1 = round1.lower()
    srv = LemmyHttp(server)
    srv.key = token
    requested = False
    while(requested == False):
        try:
            CID = GetCommunityResponse(srv.get_community(name=communityName)).community_view.community.id
            requested = True
        except:
            print("failed to get community, trying again")
    requested = False
    while(requested == False):
        try:
            post = srv.create_post(CID, str(draftYear) + " Draft!", body="")
            postID = post.json().get("post_view")
            postID = postID["post"].get("id")
            requested = True
        except:
            print("failed to create post, trying again.")


    while(True):
        r = requests.get("https://statsapi.web.nhl.com/api/v1/draft")
        lister = r.json().get("drafts")[0].get("rounds")
        teams = lister[0].get("picks")
        body = ""
        body2 = ""
        body3 = ""
        body4 = ""
        body5 = ""
        body6 = ""
        body7 = ""
        i = 0
        # Round 1
        j = len(teams)
        body = "# Round 1 \n" + "| Team Name | Pick # | Selection | \n"
        body = body + "| -------- | ------- | -------- |\n"
        while(i < j):
            #print(i)
            #teams[i].get("team")
            body = body + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
            if(str(teams[i].get("prospect").get("fullName")) != ""):
                finishedR1 = True
            i = i + 1

        #Round 2
        teams = lister[1].get("picks")
        i = 0
        j = len(teams)
        body2 = "# Round 2 \n" + "| Team Name | Pick # | Selection | \n"
        body2 = body2 + "| -------- | ------- | -------- |\n"
        while(i < j):
            #print(i)
            #teams[i].get("team")
            body2 = body2 + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
            i = i + 1

        #Round 3
        teams = lister[2].get("picks")
        i = 0
        j = len(teams)
        body3 = "# Round 3 \n" + "| Team Name | Pick # | Selection | \n"
        body3 = body3 + "| -------- | ------- | -------- |\n"
        while(i < j):
            #print(i)
            #teams[i].get("team")
            body3 = body3 + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
            i = i + 1

        #Round 4
        teams = lister[3].get("picks")
        i = 0
        j = len(teams)
        body4 = "# Round 4 \n" + "| Team Name | Pick # | Selection | \n"
        body4 = body4 + "| -------- | ------- | -------- |\n"
        while(i < j):
            #print(i)
            #teams[i].get("team")
            body4 = body4 + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
            i = i + 1

        #Round 5
        teams = lister[4].get("picks")
        i = 0
        j = len(teams)
        body5 = "# Round 5 \n" + "| Team Name | Pick # | Selection | \n"
        body5 = body5 + "| -------- | ------- | -------- |\n"
        while(i < j):
            #print(i)
            #teams[i].get("team")
            body5 = body5 + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
            i = i + 1

        #Round 6
        teams = lister[5].get("picks")
        i = 0
        j = len(teams)
        body6 = "# Round 6 \n" + "| Team Name | Pick # | Selection | \n"
        body6 = body6 + "| -------- | ------- | -------- |\n"
        while(i < j):
            body6 = body6 + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
            i = i + 1

        #Round 7
        teams = lister[6].get("picks")
        i = 0
        j = len(teams)
        body7 = "# Round 7 \n" + "| Team Name | Pick # | Selection | \n"
        body7 = body7 + "| -------- | ------- | -------- |\n"
        while(i < j):
            body7 = body7 + str(teams[i].get("team").get("name")) + " | " + str(teams[i].get("pickOverall")) + " | " + str(teams[i].get("prospect").get("fullName")) + " | \n"
            if(str(teams[i].get("prospect").get("fullName")) != ""):
                finished = True
            i = i + 1

        #update post this requires timeout enabled in plemmy, pull request has been submitted to get it merged upstream.
        try:
            srv.edit_post(postID, body=body+body2+body3+body4+body5+body6+body7)
        except:
            print("failed to contact server. Adding extra 60 seconds before retrying")
            time.sleep(60)
        if(finished == True and round1 == "n"):
            sys.exit()
        elif(finishedR1 == True and round1 == "y"):
            sys.exit()
        time.sleep(120)
