# file author: Jimmy Teng

import plotly.graph_objects as go
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash import html
import time
import textwrap3

class Node:

    def __init__(self, name, state):
        self.name = str(name)
        self.users = state['user'][:]
        self.image = state['image']
        self.details = state['detail'][:]
        self.precedingNode = None
        self.followingNode = None
        self.visuable = True
        self.selector = True
        self.x = -1
        self.y = -1

    def resetSelector(self):
        self.selector = True
    
    def isPrecedingNode(self):
        return self.precedingNode
    
    def isFollowingNode(self):
        return self.followingNode
    
    def setPrecedingNode(self):
        self.precedingNode = True
        self.followingNode = False
    
    def setFollowingNode(self):
        self.precedingNode = False
        self.followingNode = True

    def setSelector(self, value):
        self.selector = value

    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
        
    def getID(self):
        return self.name
    
    def buildStateName(self, name):
        resStr = textwrap3.wrap(name, 15)
        name = "\n".join(resStr)
        return name
    
    def getLabel(self):
        if "+" in self.name:
            return self.buildStateName(self.name.split("+")[1])
        elif "vislevel" in self.name:
            return self.buildStateName(self.name.split("vislevel")[0])
        elif self.name == "VisStart":
            count = self.getUserCount()
            return f"{count} Players Start Here"
        else:
            return self.buildStateName(self.name)
        
    def getImage(self):
        return self.image
        
    def getUsers(self):
        return self.users
    
    def getUserCount(self):
        return len(self.users)
    
    def getDetails(self):
        return self.details
    
    def getVisitCount(self):
        return len(self.details)

    def getSelector(self):
        return self.selector

    def getVisuable(self):
        return self.visuable

    def setVisuable(self, visuable):
        self.visuable = visuable
    
    def addUsers(self, users):
        # print("new users", users)
        # print("existing users", self.users)
        for user in users:
            if user not in self.users:
                self.users.append(user)
    
    def addDetails(self, details):
        for detail in details:
            for selfDetail in self.details:
                if detail['user'] == selfDetail['user'] and detail['startTime'] == selfDetail['startTime'] and detail['endTime'] == selfDetail['endTime']:
                    continue
                else:
                    self.details.append(detail)
    
    def updateSelectorBasedOnHighlightsAndUsers(self, highlighters, selectedUsers):
        self.selector = False
        for detail in self.details:
            if detail["user"] in selectedUsers:
                flag = True
                for key, value in highlighters.items():
                    if value != None and detail[key] != value:
                        flag = False
                if flag:
                    self.selector = True
                    break

    def getUserCountInList(self, userList):
        count = 0
        for user in self.users:
            if user in userList:
                count += 1
        
        return count

    def getVisitCountInList(self, userList):
        count = 0
        for detail in self.details:
            if detail["user"] in userList:
                count += 1
        
        return count