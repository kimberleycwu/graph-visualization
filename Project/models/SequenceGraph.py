# file author: Jimmy Teng

import math
import sys
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, ttest_ind
from collections import Counter
from copy import copy, deepcopy
import plotly.graph_objects as go
from nltk.util import ngrams, everygrams

from models.Node import *
from models.Edge import *
from models.SequenceNetwork import *
from utils.constants import *
from statistics import mean, median
from utils.constants import *

from app import app
import os.path

class SequenceGraph:

    def __init__(self):
        # sequenceNetwork: Next Level Abstraction
        self.sequenceNetwork = None

        # Nodes & Edges: Graph Nodes and Edges
        self.nodes = []
        self.edges = []

        # Graph Element: Graph that returned to the Cytoscape graph
        # Graph Style: Graph style that returned to the Cytoscape graph
        self.originalGraphElement = []
        self.currentGraphElement = []
        self.originalGraphStyle = []
        self.currentGraphStyle = []

    def initFromSequenceNetwork(self, sequenceNetwork):
        self.sequenceNetwork = deepcopy(sequenceNetwork)
        self.buildOriginalGraph()

    def resetSequenceNetwork(self):
        self.sequenceNetwork = None
    
    def resetNodesAndEdges(self):
        self.nodes = []
        self.edges = []

    def resetOriginalGraphElement(self):
        self.originalGraphElement = []

    def resetCurrentGraphElement(self):
        self.currentGraphElement = []
    
    def resetOriginalGraphStyle(self):
        self.originalGraphStyle = []
    
    def resetCurrentGraphStyle(self):
        self.currentGraphStyle = []

    # Reset all Sequence Graph
    def resetAll(self):
        self.resetSequenceNetwork()
        self.resetNodesAndEdges()
        self.resetOriginalGraphElement()
        self.resetCurrentGraphElement()
        self.resetOriginalGraphStyle()
        self.resetCurrentGraphStyle()

    def copyOtherSequenceGraph(self, sequenceGraph):
        self.sequenceNetwork = deepcopy(sequenceGraph.sequenceNetwork)

        self.nodes = deepcopy(sequenceGraph.nodes)
        self.edges = deepcopy(sequenceGraph.edges)

        self.originalGraphElement = deepcopy(sequenceGraph.currentGraphElement)
        self.currentGraphElement = deepcopy(sequenceGraph.currentGraphElement)
        self.originalGraphStyle = deepcopy(sequenceGraph.currentGraphStyle)
        self.currentGraphStyle = deepcopy(sequenceGraph.currentGraphStyle)

    def isImageGraph(self):
        return self.currentSequenceNetwork.isImageNetwork()

    def findNode(self, nodeName):
        for node in self.nodes:
            if node.getID() == nodeName:
                return node
        
        return Node('emptyNode', {'image': 'None', 'user':[], 'detail':[]})

    def findEdge(self, edgeName):
        for edge in self.edges:
            if edge.getID() == edgeName:
                return edge
        
        return Edge('emptyEdge', {'user':[], 'detail':[]})
        
    def getNodeIDs(self):
        res = []
        for node in self.nodes:
            res.append(node.getID())
        return res

    def getEdgeIDs(self):
        res = []
        for edge in self.edges:
            res.append(edge.getID())
        return res

    def getNodeMaxVisitCounts(self):
        maxCounts = -math.inf
        for node in self.nodes:
            maxCounts = max(maxCounts, len(node.getDetails()))      
        return maxCounts

    def getNodeMinVisitCounts(self):
        minCounts = math.inf
        for node in self.nodes:
            minCounts = min(minCounts, len(node.getDetails()))
        return minCounts

    def getEdgeMaxVisitCounts(self):
        maxCounts = -math.inf
        for edge in self.edges:
            maxCounts = max(maxCounts,len(edge.getDetails()))
        return maxCounts

    def getEdgeMinVisitCounts(self):
        minCounts = math.inf
        for edge in self.edges:
            minCounts = min(minCounts, len(edge.getDetails()))
        return minCounts

    def getNodeMaxUserCounts(self):
        maxCounts = -math.inf
        for node in self.nodes:
            maxCounts = max(maxCounts, node.getUserCount())      
        return maxCounts
    
    def getNodeMinUserCounts(self):
        minCounts = math.inf
        for node in self.nodes:
            minCounts = min(minCounts, node.getUserCount())
        return minCounts
    
    def getEdgeMaxUserCounts(self):
        maxCounts = -math.inf
        for edge in self.edges:
            maxCounts = max(maxCounts, edge.getUserCount())
        return maxCounts
    
    def getEdgeMinUserCounts(self):
        minCounts = math.inf
        for edge in self.edges:
            minCounts = min(minCounts, edge.getUserCount())
        return minCounts

    def getCurrentStyle(self):
        return self.currentGraphStyle

    def getCurrentElements(self):
        return self.currentGraphElement

    # Constuct sequence graph given sequence network.
    def buildOriginalGraph(self):
        self.buildNodesAndEdges(self.sequenceNetwork)

        # Build Graph Elements and Styles
        self.originalGraphElement = self.buildGraphElementWithPosition()
        self.currentGraphElement = self.buildGraphElementWithPosition()

        if self.sequenceNetwork.isImageNetwork():
            self.originalGraphStyle = self.buildImageSequenceGraphStyle()
            self.currentGraphStyle = self.buildImageSequenceGraphStyle()
        else:
            self.originalGraphStyle = self.buildNoImageSequenceGraphStyle()
            self.currentGraphStyle = self.buildNoImageSequenceGraphStyle()

        self.originalTotalUsers = self.sequenceNetwork.getCurrentTotalUsers()
        self.currentTotalUsers = self.sequenceNetwork.getCurrentTotalUsers()

    def buildNodesAndEdges(self, sequenceNetwork):
        # Build nodes and edges
        self.nodes = []
        self.edges = []
        states = sequenceNetwork.getStates()
        links = sequenceNetwork.getLinks()
        # print(states)
        for stateName in states.keys():
            node = Node(stateName, states[stateName])
            self.nodes.append(node)
        for linkName in links.keys():
            edge = Edge(linkName, links[linkName])
            self.edges.append(edge)
        self.currentTotalUsers = sequenceNetwork.getCurrentTotalUsers()

    def rankNextNodes(self, root, edgesList):
        # print(edgesList)
        nextNodesList = []
        for edge in edgesList:
            if edge.getSource() == root.getID():
                if self.findNode(edge.getTarget()).getX() == -1 and self.findNode(edge.getTarget()).getY() == -1:
                    nextNodesList.append(self.findNode(edge.getTarget()))

        return nextNodesList
        # print(nextNodesList)

    def dfs(self, node, edgesList, x, y, nodesToVis):
        # print(node.getID(), x, y)
        while self.occupied(x, y):
            x += 150
        if node.getX() == -1 and node.getY() == -1:
            node.setX(x)
            node.setY(y)    
        
        x += 150

        nodeList = self.rankNextNodes(node, edgesList)
        
        for nextNode in nodeList:
            self.dfs(nextNode, edgesList, x, y,nodesToVis)
            y += 100 

    # NEW! originally found in example_files
    def occupied(self, x, y):
        for node in self.nodes:
            if node.getX() == x and node.getY() == y:
                return True
        return False
    
    # NEW! originally found in example_files
    def buildSequenceGraph(self):
        self.buildNodesAndEdges(self.sequenceNetwork)

        # Build Graph Elements and Styles
        self.originalGraphElement = self.buildGraphElementWithPosition()
        self.currentGraphElement = self.buildGraphElementWithPosition()

        if self.sequenceNetwork.isImageNetwork():
            self.originalGraphStyle = self.buildImageSequenceGraphStyle()
            self.currentGraphStyle = self.buildImageSequenceGraphStyle()
        else:
            self.originalGraphStyle = self.buildNoImageSequenceGraphStyle()
            self.currentGraphStyle = self.buildNoImageSequenceGraphStyle()

        self.originalTotalUsers = self.sequenceNetwork.getCurrentTotalUsers()
        self.currentTotalUsers = self.sequenceNetwork.getCurrentTotalUsers()

    def buildGraphElementWithPosition(self):
        graph = []
        rootNode = self.findNode("VisStart")
        self.dfs(rootNode, self.edges, 0, 0, self.nodes)
        for node in self.nodes:
            # print(node.getID(), node.getVisuable())
            if node.getVisuable():
                data = {}
                data['data'] = {}
                data['data']['id'] = node.getID()
                data['data']['label'] = node.getLabel()
                data['data']['image'] = node.getImage()
                data['data']['userCounts'] = len(node.getUsers())
                data['data']['visitCounts'] = len(node.getDetails())
                data["position"] = {}
                data["position"]["x"] = node.getX()
                data["position"]["y"] = node.getY()
                graph.append(data)
        for edge in self.edges:
            sourceNode = self.findNode(edge.getSource())
            targetNode = self.findNode(edge.getTarget())
            if edge.getVisuable() and sourceNode.getVisuable() and targetNode.getVisuable():
                data = {}
                data['data'] = {}
                data['data']['id'] = edge.getID()
                data['data']['source'] = edge.getSource()
                data['data']['target'] = edge.getTarget()
                data['data']['userCounts'] = len(edge.getUsers())
                data['data']['visitCounts'] = len(edge.getDetails())
                graph.append(data)
        return graph
            
    def buildNoImageSequenceGraphStyle(self):
        styles = []
        styles = deepcopy(SEQUENCEGRAPHSTYLE)
        # maxNodeVisitCounts = self.getNodeMaxVisitCounts()
        # minNodeVisitCounts = self.getNodeMinVisitCounts()
        # maxEdgeVisitCounts = self.getEdgeMaxVisitCounts()
        # minEdgeVisitCounts = self.getEdgeMinVisitCounts()
        
        maxNodeUserCounts = self.getNodeMaxUserCounts()
        minNodeUserCounts = self.getNodeMinUserCounts()
        maxEdgeUserCounts = self.getEdgeMaxUserCounts()
        minEdgeUserCounts = self.getEdgeMinUserCounts()

        for style in styles:
            if style['selector'] == 'node':
                styleToChange = style['style']
                styleToChange['background-color'] = f'mapData(userCounts, {minNodeUserCounts}, {maxNodeUserCounts}, rgb(255,255,255), rgb(0,0,255))'

            if style['selector'] == 'edge':
                styleToChange = style['style']
                styleToChange['width'] = f'mapData(userCounts, {minEdgeUserCounts}, {maxEdgeUserCounts}, 2, 12)'
        
        addStyle = {}
        addStyle['selector'] = f'[userCounts > {0.5*(maxNodeUserCounts+minNodeUserCounts)}]'
        addStyle['style'] = {}
        if minNodeUserCounts == maxNodeUserCounts:
            addStyle['style']['color'] = 'black'
        else:
            addStyle['style']['color'] = 'white'
        styles.append(addStyle)
        # print(styles)
        return styles

    def buildImageSequenceGraphStyle(self):
        # print(sequenceGraph.sequenceNetwork)
        styles = deepcopy(SEQUENCEGRAPHWITHIMAGESTYLE)
        # maxNodeVisitCounts = self.getNodeMaxVisitCounts()
        # minNodeVisitCounts = self.getNodeMinVisitCounts()
        # maxEdgeVisitCounts = self.getEdgeMaxVisitCounts()
        # minEdgeVisitCounts = self.getEdgeMinVisitCounts()
        maxNodeUserCounts = self.getNodeMaxUserCounts()
        minNodeUserCounts = self.getNodeMinUserCounts()
        maxEdgeUserCounts = self.getEdgeMaxUserCounts()
        minEdgeUserCounts = self.getEdgeMinUserCounts()

        for nodeID in self.getNodeIDs():
            nodeStyle = {}
            nodeStyle['selector'] = f'[image = \"{self.findNode(nodeID).getImage()}\"]'
            nodeStyle['style'] = {}
            nodeStyle['style']['background-fit'] = "cover"
            # print(self.findNode(nodeID).getImage())
            if os.path.isfile(f'./assets/{self.findNode(nodeID).getImage()}'):
                nodeStyle['style']['background-image'] = app.get_asset_url(f'{self.findNode(nodeID).getImage()}')
            else:
                nodeStyle['style']['background-image'] = app.get_asset_url("notfound.png")
            styles.append(nodeStyle)
        for style in styles:
            if style['selector'] == 'node':
                styleToChange = style['style']
                styleToChange['width'] = f'mapData(userCounts, {minNodeUserCounts}, {maxNodeUserCounts}, 40, 100)'
                styleToChange['height'] = f'mapData(userCounts, {minNodeUserCounts}, {maxNodeUserCounts}, 40, 100)'
            if style['selector'] == 'edge':
                styleToChange = style['style']
                styleToChange['width'] = f'mapData(userCounts, {minEdgeUserCounts}, {maxEdgeUserCounts}, 2, 12)'
        # print(styles)
        return styles
