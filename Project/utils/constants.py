# file author: Jimmy Teng

INFINITE_SIMILARITY = 50000
SEQUENCEGRAPHSTYLE=[
                        {
                            'selector': 'node',
                            'style': {
                                'label': 'data(label)',
                                'color':'black',
                                'text-halign':'center',
                                'text-valign':'center',
                                'text-wrap': 'wrap',
                                'width':'label',
                                'height':'label',
                                'shape':'round-rectangle',
                                'border-width':'2px',
                                'border-style':'solid',
                                'border-color':'black',
                                # 'background-color':'mapData(visitCounts, 700, 1700, white, blue)',
                                'padding':'2px',
                            }
                        },
                        {
                            'selector': 'edge',
                            'style': {
                                'curve-style': 'unbundled-bezier',
                                # 'label': 'bezier',
                                'target-arrow-shape': 'triangle',
                                'arrow-scale': 2,
                            }
                        }
                    ]

SEQUENCEGRAPHWITHIMAGESTYLE=[
                        {
                            'selector': 'node',
                            'style': {
                                'width': 90,
                                'height': 80,
                                'border-color': '#000000',
                                'border-width': 5,
                            }
                        },
                        {
                            'selector': 'edge',
                            'style': {
                                'curve-style': 'unbundled-bezier',
                                # 'label': 'bezier',
                                'target-arrow-shape': 'triangle',
                            }
                        }
                    ]

SEQUENCEGRAPHSTYLEINCIRCLENODES=[
                        {
                            'selector': 'node',
                            'style': {
                                'label': 'data(label)',
                                'background-color':'white',
                                'width':'10',
                                'height':'10',
                                'border-width':'2px',
                                'border-style':'solid',
                                'border-color':'black',
                                'padding':'2px',
                            }
                        },
                        {
                            'selector': 'edge',
                            'style': {
                                'curve-style': 'unbundled-bezier',
                                # 'label': 'bezier',
                                'target-arrow-shape': 'triangle',
                                'arrow-scale': 2,
                            }
                        }
                    ]

SEGMENTATIONGRAPHSTYLE = [{'selector': 'node', 
                            'style': {'label': 'data(label)', 
                                        'color': 'black', 
                                        'text-halign': 'center', 
                                        'text-valign': 'center', 
                                        'text-wrap': 'wrap', 
                                        'width': 'label', 
                                        'height': 'label', 
                                        'shape': 'round-rectangle', 
                                        'border-width': '2px', 
                                        'border-style': 'solid', 
                                        'border-color': 'black', 
                                        'padding': '2px'}}, 
                        {'selector': 'edge', 
                            'style': {'curve-style': 'unbundled-bezier', 
                                        'target-arrow-shape': 'triangle'}}]
                                        
TREEGRAPHSTYLE=[
                        {
                            'selector': 'node',
                            'style': {
                                'label': 'data(label)',
                                'color':'black',
                                'text-halign':'center',
                                'text-valign':'center',
                                'text-wrap': 'wrap',
                                'width':'label',
                                'height':'label',
                                'shape':'round-rectangle',
                                'border-width':'2px',
                                'border-style':'solid',
                                'border-color':'black',
                                'background-color':'white',
                                'padding':'2px',
                            }
                        },
                        {
                            'selector': 'edge',
                            'style': {
                                'curve-style': 'unbundled-bezier',  
                                'target-arrow-shape': 'triangle',
                            }
                        },
                        {
                            'selector': "[relation = 'or']",
                            'style': {
                                'line-style':'dashed', 
                            }
                        },
                        {
                            'selector': '[relation = "and"]',
                            'style': {
                                'line-style':'solid', 
                            }
                        },
                    ]

