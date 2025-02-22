# file author: Jimmy Teng

import plotly.graph_objects as go
import pandas as pd
import dash
from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash import html
import time

class Edge:

    def __init__(self, name, link):
        self.id = name
        self.users = link['user'][:]
        self.source = name.split("_")[0]
        self.target = name.split("_")[1]
        self.precedingEdge = None
        self.followingEdge = None
        self.details = link['detail'][:]
        self.selector = True
        self.visuable = True

    def resetSelector(self):
        self.selector = True

    def isPrecedingEdge(self):
        return self.precedingEdge
    
    def isFollowingEdge(self):
        return self.followingEdge
    
    def setPrecedingEdge(self):
        self.precedingEdge = True
        self.followingEdge = False
    
    def setFollowingEdge(self):
        self.precedingEdge = False
        self.followingEdge = True

    def setSelector(self, value):
        self.selector = value
    
    def getID(self):
        return self.id

    def getUsers(self):
        return self.users
    
    def getUserCount(self):
        return len(self.users)

    def getSource(self):
        return self.source

    def getTarget(self):
        return self.target

    def getDetails(self):
        return self.details
    
    def getVisitCount(self):
        return len(self.details)

    def getVisuable(self):
        return self.visuable

    def getSelector(self):
        return self.selector

    def setVisuable(self, visuable):
        self.visuable = visuable

    def addUsers(self, users):
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

    def updateSelectorBasedOnUsers(self, selectedUsers):
        self.selector = False
        for detail in self.details:
            if detail["user"] in selectedUsers:
                self.selector = True
    
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