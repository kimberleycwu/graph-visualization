# file author: Jimmy Teng

import datetime
import sys
from nltk.util import ngrams, everygrams
# from TreeRequirement import *
from copy import copy, deepcopy
from utils.constants import *
import random
from PIL import Image
import pandas as pd

class SequenceNetwork:
    def __init__(self):
        # Identifier for different projects
        self.identifier = None

        # Fundamental Elements
        self.stateIDs = []
        self.linkIDs = []
        self.states = {}
        self.links = {}
        self.df = None

        # User States
        self.originalUserStates = None
        self.currentUserStates = None
        # NEW! (see line 251)
        self.actionAttributes = []

        # Other Elements for future usage
        self.userDic = {}
        self.sequenceAppearance = {}
        self.sequenceProb = {}
        self.sequenceDic = {}
    
    # Init the sequence graph from a CSV file
    def initFromCsv(self, file, identifier):
        # set the identifier
        self.identifier = identifier

        # set the df
        self.df = self.buildDf(file, identifier)

        # Build user states
        userStates = self.buildUserStatesFromCsv(identifier)
        self.originalUserStates = deepcopy(userStates)
        self.currentUserStates = deepcopy(userStates)

        # Build the elements
        self.buildStates()
        self.buildLinks()
        self.setNetworkAttributes()

    # Build the df from csv file
    def buildDf(self, filename, identier):
        if identier == "example":
            try:
                df = pd.read_csv(filename)
                return df
            except FileNotFoundError as e:
                return e
    
    # Build the user states
    def buildUserStatesFromCsv(self, identifier):
        userStates = {}

        # Find users in the data
        users = self.df["User ID"].value_counts()

        # Build user states for each user
        for user in users.keys():
            username = str(user)
            userDf = self.df[self.df["User ID"] == user]
            states = []

            # Build the start state
            if not userDf["Activity"].iloc[0] == "VisStart":
                state = self.buildStartStateForUser(userDf, identifier)
                states.append(state)

            # Build states
            for index, row in userDf.iterrows():
                state = self.buildStateForUser(row, identifier)
                states.append(state)

            # Build the end state
            if not userDf["Activity"].iloc[-1] == "VisEnd":
                state = self.buildEndStateForUser(userDf, identifier)
                states.append(state)

            userStates[username] = states 
        
        return userStates

    def buildStartStateForUser(self, userDf, identifier):
        state = {}
        if identifier == "example":
            state["Activity"] = "VisStart"
            state["StartTime"] = "0"
            state["EndTime"] = "1"
            if 'Image' in list(userDf.columns):
                state["Image"] = "start.png"
            else:
                state["Image"] = "None"
        
        return state
    
    def buildStateForUser(self, row, identifier):
        state = {}
        if identifier == "example":
            if row["Activity"] != "none":
                state["Activity"] = str(row["Activity"])
                state["StartTime"] = row["Start Time"]
                state["EndTime"] = row["End Time"]
            if 'Image' in list(row.keys()):
                state['Image'] = row['Image']
            else:
                state['Image'] = 'None'
        
        return state
    
    def buildEndStateForUser(self, userDf, identifier):
        state = {}
        if identifier == "example":
            state["Activity"] = "VisEnd"
            state["StartTime"] = "9998"
            state["EndTime"] = "9999"
            if 'Image' in list(userDf.columns):
                state["Image"] = "end.png"
            else:
                state["Image"] = "None" 
        return state

    def resetStatesAndLinks(self):
        self.stateIDs = []
        self.linkIDs = []
        self.states = {}
        self.links = {}
        self.sequenceAppearance = {}
        self.sequenceProb = {}
        self.sequenceDic = {}

    def isImageNetwork(self):
        # print(self.states)
        for state in self.states.keys():
            # print(state)
            # break
            if self.states[state]['image'] != "None":
                return True
        return False

    def refineUserStates(self, userStates):
        newUserStates = {}
        for user in userStates.keys():
            if "_" in user:
                newUser = user.replace("_", "-")
                self.userDic[newUser] = user
                newUserStates[newUser] = userStates[user]
            else:
                newUserStates[user] = userStates[user]
        # print(userStates.keys())
        # print(newUserStates.keys())
        return newUserStates

    def setOriginalUserState(self, userStates):
        self.originalUserStates = userStates

    def setNetworkAttributes(self):
        self.currentTotalUsers = self.getCurrentTotalUsers()
        self.totalNodeVisits = self.getTotalNodeVisits()
        self.totalEdgeVisits = self.getTotalLinkVisits()

    def getStates(self):
        return self.states
    
    def getLinks(self):
        return self.links

    def getCurrentTotalUsers(self):
        return len(list(self.currentUserStates.keys()))
    
    def getTotalNodeVisits(self):
        visits = 0
        for stateID in self.stateIDs:
            state = self.states[stateID]
            visits += len(state["detail"])
        return visits

    def getTotalLinkVisits(self):
        visits = 0
        for linkID in self.linkIDs:
            link = self.links[linkID]
            visits += len(link["detail"])
        return visits

    def getCurUserStates(self):
        return self.currentUserStates

    def getOriginalUserStates(self):
        return self.originalUserStates

    def getUserNames(self):
        return list(self.currentUserStates.keys())
    
    def getUniqueActions(self):
        try:
            return list(self.df["Activity"].value_counts().keys())
        except KeyError as e:
            print("No \"Activity\" column in the dataset")
            return []
    
    def getUniquePlayers(self):
        try:
            return list(self.df["User ID"].value_counts().keys())
        except KeyError as e:
            print("No \"User ID\" column in the dataset")
            return []
    
    def buildStates(self):
        self.stateIDs = []
        self.states = {}
        # for user, states in self.currentUserStates.items():
        #     print(user)
        #     print(states)
        #     break
        for user in self.currentUserStates.keys():
            for userState in self.currentUserStates[user]:
                stateID = userState['Activity']
                if stateID in self.stateIDs:
                    state = self.states[stateID]
                    users = state['user']
                    if user not in users:
                        state['user'].append(user)
                    detail = {}
                    detail['user'] = user
                    detail['startTime'] = userState['StartTime']
                    detail['endTime'] = userState['EndTime']
                    for actionAttribute in self.actionAttributes:
                        detail[actionAttribute] = userState[actionAttribute]
                    state['detail'].append(detail)
                else:
                    self.stateIDs.append(stateID)
                    self.states[stateID] = {}
                    self.states[stateID]['image'] = userState['Image']
                    self.states[stateID]['user'] = []
                    self.states[stateID]['detail'] = []
                    self.states[stateID]['user'].append(user)
                    detail = {}
                    detail['user'] = user
                    detail['startTime'] = userState['StartTime']
                    detail['endTime'] = userState['EndTime']
                    for actionAttribute in self.actionAttributes:
                        detail[actionAttribute] = userState[actionAttribute]
                    self.states[stateID]['detail'].append(detail)

    def buildLinks(self):
        self.linkIDs = []
        self.links = {}
        for user in self.currentUserStates.keys():
            for i in range(len(self.currentUserStates[user])):
                if i == len(self.currentUserStates[user]) - 1:
                    continue
                linkID = f"{self.currentUserStates[user][i]['Activity']}_{self.currentUserStates[user][i + 1]['Activity']}"
                if linkID in self.linkIDs:
                    link = self.links[linkID]
                    users = link['user']
                    if user not in users:
                        link['user'].append(user)
                    detail = {}
                    detail['user'] = user
                    detail['startTime'] = self.currentUserStates[user][i]['EndTime']
                    detail['endTime'] = self.currentUserStates[user][i + 1]['StartTime']
                    link['detail'].append(detail)
                else:
                    self.linkIDs.append(linkID)
                    self.links[linkID] = {}
                    self.links[linkID]['user'] = []
                    self.links[linkID]['detail'] = []
                    self.links[linkID]['user'].append(user)
                    detail = {}
                    detail['user'] = user
                    detail['startTime'] = self.currentUserStates[user][i]['EndTime']
                    detail['endtime'] = self.currentUserStates[user][i + 1]['StartTime']
                    self.links[linkID]['detail'].append(detail)
    
    def buildLinksBasedOnLinkIDs(self, newlinkIDs):
        self.linkIDs = []
        self.links = {}
        for user in self.currentUserStates.keys():
            for i in range(len(self.currentUserStates[user])):
                if i == len(self.currentUserStates[user]) - 1:
                    continue
                linkID = f"{self.currentUserStates[user][i]['Activity']}_{self.currentUserStates[user][i + 1]['Activity']}"
                if linkID in self.linkIDs:
                    link = self.links[linkID]
                    users = link['user']
                    if user not in users:
                        link['user'].append(user)
                    detail = {}
                    detail['user'] = user
                    detail['startTime'] = self.currentUserStates[user][i]['EndTime']
                    detail['endTime'] = self.currentUserStates[user][i + 1]['StartTime']
                    link['detail'].append(detail)
                elif linkID in newlinkIDs:
                    self.linkIDs.append(linkID)
                    self.links[linkID] = {}
                    self.links[linkID]['user'] = []
                    self.links[linkID]['detail'] = []
                    self.links[linkID]['user'].append(user)
                    detail = {}
                    detail['user'] = user
                    detail['startTime'] = self.currentUserStates[user][i]['EndTime']
                    detail['endtime'] = self.currentUserStates[user][i + 1]['StartTime']
                    self.links[linkID]['detail'].append(detail)