CORRELATIONGRAPHSTYLE=[
                        {
                            'selector': 'node',
                            'style': {
                                'label': 'data(label)',
                                'color':'black',
                                'text-halign':'center',
                                'text-valign':'center',
                                'width':'label',
                                'height':'label',
                                'shape':'round-rectangle',
                                'border-width':'2px',
                                'border-style':'solid',
                                'border-color':'black',
                                'padding':'2px',
                                'background-color':'white',
                            }
                        },
                        {
                            'selector': 'edge',
                            'style': {
                                'curve-style': 'unbundled-bezier', 
                            }
                        },
                        {
                            'selector': '[correlation > 0]',
                            'style': {
                                'line-style':'solid', 
                            }
                        },
                        {
                            'selector': '[correlation < 0]',
                            'style': {
                                'line-style':'dashed', 
                            }
                        }
                    ]

EXPLANABILITYGRAPHSTYLE = [
    {
        "selector": "node",
        "style": {
            'label': 'data(label)',
            'text-halign':'center',
            'text-valign':'center',
            'text-wrap': 'wrap',
            'width':'label',
            'height':'label',
            'shape':'round-rectangle',
            'color':'black',
        },
    },
    {
        'selector': 'edge',
        'style': {
            'curve-style': 'unbundled-bezier',
            # 'label': 'bezier',
            'target-arrow-shape': 'triangle',
            'arrow-scale': 2,
        }
    },
]

EXPLAINABILITYPLAYERCLUSTERGRAPHSTYLE = [
     {
        'selector': 'node',
        'style': {
            'content': 'data(label)'
        }
    },
]

EXPLAINABILITYGRAPHSTYLE = [
    {
        'selector': 'node',
        'style': {
            'label': 'data(label)',
            'color':'black',
            'text-halign':'center',
            'text-valign':'center',
            'text-wrap': 'wrap',
            'width':'label',
            'height':'label',
            'shape':'round-rectangle',
            'border-width':'2px',
            'border-style':'solid',
            'border-color':'black',
            # 'background-color':'mapData(visitCounts, 700, 1700, white, blue)',
            'padding':'2px',
        }
    },
    {
        'selector': 'edge',
        'style': {
            'curve-style': 'unbundled-bezier',
            # 'label': 'bezier',
            'target-arrow-shape': 'triangle',
            'arrow-scale': 2,
        }
    },
    {
        'selector': '[label *= "coral"]',
        'style': {
            'background-color': '#208eb7',
        }
    },
    {
        'selector': '[label *= "bayou"]',
        'style': {
            'background-color': '#7fac0c',
        }
    },
    {
        'selector': '[label *= "kelp"]',
        'style': {
            'background-color': '#dc9d7f',
        }
    },
    {
        'selector': '[label *= "arctic"]',
        'style': {
            'background-color': '#43e26d',
        }
    },
]


DEFUALT_MARKER = {  0: {'label': '0'},
                    20: {'label': '20'},
                    40: {'label': '40'},
                    60: {'label': '60'},
                    80: {'label': '80'},
                    100: {'label': '100'}}

