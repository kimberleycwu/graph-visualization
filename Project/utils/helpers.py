# file author: Jimmy Teng

from dash import dcc, html
import os
import dash_bootstrap_components as dbc
import pandas as pd
import sys

from copy import deepcopy

from utils.constants import *
from views.login import CURRENTUSER
from app import app


def getData(DATASETFOLDER):
    files = []
    publicDataset = os.path.join(f"./Data/public/{DATASETFOLDER}")
    for file in os.listdir(publicDataset):
        if file == '.DS_Store':
            continue
        else:
            files.append(file)
    # try:
    #     privateDataset = os.path.join(f"./Data/private/{CURRENTUSER}/{DATASETFOLDER}")
    # except FileNotFoundError:
    #     os.makedirs(f".Data/private/{CURRENTUSER}/{DATASETFOLDER}")
    #     privateDataset = os.path.join(f"./Data/private/{CURRENTUSER}/{DATASETFOLDER}")
    # for file in os.listdir(privateDataset):
    #     if file == '.DS_Store':
    #         continue
    #     else:
    #         files.append(file)

    return files

def readData(filename): 
    df = pd.read_csv(f"./Data/public/{filename}")
    # print(df)
    dfWithoutIndex = pd.read_csv(f"./Data/public/{filename}", index_col=False)
    if 'Unnamed: 0' in list(df.columns):
        return df
    else:
        return dfWithoutIndex

def buildSequenceGraphStyle(sequenceGraph):
    # print(sequenceGraph.sequenceNetwork)
    if sequenceGraph.currentSequenceNetwork.isImageNetwork():
        styles = deepcopy(SEQUENCEGRAPHWITHIMAGESTYLE)
        maxNodeVisitCounts = sequenceGraph.getNodeMaxVisitCounts()
        minNodeVisitCounts = sequenceGraph.getNodeMinVisitCounts()
        maxEdgeVisitCounts = sequenceGraph.getEdgeMaxVisitCounts()
        minEdgeVisitCounts = sequenceGraph.getEdgeMinVisitCounts()
        for nodeID in sequenceGraph.getNodeIDs():
            nodeStyle = {}
            nodeStyle['selector'] = f'[image = \"{sequenceGraph.findNode(nodeID).getImage()}\"]'
            nodeStyle['style'] = {}
            nodeStyle['style']['background-fit'] = 'cover',
            nodeStyle['style']['background-image'] = app.get_asset_url(f'{sequenceGraph.findNode(nodeID).getImage()}')
            styles.append(nodeStyle)
        for style in styles:
            if style['selector'] == 'node':
                styleToChange = style['style']
                styleToChange['width'] = f'mapData(visitCounts, {minNodeVisitCounts}, {maxNodeVisitCounts}, 40, 100)'
                styleToChange['height'] = f'mapData(visitCounts, {minNodeVisitCounts}, {maxNodeVisitCounts}, 40, 100)'
            if style['selector'] == 'edge':
                styleToChange = style['style']
                styleToChange['width'] = f'mapData(visitCounts, {minEdgeVisitCounts}, {maxEdgeVisitCounts}, 2, 12)'
        return styles

    styles = []
    styles = deepcopy(SEQUENCEGRAPHSTYLE)
    maxNodeVisitCounts = sequenceGraph.getNodeMaxVisitCounts()
    minNodeVisitCounts = sequenceGraph.getNodeMinVisitCounts()
    maxEdgeVisitCounts = sequenceGraph.getEdgeMaxVisitCounts()
    minEdgeVisitCounts = sequenceGraph.getEdgeMinVisitCounts()
    
    # print(maxNodeVisitCounts, minNodeVisitCounts, maxEdgeVisitCounts, minEdgeVisitCounts)
    for style in styles:
        if style['selector'] == 'node':
            styleToChange = style['style']
            styleToChange['background-color'] = f'mapData(visitCounts, {minNodeVisitCounts}, {maxNodeVisitCounts}, rgb(255,255,255), rgb(0,0,255))'

        if style['selector'] == 'edge':
            styleToChange = style['style']
            styleToChange['width'] = f'mapData(visitCounts, {minEdgeVisitCounts}, {maxEdgeVisitCounts}, 2, 12)'
    
    addStyle = {}
    addStyle['selector'] = f'[visitCounts > {0.5*(maxNodeVisitCounts+minNodeVisitCounts)}]'
    addStyle['style'] = {}
    if minNodeVisitCounts == maxNodeVisitCounts:
        addStyle['style']['color'] = 'black'
    else:
        addStyle['style']['color'] = 'white'
    styles.append(addStyle)
    # print(styles)
    return styles

def generateFilterNames(filename):
    df = pd.read_csv(f"./Data/public/{filename}")
    # print(len(df))
    # dfWithoutIndex = pd.read_csv(f"./Data/public/{filename}", index_col=False)
    filterNames = []
    filterOptions = []
    for column in df.columns:
        if column.startswith("actionAttribute") or column.startswith("playerAttribute"):
            values = df[column].value_counts().keys()
            filterNames.append(column)
            filterOptions.append(values)
    return filterNames, filterOptions

def generateAttributeDetails(filename):
    df = pd.read_csv(f"./Data/public/{filename}")
    # print(len(df))
    # dfWithoutIndex = pd.read_csv(f"./Data/public/{filename}", index_col=False)
    attributeDetail = {}
    for column in df.columns:
        if column.startswith("actionAttribute") or column.startswith("playerAttribute"):
            values = df[column].value_counts().keys()
            attributeDetail[column] = values
    return attributeDetail

def generateHighlightersAndFilters(filterNames, filterOptions, highlighterName, filterName):
    highlighters = []
    filters = []
    for i in range(len(filterNames)):
        varName = filterNames[i]
        varOption = filterOptions[i]
        newHighlighterDropDown = dcc.Dropdown(
            varOption,
            placeholder=f"Select {varName}",
            id={
                "type":highlighterName,
                "index":f"{i}"
            },
            style={"width":"100%"}
        )
        newFilterDropDown = dcc.Dropdown(
            varOption,
            placeholder=f"Select {varName}",
            id={
                "type":filterName,
                "index":f"{i}"
            },
            style={"width":"100%"}
        )
        newHighlighterDiv = html.Div([
            html.Div(varName.split("_")[1], style={"width":"5rem", "display":"inline-block"}),
            newHighlighterDropDown,
            html.Br(),
        ], style={"display":"flex"})
        newFilterDiv = html.Div([
            html.Div(varName.split("_")[1], style={"width":"5rem", "display":"inline-block"}),
            newFilterDropDown,
            html.Br(),
        ], style={"display":"flex"})
        highlighters.append(newHighlighterDiv)
        filters.append(newFilterDiv)
    return highlighters, filters

# Activity
# ActivityName
def buildActionMapping(file):
    df = pd.read_csv(f"./Data/public/{file}")
    actionMapping = {"VisStart":"VisStart", "VisEnd":"VisEnd"}
    try:
        for index, row in df.iterrows():
            actionMapping[str(row["Activity"])] = row['ActivityName']
        # print(actionMapping)
    except KeyError as e:
        for index, row in df.iterrows():
            actionMapping[str(row["Activity"])] = str(row['Activity'])
    except:
        # print(actionMapping)
        print("error happening when create action mapping!")
        sys.exit(0)
    # print("GENERATE", actionMapping)
    return actionMapping