SKILLNAMEMAPPING = {'62698': 'Shattering Ice', '62887': 'Crescent Wind', '5737': 'Lightning Storm', '62812': 'Hurricane of Pain', '62716': 'Shock Blast', '5492': 'Fire Attunement', '62758': 'Flame Wheel', '62876': 'Grand Finale', '62965': 'Relentless Fire', '62925': 'Singeing Strike', '62910': 'Molten End', '62807': 'Triple Sear', '62884': 'Surging Flames', '5495': 'Earth Attunement', '62975': 'Rocky Loop', '62976': 'Whirling Stones', '62778': 'Ground Pound', '5493': 'Water Attunement', '62865': 'Stream Strike', '62834': 'Icy Coil', '62958': 'Rain of Blows', '62948': 'Crashing Font', '62843': 'Cleansing Typhoon', '5494': 'Air Attunement', '62747': 'Wind Slam', '5516': 'Conjure Fiery Greatsword', '-2': 'Weapon Swap', '5517': 'Fiery Rush', '5531': 'Firestorm', '62683': 'Stonestrike', '62694': 'Water Rush', '62862': 'Chilling Crack', '23275': 'Dodge', '5548': 'Lava Font', '5679': 'Flame Burst', '5501': 'Meteor Shower', '5550': 'Ice Spike', '5515': 'Frozen Ground', '5681': 'Geyser', '5551': 'Healing Rain', '5549': 'Water Blast', '5528': 'Eruption', '5683': 'Unsteady Ground', '5686': 'Shock Wave', '51684': 'Transmute Earth', '5519': 'Stoning', '12836': 'Water Blast Combo', '5518': 'Chain Lightning', '5552': 'Lightning Surge', '5491': 'Fireball', '5682': 'Windborne Speed', '62827': 'Soothing Water', '5553': 'Gust', '5671': 'Static Field', '5736': 'Firestorm', '1066': 'Resurrect', '25491': 'Glyph of Elementals', '5735': 'Ice Storm', '5504': 'Discharge Lightning', '1175': 'Bandage', '5532': 'Flame Wave', '34651': 'Glyph of Elemental Harmony', '5505': 'Grasping Earth', '62947': 'Wind Storm', '34724': 'Glyph of Elemental Harmony', '62725': 'Elemental Celerity', '5641': 'Arcane Shield', '62992': 'Immutable Stone', '25488': 'Glyph of Elementals', '34743': 'Glyph of Elemental Harmony', '5738': 'Sandstorm', '62777': '62777', '25486': 'Glyph of Lesser Elementals', '21656': 'Arcane Brilliance', '5533': 'Fiery Eruption', '5567': 'Conjure Frost Bow', '5723': 'Frost Storm', '5568': 'Frost Fan', '5595': 'Water Arrow', '34609': 'Glyph of Elemental Harmony', '5720': 'Frost Volley', '25490': 'Glyph of Elementals', '9292': 'Lightning Strike', '5508': 'Flamestrike', '5675': 'Phoenix', '5497': 'Flamewall', '5692': "Dragon's Tooth", '5542': 'Signet of Fire', '51711': 'Transmute Fire', '5562': 'Gale', '5526': 'Arc Lightning', '5561': 'Lightning Strike', '5530': 'Swirling Winds', '5503': 'Signet of Restoration', '5721': 'Deep Freeze', '5693': 'Ice Shards', '5510': 'Water Trident', '5538': 'Shatterstone', '5490': 'Comet', '5507': 'Ether Renewal', '5570': 'Signet of Water', '9433': 'Ring of Earth', '56885': 'Earthen Blast', '25495': 'Glyph of Lesser Elementals', '5763': 'Renewal of Water', '5539': 'Arcane Blast', '25487': 'Glyph of Lesser Elementals', '5543': 'Mist Form', '5571': 'Signet of Earth'}

REGIONCOUNTRYDICT = {"North America": ["Auckland","Boston","Chicago","Denver","Los Angeles","Montreal","New York","Philadelphia", "Phoenix", "San Francisco", "San José", "Seattle", "Toronto", "Vancouver", "Washington D.C."],
                        "Africa": ["Cape Town","Nairobi","Abuja","Lagos","Cairo","Rabat"],
                        "Asia": ["Ankara","Bengaluru","Busan","Hong Kong","Hyderabad","Istanbul","Jakarta","Kuala Lumpur","Makassar","Manila","Medina","Moscow","Mumbai","Nanjing","New Delhi","St. Petersburg"],
                        "Asia/ Far East":["Bangkok","Beijing","Chengdu","Chongqing","Guangzhou","Hangzhou","Hanoi","Ho Chi Minh City","Medan","Osaka","Seoul","Shanghai","Shenzhen","Singapore","Taipei City","Tianjin","Tokyo","Zhuhai"],
                        "Australia":["Brisbane", "Melbourne", "Sydney"],
                        "Europe":["Amsterdam","Ankara","Athens","Barcelona","Berlin","Bilbao","Birmingham","Bologna","Bordeaux","Bratislava","Brussels","Bucharest","Budapest","Copenhagen","Dublin","Dusseldorf","Geneva","Glasgow","Gothenburg","Hamburg","Hanover","Helsinki","Istanbul","Kiel","Krakow","Kyiv","Lausanne","Leeds","Lille","Lisbon","London","Lyon","Madrid","Manchester","Marseille","Milan","Munich","Newcastle","Oslo","Paris","Prague","Rome","Rotterdam","Sofia","Stockholm","Tallinn","The Hague","Vienna","Warsaw","Zaragoza","Zurich"],
                        "Middle East":["Abu Dhabi","Dubai","Riyadh","Tel Aviv"],
                        "South America":["Bogota","Buenos Aires","Medellin","Mexico City","Rio de Janeiro","Santiago","Sao Paulo"]}

CATEGORYINDICATORDICT = {"Priorities":["affordable housing","fulfilling employment","unemployment","basic amenities","school education","air pollution","road congestion","green spaces","public transport","recycling","security","citizen engagement","social mobility","corruption","health services"],
                            "Attitude":["You are willing to concede personal data in order to improve traffic congestion", "You are comfortable with face recognition technologies to lower crime", "You feel the availability of online information has increased your trust in authorities", "The proportion of your day-to-day payment transactions that are non-cash (% of transactions)"],
                            "Health & Safety: STRUCTURES":["Basic sanitation meets the needs of the poorest areas","Recycling services are satisfactory","Public safety is not a problem","Air pollution is not a problem","Medical services provision is satisfactory","Finding housing with rent equal to 30% or less of a monthly salary is not a problem"],
                            "Health & Safety: TECHNOLOGIES":["Online reporting of city maintenance problems provides a speedy solution","A website or App allows residents to easily give away unwanted items","Free public wifi has improved access to city services","CCTV cameras has made residents feel safer","A website or App allows residents to effectively monitor air pollution","Arranging medical appointments online has improved access"],
                            "Mobility: Structures":["Traffic congestion is not a problem","Public transport is satisfactory"],
                            "Mobility: technologies":["Car-sharing Apps have reduced congestion","Apps that direct you to an available parking space have reduced journey time","Bicycle hiring has reduced congestion","Online scheduling and ticket sales has made public transport easier to use","The city provides information on traffic congestion through mobile phones"],
                            "Activities: structures":["Green spaces are satisfactory","Cultural activities (shows, bars, and museums) are satisfactory"],
                            "Activities: technologies":["Online purchasing of tickets to shows and museums has made it easier to attend"],
                            "Opportunities (Work & School): Structures":["Employment finding services are readily available","Most children have access to a good school","Lifelong learning opportunities are provided by local institutions","Businesses are creating new jobs","Minorities feel welcome"],
                            "Opportunities (Work & School): Technologies":["Online access to job listings has made it easier to find work","IT skills are taught well in schools","Online services provided by the city has made it easier to start a new business","The current internet speed and reliability meet connectivity needs"],
                            "Governance: Structures":["Information on local government decisions are easily accessible","Corruption of city officials is not an issue of concern","Residents contribute to decision making of local government","Residents provide feedback on local government projects"],
                            "Governance: Technologies":["Online public access to city finances has reduced corruption","Online voting has increased participation","An online platform where residents can propose ideas has improved city life","Processing Identification Documents online has reduced waiting times"]}

CATEGORYFILEDICT = {"Priorities": "Priorities",
                    "Attitude": "Attitudes",
                    "Health & Safety: STRUCTURES": "Health&Safety",
                    "Health & Safety: TECHNOLOGIES": "Health&Safety",
                    "Mobility: Structures": "Mobility",
                    "Mobility: technologies": "Mobility",
                    "Activities: structures": "Activities",
                    "Activities: technologies": "Activities",
                    "Opportunities (Work & School): Structures": "Opportunities",
                    "Opportunities (Work & School): Technologies": "Opportunities",
                    "Governance: Structures": "Governance",
                    "Governance: Technologies": "Governance"}

COLORPALETTE = {"incoming":"#FFC107", "clicked":"#E4370E", "outgoing":"#987A43", "cycle":"#50A409"}

