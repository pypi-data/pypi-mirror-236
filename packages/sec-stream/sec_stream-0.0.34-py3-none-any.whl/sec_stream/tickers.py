tickers = r'''{
    "AAPL": {
        "cik": 320193,
        "title": "Apple Inc."
    },
    "MSFT": {
        "cik": 789019,
        "title": "MICROSOFT CORP"
    },
    "GOOGL": {
        "cik": 1652044,
        "title": "Alphabet Inc."
    },
    "AMZN": {
        "cik": 1018724,
        "title": "AMAZON COM INC"
    },
    "NVDA": {
        "cik": 1045810,
        "title": "NVIDIA CORP"
    },
    "BRK-B": {
        "cik": 1067983,
        "title": "BERKSHIRE HATHAWAY INC"
    },
    "META": {
        "cik": 1326801,
        "title": "Meta Platforms, Inc."
    },
    "TSLA": {
        "cik": 1318605,
        "title": "Tesla, Inc."
    },
    "LLY": {
        "cik": 59478,
        "title": "ELI LILLY & Co"
    },
    "V": {
        "cik": 1403161,
        "title": "VISA INC."
    },
    "TSM": {
        "cik": 1046179,
        "title": "TAIWAN SEMICONDUCTOR MANUFACTURING CO LTD"
    },
    "UNH": {
        "cik": 731766,
        "title": "UNITEDHEALTH GROUP INC"
    },
    "XOM": {
        "cik": 34088,
        "title": "EXXON MOBIL CORP"
    },
    "JNJ": {
        "cik": 200406,
        "title": "JOHNSON & JOHNSON"
    },
    "JPM": {
        "cik": 19617,
        "title": "JPMORGAN CHASE & CO"
    },
    "LVMUY": {
        "cik": 824046,
        "title": "LVMH MOET HENNESSY LOUIS VUITTON"
    },
    "WMT": {
        "cik": 104169,
        "title": "Walmart Inc."
    },
    "NVO": {
        "cik": 353278,
        "title": "NOVO NORDISK A S"
    },
    "SPY": {
        "cik": 884394,
        "title": "SPDR S&P 500 ETF TRUST"
    },
    "MA": {
        "cik": 1141391,
        "title": "Mastercard Inc"
    },
    "PG": {
        "cik": 80424,
        "title": "PROCTER & GAMBLE Co"
    },
    "AVGO": {
        "cik": 1730168,
        "title": "Broadcom Inc."
    },
    "LTMAY": {
        "cik": 1047716,
        "title": "LATAM AIRLINES GROUP S.A."
    },
    "HD": {
        "cik": 354950,
        "title": "HOME DEPOT, INC."
    },
    "ORCL": {
        "cik": 1341439,
        "title": "ORACLE CORP"
    },
    "CVX": {
        "cik": 93410,
        "title": "CHEVRON CORP"
    },
    "MRK": {
        "cik": 310158,
        "title": "Merck & Co., Inc."
    },
    "ABBV": {
        "cik": 1551152,
        "title": "AbbVie Inc."
    },
    "ASML": {
        "cik": 937966,
        "title": "ASML HOLDING NV"
    },
    "KO": {
        "cik": 21344,
        "title": "COCA COLA CO"
    },
    "PEP": {
        "cik": 77476,
        "title": "PEPSICO INC"
    },
    "COST": {
        "cik": 909832,
        "title": "COSTCO WHOLESALE CORP /NEW"
    },
    "ADBE": {
        "cik": 796343,
        "title": "ADOBE INC."
    },
    "BAC": {
        "cik": 70858,
        "title": "BANK OF AMERICA CORP /DE/"
    },
    "BABA": {
        "cik": 1577552,
        "title": "Alibaba Group Holding Ltd"
    },
    "CSCO": {
        "cik": 858877,
        "title": "CISCO SYSTEMS, INC."
    },
    "TM": {
        "cik": 1094517,
        "title": "TOYOTA MOTOR CORP/"
    },
    "NVS": {
        "cik": 1114448,
        "title": "NOVARTIS AG"
    },
    "AZN": {
        "cik": 901832,
        "title": "ASTRAZENECA PLC"
    },
    "PFE": {
        "cik": 78003,
        "title": "PFIZER INC"
    },
    "TMO": {
        "cik": 97745,
        "title": "THERMO FISHER SCIENTIFIC INC."
    },
    "SHEL": {
        "cik": 1306965,
        "title": "Shell plc"
    },
    "MCD": {
        "cik": 63908,
        "title": "MCDONALDS CORP"
    },
    "FMX": {
        "cik": 1061736,
        "title": "MEXICAN ECONOMIC DEVELOPMENT INC"
    },
    "CRM": {
        "cik": 1108524,
        "title": "Salesforce, Inc."
    },
    "ACN": {
        "cik": 1467373,
        "title": "Accenture plc"
    },
    "CMCSA": {
        "cik": 1166691,
        "title": "COMCAST CORP"
    },
    "DHR": {
        "cik": 313616,
        "title": "DANAHER CORP /DE/"
    },
    "LIN": {
        "cik": 1707925,
        "title": "LINDE PLC"
    },
    "ABT": {
        "cik": 1800,
        "title": "ABBOTT LABORATORIES"
    },
    "NFLX": {
        "cik": 1065280,
        "title": "NETFLIX INC"
    },
    "AMD": {
        "cik": 2488,
        "title": "ADVANCED MICRO DEVICES INC"
    },
    "SAP": {
        "cik": 1000184,
        "title": "SAP SE"
    },
    "TMUS": {
        "cik": 1283699,
        "title": "T-Mobile US, Inc."
    },
    "HDB": {
        "cik": 1144967,
        "title": "HDFC BANK LTD"
    },
    "NKE": {
        "cik": 320187,
        "title": "NIKE, Inc."
    },
    "DIS": {
        "cik": 1744489,
        "title": "Walt Disney Co"
    },
    "WFC": {
        "cik": 72971,
        "title": "WELLS FARGO & COMPANY/MN"
    },
    "TXN": {
        "cik": 97476,
        "title": "TEXAS INSTRUMENTS INC"
    },
    "TTE": {
        "cik": 879764,
        "title": "TotalEnergies SE"
    },
    "HSBC": {
        "cik": 1089113,
        "title": "HSBC HOLDINGS PLC"
    },
    "PM": {
        "cik": 1413329,
        "title": "Philip Morris International Inc."
    },
    "UPS": {
        "cik": 1090727,
        "title": "UNITED PARCEL SERVICE INC"
    },
    "QQQ": {
        "cik": 1067839,
        "title": "INVESCO QQQ TRUST, SERIES 1"
    },
    "BHP": {
        "cik": 811809,
        "title": "BHP Group Ltd"
    },
    "COP": {
        "cik": 1163165,
        "title": "CONOCOPHILLIPS"
    },
    "CAT": {
        "cik": 18230,
        "title": "CATERPILLAR INC"
    },
    "MS": {
        "cik": 895421,
        "title": "MORGAN STANLEY"
    },
    "AMGN": {
        "cik": 318154,
        "title": "AMGEN INC"
    },
    "VZ": {
        "cik": 732712,
        "title": "VERIZON COMMUNICATIONS INC"
    },
    "INTC": {
        "cik": 50863,
        "title": "INTEL CORP"
    },
    "BA": {
        "cik": 12927,
        "title": "BOEING CO"
    },
    "INTU": {
        "cik": 896878,
        "title": "INTUIT INC."
    },
    "UNP": {
        "cik": 100885,
        "title": "UNION PACIFIC CORP"
    },
    "NEE": {
        "cik": 753308,
        "title": "NEXTERA ENERGY INC"
    },
    "SNY": {
        "cik": 1121404,
        "title": "Sanofi"
    },
    "BMY": {
        "cik": 14272,
        "title": "BRISTOL MYERS SQUIBB CO"
    },
    "IBM": {
        "cik": 51143,
        "title": "INTERNATIONAL BUSINESS MACHINES CORP"
    },
    "LOW": {
        "cik": 60667,
        "title": "LOWES COMPANIES INC"
    },
    "UL": {
        "cik": 217410,
        "title": "UNILEVER PLC"
    },
    "RY": {
        "cik": 1000275,
        "title": "ROYAL BANK OF CANADA"
    },
    "RTX": {
        "cik": 101829,
        "title": "RTX Corp"
    },
    "AMAT": {
        "cik": 6951,
        "title": "APPLIED MATERIALS INC /DE"
    },
    "HON": {
        "cik": 773840,
        "title": "HONEYWELL INTERNATIONAL INC"
    },
    "QCOM": {
        "cik": 804328,
        "title": "QUALCOMM INC/DE"
    },
    "SPGI": {
        "cik": 64040,
        "title": "S&P Global Inc."
    },
    "GE": {
        "cik": 40545,
        "title": "GENERAL ELECTRIC CO"
    },
    "BX": {
        "cik": 1393818,
        "title": "Blackstone Inc."
    },
    "AXP": {
        "cik": 4962,
        "title": "AMERICAN EXPRESS CO"
    },
    "DE": {
        "cik": 315189,
        "title": "DEERE & CO"
    },
    "LMT": {
        "cik": 936468,
        "title": "LOCKHEED MARTIN CORP"
    },
    "TD": {
        "cik": 947263,
        "title": "TORONTO DOMINION BANK"
    },
    "BKNG": {
        "cik": 1075531,
        "title": "Booking Holdings Inc."
    },
    "NOW": {
        "cik": 1373715,
        "title": "ServiceNow, Inc."
    },
    "BUD": {
        "cik": 1668717,
        "title": "Anheuser-Busch InBev SA/NV"
    },
    "EADSY": {
        "cik": 1378580,
        "title": "Airbus SE/ADR"
    },
    "SBUX": {
        "cik": 829224,
        "title": "STARBUCKS CORP"
    },
    "PLD": {
        "cik": 1045609,
        "title": "Prologis, Inc."
    },
    "RTNTF": {
        "cik": 887028,
        "title": "RIO TINTO LTD"
    },
    "ELV": {
        "cik": 1156039,
        "title": "Elevance Health, Inc."
    },
    "MDT": {
        "cik": 1613103,
        "title": "Medtronic plc"
    },
    "SCHW": {
        "cik": 316709,
        "title": "SCHWAB CHARLES CORP"
    },
    "GS": {
        "cik": 886982,
        "title": "GOLDMAN SACHS GROUP INC"
    },
    "BP": {
        "cik": 313807,
        "title": "BP PLC"
    },
    "SYK": {
        "cik": 310764,
        "title": "STRYKER CORP"
    },
    "ADP": {
        "cik": 8670,
        "title": "AUTOMATIC DATA PROCESSING INC"
    },
    "PDD": {
        "cik": 1737806,
        "title": "PDD Holdings Inc."
    },
    "TJX": {
        "cik": 109198,
        "title": "TJX COMPANIES INC /DE/"
    },
    "SONY": {
        "cik": 313838,
        "title": "Sony Group Corp"
    },
    "T": {
        "cik": 732717,
        "title": "AT&T INC."
    },
    "ISRG": {
        "cik": 1035267,
        "title": "INTUITIVE SURGICAL INC"
    },
    "BLK": {
        "cik": 1364742,
        "title": "BlackRock Inc."
    },
    "RIO": {
        "cik": 863064,
        "title": "RIO TINTO PLC"
    },
    "MDLZ": {
        "cik": 1103982,
        "title": "Mondelez International, Inc."
    },
    "EQNR": {
        "cik": 1140625,
        "title": "EQUINOR ASA"
    },
    "GILD": {
        "cik": 882095,
        "title": "GILEAD SCIENCES, INC."
    },
    "DEO": {
        "cik": 835403,
        "title": "DIAGEO PLC"
    },
    "MMC": {
        "cik": 62709,
        "title": "MARSH & MCLENNAN COMPANIES, INC."
    },
    "REGN": {
        "cik": 872589,
        "title": "REGENERON PHARMACEUTICALS, INC."
    },
    "UBER": {
        "cik": 1543151,
        "title": "Uber Technologies, Inc"
    },
    "VRTX": {
        "cik": 875320,
        "title": "VERTEX PHARMACEUTICALS INC / MA"
    },
    "MUFG": {
        "cik": 67088,
        "title": "MITSUBISHI UFJ FINANCIAL GROUP INC"
    },
    "LRCX": {
        "cik": 707549,
        "title": "LAM RESEARCH CORP"
    },
    "ADI": {
        "cik": 6281,
        "title": "ANALOG DEVICES INC"
    },
    "PBR": {
        "cik": 1119639,
        "title": "PETROBRAS - PETROLEO BRASILEIRO SA"
    },
    "ETN": {
        "cik": 1551182,
        "title": "Eaton Corp plc"
    },
    "CVS": {
        "cik": 64803,
        "title": "CVS HEALTH Corp"
    },
    "ZTS": {
        "cik": 1555280,
        "title": "Zoetis Inc."
    },
    "CSLLY": {
        "cik": 1274152,
        "title": "CSL LTD"
    },
    "CI": {
        "cik": 1739940,
        "title": "Cigna Group"
    },
    "CB": {
        "cik": 896159,
        "title": "Chubb Ltd"
    },
    "SLB": {
        "cik": 87347,
        "title": "SCHLUMBERGER LIMITED/NV"
    },
    "AMT": {
        "cik": 1053507,
        "title": "AMERICAN TOWER CORP /MA/"
    },
    "IBN": {
        "cik": 1103838,
        "title": "ICICI BANK LTD"
    },
    "C": {
        "cik": 831001,
        "title": "CITIGROUP INC"
    },
    "MBGYY": {
        "cik": 1067318,
        "title": "DAIMLER AG"
    },
    "BDX": {
        "cik": 10795,
        "title": "BECTON DICKINSON & CO"
    },
    "ABNB": {
        "cik": 1559720,
        "title": "Airbnb, Inc."
    },
    "PGR": {
        "cik": 80661,
        "title": "PROGRESSIVE CORP/OH/"
    },
    "UBS": {
        "cik": 1610520,
        "title": "UBS Group AG"
    },
    "MO": {
        "cik": 764180,
        "title": "ALTRIA GROUP, INC."
    },
    "EOG": {
        "cik": 821189,
        "title": "EOG RESOURCES INC"
    },
    "HCA": {
        "cik": 860730,
        "title": "HCA Healthcare, Inc."
    },
    "PBCRY": {
        "cik": 1463157,
        "title": "PT Bank Central Asia Tbk / ADR"
    },
    "CNI": {
        "cik": 16868,
        "title": "CANADIAN NATIONAL RAILWAY CO"
    },
    "PANW": {
        "cik": 1327567,
        "title": "Palo Alto Networks Inc"
    },
    "FI": {
        "cik": 798354,
        "title": "FISERV INC"
    },
    "SO": {
        "cik": 92122,
        "title": "SOUTHERN CO"
    },
    "CME": {
        "cik": 1156375,
        "title": "CME GROUP INC."
    },
    "CP": {
        "cik": 16875,
        "title": "CANADIAN PACIFIC KANSAS CITY LTD/CN"
    },
    "BSX": {
        "cik": 885725,
        "title": "BOSTON SCIENTIFIC CORP"
    },
    "INFY": {
        "cik": 1067491,
        "title": "Infosys Ltd"
    },
    "BTI": {
        "cik": 1303523,
        "title": "British American Tobacco p.l.c."
    },
    "ATVI": {
        "cik": 718877,
        "title": "Activision Blizzard, Inc."
    },
    "ITW": {
        "cik": 49826,
        "title": "ILLINOIS TOOL WORKS INC"
    },
    "GSK": {
        "cik": 1131399,
        "title": "GSK plc"
    },
    "ENB": {
        "cik": 895728,
        "title": "ENBRIDGE INC"
    },
    "VMW": {
        "cik": 1124610,
        "title": "VMWARE, INC."
    },
    "MU": {
        "cik": 723125,
        "title": "MICRON TECHNOLOGY INC"
    },
    "EQIX": {
        "cik": 1101239,
        "title": "EQUINIX INC"
    },
    "ABBNY": {
        "cik": 1091587,
        "title": "ABB LTD"
    },
    "SHW": {
        "cik": 89800,
        "title": "SHERWIN WILLIAMS CO"
    },
    "DUK": {
        "cik": 1326160,
        "title": "Duke Energy CORP"
    },
    "SHOP": {
        "cik": 1594805,
        "title": "SHOPIFY INC."
    },
    "TOELY": {
        "cik": 1443276,
        "title": "Tokyo Electron LTD"
    },
    "KLAC": {
        "cik": 319201,
        "title": "KLA CORP"
    },
    "KKR": {
        "cik": 1404912,
        "title": "KKR & Co. Inc."
    },
    "CNQ": {
        "cik": 1017413,
        "title": "CANADIAN NATURAL RESOURCES LTD"
    },
    "SNPS": {
        "cik": 883241,
        "title": "SYNOPSYS INC"
    },
    "PYPL": {
        "cik": 1633917,
        "title": "PayPal Holdings, Inc."
    },
    "AON": {
        "cik": 315293,
        "title": "Aon plc"
    },
    "NOC": {
        "cik": 1133421,
        "title": "NORTHROP GRUMMAN CORP /DE/"
    },
    "ENLAY": {
        "cik": 1096200,
        "title": "ENEL SOCIETA PER AZIONI"
    },
    "FDX": {
        "cik": 1048911,
        "title": "FEDEX CORP"
    },
    "NTES": {
        "cik": 1110646,
        "title": "NetEase, Inc."
    },
    "AMX": {
        "cik": 1129137,
        "title": "AMERICA MOVIL SAB DE CV/"
    },
    "WM": {
        "cik": 823768,
        "title": "WASTE MANAGEMENT INC"
    },
    "ICE": {
        "cik": 1571949,
        "title": "Intercontinental Exchange, Inc."
    },
    "APD": {
        "cik": 2969,
        "title": "Air Products & Chemicals, Inc."
    },
    "SAN": {
        "cik": 891478,
        "title": "Banco Santander, S.A."
    },
    "CHTR": {
        "cik": 1091667,
        "title": "CHARTER COMMUNICATIONS, INC. /MO/"
    },
    "ATLKY": {
        "cik": 748954,
        "title": "ATLAS COPCO AB"
    },
    "SHECY": {
        "cik": 1442651,
        "title": "Shin-Etsu Chemical Co., Ltd."
    },
    "CSX": {
        "cik": 277948,
        "title": "CSX CORP"
    },
    "HUM": {
        "cik": 49071,
        "title": "HUMANA INC"
    },
    "CDNS": {
        "cik": 813672,
        "title": "CADENCE DESIGN SYSTEMS INC"
    },
    "GD": {
        "cik": 40533,
        "title": "GENERAL DYNAMICS CORP"
    },
    "MPC": {
        "cik": 1510295,
        "title": "Marathon Petroleum Corp"
    },
    "CL": {
        "cik": 21665,
        "title": "COLGATE PALMOLIVE CO"
    },
    "MELI": {
        "cik": 1099590,
        "title": "MERCADOLIBRE INC"
    },
    "MAR": {
        "cik": 1048286,
        "title": "MARRIOTT INTERNATIONAL INC /MD/"
    },
    "SCCO": {
        "cik": 1001838,
        "title": "SOUTHERN COPPER CORP/"
    },
    "MNST": {
        "cik": 865752,
        "title": "Monster Beverage Corp"
    },
    "RELX": {
        "cik": 929869,
        "title": "RELX PLC"
    },
    "MCO": {
        "cik": 1059556,
        "title": "MOODYS CORP /DE/"
    },
    "BMO": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "WDAY": {
        "cik": 1327811,
        "title": "Workday, Inc."
    },
    "TGT": {
        "cik": 27419,
        "title": "TARGET CORP"
    },
    "TRI": {
        "cik": 1075124,
        "title": "THOMSON REUTERS CORP /CAN/"
    },
    "SMFG": {
        "cik": 1022837,
        "title": "SUMITOMO MITSUI FINANCIAL GROUP, INC."
    },
    "OLCLY": {
        "cik": 1545460,
        "title": "Oriental Land Co., Ltd./ADR"
    },
    "MCK": {
        "cik": 927653,
        "title": "MCKESSON CORP"
    },
    "ORLY": {
        "cik": 898173,
        "title": "O REILLY AUTOMOTIVE INC"
    },
    "EPD": {
        "cik": 1061219,
        "title": "ENTERPRISE PRODUCTS PARTNERS L.P."
    },
    "RACE": {
        "cik": 1648416,
        "title": "Ferrari N.V."
    },
    "OXY": {
        "cik": 797468,
        "title": "OCCIDENTAL PETROLEUM CORP /DE/"
    },
    "ANET": {
        "cik": 1596532,
        "title": "Arista Networks, Inc."
    },
    "STLA": {
        "cik": 1605484,
        "title": "Stellantis N.V."
    },
    "USB": {
        "cik": 36104,
        "title": "US BANCORP \\DE\\"
    },
    "FCX": {
        "cik": 831259,
        "title": "FREEPORT-MCMORAN INC"
    },
    "PXD": {
        "cik": 1038357,
        "title": "PIONEER NATURAL RESOURCES CO"
    },
    "BNS": {
        "cik": 9631,
        "title": "BANK OF NOVA SCOTIA"
    },
    "MMM": {
        "cik": 66740,
        "title": "3M CO"
    },
    "EMR": {
        "cik": 32604,
        "title": "EMERSON ELECTRIC CO"
    },
    "EL": {
        "cik": 1001250,
        "title": "ESTEE LAUDER COMPANIES INC"
    },
    "PRNDY": {
        "cik": 899108,
        "title": "PERNOD RICARD S A /FI"
    },
    "VALE": {
        "cik": 917851,
        "title": "Vale S.A."
    },
    "ITUB": {
        "cik": 1132597,
        "title": "Itau Unibanco Holding S.A."
    },
    "JD": {
        "cik": 1549802,
        "title": "JD.com, Inc."
    },
    "NXPI": {
        "cik": 1413447,
        "title": "NXP Semiconductors N.V."
    },
    "PSX": {
        "cik": 1534701,
        "title": "Phillips 66"
    },
    "ROP": {
        "cik": 882835,
        "title": "ROPER TECHNOLOGIES INC"
    },
    "MRVL": {
        "cik": 1835632,
        "title": "Marvell Technology, Inc."
    },
    "CMG": {
        "cik": 1058090,
        "title": "CHIPOTLE MEXICAN GRILL INC"
    },
    "ECL": {
        "cik": 31462,
        "title": "ECOLAB INC."
    },
    "BN": {
        "cik": 1001085,
        "title": "BROOKFIELD Corp /ON/"
    },
    "ING": {
        "cik": 1039765,
        "title": "ING GROEP NV"
    },
    "PH": {
        "cik": 76334,
        "title": "PARKER HANNIFIN CORP"
    },
    "E": {
        "cik": 1002242,
        "title": "ENI SPA"
    },
    "APH": {
        "cik": 820313,
        "title": "AMPHENOL CORP /DE/"
    },
    "HMC": {
        "cik": 715153,
        "title": "HONDA MOTOR CO LTD"
    },
    "CTA-PA": {
        "cik": 30554,
        "title": "EIDP, Inc."
    },
    "SNOW": {
        "cik": 1640147,
        "title": "Snowflake Inc."
    },
    "CTAS": {
        "cik": 723254,
        "title": "CINTAS CORP"
    },
    "LULU": {
        "cik": 1397187,
        "title": "lululemon athletica inc."
    },
    "PNC": {
        "cik": 713676,
        "title": "PNC FINANCIAL SERVICES GROUP, INC."
    },
    "PSA": {
        "cik": 1393311,
        "title": "Public Storage"
    },
    "NSC": {
        "cik": 702165,
        "title": "NORFOLK SOUTHERN CORP"
    },
    "F": {
        "cik": 37996,
        "title": "FORD MOTOR CO"
    },
    "TEAM": {
        "cik": 1650372,
        "title": "Atlassian Corp"
    },
    "AJG": {
        "cik": 354190,
        "title": "Arthur J. Gallagher & Co."
    },
    "STZ": {
        "cik": 16918,
        "title": "CONSTELLATION BRANDS, INC."
    },
    "MET": {
        "cik": 1099219,
        "title": "METLIFE INC"
    },
    "KDP": {
        "cik": 1418135,
        "title": "Keurig Dr Pepper Inc."
    },
    "VLO": {
        "cik": 1035002,
        "title": "VALERO ENERGY CORP/TX"
    },
    "WDS": {
        "cik": 844551,
        "title": "WOODSIDE ENERGY GROUP LTD"
    },
    "HES": {
        "cik": 4447,
        "title": "HESS CORP"
    },
    "TAK": {
        "cik": 1395064,
        "title": "TAKEDA PHARMACEUTICAL CO LTD"
    },
    "TDG": {
        "cik": 1260221,
        "title": "TransDigm Group INC"
    },
    "EW": {
        "cik": 1099800,
        "title": "Edwards Lifesciences Corp"
    },
    "ANZGY": {
        "cik": 1947559,
        "title": "ANZ GROUP HOLDINGS LIMITED/ADR"
    },
    "MSI": {
        "cik": 68505,
        "title": "Motorola Solutions, Inc."
    },
    "APO": {
        "cik": 1858681,
        "title": "Apollo Global Management, Inc."
    },
    "BBVA": {
        "cik": 842180,
        "title": "BANCO BILBAO VIZCAYA ARGENTARIA, S.A."
    },
    "RSG": {
        "cik": 1060391,
        "title": "REPUBLIC SERVICES, INC."
    },
    "GM": {
        "cik": 1467858,
        "title": "General Motors Co"
    },
    "FTNT": {
        "cik": 1262039,
        "title": "Fortinet, Inc."
    },
    "GLD": {
        "cik": 1222333,
        "title": "SPDR GOLD TRUST"
    },
    "ABEV": {
        "cik": 1565025,
        "title": "AMBEV S.A."
    },
    "TT": {
        "cik": 1466258,
        "title": "Trane Technologies plc"
    },
    "AFL": {
        "cik": 4977,
        "title": "AFLAC INC"
    },
    "NGG": {
        "cik": 1004315,
        "title": "NATIONAL GRID PLC"
    },
    "ADM": {
        "cik": 7084,
        "title": "Archer-Daniels-Midland Co"
    },
    "CARR": {
        "cik": 1783180,
        "title": "CARRIER GLOBAL Corp"
    },
    "SRE": {
        "cik": 1032208,
        "title": "SEMPRA"
    },
    "AZO": {
        "cik": 866787,
        "title": "AUTOZONE INC"
    },
    "HSY": {
        "cik": 47111,
        "title": "HERSHEY CO"
    },
    "ODFL": {
        "cik": 878927,
        "title": "OLD DOMINION FREIGHT LINE, INC."
    },
    "KVUE": {
        "cik": 1944048,
        "title": "Kenvue Inc."
    },
    "PCAR": {
        "cik": 75362,
        "title": "PACCAR INC"
    },
    "STM": {
        "cik": 932787,
        "title": "STMicroelectronics N.V."
    },
    "BIDU": {
        "cik": 1329099,
        "title": "Baidu, Inc."
    },
    "MCHP": {
        "cik": 827054,
        "title": "MICROCHIP TECHNOLOGY INC"
    },
    "PAYX": {
        "cik": 723531,
        "title": "PAYCHEX INC"
    },
    "ADSK": {
        "cik": 769397,
        "title": "Autodesk, Inc."
    },
    "CCI": {
        "cik": 1051470,
        "title": "CROWN CASTLE INC."
    },
    "KMB": {
        "cik": 55785,
        "title": "KIMBERLY CLARK CORP"
    },
    "SU": {
        "cik": 311337,
        "title": "SUNCOR ENERGY INC"
    },
    "MRNA": {
        "cik": 1682852,
        "title": "Moderna, Inc."
    },
    "SPG": {
        "cik": 1063761,
        "title": "SIMON PROPERTY GROUP INC /DE/"
    },
    "WMB": {
        "cik": 107263,
        "title": "WILLIAMS COMPANIES, INC."
    },
    "NUE": {
        "cik": 73309,
        "title": "NUCOR CORP"
    },
    "MSCI": {
        "cik": 1408198,
        "title": "MSCI Inc."
    },
    "AIG": {
        "cik": 5272,
        "title": "AMERICAN INTERNATIONAL GROUP, INC."
    },
    "ALC": {
        "cik": 1167379,
        "title": "ALCON INC"
    },
    "CPRT": {
        "cik": 900075,
        "title": "COPART INC"
    },
    "KHC": {
        "cik": 1637459,
        "title": "Kraft Heinz Co"
    },
    "CRH": {
        "cik": 849395,
        "title": "CRH PUBLIC LTD CO"
    },
    "ET": {
        "cik": 1276187,
        "title": "Energy Transfer LP"
    },
    "DXCM": {
        "cik": 1093557,
        "title": "DEXCOM INC"
    },
    "DELL": {
        "cik": 1571996,
        "title": "Dell Technologies Inc."
    },
    "ROST": {
        "cik": 745732,
        "title": "ROSS STORES, INC."
    },
    "LVS": {
        "cik": 1300514,
        "title": "LAS VEGAS SANDS CORP"
    },
    "TEL": {
        "cik": 1385157,
        "title": "TE Connectivity Ltd."
    },
    "JCI": {
        "cik": 833444,
        "title": "Johnson Controls International plc"
    },
    "AEP": {
        "cik": 4904,
        "title": "AMERICAN ELECTRIC POWER CO INC"
    },
    "ON": {
        "cik": 1097864,
        "title": "ON SEMICONDUCTOR CORP"
    },
    "GIS": {
        "cik": 40704,
        "title": "GENERAL MILLS INC"
    },
    "IDXX": {
        "cik": 874716,
        "title": "IDEXX LABORATORIES INC /DE"
    },
    "D": {
        "cik": 715957,
        "title": "DOMINION ENERGY, INC"
    },
    "WELL": {
        "cik": 766704,
        "title": "WELLTOWER INC."
    },
    "LNG": {
        "cik": 3570,
        "title": "Cheniere Energy, Inc."
    },
    "IQV": {
        "cik": 1478242,
        "title": "IQVIA HOLDINGS INC."
    },
    "COF": {
        "cik": 927628,
        "title": "CAPITAL ONE FINANCIAL CORP"
    },
    "EXC": {
        "cik": 1109357,
        "title": "EXELON CORP"
    },
    "MFG": {
        "cik": 1335730,
        "title": "MIZUHO FINANCIAL GROUP INC"
    },
    "HLT": {
        "cik": 1585689,
        "title": "Hilton Worldwide Holdings Inc."
    },
    "LI": {
        "cik": 1791706,
        "title": "Li Auto Inc."
    },
    "BSBR": {
        "cik": 1471055,
        "title": "Banco Santander (Brasil) S.A."
    },
    "DHI": {
        "cik": 882184,
        "title": "HORTON D R INC /DE/"
    },
    "PCG": {
        "cik": 1004980,
        "title": "PG&E Corp"
    },
    "KMI": {
        "cik": 1506307,
        "title": "KINDER MORGAN, INC."
    },
    "IBKR": {
        "cik": 1381197,
        "title": "Interactive Brokers Group, Inc."
    },
    "BIIB": {
        "cik": 875045,
        "title": "BIOGEN INC."
    },
    "DOW": {
        "cik": 1751788,
        "title": "DOW INC."
    },
    "BAESY": {
        "cik": 895564,
        "title": "BAE SYSTEMS PLC /FI/"
    },
    "HLN": {
        "cik": 1900304,
        "title": "Haleon plc"
    },
    "CRARY": {
        "cik": 1279967,
        "title": "CREDIT AGRICOLE S A"
    },
    "TFC": {
        "cik": 92230,
        "title": "TRUIST FINANCIAL CORP"
    },
    "O": {
        "cik": 726728,
        "title": "REALTY INCOME CORP"
    },
    "HCMLY": {
        "cik": 948696,
        "title": "LafargeHolcim Ltd/ADR"
    },
    "TRV": {
        "cik": 86312,
        "title": "TRAVELERS COMPANIES, INC."
    },
    "BCE": {
        "cik": 718940,
        "title": "BCE INC"
    },
    "CRWD": {
        "cik": 1535527,
        "title": "CrowdStrike Holdings, Inc."
    },
    "ABC": {
        "cik": 1140859,
        "title": "AMERISOURCEBERGEN CORP"
    },
    "CVE": {
        "cik": 1475260,
        "title": "CENOVUS ENERGY INC."
    },
    "SGEN": {
        "cik": 1060736,
        "title": "Seagen Inc."
    },
    "CM": {
        "cik": 1045520,
        "title": "CANADIAN IMPERIAL BANK OF COMMERCE /CAN/"
    },
    "YUM": {
        "cik": 1041061,
        "title": "YUM BRANDS INC"
    },
    "SYY": {
        "cik": 96021,
        "title": "SYSCO CORP"
    },
    "TTD": {
        "cik": 1671933,
        "title": "Trade Desk, Inc."
    },
    "TRP": {
        "cik": 1232384,
        "title": "TC ENERGY CORP"
    },
    "CTVA": {
        "cik": 1755672,
        "title": "Corteva, Inc."
    },
    "AME": {
        "cik": 1037868,
        "title": "AMETEK INC/"
    },
    "WCN": {
        "cik": 1318220,
        "title": "Waste Connections, Inc."
    },
    "BKR": {
        "cik": 1701605,
        "title": "Baker Hughes Co"
    },
    "DG": {
        "cik": 29534,
        "title": "DOLLAR GENERAL CORP"
    },
    "PPERY": {
        "cik": 1461748,
        "title": "PT Bank Mandiri (Persero) Tbk / ADR"
    },
    "DLR": {
        "cik": 1297996,
        "title": "DIGITAL REALTY TRUST, INC."
    },
    "GWW": {
        "cik": 277135,
        "title": "W.W. GRAINGER, INC."
    },
    "HAL": {
        "cik": 45012,
        "title": "HALLIBURTON CO"
    },
    "CNC": {
        "cik": 1071739,
        "title": "CENTENE CORP"
    },
    "AMP": {
        "cik": 820027,
        "title": "AMERIPRISE FINANCIAL INC"
    },
    "A": {
        "cik": 1090872,
        "title": "AGILENT TECHNOLOGIES, INC."
    },
    "MPLX": {
        "cik": 1552000,
        "title": "MPLX LP"
    },
    "IAU": {
        "cik": 1278680,
        "title": "ISHARES GOLD TRUST"
    },
    "CTSH": {
        "cik": 1058290,
        "title": "COGNIZANT TECHNOLOGY SOLUTIONS CORP"
    },
    "OTIS": {
        "cik": 1781335,
        "title": "Otis Worldwide Corp"
    },
    "NU": {
        "cik": 1691493,
        "title": "Nu Holdings Ltd."
    },
    "LYG": {
        "cik": 1160106,
        "title": "Lloyds Banking Group plc"
    },
    "DD": {
        "cik": 1666700,
        "title": "DuPont de Nemours, Inc."
    },
    "CEG": {
        "cik": 1868275,
        "title": "Constellation Energy Corp"
    },
    "LHX": {
        "cik": 202058,
        "title": "L3HARRIS TECHNOLOGIES, INC. /DE/"
    },
    "SQ": {
        "cik": 1512673,
        "title": "Block, Inc."
    },
    "BK": {
        "cik": 1390777,
        "title": "Bank of New York Mellon Corp"
    },
    "KR": {
        "cik": 56873,
        "title": "KROGER CO"
    },
    "ROK": {
        "cik": 1024478,
        "title": "ROCKWELL AUTOMATION, INC"
    },
    "VRSK": {
        "cik": 1442145,
        "title": "Verisk Analytics, Inc."
    },
    "CPNG": {
        "cik": 1834584,
        "title": "Coupang, Inc."
    },
    "PUK": {
        "cik": 1116578,
        "title": "PRUDENTIAL PLC"
    },
    "PRU": {
        "cik": 1137774,
        "title": "PRUDENTIAL FINANCIAL INC"
    },
    "CMI": {
        "cik": 26172,
        "title": "CUMMINS INC"
    },
    "CODYY": {
        "cik": 1012037,
        "title": "COMPAGNIE DE SAINT GOBAIN"
    },
    "MFC": {
        "cik": 1086888,
        "title": "MANULIFE FINANCIAL CORP"
    },
    "FIS": {
        "cik": 1136893,
        "title": "Fidelity National Information Services, Inc."
    },
    "LEN": {
        "cik": 920760,
        "title": "LENNAR CORP /NEW/"
    },
    "FAST": {
        "cik": 815556,
        "title": "FASTENAL CO"
    },
    "BF-B": {
        "cik": 14693,
        "title": "BROWN FORMAN CORP"
    },
    "PPG": {
        "cik": 79879,
        "title": "PPG INDUSTRIES INC"
    },
    "IMO": {
        "cik": 49938,
        "title": "IMPERIAL OIL LTD"
    },
    "GPN": {
        "cik": 1123360,
        "title": "GLOBAL PAYMENTS INC"
    },
    "EA": {
        "cik": 712515,
        "title": "ELECTRONIC ARTS INC."
    },
    "LYB": {
        "cik": 1489393,
        "title": "LyondellBasell Industries N.V."
    },
    "CSGP": {
        "cik": 1057352,
        "title": "COSTAR GROUP, INC."
    },
    "DVN": {
        "cik": 1090012,
        "title": "DEVON ENERGY CORP/DE"
    },
    "BBD": {
        "cik": 1160330,
        "title": "BANK BRADESCO"
    },
    "XEL": {
        "cik": 72903,
        "title": "XCEL ENERGY INC"
    },
    "FERG": {
        "cik": 1832433,
        "title": "Ferguson plc"
    },
    "PKX": {
        "cik": 889132,
        "title": "POSCO HOLDINGS INC."
    },
    "EXPGY": {
        "cik": 1376891,
        "title": "Experian Group LTD"
    },
    "QSR": {
        "cik": 1618756,
        "title": "Restaurant Brands International Inc."
    },
    "GEHC": {
        "cik": 1932393,
        "title": "GE HealthCare Technologies Inc."
    },
    "DLTR": {
        "cik": 935703,
        "title": "DOLLAR TREE, INC."
    },
    "URI": {
        "cik": 1067701,
        "title": "UNITED RENTALS, INC."
    },
    "PLTR": {
        "cik": 1321655,
        "title": "Palantir Technologies Inc."
    },
    "HPQ": {
        "cik": 47217,
        "title": "HP INC"
    },
    "WBD": {
        "cik": 1437107,
        "title": "Warner Bros. Discovery, Inc."
    },
    "NTR": {
        "cik": 1725964,
        "title": "Nutrien Ltd."
    },
    "ED": {
        "cik": 1047862,
        "title": "CONSOLIDATED EDISON INC"
    },
    "DDOG": {
        "cik": 1561550,
        "title": "Datadog, Inc."
    },
    "NEM": {
        "cik": 1164727,
        "title": "NEWMONT Corp /DE/"
    },
    "GFS": {
        "cik": 1709048,
        "title": "GLOBALFOUNDRIES Inc."
    },
    "VEEV": {
        "cik": 1393052,
        "title": "VEEVA SYSTEMS INC"
    },
    "PEG": {
        "cik": 788784,
        "title": "PUBLIC SERVICE ENTERPRISE GROUP INC"
    },
    "VTMX": {
        "cik": 1969373,
        "title": "Vesta Real Estate Corporation, S.A.B. de C.V."
    },
    "VICI": {
        "cik": 1705696,
        "title": "VICI PROPERTIES INC."
    },
    "ARGX": {
        "cik": 1697862,
        "title": "ARGENX SE"
    },
    "TLGPY": {
        "cik": 1947542,
        "title": "Telstra Group Ltd"
    },
    "ARES": {
        "cik": 1176948,
        "title": "Ares Management Corp"
    },
    "DASH": {
        "cik": 1792789,
        "title": "DoorDash, Inc."
    },
    "ORAN": {
        "cik": 1038143,
        "title": "ORANGE"
    },
    "OEZVY": {
        "cik": 1021020,
        "title": "OSTERREICHISCHE ELEKTRIZITATSWIRTSCHAFTS /FI"
    },
    "PWR": {
        "cik": 1050915,
        "title": "QUANTA SERVICES, INC."
    },
    "OKE": {
        "cik": 1039684,
        "title": "ONEOK INC /NEW/"
    },
    "WTKWY": {
        "cik": 861967,
        "title": "WOLTERS KLUWER N V /FI"
    },
    "WST": {
        "cik": 105770,
        "title": "WEST PHARMACEUTICAL SERVICES INC"
    },
    "BCS": {
        "cik": 312069,
        "title": "BARCLAYS PLC"
    },
    "CHT": {
        "cik": 1132924,
        "title": "CHUNGHWA TELECOM CO LTD"
    },
    "CCEP": {
        "cik": 1650107,
        "title": "COCA-COLA EUROPACIFIC PARTNERS plc"
    },
    "BNTX": {
        "cik": 1776985,
        "title": "BioNTech SE"
    },
    "VMC": {
        "cik": 1396009,
        "title": "Vulcan Materials CO"
    },
    "DIA": {
        "cik": 1041130,
        "title": "SPDR DOW JONES INDUSTRIAL AVERAGE ETF TRUST"
    },
    "ACGL": {
        "cik": 947484,
        "title": "ARCH CAPITAL GROUP LTD."
    },
    "SLF": {
        "cik": 1097362,
        "title": "SUN LIFE FINANCIAL INC"
    },
    "EXR": {
        "cik": 1289490,
        "title": "Extra Space Storage Inc."
    },
    "BDORY": {
        "cik": 1433913,
        "title": "BANCO DO BRASIL S.A."
    },
    "ALL": {
        "cik": 899051,
        "title": "ALLSTATE CORP"
    },
    "MBLY": {
        "cik": 1910139,
        "title": "Mobileye Global Inc."
    },
    "GOLD": {
        "cik": 756894,
        "title": "BARRICK GOLD CORP"
    },
    "CDW": {
        "cik": 1402057,
        "title": "CDW Corp"
    },
    "IR": {
        "cik": 1699150,
        "title": "Ingersoll Rand Inc."
    },
    "FTV": {
        "cik": 1659166,
        "title": "Fortive Corp"
    },
    "WEC": {
        "cik": 783325,
        "title": "WEC ENERGY GROUP, INC."
    },
    "FANG": {
        "cik": 1539838,
        "title": "Diamondback Energy, Inc."
    },
    "AWK": {
        "cik": 1410636,
        "title": "American Water Works Company, Inc."
    },
    "MLM": {
        "cik": 916076,
        "title": "MARTIN MARIETTA MATERIALS INC"
    },
    "DAL": {
        "cik": 27904,
        "title": "DELTA AIR LINES, INC."
    },
    "ILMN": {
        "cik": 1110803,
        "title": "ILLUMINA, INC."
    },
    "ALGN": {
        "cik": 1097149,
        "title": "ALIGN TECHNOLOGY INC"
    },
    "GWLIF": {
        "cik": 850918,
        "title": "GREAT-WEST LIFECO INC."
    },
    "FANUY": {
        "cik": 1446596,
        "title": "Fanuc Ltd"
    },
    "EIX": {
        "cik": 827052,
        "title": "EDISON INTERNATIONAL"
    },
    "IT": {
        "cik": 749251,
        "title": "GARTNER INC"
    },
    "GLW": {
        "cik": 24741,
        "title": "CORNING INC /NY"
    },
    "FNV": {
        "cik": 1456346,
        "title": "FRANCO NEVADA Corp"
    },
    "NWG": {
        "cik": 844150,
        "title": "NatWest Group plc"
    },
    "MDY": {
        "cik": 936958,
        "title": "SPDR S&P MIDCAP 400 ETF TRUST"
    },
    "APTV": {
        "cik": 1521332,
        "title": "Aptiv PLC"
    },
    "WIT": {
        "cik": 1123799,
        "title": "WIPRO LTD"
    },
    "MTD": {
        "cik": 1037646,
        "title": "METTLER TOLEDO INTERNATIONAL INC/"
    },
    "ANSS": {
        "cik": 1013462,
        "title": "ANSYS INC"
    },
    "SPOT": {
        "cik": 1639920,
        "title": "Spotify Technology S.A."
    },
    "MDB": {
        "cik": 1441816,
        "title": "MongoDB, Inc."
    },
    "PCRFY": {
        "cik": 63271,
        "title": "PANASONIC Corp"
    },
    "CBRE": {
        "cik": 1138118,
        "title": "CBRE GROUP, INC."
    },
    "NDAQ": {
        "cik": 1120193,
        "title": "NASDAQ, INC."
    },
    "RCL": {
        "cik": 884887,
        "title": "ROYAL CARIBBEAN CRUISES LTD"
    },
    "AVB": {
        "cik": 915912,
        "title": "AVALONBAY COMMUNITIES INC"
    },
    "ZBH": {
        "cik": 1136869,
        "title": "ZIMMER BIOMET HOLDINGS, INC."
    },
    "HUBS": {
        "cik": 1404655,
        "title": "HUBSPOT INC"
    },
    "CQP": {
        "cik": 1383650,
        "title": "Cheniere Energy Partners, L.P."
    },
    "TCOM": {
        "cik": 1269238,
        "title": "Trip.com Group Ltd"
    },
    "VOD": {
        "cik": 839923,
        "title": "VODAFONE GROUP PUBLIC LTD CO"
    },
    "TU": {
        "cik": 868675,
        "title": "TELUS CORP"
    },
    "SAUHY": {
        "cik": 1451279,
        "title": "Straumann Holding AG / ADR"
    },
    "TROW": {
        "cik": 1113169,
        "title": "PRICE T ROWE GROUP INC"
    },
    "RMD": {
        "cik": 943819,
        "title": "RESMED INC"
    },
    "EFX": {
        "cik": 33185,
        "title": "EQUIFAX INC"
    },
    "TLK": {
        "cik": 1001807,
        "title": "PERUSAHAAN PERSEROAN PERSERO PT TELEKOMUNIKASI INDONESIA TBK"
    },
    "CAJPY": {
        "cik": 16988,
        "title": "CANON INC"
    },
    "HZNP": {
        "cik": 1492426,
        "title": "Horizon Therapeutics Public Ltd Co"
    },
    "GMAB": {
        "cik": 1434265,
        "title": "GENMAB A/S"
    },
    "EQR": {
        "cik": 906107,
        "title": "EQUITY RESIDENTIAL"
    },
    "XYL": {
        "cik": 1524472,
        "title": "Xylem Inc."
    },
    "ATEYY": {
        "cik": 1158838,
        "title": "ADVANTEST CORP"
    },
    "SBAC": {
        "cik": 1034054,
        "title": "SBA COMMUNICATIONS CORP"
    },
    "TSCO": {
        "cik": 916365,
        "title": "TRACTOR SUPPLY CO /DE/"
    },
    "GIB": {
        "cik": 1061574,
        "title": "CGI INC"
    },
    "WY": {
        "cik": 106535,
        "title": "WEYERHAEUSER CO"
    },
    "MPWR": {
        "cik": 1280452,
        "title": "MONOLITHIC POWER SYSTEMS INC"
    },
    "TTWO": {
        "cik": 946581,
        "title": "TAKE TWO INTERACTIVE SOFTWARE INC"
    },
    "ALNY": {
        "cik": 1178670,
        "title": "ALNYLAM PHARMACEUTICALS, INC."
    },
    "ELP": {
        "cik": 1041792,
        "title": "ENERGY CO OF PARANA"
    },
    "EC": {
        "cik": 1444406,
        "title": "ECOPETROL S.A."
    },
    "AEM": {
        "cik": 2809,
        "title": "AGNICO EAGLE MINES LTD"
    },
    "EBAY": {
        "cik": 1065088,
        "title": "EBAY INC"
    },
    "DFS": {
        "cik": 1393612,
        "title": "Discover Financial Services"
    },
    "WBA": {
        "cik": 1618921,
        "title": "Walgreens Boots Alliance, Inc."
    },
    "TEF": {
        "cik": 814052,
        "title": "TELEFONICA S A"
    },
    "KEYS": {
        "cik": 1601046,
        "title": "Keysight Technologies, Inc."
    },
    "CHD": {
        "cik": 313927,
        "title": "CHURCH & DWIGHT CO INC /DE/"
    },
    "RYAAY": {
        "cik": 1038683,
        "title": "RYANAIR HOLDINGS PLC"
    },
    "MKC": {
        "cik": 63754,
        "title": "MCCORMICK & CO INC"
    },
    "CABHF": {
        "cik": 1436647,
        "title": "Carlsberg AS"
    },
    "ES": {
        "cik": 72741,
        "title": "EVERSOURCE ENERGY"
    },
    "ULTA": {
        "cik": 1403568,
        "title": "Ulta Beauty, Inc."
    },
    "CAH": {
        "cik": 721371,
        "title": "CARDINAL HEALTH INC"
    },
    "RJF": {
        "cik": 720005,
        "title": "RAYMOND JAMES FINANCIAL INC"
    },
    "HIG": {
        "cik": 874766,
        "title": "HARTFORD FINANCIAL SERVICES GROUP, INC."
    },
    "SE": {
        "cik": 1703399,
        "title": "Sea Ltd"
    },
    "YUMC": {
        "cik": 1673358,
        "title": "Yum China Holdings, Inc."
    },
    "ALB": {
        "cik": 915913,
        "title": "ALBEMARLE CORP"
    },
    "HPE": {
        "cik": 1645590,
        "title": "Hewlett Packard Enterprise Co"
    },
    "STE": {
        "cik": 1757898,
        "title": "STERIS plc"
    },
    "DB": {
        "cik": 1159508,
        "title": "DEUTSCHE BANK AKTIENGESELLSCHAFT"
    },
    "DTE": {
        "cik": 936340,
        "title": "DTE ENERGY CO"
    },
    "GPC": {
        "cik": 40987,
        "title": "GENUINE PARTS CO"
    },
    "STT": {
        "cik": 93751,
        "title": "STATE STREET CORP"
    },
    "MT": {
        "cik": 1243429,
        "title": "ArcelorMittal"
    },
    "WTW": {
        "cik": 1140536,
        "title": "WILLIS TOWERS WATSON PLC"
    },
    "BAX": {
        "cik": 10456,
        "title": "BAXTER INTERNATIONAL INC"
    },
    "FICO": {
        "cik": 814547,
        "title": "FAIR ISAAC CORP"
    },
    "HRL": {
        "cik": 48465,
        "title": "HORMEL FOODS CORP /DE/"
    },
    "MTB": {
        "cik": 36270,
        "title": "M&T BANK CORP"
    },
    "CTRA": {
        "cik": 858470,
        "title": "Coterra Energy Inc."
    },
    "NOK": {
        "cik": 924613,
        "title": "NOKIA CORP"
    },
    "VRSN": {
        "cik": 1014473,
        "title": "VERISIGN INC/CA"
    },
    "AEE": {
        "cik": 1002910,
        "title": "AMEREN CORP"
    },
    "BR": {
        "cik": 1383312,
        "title": "BROADRIDGE FINANCIAL SOLUTIONS, INC."
    },
    "K": {
        "cik": 55067,
        "title": "KELLOGG CO"
    },
    "RCI": {
        "cik": 733099,
        "title": "ROGERS COMMUNICATIONS INC"
    },
    "UDR": {
        "cik": 74208,
        "title": "UDR, Inc."
    },
    "ZS": {
        "cik": 1713683,
        "title": "Zscaler, Inc."
    },
    "IX": {
        "cik": 1070304,
        "title": "ORIX CORP"
    },
    "BGNE": {
        "cik": 1651308,
        "title": "BeiGene, Ltd."
    },
    "PHG": {
        "cik": 313216,
        "title": "KONINKLIJKE PHILIPS NV"
    },
    "SYM": {
        "cik": 1837240,
        "title": "Symbotic Inc."
    },
    "FE": {
        "cik": 1031296,
        "title": "FIRSTENERGY CORP"
    },
    "FRFHF": {
        "cik": 915191,
        "title": "FAIRFAX FINANCIAL HOLDINGS LTD/ CAN"
    },
    "RKT": {
        "cik": 1805284,
        "title": "Rocket Companies, Inc."
    },
    "ICLR": {
        "cik": 1060955,
        "title": "ICON PLC"
    },
    "BRO": {
        "cik": 79282,
        "title": "BROWN & BROWN, INC."
    },
    "CCL": {
        "cik": 815097,
        "title": "CARNIVAL CORP"
    },
    "TECK": {
        "cik": 886986,
        "title": "TECK RESOURCES LTD"
    },
    "INVH": {
        "cik": 1687229,
        "title": "Invitation Homes Inc."
    },
    "HWM": {
        "cik": 4281,
        "title": "Howmet Aerospace Inc."
    },
    "ZM": {
        "cik": 1585521,
        "title": "Zoom Video Communications, Inc."
    },
    "ETR": {
        "cik": 65984,
        "title": "ENTERGY CORP /DE/"
    },
    "WAB": {
        "cik": 943452,
        "title": "WESTINGHOUSE AIR BRAKE TECHNOLOGIES CORP"
    },
    "LYV": {
        "cik": 1335258,
        "title": "Live Nation Entertainment, Inc."
    },
    "FCNCA": {
        "cik": 798941,
        "title": "FIRST CITIZENS BANCSHARES INC /DE/"
    },
    "AIU": {
        "cik": 1722380,
        "title": "Meta Data Ltd"
    },
    "TW": {
        "cik": 1758730,
        "title": "Tradeweb Markets Inc."
    },
    "RIVN": {
        "cik": 1874178,
        "title": "Rivian Automotive, Inc. / DE"
    },
    "HEI": {
        "cik": 46619,
        "title": "HEICO CORP"
    },
    "JBHT": {
        "cik": 728535,
        "title": "HUNT J B TRANSPORT SERVICES INC"
    },
    "ARE": {
        "cik": 1035443,
        "title": "ALEXANDRIA REAL ESTATE EQUITIES, INC."
    },
    "MKL": {
        "cik": 1096343,
        "title": "MARKEL GROUP INC."
    },
    "TS": {
        "cik": 1190723,
        "title": "TENARIS SA"
    },
    "NIO": {
        "cik": 1736541,
        "title": "NIO Inc."
    },
    "NET": {
        "cik": 1477333,
        "title": "Cloudflare, Inc."
    },
    "ROL": {
        "cik": 84839,
        "title": "ROLLINS INC"
    },
    "DSCSY": {
        "cik": 1671750,
        "title": "Disco Corporation/ADR"
    },
    "DOV": {
        "cik": 29905,
        "title": "DOVER Corp"
    },
    "NVR": {
        "cik": 906163,
        "title": "NVR INC"
    },
    "GRMN": {
        "cik": 1121788,
        "title": "GARMIN LTD"
    },
    "TSN": {
        "cik": 100493,
        "title": "TYSON FOODS, INC."
    },
    "ZTO": {
        "cik": 1677250,
        "title": "ZTO Express (Cayman) Inc."
    },
    "FSLR": {
        "cik": 1274494,
        "title": "FIRST SOLAR, INC."
    },
    "LH": {
        "cik": 920148,
        "title": "LABORATORY CORP OF AMERICA HOLDINGS"
    },
    "FLT": {
        "cik": 1175454,
        "title": "FLEETCOR TECHNOLOGIES INC"
    },
    "TRGP": {
        "cik": 1389170,
        "title": "Targa Resources Corp."
    },
    "TDY": {
        "cik": 1094285,
        "title": "TELEDYNE TECHNOLOGIES INC"
    },
    "FTS": {
        "cik": 1666175,
        "title": "Fortis Inc."
    },
    "LUV": {
        "cik": 92380,
        "title": "SOUTHWEST AIRLINES CO"
    },
    "RTO": {
        "cik": 930157,
        "title": "RENTOKIL INITIAL PLC /FI"
    },
    "DRI": {
        "cik": 940944,
        "title": "DARDEN RESTAURANTS INC"
    },
    "PINS": {
        "cik": 1506293,
        "title": "PINTEREST, INC."
    },
    "WPM": {
        "cik": 1323404,
        "title": "Wheaton Precious Metals Corp."
    },
    "MOH": {
        "cik": 1179929,
        "title": "MOLINA HEALTHCARE, INC."
    },
    "SQM": {
        "cik": 909037,
        "title": "CHEMICAL & MINING CO OF CHILE INC"
    },
    "PPL": {
        "cik": 922224,
        "title": "PPL Corp"
    },
    "HOLX": {
        "cik": 859737,
        "title": "HOLOGIC INC"
    },
    "CLX": {
        "cik": 21076,
        "title": "CLOROX CO /DE/"
    },
    "PFG": {
        "cik": 1126328,
        "title": "PRINCIPAL FINANCIAL GROUP INC"
    },
    "COO": {
        "cik": 711404,
        "title": "COOPER COMPANIES, INC."
    },
    "KOF": {
        "cik": 910631,
        "title": "COCA COLA FEMSA SAB DE CV"
    },
    "RF": {
        "cik": 1281761,
        "title": "REGIONS FINANCIAL CORP"
    },
    "BEKE": {
        "cik": 1809587,
        "title": "KE Holdings Inc."
    },
    "LPLA": {
        "cik": 1397911,
        "title": "LPL Financial Holdings Inc."
    },
    "CUK": {
        "cik": 1125259,
        "title": "CARNIVAL PLC"
    },
    "CNP": {
        "cik": 1130310,
        "title": "CENTERPOINT ENERGY INC"
    },
    "ENPH": {
        "cik": 1463101,
        "title": "Enphase Energy, Inc."
    },
    "NTDTY": {
        "cik": 1446705,
        "title": "NTT Data Corp"
    },
    "COIN": {
        "cik": 1679788,
        "title": "Coinbase Global, Inc."
    },
    "STLD": {
        "cik": 1022671,
        "title": "STEEL DYNAMICS INC"
    },
    "EXPD": {
        "cik": 746515,
        "title": "EXPEDITORS INTERNATIONAL OF WASHINGTON INC"
    },
    "FITB": {
        "cik": 35527,
        "title": "FIFTH THIRD BANCORP"
    },
    "CNHI": {
        "cik": 1567094,
        "title": "CNH Industrial N.V."
    },
    "UWMC": {
        "cik": 1783398,
        "title": "UWM Holdings Corp"
    },
    "BEP": {
        "cik": 1533232,
        "title": "Brookfield Renewable Partners L.P."
    },
    "BBY": {
        "cik": 764478,
        "title": "BEST BUY CO INC"
    },
    "SIRI": {
        "cik": 908937,
        "title": "SIRIUS XM HOLDINGS INC."
    },
    "J": {
        "cik": 52988,
        "title": "JACOBS SOLUTIONS INC."
    },
    "UMC": {
        "cik": 1033767,
        "title": "UNITED MICROELECTRONICS CORP"
    },
    "MAA": {
        "cik": 912595,
        "title": "MID AMERICA APARTMENT COMMUNITIES INC."
    },
    "SGSOY": {
        "cik": 1069347,
        "title": "SGS SOCIETE GENERALE DE SURVEILLANCE HOLDING SA /FI"
    },
    "IRM": {
        "cik": 1020569,
        "title": "IRON MOUNTAIN INC"
    },
    "SWKS": {
        "cik": 4127,
        "title": "SKYWORKS SOLUTIONS, INC."
    },
    "BG": {
        "cik": 1144519,
        "title": "BUNGELTD"
    },
    "PHM": {
        "cik": 822416,
        "title": "PULTEGROUP INC/MI/"
    },
    "BMRN": {
        "cik": 1048477,
        "title": "BIOMARIN PHARMACEUTICAL INC"
    },
    "WMG": {
        "cik": 1319161,
        "title": "Warner Music Group Corp."
    },
    "BLDR": {
        "cik": 1316835,
        "title": "Builders FirstSource, Inc."
    },
    "ATO": {
        "cik": 731802,
        "title": "ATMOS ENERGY CORP"
    },
    "PBA": {
        "cik": 1546066,
        "title": "PEMBINA PIPELINE CORP"
    },
    "WLK": {
        "cik": 1262823,
        "title": "WESTLAKE CORP"
    },
    "PTC": {
        "cik": 857005,
        "title": "PTC INC."
    },
    "IEX": {
        "cik": 832101,
        "title": "IDEX CORP /DE/"
    },
    "BALL": {
        "cik": 9389,
        "title": "BALL Corp"
    },
    "ERIC": {
        "cik": 717826,
        "title": "ERICSSON LM TELEPHONE CO"
    },
    "RBLX": {
        "cik": 1315098,
        "title": "Roblox Corp"
    },
    "VTR": {
        "cik": 740260,
        "title": "Ventas, Inc."
    },
    "PAYC": {
        "cik": 1590955,
        "title": "Paycom Software, Inc."
    },
    "HUBB": {
        "cik": 48898,
        "title": "HUBBELL INC"
    },
    "CMS": {
        "cik": 811156,
        "title": "CMS ENERGY CORP"
    },
    "FDS": {
        "cik": 1013237,
        "title": "FACTSET RESEARCH SYSTEMS INC"
    },
    "IFF": {
        "cik": 51253,
        "title": "INTERNATIONAL FLAVORS & FRAGRANCES INC"
    },
    "CINF": {
        "cik": 20286,
        "title": "CINCINNATI FINANCIAL CORP"
    },
    "MRO": {
        "cik": 101778,
        "title": "MARATHON OIL CORP"
    },
    "SPLK": {
        "cik": 1353283,
        "title": "SPLUNK INC"
    },
    "FOXA": {
        "cik": 1754301,
        "title": "Fox Corp"
    },
    "JRONY": {
        "cik": 1438077,
        "title": "Jeronimo Martins SGPS SA"
    },
    "RS": {
        "cik": 861884,
        "title": "RELIANCE STEEL & ALUMINUM CO"
    },
    "NTAP": {
        "cik": 1002047,
        "title": "NetApp, Inc."
    },
    "UAL": {
        "cik": 100517,
        "title": "United Airlines Holdings, Inc."
    },
    "EXPE": {
        "cik": 1324424,
        "title": "Expedia Group, Inc."
    },
    "EQT": {
        "cik": 33213,
        "title": "EQT Corp"
    },
    "HBAN": {
        "cik": 49196,
        "title": "HUNTINGTON BANCSHARES INC /MD/"
    },
    "CHKP": {
        "cik": 1015922,
        "title": "CHECK POINT SOFTWARE TECHNOLOGIES LTD"
    },
    "ASX": {
        "cik": 1122411,
        "title": "ASE Technology Holding Co., Ltd."
    },
    "TER": {
        "cik": 97210,
        "title": "TERADYNE, INC"
    },
    "MGA": {
        "cik": 749098,
        "title": "MAGNA INTERNATIONAL INC"
    },
    "CBOE": {
        "cik": 1374310,
        "title": "Cboe Global Markets, Inc."
    },
    "WAT": {
        "cik": 1000697,
        "title": "WATERS CORP /DE/"
    },
    "WRB": {
        "cik": 11544,
        "title": "BERKLEY W R CORP"
    },
    "TYL": {
        "cik": 860731,
        "title": "TYLER TECHNOLOGIES INC"
    },
    "EBR": {
        "cik": 1439124,
        "title": "BRAZILIAN ELECTRIC POWER CO"
    },
    "NTRS": {
        "cik": 73124,
        "title": "NORTHERN TRUST CORP"
    },
    "CCJ": {
        "cik": 1009001,
        "title": "CAMECO CORP"
    },
    "OMC": {
        "cik": 29989,
        "title": "OMNICOM GROUP INC."
    },
    "HDELY": {
        "cik": 1400691,
        "title": "HeidelbergCement AG"
    },
    "OWL": {
        "cik": 1823945,
        "title": "BLUE OWL CAPITAL INC."
    },
    "XPEV": {
        "cik": 1810997,
        "title": "XPENG INC."
    },
    "SUI": {
        "cik": 912593,
        "title": "SUN COMMUNITIES INC"
    },
    "ESS": {
        "cik": 920522,
        "title": "ESSEX PROPERTY TRUST, INC."
    },
    "CF": {
        "cik": 1324404,
        "title": "CF Industries Holdings, Inc."
    },
    "MGM": {
        "cik": 789570,
        "title": "MGM Resorts International"
    },
    "AKAM": {
        "cik": 1086222,
        "title": "AKAMAI TECHNOLOGIES INC"
    },
    "TXT": {
        "cik": 217346,
        "title": "TEXTRON INC"
    },
    "EG": {
        "cik": 1095073,
        "title": "EVEREST GROUP, LTD."
    },
    "DGX": {
        "cik": 1022079,
        "title": "QUEST DIAGNOSTICS INC"
    },
    "EXAS": {
        "cik": 1124140,
        "title": "EXACT SCIENCES CORP"
    },
    "SNAP": {
        "cik": 1564408,
        "title": "Snap Inc"
    },
    "TRU": {
        "cik": 1552033,
        "title": "TransUnion"
    },
    "KB": {
        "cik": 1445930,
        "title": "KB Financial Group Inc."
    },
    "BAH": {
        "cik": 1443646,
        "title": "Booz Allen Hamilton Holding Corp"
    },
    "AVTR": {
        "cik": 1722482,
        "title": "Avantor, Inc."
    },
    "AER": {
        "cik": 1378789,
        "title": "AerCap Holdings N.V."
    },
    "ERIE": {
        "cik": 922621,
        "title": "ERIE INDEMNITY CO"
    },
    "ENTG": {
        "cik": 1101302,
        "title": "ENTEGRIS INC"
    },
    "DECK": {
        "cik": 910521,
        "title": "DECKERS OUTDOOR CORP"
    },
    "AXON": {
        "cik": 1069183,
        "title": "AXON ENTERPRISE, INC."
    },
    "BIP": {
        "cik": 1406234,
        "title": "Brookfield Infrastructure Partners L.P."
    },
    "INCY": {
        "cik": 879169,
        "title": "INCYTE CORP"
    },
    "TPL": {
        "cik": 1811074,
        "title": "Texas Pacific Land Corp"
    },
    "AVY": {
        "cik": 8818,
        "title": "Avery Dennison Corp"
    },
    "AMH": {
        "cik": 1562401,
        "title": "American Homes 4 Rent"
    },
    "SJM": {
        "cik": 91419,
        "title": "J M SMUCKER Co"
    },
    "RVTY": {
        "cik": 31791,
        "title": "REVVITY, INC."
    },
    "CAG": {
        "cik": 23217,
        "title": "CONAGRA BRANDS INC."
    },
    "LCID": {
        "cik": 1811210,
        "title": "Lucid Group, Inc."
    },
    "VIV": {
        "cik": 1066119,
        "title": "TELEFONICA BRASIL S.A."
    },
    "SNA": {
        "cik": 91440,
        "title": "Snap-on Inc"
    },
    "KKPNY": {
        "cik": 1001474,
        "title": "KONINKLIJKE KPN N V"
    },
    "FMS": {
        "cik": 1333141,
        "title": "Fresenius Medical Care AG & Co. KGaA"
    },
    "L": {
        "cik": 60086,
        "title": "LOEWS CORP"
    },
    "HTHT": {
        "cik": 1483994,
        "title": "H World Group Ltd"
    },
    "SMPNY": {
        "cik": 1669414,
        "title": "Sompo Japan Nipponkoa Holdings, Inc./ADR"
    },
    "AMCR": {
        "cik": 1748790,
        "title": "Amcor plc"
    },
    "LKQ": {
        "cik": 1065696,
        "title": "LKQ CORP"
    },
    "EPAM": {
        "cik": 1352010,
        "title": "EPAM Systems, Inc."
    },
    "MGDDY": {
        "cik": 896076,
        "title": "MICHELIN COMPAGNIE GENERALE DES ETABLISSEMENTS MICHELIN /FI"
    },
    "ZBRA": {
        "cik": 877212,
        "title": "ZEBRA TECHNOLOGIES CORP"
    },
    "PODD": {
        "cik": 1145197,
        "title": "INSULET CORP"
    },
    "XP": {
        "cik": 1787425,
        "title": "XP Inc."
    },
    "SYF": {
        "cik": 1601712,
        "title": "Synchrony Financial"
    },
    "BAM": {
        "cik": 1937926,
        "title": "Brookfield Asset Management Ltd."
    },
    "LW": {
        "cik": 1679273,
        "title": "Lamb Weston Holdings, Inc."
    },
    "SWK": {
        "cik": 93556,
        "title": "STANLEY BLACK & DECKER, INC."
    },
    "SSNC": {
        "cik": 1402436,
        "title": "SS&C Technologies Holdings Inc"
    },
    "JBL": {
        "cik": 898293,
        "title": "JABIL INC"
    },
    "POOL": {
        "cik": 945841,
        "title": "POOL CORP"
    },
    "SHG": {
        "cik": 1263043,
        "title": "SHINHAN FINANCIAL GROUP CO LTD"
    },
    "WPC": {
        "cik": 1025378,
        "title": "W. P. Carey Inc."
    },
    "WSO": {
        "cik": 105016,
        "title": "WATSCO INC"
    },
    "CELH": {
        "cik": 1341766,
        "title": "Celsius Holdings, Inc."
    },
    "BSY": {
        "cik": 1031308,
        "title": "BENTLEY SYSTEMS INC"
    },
    "DT": {
        "cik": 1773383,
        "title": "Dynatrace, Inc."
    },
    "APA": {
        "cik": 1841666,
        "title": "APA Corp"
    },
    "APP": {
        "cik": 1751008,
        "title": "AppLovin Corp"
    },
    "CSL": {
        "cik": 790051,
        "title": "CARLISLE COMPANIES INC"
    },
    "TAP": {
        "cik": 24545,
        "title": "MOLSON COORS BEVERAGE CO"
    },
    "STX": {
        "cik": 1137789,
        "title": "Seagate Technology Holdings plc"
    },
    "VTRS": {
        "cik": 1792044,
        "title": "Viatris Inc"
    },
    "DPZ": {
        "cik": 1286681,
        "title": "DOMINOS PIZZA INC"
    },
    "SMCI": {
        "cik": 1375365,
        "title": "Super Micro Computer, Inc."
    },
    "GEN": {
        "cik": 849399,
        "title": "Gen Digital Inc."
    },
    "AGR": {
        "cik": 1634997,
        "title": "Avangrid, Inc."
    },
    "RPRX": {
        "cik": 1802768,
        "title": "Royalty Pharma plc"
    },
    "OVV": {
        "cik": 1792580,
        "title": "Ovintiv Inc."
    },
    "TKHVY": {
        "cik": 1446444,
        "title": "Turk Hava Yollari A.O."
    },
    "MMP": {
        "cik": 1126975,
        "title": "Magellan Midstream Partners, L.P."
    },
    "VRT": {
        "cik": 1674101,
        "title": "Vertiv Holdings Co"
    },
    "LDOS": {
        "cik": 1336920,
        "title": "Leidos Holdings, Inc."
    },
    "NDSN": {
        "cik": 72331,
        "title": "NORDSON CORP"
    },
    "MOS": {
        "cik": 1285785,
        "title": "MOSAIC CO"
    },
    "U": {
        "cik": 1810806,
        "title": "Unity Software Inc."
    },
    "PTCAY": {
        "cik": 1547873,
        "title": "PT Chandra Asri Petrochemical Tbk/ADR"
    },
    "TRMB": {
        "cik": 864749,
        "title": "TRIMBLE INC."
    },
    "PKG": {
        "cik": 75677,
        "title": "PACKAGING CORP OF AMERICA"
    },
    "LBRDA": {
        "cik": 1611983,
        "title": "Liberty Broadband Corp"
    },
    "CFG": {
        "cik": 759944,
        "title": "CITIZENS FINANCIAL GROUP INC/RI"
    },
    "RPM": {
        "cik": 110621,
        "title": "RPM INTERNATIONAL INC/DE/"
    },
    "LNNGY": {
        "cik": 1447629,
        "title": "Li Ning Co. Ltd."
    },
    "BEN": {
        "cik": 38777,
        "title": "FRANKLIN RESOURCES INC"
    },
    "HLDCY": {
        "cik": 811250,
        "title": "HENDERSON LAND DEVELOPMENT COMPANY LTD /FI"
    },
    "SUZ": {
        "cik": 909327,
        "title": "Suzano S.A."
    },
    "WDC": {
        "cik": 106040,
        "title": "WESTERN DIGITAL CORP"
    },
    "EVRG": {
        "cik": 1711269,
        "title": "Evergy, Inc."
    },
    "ELS": {
        "cik": 895417,
        "title": "EQUITY LIFESTYLE PROPERTIES INC"
    },
    "CE": {
        "cik": 1306830,
        "title": "Celanese Corp"
    },
    "GRAB": {
        "cik": 1855612,
        "title": "Grab Holdings Ltd"
    },
    "JHX": {
        "cik": 1159152,
        "title": "James Hardie Industries plc"
    },
    "SGIOY": {
        "cik": 1281721,
        "title": "SHIONOGI & CO LTD"
    },
    "IHG": {
        "cik": 858446,
        "title": "INTERCONTINENTAL HOTELS GROUP PLC /NEW/"
    },
    "BOUYY": {
        "cik": 1445475,
        "title": "Bouygues SA"
    },
    "KMX": {
        "cik": 1170010,
        "title": "CARMAX INC"
    },
    "GGG": {
        "cik": 42888,
        "title": "GRACO INC"
    },
    "DKS": {
        "cik": 1089063,
        "title": "DICK'S SPORTING GOODS, INC."
    },
    "MAS": {
        "cik": 62996,
        "title": "MASCO CORP /DE/"
    },
    "LNT": {
        "cik": 352541,
        "title": "ALLIANT ENERGY CORP"
    },
    "IOT": {
        "cik": 1642896,
        "title": "Samsara Inc."
    },
    "AZPN": {
        "cik": 1897982,
        "title": "Aspen Technology, Inc."
    },
    "DKNG": {
        "cik": 1883685,
        "title": "DraftKings Inc."
    },
    "CPB": {
        "cik": 16732,
        "title": "CAMPBELL SOUP CO"
    },
    "NICE": {
        "cik": 1003935,
        "title": "NICE Ltd."
    },
    "LSCC": {
        "cik": 855658,
        "title": "LATTICE SEMICONDUCTOR CORP"
    },
    "ACI": {
        "cik": 1646972,
        "title": "Albertsons Companies, Inc."
    },
    "TECH": {
        "cik": 842023,
        "title": "BIO-TECHNE Corp"
    },
    "IPG": {
        "cik": 51644,
        "title": "INTERPUBLIC GROUP OF COMPANIES, INC."
    },
    "LII": {
        "cik": 1069202,
        "title": "LENNOX INTERNATIONAL INC"
    },
    "MTCH": {
        "cik": 891103,
        "title": "Match Group, Inc."
    },
    "GFL": {
        "cik": 1780232,
        "title": "GFL Environmental Inc."
    },
    "LEGN": {
        "cik": 1801198,
        "title": "Legend Biotech Corp"
    },
    "OC": {
        "cik": 1370946,
        "title": "Owens Corning"
    },
    "TME": {
        "cik": 1744676,
        "title": "Tencent Music Entertainment Group"
    },
    "ACM": {
        "cik": 868857,
        "title": "AECOM"
    },
    "GLPI": {
        "cik": 1575965,
        "title": "Gaming & Leisure Properties, Inc."
    },
    "AES": {
        "cik": 874761,
        "title": "AES CORP"
    },
    "RDY": {
        "cik": 1135951,
        "title": "DR REDDYS LABORATORIES LTD"
    },
    "SNN": {
        "cik": 845982,
        "title": "SMITH & NEPHEW PLC"
    },
    "H": {
        "cik": 1468174,
        "title": "Hyatt Hotels Corp"
    },
    "OKTA": {
        "cik": 1660134,
        "title": "Okta, Inc."
    },
    "NWSA": {
        "cik": 1564708,
        "title": "NEWS CORP"
    },
    "IP": {
        "cik": 51434,
        "title": "INTERNATIONAL PAPER CO /NEW/"
    },
    "RYAN": {
        "cik": 1849253,
        "title": "RYAN SPECIALTY HOLDINGS, INC."
    },
    "CHWY": {
        "cik": 1766502,
        "title": "Chewy, Inc."
    },
    "BKI": {
        "cik": 1627014,
        "title": "Black Knight, Inc."
    },
    "KIM": {
        "cik": 879101,
        "title": "KIMCO REALTY CORP"
    },
    "PAG": {
        "cik": 1019849,
        "title": "PENSKE AUTOMOTIVE GROUP, INC."
    },
    "CHK": {
        "cik": 895126,
        "title": "CHESAPEAKE ENERGY CORP"
    },
    "CRBG": {
        "cik": 1889539,
        "title": "Corebridge Financial, Inc."
    },
    "LNVGY": {
        "cik": 932477,
        "title": "LENOVO GROUP LTD"
    },
    "MANH": {
        "cik": 1056696,
        "title": "MANHATTAN ASSOCIATES INC"
    },
    "FLEX": {
        "cik": 866374,
        "title": "FLEX LTD."
    },
    "BILL": {
        "cik": 1786352,
        "title": "BILL Holdings, Inc."
    },
    "PSTG": {
        "cik": 1474432,
        "title": "Pure Storage, Inc."
    },
    "YPF": {
        "cik": 904851,
        "title": "YPF SOCIEDAD ANONIMA"
    },
    "CX": {
        "cik": 1076378,
        "title": "CEMEX SAB DE CV"
    },
    "TOST": {
        "cik": 1650164,
        "title": "Toast, Inc."
    },
    "ZG": {
        "cik": 1617640,
        "title": "ZILLOW GROUP, INC."
    },
    "HST": {
        "cik": 1070750,
        "title": "HOST HOTELS & RESORTS, INC."
    },
    "JKHY": {
        "cik": 779152,
        "title": "JACK HENRY & ASSOCIATES INC"
    },
    "TFII": {
        "cik": 1588823,
        "title": "TFI International Inc."
    },
    "CPT": {
        "cik": 906345,
        "title": "CAMDEN PROPERTY TRUST"
    },
    "SMKUY": {
        "cik": 1555812,
        "title": "Siam Makro Public Co Limited/ADR"
    },
    "NMR": {
        "cik": 1163653,
        "title": "NOMURA HOLDINGS INC"
    },
    "VST": {
        "cik": 1692819,
        "title": "Vistra Corp."
    },
    "PTBRY": {
        "cik": 1504122,
        "title": "PT Bank Negara Indonesia (Persero) Tbk/ADR"
    },
    "TEVA": {
        "cik": 818686,
        "title": "TEVA PHARMACEUTICAL INDUSTRIES LTD"
    },
    "GLPEY": {
        "cik": 1385535,
        "title": "Galp Energia, SGPS, S.A."
    },
    "BURL": {
        "cik": 1579298,
        "title": "Burlington Stores, Inc."
    },
    "CZR": {
        "cik": 1590895,
        "title": "Caesars Entertainment, Inc."
    },
    "ROKU": {
        "cik": 1428439,
        "title": "ROKU, INC"
    },
    "FMC": {
        "cik": 37785,
        "title": "FMC CORP"
    },
    "BAP": {
        "cik": 1001290,
        "title": "CREDICORP LTD"
    },
    "PNR": {
        "cik": 77360,
        "title": "PENTAIR plc"
    },
    "DINO": {
        "cik": 1915657,
        "title": "HF Sinclair Corp"
    },
    "GDDY": {
        "cik": 1609711,
        "title": "GoDaddy Inc."
    },
    "TWLO": {
        "cik": 1447669,
        "title": "TWILIO INC"
    },
    "NI": {
        "cik": 1111711,
        "title": "NISOURCE INC."
    },
    "CHRW": {
        "cik": 1043277,
        "title": "C. H. ROBINSON WORLDWIDE, INC."
    },
    "FNF": {
        "cik": 1331875,
        "title": "Fidelity National Financial, Inc."
    },
    "PEAK": {
        "cik": 765880,
        "title": "HEALTHPEAK PROPERTIES, INC."
    },
    "UTHR": {
        "cik": 1082554,
        "title": "UNITED THERAPEUTICS Corp"
    },
    "CDAY": {
        "cik": 1725057,
        "title": "Ceridian HCM Holding Inc."
    },
    "BIO": {
        "cik": 12208,
        "title": "BIO-RAD LABORATORIES, INC."
    },
    "REXR": {
        "cik": 1571283,
        "title": "Rexford Industrial Realty, Inc."
    },
    "SAIA": {
        "cik": 1177702,
        "title": "SAIA INC"
    },
    "PCTY": {
        "cik": 1591698,
        "title": "Paylocity Holding Corp"
    },
    "BCH": {
        "cik": 1161125,
        "title": "BANK OF CHILE"
    },
    "GFI": {
        "cik": 1172724,
        "title": "GOLD FIELDS LTD"
    },
    "PAA": {
        "cik": 1070423,
        "title": "PLAINS ALL AMERICAN PIPELINE LP"
    },
    "LOGI": {
        "cik": 1032975,
        "title": "LOGITECH INTERNATIONAL S.A."
    },
    "GL": {
        "cik": 320335,
        "title": "GLOBE LIFE INC."
    },
    "FIVE": {
        "cik": 1177609,
        "title": "FIVE BELOW, INC"
    },
    "WYNN": {
        "cik": 1174922,
        "title": "WYNN RESORTS LTD"
    },
    "LECO": {
        "cik": 59527,
        "title": "LINCOLN ELECTRIC HOLDINGS INC"
    },
    "UHAL": {
        "cik": 4457,
        "title": "U-Haul Holding Co /NV/"
    },
    "CNA": {
        "cik": 21175,
        "title": "CNA FINANCIAL CORP"
    },
    "CG": {
        "cik": 1527166,
        "title": "Carlyle Group Inc."
    },
    "NBIX": {
        "cik": 914475,
        "title": "NEUROCRINE BIOSCIENCES INC"
    },
    "SRPT": {
        "cik": 873303,
        "title": "Sarepta Therapeutics, Inc."
    },
    "WES": {
        "cik": 1423902,
        "title": "Western Midstream Partners, LP"
    },
    "ARCC": {
        "cik": 1287750,
        "title": "ARES CAPITAL CORP"
    },
    "CCK": {
        "cik": 1219601,
        "title": "CROWN HOLDINGS INC"
    },
    "FND": {
        "cik": 1507079,
        "title": "Floor & Decor Holdings, Inc."
    },
    "RBA": {
        "cik": 1046102,
        "title": "RB GLOBAL INC."
    },
    "REG": {
        "cik": 910606,
        "title": "REGENCY CENTERS CORP"
    },
    "DOX": {
        "cik": 1062579,
        "title": "AMDOCS LTD"
    },
    "AOS": {
        "cik": 91142,
        "title": "SMITH A O CORP"
    },
    "CRL": {
        "cik": 1100682,
        "title": "CHARLES RIVER LABORATORIES INTERNATIONAL, INC."
    },
    "TFX": {
        "cik": 96943,
        "title": "TELEFLEX INC"
    },
    "WPP": {
        "cik": 806968,
        "title": "WPP plc"
    },
    "EMRAF": {
        "cik": 1127248,
        "title": "EMERA INC"
    },
    "KEY": {
        "cik": 91576,
        "title": "KEYCORP /NEW/"
    },
    "OTEX": {
        "cik": 1002638,
        "title": "OPEN TEXT CORP"
    },
    "TTC": {
        "cik": 737758,
        "title": "TORO CO"
    },
    "EME": {
        "cik": 105634,
        "title": "EMCOR Group, Inc."
    },
    "DAR": {
        "cik": 916540,
        "title": "DARLING INGREDIENTS INC."
    },
    "HSIC": {
        "cik": 1000228,
        "title": "HENRY SCHEIN INC"
    },
    "AEG": {
        "cik": 769218,
        "title": "AEGON NV"
    },
    "QGEN": {
        "cik": 1015820,
        "title": "QIAGEN N.V."
    },
    "EMN": {
        "cik": 915389,
        "title": "EASTMAN CHEMICAL CO"
    },
    "QRVO": {
        "cik": 1604778,
        "title": "Qorvo, Inc."
    },
    "AAL": {
        "cik": 6201,
        "title": "American Airlines Group Inc."
    },
    "EQH": {
        "cik": 1333986,
        "title": "Equitable Holdings, Inc."
    },
    "BXP": {
        "cik": 1037540,
        "title": "BOSTON PROPERTIES INC"
    },
    "AFG": {
        "cik": 1042046,
        "title": "AMERICAN FINANCIAL GROUP INC"
    },
    "RRX": {
        "cik": 82811,
        "title": "REGAL REXNORD CORP"
    },
    "DOCU": {
        "cik": 1261333,
        "title": "DOCUSIGN, INC."
    },
    "WTRG": {
        "cik": 78128,
        "title": "Essential Utilities, Inc."
    },
    "WMS": {
        "cik": 1604028,
        "title": "ADVANCED DRAINAGE SYSTEMS, INC."
    },
    "CFLT": {
        "cik": 1699838,
        "title": "Confluent, Inc."
    },
    "PFGC": {
        "cik": 1618673,
        "title": "Performance Food Group Co"
    },
    "UNM": {
        "cik": 5513,
        "title": "Unum Group"
    },
    "PARA": {
        "cik": 813828,
        "title": "Paramount Global"
    },
    "ACCYY": {
        "cik": 1049183,
        "title": "ACCOR"
    },
    "UI": {
        "cik": 1511737,
        "title": "Ubiquiti Inc."
    },
    "SCI": {
        "cik": 89089,
        "title": "SERVICE CORP INTERNATIONAL"
    },
    "ARMK": {
        "cik": 1584509,
        "title": "Aramark"
    },
    "ONON": {
        "cik": 1858985,
        "title": "On Holding AG"
    },
    "PEN": {
        "cik": 1321732,
        "title": "Penumbra Inc"
    },
    "MKTX": {
        "cik": 1278021,
        "title": "MARKETAXESS HOLDINGS INC"
    },
    "ALLE": {
        "cik": 1579241,
        "title": "Allegion plc"
    },
    "FFIV": {
        "cik": 1048695,
        "title": "F5, INC."
    },
    "DBX": {
        "cik": 1467623,
        "title": "DROPBOX, INC."
    },
    "USFD": {
        "cik": 1665918,
        "title": "US Foods Holding Corp."
    },
    "NLY": {
        "cik": 1043219,
        "title": "ANNALY CAPITAL MANAGEMENT INC"
    },
    "HOOD": {
        "cik": 1783879,
        "title": "Robinhood Markets, Inc."
    },
    "COTY": {
        "cik": 1024305,
        "title": "COTY INC."
    },
    "BPYPP": {
        "cik": 1545772,
        "title": "Brookfield Property Partners L.P."
    },
    "CUBE": {
        "cik": 1298675,
        "title": "CubeSmart"
    },
    "BJ": {
        "cik": 1531152,
        "title": "BJ's Wholesale Club Holdings, Inc."
    },
    "BWA": {
        "cik": 908255,
        "title": "BORGWARNER INC"
    },
    "CHDN": {
        "cik": 20212,
        "title": "Churchill Downs Inc"
    },
    "CLH": {
        "cik": 822818,
        "title": "CLEAN HARBORS INC"
    },
    "DVA": {
        "cik": 927066,
        "title": "DAVITA INC."
    },
    "CASY": {
        "cik": 726958,
        "title": "CASEYS GENERAL STORES INC"
    },
    "SEDG": {
        "cik": 1419612,
        "title": "SOLAREDGE TECHNOLOGIES, INC."
    },
    "MORN": {
        "cik": 1289419,
        "title": "Morningstar, Inc."
    },
    "SNX": {
        "cik": 1177394,
        "title": "TD SYNNEX CORP"
    },
    "BRKR": {
        "cik": 1109354,
        "title": "BRUKER CORP"
    },
    "VIVHY": {
        "cik": 1127055,
        "title": "VIVENDI"
    },
    "KNX": {
        "cik": 1492691,
        "title": "Knight-Swift Transportation Holdings Inc."
    },
    "ETSY": {
        "cik": 1370637,
        "title": "ETSY INC"
    },
    "RNR": {
        "cik": 913144,
        "title": "RENAISSANCERE HOLDINGS LTD"
    },
    "ESLT": {
        "cik": 1027664,
        "title": "ELBIT SYSTEMS LTD"
    },
    "CAR": {
        "cik": 723612,
        "title": "AVIS BUDGET GROUP, INC."
    },
    "RGA": {
        "cik": 898174,
        "title": "REINSURANCE GROUP OF AMERICA INC"
    },
    "OUKPY": {
        "cik": 1436786,
        "title": "Outotec OYJ"
    },
    "OMRNY": {
        "cik": 800954,
        "title": "OMRON CORP /FI"
    },
    "JNPR": {
        "cik": 1043604,
        "title": "JUNIPER NETWORKS INC"
    },
    "UHS": {
        "cik": 352915,
        "title": "UNIVERSAL HEALTH SERVICES INC"
    },
    "PAC": {
        "cik": 1347557,
        "title": "Pacific Airport Group"
    },
    "JAZZ": {
        "cik": 1232524,
        "title": "Jazz Pharmaceuticals plc"
    },
    "EDU": {
        "cik": 1372920,
        "title": "New Oriental Education & Technology Group Inc."
    },
    "RGEN": {
        "cik": 730272,
        "title": "REPLIGEN CORP"
    },
    "BLD": {
        "cik": 1633931,
        "title": "TopBuild Corp"
    },
    "VIPS": {
        "cik": 1529192,
        "title": "Vipshop Holdings Ltd"
    },
    "LAMR": {
        "cik": 1090425,
        "title": "LAMAR ADVERTISING CO/NEW"
    },
    "AGCO": {
        "cik": 880266,
        "title": "AGCO CORP /DE"
    },
    "HAS": {
        "cik": 46080,
        "title": "HASBRO, INC."
    },
    "PNW": {
        "cik": 764622,
        "title": "PINNACLE WEST CAPITAL CORP"
    },
    "GRFS": {
        "cik": 1438569,
        "title": "Grifols SA"
    },
    "PCOR": {
        "cik": 1611052,
        "title": "PROCORE TECHNOLOGIES, INC."
    },
    "HII": {
        "cik": 1501585,
        "title": "HUNTINGTON INGALLS INDUSTRIES, INC."
    },
    "MTN": {
        "cik": 812011,
        "title": "VAIL RESORTS INC"
    },
    "USO": {
        "cik": 1327068,
        "title": "United States Oil Fund, LP"
    },
    "NVT": {
        "cik": 1720635,
        "title": "nVent Electric plc"
    },
    "GGB": {
        "cik": 1073404,
        "title": "GERDAU S.A."
    },
    "NYCB": {
        "cik": 910073,
        "title": "NEW YORK COMMUNITY BANCORP INC"
    },
    "COLD": {
        "cik": 1455863,
        "title": "AMERICOLD REALTY TRUST"
    },
    "BSAC": {
        "cik": 1027552,
        "title": "BANCO SANTANDER CHILE"
    },
    "KNSL": {
        "cik": 1669162,
        "title": "Kinsale Capital Group, Inc."
    },
    "MTLHY": {
        "cik": 1446418,
        "title": "Mitsubishi Chemical Holdings Corp"
    },
    "KEP": {
        "cik": 887225,
        "title": "KOREA ELECTRIC POWER CORP"
    },
    "PATH": {
        "cik": 1734722,
        "title": "UiPath, Inc."
    },
    "NRG": {
        "cik": 1013871,
        "title": "NRG ENERGY, INC."
    },
    "WSC": {
        "cik": 1647088,
        "title": "WillScot Mobile Mini Holdings Corp."
    },
    "BBWI": {
        "cik": 701985,
        "title": "Bath & Body Works, Inc."
    },
    "WWE": {
        "cik": 1091907,
        "title": "WORLD WRESTLING ENTERTAINMENTINC"
    },
    "TTEK": {
        "cik": 831641,
        "title": "TETRA TECH INC"
    },
    "JBSAY": {
        "cik": 1450123,
        "title": "JBS S.A."
    },
    "LEA": {
        "cik": 842162,
        "title": "LEAR CORP"
    },
    "FBIN": {
        "cik": 1519751,
        "title": "Fortune Brands Innovations, Inc."
    },
    "ROIV": {
        "cik": 1635088,
        "title": "Roivant Sciences Ltd."
    },
    "AR": {
        "cik": 1433270,
        "title": "ANTERO RESOURCES Corp"
    },
    "STVN": {
        "cik": 1849853,
        "title": "Stevanato Group S.p.A."
    },
    "WSM": {
        "cik": 719955,
        "title": "WILLIAMS SONOMA INC"
    },
    "ASR": {
        "cik": 1123452,
        "title": "SOUTHEAST AIRPORT GROUP"
    },
    "LAD": {
        "cik": 1023128,
        "title": "LITHIA MOTORS INC"
    },
    "KBR": {
        "cik": 1357615,
        "title": "KBR, INC."
    },
    "DLB": {
        "cik": 1308547,
        "title": "Dolby Laboratories, Inc."
    },
    "TOL": {
        "cik": 794170,
        "title": "Toll Brothers, Inc."
    },
    "TPG": {
        "cik": 1880661,
        "title": "TPG Inc."
    },
    "CTLT": {
        "cik": 1596783,
        "title": "Catalent, Inc."
    },
    "ROHCY": {
        "cik": 1442653,
        "title": "ROHM Co., Ltd."
    },
    "LBTYA": {
        "cik": 1570585,
        "title": "Liberty Global plc"
    },
    "XPO": {
        "cik": 1166003,
        "title": "XPO, Inc."
    },
    "SEIC": {
        "cik": 350894,
        "title": "SEI INVESTMENTS CO"
    },
    "ALLY": {
        "cik": 40729,
        "title": "Ally Financial Inc."
    },
    "ATR": {
        "cik": 896622,
        "title": "APTARGROUP, INC."
    },
    "SSL": {
        "cik": 314590,
        "title": "SASOL LTD"
    },
    "RHI": {
        "cik": 315213,
        "title": "ROBERT HALF INC."
    },
    "SBS": {
        "cik": 1170858,
        "title": "COMPANHIA DE SANEAMENTO BASICO DO ESTADO DE SAO PAULO-SABESP"
    },
    "SWAV": {
        "cik": 1642545,
        "title": "Shockwave Medical, Inc."
    },
    "WRK": {
        "cik": 1732845,
        "title": "WestRock Co"
    },
    "ALV": {
        "cik": 1034670,
        "title": "AUTOLIV INC"
    },
    "MNDY": {
        "cik": 1845338,
        "title": "monday.com Ltd."
    },
    "NOV": {
        "cik": 1021860,
        "title": "NOV Inc."
    },
    "FTI": {
        "cik": 1681459,
        "title": "TechnipFMC plc"
    },
    "VFC": {
        "cik": 103379,
        "title": "V F CORP"
    },
    "CGNX": {
        "cik": 851205,
        "title": "COGNEX CORP"
    },
    "ORI": {
        "cik": 74260,
        "title": "OLD REPUBLIC INTERNATIONAL CORP"
    },
    "XRAY": {
        "cik": 818479,
        "title": "DENTSPLY SIRONA Inc."
    },
    "SKX": {
        "cik": 1065837,
        "title": "SKECHERS USA INC"
    },
    "EGP": {
        "cik": 49600,
        "title": "EASTGROUP PROPERTIES INC"
    },
    "W": {
        "cik": 1616707,
        "title": "Wayfair Inc."
    },
    "ZI": {
        "cik": 1794515,
        "title": "ZoomInfo Technologies Inc."
    },
    "TPR": {
        "cik": 1116132,
        "title": "TAPESTRY, INC."
    },
    "LKNCY": {
        "cik": 1767582,
        "title": "Luckin Coffee Inc."
    },
    "WCC": {
        "cik": 929008,
        "title": "WESCO INTERNATIONAL INC"
    },
    "NATI": {
        "cik": 935494,
        "title": "NATIONAL INSTRUMENTS CORP"
    },
    "ICL": {
        "cik": 941221,
        "title": "ICL Group Ltd."
    },
    "ITT": {
        "cik": 216228,
        "title": "ITT INC."
    },
    "FRT": {
        "cik": 34903,
        "title": "FEDERAL REALTY INVESTMENT TRUST"
    },
    "CW": {
        "cik": 26324,
        "title": "CURTISS WRIGHT CORP"
    },
    "WEX": {
        "cik": 1309108,
        "title": "WEX Inc."
    },
    "TX": {
        "cik": 1342874,
        "title": "Ternium S.A."
    },
    "SOFI": {
        "cik": 1818874,
        "title": "SoFi Technologies, Inc."
    },
    "RRC": {
        "cik": 315852,
        "title": "RANGE RESOURCES CORP"
    },
    "CMS-PB": {
        "cik": 201533,
        "title": "CONSUMERS ENERGY CO"
    },
    "EWBC": {
        "cik": 1069157,
        "title": "EAST WEST BANCORP INC"
    },
    "JLL": {
        "cik": 1037976,
        "title": "JONES LANG LASALLE INC"
    },
    "CLF": {
        "cik": 764065,
        "title": "CLEVELAND-CLIFFS INC."
    },
    "LSXMA": {
        "cik": 1560385,
        "title": "Liberty Media Corp"
    },
    "IEP": {
        "cik": 813762,
        "title": "ICAHN ENTERPRISES L.P."
    },
    "SKM": {
        "cik": 1015650,
        "title": "SK TELECOM CO LTD"
    },
    "DSEEY": {
        "cik": 1481045,
        "title": "Daiwa Securities Group Inc."
    },
    "PSNY": {
        "cik": 1884082,
        "title": "Polestar Automotive Holding UK PLC"
    },
    "JEF": {
        "cik": 96223,
        "title": "Jefferies Financial Group Inc."
    },
    "AIZ": {
        "cik": 1267238,
        "title": "ASSURANT, INC."
    },
    "CHE": {
        "cik": 19584,
        "title": "CHEMED CORP"
    },
    "MIDD": {
        "cik": 769520,
        "title": "MIDDLEBY Corp"
    },
    "WWD": {
        "cik": 108312,
        "title": "Woodward, Inc."
    },
    "RL": {
        "cik": 1037038,
        "title": "RALPH LAUREN CORP"
    },
    "MEDP": {
        "cik": 1668397,
        "title": "Medpace Holdings, Inc."
    },
    "CAE": {
        "cik": 1173382,
        "title": "CAE INC"
    },
    "BERY": {
        "cik": 1378992,
        "title": "BERRY GLOBAL GROUP, INC."
    },
    "HNGKY": {
        "cik": 871464,
        "title": "HONGKONG LAND HOLDINGS LTD /FI"
    },
    "GNTX": {
        "cik": 355811,
        "title": "GENTEX CORP"
    },
    "MTZ": {
        "cik": 15615,
        "title": "MASTEC INC"
    },
    "MAT": {
        "cik": 63276,
        "title": "MATTEL INC /DE/"
    },
    "CACI": {
        "cik": 16058,
        "title": "CACI INTERNATIONAL INC /DE/"
    },
    "ALGM": {
        "cik": 866291,
        "title": "ALLEGRO MICROSYSTEMS, INC."
    },
    "GXO": {
        "cik": 1852244,
        "title": "GXO Logistics, Inc."
    },
    "PSO": {
        "cik": 938323,
        "title": "PEARSON PLC"
    },
    "GLOB": {
        "cik": 1557860,
        "title": "Globant S.A."
    },
    "OLN": {
        "cik": 74303,
        "title": "OLIN Corp"
    },
    "EDR": {
        "cik": 1766363,
        "title": "Endeavor Group Holdings, Inc."
    },
    "WHR": {
        "cik": 106640,
        "title": "WHIRLPOOL CORP /DE/"
    },
    "DCI": {
        "cik": 29644,
        "title": "DONALDSON Co INC"
    },
    "SWN": {
        "cik": 7332,
        "title": "SOUTHWESTERN ENERGY CO"
    },
    "PRI": {
        "cik": 1475922,
        "title": "Primerica, Inc."
    },
    "TPX": {
        "cik": 1206264,
        "title": "TEMPUR SEALY INTERNATIONAL, INC."
    },
    "MTDR": {
        "cik": 1520006,
        "title": "Matador Resources Co"
    },
    "SLV": {
        "cik": 1330568,
        "title": "iShares Silver Trust"
    },
    "TREX": {
        "cik": 1069878,
        "title": "TREX CO INC"
    },
    "OHI": {
        "cik": 888491,
        "title": "OMEGA HEALTHCARE INVESTORS INC"
    },
    "THC": {
        "cik": 70318,
        "title": "TENET HEALTHCARE CORP"
    },
    "NTNX": {
        "cik": 1618732,
        "title": "Nutanix, Inc."
    },
    "PR": {
        "cik": 1658566,
        "title": "Permian Resources Corp"
    },
    "ARW": {
        "cik": 7536,
        "title": "ARROW ELECTRONICS, INC."
    },
    "WBS": {
        "cik": 801337,
        "title": "WEBSTER FINANCIAL CORP"
    },
    "STN": {
        "cik": 1131383,
        "title": "STANTEC INC"
    },
    "GNRC": {
        "cik": 1474735,
        "title": "GENERAC HOLDINGS INC."
    },
    "OLED": {
        "cik": 1005284,
        "title": "UNIVERSAL DISPLAY CORP \\PA\\"
    },
    "X": {
        "cik": 1163302,
        "title": "UNITED STATES STEEL CORP"
    },
    "AGL": {
        "cik": 1831097,
        "title": "agilon health, inc."
    },
    "NCLH": {
        "cik": 1513761,
        "title": "Norwegian Cruise Line Holdings Ltd."
    },
    "BDNNY": {
        "cik": 1446457,
        "title": "Boliden AB"
    },
    "HESM": {
        "cik": 1789832,
        "title": "Hess Midstream LP"
    },
    "NE": {
        "cik": 1895262,
        "title": "Noble Corp plc"
    },
    "CNM": {
        "cik": 1856525,
        "title": "Core & Main, Inc."
    },
    "CVNA": {
        "cik": 1690820,
        "title": "CARVANA CO."
    },
    "TIMB": {
        "cik": 1826168,
        "title": "TIM S.A."
    },
    "ASXFY": {
        "cik": 1449003,
        "title": "ASX Ltd."
    },
    "FHN": {
        "cik": 36966,
        "title": "FIRST HORIZON CORP"
    },
    "MUR": {
        "cik": 717423,
        "title": "MURPHY OIL CORP"
    },
    "RGLD": {
        "cik": 85535,
        "title": "ROYAL GOLD INC"
    },
    "AN": {
        "cik": 350698,
        "title": "AUTONATION, INC."
    },
    "GTLS": {
        "cik": 892553,
        "title": "CHART INDUSTRIES INC"
    },
    "NNN": {
        "cik": 751364,
        "title": "NNN REIT, INC."
    },
    "ACHC": {
        "cik": 1520697,
        "title": "Acadia Healthcare Company, Inc."
    },
    "EHC": {
        "cik": 785161,
        "title": "Encompass Health Corp"
    },
    "EXEL": {
        "cik": 939767,
        "title": "EXELIXIS, INC."
    },
    "NYT": {
        "cik": 71691,
        "title": "NEW YORK TIMES CO"
    },
    "UELMO": {
        "cik": 100826,
        "title": "UNION ELECTRIC CO"
    },
    "IVZ": {
        "cik": 914208,
        "title": "Invesco Ltd."
    },
    "RCM": {
        "cik": 1910851,
        "title": "R1 RCM Inc. /DE"
    },
    "ITTOY": {
        "cik": 1512544,
        "title": "ITOCHU Techno-Solutions Corporation/ADR"
    },
    "TXRH": {
        "cik": 1289460,
        "title": "Texas Roadhouse, Inc."
    },
    "CIB": {
        "cik": 1071371,
        "title": "BANCOLOMBIA SA"
    },
    "SITE": {
        "cik": 1650729,
        "title": "SiteOne Landscape Supply, Inc."
    },
    "CHX": {
        "cik": 1723089,
        "title": "ChampionX Corp"
    },
    "DUFRY": {
        "cik": 1546354,
        "title": "Dufry AG/ADR"
    },
    "MSA": {
        "cik": 66570,
        "title": "MSA Safety Inc"
    },
    "VOYA": {
        "cik": 1535929,
        "title": "Voya Financial, Inc."
    },
    "MEJHY": {
        "cik": 1558812,
        "title": "MEIJI Holdings Co Ltd/ADR"
    },
    "SMBMY": {
        "cik": 1448978,
        "title": "SembCorp Marine Ltd."
    },
    "HLI": {
        "cik": 1302215,
        "title": "HOULIHAN LOKEY, INC."
    },
    "GTLB": {
        "cik": 1653482,
        "title": "Gitlab Inc."
    },
    "MUSA": {
        "cik": 1573516,
        "title": "Murphy USA Inc."
    },
    "FUTU": {
        "cik": 1754581,
        "title": "Futu Holdings Ltd"
    },
    "AU": {
        "cik": 1067428,
        "title": "ANGLOGOLD ASHANTI LTD"
    },
    "FR": {
        "cik": 921825,
        "title": "FIRST INDUSTRIAL REALTY TRUST INC"
    },
    "YNDX": {
        "cik": 1513845,
        "title": "Yandex N.V."
    },
    "LSTR": {
        "cik": 853816,
        "title": "LANDSTAR SYSTEM INC"
    },
    "BLCO": {
        "cik": 1860742,
        "title": "Bausch & Lomb Corp"
    },
    "CCCS": {
        "cik": 1818201,
        "title": "CCC Intelligent Solutions Holdings Inc."
    },
    "OGE": {
        "cik": 1021635,
        "title": "OGE ENERGY CORP."
    },
    "LNW": {
        "cik": 750004,
        "title": "Light & Wonder, Inc."
    },
    "CSAN": {
        "cik": 1430162,
        "title": "Cosan S.A."
    },
    "G": {
        "cik": 1398659,
        "title": "Genpact LTD"
    },
    "SF": {
        "cik": 720672,
        "title": "STIFEL FINANCIAL CORP"
    },
    "GPK": {
        "cik": 1408075,
        "title": "GRAPHIC PACKAGING HOLDING CO"
    },
    "APPF": {
        "cik": 1433195,
        "title": "APPFOLIO INC"
    },
    "INGR": {
        "cik": 1046257,
        "title": "Ingredion Inc"
    },
    "MNSO": {
        "cik": 1815846,
        "title": "MINISO Group Holding Ltd"
    },
    "KRTX": {
        "cik": 1771917,
        "title": "Karuna Therapeutics, Inc."
    },
    "PUTKY": {
        "cik": 1455955,
        "title": "PT United Tractors Tbk / ADR"
    },
    "YMM": {
        "cik": 1838413,
        "title": "Full Truck Alliance Co. Ltd."
    },
    "BYD": {
        "cik": 906553,
        "title": "BOYD GAMING CORP"
    },
    "BWXT": {
        "cik": 1486957,
        "title": "BWX Technologies, Inc."
    },
    "CHH": {
        "cik": 1046311,
        "title": "CHOICE HOTELS INTERNATIONAL INC /DE"
    },
    "CHRD": {
        "cik": 1486159,
        "title": "Chord Energy Corp"
    },
    "LFUS": {
        "cik": 889331,
        "title": "LITTELFUSE INC /DE"
    },
    "APG": {
        "cik": 1796209,
        "title": "APi Group Corp"
    },
    "FSV": {
        "cik": 1637810,
        "title": "FirstService Corp"
    },
    "GWRE": {
        "cik": 1528396,
        "title": "Guidewire Software, Inc."
    },
    "COKE": {
        "cik": 317540,
        "title": "Coca-Cola Consolidated, Inc."
    },
    "CIVI": {
        "cik": 1509589,
        "title": "CIVITAS RESOURCES, INC."
    },
    "WFG": {
        "cik": 1402388,
        "title": "WEST FRASER TIMBER CO., LTD"
    },
    "SSD": {
        "cik": 920371,
        "title": "Simpson Manufacturing Co., Inc."
    },
    "ELF": {
        "cik": 1600033,
        "title": "e.l.f. Beauty, Inc."
    },
    "CMC": {
        "cik": 22444,
        "title": "COMMERCIAL METALS Co"
    },
    "CYBR": {
        "cik": 1598110,
        "title": "CyberArk Software Ltd."
    },
    "PII": {
        "cik": 931015,
        "title": "Polaris Inc."
    },
    "STAG": {
        "cik": 1479094,
        "title": "STAG Industrial, Inc."
    },
    "OSK": {
        "cik": 775158,
        "title": "OSHKOSH CORP"
    },
    "HR": {
        "cik": 1360604,
        "title": "Healthcare Realty Trust Inc"
    },
    "RETA": {
        "cik": 1358762,
        "title": "REATA PHARMACEUTICALS INC"
    },
    "INSP": {
        "cik": 1609550,
        "title": "Inspire Medical Systems, Inc."
    },
    "SPSC": {
        "cik": 1092699,
        "title": "SPS COMMERCE INC"
    },
    "RH": {
        "cik": 1528849,
        "title": "RH"
    },
    "BRX": {
        "cik": 1581068,
        "title": "Brixmor Property Group Inc."
    },
    "MKSI": {
        "cik": 1049502,
        "title": "MKS INSTRUMENTS INC"
    },
    "BZ": {
        "cik": 1842827,
        "title": "Kanzhun Ltd"
    },
    "RBC": {
        "cik": 1324948,
        "title": "RBC Bearings INC"
    },
    "FIX": {
        "cik": 1035983,
        "title": "COMFORT SYSTEMS USA INC"
    },
    "OPCH": {
        "cik": 1014739,
        "title": "Option Care Health, Inc."
    },
    "TNET": {
        "cik": 937098,
        "title": "TRINET GROUP, INC."
    },
    "NTRA": {
        "cik": 1604821,
        "title": "Natera, Inc."
    },
    "AMKR": {
        "cik": 1047127,
        "title": "AMKOR TECHNOLOGY, INC."
    },
    "WH": {
        "cik": 1722684,
        "title": "WYNDHAM HOTELS & RESORTS, INC."
    },
    "BILI": {
        "cik": 1723690,
        "title": "Bilibili Inc."
    },
    "IGT": {
        "cik": 1619762,
        "title": "International Game Technology PLC"
    },
    "FCN": {
        "cik": 887936,
        "title": "FTI CONSULTING, INC"
    },
    "EXP": {
        "cik": 918646,
        "title": "EAGLE MATERIALS INC"
    },
    "SAIC": {
        "cik": 1571123,
        "title": "Science Applications International Corp"
    },
    "STWD": {
        "cik": 1465128,
        "title": "STARWOOD PROPERTY TRUST, INC."
    },
    "CACC": {
        "cik": 885550,
        "title": "CREDIT ACCEPTANCE CORP"
    },
    "CBSH": {
        "cik": 22356,
        "title": "COMMERCE BANCSHARES INC /MO/"
    },
    "CMA": {
        "cik": 28412,
        "title": "COMERICA INC /NEW/"
    },
    "DSGX": {
        "cik": 1050140,
        "title": "DESCARTES SYSTEMS GROUP INC"
    },
    "UFPI": {
        "cik": 912767,
        "title": "UFP INDUSTRIES INC"
    },
    "AXTA": {
        "cik": 1616862,
        "title": "Axalta Coating Systems Ltd."
    },
    "CIEN": {
        "cik": 936395,
        "title": "CIENA CORP"
    },
    "FRSH": {
        "cik": 1544522,
        "title": "Freshworks Inc."
    },
    "RIG": {
        "cik": 1451505,
        "title": "Transocean Ltd."
    },
    "WF": {
        "cik": 1264136,
        "title": "WOORI FINANCIAL GROUP INC."
    },
    "CFR": {
        "cik": 39263,
        "title": "CULLEN/FROST BANKERS, INC."
    },
    "MHK": {
        "cik": 851968,
        "title": "MOHAWK INDUSTRIES INC"
    },
    "SIGI": {
        "cik": 230557,
        "title": "SELECTIVE INSURANCE GROUP INC"
    },
    "DOOO": {
        "cik": 1748797,
        "title": "BRP Inc."
    },
    "FAF": {
        "cik": 1472787,
        "title": "First American Financial Corp"
    },
    "WTS": {
        "cik": 795403,
        "title": "WATTS WATER TECHNOLOGIES INC"
    },
    "GLBE": {
        "cik": 1835963,
        "title": "Global-E Online Ltd."
    },
    "CPRI": {
        "cik": 1530721,
        "title": "Capri Holdings Ltd"
    },
    "WFRD": {
        "cik": 1603923,
        "title": "Weatherford International plc"
    },
    "IRDM": {
        "cik": 1418819,
        "title": "Iridium Communications Inc."
    },
    "CROX": {
        "cik": 1334036,
        "title": "Crocs, Inc."
    },
    "NFE": {
        "cik": 1749723,
        "title": "New Fortress Energy Inc."
    },
    "EGFEY": {
        "cik": 1437178,
        "title": "EFG Eurobank Ergasias S.A./ADR"
    },
    "HRB": {
        "cik": 12659,
        "title": "H&R BLOCK INC"
    },
    "KT": {
        "cik": 892450,
        "title": "KT CORP"
    },
    "PPC": {
        "cik": 802481,
        "title": "PILGRIMS PRIDE CORP"
    },
    "HXL": {
        "cik": 717605,
        "title": "HEXCEL CORP /DE/"
    },
    "HQY": {
        "cik": 1428336,
        "title": "HEALTHEQUITY, INC."
    },
    "ESTC": {
        "cik": 1707753,
        "title": "Elastic N.V."
    },
    "NEWR": {
        "cik": 1448056,
        "title": "NEW RELIC, INC."
    },
    "CIG": {
        "cik": 1157557,
        "title": "ENERGY CO OF MINAS GERAIS"
    },
    "PBF": {
        "cik": 1534504,
        "title": "PBF Energy Inc."
    },
    "PSN": {
        "cik": 275880,
        "title": "PARSONS CORP"
    },
    "RLI": {
        "cik": 84246,
        "title": "RLI CORP"
    },
    "PHYS": {
        "cik": 1477049,
        "title": "Sprott Physical Gold Trust"
    },
    "MGY": {
        "cik": 1698990,
        "title": "Magnolia Oil & Gas Corp"
    },
    "NXT": {
        "cik": 1852131,
        "title": "Nextracker Inc."
    },
    "KGC": {
        "cik": 701818,
        "title": "KINROSS GOLD CORP"
    },
    "MASI": {
        "cik": 937556,
        "title": "MASIMO CORP"
    },
    "RMBS": {
        "cik": 917273,
        "title": "RAMBUS INC"
    },
    "BC": {
        "cik": 14930,
        "title": "BRUNSWICK CORP"
    },
    "ADT": {
        "cik": 1703056,
        "title": "ADT Inc."
    },
    "ELAN": {
        "cik": 1739104,
        "title": "Elanco Animal Health Inc"
    },
    "REYN": {
        "cik": 1786431,
        "title": "Reynolds Consumer Products Inc."
    },
    "LU": {
        "cik": 1816007,
        "title": "Lufax Holding Ltd"
    },
    "NXST": {
        "cik": 1142417,
        "title": "NEXSTAR MEDIA GROUP, INC."
    },
    "ADC": {
        "cik": 917251,
        "title": "AGREE REALTY CORP"
    },
    "ST": {
        "cik": 1477294,
        "title": "Sensata Technologies Holding plc"
    },
    "AGNC": {
        "cik": 1423689,
        "title": "AGNC Investment Corp."
    },
    "AM": {
        "cik": 1623925,
        "title": "Antero Midstream Corp"
    },
    "OGN": {
        "cik": 1821825,
        "title": "Organon & Co."
    },
    "GMED": {
        "cik": 1237831,
        "title": "GLOBUS MEDICAL INC"
    },
    "THO": {
        "cik": 730263,
        "title": "THOR INDUSTRIES INC"
    },
    "JSCPY": {
        "cik": 1449005,
        "title": "JSR Corp."
    },
    "BZZUY": {
        "cik": 1437774,
        "title": "BUZZI UNICEM S.p.A."
    },
    "AIT": {
        "cik": 109563,
        "title": "APPLIED INDUSTRIAL TECHNOLOGIES INC"
    },
    "GME": {
        "cik": 1326380,
        "title": "GameStop Corp."
    },
    "IONS": {
        "cik": 874015,
        "title": "IONIS PHARMACEUTICALS INC"
    },
    "HALO": {
        "cik": 1159036,
        "title": "HALOZYME THERAPEUTICS, INC."
    },
    "PAAS": {
        "cik": 771992,
        "title": "PAN AMERICAN SILVER CORP"
    },
    "ATI": {
        "cik": 1018963,
        "title": "ATI INC"
    },
    "INFA": {
        "cik": 1868778,
        "title": "Informatica Inc."
    },
    "ENLC": {
        "cik": 1592000,
        "title": "EnLink Midstream, LLC"
    },
    "FSK": {
        "cik": 1422183,
        "title": "FS KKR Capital Corp"
    },
    "MSM": {
        "cik": 1003078,
        "title": "MSC INDUSTRIAL DIRECT CO INC"
    },
    "ONTO": {
        "cik": 704532,
        "title": "ONTO INNOVATION INC."
    },
    "LEVI": {
        "cik": 94845,
        "title": "LEVI STRAUSS & CO"
    },
    "POST": {
        "cik": 1530950,
        "title": "Post Holdings, Inc."
    },
    "ACLS": {
        "cik": 1113232,
        "title": "AXCELIS TECHNOLOGIES INC"
    },
    "DLO": {
        "cik": 1846832,
        "title": "dLocal Ltd"
    },
    "VAL": {
        "cik": 314808,
        "title": "Valaris Ltd"
    },
    "GBTG": {
        "cik": 1820872,
        "title": "Global Business Travel Group, Inc."
    },
    "DDS": {
        "cik": 28917,
        "title": "DILLARD'S, INC."
    },
    "DV": {
        "cik": 1819928,
        "title": "DoubleVerify Holdings, Inc."
    },
    "BKGFY": {
        "cik": 1447137,
        "title": "Berkeley Group Holdings plc"
    },
    "WOLF": {
        "cik": 895419,
        "title": "WOLFSPEED, INC."
    },
    "CRCBY": {
        "cik": 1553915,
        "title": "Chongqing Rural Commercial Bank Co., Ltd./ADR"
    },
    "ATKR": {
        "cik": 1666138,
        "title": "Atkore Inc."
    },
    "SON": {
        "cik": 91767,
        "title": "SONOCO PRODUCTS CO"
    },
    "BOKF": {
        "cik": 875357,
        "title": "BOK FINANCIAL CORP"
    },
    "TKR": {
        "cik": 98362,
        "title": "TIMKEN CO"
    },
    "ALK": {
        "cik": 766421,
        "title": "ALASKA AIR GROUP, INC."
    },
    "SIM": {
        "cik": 887153,
        "title": "GRUPO SIMEC, S.A.B. de C.V."
    },
    "ITCI": {
        "cik": 1567514,
        "title": "Intra-Cellular Therapies, Inc."
    },
    "ENSG": {
        "cik": 1125376,
        "title": "ENSIGN GROUP, INC"
    },
    "SSB": {
        "cik": 764038,
        "title": "SouthState Corp"
    },
    "QLYS": {
        "cik": 1107843,
        "title": "QUALYS, INC."
    },
    "HTZ": {
        "cik": 1657853,
        "title": "HERTZ GLOBAL HOLDINGS, INC"
    },
    "NVST": {
        "cik": 1757073,
        "title": "Envista Holdings Corp"
    },
    "BMBL": {
        "cik": 1830043,
        "title": "Bumble Inc."
    },
    "HCP": {
        "cik": 1720671,
        "title": "HashiCorp, Inc."
    },
    "NOVT": {
        "cik": 1076930,
        "title": "NOVANTA INC"
    },
    "BFAM": {
        "cik": 1437578,
        "title": "BRIGHT HORIZONS FAMILY SOLUTIONS INC."
    },
    "PB": {
        "cik": 1068851,
        "title": "PROSPERITY BANCSHARES INC"
    },
    "ESNT": {
        "cik": 1448893,
        "title": "Essent Group Ltd."
    },
    "TXG": {
        "cik": 1770787,
        "title": "10x Genomics, Inc."
    },
    "ADOOY": {
        "cik": 1489079,
        "title": "Adaro Energy PT/ADR/"
    },
    "PLUG": {
        "cik": 1093691,
        "title": "PLUG POWER INC"
    },
    "ALSN": {
        "cik": 1411207,
        "title": "Allison Transmission Holdings Inc"
    },
    "SMAR": {
        "cik": 1366561,
        "title": "SMARTSHEET INC"
    },
    "OBDC": {
        "cik": 1655888,
        "title": "Blue Owl Capital Corp"
    },
    "SRC": {
        "cik": 1308606,
        "title": "SPIRIT REALTY CAPITAL, INC."
    },
    "FRHC": {
        "cik": 924805,
        "title": "Freedom Holding Corp."
    },
    "GIL": {
        "cik": 1061894,
        "title": "Gildan Activewear Inc."
    },
    "WAL": {
        "cik": 1212545,
        "title": "WESTERN ALLIANCE BANCORPORATION"
    },
    "DUOL": {
        "cik": 1562088,
        "title": "Duolingo, Inc."
    },
    "BRBR": {
        "cik": 1772016,
        "title": "BELLRING BRANDS, INC."
    },
    "SNDR": {
        "cik": 1692063,
        "title": "Schneider National, Inc."
    },
    "WK": {
        "cik": 1445305,
        "title": "WORKIVA INC"
    },
    "VMI": {
        "cik": 102729,
        "title": "VALMONT INDUSTRIES INC"
    },
    "ASND": {
        "cik": 1612042,
        "title": "Ascendis Pharma A/S"
    },
    "HGTY": {
        "cik": 1840776,
        "title": "Hagerty, Inc."
    },
    "PLNT": {
        "cik": 1637207,
        "title": "Planet Fitness, Inc."
    },
    "TENB": {
        "cik": 1660280,
        "title": "Tenable Holdings, Inc."
    },
    "MTSI": {
        "cik": 1493594,
        "title": "MACOM Technology Solutions Holdings, Inc."
    },
    "PNFP": {
        "cik": 1115055,
        "title": "PINNACLE FINANCIAL PARTNERS INC"
    },
    "CIGI": {
        "cik": 913353,
        "title": "Colliers International Group Inc."
    },
    "PRGO": {
        "cik": 1585364,
        "title": "PERRIGO Co plc"
    },
    "EVR": {
        "cik": 1360901,
        "title": "Evercore Inc."
    },
    "ZION": {
        "cik": 109380,
        "title": "ZIONS BANCORPORATION, NATIONAL ASSOCIATION /UT/"
    },
    "ABCM": {
        "cik": 1492074,
        "title": "Abcam plc"
    },
    "BEPC": {
        "cik": 1791863,
        "title": "Brookfield Renewable Corp"
    },
    "PVH": {
        "cik": 78239,
        "title": "PVH CORP. /DE/"
    },
    "FIVN": {
        "cik": 1288847,
        "title": "Five9, Inc."
    },
    "AA": {
        "cik": 1675149,
        "title": "Alcoa Corp"
    },
    "LANC": {
        "cik": 57515,
        "title": "LANCASTER COLONY CORP"
    },
    "FLO": {
        "cik": 1128928,
        "title": "FLOWERS FOODS INC"
    },
    "QDEL": {
        "cik": 1906324,
        "title": "QuidelOrtho Corp"
    },
    "GOL": {
        "cik": 1291733,
        "title": "Gol Intelligent Airlines Inc."
    },
    "ZWS": {
        "cik": 1439288,
        "title": "Zurn Elkay Water Solutions Corp"
    },
    "DTM": {
        "cik": 1842022,
        "title": "DT Midstream, Inc."
    },
    "AYI": {
        "cik": 1144215,
        "title": "ACUITY BRANDS INC"
    },
    "BECN": {
        "cik": 1124941,
        "title": "BEACON ROOFING SUPPLY INC"
    },
    "IQ": {
        "cik": 1722608,
        "title": "iQIYI, Inc."
    },
    "NSIT": {
        "cik": 932696,
        "title": "INSIGHT ENTERPRISES INC"
    },
    "RHP": {
        "cik": 1040829,
        "title": "Ryman Hospitality Properties, Inc."
    },
    "WIX": {
        "cik": 1576789,
        "title": "Wix.com Ltd."
    },
    "COHR": {
        "cik": 820318,
        "title": "COHERENT CORP."
    },
    "FIZZ": {
        "cik": 69891,
        "title": "NATIONAL BEVERAGE CORP"
    },
    "CWAN": {
        "cik": 1866368,
        "title": "Clearwater Analytics Holdings, Inc."
    },
    "ALTR": {
        "cik": 1701732,
        "title": "Altair Engineering Inc."
    },
    "SEE": {
        "cik": 1012100,
        "title": "SEALED AIR CORP/DE"
    },
    "ALKS": {
        "cik": 1520262,
        "title": "Alkermes plc."
    },
    "FLS": {
        "cik": 30625,
        "title": "FLOWSERVE CORP"
    },
    "SLGN": {
        "cik": 849869,
        "title": "SILGAN HOLDINGS INC"
    },
    "AQN": {
        "cik": 1174169,
        "title": "ALGONQUIN POWER & UTILITIES CORP."
    },
    "HLNE": {
        "cik": 1433642,
        "title": "Hamilton Lane INC"
    },
    "NEOG": {
        "cik": 711377,
        "title": "NEOGEN CORP"
    },
    "TMHC": {
        "cik": 1562476,
        "title": "Taylor Morrison Home Corp"
    },
    "ACAD": {
        "cik": 1209191,
        "title": "ACADIA PHARMACEUTICALS INC"
    },
    "HUN": {
        "cik": 1307954,
        "title": "Huntsman CORP"
    },
    "MTG": {
        "cik": 876437,
        "title": "MGIC INVESTMENT CORP"
    },
    "AIRC": {
        "cik": 1820877,
        "title": "Apartment Income REIT Corp."
    },
    "NFG": {
        "cik": 70145,
        "title": "NATIONAL FUEL GAS CO"
    },
    "MMS": {
        "cik": 1032220,
        "title": "MAXIMUS, INC."
    },
    "MTH": {
        "cik": 833079,
        "title": "Meritage Homes CORP"
    },
    "SM": {
        "cik": 893538,
        "title": "SM Energy Co"
    },
    "CLVT": {
        "cik": 1764046,
        "title": "CLARIVATE Plc"
    },
    "S": {
        "cik": 1583708,
        "title": "SentinelOne, Inc."
    },
    "JOBY": {
        "cik": 1819848,
        "title": "Joby Aviation, Inc."
    },
    "AUR": {
        "cik": 1828108,
        "title": "Aurora Innovation, Inc."
    },
    "WING": {
        "cik": 1636222,
        "title": "Wingstop Inc."
    },
    "FLR": {
        "cik": 1124198,
        "title": "FLUOR CORP"
    },
    "KEX": {
        "cik": 56047,
        "title": "KIRBY CORP"
    },
    "CR": {
        "cik": 1944013,
        "title": "Crane Co"
    },
    "UGI": {
        "cik": 884614,
        "title": "UGI CORP /PA/"
    },
    "PAM": {
        "cik": 1469395,
        "title": "Pampa Energy Inc."
    },
    "OMF": {
        "cik": 1584207,
        "title": "OneMain Holdings, Inc."
    },
    "HOG": {
        "cik": 793952,
        "title": "HARLEY-DAVIDSON, INC."
    },
    "CAVA": {
        "cik": 1639438,
        "title": "CAVA GROUP, INC."
    },
    "HGV": {
        "cik": 1674168,
        "title": "Hilton Grand Vacations Inc."
    },
    "AMG": {
        "cik": 1004434,
        "title": "AFFILIATED MANAGERS GROUP, INC."
    },
    "CWEN": {
        "cik": 1567683,
        "title": "Clearway Energy, Inc."
    },
    "KRG": {
        "cik": 1286043,
        "title": "KITE REALTY GROUP TRUST"
    },
    "CC": {
        "cik": 1627223,
        "title": "Chemours Co"
    },
    "OMAB": {
        "cik": 1378239,
        "title": "Central North Airport Group"
    },
    "TRNO": {
        "cik": 1476150,
        "title": "Terreno Realty Corp"
    },
    "CWST": {
        "cik": 911177,
        "title": "CASELLA WASTE SYSTEMS INC"
    },
    "BPOP": {
        "cik": 763901,
        "title": "POPULAR, INC."
    },
    "WTFC": {
        "cik": 1015328,
        "title": "WINTRUST FINANCIAL CORP"
    },
    "ABG": {
        "cik": 1144980,
        "title": "ASBURY AUTOMOTIVE GROUP INC"
    },
    "IAC": {
        "cik": 1800227,
        "title": "IAC Inc."
    },
    "BMI": {
        "cik": 9092,
        "title": "BADGER METER INC"
    },
    "IDA": {
        "cik": 1057877,
        "title": "IDACORP INC"
    },
    "PDI": {
        "cik": 1510599,
        "title": "PIMCO Dynamic Income Fund"
    },
    "POWI": {
        "cik": 833640,
        "title": "POWER INTEGRATIONS INC"
    },
    "MSTR": {
        "cik": 1050446,
        "title": "MICROSTRATEGY Inc"
    },
    "AZEK": {
        "cik": 1782754,
        "title": "AZEK Co Inc."
    },
    "IPGP": {
        "cik": 1111928,
        "title": "IPG PHOTONICS CORP"
    },
    "PCVX": {
        "cik": 1649094,
        "title": "Vaxcyte, Inc."
    },
    "BBIO": {
        "cik": 1743881,
        "title": "BridgeBio Pharma, Inc."
    },
    "VVV": {
        "cik": 1674910,
        "title": "VALVOLINE INC"
    },
    "PHI": {
        "cik": 78150,
        "title": "PLDT Inc."
    },
    "DNB": {
        "cik": 1799208,
        "title": "Dun & Bradstreet Holdings, Inc."
    },
    "AXS": {
        "cik": 1214816,
        "title": "AXIS CAPITAL HOLDINGS LTD"
    },
    "SHC": {
        "cik": 1822479,
        "title": "Sotera Health Co"
    },
    "RITM": {
        "cik": 1556593,
        "title": "Rithm Capital Corp."
    },
    "LNTH": {
        "cik": 1521036,
        "title": "Lantheus Holdings, Inc."
    },
    "NSA": {
        "cik": 1618563,
        "title": "National Storage Affiliates Trust"
    },
    "COLM": {
        "cik": 1050797,
        "title": "COLUMBIA SPORTSWEAR CO"
    },
    "ACT": {
        "cik": 1823529,
        "title": "Enact Holdings, Inc."
    },
    "MSSMY": {
        "cik": 1710864,
        "title": "Misumi Group Inc./ADR"
    },
    "NGKSY": {
        "cik": 1442655,
        "title": "NGK Spark Plug Co., Ltd."
    },
    "ESI": {
        "cik": 1590714,
        "title": "Element Solutions Inc"
    },
    "VNT": {
        "cik": 1786842,
        "title": "Vontier Corp"
    },
    "TRTN": {
        "cik": 1660734,
        "title": "Triton International Ltd"
    },
    "TKC": {
        "cik": 1071321,
        "title": "TURKCELL ILETISIM HIZMETLERI A S"
    },
    "RYN": {
        "cik": 52827,
        "title": "RAYONIER INC"
    },
    "OLLI": {
        "cik": 1639300,
        "title": "Ollie's Bargain Outlet Holdings, Inc."
    },
    "VNOM": {
        "cik": 1602065,
        "title": "Viper Energy Partners LP"
    },
    "ONB": {
        "cik": 707179,
        "title": "OLD NATIONAL BANCORP /IN/"
    },
    "EXPO": {
        "cik": 851520,
        "title": "EXPONENT INC"
    },
    "SAM": {
        "cik": 949870,
        "title": "BOSTON BEER CO INC"
    },
    "SWX": {
        "cik": 1692115,
        "title": "Southwest Gas Holdings, Inc."
    },
    "CPG": {
        "cik": 1545851,
        "title": "Crescent Point Energy Corp."
    },
    "VLY": {
        "cik": 714310,
        "title": "VALLEY NATIONAL BANCORP"
    },
    "HOMB": {
        "cik": 1331520,
        "title": "HOME BANCSHARES INC"
    },
    "FOUR": {
        "cik": 1794669,
        "title": "Shift4 Payments, Inc."
    },
    "DEN": {
        "cik": 945764,
        "title": "DENBURY INC"
    },
    "DOCS": {
        "cik": 1516513,
        "title": "Doximity, Inc."
    },
    "ORA": {
        "cik": 1296445,
        "title": "ORMAT TECHNOLOGIES, INC."
    },
    "AGI": {
        "cik": 1178819,
        "title": "ALAMOS GOLD INC"
    },
    "R": {
        "cik": 85961,
        "title": "RYDER SYSTEM INC"
    },
    "ASH": {
        "cik": 1674862,
        "title": "ASHLAND INC."
    },
    "BXSL": {
        "cik": 1736035,
        "title": "Blackstone Secured Lending Fund"
    },
    "EBCOY": {
        "cik": 354518,
        "title": "EBARA CORP /ADR/"
    },
    "SNV": {
        "cik": 18349,
        "title": "SYNOVUS FINANCIAL CORP"
    },
    "TDC": {
        "cik": 816761,
        "title": "TERADATA CORP /DE/"
    },
    "OZK": {
        "cik": 1569650,
        "title": "Bank OZK"
    },
    "AVT": {
        "cik": 8858,
        "title": "AVNET INC"
    },
    "NEU": {
        "cik": 1282637,
        "title": "NEWMARKET CORP"
    },
    "ENIC": {
        "cik": 1659939,
        "title": "Enel Chile S.A."
    },
    "SLAB": {
        "cik": 1038074,
        "title": "SILICON LABORATORIES INC."
    },
    "ASAN": {
        "cik": 1477720,
        "title": "Asana, Inc."
    },
    "GH": {
        "cik": 1576280,
        "title": "Guardant Health, Inc."
    },
    "SBSW": {
        "cik": 1786909,
        "title": "Sibanye Stillwater Ltd"
    },
    "FOXF": {
        "cik": 1424929,
        "title": "FOX FACTORY HOLDING CORP"
    },
    "AL": {
        "cik": 1487712,
        "title": "AIR LEASE CORP"
    },
    "PECO": {
        "cik": 1476204,
        "title": "Phillips Edison & Company, Inc."
    },
    "SYNH": {
        "cik": 1610950,
        "title": "Syneos Health, Inc."
    },
    "BOX": {
        "cik": 1372612,
        "title": "BOX INC"
    },
    "BCPC": {
        "cik": 9326,
        "title": "BALCHEM CORP"
    },
    "GGAL": {
        "cik": 1114700,
        "title": "GRUPO FINANCIERO GALICIA SA"
    },
    "WU": {
        "cik": 1365135,
        "title": "Western Union CO"
    },
    "FELE": {
        "cik": 38725,
        "title": "FRANKLIN ELECTRIC CO INC"
    },
    "NTCO": {
        "cik": 1776967,
        "title": "Natura &Co Holding S.A."
    },
    "LNC": {
        "cik": 59558,
        "title": "LINCOLN NATIONAL CORP"
    },
    "WEN": {
        "cik": 30697,
        "title": "Wendy's Co"
    },
    "PWSC": {
        "cik": 1835681,
        "title": "POWERSCHOOL HOLDINGS, INC."
    },
    "AFRM": {
        "cik": 1820953,
        "title": "Affirm Holdings, Inc."
    },
    "CRUS": {
        "cik": 772406,
        "title": "CIRRUS LOGIC, INC."
    },
    "DRS": {
        "cik": 1833756,
        "title": "Leonardo DRS, Inc."
    },
    "VNO": {
        "cik": 899689,
        "title": "VORNADO REALTY TRUST"
    },
    "HAE": {
        "cik": 313143,
        "title": "HAEMONETICS CORP"
    },
    "JHG": {
        "cik": 1274173,
        "title": "JANUS HENDERSON GROUP PLC"
    },
    "RELY": {
        "cik": 1782170,
        "title": "Remitly Global, Inc."
    },
    "BIPC": {
        "cik": 1788348,
        "title": "Brookfield Infrastructure Corp"
    },
    "ALIT": {
        "cik": 1809104,
        "title": "Alight, Inc. / Delaware"
    },
    "SUM": {
        "cik": 1621563,
        "title": "Summit Materials, Inc."
    },
    "ASO": {
        "cik": 1817358,
        "title": "Academy Sports & Outdoors, Inc."
    },
    "VIAAY": {
        "cik": 932417,
        "title": "VIENNA INTERNATIONAL AIRPORT"
    },
    "DXC": {
        "cik": 1688568,
        "title": "DXC Technology Co"
    },
    "FN": {
        "cik": 1408710,
        "title": "Fabrinet"
    },
    "AEIS": {
        "cik": 927003,
        "title": "ADVANCED ENERGY INDUSTRIES INC"
    },
    "SGRY": {
        "cik": 1638833,
        "title": "Surgery Partners, Inc."
    },
    "MLI": {
        "cik": 89439,
        "title": "MUELLER INDUSTRIES INC"
    },
    "MLCO": {
        "cik": 1381640,
        "title": "Melco Resorts & Entertainment LTD"
    },
    "POR": {
        "cik": 784977,
        "title": "PORTLAND GENERAL ELECTRIC CO /OR/"
    },
    "LPX": {
        "cik": 60519,
        "title": "LOUISIANA-PACIFIC CORP"
    },
    "MSGS": {
        "cik": 1636519,
        "title": "Madison Square Garden Sports Corp."
    },
    "GATX": {
        "cik": 40211,
        "title": "GATX CORP"
    },
    "LYFT": {
        "cik": 1759509,
        "title": "Lyft, Inc."
    },
    "NWL": {
        "cik": 814453,
        "title": "NEWELL BRANDS INC."
    },
    "HP": {
        "cik": 46765,
        "title": "Helmerich & Payne, Inc."
    },
    "ETRN": {
        "cik": 1747009,
        "title": "Equitrans Midstream Corp"
    },
    "CADE": {
        "cik": 1299939,
        "title": "Cadence Bank"
    },
    "MXCHY": {
        "cik": 1435969,
        "title": "Orbia Advance Corporation, S.A.B. de C.V./ADR"
    },
    "NEP": {
        "cik": 1603145,
        "title": "NEXTERA ENERGY PARTNERS, LP"
    },
    "FNB": {
        "cik": 37808,
        "title": "FNB CORP/PA/"
    },
    "TAL": {
        "cik": 1499620,
        "title": "TAL Education Group"
    },
    "BCC": {
        "cik": 1328581,
        "title": "BOISE CASCADE Co"
    },
    "IPAR": {
        "cik": 822663,
        "title": "INTER PARFUMS INC"
    },
    "EEFT": {
        "cik": 1029199,
        "title": "EURONET WORLDWIDE, INC."
    },
    "SVV": {
        "cik": 1883313,
        "title": "Savers Value Village, Inc."
    },
    "FFIN": {
        "cik": 36029,
        "title": "FIRST FINANCIAL BANKSHARES INC"
    },
    "ESAB": {
        "cik": 1877322,
        "title": "ESAB Corp"
    },
    "NJR": {
        "cik": 356309,
        "title": "NEW JERSEY RESOURCES CORP"
    },
    "NCR": {
        "cik": 70866,
        "title": "NCR CORP"
    },
    "IMGN": {
        "cik": 855654,
        "title": "ImmunoGen, Inc."
    },
    "IHCPF": {
        "cik": 1508633,
        "title": "Inchcape plc/ADR"
    },
    "SEB": {
        "cik": 88121,
        "title": "SEABOARD CORP /DE/"
    },
    "RDN": {
        "cik": 890926,
        "title": "RADIAN GROUP INC"
    },
    "AEL": {
        "cik": 1039828,
        "title": "AMERICAN EQUITY INVESTMENT LIFE HOLDING CO"
    },
    "BMA": {
        "cik": 1347426,
        "title": "Macro Bank Inc."
    },
    "SQSP": {
        "cik": 1496963,
        "title": "Squarespace, Inc."
    },
    "OGS": {
        "cik": 1587732,
        "title": "ONE Gas, Inc."
    },
    "FCFS": {
        "cik": 840489,
        "title": "FirstCash Holdings, Inc."
    },
    "ENS": {
        "cik": 1289308,
        "title": "EnerSys"
    },
    "MDU": {
        "cik": 67716,
        "title": "MDU RESOURCES GROUP INC"
    },
    "KRC": {
        "cik": 1025996,
        "title": "KILROY REALTY CORP"
    },
    "BRZE": {
        "cik": 1676238,
        "title": "Braze, Inc."
    },
    "MPW": {
        "cik": 1287865,
        "title": "MEDICAL PROPERTIES TRUST INC"
    },
    "IBP": {
        "cik": 1580905,
        "title": "Installed Building Products, Inc."
    },
    "UBSI": {
        "cik": 729986,
        "title": "UNITED BANKSHARES INC/WV"
    },
    "AAP": {
        "cik": 1158449,
        "title": "ADVANCE AUTO PARTS INC"
    },
    "M": {
        "cik": 794367,
        "title": "Macy's, Inc."
    },
    "COLB": {
        "cik": 887343,
        "title": "COLUMBIA BANKING SYSTEM, INC."
    },
    "PYCR": {
        "cik": 1839439,
        "title": "PAYCOR HCM, INC."
    },
    "WTM": {
        "cik": 776867,
        "title": "WHITE MOUNTAINS INSURANCE GROUP LTD"
    },
    "SRCL": {
        "cik": 861878,
        "title": "STERICYCLE INC"
    },
    "SFM": {
        "cik": 1575515,
        "title": "Sprouts Farmers Market, Inc."
    },
    "FRO": {
        "cik": 913290,
        "title": "Frontline plc"
    },
    "SLFPY": {
        "cik": 1370418,
        "title": "STANDARD LIFE PLC"
    },
    "YETI": {
        "cik": 1670592,
        "title": "YETI Holdings, Inc."
    },
    "UGP": {
        "cik": 1094972,
        "title": "ULTRAPAR HOLDINGS INC"
    },
    "FLNC": {
        "cik": 1868941,
        "title": "Fluence Energy, Inc."
    },
    "VAC": {
        "cik": 1524358,
        "title": "MARRIOTT VACATIONS WORLDWIDE Corp"
    },
    "ATS": {
        "cik": 1394832,
        "title": "ATS Corp /ATS"
    },
    "ESGR": {
        "cik": 1363829,
        "title": "Enstar Group LTD"
    },
    "BTG": {
        "cik": 1429937,
        "title": "B2GOLD CORP"
    },
    "CRC": {
        "cik": 1609253,
        "title": "California Resources Corp"
    },
    "ASGN": {
        "cik": 890564,
        "title": "ASGN Inc"
    },
    "ASMVY": {
        "cik": 1447945,
        "title": "ASM Pacific Technology Ltd."
    },
    "BLKB": {
        "cik": 1280058,
        "title": "BLACKBAUD INC"
    },
    "LTHM": {
        "cik": 1742924,
        "title": "Livent Corp."
    },
    "VC": {
        "cik": 1111335,
        "title": "VISTEON CORP"
    },
    "SDRL": {
        "cik": 1737706,
        "title": "Seadrill Ltd"
    },
    "MAN": {
        "cik": 871763,
        "title": "ManpowerGroup Inc."
    },
    "MMSI": {
        "cik": 856982,
        "title": "MERIT MEDICAL SYSTEMS INC"
    },
    "KBH": {
        "cik": 795266,
        "title": "KB HOME"
    },
    "TFSL": {
        "cik": 1381668,
        "title": "TFS Financial CORP"
    },
    "CBT": {
        "cik": 16040,
        "title": "CABOT CORP"
    },
    "GOLF": {
        "cik": 1672013,
        "title": "Acushnet Holdings Corp."
    },
    "PSLV": {
        "cik": 1494728,
        "title": "Sprott Physical Silver Trust"
    },
    "CEF": {
        "cik": 1726122,
        "title": "Sprott Physical Gold & Silver Trust"
    },
    "EVO": {
        "cik": 1412558,
        "title": "Evotec SE"
    },
    "MMYT": {
        "cik": 1495153,
        "title": "MakeMyTrip Ltd"
    },
    "PNM": {
        "cik": 1108426,
        "title": "PNM RESOURCES INC"
    },
    "COOP": {
        "cik": 933136,
        "title": "Mr. Cooper Group Inc."
    },
    "NOG": {
        "cik": 1104485,
        "title": "NORTHERN OIL & GAS, INC."
    },
    "PEGA": {
        "cik": 1013857,
        "title": "PEGASYSTEMS INC"
    },
    "CXM": {
        "cik": 1569345,
        "title": "Sprinklr, Inc."
    },
    "CNXC": {
        "cik": 1803599,
        "title": "Concentrix Corp"
    },
    "PAGP": {
        "cik": 1581990,
        "title": "PLAINS GP HOLDINGS LP"
    },
    "NSP": {
        "cik": 1000753,
        "title": "INSPERITY, INC."
    },
    "STR": {
        "cik": 1949543,
        "title": "Sitio Royalties Corp."
    },
    "THG": {
        "cik": 944695,
        "title": "HANOVER INSURANCE GROUP, INC."
    },
    "CPA": {
        "cik": 1345105,
        "title": "Copa Holdings, S.A."
    },
    "FYBR": {
        "cik": 20520,
        "title": "Frontier Communications Parent, Inc."
    },
    "STNE": {
        "cik": 1745431,
        "title": "StoneCo Ltd."
    },
    "TGS": {
        "cik": 931427,
        "title": "GAS TRANSPORTER OF THE SOUTH INC"
    },
    "CRSP": {
        "cik": 1674416,
        "title": "CRISPR Therapeutics AG"
    },
    "CRVL": {
        "cik": 874866,
        "title": "CORVEL CORP"
    },
    "TEX": {
        "cik": 97216,
        "title": "TEREX CORP"
    },
    "ZGN": {
        "cik": 1877787,
        "title": "Ermenegildo Zegna N.V."
    },
    "GPS": {
        "cik": 39911,
        "title": "GAP INC"
    },
    "FRPT": {
        "cik": 1611647,
        "title": "Freshpet, Inc."
    },
    "TDOC": {
        "cik": 1477449,
        "title": "Teladoc Health, Inc."
    },
    "SUN": {
        "cik": 1552275,
        "title": "Sunoco LP"
    },
    "DFIHY": {
        "cik": 871459,
        "title": "DAIRY FARM INTERNATIONAL HOLDINGS LTD /FI"
    },
    "CABO": {
        "cik": 1632127,
        "title": "Cable One, Inc."
    },
    "DIOD": {
        "cik": 29002,
        "title": "DIODES INC /DEL/"
    },
    "NARI": {
        "cik": 1531048,
        "title": "Inari Medical, Inc."
    },
    "SGML": {
        "cik": 1848309,
        "title": "Sigma Lithium Corp"
    },
    "PCH": {
        "cik": 1338749,
        "title": "POTLATCHDELTIC CORP"
    },
    "FUL": {
        "cik": 39368,
        "title": "FULLER H B CO"
    },
    "EURN": {
        "cik": 1604481,
        "title": "Euronav NV"
    },
    "VSH": {
        "cik": 103730,
        "title": "VISHAY INTERTECHNOLOGY INC"
    },
    "GOCO": {
        "cik": 1808220,
        "title": "GoHealth, Inc."
    },
    "AI": {
        "cik": 1577526,
        "title": "C3.ai, Inc."
    },
    "GPI": {
        "cik": 1031203,
        "title": "GROUP 1 AUTOMOTIVE INC"
    },
    "BAK": {
        "cik": 1071438,
        "title": "BRASKEM SA"
    },
    "APLS": {
        "cik": 1492422,
        "title": "Apellis Pharmaceuticals, Inc."
    },
    "INST": {
        "cik": 1841804,
        "title": "INSTRUCTURE HOLDINGS, INC."
    },
    "FOLD": {
        "cik": 1178879,
        "title": "AMICUS THERAPEUTICS, INC."
    },
    "LEG": {
        "cik": 58492,
        "title": "LEGGETT & PLATT INC"
    },
    "IRT": {
        "cik": 1466085,
        "title": "INDEPENDENCE REALTY TRUST, INC."
    },
    "ACA": {
        "cik": 1739445,
        "title": "Arcosa, Inc."
    },
    "MOG-A": {
        "cik": 67887,
        "title": "MOOG INC."
    },
    "FSS": {
        "cik": 277509,
        "title": "FEDERAL SIGNAL CORP /DE/"
    },
    "CNX": {
        "cik": 1070412,
        "title": "CNX Resources Corp"
    },
    "BKH": {
        "cik": 1130464,
        "title": "BLACK HILLS CORP /SD/"
    },
    "MP": {
        "cik": 1801368,
        "title": "MP Materials Corp. / DE"
    },
    "ATHM": {
        "cik": 1527636,
        "title": "Autohome Inc."
    },
    "AZTA": {
        "cik": 933974,
        "title": "Azenta, Inc."
    },
    "SEM": {
        "cik": 1320414,
        "title": "SELECT MEDICAL HOLDINGS CORP"
    },
    "BDC": {
        "cik": 913142,
        "title": "BELDEN INC."
    },
    "SKY": {
        "cik": 90896,
        "title": "Skyline Champion Corp"
    },
    "KD": {
        "cik": 1867072,
        "title": "Kyndryl Holdings, Inc."
    },
    "HRI": {
        "cik": 1364479,
        "title": "HERC HOLDINGS INC"
    },
    "ERF": {
        "cik": 1126874,
        "title": "ENERPLUS Corp"
    },
    "GT": {
        "cik": 42582,
        "title": "GOODYEAR TIRE & RUBBER CO /OH/"
    },
    "MANU": {
        "cik": 1549107,
        "title": "Manchester United plc"
    },
    "EXTR": {
        "cik": 1078271,
        "title": "EXTREME NETWORKS INC"
    },
    "ASAI": {
        "cik": 1834048,
        "title": "Sendas Distributor S.A."
    },
    "BSM": {
        "cik": 1621434,
        "title": "Black Stone Minerals, L.P."
    },
    "ADNT": {
        "cik": 1670541,
        "title": "Adient plc"
    },
    "SPXC": {
        "cik": 88205,
        "title": "SPX Technologies, Inc."
    },
    "DNP": {
        "cik": 806628,
        "title": "DNP SELECT INCOME FUND INC"
    },
    "FG": {
        "cik": 1934850,
        "title": "F&G Annuities & Life, Inc."
    },
    "LPL": {
        "cik": 1290109,
        "title": "LG Display Co., Ltd."
    },
    "AMN": {
        "cik": 1142750,
        "title": "AMN HEALTHCARE SERVICES INC"
    },
    "BXMT": {
        "cik": 1061630,
        "title": "BLACKSTONE MORTGAGE TRUST, INC."
    },
    "TSEM": {
        "cik": 928876,
        "title": "TOWER SEMICONDUCTOR LTD"
    },
    "GKOS": {
        "cik": 1192448,
        "title": "GLAUKOS Corp"
    },
    "PGNY": {
        "cik": 1551306,
        "title": "Progyny, Inc."
    },
    "SYNA": {
        "cik": 817720,
        "title": "SYNAPTICS Inc"
    },
    "EPRT": {
        "cik": 1728951,
        "title": "ESSENTIAL PROPERTIES REALTY TRUST, INC."
    },
    "WOR": {
        "cik": 108516,
        "title": "WORTHINGTON INDUSTRIES INC"
    },
    "AB": {
        "cik": 825313,
        "title": "ALLIANCEBERNSTEIN HOLDING L.P."
    },
    "PLTK": {
        "cik": 1828016,
        "title": "Playtika Holding Corp."
    },
    "FTAI": {
        "cik": 1590364,
        "title": "FTAI Aviation Ltd."
    },
    "PENN": {
        "cik": 921738,
        "title": "PENN Entertainment, Inc."
    },
    "HWC": {
        "cik": 750577,
        "title": "HANCOCK WHITNEY CORP"
    },
    "RUSHA": {
        "cik": 1012019,
        "title": "RUSH ENTERPRISES INC TX"
    },
    "FLYW": {
        "cik": 1580560,
        "title": "Flywire Corp"
    },
    "LOPE": {
        "cik": 1434588,
        "title": "Grand Canyon Education, Inc."
    },
    "SLM": {
        "cik": 1032033,
        "title": "SLM Corp"
    },
    "CVI": {
        "cik": 1376139,
        "title": "CVR ENERGY INC"
    },
    "FOCS": {
        "cik": 1651052,
        "title": "Focus Financial Partners Inc."
    },
    "IART": {
        "cik": 917520,
        "title": "INTEGRA LIFESCIENCES HOLDINGS CORP"
    },
    "DNA": {
        "cik": 1830214,
        "title": "Ginkgo Bioworks Holdings, Inc."
    },
    "AGO": {
        "cik": 1273813,
        "title": "ASSURED GUARANTY LTD"
    },
    "NVMI": {
        "cik": 1109345,
        "title": "NOVA LTD."
    },
    "JBT": {
        "cik": 1433660,
        "title": "John Bean Technologies CORP"
    },
    "CERE": {
        "cik": 1805387,
        "title": "Cerevel Therapeutics Holdings, Inc."
    },
    "OTTR": {
        "cik": 1466593,
        "title": "Otter Tail Corp"
    },
    "SMPL": {
        "cik": 1702744,
        "title": "Simply Good Foods Co"
    },
    "JOE": {
        "cik": 745308,
        "title": "ST JOE Co"
    },
    "SRAD": {
        "cik": 1836470,
        "title": "Sportradar Group AG"
    },
    "GRP-UN": {
        "cik": 1564538,
        "title": "GRANITE REAL ESTATE INVESTMENT TRUST"
    },
    "NNI": {
        "cik": 1258602,
        "title": "NELNET INC"
    },
    "PFSI": {
        "cik": 1745916,
        "title": "PennyMac Financial Services, Inc."
    },
    "BTE": {
        "cik": 1279495,
        "title": "BAYTEX ENERGY CORP."
    },
    "YOU": {
        "cik": 1856314,
        "title": "Clear Secure, Inc."
    },
    "USM": {
        "cik": 821130,
        "title": "UNITED STATES CELLULAR CORP"
    },
    "BCO": {
        "cik": 78890,
        "title": "BRINKS CO"
    },
    "VSAT": {
        "cik": 797721,
        "title": "VIASAT INC"
    },
    "DISH": {
        "cik": 1001082,
        "title": "DISH Network CORP"
    },
    "GEF": {
        "cik": 43920,
        "title": "GREIF, INC"
    },
    "BRFS": {
        "cik": 1122491,
        "title": "BRF S.A."
    },
    "GBCI": {
        "cik": 868671,
        "title": "GLACIER BANCORP, INC."
    },
    "NTLA": {
        "cik": 1652130,
        "title": "Intellia Therapeutics, Inc."
    },
    "CCOI": {
        "cik": 1158324,
        "title": "COGENT COMMUNICATIONS HOLDINGS, INC."
    },
    "KOS": {
        "cik": 1509991,
        "title": "Kosmos Energy Ltd."
    },
    "APPN": {
        "cik": 1441683,
        "title": "APPIAN CORP"
    },
    "CXT": {
        "cik": 25445,
        "title": "Crane NXT, Co."
    },
    "AAON": {
        "cik": 824142,
        "title": "AAON, INC."
    },
    "MDC": {
        "cik": 773141,
        "title": "M.D.C. HOLDINGS, INC."
    },
    "DOC": {
        "cik": 1574540,
        "title": "Physicians Realty Trust"
    },
    "AXSM": {
        "cik": 1579428,
        "title": "Axsome Therapeutics, Inc."
    },
    "MDGL": {
        "cik": 1157601,
        "title": "MADRIGAL PHARMACEUTICALS, INC."
    },
    "CRK": {
        "cik": 23194,
        "title": "COMSTOCK RESOURCES INC"
    },
    "AVNT": {
        "cik": 1122976,
        "title": "AVIENT CORP"
    },
    "LITE": {
        "cik": 1633978,
        "title": "Lumentum Holdings Inc."
    },
    "GTES": {
        "cik": 1718512,
        "title": "Gates Industrial Corp plc"
    },
    "APLE": {
        "cik": 1418121,
        "title": "Apple Hospitality REIT, Inc."
    },
    "SIG": {
        "cik": 832988,
        "title": "SIGNET JEWELERS LTD"
    },
    "CUZ": {
        "cik": 25232,
        "title": "COUSINS PROPERTIES INC"
    },
    "IRTC": {
        "cik": 1388658,
        "title": "iRhythm Technologies, Inc."
    },
    "VERX": {
        "cik": 1806837,
        "title": "Vertex, Inc."
    },
    "AWI": {
        "cik": 7431,
        "title": "ARMSTRONG WORLD INDUSTRIES INC"
    },
    "NVCR": {
        "cik": 1645113,
        "title": "NovoCure Ltd"
    },
    "VTSCY": {
        "cik": 1880866,
        "title": "Vitesco Technologies Group AG /ADR"
    },
    "URBN": {
        "cik": 912615,
        "title": "URBAN OUTFITTERS INC"
    },
    "WHD": {
        "cik": 1699136,
        "title": "Cactus, Inc."
    },
    "TGNA": {
        "cik": 39899,
        "title": "TEGNA INC"
    },
    "SHLS": {
        "cik": 1831651,
        "title": "Shoals Technologies Group, Inc."
    },
    "SPB": {
        "cik": 109177,
        "title": "Spectrum Brands Holdings, Inc."
    },
    "VRNS": {
        "cik": 1361113,
        "title": "VARONIS SYSTEMS INC"
    },
    "EPR": {
        "cik": 1045450,
        "title": "EPR PROPERTIES"
    },
    "LTH": {
        "cik": 1869198,
        "title": "Life Time Group Holdings, Inc."
    },
    "PDCO": {
        "cik": 891024,
        "title": "PATTERSON COMPANIES, INC."
    },
    "NCNO": {
        "cik": 1902733,
        "title": "nCino, Inc."
    },
    "INDV": {
        "cik": 1625297,
        "title": "INDIVIOR PLC"
    },
    "CNMD": {
        "cik": 816956,
        "title": "CONMED Corp"
    },
    "UCBI": {
        "cik": 857855,
        "title": "UNITED COMMUNITY BANKS INC"
    },
    "MAIN": {
        "cik": 1396440,
        "title": "Main Street Capital CORP"
    },
    "DNLI": {
        "cik": 1714899,
        "title": "Denali Therapeutics Inc."
    },
    "KRYS": {
        "cik": 1711279,
        "title": "Krystal Biotech, Inc."
    },
    "GO": {
        "cik": 1771515,
        "title": "Grocery Outlet Holding Corp."
    },
    "CORT": {
        "cik": 1088856,
        "title": "CORCEPT THERAPEUTICS INC"
    },
    "NOMD": {
        "cik": 1651717,
        "title": "Nomad Foods Ltd"
    },
    "UAA": {
        "cik": 1336917,
        "title": "Under Armour, Inc."
    },
    "ICUI": {
        "cik": 883984,
        "title": "ICU MEDICAL INC/DE"
    },
    "SR": {
        "cik": 1126956,
        "title": "SPIRE INC"
    },
    "BTU": {
        "cik": 1064728,
        "title": "PEABODY ENERGY CORP"
    },
    "SID": {
        "cik": 1049659,
        "title": "NATIONAL STEEL CO"
    },
    "RVMD": {
        "cik": 1628171,
        "title": "Revolution Medicines, Inc."
    },
    "UNF": {
        "cik": 717954,
        "title": "UNIFIRST CORP"
    },
    "BANF": {
        "cik": 760498,
        "title": "BANCFIRST CORP /OK/"
    },
    "AMTD": {
        "cik": 1769731,
        "title": "AMTD IDEA GROUP"
    },
    "STEP": {
        "cik": 1796022,
        "title": "StepStone Group Inc."
    },
    "ALE": {
        "cik": 66756,
        "title": "ALLETE INC"
    },
    "BBMPY": {
        "cik": 1553920,
        "title": "BBMG Corporation/ADR"
    },
    "CYTK": {
        "cik": 1061983,
        "title": "CYTOKINETICS INC"
    },
    "BHF": {
        "cik": 1685040,
        "title": "Brighthouse Financial, Inc."
    },
    "MATX": {
        "cik": 3453,
        "title": "Matson, Inc."
    },
    "AWR": {
        "cik": 1056903,
        "title": "AMERICAN STATES WATER CO"
    },
    "UMBF": {
        "cik": 101382,
        "title": "UMB FINANCIAL CORP"
    },
    "ZD": {
        "cik": 1084048,
        "title": "ZIFF DAVIS, INC."
    },
    "AEO": {
        "cik": 919012,
        "title": "AMERICAN EAGLE OUTFITTERS INC"
    },
    "SFBS": {
        "cik": 1430723,
        "title": "ServisFirst Bancshares, Inc."
    },
    "SANM": {
        "cik": 897723,
        "title": "SANMINA CORP"
    },
    "KSS": {
        "cik": 885639,
        "title": "KOHLS Corp"
    },
    "SEAS": {
        "cik": 1564902,
        "title": "SeaWorld Entertainment, Inc."
    },
    "BL": {
        "cik": 1666134,
        "title": "BLACKLINE, INC."
    },
    "LCII": {
        "cik": 763744,
        "title": "LCI INDUSTRIES"
    },
    "MQ": {
        "cik": 1522540,
        "title": "Marqeta, Inc."
    },
    "HI": {
        "cik": 1417398,
        "title": "Hillenbrand, Inc."
    },
    "JJSF": {
        "cik": 785956,
        "title": "J&J SNACK FOODS CORP"
    },
    "GNNDY": {
        "cik": 1380366,
        "title": "GN STORE NORD A/S"
    },
    "BNL": {
        "cik": 1424182,
        "title": "Broadstone Net Lease, Inc."
    },
    "INMD": {
        "cik": 1742692,
        "title": "InMode Ltd."
    },
    "NEA": {
        "cik": 1195737,
        "title": "Nuveen AMT-Free Quality Municipal Income Fund"
    },
    "IIJIY": {
        "cik": 1090633,
        "title": "INTERNET INITIATIVE JAPAN INC"
    },
    "VSBC": {
        "cik": 1697884,
        "title": "VITASPRING BIOMEDICAL CO. LTD."
    },
    "VIRT": {
        "cik": 1592386,
        "title": "Virtu Financial, Inc."
    },
    "TDW": {
        "cik": 98222,
        "title": "TIDEWATER INC"
    },
    "BPMC": {
        "cik": 1597264,
        "title": "Blueprint Medicines Corp"
    },
    "ARRY": {
        "cik": 1820721,
        "title": "Array Technologies, Inc."
    },
    "ARWR": {
        "cik": 879407,
        "title": "ARROWHEAD PHARMACEUTICALS, INC."
    },
    "TEO": {
        "cik": 932470,
        "title": "TELECOM ARGENTINA SA"
    },
    "BHC": {
        "cik": 885590,
        "title": "Bausch Health Companies Inc."
    },
    "PRTA": {
        "cik": 1559053,
        "title": "PROTHENA CORP PUBLIC LTD CO"
    },
    "PTEN": {
        "cik": 889900,
        "title": "PATTERSON UTI ENERGY INC"
    },
    "TJBH": {
        "cik": 1499785,
        "title": "Tengjun Biotechnology Corp."
    },
    "NWE": {
        "cik": 73088,
        "title": "NORTHWESTERN CORP"
    },
    "JWN": {
        "cik": 72333,
        "title": "NORDSTROM INC"
    },
    "QS": {
        "cik": 1811414,
        "title": "QuantumScape Corp"
    },
    "ITRI": {
        "cik": 780571,
        "title": "ITRON, INC."
    },
    "CNS": {
        "cik": 1284812,
        "title": "COHEN & STEERS, INC."
    },
    "INSM": {
        "cik": 1104506,
        "title": "INSMED Inc"
    },
    "CD": {
        "cik": 1807192,
        "title": "Chindata Group Holdings Ltd"
    },
    "VICR": {
        "cik": 751978,
        "title": "VICOR CORP"
    },
    "WB": {
        "cik": 1595761,
        "title": "WEIBO Corp"
    },
    "ENOV": {
        "cik": 1420800,
        "title": "Enovis CORP"
    },
    "MODG": {
        "cik": 837465,
        "title": "Topgolf Callaway Brands Corp."
    },
    "WNS": {
        "cik": 1356570,
        "title": "WNS (HOLDINGS) LTD"
    },
    "CVLT": {
        "cik": 1169561,
        "title": "COMMVAULT SYSTEMS INC"
    },
    "AMED": {
        "cik": 896262,
        "title": "AMEDISYS INC"
    },
    "FHI": {
        "cik": 1056288,
        "title": "FEDERATED HERMES, INC."
    },
    "GBTC": {
        "cik": 1588489,
        "title": "Grayscale Bitcoin Trust (BTC)"
    },
    "BE": {
        "cik": 1664703,
        "title": "Bloom Energy Corp"
    },
    "ABM": {
        "cik": 771497,
        "title": "ABM INDUSTRIES INC /DE/"
    },
    "TWNK": {
        "cik": 1644406,
        "title": "Hostess Brands, Inc."
    },
    "SHWDY": {
        "cik": 1446694,
        "title": "Showa Denko K.K./ADR"
    },
    "KWR": {
        "cik": 81362,
        "title": "QUAKER CHEMICAL CORP"
    },
    "KMPR": {
        "cik": 860748,
        "title": "KEMPER Corp"
    },
    "TNL": {
        "cik": 1361658,
        "title": "Travel & Leisure Co."
    },
    "PJT": {
        "cik": 1626115,
        "title": "PJT Partners Inc."
    },
    "RUN": {
        "cik": 1469367,
        "title": "Sunrun Inc."
    },
    "HAYW": {
        "cik": 1834622,
        "title": "Hayward Holdings, Inc."
    },
    "OI": {
        "cik": 812074,
        "title": "O-I Glass, Inc. /DE/"
    },
    "WDFC": {
        "cik": 105132,
        "title": "WD 40 CO"
    },
    "PINC": {
        "cik": 1577916,
        "title": "Premier, Inc."
    },
    "EXPI": {
        "cik": 1495932,
        "title": "EXP World Holdings, Inc."
    },
    "LIVN": {
        "cik": 1639691,
        "title": "LivaNova PLC"
    },
    "PTCT": {
        "cik": 1070081,
        "title": "PTC THERAPEUTICS, INC."
    },
    "ROYMY": {
        "cik": 1592438,
        "title": "Royal Mail plc/ADR"
    },
    "HELE": {
        "cik": 916789,
        "title": "HELEN OF TROY LTD"
    },
    "TPH": {
        "cik": 1561680,
        "title": "Tri Pointe Homes, Inc."
    },
    "EVH": {
        "cik": 1628908,
        "title": "Evolent Health, Inc."
    },
    "MC": {
        "cik": 1596967,
        "title": "Moelis & Co"
    },
    "AXNX": {
        "cik": 1603756,
        "title": "Axonics, Inc."
    },
    "PAGS": {
        "cik": 1712807,
        "title": "PagSeguro Digital Ltd."
    },
    "PBH": {
        "cik": 1295947,
        "title": "Prestige Consumer Healthcare Inc."
    },
    "SHAK": {
        "cik": 1620533,
        "title": "Shake Shack Inc."
    },
    "LFST": {
        "cik": 1845257,
        "title": "LifeStance Health Group, Inc."
    },
    "SSRM": {
        "cik": 921638,
        "title": "SSR MINING INC."
    },
    "PRVA": {
        "cik": 1759655,
        "title": "Privia Health Group, Inc."
    },
    "KLIC": {
        "cik": 56978,
        "title": "KULICKE & SOFFA INDUSTRIES INC"
    },
    "CEIX": {
        "cik": 1710366,
        "title": "CONSOL Energy Inc."
    },
    "KOZAY": {
        "cik": 1532173,
        "title": "Koza Altin Isletmeleri A.S./ADR"
    },
    "CEQP": {
        "cik": 1136352,
        "title": "Crestwood Equity Partners LP"
    },
    "DOCN": {
        "cik": 1582961,
        "title": "DigitalOcean Holdings, Inc."
    },
    "BUR": {
        "cik": 1714174,
        "title": "Burford Capital Ltd"
    },
    "ENV": {
        "cik": 1337619,
        "title": "ENVESTNET, INC."
    },
    "STNG": {
        "cik": 1483934,
        "title": "Scorpio Tankers Inc."
    },
    "VRRM": {
        "cik": 1682745,
        "title": "VERRA MOBILITY Corp"
    },
    "AIN": {
        "cik": 819793,
        "title": "ALBANY INTERNATIONAL CORP /DE/"
    },
    "IONQ": {
        "cik": 1824920,
        "title": "IonQ, Inc."
    },
    "MEOH": {
        "cik": 886977,
        "title": "METHANEX CORP"
    },
    "ALRM": {
        "cik": 1459200,
        "title": "Alarm.com Holdings, Inc."
    },
    "MLTX": {
        "cik": 1821586,
        "title": "MoonLake Immunotherapeutics"
    },
    "OFC": {
        "cik": 860546,
        "title": "CORPORATE OFFICE PROPERTIES TRUST"
    },
    "CWT": {
        "cik": 1035201,
        "title": "CALIFORNIA WATER SERVICE GROUP"
    },
    "TCBI": {
        "cik": 1077428,
        "title": "TEXAS CAPITAL BANCSHARES INC/TX"
    },
    "CSWI": {
        "cik": 1624794,
        "title": "CSW INDUSTRIALS, INC."
    },
    "SHZNY": {
        "cik": 1454480,
        "title": "Shenzhen Expressway Co. / ADR"
    },
    "LAZ": {
        "cik": 1311370,
        "title": "Lazard Ltd"
    },
    "RKLB": {
        "cik": 1819994,
        "title": "Rocket Lab USA, Inc."
    },
    "ABCB": {
        "cik": 351569,
        "title": "Ameris Bancorp"
    },
    "ITGR": {
        "cik": 1114483,
        "title": "Integer Holdings Corp"
    },
    "NWTN": {
        "cik": 1932737,
        "title": "NWTN, Inc."
    },
    "YELP": {
        "cik": 1345016,
        "title": "YELP INC"
    },
    "SMG": {
        "cik": 825542,
        "title": "SCOTTS MIRACLE-GRO CO"
    },
    "IBOC": {
        "cik": 315709,
        "title": "INTERNATIONAL BANCSHARES CORP"
    },
    "GMS": {
        "cik": 1600438,
        "title": "GMS Inc."
    },
    "DY": {
        "cik": 67215,
        "title": "DYCOM INDUSTRIES INC"
    },
    "PK": {
        "cik": 1617406,
        "title": "Park Hotels & Resorts Inc."
    },
    "AVAL": {
        "cik": 1504764,
        "title": "Grupo Aval Acciones Y Valores S.A."
    },
    "CRS": {
        "cik": 17843,
        "title": "CARPENTER TECHNOLOGY CORP"
    },
    "WD": {
        "cik": 1497770,
        "title": "Walker & Dunlop, Inc."
    },
    "IMCR": {
        "cik": 1671927,
        "title": "Immunocore Holdings plc"
    },
    "KNF": {
        "cik": 1955520,
        "title": "Knife River Corp"
    },
    "LAC": {
        "cik": 1440972,
        "title": "LITHIUM AMERICAS CORP."
    },
    "JXN": {
        "cik": 1822993,
        "title": "Jackson Financial Inc."
    },
    "RPD": {
        "cik": 1560327,
        "title": "Rapid7, Inc."
    },
    "WIRE": {
        "cik": 850460,
        "title": "ENCORE WIRE CORP"
    },
    "SITM": {
        "cik": 1451809,
        "title": "SITIME Corp"
    },
    "BOOT": {
        "cik": 1610250,
        "title": "Boot Barn Holdings, Inc."
    },
    "FIBK": {
        "cik": 860413,
        "title": "FIRST INTERSTATE BANCSYSTEM INC"
    },
    "KTB": {
        "cik": 1760965,
        "title": "Kontoor Brands, Inc."
    },
    "SBRA": {
        "cik": 1492298,
        "title": "Sabra Health Care REIT, Inc."
    },
    "AMR": {
        "cik": 1704715,
        "title": "Alpha Metallurgical Resources, Inc."
    },
    "AMBA": {
        "cik": 1280263,
        "title": "AMBARELLA INC"
    },
    "FROG": {
        "cik": 1800667,
        "title": "JFrog Ltd"
    },
    "ESMT": {
        "cik": 1863105,
        "title": "EngageSmart, Inc."
    },
    "HEP": {
        "cik": 1283140,
        "title": "HOLLY ENERGY PARTNERS LP"
    },
    "UPST": {
        "cik": 1647639,
        "title": "Upstart Holdings, Inc."
    },
    "TFPM": {
        "cik": 1829726,
        "title": "Triple Flag Precious Metals Corp."
    },
    "CCU": {
        "cik": 888746,
        "title": "UNITED BREWERIES CO INC"
    },
    "LXP": {
        "cik": 910108,
        "title": "LXP Industrial Trust"
    },
    "ERJ": {
        "cik": 1355444,
        "title": "EMBRAER S.A."
    },
    "LBRT": {
        "cik": 1694028,
        "title": "Liberty Energy Inc."
    },
    "RNG": {
        "cik": 1384905,
        "title": "RingCentral, Inc."
    },
    "ABR": {
        "cik": 1253986,
        "title": "ARBOR REALTY TRUST INC"
    },
    "IMVT": {
        "cik": 1764013,
        "title": "Immunovant, Inc."
    },
    "LGIH": {
        "cik": 1580670,
        "title": "LGI Homes, Inc."
    },
    "GHC": {
        "cik": 104889,
        "title": "Graham Holdings Co"
    },
    "WERN": {
        "cik": 793074,
        "title": "WERNER ENTERPRISES INC"
    },
    "IFS": {
        "cik": 1615903,
        "title": "Intercorp Financial Services Inc."
    },
    "GNW": {
        "cik": 1276520,
        "title": "GENWORTH FINANCIAL INC"
    },
    "MGEE": {
        "cik": 1161728,
        "title": "MGE ENERGY INC"
    },
    "AMC": {
        "cik": 1411579,
        "title": "AMC ENTERTAINMENT HOLDINGS, INC."
    },
    "KFY": {
        "cik": 56679,
        "title": "KORN FERRY"
    },
    "HUBG": {
        "cik": 940942,
        "title": "Hub Group, Inc."
    },
    "PLXS": {
        "cik": 785786,
        "title": "PLEXUS CORP"
    },
    "DBC": {
        "cik": 1328237,
        "title": "Invesco DB Commodity Index Tracking Fund"
    },
    "DQ": {
        "cik": 1477641,
        "title": "DAQO NEW ENERGY CORP."
    },
    "SITC": {
        "cik": 894315,
        "title": "SITE Centers Corp."
    },
    "CBZ": {
        "cik": 944148,
        "title": "CBIZ, Inc."
    },
    "ATAT": {
        "cik": 1853717,
        "title": "Atour Lifestyle Holdings Ltd"
    },
    "FTDR": {
        "cik": 1727263,
        "title": "Frontdoor, Inc."
    },
    "AKRO": {
        "cik": 1744659,
        "title": "Akero Therapeutics, Inc."
    },
    "CALX": {
        "cik": 1406666,
        "title": "CALIX, INC"
    },
    "CRI": {
        "cik": 1060822,
        "title": "CARTERS INC"
    },
    "CNO": {
        "cik": 1224608,
        "title": "CNO Financial Group, Inc."
    },
    "SDGR": {
        "cik": 1490978,
        "title": "Schrodinger, Inc."
    },
    "SLRN": {
        "cik": 1962918,
        "title": "ACELYRIN, Inc."
    },
    "NPO": {
        "cik": 1164863,
        "title": "ENPRO INDUSTRIES, INC"
    },
    "MRVI": {
        "cik": 1823239,
        "title": "MARAVAI LIFESCIENCES HOLDINGS, INC."
    },
    "TIGO": {
        "cik": 912958,
        "title": "MILLICOM INTERNATIONAL CELLULAR SA"
    },
    "CRGY": {
        "cik": 1866175,
        "title": "Crescent Energy Co"
    },
    "TV": {
        "cik": 912892,
        "title": "GRUPO TELEVISA, S.A.B."
    },
    "ESTE": {
        "cik": 10254,
        "title": "EARTHSTONE ENERGY INC"
    },
    "ESE": {
        "cik": 866706,
        "title": "ESCO TECHNOLOGIES INC"
    },
    "MGPI": {
        "cik": 835011,
        "title": "MGP INGREDIENTS INC"
    },
    "GLPG": {
        "cik": 1421876,
        "title": "GALAPAGOS NV"
    },
    "DAVA": {
        "cik": 1656081,
        "title": "Endava plc"
    },
    "ARCB": {
        "cik": 894405,
        "title": "ARCBEST CORP /DE/"
    },
    "RARE": {
        "cik": 1515673,
        "title": "Ultragenyx Pharmaceutical Inc."
    },
    "OMCL": {
        "cik": 926326,
        "title": "OMNICELL, INC."
    },
    "ASB": {
        "cik": 7789,
        "title": "ASSOCIATED BANC-CORP"
    },
    "SHOO": {
        "cik": 913241,
        "title": "STEVEN MADDEN, LTD."
    },
    "IOSP": {
        "cik": 1054905,
        "title": "INNOSPEC INC."
    },
    "AMPH": {
        "cik": 1297184,
        "title": "Amphastar Pharmaceuticals, Inc."
    },
    "DORM": {
        "cik": 868780,
        "title": "Dorman Products, Inc."
    },
    "HL": {
        "cik": 719413,
        "title": "HECLA MINING CO/DE/"
    },
    "CERT": {
        "cik": 1827090,
        "title": "Certara, Inc."
    },
    "ALVO": {
        "cik": 1898416,
        "title": "Alvotech"
    },
    "DEI": {
        "cik": 1364250,
        "title": "Douglas Emmett Inc"
    },
    "MHO": {
        "cik": 799292,
        "title": "M/I HOMES, INC."
    },
    "CBU": {
        "cik": 723188,
        "title": "COMMUNITY BANK SYSTEM, INC."
    },
    "TAC": {
        "cik": 1144800,
        "title": "TRANSALTA CORP"
    },
    "THS": {
        "cik": 1320695,
        "title": "TreeHouse Foods, Inc."
    },
    "PRGS": {
        "cik": 876167,
        "title": "PROGRESS SOFTWARE CORP /MA"
    },
    "BB": {
        "cik": 1070235,
        "title": "BLACKBERRY Ltd"
    },
    "QFIN": {
        "cik": 1741530,
        "title": "Qifu Technology, Inc."
    },
    "ARLP": {
        "cik": 1086600,
        "title": "ALLIANCE RESOURCE PARTNERS LP"
    },
    "GDRX": {
        "cik": 1809519,
        "title": "GoodRx Holdings, Inc."
    },
    "ODD": {
        "cik": 1907085,
        "title": "Oddity Tech Ltd"
    },
    "PACB": {
        "cik": 1299130,
        "title": "PACIFIC BIOSCIENCES OF CALIFORNIA, INC."
    },
    "ROG": {
        "cik": 84748,
        "title": "ROGERS CORP"
    },
    "AY": {
        "cik": 1601072,
        "title": "Atlantica Sustainable Infrastructure plc"
    },
    "MORF": {
        "cik": 1679363,
        "title": "Morphic Holding, Inc."
    },
    "SPT": {
        "cik": 1517375,
        "title": "Sprout Social, Inc."
    },
    "PTON": {
        "cik": 1639825,
        "title": "PELOTON INTERACTIVE, INC."
    },
    "MAC": {
        "cik": 912242,
        "title": "MACERICH CO"
    },
    "NXE": {
        "cik": 1698535,
        "title": "NexGen Energy Ltd."
    },
    "CATY": {
        "cik": 861842,
        "title": "CATHAY GENERAL BANCORP"
    },
    "EVTC": {
        "cik": 1559865,
        "title": "EVERTEC, Inc."
    },
    "WSFS": {
        "cik": 828944,
        "title": "WSFS FINANCIAL CORP"
    },
    "GBDC": {
        "cik": 1476765,
        "title": "GOLUB CAPITAL BDC, Inc."
    },
    "CPE": {
        "cik": 928022,
        "title": "Callon Petroleum Co"
    },
    "AVA": {
        "cik": 104918,
        "title": "AVISTA CORP"
    },
    "FBP": {
        "cik": 1057706,
        "title": "FIRST BANCORP /PR/"
    },
    "NAD": {
        "cik": 1083839,
        "title": "Nuveen Quality Municipal Income Fund"
    },
    "ARCH": {
        "cik": 1037676,
        "title": "ARCH RESOURCES, INC."
    },
    "APAM": {
        "cik": 1517302,
        "title": "Artisan Partners Asset Management Inc."
    },
    "XPRO": {
        "cik": 1575828,
        "title": "EXPRO GROUP HOLDINGS N.V."
    },
    "PZZA": {
        "cik": 901491,
        "title": "PAPA JOHNS INTERNATIONAL INC"
    },
    "ACVA": {
        "cik": 1637873,
        "title": "ACV Auctions Inc."
    },
    "AVAV": {
        "cik": 1368622,
        "title": "AeroVironment Inc"
    },
    "DFH": {
        "cik": 1825088,
        "title": "Dream Finders Homes, Inc."
    },
    "DBRG": {
        "cik": 1679688,
        "title": "DigitalBridge Group, Inc."
    },
    "NEX": {
        "cik": 1688476,
        "title": "NEXTIER OILFIELD SOLUTIONS INC."
    },
    "CHPT": {
        "cik": 1777393,
        "title": "ChargePoint Holdings, Inc."
    },
    "KAI": {
        "cik": 886346,
        "title": "KADANT INC"
    },
    "CLS": {
        "cik": 1030894,
        "title": "CELESTICA INC"
    },
    "HCM": {
        "cik": 1648257,
        "title": "HUTCHMED (China) Ltd"
    },
    "AMRC": {
        "cik": 1488139,
        "title": "Ameresco, Inc."
    },
    "HIW": {
        "cik": 921082,
        "title": "HIGHWOODS PROPERTIES, INC."
    },
    "CSTM": {
        "cik": 1563411,
        "title": "CONSTELLIUM SE"
    },
    "OR": {
        "cik": 1627272,
        "title": "Osisko Gold Royalties LTD"
    },
    "PSEC": {
        "cik": 1287032,
        "title": "PROSPECT CAPITAL CORP"
    },
    "COUR": {
        "cik": 1651562,
        "title": "Coursera, Inc."
    },
    "PSMT": {
        "cik": 1041803,
        "title": "PRICESMART INC"
    },
    "ACIW": {
        "cik": 935036,
        "title": "ACI WORLDWIDE, INC."
    },
    "SXT": {
        "cik": 310142,
        "title": "SENSIENT TECHNOLOGIES CORP"
    },
    "DRVN": {
        "cik": 1804745,
        "title": "Driven Brands Holdings Inc."
    },
    "RRR": {
        "cik": 1653653,
        "title": "Red Rock Resorts, Inc."
    },
    "ENR": {
        "cik": 1632790,
        "title": "ENERGIZER HOLDINGS, INC."
    },
    "BRC": {
        "cik": 746598,
        "title": "BRADY CORP"
    },
    "SKT": {
        "cik": 899715,
        "title": "TANGER FACTORY OUTLET CENTERS, INC"
    },
    "XENE": {
        "cik": 1582313,
        "title": "Xenon Pharmaceuticals Inc."
    },
    "CVBF": {
        "cik": 354647,
        "title": "CVB FINANCIAL CORP"
    },
    "ZLAB": {
        "cik": 1704292,
        "title": "Zai Lab Ltd"
    },
    "INDB": {
        "cik": 776901,
        "title": "INDEPENDENT BANK CORP"
    },
    "FHB": {
        "cik": 36377,
        "title": "FIRST HAWAIIAN, INC."
    },
    "MGRC": {
        "cik": 752714,
        "title": "MCGRATH RENTCORP"
    },
    "XRX": {
        "cik": 1770450,
        "title": "Xerox Holdings Corp"
    },
    "OSTIY": {
        "cik": 1570187,
        "title": "Osterreichische Post AG ADR"
    },
    "BLMN": {
        "cik": 1546417,
        "title": "Bloomin' Brands, Inc."
    },
    "FSLY": {
        "cik": 1517413,
        "title": "Fastly, Inc."
    },
    "NVEI": {
        "cik": 1765159,
        "title": "Nuvei Corp"
    },
    "STRL": {
        "cik": 874238,
        "title": "STERLING INFRASTRUCTURE, INC."
    },
    "PRMW": {
        "cik": 884713,
        "title": "Primo Water Corp /CN/"
    },
    "DEA": {
        "cik": 1622194,
        "title": "Easterly Government Properties, Inc."
    },
    "AX": {
        "cik": 1299709,
        "title": "Axos Financial, Inc."
    },
    "GLNG": {
        "cik": 1207179,
        "title": "GOLAR LNG LTD"
    },
    "ICFI": {
        "cik": 1362004,
        "title": "ICF International, Inc."
    },
    "VIST": {
        "cik": 1762506,
        "title": "Vista Energy, S.A.B. de C.V."
    },
    "NVG": {
        "cik": 1090116,
        "title": "Nuveen AMT-Free Municipal Credit Income Fund"
    },
    "NUVL": {
        "cik": 1861560,
        "title": "Nuvalent, Inc."
    },
    "LSPD": {
        "cik": 1823306,
        "title": "Lightspeed Commerce Inc."
    },
    "HTGC": {
        "cik": 1280784,
        "title": "Hercules Capital, Inc."
    },
    "ITCL": {
        "cik": 1276671,
        "title": "BANCO ITAU CHILE"
    },
    "TRMD": {
        "cik": 1655891,
        "title": "TORM plc"
    },
    "INTA": {
        "cik": 1565687,
        "title": "Intapp, Inc."
    },
    "NABL": {
        "cik": 1834488,
        "title": "N-able, Inc."
    },
    "EXG": {
        "cik": 1379438,
        "title": "Eaton Vance Tax-Managed Global Diversified Equity Income Fund"
    },
    "EBC": {
        "cik": 1810546,
        "title": "Eastern Bankshares, Inc."
    },
    "FORM": {
        "cik": 1039399,
        "title": "FORMFACTOR INC"
    },
    "VET": {
        "cik": 1293135,
        "title": "VERMILION ENERGY INC."
    },
    "RLX": {
        "cik": 1828365,
        "title": "RLX Technology Inc."
    },
    "BATRA": {
        "cik": 1958140,
        "title": "Atlanta Braves Holdings, Inc."
    },
    "CALM": {
        "cik": 16160,
        "title": "CAL-MAINE FOODS INC"
    },
    "REZI": {
        "cik": 1740332,
        "title": "RESIDEO TECHNOLOGIES, INC."
    },
    "MYRG": {
        "cik": 700923,
        "title": "MYR GROUP INC."
    },
    "NMIH": {
        "cik": 1547903,
        "title": "NMI Holdings, Inc."
    },
    "GFF": {
        "cik": 50725,
        "title": "GRIFFON CORP"
    },
    "CVCO": {
        "cik": 278166,
        "title": "CAVCO INDUSTRIES INC."
    },
    "IHS": {
        "cik": 1876183,
        "title": "IHS Holding Ltd"
    },
    "FL": {
        "cik": 850209,
        "title": "FOOT LOCKER, INC."
    },
    "CSQ": {
        "cik": 1275214,
        "title": "CALAMOS STRATEGIC TOTAL RETURN FUND"
    },
    "TR": {
        "cik": 98677,
        "title": "TOOTSIE ROLL INDUSTRIES INC"
    },
    "INSW": {
        "cik": 1679049,
        "title": "International Seaways, Inc."
    },
    "CAAP": {
        "cik": 1717393,
        "title": "CORPORACION AMERICA AIRPORTS S.A."
    },
    "XPEL": {
        "cik": 1767258,
        "title": "XPEL, Inc."
    },
    "LZ": {
        "cik": 1286139,
        "title": "LEGALZOOM.COM, INC."
    },
    "ESRT": {
        "cik": 1541401,
        "title": "Empire State Realty Trust, Inc."
    },
    "SOVO": {
        "cik": 1856608,
        "title": "Sovos Brands, Inc."
    },
    "RNW": {
        "cik": 1848763,
        "title": "ReNew Energy Global plc"
    },
    "CENT": {
        "cik": 887733,
        "title": "CENTRAL GARDEN & PET CO"
    },
    "VRTV": {
        "cik": 1599489,
        "title": "Veritiv Corp"
    },
    "DAN": {
        "cik": 26780,
        "title": "DANA INC"
    },
    "SPR": {
        "cik": 1364885,
        "title": "Spirit AeroSystems Holdings, Inc."
    },
    "DOOR": {
        "cik": 893691,
        "title": "MASONITE INTERNATIONAL CORP"
    },
    "AUB": {
        "cik": 883948,
        "title": "Atlantic Union Bankshares Corp"
    },
    "TIXT": {
        "cik": 1825155,
        "title": "TELUS International (Cda) Inc."
    },
    "GSHD": {
        "cik": 1726978,
        "title": "Goosehead Insurance, Inc."
    },
    "SFNC": {
        "cik": 90498,
        "title": "SIMMONS FIRST NATIONAL CORP"
    },
    "ATRC": {
        "cik": 1323885,
        "title": "AtriCure, Inc."
    },
    "MRTX": {
        "cik": 1576263,
        "title": "Mirati Therapeutics, Inc."
    },
    "LAUR": {
        "cik": 912766,
        "title": "LAUREATE EDUCATION, INC."
    },
    "VIAV": {
        "cik": 912093,
        "title": "VIAVI SOLUTIONS INC."
    },
    "MOD": {
        "cik": 67347,
        "title": "MODINE MANUFACTURING CO"
    },
    "CCS": {
        "cik": 1576940,
        "title": "Century Communities, Inc."
    },
    "BGC": {
        "cik": 1094831,
        "title": "BGC Group, Inc."
    },
    "YY": {
        "cik": 1530238,
        "title": "JOYY Inc."
    },
    "AKO-A": {
        "cik": 925261,
        "title": "ANDINA BOTTLING CO INC"
    },
    "VCTR": {
        "cik": 1570827,
        "title": "Victory Capital Holdings, Inc."
    },
    "SLG": {
        "cik": 1040971,
        "title": "SL GREEN REALTY CORP"
    },
    "FTRE": {
        "cik": 1965040,
        "title": "Fortrea Holdings Inc."
    },
    "DNUT": {
        "cik": 1857154,
        "title": "Krispy Kreme, Inc."
    },
    "RXO": {
        "cik": 1929561,
        "title": "RXO, Inc."
    },
    "ENVX": {
        "cik": 1828318,
        "title": "Enovix Corp"
    },
    "PD": {
        "cik": 1568100,
        "title": "PagerDuty, Inc."
    },
    "ESBA": {
        "cik": 1553079,
        "title": "Empire State Realty OP, L.P."
    },
    "HMY": {
        "cik": 1023514,
        "title": "HARMONY GOLD MINING CO LTD"
    },
    "TRIP": {
        "cik": 1526520,
        "title": "TripAdvisor, Inc."
    },
    "PPBI": {
        "cik": 1028918,
        "title": "PACIFIC PREMIER BANCORP INC"
    },
    "MRCY": {
        "cik": 1049521,
        "title": "MERCURY SYSTEMS INC"
    },
    "NAVI": {
        "cik": 1593538,
        "title": "NAVIENT CORP"
    },
    "AESI": {
        "cik": 1910950,
        "title": "Atlas Energy Solutions Inc."
    },
    "LAZR": {
        "cik": 1758057,
        "title": "Luminar Technologies, Inc./DE"
    },
    "IAS": {
        "cik": 1842718,
        "title": "INTEGRAL AD SCIENCE HOLDING CORP."
    },
    "CRDO": {
        "cik": 1807794,
        "title": "Credo Technology Group Holding Ltd"
    },
    "IDCC": {
        "cik": 1405495,
        "title": "InterDigital, Inc."
    },
    "TCN": {
        "cik": 1584425,
        "title": "Tricon Residential Inc."
    },
    "FULT": {
        "cik": 700564,
        "title": "FULTON FINANCIAL CORP"
    },
    "PROK": {
        "cik": 1850270,
        "title": "PROKIDNEY CORP."
    },
    "NHI": {
        "cik": 877860,
        "title": "NATIONAL HEALTH INVESTORS INC"
    },
    "NZF": {
        "cik": 1137887,
        "title": "Nuveen Municipal Credit Income Fund"
    },
    "MTRN": {
        "cik": 1104657,
        "title": "MATERION Corp"
    },
    "MWA": {
        "cik": 1350593,
        "title": "Mueller Water Products, Inc."
    },
    "VIEW": {
        "cik": 1811856,
        "title": "View, Inc."
    },
    "ROCK": {
        "cik": 912562,
        "title": "GIBRALTAR INDUSTRIES, INC."
    },
    "CNK": {
        "cik": 1385280,
        "title": "Cinemark Holdings, Inc."
    },
    "IIPR": {
        "cik": 1677576,
        "title": "INNOVATIVE INDUSTRIAL PROPERTIES INC"
    },
    "HASI": {
        "cik": 1561894,
        "title": "Hannon Armstrong Sustainable Infrastructure Capital, Inc."
    },
    "GRBK": {
        "cik": 1373670,
        "title": "Green Brick Partners, Inc."
    },
    "CAMT": {
        "cik": 1109138,
        "title": "CAMTEK LTD"
    },
    "SSII": {
        "cik": 1676163,
        "title": "SS Innovations International, Inc."
    },
    "TALO": {
        "cik": 1724965,
        "title": "TALOS ENERGY INC."
    },
    "FCPT": {
        "cik": 1650132,
        "title": "Four Corners Property Trust, Inc."
    },
    "PARR": {
        "cik": 821483,
        "title": "PAR PACIFIC HOLDINGS, INC."
    },
    "TMDX": {
        "cik": 1756262,
        "title": "TransMedics Group, Inc."
    },
    "OII": {
        "cik": 73756,
        "title": "OCEANEERING INTERNATIONAL INC"
    },
    "CURLF": {
        "cik": 1756770,
        "title": "Curaleaf Holdings, Inc."
    },
    "OPEN": {
        "cik": 1801169,
        "title": "Opendoor Technologies Inc."
    },
    "GTX": {
        "cik": 1735707,
        "title": "Garrett Motion Inc."
    },
    "LVWR": {
        "cik": 1898795,
        "title": "LiveWire Group, Inc."
    },
    "KW": {
        "cik": 1408100,
        "title": "Kennedy-Wilson Holdings, Inc."
    },
    "PTXKY": {
        "cik": 1545057,
        "title": "PT XL Axiata Tbk/ADR"
    },
    "ARCO": {
        "cik": 1508478,
        "title": "Arcos Dorados Holdings Inc."
    },
    "NUVA": {
        "cik": 1142596,
        "title": "NUVASIVE INC"
    },
    "ANF": {
        "cik": 1018840,
        "title": "ABERCROMBIE & FITCH CO /DE/"
    },
    "KMT": {
        "cik": 55242,
        "title": "KENNAMETAL INC"
    },
    "EVEX": {
        "cik": 1823652,
        "title": "Eve Holding, Inc."
    },
    "SJW": {
        "cik": 766829,
        "title": "SJW GROUP"
    },
    "AIR": {
        "cik": 1750,
        "title": "AAR CORP"
    },
    "VRNT": {
        "cik": 1166388,
        "title": "VERINT SYSTEMS INC"
    },
    "BOH": {
        "cik": 46195,
        "title": "BANK OF HAWAII CORP"
    },
    "STGW": {
        "cik": 876883,
        "title": "Stagwell Inc"
    },
    "PAX": {
        "cik": 1825570,
        "title": "Patria Investments Ltd"
    },
    "PAYO": {
        "cik": 1845815,
        "title": "Payoneer Global Inc."
    },
    "PRFT": {
        "cik": 1085869,
        "title": "PERFICIENT INC"
    },
    "JAMF": {
        "cik": 1721947,
        "title": "Jamf Holding Corp."
    },
    "EE": {
        "cik": 1888447,
        "title": "Excelerate Energy, Inc."
    },
    "EQC": {
        "cik": 803649,
        "title": "Equity Commonwealth"
    },
    "CRCT": {
        "cik": 1828962,
        "title": "Cricut, Inc."
    },
    "RAMP": {
        "cik": 733269,
        "title": "LiveRamp Holdings, Inc."
    },
    "JBLU": {
        "cik": 1158463,
        "title": "JETBLUE AIRWAYS CORP"
    },
    "AMBP": {
        "cik": 1845097,
        "title": "Ardagh Metal Packaging S.A."
    },
    "AMK": {
        "cik": 1591587,
        "title": "AssetMark Financial Holdings, Inc."
    },
    "HCC": {
        "cik": 1691303,
        "title": "WARRIOR MET COAL, INC."
    },
    "ADX": {
        "cik": 2230,
        "title": "ADAMS DIVERSIFIED EQUITY FUND, INC."
    },
    "SNEX": {
        "cik": 913760,
        "title": "StoneX Group Inc."
    },
    "CARG": {
        "cik": 1494259,
        "title": "CarGurus, Inc."
    },
    "RDNT": {
        "cik": 790526,
        "title": "RadNet, Inc."
    },
    "FFBC": {
        "cik": 708955,
        "title": "FIRST FINANCIAL BANCORP /OH/"
    },
    "TDS": {
        "cik": 1051512,
        "title": "TELEPHONE & DATA SYSTEMS INC /DE/"
    },
    "FUN": {
        "cik": 811532,
        "title": "CEDAR FAIR L P"
    },
    "MCW": {
        "cik": 1853513,
        "title": "Mister Car Wash, Inc."
    },
    "UTF": {
        "cik": 1275617,
        "title": "COHEN & STEERS INFRASTRUCTURE FUND INC"
    },
    "ALG": {
        "cik": 897077,
        "title": "ALAMO GROUP INC"
    },
    "STAA": {
        "cik": 718937,
        "title": "STAAR SURGICAL CO"
    },
    "PIPR": {
        "cik": 1230245,
        "title": "PIPER SANDLER COMPANIES"
    },
    "FA": {
        "cik": 1210677,
        "title": "FIRST ADVANTAGE CORP"
    },
    "TRN": {
        "cik": 99780,
        "title": "TRINITY INDUSTRIES INC"
    },
    "USAC": {
        "cik": 1522727,
        "title": "USA Compression Partners, LP"
    },
    "GPOR": {
        "cik": 874499,
        "title": "GULFPORT ENERGY CORP"
    },
    "THRM": {
        "cik": 903129,
        "title": "GENTHERM Inc"
    },
    "CEPU": {
        "cik": 1717161,
        "title": "CENTRAL PUERTO S.A."
    },
    "AYX": {
        "cik": 1689923,
        "title": "Alteryx, Inc."
    },
    "BVN": {
        "cik": 1013131,
        "title": "BUENAVENTURA MINING CO INC"
    },
    "AQPW": {
        "cik": 1317833,
        "title": "Golden Ally Lifetech Group, Inc."
    },
    "CWK": {
        "cik": 1628369,
        "title": "Cushman & Wakefield plc"
    },
    "SYSX": {
        "cik": 1737372,
        "title": "Sysorex, Inc."
    },
    "CMRF": {
        "cik": 1498547,
        "title": "CIM REAL ESTATE FINANCE TRUST, INC."
    },
    "CVAC": {
        "cik": 1809122,
        "title": "CureVac N.V."
    },
    "OLK": {
        "cik": 1835539,
        "title": "Olink Holding AB (publ)"
    },
    "GDS": {
        "cik": 1526125,
        "title": "GDS Holdings Ltd"
    },
    "WLY": {
        "cik": 107140,
        "title": "JOHN WILEY & SONS, INC."
    },
    "CSIQ": {
        "cik": 1375877,
        "title": "Canadian Solar Inc."
    },
    "NTCT": {
        "cik": 1078075,
        "title": "NETSCOUT SYSTEMS INC"
    },
    "OSIS": {
        "cik": 1039065,
        "title": "OSI SYSTEMS INC"
    },
    "AROC": {
        "cik": 1389050,
        "title": "Archrock, Inc."
    },
    "AVDX": {
        "cik": 1858257,
        "title": "AvidXchange Holdings, Inc."
    },
    "HTH": {
        "cik": 1265131,
        "title": "Hilltop Holdings Inc."
    },
    "CTRE": {
        "cik": 1590717,
        "title": "CareTrust REIT, Inc."
    },
    "CPK": {
        "cik": 19745,
        "title": "CHESAPEAKE UTILITIES CORP"
    },
    "WGO": {
        "cik": 107687,
        "title": "WINNEBAGO INDUSTRIES INC"
    },
    "KTOS": {
        "cik": 1069258,
        "title": "KRATOS DEFENSE & SECURITY SOLUTIONS, INC."
    },
    "ENLT": {
        "cik": 1922641,
        "title": "Enlight Renewable Energy Ltd."
    },
    "UTG": {
        "cik": 1263994,
        "title": "REAVES UTILITY INCOME FUND"
    },
    "HRMY": {
        "cik": 1802665,
        "title": "Harmony Biosciences Holdings, Inc."
    },
    "SBCF": {
        "cik": 730708,
        "title": "SEACOAST BANKING CORP OF FLORIDA"
    },
    "TROX": {
        "cik": 1530804,
        "title": "Tronox Holdings plc"
    },
    "GSAT": {
        "cik": 1366868,
        "title": "Globalstar, Inc."
    },
    "SCL": {
        "cik": 94049,
        "title": "STEPAN CO"
    },
    "B": {
        "cik": 9984,
        "title": "BARNES GROUP INC"
    },
    "RUM": {
        "cik": 1830081,
        "title": "Rumble Inc."
    },
    "RIOT": {
        "cik": 1167419,
        "title": "Riot Platforms, Inc."
    },
    "TBBK": {
        "cik": 1295401,
        "title": "Bancorp, Inc."
    },
    "FORG": {
        "cik": 1543916,
        "title": "ForgeRock, Inc."
    },
    "FSR": {
        "cik": 1720990,
        "title": "Fisker Inc./DE"
    },
    "STRA": {
        "cik": 1013934,
        "title": "Strategic Education, Inc."
    },
    "BKE": {
        "cik": 885245,
        "title": "BUCKLE INC"
    },
    "GPRE": {
        "cik": 1309402,
        "title": "Green Plains Inc."
    },
    "EVCM": {
        "cik": 1853145,
        "title": "EverCommerce Inc."
    },
    "BKU": {
        "cik": 1504008,
        "title": "BankUnited, Inc."
    },
    "DVAX": {
        "cik": 1029142,
        "title": "DYNAVAX TECHNOLOGIES CORP"
    },
    "NXRT": {
        "cik": 1620393,
        "title": "NexPoint Residential Trust, Inc."
    },
    "QTWO": {
        "cik": 1410384,
        "title": "Q2 Holdings, Inc."
    },
    "ERO": {
        "cik": 1853860,
        "title": "Ero Copper Corp."
    },
    "EPC": {
        "cik": 1096752,
        "title": "EDGEWELL PERSONAL CARE Co"
    },
    "UE": {
        "cik": 1611547,
        "title": "Urban Edge Properties"
    },
    "MARA": {
        "cik": 1507605,
        "title": "MARATHON DIGITAL HOLDINGS, INC."
    },
    "VCYT": {
        "cik": 1384101,
        "title": "VERACYTE, INC."
    },
    "ODP": {
        "cik": 800240,
        "title": "ODP Corp"
    },
    "MTX": {
        "cik": 891014,
        "title": "MINERALS TECHNOLOGIES INC"
    },
    "ATMU": {
        "cik": 1921963,
        "title": "Atmus Filtration Technologies Inc."
    },
    "BFH": {
        "cik": 1101215,
        "title": "BREAD FINANCIAL HOLDINGS, INC."
    },
    "HLIO": {
        "cik": 1024795,
        "title": "HELIOS TECHNOLOGIES, INC."
    },
    "ETY": {
        "cik": 1340736,
        "title": "Eaton Vance Tax-Managed Diversified Equity Income Fund"
    },
    "UPWK": {
        "cik": 1627475,
        "title": "UPWORK, INC"
    },
    "SIMO": {
        "cik": 1329394,
        "title": "Silicon Motion Technology CORP"
    },
    "HBI": {
        "cik": 1359841,
        "title": "Hanesbrands Inc."
    },
    "GDV": {
        "cik": 1260729,
        "title": "GABELLI DIVIDEND & INCOME TRUST"
    },
    "ATGE": {
        "cik": 730464,
        "title": "Adtalem Global Education Inc."
    },
    "VTYX": {
        "cik": 1851194,
        "title": "Ventyx Biosciences, Inc."
    },
    "HURN": {
        "cik": 1289848,
        "title": "Huron Consulting Group Inc."
    },
    "SXI": {
        "cik": 310354,
        "title": "STANDEX INTERNATIONAL CORP/DE/"
    },
    "SVMB": {
        "cik": 1647822,
        "title": "SavMobi Technology Inc."
    },
    "CBRL": {
        "cik": 1067294,
        "title": "CRACKER BARREL OLD COUNTRY STORE, INC"
    },
    "PRIM": {
        "cik": 1361538,
        "title": "Primoris Services Corp"
    },
    "WMK": {
        "cik": 105418,
        "title": "WEIS MARKETS INC"
    },
    "NGVT": {
        "cik": 1653477,
        "title": "Ingevity Corp"
    },
    "LILA": {
        "cik": 1712184,
        "title": "Liberty Latin America Ltd."
    },
    "KNTK": {
        "cik": 1692787,
        "title": "Kinetik Holdings Inc."
    },
    "AILIH": {
        "cik": 18654,
        "title": "Ameren Illinois Co"
    },
    "SIX": {
        "cik": 701374,
        "title": "Six Flags Entertainment Corp"
    },
    "GVA": {
        "cik": 861459,
        "title": "GRANITE CONSTRUCTION INC"
    },
    "BEAM": {
        "cik": 1745999,
        "title": "Beam Therapeutics Inc."
    },
    "CLBK": {
        "cik": 1723596,
        "title": "Columbia Financial, Inc."
    },
    "PTY": {
        "cik": 1190935,
        "title": "PIMCO CORPORATE & INCOME OPPORTUNITY FUND"
    },
    "HPK": {
        "cik": 1792849,
        "title": "HighPeak Energy, Inc."
    },
    "SAVE": {
        "cik": 1498710,
        "title": "Spirit Airlines, Inc."
    },
    "SAH": {
        "cik": 1043509,
        "title": "SONIC AUTOMOTIVE INC"
    },
    "VRE": {
        "cik": 924901,
        "title": "Veris Residential, Inc."
    },
    "ZNTL": {
        "cik": 1725160,
        "title": "Zentalis Pharmaceuticals, Inc."
    },
    "MXL": {
        "cik": 1288469,
        "title": "MAXLINEAR, INC"
    },
    "WAFD": {
        "cik": 936528,
        "title": "WASHINGTON FEDERAL INC"
    },
    "NEO": {
        "cik": 1077183,
        "title": "NEOGENOMICS INC"
    },
    "OUT": {
        "cik": 1579877,
        "title": "OUTFRONT Media Inc."
    },
    "ACHR": {
        "cik": 1824502,
        "title": "Archer Aviation Inc."
    },
    "AGM": {
        "cik": 845877,
        "title": "FEDERAL AGRICULTURAL MORTGAGE CORP"
    },
    "TNDM": {
        "cik": 1438133,
        "title": "TANDEM DIABETES CARE INC"
    },
    "BOWL": {
        "cik": 1840572,
        "title": "Bowlero Corp."
    },
    "WOOF": {
        "cik": 1826470,
        "title": "Petco Health & Wellness Company, Inc."
    },
    "CLM": {
        "cik": 814083,
        "title": "CORNERSTONE STRATEGIC VALUE FUND INC"
    },
    "RC": {
        "cik": 1527590,
        "title": "Ready Capital Corp"
    },
    "SHO": {
        "cik": 1295810,
        "title": "Sunstone Hotel Investors, Inc."
    },
    "CVII": {
        "cik": 1828248,
        "title": "Churchill Capital Corp VII"
    },
    "SBLK": {
        "cik": 1386716,
        "title": "Star Bulk Carriers Corp."
    },
    "ROAD": {
        "cik": 1718227,
        "title": "Construction Partners, Inc."
    },
    "NS": {
        "cik": 1110805,
        "title": "NuStar Energy L.P."
    },
    "SKYW": {
        "cik": 793733,
        "title": "SKYWEST INC"
    },
    "BORR": {
        "cik": 1715497,
        "title": "Borr Drilling Ltd"
    },
    "BROS": {
        "cik": 1866581,
        "title": "Dutch Bros Inc."
    },
    "INTR": {
        "cik": 1864163,
        "title": "Inter & Co, Inc."
    },
    "SONO": {
        "cik": 1314727,
        "title": "Sonos Inc"
    },
    "FRME": {
        "cik": 712534,
        "title": "FIRST MERCHANTS CORP"
    },
    "DK": {
        "cik": 1694426,
        "title": "Delek US Holdings, Inc."
    },
    "EGO": {
        "cik": 918608,
        "title": "ELDORADO GOLD CORP /FI"
    },
    "PATK": {
        "cik": 76605,
        "title": "PATRICK INDUSTRIES INC"
    },
    "AGYS": {
        "cik": 78749,
        "title": "AGILYSYS INC"
    },
    "RES": {
        "cik": 742278,
        "title": "RPC INC"
    },
    "PEB": {
        "cik": 1474098,
        "title": "Pebblebrook Hotel Trust"
    },
    "GOF": {
        "cik": 1380936,
        "title": "GUGGENHEIM STRATEGIC OPPORTUNITIES FUND"
    },
    "AMEH": {
        "cik": 1083446,
        "title": "Apollo Medical Holdings, Inc."
    },
    "LRN": {
        "cik": 1157408,
        "title": "Stride, Inc."
    },
    "SWI": {
        "cik": 1739942,
        "title": "SolarWinds Corp"
    },
    "OLPX": {
        "cik": 1868726,
        "title": "OLAPLEX HOLDINGS, INC."
    },
    "DKL": {
        "cik": 1552797,
        "title": "Delek Logistics Partners, LP"
    },
    "MRTN": {
        "cik": 799167,
        "title": "MARTEN TRANSPORT LTD"
    },
    "MOMO": {
        "cik": 1610601,
        "title": "Hello Group Inc."
    },
    "PCRX": {
        "cik": 1396814,
        "title": "Pacira BioSciences, Inc."
    },
    "NUV": {
        "cik": 812801,
        "title": "NUVEEN MUNICIPAL VALUE FUND INC"
    },
    "HLMN": {
        "cik": 1822492,
        "title": "Hillman Solutions Corp."
    },
    "TSLX": {
        "cik": 1508655,
        "title": "Sixth Street Specialty Lending, Inc."
    },
    "ALTB": {
        "cik": 1642365,
        "title": "Alpine Auto Brokers Inc."
    },
    "SABR": {
        "cik": 1597033,
        "title": "Sabre Corp"
    },
    "ACDC": {
        "cik": 1881487,
        "title": "ProFrac Holding Corp."
    },
    "SWTX": {
        "cik": 1773427,
        "title": "SpringWorks Therapeutics, Inc."
    },
    "PLAY": {
        "cik": 1525769,
        "title": "Dave & Buster's Entertainment, Inc."
    },
    "CCYC": {
        "cik": 1681769,
        "title": "Clancy Corp"
    },
    "TGH": {
        "cik": 1413159,
        "title": "TEXTAINER GROUP HOLDINGS LTD"
    },
    "RXRX": {
        "cik": 1601830,
        "title": "RECURSION PHARMACEUTICALS, INC."
    },
    "BIGZ": {
        "cik": 1836057,
        "title": "BlackRock Innovation & Growth Term Trust"
    },
    "FWRD": {
        "cik": 912728,
        "title": "FORWARD AIR CORP"
    },
    "VSTO": {
        "cik": 1616318,
        "title": "Vista Outdoor Inc."
    },
    "SPNT": {
        "cik": 1576018,
        "title": "SiriusPoint Ltd"
    },
    "ANDE": {
        "cik": 821026,
        "title": "Andersons, Inc."
    },
    "ACLX": {
        "cik": 1786205,
        "title": "Arcellx, Inc."
    },
    "SGHC": {
        "cik": 1878057,
        "title": "Super Group (SGHC) Ltd"
    },
    "BNRE": {
        "cik": 1837429,
        "title": "Brookfield Reinsurance Ltd."
    },
    "VIR": {
        "cik": 1706431,
        "title": "Vir Biotechnology, Inc."
    },
    "ATEC": {
        "cik": 1350653,
        "title": "Alphatec Holdings, Inc."
    },
    "BRDG": {
        "cik": 1854401,
        "title": "Bridge Investment Group Holdings Inc."
    },
    "ALGT": {
        "cik": 1362468,
        "title": "Allegiant Travel CO"
    },
    "SUPN": {
        "cik": 1356576,
        "title": "SUPERNUS PHARMACEUTICALS, INC."
    },
    "CSGS": {
        "cik": 1005757,
        "title": "CSG SYSTEMS INTERNATIONAL INC"
    },
    "COHU": {
        "cik": 21535,
        "title": "COHU INC"
    },
    "JKS": {
        "cik": 1481513,
        "title": "JinkoSolar Holding Co., Ltd."
    },
    "TLRY": {
        "cik": 1731348,
        "title": "Tilray Brands, Inc."
    },
    "IBTX": {
        "cik": 1564618,
        "title": "Independent Bank Group, Inc."
    },
    "BMEZ": {
        "cik": 1785971,
        "title": "BlackRock Health Sciences Term Trust"
    },
    "PAY": {
        "cik": 1841156,
        "title": "Paymentus Holdings, Inc."
    },
    "MIR": {
        "cik": 1809987,
        "title": "Mirion Technologies, Inc."
    },
    "CMPR": {
        "cik": 1262976,
        "title": "CIMPRESS plc"
    },
    "USA": {
        "cik": 799195,
        "title": "LIBERTY ALL STAR EQUITY FUND"
    },
    "ZIP": {
        "cik": 1617553,
        "title": "ZIPRECRUITER, INC."
    },
    "JBI": {
        "cik": 1839839,
        "title": "Janus International Group, Inc."
    },
    "PRK": {
        "cik": 805676,
        "title": "PARK NATIONAL CORP /OH/"
    },
    "PLUS": {
        "cik": 1022408,
        "title": "EPLUS INC"
    },
    "FLNG": {
        "cik": 1772253,
        "title": "Flex LNG Ltd."
    },
    "HMNTY": {
        "cik": 1915760,
        "title": "Hemnet Group AB/ADR"
    },
    "EVT": {
        "cik": 1253327,
        "title": "EATON VANCE TAX ADVANTAGED DIVIDEND INCOME FUND"
    },
    "DRH": {
        "cik": 1298946,
        "title": "DiamondRock Hospitality Co"
    },
    "CRTO": {
        "cik": 1576427,
        "title": "Criteo S.A."
    },
    "ROIC": {
        "cik": 1407623,
        "title": "RETAIL OPPORTUNITY INVESTMENTS CORP"
    },
    "VGR": {
        "cik": 59440,
        "title": "VECTOR GROUP LTD"
    },
    "HBM": {
        "cik": 1322422,
        "title": "Hudbay Minerals Inc."
    },
    "KAR": {
        "cik": 1395942,
        "title": "OPENLANE, Inc."
    },
    "JACK": {
        "cik": 807882,
        "title": "JACK IN THE BOX INC"
    },
    "HEES": {
        "cik": 1339605,
        "title": "H&E Equipment Services, Inc."
    },
    "DHT": {
        "cik": 1331284,
        "title": "DHT Holdings, Inc."
    },
    "LUMN": {
        "cik": 18926,
        "title": "Lumen Technologies, Inc."
    },
    "NWLI": {
        "cik": 1635984,
        "title": "National Western Life Group, Inc."
    },
    "CAKE": {
        "cik": 887596,
        "title": "CHEESECAKE FACTORY INC"
    },
    "SPNS": {
        "cik": 885740,
        "title": "SAPIENS INTERNATIONAL CORP N V"
    },
    "SMTC": {
        "cik": 88941,
        "title": "SEMTECH CORP"
    },
    "ABCL": {
        "cik": 1703057,
        "title": "AbCellera Biologics Inc."
    },
    "UPBD": {
        "cik": 933036,
        "title": "UPBOUND GROUP, INC."
    },
    "AG": {
        "cik": 1308648,
        "title": "FIRST MAJESTIC SILVER CORP"
    },
    "MBC": {
        "cik": 1941365,
        "title": "MasterBrand, Inc."
    },
    "RNST": {
        "cik": 715072,
        "title": "RENASANT CORP"
    },
    "PRO": {
        "cik": 1392972,
        "title": "PROS Holdings, Inc."
    },
    "SLVM": {
        "cik": 1856485,
        "title": "Sylvamo Corp"
    },
    "PCT": {
        "cik": 1830033,
        "title": "PureCycle Technologies, Inc."
    },
    "BCAT": {
        "cik": 1809541,
        "title": "BlackRock Capital Allocation Term Trust"
    },
    "LGF-A": {
        "cik": 929351,
        "title": "LIONS GATE ENTERTAINMENT CORP /CN/"
    },
    "NMRK": {
        "cik": 1690680,
        "title": "NEWMARK GROUP, INC."
    },
    "PRG": {
        "cik": 1808834,
        "title": "PROG Holdings, Inc."
    },
    "MCY": {
        "cik": 64996,
        "title": "MERCURY GENERAL CORP"
    },
    "TGLS": {
        "cik": 1534675,
        "title": "Tecnoglass Inc."
    },
    "DO": {
        "cik": 949039,
        "title": "DIAMOND OFFSHORE DRILLING, INC."
    },
    "PBAJ": {
        "cik": 745543,
        "title": "PETRO USA, INC."
    },
    "GETY": {
        "cik": 1898496,
        "title": "Getty Images Holdings, Inc."
    },
    "GTBIF": {
        "cik": 1795139,
        "title": "Green Thumb Industries Inc."
    },
    "IMKTA": {
        "cik": 50493,
        "title": "INGLES MARKETS INC"
    },
    "OXM": {
        "cik": 75288,
        "title": "OXFORD INDUSTRIES INC"
    },
    "MSGE": {
        "cik": 1952073,
        "title": "Madison Square Garden Entertainment Corp."
    },
    "GAB": {
        "cik": 794685,
        "title": "GABELLI EQUITY TRUST INC"
    },
    "PGTI": {
        "cik": 1354327,
        "title": "PGT Innovations, Inc."
    },
    "BRP": {
        "cik": 1781755,
        "title": "BRP Group, Inc."
    },
    "AAT": {
        "cik": 1500217,
        "title": "American Assets Trust, Inc."
    },
    "GOOS": {
        "cik": 1690511,
        "title": "Canada Goose Holdings Inc."
    },
    "LTGHY": {
        "cik": 1569963,
        "title": "Life Healthcare Group Holdings Limited/ADR"
    },
    "CPRX": {
        "cik": 1369568,
        "title": "CATALYST PHARMACEUTICALS, INC."
    },
    "UDMY": {
        "cik": 1607939,
        "title": "Udemy, Inc."
    },
    "ZETA": {
        "cik": 1851003,
        "title": "Zeta Global Holdings Corp."
    },
    "SG": {
        "cik": 1477815,
        "title": "Sweetgreen, Inc."
    },
    "FIHL": {
        "cik": 1636639,
        "title": "Fidelis Insurance Holdings Ltd"
    },
    "PERI": {
        "cik": 1338940,
        "title": "Perion Network Ltd."
    },
    "HLF": {
        "cik": 1180262,
        "title": "HERBALIFE LTD."
    },
    "CTOS": {
        "cik": 1709682,
        "title": "Custom Truck One Source, Inc."
    },
    "ENVA": {
        "cik": 1529864,
        "title": "Enova International, Inc."
    },
    "GSBD": {
        "cik": 1572694,
        "title": "Goldman Sachs BDC, Inc."
    },
    "VVX": {
        "cik": 1601548,
        "title": "V2X, Inc."
    },
    "TWKS": {
        "cik": 1866550,
        "title": "Thoughtworks Holding, Inc."
    },
    "JBGS": {
        "cik": 1689796,
        "title": "JBG SMITH Properties"
    },
    "IOVA": {
        "cik": 1425205,
        "title": "IOVANCE BIOTHERAPEUTICS, INC."
    },
    "IDYA": {
        "cik": 1676725,
        "title": "IDEAYA Biosciences, Inc."
    },
    "VSCO": {
        "cik": 1856437,
        "title": "Victoria's Secret & Co."
    },
    "PI": {
        "cik": 1114995,
        "title": "IMPINJ INC"
    },
    "ATSG": {
        "cik": 894081,
        "title": "Air Transport Services Group, Inc."
    },
    "NVEE": {
        "cik": 1532961,
        "title": "NV5 Global, Inc."
    },
    "TGTX": {
        "cik": 1001316,
        "title": "TG THERAPEUTICS, INC."
    },
    "ERII": {
        "cik": 1421517,
        "title": "Energy Recovery, Inc."
    },
    "VCEL": {
        "cik": 887359,
        "title": "Vericel Corp"
    },
    "SATS": {
        "cik": 1415404,
        "title": "EchoStar CORP"
    },
    "ECAT": {
        "cik": 1864843,
        "title": "BlackRock ESG Capital Allocation Term Trust"
    },
    "RLJ": {
        "cik": 1511337,
        "title": "RLJ Lodging Trust"
    },
    "IVT": {
        "cik": 1307748,
        "title": "InvenTrust Properties Corp."
    },
    "BTDR": {
        "cik": 1899123,
        "title": "Bitdeer Technologies Group"
    },
    "SAND": {
        "cik": 1434614,
        "title": "SANDSTORM GOLD LTD"
    },
    "IRWD": {
        "cik": 1446847,
        "title": "IRONWOOD PHARMACEUTICALS INC"
    },
    "CRSR": {
        "cik": 1743759,
        "title": "Corsair Gaming, Inc."
    },
    "WSBC": {
        "cik": 203596,
        "title": "WESBANCO INC"
    },
    "VRNA": {
        "cik": 1657312,
        "title": "Verona Pharma plc"
    },
    "GOGO": {
        "cik": 1537054,
        "title": "Gogo Inc."
    },
    "USPH": {
        "cik": 885978,
        "title": "U S PHYSICAL THERAPY INC /NV"
    },
    "NBTB": {
        "cik": 790359,
        "title": "NBT BANCORP INC"
    },
    "UEC": {
        "cik": 1334933,
        "title": "URANIUM ENERGY CORP"
    },
    "TH": {
        "cik": 1712189,
        "title": "Target Hospitality Corp."
    },
    "LOMA": {
        "cik": 1711375,
        "title": "Loma Negra Compania Industrial Argentina Sociedad Anonima"
    },
    "AHCO": {
        "cik": 1725255,
        "title": "AdaptHealth Corp."
    },
    "TTMI": {
        "cik": 1116942,
        "title": "TTM TECHNOLOGIES INC"
    },
    "AHL-PC": {
        "cik": 1267395,
        "title": "ASPEN INSURANCE HOLDINGS LTD"
    },
    "GTY": {
        "cik": 1052752,
        "title": "GETTY REALTY CORP /MD/"
    },
    "CODI": {
        "cik": 1345126,
        "title": "Compass Diversified Holdings"
    },
    "OSCR": {
        "cik": 1568651,
        "title": "Oscar Health, Inc."
    },
    "OCSL": {
        "cik": 1414932,
        "title": "Oaktree Specialty Lending Corp"
    },
    "ALKT": {
        "cik": 1529274,
        "title": "ALKAMI TECHNOLOGY, INC."
    },
    "SSTK": {
        "cik": 1549346,
        "title": "Shutterstock, Inc."
    },
    "ZIM": {
        "cik": 1654126,
        "title": "ZIM Integrated Shipping Services Ltd."
    },
    "NAC": {
        "cik": 1074952,
        "title": "Nuveen California Quality Municipal Income Fund"
    },
    "NOVA": {
        "cik": 1772695,
        "title": "Sunnova Energy International Inc."
    },
    "AGIO": {
        "cik": 1439222,
        "title": "AGIOS PHARMACEUTICALS, INC."
    },
    "IE": {
        "cik": 1879016,
        "title": "Ivanhoe Electric Inc."
    },
    "BANR": {
        "cik": 946673,
        "title": "BANNER CORP"
    },
    "TFIN": {
        "cik": 1539638,
        "title": "Triumph Financial, Inc."
    },
    "ULCC": {
        "cik": 1670076,
        "title": "Frontier Group Holdings, Inc."
    },
    "RVT": {
        "cik": 804116,
        "title": "ROYCE VALUE TRUST, INC."
    },
    "KN": {
        "cik": 1587523,
        "title": "Knowles Corp"
    },
    "LOB": {
        "cik": 1462120,
        "title": "Live Oak Bancshares, Inc."
    },
    "VECO": {
        "cik": 103145,
        "title": "VEECO INSTRUMENTS INC"
    },
    "RADI": {
        "cik": 1810739,
        "title": "Radius Global Infrastructure, Inc."
    },
    "ADUS": {
        "cik": 1468328,
        "title": "Addus HomeCare Corp"
    },
    "TY": {
        "cik": 99614,
        "title": "TRI-CONTINENTAL CORP"
    },
    "TNC": {
        "cik": 97134,
        "title": "TENNANT CO"
    },
    "RQI": {
        "cik": 1157842,
        "title": "COHEN & STEERS QUALITY INCOME REALTY FUND INC"
    },
    "EFSC": {
        "cik": 1025835,
        "title": "ENTERPRISE FINANCIAL SERVICES CORP"
    },
    "EAT": {
        "cik": 703351,
        "title": "BRINKER INTERNATIONAL, INC"
    },
    "COCO": {
        "cik": 1482981,
        "title": "Vita Coco Company, Inc."
    },
    "FBK": {
        "cik": 1649749,
        "title": "FB Financial Corp"
    },
    "UCTT": {
        "cik": 1275014,
        "title": "Ultra Clean Holdings, Inc."
    },
    "TNK": {
        "cik": 1419945,
        "title": "TEEKAY TANKERS LTD."
    },
    "RVNC": {
        "cik": 1479290,
        "title": "Revance Therapeutics, Inc."
    },
    "AKR": {
        "cik": 899629,
        "title": "ACADIA REALTY TRUST"
    },
    "BDJ": {
        "cik": 1332283,
        "title": "BlackRock Enhanced Equity Dividend Trust"
    },
    "HIMS": {
        "cik": 1773751,
        "title": "Hims & Hers Health, Inc."
    },
    "RYTM": {
        "cik": 1649904,
        "title": "RHYTHM PHARMACEUTICALS, INC."
    },
    "EYE": {
        "cik": 1710155,
        "title": "National Vision Holdings, Inc."
    },
    "GOGL": {
        "cik": 1029145,
        "title": "Golden Ocean Group Ltd"
    },
    "HNI": {
        "cik": 48287,
        "title": "HNI CORP"
    },
    "TRMK": {
        "cik": 36146,
        "title": "TRUSTMARK CORP"
    },
    "GCMG": {
        "cik": 1819796,
        "title": "GCM Grosvenor Inc."
    },
    "ORLA": {
        "cik": 1680056,
        "title": "Orla Mining Ltd."
    },
    "PTVE": {
        "cik": 1527508,
        "title": "Pactiv Evergreen Inc."
    },
    "MLNK": {
        "cik": 1834494,
        "title": "MeridianLink, Inc."
    },
    "HE": {
        "cik": 354707,
        "title": "HAWAIIAN ELECTRIC INDUSTRIES INC"
    },
    "WRBY": {
        "cik": 1504776,
        "title": "Warby Parker Inc."
    },
    "OFG": {
        "cik": 1030469,
        "title": "OFG BANCORP"
    },
    "NWN": {
        "cik": 1733998,
        "title": "Northwest Natural Holding Co"
    },
    "NAPA": {
        "cik": 1835256,
        "title": "Duckhorn Portfolio, Inc."
    },
    "CLDX": {
        "cik": 744218,
        "title": "Celldex Therapeutics, Inc."
    },
    "NVTS": {
        "cik": 1821769,
        "title": "Navitas Semiconductor Corp"
    },
    "BTT": {
        "cik": 1528437,
        "title": "BlackRock Municipal 2030 Target Term Trust"
    },
    "CNNE": {
        "cik": 1704720,
        "title": "Cannae Holdings, Inc."
    },
    "KRP": {
        "cik": 1657788,
        "title": "Kimbell Royalty Partners, LP"
    },
    "PHR": {
        "cik": 1412408,
        "title": "Phreesia, Inc."
    },
    "ECX": {
        "cik": 1861974,
        "title": "ECARX Holdings Inc."
    },
    "CLBT": {
        "cik": 1854587,
        "title": "Cellebrite DI Ltd."
    },
    "FINV": {
        "cik": 1691445,
        "title": "FinVolution Group"
    },
    "CMTG": {
        "cik": 1666291,
        "title": "Claros Mortgage Trust, Inc."
    },
    "MYGN": {
        "cik": 899923,
        "title": "MYRIAD GENETICS INC"
    },
    "EQX": {
        "cik": 1756607,
        "title": "Equinox Gold Corp."
    },
    "EPAC": {
        "cik": 6955,
        "title": "ENERPAC TOOL GROUP CORP"
    },
    "ARVN": {
        "cik": 1655759,
        "title": "ARVINAS, INC."
    },
    "COMP": {
        "cik": 1563190,
        "title": "Compass, Inc."
    },
    "NWBI": {
        "cik": 1471265,
        "title": "Northwest Bancshares, Inc."
    },
    "VRTS": {
        "cik": 883237,
        "title": "VIRTUS INVESTMENT PARTNERS, INC."
    },
    "HLX": {
        "cik": 866829,
        "title": "HELIX ENERGY SOLUTIONS GROUP INC"
    },
    "VKTX": {
        "cik": 1607678,
        "title": "Viking Therapeutics, Inc."
    },
    "PX": {
        "cik": 1841968,
        "title": "P10, Inc."
    },
    "AMLX": {
        "cik": 1658551,
        "title": "Amylyx Pharmaceuticals, Inc."
    },
    "SEAT": {
        "cik": 1856031,
        "title": "Vivid Seats Inc."
    },
    "NTB": {
        "cik": 1653242,
        "title": "Bank of N.T. Butterfield & Son Ltd"
    },
    "DCBO": {
        "cik": 1829959,
        "title": "Docebo Inc."
    },
    "BCRX": {
        "cik": 882796,
        "title": "BIOCRYST PHARMACEUTICALS INC"
    },
    "PLAB": {
        "cik": 810136,
        "title": "PHOTRONICS INC"
    },
    "CNXN": {
        "cik": 1050377,
        "title": "PC CONNECTION INC"
    },
    "IESC": {
        "cik": 1048268,
        "title": "IES Holdings, Inc."
    },
    "ARI": {
        "cik": 1467760,
        "title": "Apollo Commercial Real Estate Finance, Inc."
    },
    "ESTA": {
        "cik": 1688757,
        "title": "ESTABLISHMENT LABS HOLDINGS INC."
    },
    "MLKN": {
        "cik": 66382,
        "title": "MILLERKNOLL, INC."
    },
    "RCUS": {
        "cik": 1724521,
        "title": "Arcus Biosciences, Inc."
    },
    "NAAS": {
        "cik": 1712178,
        "title": "NaaS Technology Inc."
    },
    "FOR": {
        "cik": 1406587,
        "title": "Forestar Group Inc."
    },
    "MDRX": {
        "cik": 1124804,
        "title": "Veradigm Inc."
    },
    "ARHS": {
        "cik": 1875444,
        "title": "Arhaus, Inc."
    },
    "TARO": {
        "cik": 906338,
        "title": "TARO PHARMACEUTICAL INDUSTRIES LTD"
    },
    "KGS": {
        "cik": 1767042,
        "title": "Kodiak Gas Services, Inc."
    },
    "DAC": {
        "cik": 1369241,
        "title": "Danaos Corp"
    },
    "LKFN": {
        "cik": 721994,
        "title": "LAKELAND FINANCIAL CORP"
    },
    "ATUS": {
        "cik": 1702780,
        "title": "Altice USA, Inc."
    },
    "ETV": {
        "cik": 1322436,
        "title": "Eaton Vance Tax-Managed Buy-Write Opportunities Fund"
    },
    "PRCT": {
        "cik": 1588978,
        "title": "PROCEPT BioRobotics Corp"
    },
    "CHCO": {
        "cik": 726854,
        "title": "CITY HOLDING CO"
    },
    "STER": {
        "cik": 1645070,
        "title": "Sterling Check Corp."
    },
    "MSEX": {
        "cik": 66004,
        "title": "MIDDLESEX WATER CO"
    },
    "PDO": {
        "cik": 1798618,
        "title": "PIMCO Dynamic Income Opportunities Fund"
    },
    "AUPH": {
        "cik": 1600620,
        "title": "Aurinia Pharmaceuticals Inc."
    },
    "SMMT": {
        "cik": 1599298,
        "title": "Summit Therapeutics Inc."
    },
    "DFIN": {
        "cik": 1669811,
        "title": "Donnelley Financial Solutions, Inc."
    },
    "MNTK": {
        "cik": 1826600,
        "title": "Montauk Renewables, Inc."
    },
    "ZUO": {
        "cik": 1423774,
        "title": "ZUORA INC"
    },
    "SYBT": {
        "cik": 835324,
        "title": "Stock Yards Bancorp, Inc."
    },
    "AGTI": {
        "cik": 1749704,
        "title": "AGILITI, INC. DE"
    },
    "CTS": {
        "cik": 26058,
        "title": "CTS CORP"
    },
    "AFYA": {
        "cik": 1771007,
        "title": "Afya Ltd"
    },
    "SFL": {
        "cik": 1289877,
        "title": "SFL Corp Ltd."
    },
    "PGY": {
        "cik": 1883085,
        "title": "Pagaya Technologies Ltd."
    },
    "XNCR": {
        "cik": 1326732,
        "title": "Xencor Inc"
    },
    "WKC": {
        "cik": 789460,
        "title": "WORLD KINECT CORP"
    },
    "BXMX": {
        "cik": 1298699,
        "title": "Nuveen S&P 500 BuyWrite Income Fund"
    },
    "ETWO": {
        "cik": 1800347,
        "title": "E2open Parent Holdings, Inc."
    },
    "SCHL": {
        "cik": 866729,
        "title": "SCHOLASTIC CORP"
    },
    "SHCO": {
        "cik": 1846510,
        "title": "Soho House & Co Inc."
    },
    "CLMT": {
        "cik": 1340122,
        "title": "Calumet Specialty Products Partners, L.P."
    },
    "TTEC": {
        "cik": 1013880,
        "title": "TTEC Holdings, Inc."
    },
    "NG": {
        "cik": 1173420,
        "title": "NOVAGOLD RESOURCES INC"
    },
    "SVC": {
        "cik": 945394,
        "title": "Service Properties Trust"
    },
    "FCF": {
        "cik": 712537,
        "title": "FIRST COMMONWEALTH FINANCIAL CORP /PA/"
    },
    "AMPL": {
        "cik": 1866692,
        "title": "Amplitude, Inc."
    },
    "BBUC": {
        "cik": 1871130,
        "title": "Brookfield Business Corp"
    },
    "BSTZ": {
        "cik": 1768666,
        "title": "BlackRock Science & Technology Term Trust"
    },
    "ELME": {
        "cik": 104894,
        "title": "Elme Communities"
    },
    "BHVN": {
        "cik": 1935979,
        "title": "Biohaven Ltd."
    },
    "NISUY": {
        "cik": 110095,
        "title": "NIPPON SUISAN KAISHA LTD /ADR/"
    },
    "RILY": {
        "cik": 1464790,
        "title": "B. Riley Financial, Inc."
    },
    "GENI": {
        "cik": 1834489,
        "title": "Genius Sports Ltd"
    },
    "GERN": {
        "cik": 886744,
        "title": "GERON CORP"
    },
    "GSG": {
        "cik": 1332174,
        "title": "iShares S&P GSCI Commodity-Indexed Trust"
    },
    "HTLF": {
        "cik": 920112,
        "title": "HEARTLAND FINANCIAL USA INC"
    },
    "LNN": {
        "cik": 836157,
        "title": "LINDSAY CORP"
    },
    "OPK": {
        "cik": 944809,
        "title": "OPKO HEALTH, INC."
    },
    "OPRA": {
        "cik": 1737450,
        "title": "Opera Ltd"
    },
    "LTC": {
        "cik": 887905,
        "title": "LTC PROPERTIES INC"
    },
    "SAFE": {
        "cik": 1095651,
        "title": "Safehold Inc."
    },
    "GBX": {
        "cik": 923120,
        "title": "GREENBRIER COMPANIES INC"
    },
    "LZB": {
        "cik": 57131,
        "title": "LA-Z-BOY INC"
    },
    "DADA": {
        "cik": 1793862,
        "title": "Dada Nexus Ltd"
    },
    "LADR": {
        "cik": 1577670,
        "title": "Ladder Capital Corp"
    },
    "STEW": {
        "cik": 102426,
        "title": "SRH Total Return Fund, Inc."
    },
    "RLAY": {
        "cik": 1812364,
        "title": "Relay Therapeutics, Inc."
    },
    "KEN": {
        "cik": 1611005,
        "title": "Kenon Holdings Ltd."
    },
    "JPS": {
        "cik": 1176433,
        "title": "Nuveen Preferred & Income Securities Fund"
    },
    "PDFS": {
        "cik": 1120914,
        "title": "PDF SOLUTIONS INC"
    },
    "ALEX": {
        "cik": 1545654,
        "title": "Alexander & Baldwin, Inc."
    },
    "PLMR": {
        "cik": 1761312,
        "title": "Palomar Holdings, Inc."
    },
    "CMRE": {
        "cik": 1503584,
        "title": "Costamare Inc."
    },
    "LNZA": {
        "cik": 1843724,
        "title": "LanzaTech Global, Inc."
    },
    "MATW": {
        "cik": 63296,
        "title": "MATTHEWS INTERNATIONAL CORP"
    },
    "MNKD": {
        "cik": 899460,
        "title": "MANNKIND CORP"
    },
    "RCKT": {
        "cik": 1281895,
        "title": "ROCKET PHARMACEUTICALS, INC."
    },
    "NMFC": {
        "cik": 1496099,
        "title": "New Mountain Finance Corp"
    },
    "CIM": {
        "cik": 1409493,
        "title": "CHIMERA INVESTMENT CORP"
    },
    "CASH": {
        "cik": 907471,
        "title": "PATHWARD FINANCIAL, INC."
    },
    "XHR": {
        "cik": 1616000,
        "title": "Xenia Hotels & Resorts, Inc."
    },
    "HYT": {
        "cik": 1222401,
        "title": "BLACKROCK CORPORATE HIGH YIELD FUND, INC."
    },
    "FDP": {
        "cik": 1047340,
        "title": "FRESH DEL MONTE PRODUCE INC"
    },
    "AVPT": {
        "cik": 1777921,
        "title": "AvePoint, Inc."
    },
    "MBIN": {
        "cik": 1629019,
        "title": "Merchants Bancorp"
    },
    "SNDX": {
        "cik": 1395937,
        "title": "Syndax Pharmaceuticals Inc"
    },
    "MCRI": {
        "cik": 907242,
        "title": "MONARCH CASINO & RESORT INC"
    },
    "CARS": {
        "cik": 1683606,
        "title": "Cars.com Inc."
    },
    "UFPT": {
        "cik": 914156,
        "title": "UFP TECHNOLOGIES INC"
    },
    "MSC": {
        "cik": 1713334,
        "title": "STUDIO CITY INTERNATIONAL HOLDINGS Ltd"
    },
    "HSAI": {
        "cik": 1861737,
        "title": "Hesai Group"
    },
    "OEC": {
        "cik": 1609804,
        "title": "Orion S.A."
    },
    "GIC": {
        "cik": 945114,
        "title": "GLOBAL INDUSTRIAL Co"
    },
    "PFS": {
        "cik": 1178970,
        "title": "PROVIDENT FINANCIAL SERVICES INC"
    },
    "EVGO": {
        "cik": 1821159,
        "title": "EVgo Inc."
    },
    "SPHR": {
        "cik": 1795250,
        "title": "Sphere Entertainment Co."
    },
    "OPAL": {
        "cik": 1842279,
        "title": "OPAL Fuels Inc."
    },
    "MD": {
        "cik": 893949,
        "title": "Pediatrix Medical Group, Inc."
    },
    "WINA": {
        "cik": 908315,
        "title": "WINMARK CORP"
    },
    "SPWR": {
        "cik": 867773,
        "title": "SUNPOWER CORP"
    },
    "FBNC": {
        "cik": 811589,
        "title": "FIRST BANCORP /NC/"
    },
    "JELD": {
        "cik": 1674335,
        "title": "JELD-WEN Holding, Inc."
    },
    "SEMR": {
        "cik": 1831840,
        "title": "SEMrush Holdings, Inc."
    },
    "ANIP": {
        "cik": 1023024,
        "title": "ANI PHARMACEUTICALS INC"
    },
    "LESL": {
        "cik": 1821806,
        "title": "Leslie's, Inc."
    },
    "TWO": {
        "cik": 1465740,
        "title": "TWO HARBORS INVESTMENT CORP."
    },
    "ETG": {
        "cik": 1270523,
        "title": "EATON VANCE TAX ADVANTAGED GLOBAL DIVIDEND INCOME FUND"
    },
    "BLDP": {
        "cik": 1453015,
        "title": "Ballard Power Systems Inc."
    },
    "LMAT": {
        "cik": 1158895,
        "title": "LEMAITRE VASCULAR INC"
    },
    "CMP": {
        "cik": 1227654,
        "title": "COMPASS MINERALS INTERNATIONAL INC"
    },
    "APGE": {
        "cik": 1974640,
        "title": "Apogee Therapeutics, Inc."
    },
    "MMI": {
        "cik": 1578732,
        "title": "Marcus & Millichap, Inc."
    },
    "KFRC": {
        "cik": 930420,
        "title": "KFORCE INC"
    },
    "IRON": {
        "cik": 1816736,
        "title": "Disc Medicine, Inc."
    },
    "STC": {
        "cik": 94344,
        "title": "STEWART INFORMATION SERVICES CORP"
    },
    "DAWN": {
        "cik": 1845337,
        "title": "Day One Biopharmaceuticals, Inc."
    },
    "PHIN": {
        "cik": 1968915,
        "title": "PHINIA INC."
    },
    "UNIT": {
        "cik": 1620280,
        "title": "Uniti Group Inc."
    },
    "TRUP": {
        "cik": 1371285,
        "title": "TRUPANION, INC."
    },
    "DSL": {
        "cik": 1566388,
        "title": "DoubleLine Income Solutions Fund"
    },
    "ANGI": {
        "cik": 1705110,
        "title": "Angi Inc."
    },
    "CGAU": {
        "cik": 1854640,
        "title": "Centerra Gold Inc."
    },
    "NBHC": {
        "cik": 1475841,
        "title": "National Bank Holdings Corp"
    },
    "USNA": {
        "cik": 896264,
        "title": "USANA HEALTH SCIENCES INC"
    },
    "VZIO": {
        "cik": 1835591,
        "title": "Vizio Holding Corp."
    },
    "ETNB": {
        "cik": 1785173,
        "title": "89bio, Inc."
    },
    "STEL": {
        "cik": 1473844,
        "title": "Stellar Bancorp, Inc."
    },
    "NUS": {
        "cik": 1021561,
        "title": "NU SKIN ENTERPRISES, INC."
    },
    "WABC": {
        "cik": 311094,
        "title": "WESTAMERICA BANCORPORATION"
    },
    "CBAY": {
        "cik": 1042074,
        "title": "CymaBay Therapeutics, Inc."
    },
    "HWKN": {
        "cik": 46250,
        "title": "HAWKINS INC"
    },
    "UTZ": {
        "cik": 1739566,
        "title": "Utz Brands, Inc."
    },
    "KNSA": {
        "cik": 1730430,
        "title": "Kiniksa Pharmaceuticals, Ltd."
    },
    "OMI": {
        "cik": 75252,
        "title": "OWENS & MINOR INC/VA/"
    },
    "DNN": {
        "cik": 1063259,
        "title": "DENISON MINES CORP."
    },
    "GEL": {
        "cik": 1022321,
        "title": "GENESIS ENERGY LP"
    },
    "CCF": {
        "cik": 830524,
        "title": "CHASE CORP"
    },
    "KC": {
        "cik": 1795589,
        "title": "Kingsoft Cloud Holdings Ltd"
    },
    "HTLD": {
        "cik": 799233,
        "title": "HEARTLAND EXPRESS INC"
    },
    "MEG": {
        "cik": 1643615,
        "title": "Montrose Environmental Group, Inc."
    },
    "EVRI": {
        "cik": 1318568,
        "title": "Everi Holdings Inc."
    },
    "PRME": {
        "cik": 1894562,
        "title": "Prime Medicine, Inc."
    },
    "KALU": {
        "cik": 811596,
        "title": "KAISER ALUMINUM CORP"
    },
    "CHGG": {
        "cik": 1364954,
        "title": "CHEGG, INC"
    },
    "AMRX": {
        "cik": 1723128,
        "title": "Amneal Pharmaceuticals, Inc."
    },
    "BFS": {
        "cik": 907254,
        "title": "SAUL CENTERS, INC."
    },
    "UNFI": {
        "cik": 1020859,
        "title": "UNITED NATURAL FOODS INC"
    },
    "SGH": {
        "cik": 1616533,
        "title": "SMART Global Holdings, Inc."
    },
    "DNOW": {
        "cik": 1599617,
        "title": "NOW Inc."
    },
    "EDN": {
        "cik": 1395213,
        "title": "EDENOR"
    },
    "JBSS": {
        "cik": 880117,
        "title": "SANFILIPPO JOHN B & SON INC"
    },
    "TCBK": {
        "cik": 356171,
        "title": "TRICO BANCSHARES /"
    },
    "SAGE": {
        "cik": 1597553,
        "title": "Sage Therapeutics, Inc."
    },
    "DCPH": {
        "cik": 1654151,
        "title": "Deciphera Pharmaceuticals, Inc."
    },
    "HLIT": {
        "cik": 851310,
        "title": "HARMONIC INC"
    },
    "CUBI": {
        "cik": 1488813,
        "title": "Customers Bancorp, Inc."
    },
    "KYN": {
        "cik": 1293613,
        "title": "Kayne Anderson Energy Infrastructure Fund, Inc."
    },
    "AMWD": {
        "cik": 794619,
        "title": "AMERICAN WOODMARK CORP"
    },
    "AZZ": {
        "cik": 8947,
        "title": "AZZ INC"
    },
    "ASTE": {
        "cik": 792987,
        "title": "ASTEC INDUSTRIES INC"
    },
    "CXW": {
        "cik": 1070985,
        "title": "CoreCivic, Inc."
    },
    "AVID": {
        "cik": 896841,
        "title": "AVID TECHNOLOGY, INC."
    },
    "IRS": {
        "cik": 933267,
        "title": "IRSA INVESTMENTS & REPRESENTATIONS INC"
    },
    "AIV": {
        "cik": 922864,
        "title": "APARTMENT INVESTMENT & MANAGEMENT CO"
    },
    "UVV": {
        "cik": 102037,
        "title": "UNIVERSAL CORP /VA/"
    },
    "AGRO": {
        "cik": 1499505,
        "title": "Adecoagro S.A."
    },
    "ROVR": {
        "cik": 1826018,
        "title": "ROVER GROUP, INC."
    },
    "DSGR": {
        "cik": 703604,
        "title": "Distribution Solutions Group, Inc."
    },
    "BBU": {
        "cik": 1654795,
        "title": "Brookfield Business Partners L.P."
    },
    "HOPE": {
        "cik": 1128361,
        "title": "HOPE BANCORP INC"
    },
    "ALHC": {
        "cik": 1832466,
        "title": "Alignment Healthcare, Inc."
    },
    "HMN": {
        "cik": 850141,
        "title": "HORACE MANN EDUCATORS CORP /DE/"
    },
    "DOLE": {
        "cik": 1857475,
        "title": "Dole plc"
    },
    "MEI": {
        "cik": 65270,
        "title": "METHODE ELECTRONICS INC"
    },
    "AEHR": {
        "cik": 1040470,
        "title": "AEHR TEST SYSTEMS"
    },
    "NFJ": {
        "cik": 1260563,
        "title": "Virtus Dividend, Interest & Premium Strategy Fund"
    },
    "VEON": {
        "cik": 1468091,
        "title": "VEON Ltd."
    },
    "OSTK": {
        "cik": 1130713,
        "title": "OVERSTOCK.COM, INC"
    },
    "LGND": {
        "cik": 886163,
        "title": "LIGAND PHARMACEUTICALS INC"
    },
    "REPL": {
        "cik": 1737953,
        "title": "Replimune Group, Inc."
    },
    "PUMP": {
        "cik": 1680247,
        "title": "ProPetro Holding Corp."
    },
    "LIFX": {
        "cik": 1581760,
        "title": "Life360, Inc."
    },
    "VLRS": {
        "cik": 1520504,
        "title": "Controladora Vuela Compania de Aviacion, S.A.B. de C.V."
    },
    "SHEN": {
        "cik": 354963,
        "title": "SHENANDOAH TELECOMMUNICATIONS CO/VA/"
    },
    "CWH": {
        "cik": 1669779,
        "title": "Camping World Holdings, Inc."
    },
    "FORTY": {
        "cik": 1045986,
        "title": "FORMULA SYSTEMS (1985) LTD"
    },
    "CIR": {
        "cik": 1091883,
        "title": "CIRCOR INTERNATIONAL INC"
    },
    "BUSE": {
        "cik": 314489,
        "title": "FIRST BUSEY CORP /NV/"
    },
    "CHEF": {
        "cik": 1517175,
        "title": "Chefs' Warehouse, Inc."
    },
    "USLM": {
        "cik": 82020,
        "title": "UNITED STATES LIME & MINERALS INC"
    },
    "GNL": {
        "cik": 1526113,
        "title": "Global Net Lease, Inc."
    },
    "DMLP": {
        "cik": 1172358,
        "title": "DORCHESTER MINERALS, L.P."
    },
    "RVLV": {
        "cik": 1746618,
        "title": "Revolve Group, Inc."
    },
    "QQQX": {
        "cik": 1608741,
        "title": "Nuveen NASDAQ 100 Dynamic Overwrite Fund"
    },
    "JMKJ": {
        "cik": 1624140,
        "title": "Nine Alliance Science & Technology Group"
    },
    "NMZ": {
        "cik": 1266585,
        "title": "NUVEEN MUNICIPAL HIGH INCOME OPPORTUNITY FUND"
    },
    "MAG": {
        "cik": 1230992,
        "title": "MAG SILVER CORP"
    },
    "KYMR": {
        "cik": 1815442,
        "title": "Kymera Therapeutics, Inc."
    },
    "CLB": {
        "cik": 1958086,
        "title": "Core Laboratories Inc. /DE/"
    },
    "PTGX": {
        "cik": 1377121,
        "title": "Protagonist Therapeutics, Inc"
    },
    "MBUU": {
        "cik": 1590976,
        "title": "MALIBU BOATS, INC."
    },
    "NTST": {
        "cik": 1798100,
        "title": "NETSTREIT Corp."
    },
    "OSW": {
        "cik": 1758488,
        "title": "ONESPAWORLD HOLDINGS Ltd"
    },
    "TWST": {
        "cik": 1581280,
        "title": "Twist Bioscience Corp"
    },
    "NIC": {
        "cik": 1174850,
        "title": "NICOLET BANKSHARES INC"
    },
    "PLYA": {
        "cik": 1692412,
        "title": "Playa Hotels & Resorts N.V."
    },
    "GPCR": {
        "cik": 1888886,
        "title": "Structure Therapeutics Inc."
    },
    "DGII": {
        "cik": 854775,
        "title": "DIGI INTERNATIONAL INC"
    },
    "ECVT": {
        "cik": 1708035,
        "title": "Ecovyst Inc."
    },
    "MGNI": {
        "cik": 1595974,
        "title": "MAGNITE, INC."
    },
    "STBA": {
        "cik": 719220,
        "title": "S&T BANCORP INC"
    },
    "HHRS": {
        "cik": 1946425,
        "title": "Hammerhead Energy Inc."
    },
    "CTKB": {
        "cik": 1831915,
        "title": "Cytek Biosciences, Inc."
    },
    "NKLA": {
        "cik": 1731289,
        "title": "Nikola Corp"
    },
    "AZUL": {
        "cik": 1432364,
        "title": "AZUL SA"
    },
    "ECPG": {
        "cik": 1084961,
        "title": "ENCORE CAPITAL GROUP INC"
    },
    "PGRE": {
        "cik": 1605607,
        "title": "Paramount Group, Inc."
    },
    "HCCI": {
        "cik": 1403431,
        "title": "Heritage-Crystal Clean, Inc."
    },
    "UUUU": {
        "cik": 1385849,
        "title": "ENERGY FUELS INC"
    },
    "SRCE": {
        "cik": 34782,
        "title": "1ST SOURCE CORP"
    },
    "DH": {
        "cik": 1861795,
        "title": "Definitive Healthcare Corp."
    },
    "PMT": {
        "cik": 1464423,
        "title": "PennyMac Mortgage Investment Trust"
    },
    "FNA": {
        "cik": 1531978,
        "title": "Paragon 28, Inc."
    },
    "EWCZ": {
        "cik": 1856236,
        "title": "European Wax Center, Inc."
    },
    "HAIN": {
        "cik": 910406,
        "title": "HAIN CELESTIAL GROUP INC"
    },
    "EH": {
        "cik": 1759783,
        "title": "EHang Holdings Ltd"
    },
    "FTCH": {
        "cik": 1740915,
        "title": "Farfetch Ltd"
    },
    "CBD": {
        "cik": 1038572,
        "title": "BRAZILIAN DISTRIBUTION CO COMPANHIA BRASILEIRA DE DISTR CBD"
    },
    "APOG": {
        "cik": 6845,
        "title": "APOGEE ENTERPRISES, INC."
    },
    "KRNT": {
        "cik": 1625791,
        "title": "Kornit Digital Ltd."
    },
    "BST": {
        "cik": 1616678,
        "title": "BlackRock Science & Technology Trust"
    },
    "GDEV": {
        "cik": 1848739,
        "title": "GDEV Inc."
    },
    "EQRX": {
        "cik": 1843762,
        "title": "EQRx, Inc."
    },
    "MRUS": {
        "cik": 1651311,
        "title": "Merus N.V."
    },
    "MOR": {
        "cik": 1340243,
        "title": "MorphoSys AG"
    },
    "ATEN": {
        "cik": 1580808,
        "title": "A10 Networks, Inc."
    },
    "NXGN": {
        "cik": 708818,
        "title": "NEXTGEN HEALTHCARE, INC."
    },
    "VTLE": {
        "cik": 1528129,
        "title": "Vital Energy, Inc."
    },
    "SBH": {
        "cik": 1368458,
        "title": "Sally Beauty Holdings, Inc."
    },
    "KROS": {
        "cik": 1664710,
        "title": "Keros Therapeutics, Inc."
    },
    "MPLN": {
        "cik": 1793229,
        "title": "MultiPlan Corp"
    },
    "EVV": {
        "cik": 1222922,
        "title": "EATON VANCE LTD DURATION INCOME FUND"
    },
    "GLP": {
        "cik": 1323468,
        "title": "GLOBAL PARTNERS LP"
    },
    "FBRT": {
        "cik": 1562528,
        "title": "Franklin BSP Realty Trust, Inc."
    },
    "XPOF": {
        "cik": 1802156,
        "title": "Xponential Fitness, Inc."
    },
    "HIMX": {
        "cik": 1342338,
        "title": "Himax Technologies, Inc."
    },
    "PRDO": {
        "cik": 1046568,
        "title": "PERDOCEO EDUCATION Corp"
    },
    "FIGS": {
        "cik": 1846576,
        "title": "FIGS, Inc."
    },
    "SANA": {
        "cik": 1770121,
        "title": "Sana Biotechnology, Inc."
    },
    "MNRO": {
        "cik": 876427,
        "title": "MONRO, INC."
    },
    "FWRG": {
        "cik": 1789940,
        "title": "First Watch Restaurant Group, Inc."
    },
    "CMCO": {
        "cik": 1005229,
        "title": "COLUMBUS MCKINNON CORP"
    },
    "WT": {
        "cik": 880631,
        "title": "WisdomTree, Inc."
    },
    "NHC": {
        "cik": 1047335,
        "title": "NATIONAL HEALTHCARE CORP"
    },
    "GSM": {
        "cik": 1639877,
        "title": "Ferroglobe PLC"
    },
    "GRNT": {
        "cik": 1928446,
        "title": "Granite Ridge Resources, Inc."
    },
    "IMAX": {
        "cik": 921582,
        "title": "IMAX CORP"
    },
    "YEXT": {
        "cik": 1614178,
        "title": "Yext, Inc."
    },
    "FSCO": {
        "cik": 1568194,
        "title": "FS Credit Opportunities Corp."
    },
    "TRS": {
        "cik": 842633,
        "title": "TRIMAS CORP"
    },
    "ARIS": {
        "cik": 1865187,
        "title": "Aris Water Solutions, Inc."
    },
    "MODN": {
        "cik": 1118417,
        "title": "MODEL N, INC."
    },
    "ADEA": {
        "cik": 1803696,
        "title": "Adeia Inc."
    },
    "EIG": {
        "cik": 1379041,
        "title": "Employers Holdings, Inc."
    },
    "PBT": {
        "cik": 319654,
        "title": "PERMIAN BASIN ROYALTY TRUST"
    },
    "PAR": {
        "cik": 708821,
        "title": "PAR TECHNOLOGY CORP"
    },
    "NRC": {
        "cik": 70487,
        "title": "NATIONAL RESEARCH CORP"
    },
    "WNC": {
        "cik": 879526,
        "title": "WABASH NATIONAL Corp"
    },
    "NBR": {
        "cik": 1163739,
        "title": "NABORS INDUSTRIES LTD"
    },
    "IAG": {
        "cik": 1203464,
        "title": "IAMGOLD CORP"
    },
    "ARGO": {
        "cik": 1091748,
        "title": "Argo Group International Holdings, Ltd."
    },
    "ARR": {
        "cik": 1428205,
        "title": "Armour Residential REIT, Inc."
    },
    "OLO": {
        "cik": 1431695,
        "title": "Olo Inc."
    },
    "GB": {
        "cik": 1799983,
        "title": "Global Blue Group Holding AG"
    },
    "LZM": {
        "cik": 1958217,
        "title": "Lifezone Metals Ltd"
    },
    "MFA": {
        "cik": 1055160,
        "title": "MFA FINANCIAL, INC."
    },
    "TBLA": {
        "cik": 1840502,
        "title": "Taboola.com Ltd."
    },
    "BIOGY": {
        "cik": 1572957,
        "title": "BioGaia AB/ADR"
    },
    "VBTX": {
        "cik": 1501570,
        "title": "Veritex Holdings, Inc."
    },
    "SAFT": {
        "cik": 1172052,
        "title": "SAFETY INSURANCE GROUP INC"
    },
    "RYI": {
        "cik": 1481582,
        "title": "Ryerson Holding Corp"
    },
    "GES": {
        "cik": 912463,
        "title": "GUESS INC"
    },
    "AVDL": {
        "cik": 1012477,
        "title": "AVADEL PHARMACEUTICALS PLC"
    },
    "NPWR": {
        "cik": 1845437,
        "title": "NET Power Inc."
    },
    "IRBT": {
        "cik": 1159167,
        "title": "IROBOT CORP"
    },
    "FVRR": {
        "cik": 1762301,
        "title": "Fiverr International Ltd."
    },
    "EB": {
        "cik": 1475115,
        "title": "Eventbrite, Inc."
    },
    "AVNS": {
        "cik": 1606498,
        "title": "AVANOS MEDICAL, INC."
    },
    "GDEN": {
        "cik": 1071255,
        "title": "GOLDEN ENTERTAINMENT, INC."
    },
    "CRNC": {
        "cik": 1768267,
        "title": "Cerence Inc."
    },
    "OCFC": {
        "cik": 1004702,
        "title": "OCEANFIRST FINANCIAL CORP"
    },
    "PLRX": {
        "cik": 1746473,
        "title": "PLIANT THERAPEUTICS, INC."
    },
    "RXST": {
        "cik": 1111485,
        "title": "RxSight, Inc."
    },
    "EAI": {
        "cik": 7323,
        "title": "ENTERGY ARKANSAS, LLC"
    },
    "PTLO": {
        "cik": 1871509,
        "title": "Portillo's Inc."
    },
    "SASR": {
        "cik": 824410,
        "title": "SANDY SPRING BANCORP INC"
    },
    "HOLI": {
        "cik": 1357450,
        "title": "Hollysys Automation Technologies, Ltd."
    },
    "MUC": {
        "cik": 1051004,
        "title": "BLACKROCK MUNIHOLDINGS CALIFORNIA QUALITY FUND, INC."
    },
    "IMTX": {
        "cik": 1809196,
        "title": "Immatics N.V."
    },
    "EMBC": {
        "cik": 1872789,
        "title": "Embecta Corp."
    },
    "LPG": {
        "cik": 1596993,
        "title": "DORIAN LPG LTD."
    },
    "LPRO": {
        "cik": 1806201,
        "title": "Open Lending Corp"
    },
    "BCSF": {
        "cik": 1655050,
        "title": "Bain Capital Specialty Finance, Inc."
    },
    "COGT": {
        "cik": 1622229,
        "title": "Cogent Biosciences, Inc."
    },
    "SDA": {
        "cik": 1936804,
        "title": "SunCar Technology Group Inc."
    },
    "AMSF": {
        "cik": 1018979,
        "title": "AMERISAFE INC"
    },
    "SSYS": {
        "cik": 1517396,
        "title": "STRATASYS LTD."
    },
    "TVTX": {
        "cik": 1438533,
        "title": "Travere Therapeutics, Inc."
    },
    "NVGS": {
        "cik": 1581804,
        "title": "Navigator Holdings Ltd."
    },
    "CET": {
        "cik": 18748,
        "title": "CENTRAL SECURITIES CORP"
    },
    "AMPS": {
        "cik": 1828723,
        "title": "Altus Power, Inc."
    },
    "FLGT": {
        "cik": 1674930,
        "title": "Fulgent Genetics, Inc."
    },
    "BBAR": {
        "cik": 913059,
        "title": "Banco BBVA Argentina S.A."
    },
    "ICHR": {
        "cik": 1652535,
        "title": "ICHOR HOLDINGS, LTD."
    },
    "MIRM": {
        "cik": 1759425,
        "title": "Mirum Pharmaceuticals, Inc."
    },
    "BBDC": {
        "cik": 1379785,
        "title": "Barings BDC, Inc."
    },
    "RTL": {
        "cik": 1568162,
        "title": "Necessity Retail REIT, Inc."
    },
    "ACCD": {
        "cik": 1481646,
        "title": "Accolade, Inc."
    },
    "NEXT": {
        "cik": 1612720,
        "title": "NextDecade Corp."
    },
    "VTEX": {
        "cik": 1793663,
        "title": "VTEX"
    },
    "AHH": {
        "cik": 1569187,
        "title": "Armada Hoffler Properties, Inc."
    },
    "PTA": {
        "cik": 1793882,
        "title": "Cohen & Steers Tax-Advantaged Preferred Securities & Income Fund"
    },
    "GAM": {
        "cik": 40417,
        "title": "GENERAL AMERICAN INVESTORS CO INC"
    },
    "KRUS": {
        "cik": 1772177,
        "title": "KURA SUSHI USA, INC."
    },
    "EAF": {
        "cik": 931148,
        "title": "GRAFTECH INTERNATIONAL LTD"
    },
    "EVLV": {
        "cik": 1805385,
        "title": "Evolv Technologies Holdings, Inc."
    },
    "BHLB": {
        "cik": 1108134,
        "title": "BERKSHIRE HILLS BANCORP INC"
    },
    "SPLP": {
        "cik": 1452857,
        "title": "STEEL PARTNERS HOLDINGS L.P."
    },
    "BBN": {
        "cik": 1493683,
        "title": "BlackRock Taxable Municipal Bond Trust"
    },
    "SCRM": {
        "cik": 1893325,
        "title": "Screaming Eagle Acquisition Corp."
    },
    "SCS": {
        "cik": 1050825,
        "title": "STEELCASE INC"
    },
    "ARKO": {
        "cik": 1823794,
        "title": "ARKO Corp."
    },
    "KRO": {
        "cik": 1257640,
        "title": "KRONOS WORLDWIDE INC"
    },
    "TMST": {
        "cik": 1598428,
        "title": "TimkenSteel Corp"
    },
    "HKD": {
        "cik": 1809691,
        "title": "AMTD Digital Inc."
    },
    "NOAH": {
        "cik": 1499543,
        "title": "Noah Holdings Ltd"
    },
    "RDFN": {
        "cik": 1382821,
        "title": "Redfin Corp"
    },
    "CSR": {
        "cik": 798359,
        "title": "CENTERSPACE"
    },
    "CAL": {
        "cik": 14707,
        "title": "CALERES INC"
    },
    "SBR": {
        "cik": 710752,
        "title": "SABINE ROYALTY TRUST"
    },
    "INDI": {
        "cik": 1841925,
        "title": "indie Semiconductor, Inc."
    },
    "TMCI": {
        "cik": 1630627,
        "title": "TREACE MEDICAL CONCEPTS, INC."
    },
    "TSAT": {
        "cik": 1845840,
        "title": "Telesat Corp"
    },
    "LMND": {
        "cik": 1691421,
        "title": "Lemonade, Inc."
    },
    "SLCA": {
        "cik": 1524741,
        "title": "U.S. SILICA HOLDINGS, INC."
    },
    "GRND": {
        "cik": 1820144,
        "title": "Grindr Inc."
    },
    "FREY": {
        "cik": 1844224,
        "title": "FREYR Battery"
    },
    "SBOW": {
        "cik": 351817,
        "title": "SILVERBOW RESOURCES, INC."
    },
    "OBK": {
        "cik": 1516912,
        "title": "Origin Bancorp, Inc."
    },
    "DRQ": {
        "cik": 1042893,
        "title": "DRIL-QUIP INC"
    },
    "ACEL": {
        "cik": 1698991,
        "title": "Accel Entertainment, Inc."
    },
    "BNGO": {
        "cik": 1411690,
        "title": "Bionano Genomics, Inc."
    },
    "SBSI": {
        "cik": 705432,
        "title": "SOUTHSIDE BANCSHARES INC"
    },
    "PLYM": {
        "cik": 1515816,
        "title": "Plymouth Industrial REIT, Inc."
    },
    "ASIX": {
        "cik": 1673985,
        "title": "AdvanSix Inc."
    },
    "TASK": {
        "cik": 1829864,
        "title": "TaskUs, Inc."
    },
    "FBMS": {
        "cik": 947559,
        "title": "FIRST BANCSHARES INC /MS/"
    },
    "PRA": {
        "cik": 1127703,
        "title": "PROASSURANCE CORP"
    },
    "MATV": {
        "cik": 1000623,
        "title": "Mativ Holdings, Inc."
    },
    "VALN": {
        "cik": 1836564,
        "title": "Valneva SE"
    },
    "SA": {
        "cik": 1231346,
        "title": "SEABRIDGE GOLD INC"
    },
    "DCGO": {
        "cik": 1822359,
        "title": "DocGo Inc."
    },
    "VRNOF": {
        "cik": 1848416,
        "title": "Verano Holdings Corp."
    },
    "SLP": {
        "cik": 1023459,
        "title": "Simulations Plus, Inc."
    },
    "PEBO": {
        "cik": 318300,
        "title": "PEOPLES BANCORP INC"
    },
    "PACW": {
        "cik": 1102112,
        "title": "PACWEST BANCORP"
    },
    "MED": {
        "cik": 910329,
        "title": "MEDIFAST INC"
    },
    "CDRE": {
        "cik": 1860543,
        "title": "Cadre Holdings, Inc."
    },
    "ADPT": {
        "cik": 1478320,
        "title": "Adaptive Biotechnologies Corp"
    },
    "EXLS": {
        "cik": 1297989,
        "title": "ExlService Holdings, Inc."
    },
    "RGR": {
        "cik": 95029,
        "title": "STURM RUGER & CO INC"
    },
    "PWP": {
        "cik": 1777835,
        "title": "Perella Weinberg Partners"
    },
    "SPH": {
        "cik": 1005210,
        "title": "SUBURBAN PROPANE PARTNERS LP"
    },
    "EVBG": {
        "cik": 1437352,
        "title": "EVERBRIDGE, INC."
    },
    "FPF": {
        "cik": 1567569,
        "title": "First Trust Intermediate Duration Preferred & Income Fund"
    },
    "RA": {
        "cik": 1655099,
        "title": "Brookfield Real Assets Income Fund Inc."
    },
    "GIII": {
        "cik": 821002,
        "title": "G III APPAREL GROUP LTD /DE/"
    },
    "CLNE": {
        "cik": 1368265,
        "title": "Clean Energy Fuels Corp."
    },
    "BTZ": {
        "cik": 1379384,
        "title": "BLACKROCK CREDIT ALLOCATION INCOME TRUST"
    },
    "QTRX": {
        "cik": 1503274,
        "title": "Quanterix Corp"
    },
    "ALX": {
        "cik": 3499,
        "title": "ALEXANDERS INC"
    },
    "EOS": {
        "cik": 1308335,
        "title": "Eaton Vance Enhanced Equity Income Fund II"
    },
    "WTTR": {
        "cik": 1693256,
        "title": "Select Water Solutions, Inc."
    },
    "POWL": {
        "cik": 80420,
        "title": "POWELL INDUSTRIES INC"
    },
    "GEO": {
        "cik": 923796,
        "title": "GEO GROUP INC"
    },
    "CRESY": {
        "cik": 1034957,
        "title": "CRESUD INC"
    },
    "NAMS": {
        "cik": 1936258,
        "title": "NewAmsterdam Pharma Co N.V."
    },
    "HCSG": {
        "cik": 731012,
        "title": "HEALTHCARE SERVICES GROUP INC"
    },
    "PFBC": {
        "cik": 1492165,
        "title": "Preferred Bank"
    },
    "PDS": {
        "cik": 1013605,
        "title": "PRECISION DRILLING Corp"
    },
    "ARLO": {
        "cik": 1736946,
        "title": "Arlo Technologies, Inc."
    },
    "SKWD": {
        "cik": 1519449,
        "title": "Skyward Specialty Insurance Group, Inc."
    },
    "NGMS": {
        "cik": 1821349,
        "title": "NeoGames S.A."
    },
    "KIDS": {
        "cik": 1425450,
        "title": "ORTHOPEDIATRICS CORP"
    },
    "CCRN": {
        "cik": 1141103,
        "title": "CROSS COUNTRY HEALTHCARE INC"
    },
    "ARCE": {
        "cik": 1740594,
        "title": "Arco Platform Ltd."
    },
    "APPS": {
        "cik": 317788,
        "title": "Digital Turbine, Inc."
    },
    "BHE": {
        "cik": 863436,
        "title": "BENCHMARK ELECTRONICS INC"
    },
    "OXLC": {
        "cik": 1495222,
        "title": "Oxford Lane Capital Corp."
    },
    "MRRTY": {
        "cik": 1496919,
        "title": "MARFRIG GLOBAL FOODS S.A."
    },
    "INFN": {
        "cik": 1138639,
        "title": "Infinera Corp"
    },
    "UMH": {
        "cik": 752642,
        "title": "UMH PROPERTIES, INC."
    },
    "ADMA": {
        "cik": 1368514,
        "title": "ADMA BIOLOGICS, INC."
    },
    "BRCC": {
        "cik": 1891101,
        "title": "BRC Inc."
    },
    "BGS": {
        "cik": 1278027,
        "title": "B&G Foods, Inc."
    },
    "PRM": {
        "cik": 1880319,
        "title": "Perimeter Solutions, SA"
    },
    "BZH": {
        "cik": 915840,
        "title": "BEAZER HOMES USA INC"
    },
    "RSI": {
        "cik": 1793659,
        "title": "Rush Street Interactive, Inc."
    },
    "PLL": {
        "cik": 1728205,
        "title": "Piedmont Lithium Inc."
    },
    "RNP": {
        "cik": 1224450,
        "title": "COHEN & STEERS REIT & PREFERRED & INCOME FUND INC"
    },
    "VRDN": {
        "cik": 1590750,
        "title": "Viridian Therapeutics, Inc.DE"
    },
    "INVA": {
        "cik": 1080014,
        "title": "Innoviva, Inc."
    },
    "SCHN": {
        "cik": 912603,
        "title": "RADIUS RECYCLING"
    },
    "LBAI": {
        "cik": 846901,
        "title": "LAKELAND BANCORP INC"
    },
    "PNT": {
        "cik": 1811764,
        "title": "POINT Biopharma Global Inc."
    },
    "TUYA": {
        "cik": 1829118,
        "title": "Tuya Inc."
    },
    "RWT": {
        "cik": 930236,
        "title": "REDWOOD TRUST INC"
    },
    "VERV": {
        "cik": 1840574,
        "title": "Verve Therapeutics, Inc."
    },
    "RBCAA": {
        "cik": 921557,
        "title": "REPUBLIC BANCORP INC /KY/"
    },
    "CRNX": {
        "cik": 1658247,
        "title": "Crinetics Pharmaceuticals, Inc."
    },
    "PL": {
        "cik": 1836833,
        "title": "Planet Labs PBC"
    },
    "BRKL": {
        "cik": 1049782,
        "title": "BROOKLINE BANCORP INC"
    },
    "NAT": {
        "cik": 1000177,
        "title": "NORDIC AMERICAN TANKERS Ltd"
    },
    "DCOM": {
        "cik": 846617,
        "title": "Dime Community Bancshares, Inc. /NY/"
    },
    "QCRH": {
        "cik": 906465,
        "title": "QCR HOLDINGS INC"
    },
    "MFIC": {
        "cik": 1278752,
        "title": "MidCap Financial Investment Corp"
    },
    "BSIG": {
        "cik": 1748824,
        "title": "BrightSphere Investment Group Inc."
    },
    "ETW": {
        "cik": 1322435,
        "title": "Eaton Vance Tax-Managed Global Buy-Write Opportunities Fund"
    },
    "AOSL": {
        "cik": 1387467,
        "title": "ALPHA & OMEGA SEMICONDUCTOR Ltd"
    },
    "ADV": {
        "cik": 1776661,
        "title": "Advantage Solutions Inc."
    },
    "NRK": {
        "cik": 1195739,
        "title": "NUVEEN NEW YORK AMT-FREE QUALITY MUNICIPAL INCOME FUND"
    },
    "TDCX": {
        "cik": 1803112,
        "title": "TDCX Inc."
    },
    "AMAM": {
        "cik": 1836056,
        "title": "Ambrx Biopharma Inc."
    },
    "EFC": {
        "cik": 1411342,
        "title": "Ellington Financial Inc."
    },
    "GABC": {
        "cik": 714395,
        "title": "GERMAN AMERICAN BANCORP, INC."
    },
    "ATRI": {
        "cik": 701288,
        "title": "ATRION CORP"
    },
    "ALTI": {
        "cik": 1838615,
        "title": "AlTi Global, Inc."
    },
    "KUBR": {
        "cik": 1081834,
        "title": "Kuber Resources Corp"
    },
    "AWF": {
        "cik": 906013,
        "title": "ALLIANCEBERNSTEIN GLOBAL HIGH INCOME FUND INC"
    },
    "MDXG": {
        "cik": 1376339,
        "title": "MIMEDX GROUP, INC."
    },
    "FSM": {
        "cik": 1341335,
        "title": "FORTUNA SILVER MINES INC"
    },
    "PHAT": {
        "cik": 1783183,
        "title": "Phathom Pharmaceuticals, Inc."
    },
    "BLX": {
        "cik": 890541,
        "title": "FOREIGN TRADE BANK OF LATIN AMERICA, INC."
    },
    "NX": {
        "cik": 1423221,
        "title": "Quanex Building Products CORP"
    },
    "ASTS": {
        "cik": 1780312,
        "title": "AST SpaceMobile, Inc."
    },
    "THR": {
        "cik": 1489096,
        "title": "Thermon Group Holdings, Inc."
    },
    "DLX": {
        "cik": 27996,
        "title": "DELUXE CORP"
    },
    "NRP": {
        "cik": 1171486,
        "title": "NATURAL RESOURCE PARTNERS LP"
    },
    "DIN": {
        "cik": 49754,
        "title": "Dine Brands Global, Inc."
    },
    "RPAY": {
        "cik": 1720592,
        "title": "Repay Holdings Corp"
    },
    "PIII": {
        "cik": 1832511,
        "title": "P3 Health Partners Inc."
    },
    "COLL": {
        "cik": 1267565,
        "title": "COLLEGIUM PHARMACEUTICAL, INC"
    },
    "HPP": {
        "cik": 1482512,
        "title": "Hudson Pacific Properties, Inc."
    },
    "CHCT": {
        "cik": 1631569,
        "title": "Community Healthcare Trust Inc"
    },
    "CHY": {
        "cik": 1222719,
        "title": "CALAMOS CONVERTIBLE & HIGH INCOME FUND"
    },
    "SILK": {
        "cik": 1397702,
        "title": "Silk Road Medical Inc"
    },
    "UAN": {
        "cik": 1425292,
        "title": "CVR PARTNERS, LP"
    },
    "SSU": {
        "cik": 1869858,
        "title": "SIGNA Sports United N.V."
    },
    "STEM": {
        "cik": 1758766,
        "title": "STEM, INC."
    },
    "SNCY": {
        "cik": 1743907,
        "title": "Sun Country Airlines Holdings, Inc."
    },
    "IMOS": {
        "cik": 1123134,
        "title": "CHIPMOS TECHNOLOGIES INC"
    },
    "BLTE": {
        "cik": 1889109,
        "title": "BELITE BIO, INC"
    },
    "SKIN": {
        "cik": 1818093,
        "title": "Beauty Health Co"
    },
    "AOD": {
        "cik": 1379400,
        "title": "abrdn Total Dynamic Dividend Fund"
    },
    "AXL": {
        "cik": 1062231,
        "title": "AMERICAN AXLE & MANUFACTURING HOLDINGS INC"
    },
    "SBGI": {
        "cik": 1971213,
        "title": "Sinclair, Inc."
    },
    "DDD": {
        "cik": 910638,
        "title": "3D SYSTEMS CORP"
    },
    "WALD": {
        "cik": 1840199,
        "title": "Waldencast plc"
    },
    "TTGT": {
        "cik": 1293282,
        "title": "TechTarget Inc"
    },
    "BRSP": {
        "cik": 1717547,
        "title": "BrightSpire Capital, Inc."
    },
    "CSWC": {
        "cik": 17313,
        "title": "CAPITAL SOUTHWEST CORP"
    },
    "WRLD": {
        "cik": 108385,
        "title": "WORLD ACCEPTANCE CORP"
    },
    "SIBN": {
        "cik": 1459839,
        "title": "SI-BONE, Inc."
    },
    "RPT": {
        "cik": 842183,
        "title": "RPT Realty"
    },
    "CRF": {
        "cik": 33934,
        "title": "CORNERSTONE TOTAL RETURN FUND INC"
    },
    "BFC": {
        "cik": 1746109,
        "title": "Bank First Corp"
    },
    "WEST": {
        "cik": 1806347,
        "title": "Westrock Coffee Co"
    },
    "CFFN": {
        "cik": 1490906,
        "title": "Capitol Federal Financial, Inc."
    },
    "INBX": {
        "cik": 1739614,
        "title": "Inhibrx, Inc."
    },
    "HQH": {
        "cik": 805267,
        "title": "TEKLA HEALTHCARE INVESTORS"
    },
    "SII": {
        "cik": 1512920,
        "title": "SPROTT INC."
    },
    "DRD": {
        "cik": 1023512,
        "title": "DRDGOLD LTD"
    },
    "SLRC": {
        "cik": 1418076,
        "title": "SLR Investment Corp."
    },
    "ARCT": {
        "cik": 1768224,
        "title": "Arcturus Therapeutics Holdings Inc."
    },
    "MQY": {
        "cik": 890196,
        "title": "BLACKROCK MUNIYIELD QUALITY FUND, INC."
    },
    "XMTR": {
        "cik": 1657573,
        "title": "Xometry, Inc."
    },
    "CII": {
        "cik": 1278895,
        "title": "BLACKROCK ENHANCED CAPITAL & INCOME FUND, INC."
    },
    "BCYC": {
        "cik": 1761612,
        "title": "BICYCLE THERAPEUTICS plc"
    },
    "VSEC": {
        "cik": 102752,
        "title": "VSE CORP"
    },
    "NBXG": {
        "cik": 1843181,
        "title": "Neuberger Berman Next Generation Connectivity Fund Inc."
    },
    "REVG": {
        "cik": 1687221,
        "title": "REV Group, Inc."
    },
    "KURA": {
        "cik": 1422143,
        "title": "Kura Oncology, Inc."
    },
    "EVA": {
        "cik": 1592057,
        "title": "Enviva Inc."
    },
    "MUI": {
        "cik": 1232860,
        "title": "BLACKROCK MUNICIPAL INCOME FUND, INC."
    },
    "CHI": {
        "cik": 1171471,
        "title": "CALAMOS CONVERTIBLE OPPORTUNITIES & INCOME FUND"
    },
    "NYMT": {
        "cik": 1273685,
        "title": "NEW YORK MORTGAGE TRUST INC"
    },
    "AMRK": {
        "cik": 1591588,
        "title": "A-Mark Precious Metals, Inc."
    },
    "BCX": {
        "cik": 1506289,
        "title": "BlackRock Resources & Commodities Strategy Trust"
    },
    "CDE": {
        "cik": 215466,
        "title": "Coeur Mining, Inc."
    },
    "AC": {
        "cik": 1642122,
        "title": "Associated Capital Group, Inc."
    },
    "KIND": {
        "cik": 1846069,
        "title": "Nextdoor Holdings, Inc."
    },
    "OFLX": {
        "cik": 1317945,
        "title": "Omega Flex, Inc."
    },
    "ACMR": {
        "cik": 1680062,
        "title": "ACM Research, Inc."
    },
    "GRC": {
        "cik": 42682,
        "title": "GORMAN RUPP CO"
    },
    "VREX": {
        "cik": 1681622,
        "title": "Varex Imaging Corp"
    },
    "GDOT": {
        "cik": 1386278,
        "title": "GREEN DOT CORP"
    },
    "PHAR": {
        "cik": 1828316,
        "title": "Pharming Group N.V."
    },
    "EXAI": {
        "cik": 1865408,
        "title": "Exscientia plc"
    },
    "GDYN": {
        "cik": 1743725,
        "title": "GRID DYNAMICS HOLDINGS, INC."
    },
    "BIGC": {
        "cik": 1626450,
        "title": "BigCommerce Holdings, Inc."
    },
    "SPTN": {
        "cik": 877422,
        "title": "SpartanNash Co"
    },
    "ETD": {
        "cik": 896156,
        "title": "ETHAN ALLEN INTERIORS INC"
    },
    "BDN": {
        "cik": 790816,
        "title": "BRANDYWINE REALTY TRUST"
    },
    "KOP": {
        "cik": 1315257,
        "title": "Koppers Holdings Inc."
    },
    "PDM": {
        "cik": 1042776,
        "title": "Piedmont Office Realty Trust, Inc."
    },
    "VERA": {
        "cik": 1831828,
        "title": "Vera Therapeutics, Inc."
    },
    "PLPC": {
        "cik": 80035,
        "title": "PREFORMED LINE PRODUCTS CO"
    },
    "WKME": {
        "cik": 1847584,
        "title": "WalkMe Ltd."
    },
    "VTOL": {
        "cik": 1525221,
        "title": "Bristow Group Inc."
    },
    "BY": {
        "cik": 1702750,
        "title": "BYLINE BANCORP, INC."
    },
    "SMP": {
        "cik": 93389,
        "title": "STANDARD MOTOR PRODUCTS, INC."
    },
    "WW": {
        "cik": 105319,
        "title": "WW INTERNATIONAL, INC."
    },
    "AVTA": {
        "cik": 1068875,
        "title": "AVANTAX, INC."
    },
    "THRY": {
        "cik": 1556739,
        "title": "Thryv Holdings, Inc."
    },
    "RGNX": {
        "cik": 1590877,
        "title": "REGENXBIO Inc."
    },
    "LWLG": {
        "cik": 1325964,
        "title": "Lightwave Logic, Inc."
    },
    "SPCE": {
        "cik": 1706946,
        "title": "Virgin Galactic Holdings, Inc"
    },
    "BV": {
        "cik": 1734713,
        "title": "BrightView Holdings, Inc."
    },
    "KREF": {
        "cik": 1631596,
        "title": "KKR Real Estate Finance Trust Inc."
    },
    "WLKP": {
        "cik": 1604665,
        "title": "Westlake Chemical Partners LP"
    },
    "UTL": {
        "cik": 755001,
        "title": "UNITIL CORP"
    },
    "SP": {
        "cik": 1059262,
        "title": "SP Plus Corp"
    },
    "GTN": {
        "cik": 43196,
        "title": "GRAY TELEVISION INC"
    },
    "NFGC": {
        "cik": 1840616,
        "title": "New Found Gold Corp."
    },
    "GOTU": {
        "cik": 1768259,
        "title": "Gaotu Techedu Inc."
    },
    "HRT": {
        "cik": 1859285,
        "title": "HireRight Holdings Corp"
    },
    "THQ": {
        "cik": 1604522,
        "title": "Tekla Healthcare Opportunities Fund"
    },
    "CDMO": {
        "cik": 704562,
        "title": "Avid Bioservices, Inc."
    },
    "TMP": {
        "cik": 1005817,
        "title": "TOMPKINS FINANCIAL CORP"
    },
    "LXU": {
        "cik": 60714,
        "title": "LSB INDUSTRIES, INC."
    },
    "LICY": {
        "cik": 1828811,
        "title": "Li-Cycle Holdings Corp."
    },
    "ARDX": {
        "cik": 1437402,
        "title": "ARDELYX, INC."
    },
    "NYAX": {
        "cik": 1901279,
        "title": "Nayax Ltd."
    },
    "GHLD": {
        "cik": 1821160,
        "title": "Guild Holdings Co"
    },
    "PRAA": {
        "cik": 1185348,
        "title": "PRA GROUP INC"
    },
    "AAC": {
        "cik": 1829432,
        "title": "Ares Acquisition Corp"
    },
    "MRC": {
        "cik": 1439095,
        "title": "MRC GLOBAL INC."
    },
    "HY": {
        "cik": 1173514,
        "title": "HYSTER-YALE MATERIALS HANDLING, INC."
    },
    "RSKD": {
        "cik": 1851112,
        "title": "Riskified Ltd."
    },
    "NRGX": {
        "cik": 1756908,
        "title": "PIMCO Energy & Tactical Credit Opportunities Fund"
    },
    "OTLY": {
        "cik": 1843586,
        "title": "Oatly Group AB"
    },
    "SXC": {
        "cik": 1514705,
        "title": "SunCoke Energy, Inc."
    },
    "BKD": {
        "cik": 1332349,
        "title": "Brookdale Senior Living Inc."
    },
    "INNV": {
        "cik": 1834376,
        "title": "InnovAge Holding Corp."
    },
    "SNPO": {
        "cik": 1856430,
        "title": "Snap One Holdings Corp."
    },
    "CLCO": {
        "cik": 1944057,
        "title": "Cool Co Ltd."
    },
    "MLAB": {
        "cik": 724004,
        "title": "MESA LABORATORIES INC /CO/"
    },
    "CGBD": {
        "cik": 1544206,
        "title": "Carlyle Secured Lending, Inc."
    },
    "CRAI": {
        "cik": 1053706,
        "title": "CRA INTERNATIONAL, INC."
    },
    "CNOB": {
        "cik": 712771,
        "title": "ConnectOne Bancorp, Inc."
    },
    "YALA": {
        "cik": 1794350,
        "title": "Yalla Group Ltd"
    },
    "NSSC": {
        "cik": 69633,
        "title": "NAPCO SECURITY TECHNOLOGIES, INC"
    },
    "EFXT": {
        "cik": 1904856,
        "title": "Enerflex Ltd."
    },
    "SNMP": {
        "cik": 1362705,
        "title": "Evolve Transition Infrastructure LP"
    },
    "BYND": {
        "cik": 1655210,
        "title": "BEYOND MEAT, INC."
    },
    "EGBN": {
        "cik": 1050441,
        "title": "EAGLE BANCORP INC"
    },
    "CAPL": {
        "cik": 1538849,
        "title": "CrossAmerica Partners LP"
    },
    "TWI": {
        "cik": 899751,
        "title": "TITAN INTERNATIONAL INC"
    },
    "TRNS": {
        "cik": 99302,
        "title": "TRANSCAT INC"
    },
    "RDWR": {
        "cik": 1094366,
        "title": "RADWARE LTD"
    },
    "PSFE": {
        "cik": 1833835,
        "title": "Paysafe Ltd"
    },
    "ASTL": {
        "cik": 1860805,
        "title": "Algoma Steel Group Inc."
    },
    "TELL": {
        "cik": 61398,
        "title": "TELLURIAN INC. /DE/"
    },
    "ZUUS": {
        "cik": 1687926,
        "title": "ZEUUS, INC."
    },
    "IIIV": {
        "cik": 1728688,
        "title": "i3 Verticals, Inc."
    },
    "SES": {
        "cik": 1819142,
        "title": "SES AI Corp"
    },
    "PRLB": {
        "cik": 1443669,
        "title": "Proto Labs Inc"
    },
    "ULH": {
        "cik": 1308208,
        "title": "UNIVERSAL LOGISTICS HOLDINGS, INC."
    },
    "IBRX": {
        "cik": 1326110,
        "title": "ImmunityBio, Inc."
    },
    "PKST": {
        "cik": 1600626,
        "title": "Peakstone Realty Trust"
    },
    "BXC": {
        "cik": 1301787,
        "title": "BlueLinx Holdings Inc."
    },
    "MTTR": {
        "cik": 1819394,
        "title": "Matterport, Inc./DE"
    },
    "CENX": {
        "cik": 949157,
        "title": "CENTURY ALUMINUM CO"
    },
    "MTEM": {
        "cik": 1183765,
        "title": "Molecular Templates, Inc."
    },
    "FMCB": {
        "cik": 1085913,
        "title": "FARMERS & MERCHANTS BANCORP"
    },
    "NVAX": {
        "cik": 1000694,
        "title": "NOVAVAX INC"
    },
    "HZO": {
        "cik": 1057060,
        "title": "MARINEMAX INC"
    },
    "COMM": {
        "cik": 1517228,
        "title": "CommScope Holding Company, Inc."
    },
    "CCVI": {
        "cik": 1828250,
        "title": "Churchill Capital Corp VI"
    },
    "BASE": {
        "cik": 1845022,
        "title": "Couchbase, Inc."
    },
    "PHK": {
        "cik": 1219360,
        "title": "PIMCO HIGH INCOME FUND"
    },
    "GGR": {
        "cik": 1886190,
        "title": "Gogoro Inc."
    },
    "NNDM": {
        "cik": 1643303,
        "title": "Nano Dimension Ltd."
    },
    "BANC": {
        "cik": 1169770,
        "title": "BANC OF CALIFORNIA, INC."
    },
    "WDI": {
        "cik": 1819559,
        "title": "Western Asset Diversified Income Fund"
    },
    "NRDY": {
        "cik": 1819404,
        "title": "Nerdy Inc."
    },
    "BJRI": {
        "cik": 1013488,
        "title": "BJs RESTAURANTS INC"
    },
    "MYI": {
        "cik": 883412,
        "title": "BLACKROCK MUNIYIELD QUALITY FUND III, INC."
    },
    "FDMT": {
        "cik": 1650648,
        "title": "4D Molecular Therapeutics, Inc."
    },
    "ZH": {
        "cik": 1835724,
        "title": "Zhihu Inc."
    },
    "CIFR": {
        "cik": 1819989,
        "title": "Cipher Mining Inc."
    },
    "NEXA": {
        "cik": 1713930,
        "title": "Nexa Resources S.A."
    },
    "SILV": {
        "cik": 1659520,
        "title": "SilverCrest Metals Inc."
    },
    "AVO": {
        "cik": 1802974,
        "title": "Mission Produce, Inc."
    },
    "MAXN": {
        "cik": 1796898,
        "title": "Maxeon Solar Technologies, Ltd."
    },
    "SAVA": {
        "cik": 1069530,
        "title": "CASSAVA SCIENCES INC"
    },
    "EDIT": {
        "cik": 1650664,
        "title": "Editas Medicine, Inc."
    },
    "ELVN": {
        "cik": 1672619,
        "title": "Enliven Therapeutics, Inc."
    },
    "BLBD": {
        "cik": 1589526,
        "title": "Blue Bird Corp"
    },
    "SCSC": {
        "cik": 918965,
        "title": "SCANSOURCE, INC."
    },
    "TCPC": {
        "cik": 1370755,
        "title": "BlackRock TCP Capital Corp."
    },
    "CNDT": {
        "cik": 1677703,
        "title": "CONDUENT Inc"
    },
    "TCNNF": {
        "cik": 1754195,
        "title": "Trulieve Cannabis Corp."
    },
    "PLOW": {
        "cik": 1287213,
        "title": "DOUGLAS DYNAMICS, INC"
    },
    "GSL": {
        "cik": 1430725,
        "title": "Global Ship Lease, Inc."
    },
    "DHC": {
        "cik": 1075415,
        "title": "DIVERSIFIED HEALTHCARE TRUST"
    },
    "HLLY": {
        "cik": 1822928,
        "title": "Holley Inc."
    },
    "SSP": {
        "cik": 832428,
        "title": "E.W. SCRIPPS Co"
    },
    "KARO": {
        "cik": 1828102,
        "title": "Karooooo Ltd."
    },
    "NGD": {
        "cik": 800166,
        "title": "New Gold Inc. /FI"
    },
    "OM": {
        "cik": 1484612,
        "title": "Outset Medical, Inc."
    },
    "CRMT": {
        "cik": 799850,
        "title": "AMERICAS CARMART INC"
    },
    "HOUS": {
        "cik": 1398987,
        "title": "Anywhere Real Estate Inc."
    },
    "CRON": {
        "cik": 1656472,
        "title": "Cronos Group Inc."
    },
    "REPX": {
        "cik": 1001614,
        "title": "Riley Exploration Permian, Inc."
    },
    "LC": {
        "cik": 1409970,
        "title": "LendingClub Corp"
    },
    "EOSS": {
        "cik": 1651958,
        "title": "EOS INC."
    },
    "TTI": {
        "cik": 844965,
        "title": "TETRA TECHNOLOGIES INC"
    },
    "CBL": {
        "cik": 910612,
        "title": "CBL & ASSOCIATES PROPERTIES INC"
    },
    "MYE": {
        "cik": 69488,
        "title": "MYERS INDUSTRIES INC"
    },
    "KE": {
        "cik": 1606757,
        "title": "Kimball Electronics, Inc."
    },
    "JQC": {
        "cik": 1227476,
        "title": "Nuveen Credit Strategies Income Fund"
    },
    "BALY": {
        "cik": 1747079,
        "title": "Bally's Corp"
    },
    "BIOX": {
        "cik": 1769484,
        "title": "Bioceres Crop Solutions Corp."
    },
    "LEU": {
        "cik": 1065059,
        "title": "CENTRUS ENERGY CORP"
    },
    "EIM": {
        "cik": 1176984,
        "title": "EATON VANCE MUNICIPAL BOND FUND"
    },
    "DLY": {
        "cik": 1788399,
        "title": "DoubleLine Yield Opportunities Fund"
    },
    "NMM": {
        "cik": 1415921,
        "title": "Navios Maritime Partners L.P."
    },
    "PFC": {
        "cik": 946647,
        "title": "PREMIER FINANCIAL CORP"
    },
    "WEAV": {
        "cik": 1609151,
        "title": "Weave Communications, Inc."
    },
    "CCO": {
        "cik": 1334978,
        "title": "Clear Channel Outdoor Holdings, Inc."
    },
    "OABI": {
        "cik": 1846253,
        "title": "OmniAb, Inc."
    },
    "GHIX": {
        "cik": 1894630,
        "title": "Gores Holdings IX, Inc."
    },
    "OFIX": {
        "cik": 884624,
        "title": "Orthofix Medical Inc."
    },
    "HTD": {
        "cik": 1260041,
        "title": "JOHN HANCOCK TAX-ADVANTAGED DIVIDEND INCOME FUND"
    },
    "CHUY": {
        "cik": 1524931,
        "title": "CHUY'S HOLDINGS, INC."
    },
    "NRDS": {
        "cik": 1625278,
        "title": "NERDWALLET, INC."
    },
    "PHVS": {
        "cik": 1830487,
        "title": "Pharvaris N.V."
    },
    "VTS": {
        "cik": 1944558,
        "title": "Vitesse Energy, Inc."
    },
    "JPC": {
        "cik": 1216583,
        "title": "Nuveen Preferred & Income Opportunities Fund"
    },
    "AORT": {
        "cik": 784199,
        "title": "ARTIVION, INC."
    },
    "MEGI": {
        "cik": 1855066,
        "title": "MainStay CBRE Global Infrastructure Megatrends Term Fund"
    },
    "LVRO": {
        "cik": 1945711,
        "title": "Lavoro Ltd"
    },
    "AVXL": {
        "cik": 1314052,
        "title": "ANAVEX LIFE SCIENCES CORP."
    },
    "PGRU": {
        "cik": 1873331,
        "title": "PROPERTYGURU GROUP LTD"
    },
    "RAPT": {
        "cik": 1673772,
        "title": "RAPT Therapeutics, Inc."
    },
    "HCAT": {
        "cik": 1636422,
        "title": "Health Catalyst, Inc."
    },
    "SMRT": {
        "cik": 1837014,
        "title": "SmartRent, Inc."
    },
    "DX": {
        "cik": 826675,
        "title": "DYNEX CAPITAL INC"
    },
    "SPRY": {
        "cik": 1671858,
        "title": "ARS Pharmaceuticals, Inc."
    },
    "PRTC": {
        "cik": 1782999,
        "title": "PureTech Health plc"
    },
    "ALCC": {
        "cik": 1849056,
        "title": "AltC Acquisition Corp."
    },
    "OSBC": {
        "cik": 357173,
        "title": "OLD SECOND BANCORP INC"
    },
    "NXP": {
        "cik": 883618,
        "title": "NUVEEN SELECT TAX FREE INCOME PORTFOLIO"
    },
    "TITN": {
        "cik": 1409171,
        "title": "Titan Machinery Inc."
    },
    "CNTA": {
        "cik": 1847903,
        "title": "Centessa Pharmaceuticals plc"
    },
    "SCVL": {
        "cik": 895447,
        "title": "SHOE CARNIVAL INC"
    },
    "DMRC": {
        "cik": 1438231,
        "title": "Digimarc CORP"
    },
    "NVRO": {
        "cik": 1444380,
        "title": "NEVRO CORP"
    },
    "TYGO": {
        "cik": 1855447,
        "title": "TIGO ENERGY, INC."
    },
    "CYRX": {
        "cik": 1124524,
        "title": "Cryoport, Inc."
    },
    "BRY": {
        "cik": 1705873,
        "title": "Berry Corp (bry)"
    },
    "TXO": {
        "cik": 1559432,
        "title": "TXO Partners, L.P."
    },
    "HSTM": {
        "cik": 1095565,
        "title": "HEALTHSTREAM INC"
    },
    "DBI": {
        "cik": 1319947,
        "title": "Designer Brands Inc."
    },
    "VMEO": {
        "cik": 1837686,
        "title": "Vimeo, Inc."
    },
    "FNMA": {
        "cik": 310522,
        "title": "FEDERAL NATIONAL MORTGAGE ASSOCIATION FANNIE MAE"
    },
    "CTBI": {
        "cik": 350852,
        "title": "COMMUNITY TRUST BANCORP INC /KY/"
    },
    "BBSI": {
        "cik": 902791,
        "title": "BARRETT BUSINESS SERVICES INC"
    },
    "TYRA": {
        "cik": 1863127,
        "title": "Tyra Biosciences, Inc."
    },
    "WWW": {
        "cik": 110471,
        "title": "WOLVERINE WORLD WIDE INC /DE/"
    },
    "ALPN": {
        "cik": 1626199,
        "title": "ALPINE IMMUNE SCIENCES, INC."
    },
    "KELYA": {
        "cik": 55135,
        "title": "KELLY SERVICES INC"
    },
    "TK": {
        "cik": 911971,
        "title": "TEEKAY CORP"
    },
    "CLOV": {
        "cik": 1801170,
        "title": "CLOVER HEALTH INVESTMENTS, CORP. /DE"
    },
    "AACT": {
        "cik": 1853138,
        "title": "Ares Acquisition Corp II"
    },
    "MDVL": {
        "cik": 1402479,
        "title": "MedAvail Holdings, Inc."
    },
    "FFC": {
        "cik": 1174164,
        "title": "Flaherty & Crumrine PREFERRED & INCOME SECURITIES FUND INC"
    },
    "SVA": {
        "cik": 1084201,
        "title": "SINOVAC BIOTECH LTD"
    },
    "EOI": {
        "cik": 1300391,
        "title": "Eaton Vance Enhanced Equity Income Fund"
    },
    "ASLE": {
        "cik": 1754170,
        "title": "AerSale Corp"
    },
    "CHS": {
        "cik": 897429,
        "title": "CHICO'S FAS, INC."
    },
    "FAX": {
        "cik": 790500,
        "title": "ABRDN ASIA-PACIFIC INCOME FUND, INC."
    },
    "DCO": {
        "cik": 30305,
        "title": "DUCOMMUN INC /DE/"
    },
    "WOW": {
        "cik": 1701051,
        "title": "WideOpenWest, Inc."
    },
    "ENFN": {
        "cik": 1868912,
        "title": "Enfusion, Inc."
    },
    "PUBM": {
        "cik": 1422930,
        "title": "PubMatic, Inc."
    },
    "REX": {
        "cik": 744187,
        "title": "REX AMERICAN RESOURCES Corp"
    },
    "ADTN": {
        "cik": 926282,
        "title": "ADTRAN Holdings, Inc."
    },
    "IOCJY": {
        "cik": 922357,
        "title": "IOCHPE-MAXION SA /FI"
    },
    "ALLG": {
        "cik": 1874474,
        "title": "Allego N.V."
    },
    "TNP": {
        "cik": 1166663,
        "title": "TSAKOS ENERGY NAVIGATION LTD"
    },
    "CVLG": {
        "cik": 928658,
        "title": "COVENANT LOGISTICS GROUP, INC."
    },
    "NOA": {
        "cik": 1368519,
        "title": "North American Construction Group Ltd."
    },
    "UHT": {
        "cik": 798783,
        "title": "UNIVERSAL HEALTH REALTY INCOME TRUST"
    },
    "GMRE": {
        "cik": 1533615,
        "title": "Global Medical REIT Inc."
    },
    "PCN": {
        "cik": 1160990,
        "title": "PIMCO CORPORATE & INCOME STRATEGY FUND"
    },
    "IMXI": {
        "cik": 1683695,
        "title": "International Money Express, Inc."
    },
    "FCEL": {
        "cik": 886128,
        "title": "FUELCELL ENERGY INC"
    },
    "TNGX": {
        "cik": 1819133,
        "title": "Tango Therapeutics, Inc."
    },
    "EVM": {
        "cik": 1177161,
        "title": "EATON VANCE CALIFORNIA MUNICIPAL BOND FUND"
    },
    "HCKT": {
        "cik": 1057379,
        "title": "HACKETT GROUP, INC."
    },
    "WDH": {
        "cik": 1823986,
        "title": "Waterdrop Inc."
    },
    "NDMO": {
        "cik": 1793129,
        "title": "Nuveen Dynamic Municipal Opportunities Fund"
    },
    "DYN": {
        "cik": 1818794,
        "title": "Dyne Therapeutics, Inc."
    },
    "SLI": {
        "cik": 1537137,
        "title": "STANDARD LITHIUM LTD."
    },
    "HAYN": {
        "cik": 858655,
        "title": "HAYNES INTERNATIONAL INC"
    },
    "RICK": {
        "cik": 935419,
        "title": "RCI HOSPITALITY HOLDINGS, INC."
    },
    "PAXS": {
        "cik": 1886878,
        "title": "PIMCO Access Income Fund"
    },
    "CVGW": {
        "cik": 1133470,
        "title": "CALAVO GROWERS INC"
    },
    "ECC": {
        "cik": 1604174,
        "title": "Eagle Point Credit Co Inc."
    },
    "GSBC": {
        "cik": 854560,
        "title": "GREAT SOUTHERN BANCORP, INC."
    },
    "MGIC": {
        "cik": 876779,
        "title": "MAGIC SOFTWARE ENTERPRISES LTD"
    },
    "CINT": {
        "cik": 1868995,
        "title": "CI&T Inc"
    },
    "CLW": {
        "cik": 1441236,
        "title": "Clearwater Paper Corp"
    },
    "CCAP": {
        "cik": 1633336,
        "title": "Crescent Capital BDC, Inc."
    },
    "VSLAX": {
        "cik": 853180,
        "title": "Invesco Senior Loan Fund"
    },
    "VMO": {
        "cik": 884152,
        "title": "Invesco Municipal Opportunity Trust"
    },
    "ATEX": {
        "cik": 1304492,
        "title": "Anterix Inc."
    },
    "WTI": {
        "cik": 1288403,
        "title": "W&T OFFSHORE INC"
    },
    "NMCO": {
        "cik": 1774342,
        "title": "Nuveen Municipal Credit Opportunities Fund"
    },
    "HFWA": {
        "cik": 1046025,
        "title": "HERITAGE FINANCIAL CORP /WA/"
    },
    "PBI": {
        "cik": 78814,
        "title": "PITNEY BOWES INC /DE/"
    },
    "BOE": {
        "cik": 1320375,
        "title": "BlackRock Enhanced Global Dividend Trust"
    },
    "HBT": {
        "cik": 775215,
        "title": "HBT Financial, Inc."
    },
    "FUBO": {
        "cik": 1484769,
        "title": "fuboTV Inc. /FL"
    },
    "LDI": {
        "cik": 1831631,
        "title": "loanDepot, Inc."
    },
    "KAMN": {
        "cik": 54381,
        "title": "KAMAN Corp"
    },
    "IRMD": {
        "cik": 1325618,
        "title": "IRADIMED CORP"
    },
    "BMEA": {
        "cik": 1840439,
        "title": "Biomea Fusion, Inc."
    },
    "PAHC": {
        "cik": 1069899,
        "title": "PHIBRO ANIMAL HEALTH CORP"
    },
    "HBIA": {
        "cik": 732417,
        "title": "HILLS BANCORPORATION"
    },
    "VVI": {
        "cik": 884219,
        "title": "VIAD CORP"
    },
    "TSNDF": {
        "cik": 1778129,
        "title": "TerrAscend Corp."
    },
    "MOV": {
        "cik": 72573,
        "title": "MOVADO GROUP INC"
    },
    "AIO": {
        "cik": 1778114,
        "title": "Virtus Artificial Intelligence & Technology Opportunities Fund"
    },
    "TGI": {
        "cik": 1021162,
        "title": "TRIUMPH GROUP INC"
    },
    "ALEC": {
        "cik": 1653087,
        "title": "Alector, Inc."
    },
    "COOK": {
        "cik": 1857853,
        "title": "Traeger, Inc."
    },
    "FCBC": {
        "cik": 859070,
        "title": "FIRST COMMUNITY BANKSHARES INC /VA/"
    },
    "DOMO": {
        "cik": 1505952,
        "title": "DOMO, INC."
    },
    "MHD": {
        "cik": 1034665,
        "title": "BLACKROCK MUNIHOLDINGS FUND, INC."
    },
    "AMBI": {
        "cik": 1937441,
        "title": "Ambipar Emergency Response"
    },
    "EUBG": {
        "cik": 1171326,
        "title": "ENTREPRENEUR UNIVERSE BRIGHT GROUP"
    },
    "IDT": {
        "cik": 1005731,
        "title": "IDT CORP"
    },
    "SWBI": {
        "cik": 1092796,
        "title": "SMITH & WESSON BRANDS, INC."
    },
    "BIOL": {
        "cik": 811240,
        "title": "BIOLASE, INC"
    },
    "JOUT": {
        "cik": 788329,
        "title": "JOHNSON OUTDOORS INC"
    },
    "FC": {
        "cik": 886206,
        "title": "FRANKLIN COVEY CO"
    },
    "CION": {
        "cik": 1534254,
        "title": "CION Investment Corp"
    },
    "VVR": {
        "cik": 1059386,
        "title": "Invesco Senior Income Trust"
    },
    "IGR": {
        "cik": 1268884,
        "title": "CBRE GLOBAL REAL ESTATE INCOME FUND"
    },
    "IIIN": {
        "cik": 764401,
        "title": "INSTEEL INDUSTRIES INC"
    },
    "GPRO": {
        "cik": 1500435,
        "title": "GoPro, Inc."
    },
    "SD": {
        "cik": 1349436,
        "title": "SANDRIDGE ENERGY INC"
    },
    "INN": {
        "cik": 1497645,
        "title": "Summit Hotel Properties, Inc."
    },
    "DXPE": {
        "cik": 1020710,
        "title": "DXP ENTERPRISES INC"
    },
    "TIPT": {
        "cik": 1393726,
        "title": "TIPTREE INC."
    },
    "FORR": {
        "cik": 1023313,
        "title": "FORRESTER RESEARCH, INC."
    },
    "YORW": {
        "cik": 108985,
        "title": "YORK WATER CO"
    },
    "MUJ": {
        "cik": 1053988,
        "title": "BLACKROCK MUNIHOLDINGS NEW JERSEY QUALITY FUND, INC."
    },
    "EHAB": {
        "cik": 1803737,
        "title": "Enhabit, Inc."
    },
    "GNLX": {
        "cik": 1231457,
        "title": "GENELUX Corp"
    },
    "ITRN": {
        "cik": 1337117,
        "title": "Ituran Location & Control Ltd."
    },
    "DBA": {
        "cik": 1383082,
        "title": "INVESCO DB AGRICULTURE FUND"
    },
    "ZING": {
        "cik": 1844270,
        "title": "FTAC ZEUS ACQUISITION CORP."
    },
    "MERC": {
        "cik": 1333274,
        "title": "MERCER INTERNATIONAL INC."
    },
    "AMBC": {
        "cik": 874501,
        "title": "AMBAC FINANCIAL GROUP INC"
    },
    "GNK": {
        "cik": 1326200,
        "title": "GENCO SHIPPING & TRADING LTD"
    },
    "RNA": {
        "cik": 1599901,
        "title": "Avidity Biosciences, Inc."
    },
    "PETQ": {
        "cik": 1668673,
        "title": "PetIQ, Inc."
    },
    "SRI": {
        "cik": 1043337,
        "title": "STONERIDGE INC"
    },
    "CCB": {
        "cik": 1437958,
        "title": "COASTAL FINANCIAL CORP"
    },
    "LANV": {
        "cik": 1922097,
        "title": "Lanvin Group Holdings Ltd"
    },
    "CCSI": {
        "cik": 1866633,
        "title": "Consensus Cloud Solutions, Inc."
    },
    "GHG": {
        "cik": 1724755,
        "title": "GreenTree Hospitality Group Ltd."
    },
    "BELFA": {
        "cik": 729580,
        "title": "BEL FUSE INC /NJ"
    },
    "NVRI": {
        "cik": 45876,
        "title": "ENVIRI Corp"
    },
    "BH-A": {
        "cik": 1726173,
        "title": "Biglari Holdings Inc."
    },
    "FPI": {
        "cik": 1591670,
        "title": "Farmland Partners Inc."
    },
    "ALLO": {
        "cik": 1737287,
        "title": "Allogene Therapeutics, Inc."
    },
    "PFN": {
        "cik": 1296250,
        "title": "PIMCO Income Strategy Fund II"
    },
    "ATNI": {
        "cik": 879585,
        "title": "ATN International, Inc."
    },
    "BVH": {
        "cik": 315858,
        "title": "Bluegreen Vacations Holding Corp"
    },
    "AMTB": {
        "cik": 1734342,
        "title": "Amerant Bancorp Inc."
    },
    "FMBH": {
        "cik": 700565,
        "title": "FIRST MID BANCSHARES, INC."
    },
    "NIE": {
        "cik": 1383441,
        "title": "Virtus Equity & Convertible Income Fund"
    },
    "GLDD": {
        "cik": 1372020,
        "title": "Great Lakes Dredge & Dock CORP"
    },
    "CLFD": {
        "cik": 796505,
        "title": "Clearfield, Inc."
    },
    "MOND": {
        "cik": 1828852,
        "title": "Mondee Holdings, Inc."
    },
    "PML": {
        "cik": 1170299,
        "title": "PIMCO MUNICIPAL INCOME FUND II"
    },
    "TILE": {
        "cik": 715787,
        "title": "INTERFACE INC"
    },
    "PEO": {
        "cik": 216851,
        "title": "ADAMS NATURAL RESOURCES FUND, INC."
    },
    "MTAL": {
        "cik": 1950246,
        "title": "Metals Acquisition Ltd"
    },
    "HROW": {
        "cik": 1360214,
        "title": "HARROW HEALTH, INC."
    },
    "LQDT": {
        "cik": 1235468,
        "title": "LIQUIDITY SERVICES INC"
    },
    "MPX": {
        "cik": 1129155,
        "title": "MARINE PRODUCTS CORP"
    },
    "AUTL": {
        "cik": 1730463,
        "title": "Autolus Therapeutics plc"
    },
    "GHRS": {
        "cik": 1855129,
        "title": "GH Research PLC"
    },
    "APLD": {
        "cik": 1144879,
        "title": "Applied Digital Corp."
    },
    "GGN": {
        "cik": 1313510,
        "title": "GAMCO Global Gold, Natural Resources & Income Trust"
    },
    "LYEL": {
        "cik": 1806952,
        "title": "Lyell Immunopharma, Inc."
    },
    "JRVR": {
        "cik": 1620459,
        "title": "James River Group Holdings, Ltd."
    },
    "DWAC": {
        "cik": 1849635,
        "title": "Digital World Acquisition Corp."
    },
    "AMAL": {
        "cik": 1823608,
        "title": "Amalgamated Financial Corp."
    },
    "ZEUS": {
        "cik": 917470,
        "title": "OLYMPIC STEEL INC"
    },
    "SCWX": {
        "cik": 1468666,
        "title": "SecureWorks Corp"
    },
    "ASC": {
        "cik": 1577437,
        "title": "Ardmore Shipping Corp"
    },
    "HFRO": {
        "cik": 1710680,
        "title": "HIGHLAND OPPORTUNITIES & INCOME FUND"
    },
    "CLSK": {
        "cik": 827876,
        "title": "CLEANSPARK, INC."
    },
    "MODV": {
        "cik": 1220754,
        "title": "ModivCare Inc"
    },
    "TBPH": {
        "cik": 1583107,
        "title": "Theravance Biopharma, Inc."
    },
    "ATRO": {
        "cik": 8063,
        "title": "ASTRONICS CORP"
    },
    "EBF": {
        "cik": 33002,
        "title": "ENNIS, INC."
    },
    "GPRK": {
        "cik": 1464591,
        "title": "GeoPark Ltd"
    },
    "LAW": {
        "cik": 1625641,
        "title": "CS Disco, Inc."
    },
    "EXK": {
        "cik": 1277866,
        "title": "ENDEAVOUR SILVER CORP"
    },
    "OBE": {
        "cik": 1334388,
        "title": "OBSIDIAN ENERGY LTD."
    },
    "YSG": {
        "cik": 1819580,
        "title": "Yatsen Holding Ltd"
    },
    "BHK": {
        "cik": 1160864,
        "title": "BLACKROCK CORE BOND TRUST"
    },
    "BME": {
        "cik": 1314966,
        "title": "BlackRock Health Sciences Trust"
    },
    "BIT": {
        "cik": 1562818,
        "title": "BlackRock Multi-Sector Income Trust"
    },
    "LAND": {
        "cik": 1495240,
        "title": "GLADSTONE LAND Corp"
    },
    "AGX": {
        "cik": 100591,
        "title": "ARGAN INC"
    },
    "TRST": {
        "cik": 357301,
        "title": "TRUSTCO BANK CORP N Y"
    },
    "HTBK": {
        "cik": 1053352,
        "title": "HERITAGE COMMERCE CORP"
    },
    "GCBC": {
        "cik": 1070524,
        "title": "GREENE COUNTY BANCORP INC"
    },
    "HSII": {
        "cik": 1066605,
        "title": "HEIDRICK & STRUGGLES INTERNATIONAL INC"
    },
    "MTW": {
        "cik": 61986,
        "title": "MANITOWOC CO INC"
    },
    "SHYF": {
        "cik": 743238,
        "title": "SHYFT GROUP, INC."
    },
    "WBX": {
        "cik": 1866501,
        "title": "Wallbox N.V."
    },
    "TRDA": {
        "cik": 1689375,
        "title": "Entrada Therapeutics, Inc."
    },
    "VTRU": {
        "cik": 1805012,
        "title": "Vitru Ltd"
    },
    "DENN": {
        "cik": 852772,
        "title": "DENNY'S Corp"
    },
    "CABA": {
        "cik": 1759138,
        "title": "Cabaletta Bio, Inc."
    },
    "CTLP": {
        "cik": 896429,
        "title": "CANTALOUPE, INC."
    },
    "QNST": {
        "cik": 1117297,
        "title": "QUINSTREET, INC"
    },
    "SRDX": {
        "cik": 924717,
        "title": "SURMODICS INC"
    },
    "AMOT": {
        "cik": 46129,
        "title": "ALLIED MOTION TECHNOLOGIES INC"
    },
    "GAMB": {
        "cik": 1839799,
        "title": "Gambling.com Group Ltd"
    },
    "UVSP": {
        "cik": 102212,
        "title": "UNIVEST FINANCIAL Corp"
    },
    "RERE": {
        "cik": 1838957,
        "title": "ATRenew Inc."
    },
    "EOLS": {
        "cik": 1570562,
        "title": "Evolus, Inc."
    },
    "MBWM": {
        "cik": 1042729,
        "title": "MERCANTILE BANK CORP"
    },
    "HAFC": {
        "cik": 1109242,
        "title": "HANMI FINANCIAL CORP"
    },
    "BWMX": {
        "cik": 1788257,
        "title": "BETTERWARE DE MEXICO, S.A.P.I. DE C.V"
    },
    "EMD": {
        "cik": 1227862,
        "title": "WESTERN ASSET EMERGING MARKETS DEBT FUND INC."
    },
    "FRPH": {
        "cik": 844059,
        "title": "FRP HOLDINGS, INC."
    },
    "ETJ": {
        "cik": 1395325,
        "title": "Eaton Vance Risk-Managed Diversified Equity Income Fund"
    },
    "HIBB": {
        "cik": 1017480,
        "title": "HIBBETT INC"
    },
    "ME": {
        "cik": 1804591,
        "title": "23andMe Holding Co."
    },
    "IIM": {
        "cik": 885601,
        "title": "Invesco Value Municipal Income Trust"
    },
    "CASS": {
        "cik": 708781,
        "title": "CASS INFORMATION SYSTEMS INC"
    },
    "JANX": {
        "cik": 1817713,
        "title": "Janux Therapeutics, Inc."
    },
    "RGP": {
        "cik": 1084765,
        "title": "RESOURCES CONNECTION, INC."
    },
    "CFB": {
        "cik": 1458412,
        "title": "CROSSFIRST BANKSHARES, INC."
    },
    "ANAB": {
        "cik": 1370053,
        "title": "ANAPTYSBIO, INC"
    },
    "ML": {
        "cik": 1807846,
        "title": "MONEYLION INC."
    },
    "BGY": {
        "cik": 1393299,
        "title": "BlackRock Enhanced International Dividend Trust"
    },
    "CRBU": {
        "cik": 1619856,
        "title": "Caribou Biosciences, Inc."
    },
    "NPK": {
        "cik": 80172,
        "title": "NATIONAL PRESTO INDUSTRIES INC"
    },
    "BOC": {
        "cik": 1494582,
        "title": "BOSTON OMAHA Corp"
    },
    "ACRE": {
        "cik": 1529377,
        "title": "Ares Commercial Real Estate Corp"
    },
    "DESP": {
        "cik": 1703141,
        "title": "Despegar.com, Corp."
    },
    "ISPR": {
        "cik": 1948455,
        "title": "Ispire Technology Inc."
    },
    "WIW": {
        "cik": 1267902,
        "title": "WESTERN ASSET INFLATION-LINKED OPPORTUNITIES & INCOME FUND"
    },
    "GOOD": {
        "cik": 1234006,
        "title": "GLADSTONE COMMERCIAL CORP"
    },
    "HUYA": {
        "cik": 1728190,
        "title": "HUYA Inc."
    },
    "CCD": {
        "cik": 1602584,
        "title": "Calamos Dynamic Convertible & Income Fund"
    },
    "HUT": {
        "cik": 1731805,
        "title": "HUT 8 MINING CORP."
    },
    "ACRS": {
        "cik": 1557746,
        "title": "Aclaris Therapeutics, Inc."
    },
    "VINP": {
        "cik": 1826286,
        "title": "Vinci Partners Investments Ltd."
    },
    "EYPT": {
        "cik": 1314102,
        "title": "EyePoint Pharmaceuticals, Inc."
    },
    "RWAY": {
        "cik": 1653384,
        "title": "Runway Growth Finance Corp."
    },
    "GCT": {
        "cik": 1857816,
        "title": "GigaCloud Technology Inc"
    },
    "BTO": {
        "cik": 925683,
        "title": "JOHN HANCOCK FINANCIAL OPPORTUNITIES FUND"
    },
    "SYTA": {
        "cik": 1649009,
        "title": "Siyata Mobile Inc."
    },
    "TRTX": {
        "cik": 1630472,
        "title": "TPG RE Finance Trust, Inc."
    },
    "TIGR": {
        "cik": 1756699,
        "title": "UP Fintech Holding Ltd"
    },
    "RUPRF": {
        "cik": 1010000,
        "title": "RUPERT RESOURCES LTD"
    },
    "MVST": {
        "cik": 1760689,
        "title": "Microvast Holdings, Inc."
    },
    "NKX": {
        "cik": 1195738,
        "title": "NUVEEN CALIFORNIA AMT-FREE QUALITY MUNICIPAL INCOME FUND"
    },
    "CCBG": {
        "cik": 726601,
        "title": "CAPITAL CITY BANK GROUP INC"
    },
    "PFLT": {
        "cik": 1504619,
        "title": "PennantPark Floating Rate Capital Ltd."
    },
    "HVT": {
        "cik": 216085,
        "title": "HAVERTY FURNITURE COMPANIES INC"
    },
    "KRNY": {
        "cik": 1617242,
        "title": "Kearny Financial Corp."
    },
    "LIND": {
        "cik": 1512499,
        "title": "LINDBLAD EXPEDITIONS HOLDINGS, INC."
    },
    "PGC": {
        "cik": 1050743,
        "title": "PEAPACK GLADSTONE FINANCIAL CORP"
    },
    "IAUX": {
        "cik": 1853962,
        "title": "i-80 Gold Corp."
    },
    "NFBK": {
        "cik": 1493225,
        "title": "Northfield Bancorp, Inc."
    },
    "LDP": {
        "cik": 1548717,
        "title": "Cohen & Steers Ltd Duration Preferred & Income Fund, Inc."
    },
    "DIAX": {
        "cik": 1608742,
        "title": "Nuveen Dow 30sm Dynamic Overwrite Fund"
    },
    "NLST": {
        "cik": 1282631,
        "title": "NETLIST INC"
    },
    "TRIN": {
        "cik": 1786108,
        "title": "Trinity Capital Inc."
    },
    "STKL": {
        "cik": 351834,
        "title": "SunOpta Inc."
    },
    "SNBR": {
        "cik": 827187,
        "title": "Sleep Number Corp"
    },
    "CMPO": {
        "cik": 1823144,
        "title": "CompoSecure, Inc."
    },
    "MAX": {
        "cik": 1818383,
        "title": "MediaAlpha, Inc."
    },
    "ATLC": {
        "cik": 1464343,
        "title": "Atlanticus Holdings Corp"
    },
    "XPER": {
        "cik": 1788999,
        "title": "Xperi Inc."
    },
    "SMBC": {
        "cik": 916907,
        "title": "SOUTHERN MISSOURI BANCORP, INC."
    },
    "LEGH": {
        "cik": 1436208,
        "title": "Legacy Housing Corp"
    },
    "THW": {
        "cik": 1635977,
        "title": "Tekla World Healthcare Fund"
    },
    "EGY": {
        "cik": 894627,
        "title": "VAALCO ENERGY INC /DE/"
    },
    "SVRA": {
        "cik": 1160308,
        "title": "Savara Inc"
    },
    "RMAX": {
        "cik": 1581091,
        "title": "RE/MAX Holdings, Inc."
    },
    "PVNC": {
        "cik": 1134982,
        "title": "PREVENTION INSURANCE COM"
    },
    "DHIL": {
        "cik": 909108,
        "title": "DIAMOND HILL INVESTMENT GROUP INC"
    },
    "SOUN": {
        "cik": 1840856,
        "title": "SOUNDHOUND AI, INC."
    },
    "UFCS": {
        "cik": 101199,
        "title": "UNITED FIRE GROUP INC"
    },
    "NGL": {
        "cik": 1504461,
        "title": "NGL Energy Partners LP"
    },
    "VGM": {
        "cik": 880892,
        "title": "Invesco Trust for Investment Grade Municipals"
    },
    "SCLX": {
        "cik": 1820190,
        "title": "Scilex Holding Co"
    },
    "FTHY": {
        "cik": 1810523,
        "title": "FIRST TRUST HIGH YIELD OPPORTUNITIES 2027 TERM FUND"
    },
    "BFST": {
        "cik": 1624322,
        "title": "Business First Bancshares, Inc."
    },
    "VKQ": {
        "cik": 877463,
        "title": "Invesco Municipal Trust"
    },
    "KRT": {
        "cik": 1758021,
        "title": "Karat Packaging Inc."
    },
    "GUT": {
        "cik": 1080720,
        "title": "GABELLI UTILITY TRUST"
    },
    "MCBS": {
        "cik": 1747068,
        "title": "MetroCity Bankshares, Inc."
    },
    "VITL": {
        "cik": 1579733,
        "title": "Vital Farms, Inc."
    },
    "LASR": {
        "cik": 1124796,
        "title": "NLIGHT, INC."
    },
    "GENK": {
        "cik": 1891856,
        "title": "GEN Restaurant Group, Inc."
    },
    "SOI": {
        "cik": 1697500,
        "title": "Solaris Oilfield Infrastructure, Inc."
    },
    "HBNC": {
        "cik": 706129,
        "title": "HORIZON BANCORP INC /IN/"
    },
    "MITK": {
        "cik": 807863,
        "title": "MITEK SYSTEMS INC"
    },
    "MCS": {
        "cik": 62234,
        "title": "MARCUS CORP"
    },
    "AGEN": {
        "cik": 1098972,
        "title": "AGENUS INC"
    },
    "CAC": {
        "cik": 750686,
        "title": "CAMDEN NATIONAL CORP"
    },
    "AERG": {
        "cik": 879911,
        "title": "APPLIED ENERGETICS, INC."
    },
    "MLYS": {
        "cik": 1933414,
        "title": "Mineralys Therapeutics, Inc."
    },
    "PDT": {
        "cik": 855886,
        "title": "JOHN HANCOCK PREMIUM DIVIDEND FUND"
    },
    "IFN": {
        "cik": 917100,
        "title": "INDIA FUND, INC."
    },
    "HEPS": {
        "cik": 1850235,
        "title": "D-MARKET Electronic Services & Trading"
    },
    "BGB": {
        "cik": 1546429,
        "title": "Blackstone Strategic Credit 2027 Term Fund"
    },
    "CEM": {
        "cik": 1488775,
        "title": "ClearBridge MLP & Midstream Fund Inc."
    },
    "BROG": {
        "cik": 1774983,
        "title": "Brooge Energy Ltd"
    },
    "OIS": {
        "cik": 1121484,
        "title": "OIL STATES INTERNATIONAL, INC"
    },
    "IGIC": {
        "cik": 1794338,
        "title": "International General Insurance Holdings Ltd."
    },
    "RBBN": {
        "cik": 1708055,
        "title": "Ribbon Communications Inc."
    },
    "OCS": {
        "cik": 1953530,
        "title": "Oculis Holding AG"
    },
    "ACCO": {
        "cik": 712034,
        "title": "ACCO BRANDS Corp"
    },
    "FLWS": {
        "cik": 1084869,
        "title": "1 800 FLOWERS COM INC"
    },
    "AMCX": {
        "cik": 1514991,
        "title": "AMC Networks Inc."
    },
    "DM": {
        "cik": 1754820,
        "title": "Desktop Metal, Inc."
    },
    "VALU": {
        "cik": 717720,
        "title": "VALUE LINE INC"
    },
    "DDL": {
        "cik": 1854545,
        "title": "Dingdong (Cayman) Ltd"
    },
    "ZYME": {
        "cik": 1937653,
        "title": "Zymeworks Inc."
    },
    "SUPV": {
        "cik": 1517399,
        "title": "Grupo Supervielle S.A."
    },
    "ARTNA": {
        "cik": 863110,
        "title": "ARTESIAN RESOURCES CORP"
    },
    "SMR": {
        "cik": 1822966,
        "title": "NUSCALE POWER Corp"
    },
    "MSBI": {
        "cik": 1466026,
        "title": "Midland States Bancorp, Inc."
    },
    "QD": {
        "cik": 1692705,
        "title": "Qudian Inc."
    },
    "WASH": {
        "cik": 737468,
        "title": "WASHINGTON TRUST BANCORP INC"
    },
    "CEVA": {
        "cik": 1173489,
        "title": "CEVA INC"
    },
    "BLE": {
        "cik": 1176194,
        "title": "BLACKROCK MUNICIPAL INCOME TRUST II"
    },
    "OSUR": {
        "cik": 1116463,
        "title": "ORASURE TECHNOLOGIES INC"
    },
    "HOV": {
        "cik": 357294,
        "title": "HOVNANIAN ENTERPRISES INC"
    },
    "FDUS": {
        "cik": 1513363,
        "title": "FIDUS INVESTMENT Corp"
    },
    "TBLD": {
        "cik": 1820378,
        "title": "Thornburg Income Builder Opportunities Trust"
    },
    "SMWB": {
        "cik": 1842731,
        "title": "SIMILARWEB LTD."
    },
    "CSTL": {
        "cik": 1447362,
        "title": "CASTLE BIOSCIENCES INC"
    },
    "HCI": {
        "cik": 1400810,
        "title": "HCI Group, Inc."
    },
    "FMNB": {
        "cik": 709337,
        "title": "FARMERS NATIONAL BANC CORP /OH/"
    },
    "SCPL": {
        "cik": 1760717,
        "title": "SciPlay Corp"
    },
    "IQI": {
        "cik": 885125,
        "title": "Invesco Quality Municipal Income Trust"
    },
    "HLVX": {
        "cik": 1888012,
        "title": "HilleVax, Inc."
    },
    "ODC": {
        "cik": 74046,
        "title": "Oil-Dri Corp of America"
    },
    "UNTC": {
        "cik": 798949,
        "title": "UNIT CORP"
    },
    "BLFS": {
        "cik": 834365,
        "title": "BIOLIFE SOLUTIONS INC"
    },
    "NWBO": {
        "cik": 1072379,
        "title": "NORTHWEST BIOTHERAPEUTICS INC"
    },
    "LBC": {
        "cik": 1475348,
        "title": "Luther Burbank Corp"
    },
    "LILM": {
        "cik": 1855756,
        "title": "Lilium N.V."
    },
    "VPG": {
        "cik": 1487952,
        "title": "Vishay Precision Group, Inc."
    },
    "ABL": {
        "cik": 1814287,
        "title": "Abacus Life, Inc."
    },
    "WSR": {
        "cik": 1175535,
        "title": "Whitestone REIT"
    },
    "BOOM": {
        "cik": 34067,
        "title": "DMC Global Inc."
    },
    "URGN": {
        "cik": 1668243,
        "title": "UroGen Pharma Ltd."
    },
    "BUI": {
        "cik": 1528988,
        "title": "BlackRock Utilities, Infrastructure & Power Opportunities Trust"
    },
    "RXT": {
        "cik": 1810019,
        "title": "Rackspace Technology, Inc."
    },
    "EZPW": {
        "cik": 876523,
        "title": "EZCORP INC"
    },
    "DGICA": {
        "cik": 800457,
        "title": "DONEGAL GROUP INC"
    },
    "HA": {
        "cik": 1172222,
        "title": "HAWAIIAN HOLDINGS INC"
    },
    "PTSI": {
        "cik": 798287,
        "title": "PAM TRANSPORTATION SERVICES INC"
    },
    "OTMO": {
        "cik": 1842498,
        "title": "Otonomo Technologies Ltd."
    },
    "PERF": {
        "cik": 1899830,
        "title": "Perfect Corp."
    },
    "METC": {
        "cik": 1687187,
        "title": "Ramaco Resources, Inc."
    },
    "LND": {
        "cik": 1499849,
        "title": "BrasilAgro - Brazilian Agricultural Real Estate Co"
    },
    "MYD": {
        "cik": 879361,
        "title": "BLACKROCK MUNIYIELD FUND, INC."
    },
    "HCVI": {
        "cik": 1842937,
        "title": "Hennessy Capital Investment Corp. VI"
    },
    "BENF": {
        "cik": 1775734,
        "title": "Beneficient"
    },
    "VNET": {
        "cik": 1508475,
        "title": "VNET Group, Inc."
    },
    "HDSN": {
        "cik": 925528,
        "title": "HUDSON TECHNOLOGIES INC /NY"
    },
    "CALT": {
        "cik": 1795579,
        "title": "Calliditas Therapeutics AB"
    },
    "BLW": {
        "cik": 1233681,
        "title": "BLACKROCK Ltd DURATION INCOME TRUST"
    },
    "CDNA": {
        "cik": 1217234,
        "title": "CareDx, Inc."
    },
    "TBI": {
        "cik": 768899,
        "title": "TrueBlue, Inc."
    },
    "NXJ": {
        "cik": 1087786,
        "title": "NUVEEN NEW JERSEY QUALITY MUNICIPAL INCOME FUND"
    },
    "NR": {
        "cik": 71829,
        "title": "NEWPARK RESOURCES INC"
    },
    "NNOX": {
        "cik": 1795251,
        "title": "Nano-X Imaging Ltd."
    },
    "MMD": {
        "cik": 1518557,
        "title": "MainStay MacKay DefinedTerm Municipal Opportunities Fund"
    },
    "STK": {
        "cik": 1471420,
        "title": "Columbia Seligman Premium Technology Growth Fund, Inc."
    },
    "BFAC": {
        "cik": 1880441,
        "title": "Battery Future Acquisition Corp."
    },
    "PXPC": {
        "cik": 1785493,
        "title": "Phoenix Plus Corp."
    },
    "MVIS": {
        "cik": 65770,
        "title": "MICROVISION, INC."
    },
    "TARS": {
        "cik": 1819790,
        "title": "Tarsus Pharmaceuticals, Inc."
    },
    "MCB": {
        "cik": 1476034,
        "title": "Metropolitan Bank Holding Corp."
    },
    "DSU": {
        "cik": 1051003,
        "title": "BLACKROCK DEBT STRATEGIES FUND, INC."
    },
    "CNSL": {
        "cik": 1304421,
        "title": "Consolidated Communications Holdings, Inc."
    },
    "GBLI": {
        "cik": 1494904,
        "title": "Global Indemnity Group, LLC"
    },
    "HONE": {
        "cik": 1769617,
        "title": "HarborOne Bancorp, Inc."
    },
    "CPF": {
        "cik": 701347,
        "title": "CENTRAL PACIFIC FINANCIAL CORP"
    },
    "DAO": {
        "cik": 1781753,
        "title": "Youdao, Inc."
    },
    "EWTX": {
        "cik": 1710072,
        "title": "Edgewise Therapeutics, Inc."
    },
    "MCRB": {
        "cik": 1609809,
        "title": "Seres Therapeutics, Inc."
    },
    "YUMM": {
        "cik": 1073748,
        "title": "YUMMIES INC"
    },
    "CSV": {
        "cik": 1016281,
        "title": "CARRIAGE SERVICES INC"
    },
    "DBO": {
        "cik": 1383058,
        "title": "Invesco DB Oil Fund"
    },
    "MYPS": {
        "cik": 1823878,
        "title": "PLAYSTUDIOS, Inc."
    },
    "LYTS": {
        "cik": 763532,
        "title": "LSI INDUSTRIES INC"
    },
    "SPFI": {
        "cik": 1163668,
        "title": "SOUTH PLAINS FINANCIAL, INC."
    },
    "JFR": {
        "cik": 1276533,
        "title": "NUVEEN FLOATING RATE INCOME FUND"
    },
    "GHY": {
        "cik": 1554697,
        "title": "PGIM Global High Yield Fund, Inc."
    },
    "LEV": {
        "cik": 1834974,
        "title": "Lion Electric Co"
    },
    "CLDT": {
        "cik": 1476045,
        "title": "Chatham Lodging Trust"
    },
    "CECO": {
        "cik": 3197,
        "title": "CECO ENVIRONMENTAL CORP"
    },
    "CPAC": {
        "cik": 1221029,
        "title": "CEMENTOS PACASMAYO SAA"
    },
    "GUG": {
        "cik": 1864208,
        "title": "Guggenheim Active Allocation Fund"
    },
    "AATP": {
        "cik": 1713210,
        "title": "Agape ATP Corp"
    },
    "THRN": {
        "cik": 1844280,
        "title": "Thorne Healthtech, Inc."
    },
    "GRVY": {
        "cik": 1313310,
        "title": "GRAVITY Co., Ltd."
    },
    "SFWL": {
        "cik": 1863218,
        "title": "SHENGFENG DEVELOPMENT Ltd"
    },
    "AIRS": {
        "cik": 1870940,
        "title": "Airsculpt Technologies, Inc."
    },
    "CYD": {
        "cik": 932695,
        "title": "CHINA YUCHAI INTERNATIONAL LTD"
    },
    "MCFT": {
        "cik": 1638290,
        "title": "MasterCraft Boat Holdings, Inc."
    },
    "NFYS": {
        "cik": 1850502,
        "title": "Enphys Acquisition Corp."
    },
    "APLM": {
        "cik": 1944885,
        "title": "Apollomics Inc."
    },
    "EBIX": {
        "cik": 814549,
        "title": "EBIX INC"
    },
    "TRTL": {
        "cik": 1847112,
        "title": "TortoiseEcofin Acquisition Corp. III"
    },
    "ALTG": {
        "cik": 1759824,
        "title": "ALTA EQUIPMENT GROUP INC."
    },
    "SVM": {
        "cik": 1340677,
        "title": "SILVERCORP METALS INC"
    },
    "MLR": {
        "cik": 924822,
        "title": "MILLER INDUSTRIES INC /TN/"
    },
    "LQDA": {
        "cik": 1819576,
        "title": "Liquidia Corp"
    },
    "AVD": {
        "cik": 5981,
        "title": "AMERICAN VANGUARD CORP"
    },
    "OSPN": {
        "cik": 1044777,
        "title": "OneSpan Inc."
    },
    "TRC": {
        "cik": 96869,
        "title": "TEJON RANCH CO"
    },
    "CDLX": {
        "cik": 1666071,
        "title": "Cardlytics, Inc."
    },
    "MBI": {
        "cik": 814585,
        "title": "MBIA INC"
    },
    "CRD-A": {
        "cik": 25475,
        "title": "CRAWFORD & CO"
    },
    "PACK": {
        "cik": 1712463,
        "title": "Ranpak Holdings Corp."
    },
    "THFF": {
        "cik": 714562,
        "title": "FIRST FINANCIAL CORP /IN/"
    },
    "VCV": {
        "cik": 895531,
        "title": "Invesco California Value Municipal Income Trust"
    },
    "CYH": {
        "cik": 1108109,
        "title": "COMMUNITY HEALTH SYSTEMS INC"
    },
    "INRE": {
        "cik": 1528985,
        "title": "Inland Real Estate Income Trust, Inc."
    },
    "AAOI": {
        "cik": 1158114,
        "title": "APPLIED OPTOELECTRONICS, INC."
    },
    "ARQT": {
        "cik": 1787306,
        "title": "Arcutis Biotherapeutics, Inc."
    },
    "GCI": {
        "cik": 1579684,
        "title": "Gannett Co., Inc."
    },
    "NBB": {
        "cik": 1478888,
        "title": "Nuveen Taxable Municipal Income Fund"
    },
    "SUAC": {
        "cik": 1885461,
        "title": "ShoulderUP Technology Acquisition Corp."
    },
    "AMRN": {
        "cik": 897448,
        "title": "AMARIN CORP PLC\\UK"
    },
    "EGLE": {
        "cik": 1322439,
        "title": "Eagle Bulk Shipping Inc."
    },
    "SWIM": {
        "cik": 1833197,
        "title": "Latham Group, Inc."
    },
    "ACRO": {
        "cik": 1847891,
        "title": "Acropolis Infrastructure Acquisition Corp."
    },
    "WVE": {
        "cik": 1631574,
        "title": "Wave Life Sciences Ltd."
    },
    "AMPX": {
        "cik": 1899287,
        "title": "Amprius Technologies, Inc."
    },
    "HPS": {
        "cik": 1215913,
        "title": "JOHN HANCOCK PREFERRED INCOME FUND III"
    },
    "PROC": {
        "cik": 1863362,
        "title": "Procaps Group, S.A."
    },
    "ALDX": {
        "cik": 1341235,
        "title": "Aldeyra Therapeutics, Inc."
    },
    "TPC": {
        "cik": 77543,
        "title": "TUTOR PERINI CORP"
    },
    "SNDL": {
        "cik": 1766600,
        "title": "SNDL Inc."
    },
    "FRA": {
        "cik": 1259708,
        "title": "BLACKROCK FLOATING RATE INCOME STRATEGIES FUND, INC."
    },
    "LXRX": {
        "cik": 1062822,
        "title": "LEXICON PHARMACEUTICALS, INC."
    },
    "ICPT": {
        "cik": 1270073,
        "title": "INTERCEPT PHARMACEUTICALS, INC."
    },
    "NRGV": {
        "cik": 1828536,
        "title": "Energy Vault Holdings, Inc."
    },
    "BWMN": {
        "cik": 1847590,
        "title": "Bowman Consulting Group Ltd."
    },
    "CHRS": {
        "cik": 1512762,
        "title": "Coherus BioSciences, Inc."
    },
    "ASGI": {
        "cik": 1793855,
        "title": "abrdn Global Infrastructure Income Fund"
    },
    "FPH": {
        "cik": 1574197,
        "title": "Five Point Holdings, LLC"
    },
    "NEWT": {
        "cik": 1587987,
        "title": "NewtekOne, Inc."
    },
    "IVR": {
        "cik": 1437071,
        "title": "Invesco Mortgage Capital Inc."
    },
    "RPTX": {
        "cik": 1808158,
        "title": "Repare Therapeutics Inc."
    },
    "BFK": {
        "cik": 1137393,
        "title": "BLACKROCK MUNICIPAL INCOME TRUST"
    },
    "TPB": {
        "cik": 1290677,
        "title": "Turning Point Brands, Inc."
    },
    "SRG": {
        "cik": 1628063,
        "title": "Seritage Growth Properties"
    },
    "CATC": {
        "cik": 711772,
        "title": "CAMBRIDGE BANCORP"
    },
    "GAIN": {
        "cik": 1321741,
        "title": "GLADSTONE INVESTMENT CORPORATIONDE"
    },
    "QURE": {
        "cik": 1590560,
        "title": "uniQure N.V."
    },
    "PNNT": {
        "cik": 1383414,
        "title": "PENNANTPARK INVESTMENT CORP"
    },
    "SFIX": {
        "cik": 1576942,
        "title": "Stitch Fix, Inc."
    },
    "KVSA": {
        "cik": 1841873,
        "title": "Khosla Ventures Acquisition Co."
    },
    "SLAM": {
        "cik": 1838162,
        "title": "Slam Corp."
    },
    "WULF": {
        "cik": 1083301,
        "title": "TERAWULF INC."
    },
    "ONEW": {
        "cik": 1772921,
        "title": "OneWater Marine Inc."
    },
    "BW": {
        "cik": 1630805,
        "title": "Babcock & Wilcox Enterprises, Inc."
    },
    "SGU": {
        "cik": 1002590,
        "title": "STAR GROUP, L.P."
    },
    "FFIC": {
        "cik": 923139,
        "title": "FLUSHING FINANCIAL CORP"
    },
    "NN": {
        "cik": 1865631,
        "title": "NEXTNAV INC."
    },
    "AMNB": {
        "cik": 741516,
        "title": "AMERICAN NATIONAL BANKSHARES INC."
    },
    "SKE": {
        "cik": 1713748,
        "title": "Skeena Resources Ltd"
    },
    "FFWM": {
        "cik": 1413837,
        "title": "First Foundation Inc."
    },
    "GNE": {
        "cik": 1528356,
        "title": "Genie Energy Ltd."
    },
    "TCMD": {
        "cik": 1027838,
        "title": "TACTILE SYSTEMS TECHNOLOGY INC"
    },
    "MVF": {
        "cik": 835948,
        "title": "BLACKROCK MUNIVEST FUND, INC."
    },
    "BBCP": {
        "cik": 1703956,
        "title": "Concrete Pumping Holdings, Inc."
    },
    "RMT": {
        "cik": 912147,
        "title": "ROYCE MICRO-CAP TRUST, INC."
    },
    "NETI": {
        "cik": 1587264,
        "title": "ENETI INC."
    },
    "NRIX": {
        "cik": 1549595,
        "title": "Nurix Therapeutics, Inc."
    },
    "ORC": {
        "cik": 1518621,
        "title": "Orchid Island Capital, Inc."
    },
    "VEL": {
        "cik": 1692376,
        "title": "Velocity Financial, Inc."
    },
    "IHRT": {
        "cik": 1400891,
        "title": "iHeartMedia, Inc."
    },
    "MMU": {
        "cik": 886043,
        "title": "WESTERN ASSET MANAGED MUNICIPALS FUND INC."
    },
    "ITOS": {
        "cik": 1808865,
        "title": "iTeos Therapeutics, Inc."
    },
    "EOSE": {
        "cik": 1805077,
        "title": "Eos Energy Enterprises, Inc."
    },
    "DJCO": {
        "cik": 783412,
        "title": "DAILY JOURNAL CORP"
    },
    "CGEM": {
        "cik": 1789972,
        "title": "Cullinan Oncology, Inc."
    },
    "QSG": {
        "cik": 1932770,
        "title": "QuantaSing Group Ltd"
    },
    "NEGG": {
        "cik": 1474627,
        "title": "Newegg Commerce, Inc."
    },
    "TSE": {
        "cik": 1519061,
        "title": "Trinseo PLC"
    },
    "RTC": {
        "cik": 1381074,
        "title": "Baijiayun Group Ltd"
    },
    "CMPS": {
        "cik": 1816590,
        "title": "COMPASS Pathways plc"
    },
    "PGEN": {
        "cik": 1356090,
        "title": "PRECIGEN, INC."
    },
    "UVE": {
        "cik": 891166,
        "title": "UNIVERSAL INSURANCE HOLDINGS, INC."
    },
    "VYGR": {
        "cik": 1640266,
        "title": "Voyager Therapeutics, Inc."
    },
    "OLP": {
        "cik": 712770,
        "title": "ONE LIBERTY PROPERTIES INC"
    },
    "RCEL": {
        "cik": 1762303,
        "title": "AVITA Medical, Inc."
    },
    "DDI": {
        "cik": 1799567,
        "title": "DoubleDown Interactive Co., Ltd."
    },
    "GIM": {
        "cik": 828803,
        "title": "TEMPLETON GLOBAL INCOME FUND"
    },
    "LSEA": {
        "cik": 1721386,
        "title": "Landsea Homes Corp"
    },
    "ASPN": {
        "cik": 1145986,
        "title": "ASPEN AEROGELS INC"
    },
    "MULN": {
        "cik": 1499961,
        "title": "MULLEN AUTOMOTIVE INC."
    },
    "MTLS": {
        "cik": 1091223,
        "title": "MATERIALISE NV"
    },
    "HTBI": {
        "cik": 1538263,
        "title": "HomeTrust Bancshares, Inc."
    },
    "OPY": {
        "cik": 791963,
        "title": "OPPENHEIMER HOLDINGS INC"
    },
    "NCMI": {
        "cik": 1377630,
        "title": "National CineMedia, Inc."
    },
    "NQP": {
        "cik": 870780,
        "title": "NUVEEN PENNSYLVANIA QUALITY MUNICIPAL INCOME FUND"
    },
    "ALVR": {
        "cik": 1754068,
        "title": "Allovir, Inc."
    },
    "ICG": {
        "cik": 1895597,
        "title": "Intchains Group Ltd"
    },
    "RRAC": {
        "cik": 1860879,
        "title": "Rigel Resource Acquisition Corp."
    },
    "EMO": {
        "cik": 1517518,
        "title": "ClearBridge Energy Midstream Opportunity Fund Inc."
    },
    "HPI": {
        "cik": 1176199,
        "title": "JOHN HANCOCK PREFERRED INCOME FUND"
    },
    "PLM": {
        "cik": 866028,
        "title": "POLYMET MINING CORP"
    },
    "IBCP": {
        "cik": 39311,
        "title": "INDEPENDENT BANK CORP /MI/"
    },
    "IGD": {
        "cik": 1285890,
        "title": "Voya GLOBAL EQUITY DIVIDEND & PREMIUM OPPORTUNITY FUND"
    },
    "AVTE": {
        "cik": 1798749,
        "title": "Aerovate Therapeutics, Inc."
    },
    "ISD": {
        "cik": 1534880,
        "title": "PGIM High Yield Bond Fund, Inc."
    },
    "ORIC": {
        "cik": 1796280,
        "title": "Oric Pharmaceuticals, Inc."
    },
    "BCHPY": {
        "cik": 1887388,
        "title": "Brainchip Holdings Limited/ADR"
    },
    "VTNR": {
        "cik": 890447,
        "title": "Vertex Energy Inc."
    },
    "LUNG": {
        "cik": 1127537,
        "title": "Pulmonx Corp"
    },
    "CWCO": {
        "cik": 928340,
        "title": "Consolidated Water Co. Ltd."
    },
    "HYAC": {
        "cik": 1970509,
        "title": "Haymaker Acquisition Corp. 4"
    },
    "CAN": {
        "cik": 1780652,
        "title": "Canaan Inc."
    },
    "TROO": {
        "cik": 1412095,
        "title": "Troops, Inc. /Cayman Islands/"
    },
    "TAST": {
        "cik": 809248,
        "title": "CARROLS RESTAURANT GROUP, INC."
    },
    "NML": {
        "cik": 1562051,
        "title": "Neuberger Berman Energy Infrastructure & Income Fund Inc."
    },
    "DSX": {
        "cik": 1318885,
        "title": "DIANA SHIPPING INC."
    },
    "EVC": {
        "cik": 1109116,
        "title": "ENTRAVISION COMMUNICATIONS CORP"
    },
    "EQBK": {
        "cik": 1227500,
        "title": "EQUITY BANCSHARES INC"
    },
    "SMBK": {
        "cik": 1038773,
        "title": "SMARTFINANCIAL INC."
    },
    "AVK": {
        "cik": 1219120,
        "title": "ADVENT CONVERTIBLE & INCOME FUND"
    },
    "GLRE": {
        "cik": 1385613,
        "title": "GREENLIGHT CAPITAL RE, LTD."
    },
    "ERAS": {
        "cik": 1761918,
        "title": "Erasca, Inc."
    },
    "NXDT": {
        "cik": 1356115,
        "title": "NEXPOINT DIVERSIFIED REAL ESTATE TRUST"
    },
    "ESQ": {
        "cik": 1531031,
        "title": "Esquire Financial Holdings, Inc."
    },
    "CCNE": {
        "cik": 736772,
        "title": "CNB FINANCIAL CORP/PA"
    },
    "MBSC": {
        "cik": 1856589,
        "title": "M3-Brigade Acquisition III Corp."
    },
    "FSBC": {
        "cik": 1275168,
        "title": "FIVE STAR BANCORP"
    },
    "TDUP": {
        "cik": 1484778,
        "title": "ThredUp Inc."
    },
    "QUOT": {
        "cik": 1115128,
        "title": "Quotient Technology Inc."
    },
    "TGB": {
        "cik": 878518,
        "title": "TASEKO MINES LTD"
    },
    "NMAI": {
        "cik": 1861115,
        "title": "Nuveen Multi-Asset Income Fund"
    },
    "MXCT": {
        "cik": 1287098,
        "title": "MAXCYTE, INC."
    },
    "ABML": {
        "cik": 1576873,
        "title": "AMERICAN BATTERY TECHNOLOGY Co"
    },
    "EGHT": {
        "cik": 1023731,
        "title": "8X8 INC /DE/"
    },
    "BHB": {
        "cik": 743367,
        "title": "BAR HARBOR BANKSHARES"
    },
    "FRGE": {
        "cik": 1827821,
        "title": "Forge Global Holdings, Inc."
    },
    "BHRB": {
        "cik": 1964333,
        "title": "Burke & Herbert Financial Services Corp."
    },
    "ETB": {
        "cik": 1308927,
        "title": "Eaton Vance Tax-Managed Buy-Write Income Fund"
    },
    "JPI": {
        "cik": 1547994,
        "title": "Nuveen Preferred & Income Term Fund"
    },
    "CXAC": {
        "cik": 1856242,
        "title": "C5 Acquisition Corp"
    },
    "AURA": {
        "cik": 1501796,
        "title": "Aura Biosciences, Inc."
    },
    "SRRK": {
        "cik": 1727196,
        "title": "Scholar Rock Holding Corp"
    },
    "EVN": {
        "cik": 1074540,
        "title": "EATON VANCE MUNICIPAL INCOME TRUST"
    },
    "SLGC": {
        "cik": 1837412,
        "title": "SomaLogic, Inc."
    },
    "SENEA": {
        "cik": 88948,
        "title": "Seneca Foods Corp"
    },
    "AAN": {
        "cik": 1821393,
        "title": "Aaron's Company, Inc."
    },
    "ADSE": {
        "cik": 1879248,
        "title": "Ads-Tec Energy Public Ltd Co"
    },
    "NPFD": {
        "cik": 1865389,
        "title": "Nuveen Variable Rate Preferred & Income Fund"
    },
    "TPVG": {
        "cik": 1580345,
        "title": "TriplePoint Venture Growth BDC Corp."
    },
    "MRNS": {
        "cik": 1267813,
        "title": "MARINUS PHARMACEUTICALS, INC."
    },
    "HRZN": {
        "cik": 1487428,
        "title": "Horizon Technology Finance Corp"
    },
    "PLSE": {
        "cik": 1625101,
        "title": "Pulse Biosciences, Inc."
    },
    "NVEC": {
        "cik": 724910,
        "title": "NVE CORP /NEW/"
    },
    "SLDP": {
        "cik": 1844862,
        "title": "Solid Power, Inc."
    },
    "UHG": {
        "cik": 1830188,
        "title": "United Homes Group, Inc."
    },
    "GLAD": {
        "cik": 1143513,
        "title": "GLADSTONE CAPITAL CORP"
    },
    "APTM": {
        "cik": 1845550,
        "title": "Alpha Partners Technology Merger Corp."
    },
    "GCO": {
        "cik": 18498,
        "title": "GENESCO INC"
    },
    "KODK": {
        "cik": 31235,
        "title": "EASTMAN KODAK CO"
    },
    "XPDB": {
        "cik": 1855474,
        "title": "Power & Digital Infrastructure Acquisition II Corp."
    },
    "KALV": {
        "cik": 1348911,
        "title": "KalVista Pharmaceuticals, Inc."
    },
    "REI": {
        "cik": 1384195,
        "title": "RING ENERGY, INC."
    },
    "NREF": {
        "cik": 1786248,
        "title": "NexPoint Real Estate Finance, Inc."
    },
    "ABOS": {
        "cik": 1576885,
        "title": "Acumen Pharmaceuticals, Inc."
    },
    "NEWP": {
        "cik": 1369085,
        "title": "NEW PACIFIC METALS CORP"
    },
    "MYN": {
        "cik": 882150,
        "title": "BLACKROCK MUNIYIELD NEW YORK QUALITY FUND, INC."
    },
    "EXFY": {
        "cik": 1476840,
        "title": "Expensify, Inc."
    },
    "TRVG": {
        "cik": 1683825,
        "title": "trivago N.V."
    },
    "INOD": {
        "cik": 903651,
        "title": "INNODATA INC"
    },
    "CHW": {
        "cik": 1396277,
        "title": "Calamos Global Dynamic Income Fund"
    },
    "OLMA": {
        "cik": 1750284,
        "title": "Olema Pharmaceuticals, Inc."
    },
    "AMWL": {
        "cik": 1393584,
        "title": "American Well Corp"
    },
    "GILT": {
        "cik": 897322,
        "title": "GILAT SATELLITE NETWORKS LTD"
    },
    "NESR": {
        "cik": 1698514,
        "title": "National Energy Services Reunited Corp."
    },
    "CTO": {
        "cik": 23795,
        "title": "CTO Realty Growth, Inc."
    },
    "NETC": {
        "cik": 1854458,
        "title": "Nabors Energy Transition Corp."
    },
    "SHCR": {
        "cik": 1816233,
        "title": "Sharecare, Inc."
    },
    "ALRS": {
        "cik": 903419,
        "title": "ALERUS FINANCIAL CORP"
    },
    "PNTG": {
        "cik": 1766400,
        "title": "Pennant Group, Inc."
    },
    "STRW": {
        "cik": 1782430,
        "title": "Strawberry Fields REIT, Inc."
    },
    "EAD": {
        "cik": 1210123,
        "title": "ALLSPRING INCOME OPPORTUNITIES FUND"
    },
    "NAUT": {
        "cik": 1808805,
        "title": "Nautilus Biotechnology, Inc."
    },
    "SIFY": {
        "cik": 1094324,
        "title": "SIFY TECHNOLOGIES LTD"
    },
    "NUVB": {
        "cik": 1811063,
        "title": "Nuvation Bio Inc."
    },
    "AMSWA": {
        "cik": 713425,
        "title": "AMERICAN SOFTWARE INC"
    },
    "BLUE": {
        "cik": 1293971,
        "title": "bluebird bio, Inc."
    },
    "DSP": {
        "cik": 1828791,
        "title": "Viant Technology Inc."
    },
    "SDHY": {
        "cik": 1812923,
        "title": "PGIM Short Duration High Yield Opportunities Fund"
    },
    "SOHU": {
        "cik": 1734107,
        "title": "Sohu.com Ltd"
    },
    "RMR": {
        "cik": 1644378,
        "title": "RMR GROUP INC."
    },
    "NOTE": {
        "cik": 1823466,
        "title": "FiscalNote Holdings, Inc."
    },
    "MGTX": {
        "cik": 1735438,
        "title": "MeiraGTx Holdings plc"
    },
    "VHI": {
        "cik": 59255,
        "title": "VALHI INC /DE/"
    },
    "BFLY": {
        "cik": 1804176,
        "title": "Butterfly Network, Inc."
    },
    "LMB": {
        "cik": 1606163,
        "title": "Limbach Holdings, Inc."
    },
    "DAKT": {
        "cik": 915779,
        "title": "DAKTRONICS INC /SD/"
    },
    "PACI": {
        "cik": 1853070,
        "title": "PROOF Acquisition Corp I"
    },
    "ZUMZ": {
        "cik": 1318008,
        "title": "Zumiez Inc"
    },
    "ACTG": {
        "cik": 934549,
        "title": "ACACIA RESEARCH CORP"
    },
    "NFNT": {
        "cik": 1862327,
        "title": "Infinite Acquisition Corp."
    },
    "APGB": {
        "cik": 1838337,
        "title": "Apollo Strategic Growth Capital II"
    },
    "FSD": {
        "cik": 1494530,
        "title": "FIRST TRUST HIGH INCOME LONG/SHORT FUND"
    },
    "SHBI": {
        "cik": 1035092,
        "title": "SHORE BANCSHARES INC"
    },
    "BBW": {
        "cik": 1113809,
        "title": "BUILD-A-BEAR WORKSHOP INC"
    },
    "NTGR": {
        "cik": 1122904,
        "title": "NETGEAR, INC."
    },
    "EVE": {
        "cik": 1861121,
        "title": "EVe Mobility Acquisition Corp"
    },
    "CVRX": {
        "cik": 1235912,
        "title": "CVRx, Inc."
    },
    "ETO": {
        "cik": 1281926,
        "title": "Eaton Vance Tax-Advantaged Global Dividend Opportunities Fund"
    },
    "CBUS": {
        "cik": 1705843,
        "title": "Cibus, Inc."
    },
    "DPG": {
        "cik": 1515671,
        "title": "Duff & Phelps Utility & Infrastructure Fund Inc."
    },
    "HNRG": {
        "cik": 788965,
        "title": "HALLADOR ENERGY CO"
    },
    "KCGI": {
        "cik": 1865407,
        "title": "Kensington Capital Acquisition Corp. V"
    },
    "FEI": {
        "cik": 1556336,
        "title": "FIRST TRUST MLP & ENERGY INCOME FUND"
    },
    "MPB": {
        "cik": 879635,
        "title": "MID PENN BANCORP INC"
    },
    "ACP": {
        "cik": 1503290,
        "title": "abrdn Income Credit Strategies Fund"
    },
    "SB": {
        "cik": 1434754,
        "title": "SAFE BULKERS, INC."
    },
    "CNDA": {
        "cik": 1851959,
        "title": "Concord Acquisition Corp II"
    },
    "EBTC": {
        "cik": 1018399,
        "title": "ENTERPRISE BANCORP INC /MA/"
    },
    "DFP": {
        "cik": 1559991,
        "title": "Flaherty & Crumrine Dynamic Preferred & Income Fund Inc"
    },
    "BLEU": {
        "cik": 1843370,
        "title": "bleuacacia ltd"
    },
    "EMLD": {
        "cik": 1889123,
        "title": "FTAC Emerald Acquisition Corp."
    },
    "FMCC": {
        "cik": 1026214,
        "title": "FEDERAL HOME LOAN MORTGAGE CORP"
    },
    "NOTR": {
        "cik": 1784440,
        "title": "Nowtransit Inc"
    },
    "LOCO": {
        "cik": 1606366,
        "title": "El Pollo Loco Holdings, Inc."
    },
    "DTC": {
        "cik": 1870600,
        "title": "Solo Brands, Inc."
    },
    "VKI": {
        "cik": 908993,
        "title": "Invesco Advantage Municipal Income Trust II"
    },
    "LIFW": {
        "cik": 1802450,
        "title": "MSP Recovery, Inc."
    },
    "LEO": {
        "cik": 818972,
        "title": "BNY MELLON STRATEGIC MUNICIPALS, INC."
    },
    "THCH": {
        "cik": 1877333,
        "title": "TH International Ltd"
    },
    "HIO": {
        "cik": 910068,
        "title": "WESTERN ASSET HIGH INCOME OPPORTUNITY FUND INC."
    },
    "LOVE": {
        "cik": 1701758,
        "title": "Lovesac Co"
    },
    "QIWI": {
        "cik": 1561566,
        "title": "QIWI"
    },
    "GHI": {
        "cik": 1059142,
        "title": "Greystone Housing Impact Investors LP"
    },
    "PSTL": {
        "cik": 1759774,
        "title": "Postal Realty Trust, Inc."
    },
    "ARL": {
        "cik": 1102238,
        "title": "AMERICAN REALTY INVESTORS INC"
    },
    "BRT": {
        "cik": 14846,
        "title": "BRT Apartments Corp."
    },
    "RRBI": {
        "cik": 1071236,
        "title": "RED RIVER BANCSHARES INC"
    },
    "FFA": {
        "cik": 1291334,
        "title": "FIRST TRUST ENHANCED EQUITY INCOME FUND"
    },
    "HUMA": {
        "cik": 1818382,
        "title": "Humacyte, Inc."
    },
    "BGR": {
        "cik": 1306550,
        "title": "BlackRock Energy & Resources Trust"
    },
    "AKTX": {
        "cik": 1541157,
        "title": "Akari Therapeutics Plc"
    },
    "IGMS": {
        "cik": 1496323,
        "title": "IGM Biosciences, Inc."
    },
    "OTLK": {
        "cik": 1649989,
        "title": "Outlook Therapeutics, Inc."
    },
    "MX": {
        "cik": 1325702,
        "title": "MAGNACHIP SEMICONDUCTOR Corp"
    },
    "HQL": {
        "cik": 884121,
        "title": "TEKLA LIFE SCIENCES INVESTORS"
    },
    "PUYI": {
        "cik": 1750264,
        "title": "PUYI, INC."
    },
    "CJET": {
        "cik": 1957413,
        "title": "Chijet Motor Company, Inc."
    },
    "IONR": {
        "cik": 1896084,
        "title": "ioneer Ltd"
    },
    "EFR": {
        "cik": 1258623,
        "title": "EATON VANCE SENIOR FLOATING RATE TRUST"
    },
    "EFT": {
        "cik": 1288992,
        "title": "Eaton Vance Floating-Rate Income Trust"
    },
    "MOFG": {
        "cik": 1412665,
        "title": "MidWestOne Financial Group, Inc."
    },
    "GNTY": {
        "cik": 1058867,
        "title": "GUARANTY BANCSHARES INC /TX/"
    },
    "OOMA": {
        "cik": 1327688,
        "title": "OOMA INC"
    },
    "SGHT": {
        "cik": 1531177,
        "title": "Sight Sciences, Inc."
    },
    "SCU": {
        "cik": 1403256,
        "title": "Sculptor Capital Management, Inc."
    },
    "VLGEA": {
        "cik": 103595,
        "title": "VILLAGE SUPER MARKET INC"
    },
    "IBEX": {
        "cik": 1720420,
        "title": "IBEX Ltd"
    },
    "PPT": {
        "cik": 827773,
        "title": "PUTNAM PREMIER INCOME TRUST"
    },
    "PLCE": {
        "cik": 1041859,
        "title": "Childrens Place, Inc."
    },
    "SMMF": {
        "cik": 811808,
        "title": "SUMMIT FINANCIAL GROUP, INC."
    },
    "GEVO": {
        "cik": 1392380,
        "title": "Gevo, Inc."
    },
    "CGNT": {
        "cik": 1824814,
        "title": "Cognyte Software Ltd."
    },
    "EU": {
        "cik": 1500881,
        "title": "enCore Energy Corp."
    },
    "IVCA": {
        "cik": 1852889,
        "title": "Investcorp India Acquisition Corp"
    },
    "RSVR": {
        "cik": 1824403,
        "title": "Reservoir Media, Inc."
    },
    "BFZ": {
        "cik": 1137391,
        "title": "BLACKROCK CALIFORNIA MUNICIPAL INCOME TRUST"
    },
    "ABUS": {
        "cik": 1447028,
        "title": "Arbutus Biopharma Corp"
    },
    "BTMD": {
        "cik": 1819253,
        "title": "biote Corp."
    },
    "TYG": {
        "cik": 1268533,
        "title": "TORTOISE ENERGY INFRASTRUCTURE CORP"
    },
    "KMF": {
        "cik": 1500096,
        "title": "Kayne Anderson NextGen Energy & Infrastructure, Inc."
    },
    "PMVP": {
        "cik": 1699382,
        "title": "PMV Pharmaceuticals, Inc."
    },
    "TMC": {
        "cik": 1798562,
        "title": "TMC the metals Co Inc."
    },
    "SIGA": {
        "cik": 1010086,
        "title": "SIGA TECHNOLOGIES INC"
    },
    "FIP": {
        "cik": 1899883,
        "title": "FTAI Infrastructure Inc."
    },
    "GFGD": {
        "cik": 1876714,
        "title": "Growth for Good Acquisition Corp"
    },
    "PEGR": {
        "cik": 1847241,
        "title": "Project Energy Reimagined Acquisition Corp."
    },
    "VNDA": {
        "cik": 1347178,
        "title": "Vanda Pharmaceuticals Inc."
    },
    "TSP": {
        "cik": 1823593,
        "title": "TuSimple Holdings Inc."
    },
    "AUDC": {
        "cik": 1086434,
        "title": "AUDIOCODES LTD"
    },
    "LX": {
        "cik": 1708259,
        "title": "LexinFintech Holdings Ltd."
    },
    "CARE": {
        "cik": 1829576,
        "title": "Carter Bankshares, Inc."
    },
    "GBAB": {
        "cik": 1495825,
        "title": "Guggenheim Taxable Municipal Bond & Investment Grade Debt Trust"
    },
    "FANH": {
        "cik": 1413855,
        "title": "FANHUA INC."
    },
    "BAND": {
        "cik": 1514416,
        "title": "Bandwidth Inc."
    },
    "ORGO": {
        "cik": 1661181,
        "title": "Organogenesis Holdings Inc."
    },
    "SJT": {
        "cik": 319655,
        "title": "SAN JUAN BASIN ROYALTY TRUST"
    },
    "IPI": {
        "cik": 1421461,
        "title": "Intrepid Potash, Inc."
    },
    "BRLT": {
        "cik": 1866757,
        "title": "Brilliant Earth Group, Inc."
    },
    "QRTEA": {
        "cik": 1355096,
        "title": "Qurate Retail, Inc."
    },
    "NVX": {
        "cik": 1859795,
        "title": "NOVONIX Ltd"
    },
    "ANGO": {
        "cik": 1275187,
        "title": "ANGIODYNAMICS INC"
    },
    "UTMD": {
        "cik": 706698,
        "title": "UTAH MEDICAL PRODUCTS INC"
    },
    "PFTA": {
        "cik": 1853580,
        "title": "PORTAGE FINTECH ACQUISITION CORP."
    },
    "AWP": {
        "cik": 1390195,
        "title": "abrdn Global Premier Properties Fund"
    },
    "CRLBF": {
        "cik": 1832928,
        "title": "Cresco Labs Inc."
    },
    "INSE": {
        "cik": 1615063,
        "title": "Inspired Entertainment, Inc."
    },
    "SMTI": {
        "cik": 714256,
        "title": "Sanara MedTech Inc."
    },
    "RFMZ": {
        "cik": 1817159,
        "title": "RiverNorth Flexible Municipal Income Fund II, Inc."
    },
    "ENTA": {
        "cik": 1177648,
        "title": "ENANTA PHARMACEUTICALS INC"
    },
    "OPI": {
        "cik": 1456772,
        "title": "OFFICE PROPERTIES INCOME TRUST"
    },
    "PMO": {
        "cik": 900422,
        "title": "PUTNAM MUNICIPAL OPPORTUNITIES TRUST"
    },
    "CLIN": {
        "cik": 1883984,
        "title": "Clean Earth Acquisitions Corp."
    },
    "MUX": {
        "cik": 314203,
        "title": "McEwen Mining Inc."
    },
    "ONL": {
        "cik": 1873923,
        "title": "Orion Office REIT Inc."
    },
    "XERS": {
        "cik": 1867096,
        "title": "Xeris Biopharma Holdings, Inc."
    },
    "ICVX": {
        "cik": 1786255,
        "title": "Icosavax, Inc."
    },
    "KTF": {
        "cik": 839533,
        "title": "DWS MUNICIPAL INCOME TRUST"
    },
    "URG": {
        "cik": 1375205,
        "title": "UR-ENERGY INC"
    },
    "BRW": {
        "cik": 826020,
        "title": "Saba Capital Income & Opportunities Fund"
    },
    "DOYU": {
        "cik": 1762417,
        "title": "DouYu International Holdings Ltd"
    },
    "JGGC": {
        "cik": 1857518,
        "title": "Jaguar Global Growth Corp I"
    },
    "HPF": {
        "cik": 1189740,
        "title": "JOHN HANCOCK PREFERRED INCOME FUND II"
    },
    "SVII": {
        "cik": 1843477,
        "title": "Spring Valley Acquisition Corp. II"
    },
    "RLGT": {
        "cik": 1171155,
        "title": "RADIANT LOGISTICS, INC"
    },
    "LPSN": {
        "cik": 1102993,
        "title": "LIVEPERSON INC"
    },
    "SLVR": {
        "cik": 1842644,
        "title": "SILVERspac Inc."
    },
    "PFIS": {
        "cik": 1056943,
        "title": "PEOPLES FINANCIAL SERVICES CORP."
    },
    "EPM": {
        "cik": 1006655,
        "title": "EVOLUTION PETROLEUM CORP"
    },
    "GBIO": {
        "cik": 1733294,
        "title": "Generation Bio Co."
    },
    "CIX": {
        "cik": 1049606,
        "title": "COMPX INTERNATIONAL INC"
    },
    "NWPX": {
        "cik": 1001385,
        "title": "NORTHWEST PIPE CO"
    },
    "HWEL": {
        "cik": 1845013,
        "title": "Healthwell Acquisition Corp. I"
    },
    "KIO": {
        "cik": 1515940,
        "title": "KKR Income Opportunities Fund"
    },
    "SOR": {
        "cik": 91847,
        "title": "SOURCE CAPITAL INC /DE/"
    },
    "MVBF": {
        "cik": 1277902,
        "title": "MVB FINANCIAL CORP"
    },
    "EVI": {
        "cik": 65312,
        "title": "EVI INDUSTRIES, INC."
    },
    "FF": {
        "cik": 1337298,
        "title": "FutureFuel Corp."
    },
    "GRPN": {
        "cik": 1490281,
        "title": "Groupon, Inc."
    },
    "MIESY": {
        "cik": 1567924,
        "title": "Mitsui E&S Holdings Co., Ltd./ADR"
    },
    "AVNW": {
        "cik": 1377789,
        "title": "AVIAT NETWORKS, INC."
    },
    "FHTX": {
        "cik": 1822462,
        "title": "Foghorn Therapeutics Inc."
    },
    "NBTX": {
        "cik": 1760854,
        "title": "Nanobiotix S.A."
    },
    "JRI": {
        "cik": 1539337,
        "title": "Nuveen Real Asset Income & Growth Fund"
    },
    "HIX": {
        "cik": 1058239,
        "title": "WESTERN ASSET HIGH INCOME FUND II INC."
    },
    "NAN": {
        "cik": 1074769,
        "title": "NUVEEN NEW YORK QUALITY MUNICIPAL INCOME FUND"
    },
    "REAX": {
        "cik": 1862461,
        "title": "Real Brokerage Inc"
    },
    "OSG": {
        "cik": 75208,
        "title": "OVERSEAS SHIPHOLDING GROUP INC"
    },
    "CRNCY": {
        "cik": 909531,
        "title": "CAIRN ENERGY PLC"
    },
    "FWAC": {
        "cik": 1847874,
        "title": "Fifth Wall Acquisition Corp. III"
    },
    "OZ": {
        "cik": 1807046,
        "title": "Belpointe PREP, LLC"
    },
    "IPXX": {
        "cik": 1970622,
        "title": "Inflection Point Acquisition Corp. II"
    },
    "MGNX": {
        "cik": 1125345,
        "title": "MACROGENICS INC"
    },
    "JMIA": {
        "cik": 1756708,
        "title": "Jumia Technologies AG"
    },
    "SAR": {
        "cik": 1377936,
        "title": "SARATOGA INVESTMENT CORP."
    },
    "BITF": {
        "cik": 1812477,
        "title": "Bitfarms Ltd"
    },
    "MIY": {
        "cik": 890393,
        "title": "BLACKROCK MUNIYIELD MICHIGAN QUALITY FUND, INC."
    },
    "TERN": {
        "cik": 1831363,
        "title": "Terns Pharmaceuticals, Inc."
    },
    "FNKO": {
        "cik": 1704711,
        "title": "Funko, Inc."
    },
    "PLAO": {
        "cik": 1849737,
        "title": "Patria Latin American Opportunity Acquisition Corp."
    },
    "PRTH": {
        "cik": 1653558,
        "title": "Priority Technology Holdings, Inc."
    },
    "BMRC": {
        "cik": 1403475,
        "title": "Bank of Marin Bancorp"
    },
    "GAQ": {
        "cik": 1852061,
        "title": "Generation Asia I Acquisition Ltd"
    },
    "WTBA": {
        "cik": 1166928,
        "title": "WEST BANCORPORATION INC"
    },
    "FARO": {
        "cik": 917491,
        "title": "FARO TECHNOLOGIES INC"
    },
    "ONTF": {
        "cik": 1110611,
        "title": "ON24 INC."
    },
    "VMD": {
        "cik": 1729149,
        "title": "VIEMED HEALTHCARE, INC."
    },
    "MIN": {
        "cik": 826735,
        "title": "MFS INTERMEDIATE INCOME TRUST"
    },
    "FFIE": {
        "cik": 1805521,
        "title": "FARADAY FUTURE INTELLIGENT ELECTRIC INC."
    },
    "GLUE": {
        "cik": 1826457,
        "title": "Monte Rosa Therapeutics, Inc."
    },
    "MCBC": {
        "cik": 1053584,
        "title": "MACATAWA BANK CORP"
    },
    "SBT": {
        "cik": 1680379,
        "title": "Sterling Bancorp, Inc."
    },
    "RNGR": {
        "cik": 1699039,
        "title": "Ranger Energy Services, Inc."
    },
    "CERS": {
        "cik": 1020214,
        "title": "CERUS CORP"
    },
    "ZIMV": {
        "cik": 1876588,
        "title": "ZimVie Inc."
    },
    "HKIT": {
        "cik": 1742341,
        "title": "HiTek Global Inc."
    },
    "LXFR": {
        "cik": 1096056,
        "title": "LUXFER HOLDINGS PLC"
    },
    "GPP": {
        "cik": 1635650,
        "title": "Green Plains Partners LP"
    },
    "CLAR": {
        "cik": 913277,
        "title": "Clarus Corp"
    },
    "BTWN": {
        "cik": 1815086,
        "title": "Bridgetown Holdings Ltd"
    },
    "SLND": {
        "cik": 1883814,
        "title": "Southland Holdings, Inc."
    },
    "RENE": {
        "cik": 1889112,
        "title": "Cartesian Growth Corp II"
    },
    "OCUL": {
        "cik": 1393434,
        "title": "OCULAR THERAPEUTIX, INC"
    },
    "LE": {
        "cik": 799288,
        "title": "LANDS' END, INC."
    },
    "TRMR": {
        "cik": 1849396,
        "title": "Tremor International Ltd."
    },
    "AROW": {
        "cik": 717538,
        "title": "ARROW FINANCIAL CORP"
    },
    "WNNR": {
        "cik": 1843714,
        "title": "Andretti Acquisition Corp."
    },
    "CITE": {
        "cik": 1848437,
        "title": "Cartica Acquisition Corp"
    },
    "LCAA": {
        "cik": 1841024,
        "title": "L Catterton Asia Acquisition Corp"
    },
    "NGVC": {
        "cik": 1547459,
        "title": "Natural Grocers by Vitamin Cottage, Inc."
    },
    "GDRZF": {
        "cik": 1072725,
        "title": "GOLD RESERVE INC"
    },
    "UTAA": {
        "cik": 1879221,
        "title": "UTA Acquisition Corp"
    },
    "MHN": {
        "cik": 1038186,
        "title": "BLACKROCK MUNIHOLDINGS NEW YORK QUALITY FUND, INC."
    },
    "CMPX": {
        "cik": 1738021,
        "title": "Compass Therapeutics, Inc."
    },
    "BRD": {
        "cik": 1847351,
        "title": "Beard Energy Transition Acquisition Corp."
    },
    "TRIS": {
        "cik": 1852736,
        "title": "Tristar Acquisition I Corp."
    },
    "NATR": {
        "cik": 275053,
        "title": "NATURES SUNSHINE PRODUCTS INC"
    },
    "BSRR": {
        "cik": 1130144,
        "title": "SIERRA BANCORP"
    },
    "WLDN": {
        "cik": 1370450,
        "title": "Willdan Group, Inc."
    },
    "DPCS": {
        "cik": 1857803,
        "title": "DP Cap Acquisition Corp I"
    },
    "PGSS": {
        "cik": 1861541,
        "title": "Pegasus Digital Mobility Acquisition Corp."
    },
    "EDD": {
        "cik": 1388141,
        "title": "Morgan Stanley Emerging Markets Domestic Debt Fund, Inc."
    },
    "AIXI": {
        "cik": 1935172,
        "title": "Xiao-I Corp"
    },
    "CVGI": {
        "cik": 1290900,
        "title": "Commercial Vehicle Group, Inc."
    },
    "LCW": {
        "cik": 1847577,
        "title": "Learn CW Investment Corp"
    },
    "AFRI": {
        "cik": 1903870,
        "title": "Forafric Global PLC"
    },
    "SMHI": {
        "cik": 1690334,
        "title": "SEACOR Marine Holdings Inc."
    },
    "PORT": {
        "cik": 1865200,
        "title": "Southport Acquisition Corp"
    },
    "DBVT": {
        "cik": 1613780,
        "title": "DBV Technologies S.A."
    },
    "CGC": {
        "cik": 1737927,
        "title": "Canopy Growth Corp"
    },
    "HIVE": {
        "cik": 1720424,
        "title": "HIVE Digital Technologies Ltd."
    },
    "LVOX": {
        "cik": 1723648,
        "title": "LiveVox Holdings, Inc."
    },
    "AEAE": {
        "cik": 1852016,
        "title": "AltEnergy Acquisition Corp"
    },
    "VMCA": {
        "cik": 1892747,
        "title": "Valuence Merger Corp. I"
    },
    "CBRG": {
        "cik": 1845149,
        "title": "Chain Bridge I"
    },
    "WLFC": {
        "cik": 1018164,
        "title": "WILLIS LEASE FINANCE CORP"
    },
    "ZURA": {
        "cik": 1855644,
        "title": "Zura Bio Ltd"
    },
    "MLP": {
        "cik": 63330,
        "title": "MAUI LAND & PINEAPPLE CO INC"
    },
    "FLIC": {
        "cik": 740663,
        "title": "FIRST OF LONG ISLAND CORP"
    },
    "CPZ": {
        "cik": 1717457,
        "title": "Calamos Long/Short Equity & Dynamic Income Trust"
    },
    "AVAH": {
        "cik": 1832332,
        "title": "Aveanna Healthcare Holdings, Inc."
    },
    "JWSM": {
        "cik": 1831359,
        "title": "Jaws Mustang Acquisition Corp"
    },
    "WHF": {
        "cik": 1552198,
        "title": "WhiteHorse Finance, Inc."
    },
    "KNSW": {
        "cik": 1885444,
        "title": "KnightSwan Acquisition Corp"
    },
    "IVCB": {
        "cik": 1857410,
        "title": "Investcorp Europe Acquisition Corp I"
    },
    "RMM": {
        "cik": 1771226,
        "title": "RiverNorth Managed Duration Municipal Income Fund, Inc."
    },
    "SKYT": {
        "cik": 1819974,
        "title": "SkyWater Technology, Inc"
    },
    "CPLP": {
        "cik": 1392326,
        "title": "Capital Product Partners L.P."
    },
    "ASG": {
        "cik": 786035,
        "title": "LIBERTY ALL STAR GROWTH FUND INC."
    },
    "MCI": {
        "cik": 275694,
        "title": "BARINGS CORPORATE INVESTORS"
    },
    "BKUH": {
        "cik": 1440153,
        "title": "Bakhu Holdings, Corp."
    },
    "CZNC": {
        "cik": 810958,
        "title": "CITIZENS & NORTHERN CORP"
    },
    "VTDRF": {
        "cik": 1465872,
        "title": "VANTAGE DRILLING INTERNATIONAL"
    },
    "NCV": {
        "cik": 1214935,
        "title": "Virtus Convertible & Income Fund"
    },
    "TCI": {
        "cik": 733590,
        "title": "TRANSCONTINENTAL REALTY INVESTORS INC"
    },
    "TSVT": {
        "cik": 1860782,
        "title": "2seventy bio, Inc."
    },
    "NATH": {
        "cik": 69733,
        "title": "NATHANS FAMOUS, INC."
    },
    "TDF": {
        "cik": 919893,
        "title": "TEMPLETON DRAGON FUND INC"
    },
    "VAXX": {
        "cik": 1851657,
        "title": "Vaxxinity, Inc."
    },
    "QUAD": {
        "cik": 1481792,
        "title": "Quad/Graphics, Inc."
    },
    "CREEF": {
        "cik": 1851230,
        "title": "Crescera Capital Acquisition Corp."
    },
    "INVZ": {
        "cik": 1835654,
        "title": "Innoviz Technologies Ltd."
    },
    "FOF": {
        "cik": 1375340,
        "title": "Cohen & Steers Closed-End Opportunity Fund, Inc."
    },
    "SCM": {
        "cik": 1551901,
        "title": "Stellus Capital Investment Corp"
    },
    "BLND": {
        "cik": 1855747,
        "title": "Blend Labs, Inc."
    },
    "RDVT": {
        "cik": 1720116,
        "title": "Red Violet, Inc."
    },
    "AFB": {
        "cik": 1162027,
        "title": "ALLIANCEBERNSTEIN NATIONAL MUNICIPAL INCOME FUND"
    },
    "API": {
        "cik": 1802883,
        "title": "Agora, Inc."
    },
    "BAER": {
        "cik": 1941536,
        "title": "Bridger Aerospace Group Holdings, Inc."
    },
    "RFI": {
        "cik": 891290,
        "title": "COHEN & STEERS TOTAL RETURN REALTY FUND INC"
    },
    "NTPIF": {
        "cik": 829365,
        "title": "NAM TAI PROPERTY INC."
    },
    "FINS": {
        "cik": 1745059,
        "title": "Angel Oak Financial Strategies Income Term Trust"
    },
    "SDSYA": {
        "cik": 1163609,
        "title": "SOUTH DAKOTA SOYBEAN PROCESSORS LLC"
    },
    "JFIN": {
        "cik": 1743102,
        "title": "Jiayin Group Inc."
    },
    "PFL": {
        "cik": 1244183,
        "title": "PIMCO INCOME STRATEGY FUND"
    },
    "BLNK": {
        "cik": 1429764,
        "title": "Blink Charging Co."
    },
    "TGAA": {
        "cik": 1847355,
        "title": "Target Global Acquisition I Corp."
    },
    "ARDC": {
        "cik": 1515324,
        "title": "Ares Dynamic Credit Allocation Fund, Inc."
    },
    "CVEO": {
        "cik": 1590584,
        "title": "Civeo Corp"
    },
    "VSTA": {
        "cik": 1792829,
        "title": "Vasta Platform Ltd"
    },
    "ZYXI": {
        "cik": 846475,
        "title": "ZYNEX INC"
    },
    "IMRX": {
        "cik": 1790340,
        "title": "Immuneering Corp"
    },
    "ODV": {
        "cik": 1431852,
        "title": "Osisko Development Corp."
    },
    "QSI": {
        "cik": 1816431,
        "title": "Quantum-Si Inc"
    },
    "OIA": {
        "cik": 835333,
        "title": "Invesco Municipal Income Opportunities Trust"
    },
    "AVIR": {
        "cik": 1593899,
        "title": "Atea Pharmaceuticals, Inc."
    },
    "ITIC": {
        "cik": 720858,
        "title": "INVESTORS TITLE CO"
    },
    "BWB": {
        "cik": 1341317,
        "title": "Bridgewater Bancshares Inc"
    },
    "GATO": {
        "cik": 1517006,
        "title": "Gatos Silver, Inc."
    },
    "SCPH": {
        "cik": 1604950,
        "title": "scPharmaceuticals Inc."
    },
    "NVTA": {
        "cik": 1501134,
        "title": "Invitae Corp"
    },
    "CCV": {
        "cik": 1812234,
        "title": "Churchill Capital Corp V"
    },
    "OVID": {
        "cik": 1636651,
        "title": "Ovid Therapeutics Inc."
    },
    "ASA": {
        "cik": 1230869,
        "title": "ASA Gold & Precious Metals Ltd"
    },
    "ALTO": {
        "cik": 778164,
        "title": "Alto Ingredients, Inc."
    },
    "CSTR": {
        "cik": 1676479,
        "title": "CapStar Financial Holdings, Inc."
    },
    "SKGR": {
        "cik": 1912461,
        "title": "SK Growth Opportunities Corp"
    },
    "NCA": {
        "cik": 818851,
        "title": "NUVEEN CALIFORNIA MUNICIPAL VALUE FUND"
    },
    "CURV": {
        "cik": 1792781,
        "title": "Torrid Holdings Inc."
    },
    "STRO": {
        "cik": 1382101,
        "title": "SUTRO BIOPHARMA, INC."
    },
    "PKE": {
        "cik": 76267,
        "title": "PARK AEROSPACE CORP"
    },
    "BYM": {
        "cik": 1181187,
        "title": "BLACKROCK MUNICIPAL INCOME QUALITY TRUST"
    },
    "EDAP": {
        "cik": 1041934,
        "title": "EDAP TMS SA"
    },
    "CONX": {
        "cik": 1823000,
        "title": "CONX Corp."
    },
    "WAVC": {
        "cik": 1849580,
        "title": "Waverley Capital Acquisition Corp. 1"
    },
    "BANT": {
        "cik": 1704795,
        "title": "Bantec, Inc."
    },
    "FNLC": {
        "cik": 765207,
        "title": "First Bancorp, Inc /ME/"
    },
    "NLCP": {
        "cik": 1854964,
        "title": "NewLake Capital Partners, Inc."
    },
    "PMM": {
        "cik": 844790,
        "title": "PUTNAM MANAGED MUNICIPAL INCOME TRUST"
    },
    "PCYO": {
        "cik": 276720,
        "title": "PURE CYCLE CORP"
    },
    "ARAY": {
        "cik": 1138723,
        "title": "ACCURAY INC"
    },
    "VCSA": {
        "cik": 1874944,
        "title": "Vacasa, Inc."
    },
    "GHL": {
        "cik": 1282977,
        "title": "GREENHILL & CO INC"
    },
    "ACNB": {
        "cik": 715579,
        "title": "ACNB CORP"
    },
    "LFCR": {
        "cik": 1005286,
        "title": "LIFECORE BIOMEDICAL, INC. \\DE\\"
    },
    "CDAQ": {
        "cik": 1851909,
        "title": "Compass Digital Acquisition Corp."
    },
    "TNYA": {
        "cik": 1858848,
        "title": "Tenaya Therapeutics, Inc."
    },
    "FISI": {
        "cik": 862831,
        "title": "FINANCIAL INSTITUTIONS INC"
    },
    "ANIK": {
        "cik": 898437,
        "title": "Anika Therapeutics, Inc."
    },
    "CIVB": {
        "cik": 944745,
        "title": "CIVISTA BANCSHARES, INC."
    },
    "TRHC": {
        "cik": 1651561,
        "title": "Tabula Rasa HealthCare, Inc."
    },
    "CBNK": {
        "cik": 1419536,
        "title": "Capital Bancorp Inc"
    },
    "SGMT": {
        "cik": 1400118,
        "title": "Sagimet Biosciences Inc."
    },
    "SPXX": {
        "cik": 1338561,
        "title": "Nuveen S&P 500 Dynamic Overwrite Fund"
    },
    "CPS": {
        "cik": 1320461,
        "title": "Cooper-Standard Holdings Inc."
    },
    "DXLG": {
        "cik": 813298,
        "title": "DESTINATION XL GROUP, INC."
    },
    "CAF": {
        "cik": 1368493,
        "title": "Morgan Stanley China A Share Fund, Inc."
    },
    "OB": {
        "cik": 1454938,
        "title": "Outbrain Inc."
    },
    "LINC": {
        "cik": 1286613,
        "title": "LINCOLN EDUCATIONAL SERVICES CORP"
    },
    "OPAD": {
        "cik": 1825024,
        "title": "Offerpad Solutions Inc."
    },
    "MYTE": {
        "cik": 1831907,
        "title": "MYT Netherlands Parent B.V."
    },
    "PANL": {
        "cik": 1606909,
        "title": "Pangaea Logistics Solutions Ltd."
    },
    "NODK": {
        "cik": 1681206,
        "title": "NI Holdings, Inc."
    },
    "GWRS": {
        "cik": 1434728,
        "title": "Global Water Resources, Inc."
    },
    "AMLI": {
        "cik": 1699880,
        "title": "American Lithium Corp."
    },
    "AMSC": {
        "cik": 880807,
        "title": "AMERICAN SUPERCONDUCTOR CORP /DE/"
    },
    "ASCB": {
        "cik": 1876716,
        "title": "ASPAC II Acquisition Corp."
    },
    "FATE": {
        "cik": 1434316,
        "title": "FATE THERAPEUTICS INC"
    },
    "ANTX": {
        "cik": 1880438,
        "title": "AN2 Therapeutics, Inc."
    },
    "LMNR": {
        "cik": 1342423,
        "title": "Limoneira CO"
    },
    "ATAI": {
        "cik": 1840904,
        "title": "ATAI Life Sciences N.V."
    },
    "FEN": {
        "cik": 1284940,
        "title": "FIRST TRUST ENERGY INCOME & GROWTH FUND"
    },
    "MULG": {
        "cik": 1629665,
        "title": "MULIANG VIAGOO TECHNOLOGY, INC."
    },
    "HT": {
        "cik": 1063344,
        "title": "HERSHA HOSPITALITY TRUST"
    },
    "VHNA": {
        "cik": 1868640,
        "title": "Vahanna Tech Edge Acquisition I Corp."
    },
    "GOEV": {
        "cik": 1750153,
        "title": "Canoo Inc."
    },
    "BCAL": {
        "cik": 1795815,
        "title": "Southern California Bancorp CA"
    },
    "OPFI": {
        "cik": 1818502,
        "title": "OppFi Inc."
    },
    "BGH": {
        "cik": 1521404,
        "title": "BARINGS GLOBAL SHORT DURATION HIGH YIELD FUND"
    },
    "RM": {
        "cik": 1519401,
        "title": "Regional Management Corp."
    },
    "VLD": {
        "cik": 1825079,
        "title": "Velo3D, Inc."
    },
    "GLASF": {
        "cik": 1848731,
        "title": "Glass House Brands Inc."
    },
    "VSTM": {
        "cik": 1526119,
        "title": "Verastem, Inc."
    },
    "OBT": {
        "cik": 1754226,
        "title": "Orange County Bancorp, Inc. /DE/"
    },
    "ZTR": {
        "cik": 836412,
        "title": "Virtus Total Return Fund Inc."
    },
    "DSM": {
        "cik": 855887,
        "title": "BNY MELLON STRATEGIC MUNICIPAL BOND FUND, INC."
    },
    "THRD": {
        "cik": 1923840,
        "title": "Third Harmonic Bio, Inc."
    },
    "WSBF": {
        "cik": 1569994,
        "title": "Waterstone Financial, Inc."
    },
    "ABIT": {
        "cik": 1095146,
        "title": "Athena Bitcoin Global"
    },
    "UTI": {
        "cik": 1261654,
        "title": "UNIVERSAL TECHNICAL INSTITUTE INC"
    },
    "PRLH": {
        "cik": 1856161,
        "title": "Pearl Holdings Acquisition Corp"
    },
    "YMAB": {
        "cik": 1722964,
        "title": "Y-mAbs Therapeutics, Inc."
    },
    "VUZI": {
        "cik": 1463972,
        "title": "Vuzix Corp"
    },
    "HBCP": {
        "cik": 1436425,
        "title": "HOME BANCORP, INC."
    },
    "KLTR": {
        "cik": 1432133,
        "title": "KALTURA INC"
    },
    "FDBC": {
        "cik": 1098151,
        "title": "FIDELITY D & D BANCORP INC"
    },
    "PSQH": {
        "cik": 1847064,
        "title": "PSQ Holdings, Inc."
    },
    "TLYS": {
        "cik": 1524025,
        "title": "TILLY'S, INC."
    },
    "EEX": {
        "cik": 1579214,
        "title": "Emerald Holding, Inc."
    },
    "ERC": {
        "cik": 1227073,
        "title": "ALLSPRING MULTI-SECTOR INCOME FUND"
    },
    "SEDA": {
        "cik": 1846975,
        "title": "SDCL EDGE Acquisition Corp"
    },
    "ALLK": {
        "cik": 1564824,
        "title": "Allakos Inc."
    },
    "ILPT": {
        "cik": 1717307,
        "title": "Industrial Logistics Properties Trust"
    },
    "HYI": {
        "cik": 1497186,
        "title": "Western Asset High Yield Defined Opportunity Fund Inc."
    },
    "HQI": {
        "cik": 1140102,
        "title": "HireQuest, Inc."
    },
    "RAASY": {
        "cik": 1804583,
        "title": "Cloopen Group Holding Ltd"
    },
    "JGH": {
        "cik": 1615905,
        "title": "Nuveen Global High Income Fund"
    },
    "FMAO": {
        "cik": 792966,
        "title": "FARMERS & MERCHANTS BANCORP INC"
    },
    "TCBX": {
        "cik": 1781730,
        "title": "Third Coast Bancshares, Inc."
    },
    "BGT": {
        "cik": 1287480,
        "title": "BLACKROCK FLOATING RATE INCOME TRUST"
    },
    "UCAR": {
        "cik": 1939780,
        "title": "U Power Ltd"
    },
    "FCT": {
        "cik": 1282850,
        "title": "FIRST TRUST SENIOR FLOATING RATE INCOME FUND II"
    },
    "MCR": {
        "cik": 851170,
        "title": "MFS CHARTER INCOME TRUST"
    },
    "DLTH": {
        "cik": 1649744,
        "title": "DULUTH HOLDINGS INC."
    },
    "RBB": {
        "cik": 1499422,
        "title": "RBB Bancorp"
    },
    "NL": {
        "cik": 72162,
        "title": "NL INDUSTRIES INC"
    },
    "TTSH": {
        "cik": 1552800,
        "title": "TILE SHOP HOLDINGS, INC."
    },
    "CORZQ": {
        "cik": 1839341,
        "title": "Core Scientific, Inc./tx"
    },
    "ACIU": {
        "cik": 1651625,
        "title": "AC Immune SA"
    },
    "CMTL": {
        "cik": 23197,
        "title": "COMTECH TELECOMMUNICATIONS CORP /DE/"
    },
    "EOT": {
        "cik": 1454741,
        "title": "Eaton Vance National Municipal Opportunities Trust"
    },
    "GPMT": {
        "cik": 1703644,
        "title": "Granite Point Mortgage Trust Inc."
    },
    "XFLT": {
        "cik": 1703079,
        "title": "XAI Octagon Floating Rate & Alternative Income Term Trust"
    },
    "SPOK": {
        "cik": 1289945,
        "title": "Spok Holdings, Inc"
    },
    "MMT": {
        "cik": 809173,
        "title": "MFS MULTIMARKET INCOME TRUST"
    },
    "LOCC": {
        "cik": 1848323,
        "title": "Live Oak Crestview Climate Acquisition Corp."
    },
    "HYZN": {
        "cik": 1716583,
        "title": "Hyzon Motors Inc."
    },
    "REFI": {
        "cik": 1867949,
        "title": "Chicago Atlantic Real Estate Finance, Inc."
    },
    "TALK": {
        "cik": 1803901,
        "title": "Talkspace, Inc."
    },
    "FBIZ": {
        "cik": 1521951,
        "title": "FIRST BUSINESS FINANCIAL SERVICES, INC."
    },
    "HFFG": {
        "cik": 1680873,
        "title": "HF Foods Group Inc."
    },
    "SKYH": {
        "cik": 1823587,
        "title": "Sky Harbour Group Corp"
    },
    "PINE": {
        "cik": 1786117,
        "title": "Alpine Income Property Trust, Inc."
    },
    "BLDE": {
        "cik": 1779128,
        "title": "Blade Air Mobility, Inc."
    },
    "MXF": {
        "cik": 65433,
        "title": "MEXICO FUND INC"
    },
    "AGS": {
        "cik": 1593548,
        "title": "PlayAGS, Inc."
    },
    "AMPY": {
        "cik": 1533924,
        "title": "Amplify Energy Corp."
    },
    "CHMX": {
        "cik": 1657045,
        "title": "NEXT-ChemX Corporation."
    },
    "CPSI": {
        "cik": 1169445,
        "title": "COMPUTER PROGRAMS & SYSTEMS INC"
    },
    "AKYA": {
        "cik": 1711933,
        "title": "Akoya Biosciences, Inc."
    },
    "BYNO": {
        "cik": 1801417,
        "title": "byNordic Acquisition Corp"
    },
    "MSB": {
        "cik": 65172,
        "title": "MESABI TRUST"
    },
    "BOCN": {
        "cik": 1856961,
        "title": "Blue Ocean Acquisition Corp"
    },
    "AEF": {
        "cik": 846676,
        "title": "ABRDN EMERGING MARKETS EQUITY INCOME FUND, INC."
    },
    "CFIV": {
        "cik": 1825249,
        "title": "CF ACQUISITION CORP. IV"
    },
    "NEN": {
        "cik": 746514,
        "title": "NEW ENGLAND REALTY ASSOCIATES LIMITED PARTNERSHIP"
    },
    "CARM": {
        "cik": 1485003,
        "title": "Carisma Therapeutics Inc."
    },
    "RGTI": {
        "cik": 1838359,
        "title": "Rigetti Computing, Inc."
    },
    "UIS": {
        "cik": 746838,
        "title": "UNISYS CORP"
    },
    "BLFY": {
        "cik": 1846017,
        "title": "Blue Foundry Bancorp"
    },
    "AXGN": {
        "cik": 805928,
        "title": "Axogen, Inc."
    },
    "UONE": {
        "cik": 1041657,
        "title": "URBAN ONE, INC."
    },
    "EM": {
        "cik": 1834253,
        "title": "Smart Share Global Ltd"
    },
    "VLN": {
        "cik": 1863006,
        "title": "Valens Semiconductor Ltd."
    },
    "BVS": {
        "cik": 1665988,
        "title": "Bioventus Inc."
    },
    "BKCC": {
        "cik": 1326003,
        "title": "BlackRock Capital Investment Corp"
    },
    "SLN": {
        "cik": 1479615,
        "title": "Silence Therapeutics plc"
    },
    "SSTI": {
        "cik": 1351636,
        "title": "SOUNDTHINKING, INC."
    },
    "STOK": {
        "cik": 1623526,
        "title": "Stoke Therapeutics, Inc."
    },
    "CORBF": {
        "cik": 1467808,
        "title": "Global Cord Blood Corp"
    },
    "JMSB": {
        "cik": 1710482,
        "title": "John Marshall Bancorp, Inc."
    },
    "AFCG": {
        "cik": 1822523,
        "title": "AFC Gamma, Inc."
    },
    "FTF": {
        "cik": 1233087,
        "title": "FRANKLIN LTD DURATION INCOME TRUST"
    },
    "JILL": {
        "cik": 1687932,
        "title": "J.Jill, Inc."
    },
    "SENS": {
        "cik": 1616543,
        "title": "Senseonics Holdings, Inc."
    },
    "YI": {
        "cik": 1738906,
        "title": "111, Inc."
    },
    "NRIM": {
        "cik": 1163370,
        "title": "NORTHRIM BANCORP INC"
    },
    "CLPR": {
        "cik": 1649096,
        "title": "Clipper Realty Inc."
    },
    "OBIO": {
        "cik": 1814114,
        "title": "Orchestra BioMed Holdings, Inc."
    },
    "BARK": {
        "cik": 1819574,
        "title": "Bark, Inc."
    },
    "BKT": {
        "cik": 832327,
        "title": "BLACKROCK INCOME TRUST, INC."
    },
    "CFFS": {
        "cik": 1839519,
        "title": "CF Acquisition Corp. VII"
    },
    "CZFS": {
        "cik": 739421,
        "title": "CITIZENS FINANCIAL SERVICES INC"
    },
    "KMDA": {
        "cik": 1567529,
        "title": "KAMADA LTD"
    },
    "ATLX": {
        "cik": 1540684,
        "title": "Atlas Lithium Corp"
    },
    "THCP": {
        "cik": 1843993,
        "title": "Thunder Bridge Capital Partners IV, Inc."
    },
    "PMF": {
        "cik": 1140392,
        "title": "PIMCO MUNICIPAL INCOME FUND"
    },
    "NECB": {
        "cik": 1847398,
        "title": "NorthEast Community Bancorp, Inc./MD/"
    },
    "PMX": {
        "cik": 1181506,
        "title": "PIMCO MUNICIPAL INCOME FUND III"
    },
    "WEYS": {
        "cik": 106532,
        "title": "WEYCO GROUP INC"
    },
    "MKFG": {
        "cik": 1816613,
        "title": "Markforged Holding Corp"
    },
    "UNTY": {
        "cik": 920427,
        "title": "UNITY BANCORP INC /NJ/"
    },
    "PMTS": {
        "cik": 1641614,
        "title": "CPI Card Group Inc."
    },
    "CMBM": {
        "cik": 1738177,
        "title": "Cambium Networks Corp"
    },
    "TREE": {
        "cik": 1434621,
        "title": "LendingTree, Inc."
    },
    "HIPO": {
        "cik": 1828105,
        "title": "Hippo Holdings Inc."
    },
    "PETS": {
        "cik": 1040130,
        "title": "PETMED EXPRESS INC"
    },
    "NUW": {
        "cik": 1450445,
        "title": "Nuveen AMT-Free Municipal Value Fund"
    },
    "HAWEL": {
        "cik": 46207,
        "title": "HAWAIIAN ELECTRIC CO INC"
    },
    "NHHS": {
        "cik": 1503707,
        "title": "NorthStar Healthcare Income, Inc."
    },
    "KNDI": {
        "cik": 1316517,
        "title": "Kandi Technologies Group, Inc."
    },
    "FET": {
        "cik": 1401257,
        "title": "FORUM ENERGY TECHNOLOGIES, INC."
    },
    "EBS": {
        "cik": 1367644,
        "title": "Emergent BioSolutions Inc."
    },
    "BNY": {
        "cik": 1137390,
        "title": "BLACKROCK NEW YORK MUNICIPAL INCOME TRUST"
    },
    "FULC": {
        "cik": 1680581,
        "title": "Fulcrum Therapeutics, Inc."
    },
    "RCS": {
        "cik": 916183,
        "title": "PIMCO STRATEGIC INCOME FUND, INC"
    },
    "ASUR": {
        "cik": 884144,
        "title": "ASURE SOFTWARE INC"
    },
    "IPHA": {
        "cik": 1598599,
        "title": "Innate Pharma SA"
    },
    "POWW": {
        "cik": 1015383,
        "title": "AMMO, INC."
    },
    "NIU": {
        "cik": 1744781,
        "title": "Niu Technologies"
    },
    "CDZI": {
        "cik": 727273,
        "title": "CADIZ INC"
    },
    "NVCT": {
        "cik": 1875558,
        "title": "Nuvectis Pharma, Inc."
    },
    "UROY": {
        "cik": 1711570,
        "title": "Uranium Royalty Corp."
    },
    "FIF": {
        "cik": 1513789,
        "title": "FIRST TRUST ENERGY INFRASTRUCTURE FUND"
    },
    "TSBK": {
        "cik": 1046050,
        "title": "TIMBERLAND BANCORP INC"
    },
    "RIV": {
        "cik": 1501072,
        "title": "RIVERNORTH OPPORTUNITIES FUND, INC."
    },
    "PKOH": {
        "cik": 76282,
        "title": "PARK OHIO HOLDINGS CORP"
    },
    "LCTX": {
        "cik": 876343,
        "title": "Lineage Cell Therapeutics, Inc."
    },
    "HOFT": {
        "cik": 1077688,
        "title": "HOOKER FURNISHINGS Corp"
    },
    "BCML": {
        "cik": 1730984,
        "title": "BayCom Corp"
    },
    "EGRX": {
        "cik": 827871,
        "title": "EAGLE PHARMACEUTICALS, INC."
    },
    "FSBW": {
        "cik": 1530249,
        "title": "FS Bancorp, Inc."
    },
    "FUND": {
        "cik": 825202,
        "title": "SPROTT FOCUS TRUST INC."
    },
    "PRTS": {
        "cik": 1378950,
        "title": "CarParts.com, Inc."
    },
    "LSAK": {
        "cik": 1041514,
        "title": "LESAKA TECHNOLOGIES INC"
    },
    "DRTS": {
        "cik": 1871321,
        "title": "Alpha Tau Medical Ltd."
    },
    "TIHE": {
        "cik": 1066719,
        "title": "Taihe Group, Inc."
    },
    "PRPL": {
        "cik": 1643953,
        "title": "Purple Innovation, Inc."
    },
    "ICNC": {
        "cik": 1858351,
        "title": "Iconic Sports Acquisition Corp."
    },
    "NC": {
        "cik": 789933,
        "title": "NACCO INDUSTRIES INC"
    },
    "ACRV": {
        "cik": 1781174,
        "title": "Acrivon Therapeutics, Inc."
    },
    "TWOU": {
        "cik": 1459417,
        "title": "2U, Inc."
    },
    "LMDX": {
        "cik": 1685428,
        "title": "LumiraDx Ltd"
    },
    "GTE": {
        "cik": 1273441,
        "title": "GRAN TIERRA ENERGY INC."
    },
    "IREN": {
        "cik": 1878848,
        "title": "Iris Energy Ltd"
    },
    "OMER": {
        "cik": 1285819,
        "title": "OMEROS CORP"
    },
    "ORRF": {
        "cik": 826154,
        "title": "ORRSTOWN FINANCIAL SERVICES INC"
    },
    "APCA": {
        "cik": 1862993,
        "title": "AP Acquisition Corp"
    },
    "PBFS": {
        "cik": 1769663,
        "title": "Pioneer Bancorp, Inc./MD"
    },
    "MEC": {
        "cik": 1766368,
        "title": "Mayville Engineering Company, Inc."
    },
    "MBCN": {
        "cik": 836147,
        "title": "MIDDLEFIELD BANC CORP"
    },
    "LGO": {
        "cik": 1400438,
        "title": "Largo Inc."
    },
    "WRN": {
        "cik": 1364125,
        "title": "Western Copper & Gold Corp"
    },
    "GTII": {
        "cik": 356590,
        "title": "GLOBAL TECH INDUSTRIES GROUP, INC."
    },
    "DBL": {
        "cik": 1525201,
        "title": "DoubleLine Opportunistic Credit Fund"
    },
    "FRBN": {
        "cik": 1874495,
        "title": "Forbion European Acquisition Corp."
    },
    "TEI": {
        "cik": 909112,
        "title": "TEMPLETON EMERGING MARKETS INCOME FUND"
    },
    "SST": {
        "cik": 1805833,
        "title": "System1, Inc."
    },
    "PBPB": {
        "cik": 1195734,
        "title": "POTBELLY CORP"
    },
    "MNTN": {
        "cik": 1863719,
        "title": "Everest Consolidator Acquisition Corp"
    },
    "AKBA": {
        "cik": 1517022,
        "title": "Akebia Therapeutics, Inc."
    },
    "YRD": {
        "cik": 1631761,
        "title": "Yiren Digital Ltd."
    },
    "CNF": {
        "cik": 1733868,
        "title": "CNFinance Holdings Ltd."
    },
    "PTHR": {
        "cik": 1930021,
        "title": "Pono Capital Three, Inc."
    },
    "CMT": {
        "cik": 1026655,
        "title": "CORE MOLDING TECHNOLOGIES INC"
    },
    "IMMR": {
        "cik": 1058811,
        "title": "IMMERSION CORP"
    },
    "OCN": {
        "cik": 873860,
        "title": "OCWEN FINANCIAL CORP"
    },
    "EVTL": {
        "cik": 1867102,
        "title": "Vertical Aerospace Ltd."
    },
    "IIF": {
        "cik": 916618,
        "title": "MORGAN STANLEY INDIA INVESTMENT FUND, INC."
    },
    "NWFL": {
        "cik": 1013272,
        "title": "NORWOOD FINANCIAL CORP"
    },
    "ICTSF": {
        "cik": 1010134,
        "title": "ICTS INTERNATIONAL N V"
    },
    "KFS": {
        "cik": 1072627,
        "title": "KINGSWAY FINANCIAL SERVICES INC"
    },
    "SPWH": {
        "cik": 1132105,
        "title": "SPORTSMAN'S WAREHOUSE HOLDINGS, INC."
    },
    "BSVN": {
        "cik": 1746129,
        "title": "Bank7 Corp."
    },
    "DSKE": {
        "cik": 1642453,
        "title": "Daseke, Inc."
    },
    "III": {
        "cik": 1371489,
        "title": "Information Services Group Inc."
    },
    "GBBK": {
        "cik": 1894951,
        "title": "Global Blockchain Acquisition Corp."
    },
    "PCB": {
        "cik": 1423869,
        "title": "PCB BANCORP"
    },
    "AGD": {
        "cik": 1362481,
        "title": "abrdn Global Dynamic Dividend Fund"
    },
    "RBTK": {
        "cik": 1594204,
        "title": "ZHEN DING RESOURCES INC."
    },
    "NYXH": {
        "cik": 1857190,
        "title": "Nyxoah SA"
    },
    "QIPT": {
        "cik": 1540013,
        "title": "Quipt Home Medical Corp."
    },
    "INFU": {
        "cik": 1337013,
        "title": "InfuSystem Holdings, Inc"
    },
    "CTR": {
        "cik": 1547341,
        "title": "ClearBridge MLP & Midstream Total Return Fund Inc."
    },
    "ATXS": {
        "cik": 1454789,
        "title": "Astria Therapeutics, Inc."
    },
    "MASS": {
        "cik": 1555279,
        "title": "908 Devices Inc."
    },
    "RCAC": {
        "cik": 1874218,
        "title": "Revelstone Capital Acquisition Corp."
    },
    "VPV": {
        "cik": 895528,
        "title": "Invesco Pennsylvania Value Municipal Income Trust"
    },
    "SFST": {
        "cik": 1090009,
        "title": "SOUTHERN FIRST BANCSHARES INC"
    },
    "TWN": {
        "cik": 804123,
        "title": "TAIWAN FUND INC"
    },
    "OUST": {
        "cik": 1816581,
        "title": "Ouster, Inc."
    },
    "TCOA": {
        "cik": 1846750,
        "title": "Zalatoris Acquisition Corp."
    },
    "LUNA": {
        "cik": 1239819,
        "title": "LUNA INNOVATIONS INC"
    },
    "AOMR": {
        "cik": 1766478,
        "title": "Angel Oak Mortgage REIT, Inc."
    },
    "BOAC": {
        "cik": 1818089,
        "title": "Bluescape Opportunities Acquisition Corp."
    },
    "RMNI": {
        "cik": 1635282,
        "title": "Rimini Street, Inc."
    },
    "HYLN": {
        "cik": 1759631,
        "title": "Hyliion Holdings Corp."
    },
    "FNGR": {
        "cik": 1602409,
        "title": "FingerMotion, Inc."
    },
    "DC": {
        "cik": 1852353,
        "title": "Dakota Gold Corp."
    },
    "BZUN": {
        "cik": 1625414,
        "title": "Baozun Inc."
    },
    "CMAX": {
        "cik": 1813914,
        "title": "CareMax, Inc."
    },
    "NCZ": {
        "cik": 1227857,
        "title": "Virtus Convertible & Income Fund II"
    },
    "SCD": {
        "cik": 1270131,
        "title": "LMP CAPITAL & INCOME FUND INC."
    },
    "GRCL": {
        "cik": 1826492,
        "title": "Gracell Biotechnologies Inc."
    },
    "SLQT": {
        "cik": 1794783,
        "title": "SelectQuote, Inc."
    },
    "FENC": {
        "cik": 1211583,
        "title": "FENNEC PHARMACEUTICALS INC."
    },
    "TCX": {
        "cik": 909494,
        "title": "TUCOWS INC /PA/"
    },
    "SOL": {
        "cik": 1417892,
        "title": "Emeren Group Ltd"
    },
    "RLTY": {
        "cik": 1866874,
        "title": "Cohen & Steers Real Estate Opportunities & Income Fund"
    },
    "FRST": {
        "cik": 1325670,
        "title": "Primis Financial Corp."
    },
    "REAL": {
        "cik": 1573221,
        "title": "TheRealReal, Inc."
    },
    "CRMD": {
        "cik": 1410098,
        "title": "CorMedix Inc."
    },
    "FUST": {
        "cik": 1636051,
        "title": "FUSE GROUP HOLDING INC."
    },
    "FDEU": {
        "cik": 1646109,
        "title": "FIRST TRUST DYNAMIC EUROPE EQUITY INCOME FUND"
    },
    "TSI": {
        "cik": 809559,
        "title": "TCW STRATEGIC INCOME FUND INC"
    },
    "USCB": {
        "cik": 1901637,
        "title": "USCB FINANCIAL HOLDINGS, INC."
    },
    "TELA": {
        "cik": 1561921,
        "title": "TELA Bio, Inc."
    },
    "AEVA": {
        "cik": 1789029,
        "title": "Aeva Technologies, Inc."
    },
    "STRS": {
        "cik": 885508,
        "title": "STRATUS PROPERTIES INC"
    },
    "OPRT": {
        "cik": 1538716,
        "title": "Oportun Financial Corp"
    },
    "AIP": {
        "cik": 1667011,
        "title": "Arteris, Inc."
    },
    "MQT": {
        "cik": 887394,
        "title": "BLACKROCK MUNIYIELD QUALITY FUND II, INC."
    },
    "AENT": {
        "cik": 1823584,
        "title": "ALLIANCE ENTERTAINMENT HOLDING CORP"
    },
    "STKS": {
        "cik": 1399520,
        "title": "ONE Group Hospitality, Inc."
    },
    "FRGI": {
        "cik": 1534992,
        "title": "Fiesta Restaurant Group, Inc."
    },
    "MOLN": {
        "cik": 1745114,
        "title": "MOLECULAR PARTNERS AG"
    },
    "WEWA": {
        "cik": 1616156,
        "title": "WEWARDS, INC."
    },
    "SDC": {
        "cik": 1775625,
        "title": "SmileDirectClub, Inc."
    },
    "GROY": {
        "cik": 1834026,
        "title": "Gold Royalty Corp."
    },
    "MVT": {
        "cik": 897269,
        "title": "BLACKROCK MUNIVEST FUND II, INC."
    },
    "FLJ": {
        "cik": 1769256,
        "title": "FLJ Group Ltd"
    },
    "BIG": {
        "cik": 768835,
        "title": "BIG LOTS INC"
    },
    "PSF": {
        "cik": 1498612,
        "title": "Cohen & Steers Select Preferred & Income Fund, Inc."
    },
    "SCWO": {
        "cik": 933972,
        "title": "374Water Inc."
    },
    "IRRX": {
        "cik": 1854795,
        "title": "INTEGRATED RAIL & RESOURCES ACQUISITION CORP"
    },
    "MTA": {
        "cik": 1722606,
        "title": "Metalla Royalty & Streaming Ltd."
    },
    "CUTR": {
        "cik": 1162461,
        "title": "CUTERA INC"
    },
    "HSDT": {
        "cik": 1610853,
        "title": "HELIUS MEDICAL TECHNOLOGIES, INC."
    },
    "MESO": {
        "cik": 1345099,
        "title": "MESOBLAST LTD"
    },
    "PRPC": {
        "cik": 1821329,
        "title": "CC Neuberger Principal Holdings III"
    },
    "RIGL": {
        "cik": 1034842,
        "title": "RIGEL PHARMACEUTICALS INC"
    },
    "PKBK": {
        "cik": 1315399,
        "title": "PARKE BANCORP, INC."
    },
    "HSHP": {
        "cik": 1959455,
        "title": "Himalaya Shipping Ltd."
    },
    "OVLY": {
        "cik": 1431567,
        "title": "Oak Valley Bancorp"
    },
    "MUE": {
        "cik": 1071899,
        "title": "BLACKROCK MUNIHOLDINGS QUALITY FUND II, INC."
    },
    "TPIC": {
        "cik": 1455684,
        "title": "TPI COMPOSITES, INC"
    },
    "RDW": {
        "cik": 1819810,
        "title": "Redwire Corp"
    },
    "ARTE": {
        "cik": 1839990,
        "title": "Artemis Strategic Investment Corp"
    },
    "LAB": {
        "cik": 1162194,
        "title": "STANDARD BIOTOOLS INC."
    },
    "TUSK": {
        "cik": 1679268,
        "title": "MAMMOTH ENERGY SERVICES, INC."
    },
    "FTCI": {
        "cik": 1828161,
        "title": "FTC Solar, Inc."
    },
    "FSTR": {
        "cik": 352825,
        "title": "FOSTER L B CO"
    },
    "INZY": {
        "cik": 1693011,
        "title": "Inozyme Pharma, Inc."
    },
    "VRA": {
        "cik": 1495320,
        "title": "Vera Bradley, Inc."
    },
    "ESCA": {
        "cik": 33488,
        "title": "ESCALADE INC"
    },
    "GPJA": {
        "cik": 41091,
        "title": "GEORGIA POWER CO"
    },
    "CNLHN": {
        "cik": 23426,
        "title": "CONNECTICUT LIGHT & POWER CO"
    },
    "CELC": {
        "cik": 1603454,
        "title": "Celcuity Inc."
    },
    "ARBE": {
        "cik": 1861841,
        "title": "Arbe Robotics Ltd."
    },
    "VBNK": {
        "cik": 1690639,
        "title": "VersaBank"
    },
    "SBXC": {
        "cik": 1859686,
        "title": "SilverBox Corp III"
    },
    "PSTX": {
        "cik": 1661460,
        "title": "Poseida Therapeutics, Inc."
    },
    "IKNA": {
        "cik": 1835579,
        "title": "Ikena Oncology, Inc."
    },
    "MFM": {
        "cik": 801961,
        "title": "MFS MUNICIPAL INCOME TRUST"
    },
    "AUGX": {
        "cik": 1769804,
        "title": "Augmedix, Inc."
    },
    "EHTH": {
        "cik": 1333493,
        "title": "eHealth, Inc."
    },
    "EAXR": {
        "cik": 832370,
        "title": "Ealixir, Inc."
    },
    "BTBT": {
        "cik": 1710350,
        "title": "Bit Digital, Inc"
    },
    "DNMR": {
        "cik": 1779020,
        "title": "Danimer Scientific, Inc."
    },
    "TSBX": {
        "cik": 1764974,
        "title": "Turnstone Biologics Corp."
    },
    "ISRL": {
        "cik": 1915328,
        "title": "Israel Acquisitions Corp"
    },
    "FVCB": {
        "cik": 1675644,
        "title": "FVCBankcorp, Inc."
    },
    "SKIL": {
        "cik": 1774675,
        "title": "Skillsoft Corp."
    },
    "BIOS": {
        "cik": 1856653,
        "title": "BioPlus Acquisition Corp."
    },
    "RPHM": {
        "cik": 1637715,
        "title": "Reneo Pharmaceuticals, Inc."
    },
    "EGAN": {
        "cik": 1066194,
        "title": "EGAIN Corp"
    },
    "GLO": {
        "cik": 1350869,
        "title": "Clough Global Opportunities Fund"
    },
    "EMCG": {
        "cik": 1869601,
        "title": "Embrace Change Acquisition Corp."
    },
    "REKR": {
        "cik": 1697851,
        "title": "Rekor Systems, Inc."
    },
    "NUTX": {
        "cik": 1479681,
        "title": "Nutex Health, Inc."
    },
    "HYBT": {
        "cik": 1086303,
        "title": "Heyu Biological Technology Corp"
    },
    "FXE": {
        "cik": 1328598,
        "title": "Invesco CurrencyShares Euro Trust"
    },
    "PDLB": {
        "cik": 1874071,
        "title": "Ponce Financial Group, Inc."
    },
    "IFRX": {
        "cik": 1708688,
        "title": "InflaRx N.V."
    },
    "AFT": {
        "cik": 1502573,
        "title": "Apollo Senior Floating Rate Fund Inc."
    },
    "PHYT": {
        "cik": 1848756,
        "title": "Pyrophyte Acquisition Corp."
    },
    "LTRY": {
        "cik": 1673481,
        "title": "Lottery.com Inc."
    },
    "SWKH": {
        "cik": 1089907,
        "title": "SWK Holdings Corp"
    },
    "MRAM": {
        "cik": 1438423,
        "title": "EVERSPIN TECHNOLOGIES INC"
    },
    "RCFA": {
        "cik": 1870143,
        "title": "RCF Acquisition Corp."
    },
    "HRTX": {
        "cik": 818033,
        "title": "HERON THERAPEUTICS, INC. /DE/"
    },
    "JCE": {
        "cik": 1385763,
        "title": "Nuveen Core Equity Alpha Fund"
    },
    "PLBC": {
        "cik": 1168455,
        "title": "PLUMAS BANCORP"
    },
    "ORGN": {
        "cik": 1802457,
        "title": "Origin Materials, Inc."
    },
    "JRS": {
        "cik": 1158289,
        "title": "NUVEEN REAL ESTATE INCOME FUND"
    },
    "BIRD": {
        "cik": 1653909,
        "title": "Allbirds, Inc."
    },
    "BWFG": {
        "cik": 1505732,
        "title": "Bankwell Financial Group, Inc."
    },
    "RANI": {
        "cik": 1856725,
        "title": "Rani Therapeutics Holdings, Inc."
    },
    "VOR": {
        "cik": 1817229,
        "title": "Vor Biopharma Inc."
    },
    "TOP": {
        "cik": 1848275,
        "title": "TOP Financial Group Ltd"
    },
    "JOF": {
        "cik": 859796,
        "title": "JAPAN SMALLER CAPITALIZATION FUND INC"
    },
    "GENC": {
        "cik": 64472,
        "title": "GENCOR INDUSTRIES INC"
    },
    "MAPS": {
        "cik": 1779474,
        "title": "WM TECHNOLOGY, INC."
    },
    "HYW": {
        "cik": 1785680,
        "title": "Hywin Holdings Ltd."
    },
    "BBAI": {
        "cik": 1836981,
        "title": "BigBear.ai Holdings, Inc."
    },
    "LIAN": {
        "cik": 1831283,
        "title": "LianBio"
    },
    "VZLA": {
        "cik": 1796073,
        "title": "Vizsla Silver Corp."
    },
    "ELLO": {
        "cik": 946394,
        "title": "Ellomay Capital Ltd."
    },
    "CVLY": {
        "cik": 806279,
        "title": "CODORUS VALLEY BANCORP INC"
    },
    "SSBK": {
        "cik": 1689731,
        "title": "Southern States Bancshares, Inc."
    },
    "EDTX": {
        "cik": 1817153,
        "title": "EdtechX Holdings Acquisition Corp. II"
    },
    "EVER": {
        "cik": 1640428,
        "title": "EverQuote, Inc."
    },
    "FGPR": {
        "cik": 922358,
        "title": "FERRELLGAS PARTNERS L P"
    },
    "PPYA": {
        "cik": 1894057,
        "title": "Papaya Growth Opportunity Corp. I"
    },
    "RYAM": {
        "cik": 1597672,
        "title": "RAYONIER ADVANCED MATERIALS INC."
    },
    "KGNR": {
        "cik": 1593773,
        "title": "AMJ Global Technology"
    },
    "VOXX": {
        "cik": 807707,
        "title": "VOXX International Corp"
    },
    "ACV": {
        "cik": 1636289,
        "title": "Virtus Diversified Income & Convertible Fund"
    },
    "EP": {
        "cik": 887396,
        "title": "EMPIRE PETROLEUM CORP"
    },
    "NGM": {
        "cik": 1426332,
        "title": "NGM BIOPHARMACEUTICALS INC"
    },
    "XFOR": {
        "cik": 1501697,
        "title": "X4 Pharmaceuticals, Inc"
    },
    "MCAA": {
        "cik": 1856995,
        "title": "Mountain & Co. I Acquisition Corp."
    },
    "DMB": {
        "cik": 1565381,
        "title": "BNY Mellon Municipal Bond Infrastructure Fund, Inc."
    },
    "CMCL": {
        "cik": 766011,
        "title": "Caledonia Mining Corp Plc"
    },
    "CLMB": {
        "cik": 945983,
        "title": "Climb Global Solutions, Inc."
    },
    "BGFV": {
        "cik": 1156388,
        "title": "BIG 5 SPORTING GOODS Corp"
    },
    "TIO": {
        "cik": 854800,
        "title": "Tingo Group, Inc."
    },
    "AMTX": {
        "cik": 738214,
        "title": "AEMETIS, INC"
    },
    "WATT": {
        "cik": 1575793,
        "title": "Energous Corp"
    },
    "CNTY": {
        "cik": 911147,
        "title": "CENTURY CASINOS INC /CO/"
    },
    "BKSY": {
        "cik": 1753539,
        "title": "BlackSky Technology Inc."
    },
    "CIO": {
        "cik": 1593222,
        "title": "City Office REIT, Inc."
    },
    "PHT": {
        "cik": 1166258,
        "title": "PIONEER HIGH INCOME FUND, INC."
    },
    "LLAP": {
        "cik": 1835512,
        "title": "Terran Orbital Corp"
    },
    "ERLFF": {
        "cik": 1271554,
        "title": "Entree Resources Ltd."
    },
    "BKN": {
        "cik": 894242,
        "title": "BLACKROCK INVESTMENT QUALITY MUNICIPAL TRUST, INC."
    },
    "ALXO": {
        "cik": 1810182,
        "title": "ALX ONCOLOGY HOLDINGS INC"
    },
    "HOLO": {
        "cik": 1841209,
        "title": "MicroCloud Hologram Inc."
    },
    "CAPR": {
        "cik": 1133869,
        "title": "CAPRICOR THERAPEUTICS, INC."
    },
    "CFFI": {
        "cik": 913341,
        "title": "C & F FINANCIAL CORP"
    },
    "DHY": {
        "cik": 1061353,
        "title": "CREDIT SUISSE HIGH YIELD BOND FUND"
    },
    "VABK": {
        "cik": 1572334,
        "title": "Virginia National Bankshares Corp"
    },
    "PPTA": {
        "cik": 1526243,
        "title": "PERPETUA RESOURCES CORP."
    },
    "MFIN": {
        "cik": 1000209,
        "title": "MEDALLION FINANCIAL CORP"
    },
    "LFAC": {
        "cik": 1851266,
        "title": "LF Capital Acquisition Corp. II"
    },
    "TWIN": {
        "cik": 100378,
        "title": "TWIN DISC INC"
    },
    "CYDY": {
        "cik": 1175680,
        "title": "CytoDyn Inc."
    },
    "BHR": {
        "cik": 1574085,
        "title": "Braemar Hotels & Resorts Inc."
    },
    "CHMG": {
        "cik": 763563,
        "title": "CHEMUNG FINANCIAL CORP"
    },
    "INVE": {
        "cik": 1036044,
        "title": "Identiv, Inc."
    },
    "BCBP": {
        "cik": 1228454,
        "title": "BCB BANCORP INC"
    },
    "OPP": {
        "cik": 1678130,
        "title": "RiverNorth/DoubleLine Strategic Opportunity Fund, Inc."
    },
    "HEAR": {
        "cik": 1493761,
        "title": "Turtle Beach Corp"
    },
    "TENK": {
        "cik": 1851484,
        "title": "TenX Keane Acquisition"
    },
    "ASRT": {
        "cik": 1808665,
        "title": "Assertio Holdings, Inc."
    },
    "NXMH": {
        "cik": 1811530,
        "title": "Next Meats Holdings, Inc."
    },
    "TRUE": {
        "cik": 1327318,
        "title": "TrueCar, Inc."
    },
    "NTG": {
        "cik": 1490286,
        "title": "Tortoise Midstream Energy Fund, Inc."
    },
    "LGI": {
        "cik": 1278211,
        "title": "LAZARD GLOBAL TOTAL RETURN & INCOME FUND INC"
    },
    "VTN": {
        "cik": 883265,
        "title": "Invesco Trust for Investment Grade New York Municipals"
    },
    "GWH": {
        "cik": 1819438,
        "title": "ESS Tech, Inc."
    },
    "DBB": {
        "cik": 1383084,
        "title": "INVESCO DB BASE METALS FUND"
    },
    "WIA": {
        "cik": 1254370,
        "title": "WESTERN ASSET INFLATION-LINKED INCOME FUND"
    },
    "RLYB": {
        "cik": 1739410,
        "title": "Rallybio Corp"
    },
    "AURC": {
        "cik": 1835856,
        "title": "Aurora Acquisition Corp."
    },
    "JAKK": {
        "cik": 1009829,
        "title": "JAKKS PACIFIC INC"
    },
    "PTMN": {
        "cik": 1372807,
        "title": "Portman Ridge Finance Corp"
    },
    "GASS": {
        "cik": 1328919,
        "title": "StealthGas Inc."
    },
    "NBH": {
        "cik": 1178839,
        "title": "NEUBERGER BERMAN MUNICIPAL FUND INC."
    },
    "AIF": {
        "cik": 1526697,
        "title": "Apollo Tactical Income Fund Inc."
    },
    "EMX": {
        "cik": 1285786,
        "title": "EMX Royalty Corp"
    },
    "VIGL": {
        "cik": 1827087,
        "title": "Vigil Neuroscience, Inc."
    },
    "NPV": {
        "cik": 897421,
        "title": "NUVEEN VIRGINIA QUALITY MUNICIPAL INCOME FUND"
    },
    "FSP": {
        "cik": 1031316,
        "title": "FRANKLIN STREET PROPERTIES CORP /MA/"
    },
    "ETX": {
        "cik": 1563696,
        "title": "Eaton Vance Municipal Income 2028 Term Trust"
    },
    "EMP": {
        "cik": 66901,
        "title": "ENTERGY MISSISSIPPI, LLC"
    },
    "VRCA": {
        "cik": 1660334,
        "title": "Verrica Pharmaceuticals Inc."
    },
    "CCHWF": {
        "cik": 1776738,
        "title": "Columbia Care Inc."
    },
    "GNFT": {
        "cik": 1757064,
        "title": "Genfit S.A."
    },
    "STBX": {
        "cik": 1914818,
        "title": "Starbox Group Holdings Ltd."
    },
    "EOD": {
        "cik": 1386067,
        "title": "ALLSPRING GLOBAL DIVIDEND OPPORTUNITY FUND"
    },
    "PROF": {
        "cik": 1628808,
        "title": "Profound Medical Corp."
    },
    "PWOD": {
        "cik": 716605,
        "title": "PENNS WOODS BANCORP INC"
    },
    "INTT": {
        "cik": 1036262,
        "title": "INTEST CORP"
    },
    "MHI": {
        "cik": 1223026,
        "title": "PIONEER MUNICIPAL HIGH INCOME FUND, INC."
    },
    "HGLB": {
        "cik": 1622148,
        "title": "HIGHLAND GLOBAL ALLOCATION FUND"
    },
    "CCRD": {
        "cik": 320340,
        "title": "CoreCard Corp"
    },
    "HLCO": {
        "cik": 1441082,
        "title": "Healing Co Inc."
    },
    "CPSS": {
        "cik": 889609,
        "title": "CONSUMER PORTFOLIO SERVICES, INC."
    },
    "HIE": {
        "cik": 1519505,
        "title": "Miller/Howard High Income Equity Fund"
    },
    "IVVD": {
        "cik": 1832038,
        "title": "Invivyd, Inc."
    },
    "PNRG": {
        "cik": 56868,
        "title": "PRIMEENERGY RESOURCES CORP"
    },
    "DOUG": {
        "cik": 1878897,
        "title": "Douglas Elliman Inc."
    },
    "MHLD": {
        "cik": 1412100,
        "title": "Maiden Holdings, Ltd."
    },
    "RGCO": {
        "cik": 1069533,
        "title": "RGC RESOURCES INC"
    },
    "SAMG": {
        "cik": 1549966,
        "title": "Silvercrest Asset Management Group Inc."
    },
    "MYFW": {
        "cik": 1327607,
        "title": "First Western Financial Inc"
    },
    "KPTI": {
        "cik": 1503802,
        "title": "Karyopharm Therapeutics Inc."
    },
    "ZOM": {
        "cik": 1684144,
        "title": "Zomedica Corp."
    },
    "SMLR": {
        "cik": 1554859,
        "title": "Semler Scientific, Inc."
    },
    "ENJ": {
        "cik": 71508,
        "title": "ENTERGY NEW ORLEANS, LLC"
    },
    "GDO": {
        "cik": 1472341,
        "title": "WESTERN ASSET GLOBAL CORPORATE DEFINED OPPORTUNITY FUND INC."
    },
    "PCK": {
        "cik": 1170300,
        "title": "PIMCO CALIFORNIA MUNICIPAL INCOME FUND II"
    },
    "XYF": {
        "cik": 1725033,
        "title": "X Financial"
    },
    "FUSN": {
        "cik": 1805890,
        "title": "Fusion Pharmaceuticals Inc."
    },
    "CTRN": {
        "cik": 1318484,
        "title": "Citi Trends Inc"
    },
    "PRAX": {
        "cik": 1689548,
        "title": "Praxis Precision Medicines, Inc."
    },
    "OPT": {
        "cik": 1815620,
        "title": "Opthea Ltd"
    },
    "EMF": {
        "cik": 809708,
        "title": "TEMPLETON EMERGING MARKETS FUND"
    },
    "BRKH": {
        "cik": 1871638,
        "title": "BurTech Acquisition Corp."
    },
    "VADP": {
        "cik": 1700849,
        "title": "Vado Corp."
    },
    "DHX": {
        "cik": 1393883,
        "title": "DHI GROUP, INC."
    },
    "RGC": {
        "cik": 1829667,
        "title": "Regencell Bioscience Holdings Ltd"
    },
    "VAQC": {
        "cik": 1842386,
        "title": "Vector Acquisition Corp II"
    },
    "ALCO": {
        "cik": 3545,
        "title": "ALICO, INC."
    },
    "XOMA": {
        "cik": 791908,
        "title": "XOMA Corp"
    },
    "BPRN": {
        "cik": 1913971,
        "title": "Princeton Bancorp, Inc."
    },
    "CANO": {
        "cik": 1800682,
        "title": "Cano Health, Inc."
    },
    "CBAN": {
        "cik": 711669,
        "title": "COLONY BANKCORP INC"
    },
    "COFS": {
        "cik": 803164,
        "title": "CHOICEONE FINANCIAL SERVICES INC"
    },
    "PCQ": {
        "cik": 1140411,
        "title": "PIMCO CALIFORNIA MUNICIPAL INCOME FUND"
    },
    "PRST": {
        "cik": 1822145,
        "title": "Presto Automation Inc."
    },
    "MAV": {
        "cik": 1258943,
        "title": "PIONEER MUNICIPAL HIGH INCOME ADVANTAGE FUND, INC."
    },
    "ACB": {
        "cik": 1683541,
        "title": "AURORA CANNABIS INC"
    },
    "PFMT": {
        "cik": 1550695,
        "title": "Performant Financial Corp"
    },
    "ITI": {
        "cik": 350868,
        "title": "ITERIS, INC."
    },
    "ESEA": {
        "cik": 1341170,
        "title": "EUROSEAS LTD."
    },
    "SKLZ": {
        "cik": 1801661,
        "title": "Skillz Inc."
    },
    "RPMT": {
        "cik": 1437283,
        "title": "REGO PAYMENT ARCHITECTURES, INC."
    },
    "FSNB": {
        "cik": 1840225,
        "title": "Fusion Acquisition Corp. II"
    },
    "OMGA": {
        "cik": 1850838,
        "title": "Omega Therapeutics, Inc."
    },
    "HBIO": {
        "cik": 1123494,
        "title": "HARVARD BIOSCIENCE INC"
    },
    "IHIT": {
        "cik": 1682811,
        "title": "INVESCO HIGH INCOME 2023 TARGET TERM FUND"
    },
    "ADAP": {
        "cik": 1621227,
        "title": "Adaptimmune Therapeutics PLC"
    },
    "TOUR": {
        "cik": 1597095,
        "title": "Tuniu Corp"
    },
    "LCNB": {
        "cik": 1074902,
        "title": "LCNB CORP"
    },
    "STHO": {
        "cik": 1953366,
        "title": "Star Holdings"
    },
    "SKYX": {
        "cik": 1598981,
        "title": "SKYX Platforms Corp."
    },
    "QBTS": {
        "cik": 1907982,
        "title": "D-Wave Quantum Inc."
    },
    "SNFCA": {
        "cik": 318673,
        "title": "SECURITY NATIONAL FINANCIAL CORP"
    },
    "KNOP": {
        "cik": 1564180,
        "title": "KNOT Offshore Partners LP"
    },
    "VRDR": {
        "cik": 1506929,
        "title": "VERDE RESOURCES, INC."
    },
    "PUCK": {
        "cik": 1836100,
        "title": "Goal Acquisitions Corp."
    },
    "PRLD": {
        "cik": 1678660,
        "title": "Prelude Therapeutics Inc"
    },
    "MACK": {
        "cik": 1274792,
        "title": "MERRIMACK PHARMACEUTICALS INC"
    },
    "MTRX": {
        "cik": 866273,
        "title": "MATRIX SERVICE CO"
    },
    "MIO": {
        "cik": 1864290,
        "title": "Pioneer Municipal High Income Opportunities Fund, Inc."
    },
    "HMST": {
        "cik": 1518715,
        "title": "HomeStreet, Inc."
    },
    "SELB": {
        "cik": 1453687,
        "title": "SELECTA BIOSCIENCES INC"
    },
    "GHM": {
        "cik": 716314,
        "title": "GRAHAM CORP"
    },
    "HHLA": {
        "cik": 1824185,
        "title": "HH&L Acquisition Co."
    },
    "KLXE": {
        "cik": 1738827,
        "title": "KLX Energy Services Holdings, Inc."
    },
    "SILC": {
        "cik": 916793,
        "title": "SILICOM LTD."
    },
    "LRMR": {
        "cik": 1374690,
        "title": "Larimar Therapeutics, Inc."
    },
    "OXSQ": {
        "cik": 1259429,
        "title": "Oxford Square Capital Corp."
    },
    "IGI": {
        "cik": 1462586,
        "title": "Western Asset Investment Grade Defined Opportunity Trust Inc."
    },
    "ESSA": {
        "cik": 1382230,
        "title": "ESSA Bancorp, Inc."
    },
    "INBK": {
        "cik": 1562463,
        "title": "First Internet Bancorp"
    },
    "PESI": {
        "cik": 891532,
        "title": "PERMA FIX ENVIRONMENTAL SERVICES INC"
    },
    "MNSB": {
        "cik": 1693577,
        "title": "MainStreet Bancshares, Inc."
    },
    "VAPO": {
        "cik": 1253176,
        "title": "VAPOTHERM INC"
    },
    "RRGB": {
        "cik": 1171759,
        "title": "RED ROBIN GOURMET BURGERS INC"
    },
    "BSL": {
        "cik": 1486298,
        "title": "Blackstone Senior Floating Rate 2027 Term Fund"
    },
    "ALYA": {
        "cik": 1734520,
        "title": "Alithya Group inc"
    },
    "PDSB": {
        "cik": 1472091,
        "title": "PDS Biotechnology Corp"
    },
    "HYPR": {
        "cik": 1833769,
        "title": "Hyperfine, Inc."
    },
    "PZC": {
        "cik": 1181504,
        "title": "PIMCO CALIFORNIA MUNICIPAL INCOME FUND III"
    },
    "ZVRA": {
        "cik": 1434647,
        "title": "ZEVRA THERAPEUTICS, INC."
    },
    "FT": {
        "cik": 833040,
        "title": "FRANKLIN UNIVERSAL TRUST"
    },
    "IVA": {
        "cik": 1756594,
        "title": "Inventiva S.A."
    },
    "PIIVX": {
        "cik": 1557265,
        "title": "Private Shares Fund"
    },
    "OAKC": {
        "cik": 1588871,
        "title": "Oakworth Capital, Inc."
    },
    "CVCY": {
        "cik": 1127371,
        "title": "CENTRAL VALLEY COMMUNITY BANCORP"
    },
    "TG": {
        "cik": 850429,
        "title": "TREDEGAR CORP"
    },
    "LGST": {
        "cik": 1860871,
        "title": "Semper Paratus Acquisition Corp"
    },
    "IFIN": {
        "cik": 1862935,
        "title": "InFinT Acquisition Corp"
    },
    "MG": {
        "cik": 1436126,
        "title": "Mistras Group, Inc."
    },
    "TEAF": {
        "cik": 1704299,
        "title": "ECOFIN SUSTAINABLE & SOCIAL IMPACT TERM FUND"
    },
    "WKHS": {
        "cik": 1425287,
        "title": "Workhorse Group Inc."
    },
    "PVBC": {
        "cik": 1778784,
        "title": "Provident Bancorp, Inc. /MD/"
    },
    "LTRPA": {
        "cik": 1606745,
        "title": "Liberty TripAdvisor Holdings, Inc."
    },
    "GRWG": {
        "cik": 1604868,
        "title": "GrowGeneration Corp."
    },
    "ZVIA": {
        "cik": 1854139,
        "title": "Zevia PBC"
    },
    "FLL": {
        "cik": 891482,
        "title": "FULL HOUSE RESORTS INC"
    },
    "AGAC": {
        "cik": 1833909,
        "title": "African Gold Acquisition Corp"
    },
    "NUBI": {
        "cik": 1881551,
        "title": "Nubia Brand International Corp."
    },
    "VBF": {
        "cik": 5094,
        "title": "Invesco Bond Fund"
    },
    "RELL": {
        "cik": 355948,
        "title": "RICHARDSON ELECTRONICS, LTD."
    },
    "GRIN": {
        "cik": 1725293,
        "title": "Grindrod Shipping Holdings Ltd."
    },
    "PEPG": {
        "cik": 1835597,
        "title": "PepGen Inc."
    },
    "FREE": {
        "cik": 1753706,
        "title": "Whole Earth Brands, Inc."
    },
    "BCOV": {
        "cik": 1313275,
        "title": "BRIGHTCOVE INC"
    },
    "PBYI": {
        "cik": 1401667,
        "title": "PUMA BIOTECHNOLOGY, INC."
    },
    "LYBC": {
        "cik": 816332,
        "title": "LYONS BANCORP INC"
    },
    "CANG": {
        "cik": 1725123,
        "title": "Cango Inc."
    },
    "GDHG": {
        "cik": 1928340,
        "title": "GOLDEN HEAVEN GROUP HOLDINGS LTD."
    },
    "LYRA": {
        "cik": 1327273,
        "title": "Lyra Therapeutics, Inc."
    },
    "EACO": {
        "cik": 784539,
        "title": "EACO CORP"
    },
    "DIBS": {
        "cik": 1600641,
        "title": "1stdibs.com, Inc."
    },
    "BDTX": {
        "cik": 1701541,
        "title": "Black Diamond Therapeutics, Inc."
    },
    "MRCC": {
        "cik": 1512931,
        "title": "MONROE CAPITAL Corp"
    },
    "RCMT": {
        "cik": 700841,
        "title": "RCM TECHNOLOGIES, INC."
    },
    "ADRT": {
        "cik": 1864032,
        "title": "Ault Disruptive Technologies Corp"
    },
    "VNJA": {
        "cik": 1532383,
        "title": "VANJIA CORP"
    },
    "WILC": {
        "cik": 1030997,
        "title": "G WILLI FOOD INTERNATIONAL LTD"
    },
    "VRM": {
        "cik": 1580864,
        "title": "Vroom, Inc."
    },
    "PCYG": {
        "cik": 50471,
        "title": "PARK CITY GROUP INC"
    },
    "CARA": {
        "cik": 1346830,
        "title": "Cara Therapeutics, Inc."
    },
    "ENX": {
        "cik": 1177162,
        "title": "EATON VANCE NEW YORK MUNICIPAL BOND FUND"
    },
    "GGT": {
        "cik": 921671,
        "title": "GABELLI MULTIMEDIA TRUST INC."
    },
    "IH": {
        "cik": 1814423,
        "title": "iHuman Inc."
    },
    "CCLP": {
        "cik": 1449488,
        "title": "CSI Compressco LP"
    },
    "ALSA": {
        "cik": 1865111,
        "title": "Alpha Star Acquisition Corp"
    },
    "ATLO": {
        "cik": 1132651,
        "title": "AMES NATIONAL CORP"
    },
    "EVGR": {
        "cik": 1900402,
        "title": "Evergreen Corp"
    },
    "EMAN": {
        "cik": 1046995,
        "title": "EMAGIN CORP"
    },
    "INSI": {
        "cik": 30125,
        "title": "Insight Select Income Fund"
    },
    "CTG": {
        "cik": 23111,
        "title": "COMPUTER TASK GROUP INC"
    },
    "RTGN": {
        "cik": 1836295,
        "title": "RetinalGenix Technologies Inc."
    },
    "FTII": {
        "cik": 1889450,
        "title": "FutureTech II Acquisition Corp."
    },
    "FLME": {
        "cik": 1831481,
        "title": "Flame Acquisition Corp."
    },
    "SQNS": {
        "cik": 1383395,
        "title": "SEQUANS COMMUNICATIONS"
    },
    "GRX": {
        "cik": 1391437,
        "title": "Gabelli Healthcare & WellnessRx Trust"
    },
    "IMAB": {
        "cik": 1778016,
        "title": "I-Mab"
    },
    "CCCC": {
        "cik": 1662579,
        "title": "C4 Therapeutics, Inc."
    },
    "TGAN": {
        "cik": 1715768,
        "title": "Transphorm, Inc."
    },
    "ATNM": {
        "cik": 1388320,
        "title": "Actinium Pharmaceuticals, Inc."
    },
    "TSQ": {
        "cik": 1499832,
        "title": "Townsquare Media, Inc."
    },
    "BCSA": {
        "cik": 1873441,
        "title": "Blockchain Coinvestors Acquisition Corp. I"
    },
    "MNMD": {
        "cik": 1813814,
        "title": "Mind Medicine (MindMed) Inc."
    },
    "ADVM": {
        "cik": 1501756,
        "title": "Adverum Biotechnologies, Inc."
    },
    "KRNL": {
        "cik": 1832950,
        "title": "Kernel Group Holdings, Inc."
    },
    "VCXB": {
        "cik": 1848948,
        "title": "10X Capital Venture Acquisition Corp. III"
    },
    "EVBN": {
        "cik": 842518,
        "title": "EVANS BANCORP INC"
    },
    "LVO": {
        "cik": 1491419,
        "title": "LiveOne, Inc."
    },
    "CFNB": {
        "cik": 803016,
        "title": "CALIFORNIA FIRST LEASING CORP"
    },
    "ATOM": {
        "cik": 1420520,
        "title": "Atomera Inc"
    },
    "IMMP": {
        "cik": 1506184,
        "title": "IMMUTEP Ltd"
    },
    "APYX": {
        "cik": 719135,
        "title": "Apyx Medical Corp"
    },
    "EHI": {
        "cik": 1228509,
        "title": "WESTERN ASSET GLOBAL HIGH INCOME FUND INC."
    },
    "AVBH": {
        "cik": 1443575,
        "title": "Avidbank Holdings, Inc."
    },
    "ROSS": {
        "cik": 1841610,
        "title": "Ross Acquisition Corp II"
    },
    "IPSC": {
        "cik": 1850119,
        "title": "Century Therapeutics, Inc."
    },
    "KYCH": {
        "cik": 1865701,
        "title": "Keyarch Acquisition Corp"
    },
    "DHF": {
        "cik": 1057861,
        "title": "BNY MELLON HIGH YIELD STRATEGIES FUND"
    },
    "MPAA": {
        "cik": 918251,
        "title": "MOTORCAR PARTS OF AMERICA INC"
    },
    "CRNT": {
        "cik": 1119769,
        "title": "CERAGON NETWORKS LTD"
    },
    "NMG": {
        "cik": 1649752,
        "title": "Nouveau Monde Graphite Inc."
    },
    "SGMO": {
        "cik": 1001233,
        "title": "SANGAMO THERAPEUTICS, INC"
    },
    "CTV": {
        "cik": 1835378,
        "title": "Innovid Corp."
    },
    "NKSH": {
        "cik": 796534,
        "title": "NATIONAL BANKSHARES INC"
    },
    "SEVN": {
        "cik": 1452477,
        "title": "Seven Hills Realty Trust"
    },
    "CATO": {
        "cik": 18255,
        "title": "CATO CORP"
    },
    "SEER": {
        "cik": 1726445,
        "title": "Seer, Inc."
    },
    "AENZ": {
        "cik": 1572621,
        "title": "AENZA S.A.A."
    },
    "NNY": {
        "cik": 818850,
        "title": "NUVEEN NEW YORK MUNICIPAL VALUE FUND"
    },
    "PIM": {
        "cik": 830622,
        "title": "PUTNAM MASTER INTERMEDIATE INCOME TRUST"
    },
    "LAZY": {
        "cik": 1721741,
        "title": "Lazydays Holdings, Inc."
    },
    "AFAR": {
        "cik": 1901886,
        "title": "Aura Fat Projects Acquisition Corp"
    },
    "CBH": {
        "cik": 1701809,
        "title": "Virtus Convertible & Income 2024 Target Term Fund"
    },
    "JSPR": {
        "cik": 1788028,
        "title": "Jasper Therapeutics, Inc."
    },
    "DBP": {
        "cik": 1383057,
        "title": "Invesco DB Precious Metals Fund"
    },
    "LCUT": {
        "cik": 874396,
        "title": "LIFETIME BRANDS, INC"
    },
    "SOPH": {
        "cik": 1840706,
        "title": "SOPHiA GENETICS SA"
    },
    "WEL": {
        "cik": 1877557,
        "title": "Integrated Wellness Acquisition Corp"
    },
    "MREO": {
        "cik": 1719714,
        "title": "Mereo Biopharma Group plc"
    },
    "ANNX": {
        "cik": 1528115,
        "title": "Annexon, Inc."
    },
    "CALB": {
        "cik": 1752036,
        "title": "California BanCorp"
    },
    "YTRA": {
        "cik": 1516899,
        "title": "Yatra Online, Inc."
    },
    "VCIG": {
        "cik": 1930510,
        "title": "VCI Global Ltd"
    },
    "KOPN": {
        "cik": 771266,
        "title": "KOPIN CORP"
    },
    "CHEA": {
        "cik": 1856948,
        "title": "Chenghe Acquisition Co."
    },
    "HYB": {
        "cik": 825345,
        "title": "NEW AMERICA HIGH INCOME FUND INC"
    },
    "DCFC": {
        "cik": 1862490,
        "title": "Tritium DCFC Ltd"
    },
    "ANZU": {
        "cik": 1840877,
        "title": "Anzu Special Acquisition Corp I"
    },
    "ROCL": {
        "cik": 1885998,
        "title": "Roth CH Acquisition V Co."
    },
    "EFHT": {
        "cik": 1922858,
        "title": "EF Hutton Acquisition Corp I"
    },
    "CSTE": {
        "cik": 1504379,
        "title": "Caesarstone Ltd."
    },
    "ABSI": {
        "cik": 1672688,
        "title": "Absci Corp"
    },
    "XTNT": {
        "cik": 1453593,
        "title": "Xtant Medical Holdings, Inc."
    },
    "HCMA": {
        "cik": 1845368,
        "title": "HCM Acquisition Corp"
    },
    "FEXD": {
        "cik": 1852407,
        "title": "Fintech Ecosystem Development Corp."
    },
    "HBB": {
        "cik": 1709164,
        "title": "Hamilton Beach Brands Holding Co"
    },
    "SATL": {
        "cik": 1874315,
        "title": "Satellogic Inc."
    },
    "MCN": {
        "cik": 1289868,
        "title": "Madison Covered Call & Equity Strategy Fund"
    },
    "AJX": {
        "cik": 1614806,
        "title": "Great Ajax Corp."
    },
    "TGVC": {
        "cik": 1865191,
        "title": "TG Venture Acquisition Corp."
    },
    "EGIO": {
        "cik": 1391127,
        "title": "Edgio, Inc."
    },
    "ELA": {
        "cik": 701719,
        "title": "Envela Corp"
    },
    "CIA": {
        "cik": 24090,
        "title": "CITIZENS, INC."
    },
    "LHC": {
        "cik": 1824153,
        "title": "Leo Holdings Corp. II"
    },
    "WMPN": {
        "cik": 1828376,
        "title": "William Penn Bancorporation"
    },
    "ISBA": {
        "cik": 842517,
        "title": "ISABELLA BANK Corp"
    },
    "BBBYQ": {
        "cik": 886158,
        "title": "BED BATH & BEYOND INC"
    },
    "MBAC": {
        "cik": 1839175,
        "title": "M3-Brigade Acquisition II Corp."
    },
    "SEEL": {
        "cik": 1017491,
        "title": "SEELOS THERAPEUTICS, INC."
    },
    "IDE": {
        "cik": 1417802,
        "title": "Voya Infrastructure, Industrials & Materials Fund"
    },
    "OPTN": {
        "cik": 1494650,
        "title": "OptiNose, Inc."
    },
    "ARC": {
        "cik": 1305168,
        "title": "ARC DOCUMENT SOLUTIONS, INC."
    },
    "BRBS": {
        "cik": 842717,
        "title": "BLUE RIDGE BANKSHARES, INC."
    },
    "XBIT": {
        "cik": 1626878,
        "title": "XBiotech Inc."
    },
    "NSTD": {
        "cik": 1835814,
        "title": "Northern Star Investment Corp. IV"
    },
    "GF": {
        "cik": 858706,
        "title": "NEW GERMANY FUND INC"
    },
    "CIK": {
        "cik": 810766,
        "title": "CREDIT SUISSE ASSET MANAGEMENT INCOME FUND INC"
    },
    "DLHC": {
        "cik": 785557,
        "title": "DLH Holdings Corp."
    },
    "BMN": {
        "cik": 1832871,
        "title": "BlackRock 2037 Municipal Target Term Trust"
    },
    "SMLP": {
        "cik": 1549922,
        "title": "Summit Midstream Partners, LP"
    },
    "BLZE": {
        "cik": 1462056,
        "title": "Backblaze, Inc."
    },
    "SOS": {
        "cik": 1346610,
        "title": "SOS Ltd"
    },
    "FPL": {
        "cik": 1589420,
        "title": "FIRST TRUST NEW OPPORTUNITIES MLP & ENERGY FUND"
    },
    "ALCY": {
        "cik": 1901336,
        "title": "Alchemy Investments Acquisition Corp 1"
    },
    "SYT": {
        "cik": 1946216,
        "title": "SYLA Technologies Co., Ltd."
    },
    "INGN": {
        "cik": 1294133,
        "title": "Inogen Inc"
    },
    "POET": {
        "cik": 1437424,
        "title": "POET TECHNOLOGIES INC."
    },
    "DBE": {
        "cik": 1383062,
        "title": "Invesco DB Energy Fund"
    },
    "OPBK": {
        "cik": 1722010,
        "title": "OP Bancorp"
    },
    "FLC": {
        "cik": 1245648,
        "title": "FLAHERTY & CRUMRINE TOTAL RETURN FUND INC"
    },
    "AADI": {
        "cik": 1422142,
        "title": "Aadi Bioscience, Inc."
    },
    "MIXT": {
        "cik": 1576914,
        "title": "MiX Telematics Ltd"
    },
    "GRTS": {
        "cik": 1656634,
        "title": "Gritstone bio, Inc."
    },
    "BGX": {
        "cik": 1504234,
        "title": "Blackstone Long-Short Credit Income Fund"
    },
    "NSTC": {
        "cik": 1835817,
        "title": "Northern Star Investment Corp. III"
    },
    "QRHC": {
        "cik": 1442236,
        "title": "Quest Resource Holding Corp"
    },
    "RCKY": {
        "cik": 895456,
        "title": "ROCKY BRANDS, INC."
    },
    "CTGO": {
        "cik": 1502377,
        "title": "Contango ORE, Inc."
    },
    "NHS": {
        "cik": 1487610,
        "title": "Neuberger Berman High Yield Strategies Fund Inc."
    },
    "MVO": {
        "cik": 1371782,
        "title": "MV Oil Trust"
    },
    "DNIF": {
        "cik": 1059213,
        "title": "DIVIDEND & INCOME FUND"
    },
    "MPA": {
        "cik": 891038,
        "title": "BLACKROCK MUNIYIELD PENNSYLVANIA QUALITY FUND"
    },
    "SACH": {
        "cik": 1682220,
        "title": "Sachem Capital Corp."
    },
    "MPV": {
        "cik": 831655,
        "title": "BARINGS PARTICIPATION INVESTORS"
    },
    "BHIL": {
        "cik": 1830210,
        "title": "Benson Hill, Inc."
    },
    "FTCO": {
        "cik": 1828377,
        "title": "Fortitude Gold Corp"
    },
    "IPX": {
        "cik": 1898601,
        "title": "IPERIONX Ltd"
    },
    "LTRX": {
        "cik": 1114925,
        "title": "LANTRONIX INC"
    },
    "NINE": {
        "cik": 1532286,
        "title": "Nine Energy Service, Inc."
    },
    "CDRO": {
        "cik": 1866782,
        "title": "Codere Online Luxembourg, S.A."
    },
    "KGEIF": {
        "cik": 1477081,
        "title": "Kolibri Global Energy Inc."
    },
    "VOC": {
        "cik": 1505413,
        "title": "VOC Energy Trust"
    },
    "OCEA": {
        "cik": 1869974,
        "title": "Ocean Biomedical, Inc."
    },
    "JYNT": {
        "cik": 1612630,
        "title": "JOINT Corp"
    },
    "CTXR": {
        "cik": 1506251,
        "title": "Citius Pharmaceuticals, Inc."
    },
    "HRTG": {
        "cik": 1598665,
        "title": "Heritage Insurance Holdings, Inc."
    },
    "INMB": {
        "cik": 1711754,
        "title": "Inmune Bio, Inc."
    },
    "FOA": {
        "cik": 1828937,
        "title": "Finance of America Companies Inc."
    },
    "TLGY": {
        "cik": 1879814,
        "title": "TLGY ACQUISITION CORP"
    },
    "LCA": {
        "cik": 1844642,
        "title": "Landcadia Holdings IV, Inc."
    },
    "GLDG": {
        "cik": 1538847,
        "title": "GoldMining Inc."
    },
    "ESPR": {
        "cik": 1434868,
        "title": "Esperion Therapeutics, Inc."
    },
    "MRSN": {
        "cik": 1442836,
        "title": "Mersana Therapeutics, Inc."
    },
    "ISSC": {
        "cik": 836690,
        "title": "INNOVATIVE SOLUTIONS & SUPPORT INC"
    },
    "ATRA": {
        "cik": 1604464,
        "title": "Atara Biotherapeutics, Inc."
    },
    "PLMI": {
        "cik": 1840317,
        "title": "Plum Acquisition Corp. I"
    },
    "OFS": {
        "cik": 1487918,
        "title": "OFS Capital Corp"
    },
    "BNR": {
        "cik": 1792267,
        "title": "Burning Rock Biotech Ltd"
    },
    "TLS": {
        "cik": 320121,
        "title": "TELOS CORP"
    },
    "OPRX": {
        "cik": 1448431,
        "title": "OptimizeRx Corp"
    },
    "OCFT": {
        "cik": 1780531,
        "title": "ONECONNECT FINANCIAL TECHNOLOGY CO., LTD."
    },
    "MOBV": {
        "cik": 1931691,
        "title": "Mobiv Acquisition Corp"
    },
    "WNEB": {
        "cik": 1157647,
        "title": "Western New England Bancorp, Inc."
    },
    "SHLT": {
        "cik": 1166834,
        "title": "SHL TELEMEDICINE LTD"
    },
    "SAMA": {
        "cik": 1843100,
        "title": "Schultze Special Purpose Acquisition Corp. II"
    },
    "HURC": {
        "cik": 315374,
        "title": "HURCO COMPANIES INC"
    },
    "ONCY": {
        "cik": 1129928,
        "title": "ONCOLYTICS BIOTECH INC"
    },
    "ZTEK": {
        "cik": 1904501,
        "title": "Zentek Ltd."
    },
    "CWGL": {
        "cik": 1562151,
        "title": "Crimson Wine Group, Ltd"
    },
    "FNRN": {
        "cik": 1114927,
        "title": "FIRST NORTHERN COMMUNITY BANCORP"
    },
    "PLX": {
        "cik": 1006281,
        "title": "Protalix BioTherapeutics, Inc."
    },
    "LBPH": {
        "cik": 1832168,
        "title": "Longboard Pharmaceuticals, Inc."
    },
    "NRO": {
        "cik": 1261166,
        "title": "NEUBERGER BERMAN REAL ESTATE SECURITIES INCOME FUND INC"
    },
    "PIAI": {
        "cik": 1819175,
        "title": "Prime Impact Acquisition I"
    },
    "NAK": {
        "cik": 1164771,
        "title": "NORTHERN DYNASTY MINERALS LTD"
    },
    "RMGC": {
        "cik": 1838108,
        "title": "RMG Acquisition Corp. III"
    },
    "EZGO": {
        "cik": 1806904,
        "title": "EZGO Technologies Ltd."
    },
    "LOOP": {
        "cik": 1504678,
        "title": "Loop Industries, Inc."
    },
    "STXS": {
        "cik": 1289340,
        "title": "Stereotaxis, Inc."
    },
    "RDCM": {
        "cik": 1016838,
        "title": "RADCOM LTD"
    },
    "MGRM": {
        "cik": 1769759,
        "title": "MONOGRAM ORTHOPAEDICS INC"
    },
    "BSET": {
        "cik": 10329,
        "title": "BASSETT FURNITURE INDUSTRIES INC"
    },
    "FSRX": {
        "cik": 1834336,
        "title": "Finserv Acquisition Corp. II"
    },
    "GAU": {
        "cik": 1377757,
        "title": "Galiano Gold Inc."
    },
    "MHF": {
        "cik": 830487,
        "title": "WESTERN ASSET MUNICIPAL HIGH INCOME FUND INC."
    },
    "FLFV": {
        "cik": 1912582,
        "title": "Feutune Light Acquisition Corp"
    },
    "NKTR": {
        "cik": 906709,
        "title": "NEKTAR THERAPEUTICS"
    },
    "IOAC": {
        "cik": 1854275,
        "title": "Innovative International Acquisition Corp."
    },
    "FRXB": {
        "cik": 1840161,
        "title": "Forest Road Acquisition Corp. II"
    },
    "RNLX": {
        "cik": 1811115,
        "title": "Renalytix plc"
    },
    "TWLV": {
        "cik": 1819498,
        "title": "Twelve Seas Investment Co. II"
    },
    "LWAY": {
        "cik": 814586,
        "title": "Lifeway Foods, Inc."
    },
    "AKTS": {
        "cik": 1584754,
        "title": "Akoustis Technologies, Inc."
    },
    "TRVI": {
        "cik": 1563880,
        "title": "Trevi Therapeutics, Inc."
    },
    "CLPT": {
        "cik": 1285550,
        "title": "ClearPoint Neuro, Inc."
    },
    "TMNA": {
        "cik": 1648365,
        "title": "AGRI-FINTECH HOLDINGS, INC."
    },
    "MOGO": {
        "cik": 1602842,
        "title": "Mogo Inc."
    },
    "NGS": {
        "cik": 1084991,
        "title": "NATURAL GAS SERVICES GROUP INC"
    },
    "FZT": {
        "cik": 1839824,
        "title": "FAST Acquisition Corp. II"
    },
    "HNVR": {
        "cik": 1828588,
        "title": "Hanover Bancorp, Inc. /NY"
    },
    "BWG": {
        "cik": 1504545,
        "title": "BrandywineGLOBAL-Global Income Opportunities Fund Inc"
    },
    "EVG": {
        "cik": 1287498,
        "title": "Eaton Vance Short Duration Diversified Income Fund"
    },
    "MRBK": {
        "cik": 1750735,
        "title": "Meridian Corp"
    },
    "SY": {
        "cik": 1758530,
        "title": "So-Young International Inc."
    },
    "BPT": {
        "cik": 850033,
        "title": "BP PRUDHOE BAY ROYALTY TRUST"
    },
    "NDLS": {
        "cik": 1275158,
        "title": "NOODLES & Co"
    },
    "PTRS": {
        "cik": 832090,
        "title": "PARTNERS BANCORP"
    },
    "EVLO": {
        "cik": 1694665,
        "title": "Evelo Biosciences, Inc."
    },
    "SGC": {
        "cik": 95574,
        "title": "SUPERIOR GROUP OF COMPANIES, INC."
    },
    "GRPH": {
        "cik": 1815776,
        "title": "Graphite Bio, Inc."
    },
    "DGWR": {
        "cik": 1637866,
        "title": "Deep Green Waste & Recycling, Inc."
    },
    "CNDB": {
        "cik": 1851961,
        "title": "Concord Acquisition Corp III"
    },
    "ORMP": {
        "cik": 1176309,
        "title": "ORAMED PHARMACEUTICALS INC."
    },
    "TUP": {
        "cik": 1008654,
        "title": "TUPPERWARE BRANDS CORP"
    },
    "RMBI": {
        "cik": 1767837,
        "title": "Richmond Mutual Bancorporation, Inc."
    },
    "FCCO": {
        "cik": 932781,
        "title": "FIRST COMMUNITY CORP /SC/"
    },
    "CSTA": {
        "cik": 1834032,
        "title": "Constellation Acquisition Corp I"
    },
    "FINW": {
        "cik": 1856365,
        "title": "Finwise Bancorp"
    },
    "RMMZ": {
        "cik": 1870833,
        "title": "RiverNorth Managed Duration Municipal Income Fund II, Inc."
    },
    "LGVC": {
        "cik": 1879297,
        "title": "LAMF Global Ventures Corp. I"
    },
    "PRDS": {
        "cik": 1822711,
        "title": "PARDES BIOSCIENCES, INC."
    },
    "SGA": {
        "cik": 886136,
        "title": "SAGA COMMUNICATIONS INC"
    },
    "UFI": {
        "cik": 100726,
        "title": "UNIFI INC"
    },
    "VATE": {
        "cik": 1006837,
        "title": "INNOVATE Corp."
    },
    "ISTR": {
        "cik": 1602658,
        "title": "Investar Holding Corp"
    },
    "CAAS": {
        "cik": 1157762,
        "title": "CHINA AUTOMOTIVE SYSTEMS INC"
    },
    "BDSX": {
        "cik": 1439725,
        "title": "BIODESIX INC"
    },
    "GFX": {
        "cik": 1823896,
        "title": "Golden Falcon Acquisition Corp."
    },
    "FREVS": {
        "cik": 36840,
        "title": "FIRST REAL ESTATE INVESTMENT TRUST OF NEW JERSEY"
    },
    "MUA": {
        "cik": 901243,
        "title": "BLACKROCK MUNIASSETS FUND, INC."
    },
    "IGA": {
        "cik": 1332943,
        "title": "Voya Global Advantage & Premium Opportunity Fund"
    },
    "FRAF": {
        "cik": 723646,
        "title": "FRANKLIN FINANCIAL SERVICES CORP /PA/"
    },
    "LGYV": {
        "cik": 1616788,
        "title": "LEGACY VENTURES INTERNATIONAL INC."
    },
    "HEQ": {
        "cik": 1496749,
        "title": "John Hancock Hedged Equity & Income Fund"
    },
    "MSD": {
        "cik": 904112,
        "title": "MORGAN STANLEY EMERGING MARKETS DEBT FUND INC"
    },
    "ZFOX": {
        "cik": 1823575,
        "title": "ZeroFox Holdings, Inc."
    },
    "ARMP": {
        "cik": 921114,
        "title": "Armata Pharmaceuticals, Inc."
    },
    "FXY": {
        "cik": 1353613,
        "title": "Invesco CurrencyShares Japanese Yen Trust"
    },
    "GMDA": {
        "cik": 1600847,
        "title": "Gamida Cell Ltd."
    },
    "WPRT": {
        "cik": 1370416,
        "title": "WESTPORT FUEL SYSTEMS INC."
    },
    "ABXXF": {
        "cik": 1971975,
        "title": "Abaxx Technologies Inc."
    },
    "WTMA": {
        "cik": 1866226,
        "title": "Welsbach Technology Metals Acquisition Corp."
    },
    "NSTG": {
        "cik": 1401708,
        "title": "NanoString Technologies Inc"
    },
    "TALS": {
        "cik": 1827506,
        "title": "Talaris Therapeutics, Inc."
    },
    "DHCA": {
        "cik": 1838163,
        "title": "DHC Acquisition Corp."
    },
    "SJ": {
        "cik": 1753673,
        "title": "Scienjoy Holding Corp"
    },
    "ARQQ": {
        "cik": 1859690,
        "title": "Arqit Quantum Inc."
    },
    "BIVI": {
        "cik": 1580149,
        "title": "BIOVIE INC."
    },
    "CUE": {
        "cik": 1645460,
        "title": "Cue Biopharma, Inc."
    },
    "TCS": {
        "cik": 1411688,
        "title": "Container Store Group, Inc."
    },
    "ACAQ": {
        "cik": 1869141,
        "title": "Athena Consumer Acquisition Corp."
    },
    "HNST": {
        "cik": 1530979,
        "title": "Honest Company, Inc."
    },
    "LFMD": {
        "cik": 948320,
        "title": "LifeMD, Inc."
    },
    "SPE": {
        "cik": 897802,
        "title": "SPECIAL OPPORTUNITIES FUND, INC."
    },
    "LITB": {
        "cik": 1523836,
        "title": "LightInTheBox Holding Co., Ltd."
    },
    "PRQR": {
        "cik": 1612940,
        "title": "ProQR Therapeutics N.V."
    },
    "FGBI": {
        "cik": 1408534,
        "title": "First Guaranty Bancshares, Inc."
    },
    "ATEK": {
        "cik": 1882198,
        "title": "Athena Technology Acquisition Corp. II"
    },
    "ESHA": {
        "cik": 1918661,
        "title": "ESH Acquisition Corp."
    },
    "LOMLF": {
        "cik": 1509397,
        "title": "Lion One Metals Ltd."
    },
    "ROOT": {
        "cik": 1788882,
        "title": "Root, Inc."
    },
    "FGEN": {
        "cik": 921299,
        "title": "FIBROGEN INC"
    },
    "BTA": {
        "cik": 1343793,
        "title": "BlackRock Long-Term Municipal Advantage Trust"
    },
    "ALT": {
        "cik": 1326190,
        "title": "Altimmune, Inc."
    },
    "SANG": {
        "cik": 1753368,
        "title": "Sangoma Technologies Corp"
    },
    "ULBI": {
        "cik": 875657,
        "title": "ULTRALIFE CORP"
    },
    "GLST": {
        "cik": 1922331,
        "title": "Global Star Acquisition Inc."
    },
    "DIT": {
        "cik": 928465,
        "title": "AMCON DISTRIBUTING CO"
    },
    "GNSS": {
        "cik": 924383,
        "title": "Genasys Inc."
    },
    "PHX": {
        "cik": 315131,
        "title": "PHX MINERALS INC."
    },
    "JUN": {
        "cik": 1838814,
        "title": "Juniper II Corp."
    },
    "BMAC": {
        "cik": 1848020,
        "title": "Black Mountain Acquisition Corp."
    },
    "TBCP": {
        "cik": 1815753,
        "title": "Thunder Bridge Capital Partners III Inc."
    },
    "CRGO": {
        "cik": 1927719,
        "title": "Freightos Ltd"
    },
    "MHGU": {
        "cik": 808219,
        "title": "MERITAGE HOSPITALITY GROUP INC"
    },
    "DMF": {
        "cik": 839122,
        "title": "BNY MELLON MUNICIPAL INCOME, INC."
    },
    "PLG": {
        "cik": 1095052,
        "title": "PLATINUM GROUP METALS LTD"
    },
    "GLSI": {
        "cik": 1799788,
        "title": "Greenwich LifeSciences, Inc."
    },
    "EPIX": {
        "cik": 1633932,
        "title": "ESSA Pharma Inc."
    },
    "GMFI": {
        "cik": 1866547,
        "title": "Aetherium Acquisition Corp"
    },
    "DBTX": {
        "cik": 1656536,
        "title": "Decibel Therapeutics, Inc."
    },
    "USAP": {
        "cik": 931584,
        "title": "UNIVERSAL STAINLESS & ALLOY PRODUCTS INC"
    },
    "MHH": {
        "cik": 1437226,
        "title": "Mastech Digital, Inc."
    },
    "GATE": {
        "cik": 1838513,
        "title": "Marblegate Acquisition Corp."
    },
    "NPCE": {
        "cik": 1528287,
        "title": "NeuroPace Inc"
    },
    "GDLC": {
        "cik": 1729997,
        "title": "Grayscale Digital Large Cap Fund LLC"
    },
    "RVSB": {
        "cik": 1041368,
        "title": "RIVERVIEW BANCORP INC"
    },
    "KOD": {
        "cik": 1468748,
        "title": "Kodiak Sciences Inc."
    },
    "BCAB": {
        "cik": 1826892,
        "title": "BioAtla, Inc."
    },
    "CFBK": {
        "cik": 1070680,
        "title": "CF BANKSHARES INC."
    },
    "PRTK": {
        "cik": 1178711,
        "title": "Paratek Pharmaceuticals, Inc."
    },
    "THRX": {
        "cik": 1745020,
        "title": "Theseus Pharmaceuticals, Inc."
    },
    "WEA": {
        "cik": 1163792,
        "title": "WESTERN ASSET PREMIER BOND FUND"
    },
    "AAIC": {
        "cik": 1209028,
        "title": "Arlington Asset Investment Corp."
    },
    "JHS": {
        "cik": 759866,
        "title": "JOHN HANCOCK INCOME SECURITIES TRUST"
    },
    "DTI": {
        "cik": 1884516,
        "title": "Drilling Tools International Corp"
    },
    "TSHA": {
        "cik": 1806310,
        "title": "Taysha Gene Therapies, Inc."
    },
    "PFD": {
        "cik": 868578,
        "title": "FLAHERTY & CRUMRINE PREFERRED & INCOME FUND INC"
    },
    "AOUT": {
        "cik": 1808997,
        "title": "American Outdoor Brands, Inc."
    },
    "FNWB": {
        "cik": 1556727,
        "title": "First Northwest Bancorp"
    },
    "MITT": {
        "cik": 1514281,
        "title": "AG Mortgage Investment Trust, Inc."
    },
    "UBFO": {
        "cik": 1137547,
        "title": "UNITED SECURITY BANCSHARES"
    },
    "GPAC": {
        "cik": 1831979,
        "title": "Global Partner Acquisition Corp II"
    },
    "PNRLF": {
        "cik": 795800,
        "title": "Premium Nickel Resources Ltd."
    },
    "CRT": {
        "cik": 881787,
        "title": "CROSS TIMBERS ROYALTY TRUST"
    },
    "ELVA": {
        "cik": 1844450,
        "title": "Electrovaya Inc."
    },
    "USGO": {
        "cik": 1947244,
        "title": "U.S. GoldMining Inc."
    },
    "EPSN": {
        "cik": 1726126,
        "title": "Epsilon Energy Ltd."
    },
    "EZOO": {
        "cik": 1752372,
        "title": "Ezagoo Ltd"
    },
    "KRMD": {
        "cik": 704440,
        "title": "KORU Medical Systems, Inc."
    },
    "OPA": {
        "cik": 1843121,
        "title": "Magnum Opus Acquisition Ltd"
    },
    "OGI": {
        "cik": 1620737,
        "title": "ORGANIGRAM HOLDINGS INC."
    },
    "BYTS": {
        "cik": 1842566,
        "title": "BYTE Acquisition Corp."
    },
    "MCAC": {
        "cik": 1895249,
        "title": "Monterey Capital Acquisition Corp"
    },
    "DMO": {
        "cik": 1478102,
        "title": "Western Asset Mortgage Opportunity Fund Inc."
    },
    "FIAC": {
        "cik": 1854480,
        "title": "Focus Impact Acquisition Corp."
    },
    "FTHM": {
        "cik": 1753162,
        "title": "Fathom Holdings Inc."
    },
    "NSTB": {
        "cik": 1834518,
        "title": "Northern Star Investment Corp. II"
    },
    "NPAB": {
        "cik": 1837929,
        "title": "New Providence Acquisition Corp. II"
    },
    "CRGE": {
        "cik": 1277250,
        "title": "Charge Enterprises, Inc."
    },
    "ARRW": {
        "cik": 1835972,
        "title": "Arrowroot Acquisition Corp."
    },
    "LL": {
        "cik": 1396033,
        "title": "LL Flooring Holdings, Inc."
    },
    "ACBM": {
        "cik": 1622996,
        "title": "ACRO BIOMEDICAL CO., LTD."
    },
    "COOL": {
        "cik": 1829953,
        "title": "Corner Growth Acquisition Corp."
    },
    "UEIC": {
        "cik": 101984,
        "title": "UNIVERSAL ELECTRONICS INC"
    },
    "YERBF": {
        "cik": 1978133,
        "title": "YERBAE BRANDS CORP."
    },
    "DSAQ": {
        "cik": 1871745,
        "title": "Direct Selling Acquisition Corp."
    },
    "TRCA": {
        "cik": 1840353,
        "title": "Twin Ridge Capital Acquisition Corp."
    },
    "WISH": {
        "cik": 1822250,
        "title": "ContextLogic Inc."
    },
    "ASYS": {
        "cik": 720500,
        "title": "AMTECH SYSTEMS INC"
    },
    "SRT": {
        "cik": 1031029,
        "title": "Startek, Inc."
    },
    "FAT": {
        "cik": 1705012,
        "title": "Fat Brands, Inc"
    },
    "FNCB": {
        "cik": 1035976,
        "title": "FNCB Bancorp, Inc."
    },
    "HWBK": {
        "cik": 893847,
        "title": "HAWTHORN BANCSHARES, INC."
    },
    "BYN": {
        "cik": 1852633,
        "title": "Banyan Acquisition Corp"
    },
    "VXRT": {
        "cik": 72444,
        "title": "Vaxart, Inc."
    },
    "FEAM": {
        "cik": 1888654,
        "title": "5E Advanced Materials, Inc."
    },
    "OVBC": {
        "cik": 894671,
        "title": "OHIO VALLEY BANC CORP"
    },
    "NAZ": {
        "cik": 892992,
        "title": "NUVEEN ARIZONA QUALITY MUNICIPAL INCOME FUND"
    },
    "FCUV": {
        "cik": 1590418,
        "title": "FOCUS UNIVERSAL INC."
    },
    "CTSO": {
        "cik": 1175151,
        "title": "Cytosorbents Corp"
    },
    "RBT": {
        "cik": 1862068,
        "title": "Rubicon Technologies, Inc."
    },
    "ECF": {
        "cik": 793040,
        "title": "ELLSWORTH GROWTH & INCOME FUND LTD"
    },
    "USCT": {
        "cik": 1860514,
        "title": "TKB Critical Technologies 1"
    },
    "ONYX": {
        "cik": 1849548,
        "title": "Onyx Acquisition Co. I"
    },
    "BEEM": {
        "cik": 1398805,
        "title": "Beam Global"
    },
    "FLXS": {
        "cik": 37472,
        "title": "FLEXSTEEL INDUSTRIES INC"
    },
    "APXI": {
        "cik": 1868573,
        "title": "APx Acquisition Corp. I"
    },
    "CDXC": {
        "cik": 1386570,
        "title": "ChromaDex Corp."
    },
    "BANX": {
        "cik": 1578987,
        "title": "ArrowMark Financial Corp."
    },
    "BTAI": {
        "cik": 1720893,
        "title": "BioXcel Therapeutics, Inc."
    },
    "PYR": {
        "cik": 1743344,
        "title": "PyroGenesis Canada Inc."
    },
    "NB": {
        "cik": 1512228,
        "title": "NIOCORP DEVELOPMENTS LTD"
    },
    "ATOS": {
        "cik": 1488039,
        "title": "ATOSSA THERAPEUTICS, INC."
    },
    "BRAG": {
        "cik": 1867834,
        "title": "Bragg Gaming Group Inc."
    },
    "WGS": {
        "cik": 1818331,
        "title": "GeneDx Holdings Corp."
    },
    "DECA": {
        "cik": 1913577,
        "title": "Denali Capital Acquisition Corp."
    },
    "GRRR": {
        "cik": 1903145,
        "title": "Gorilla Technology Group Inc."
    },
    "FMN": {
        "cik": 1199004,
        "title": "Federated Hermes Premier Municipal Income Fund"
    },
    "ADTH": {
        "cik": 1838672,
        "title": "AdTheorent Holding Company, Inc."
    },
    "RBOT": {
        "cik": 1812173,
        "title": "Vicarious Surgical Inc."
    },
    "VENG": {
        "cik": 1676580,
        "title": "VISION ENERGY Corp"
    },
    "CRKN": {
        "cik": 1761696,
        "title": "Crown Electrokinetics Corp."
    },
    "DCF": {
        "cik": 1627854,
        "title": "BNY Mellon Alcentra Global Credit Income 2024 Target Term Fund, Inc."
    },
    "CDXS": {
        "cik": 1200375,
        "title": "CODEXIS, INC."
    },
    "GROV": {
        "cik": 1841761,
        "title": "Grove Collaborative Holdings, Inc."
    },
    "ZJYL": {
        "cik": 1837821,
        "title": "Jin Medical International Ltd."
    },
    "HGBL": {
        "cik": 849145,
        "title": "Heritage Global Inc."
    },
    "INO": {
        "cik": 1055726,
        "title": "INOVIO PHARMACEUTICALS, INC."
    },
    "KLDI": {
        "cik": 1752474,
        "title": "KLDiscovery Inc."
    },
    "NTIC": {
        "cik": 875582,
        "title": "NORTHERN TECHNOLOGIES INTERNATIONAL CORP"
    },
    "BKKT": {
        "cik": 1820302,
        "title": "Bakkt Holdings, Inc."
    },
    "MNOV": {
        "cik": 1226616,
        "title": "MEDICINOVA INC"
    },
    "MYNA": {
        "cik": 1850453,
        "title": "Mynaric AG"
    },
    "VFL": {
        "cik": 895574,
        "title": "abrdn National Municipal Income Fund"
    },
    "CPTK": {
        "cik": 1827899,
        "title": "Crown PropTech Acquisitions"
    },
    "AHI": {
        "cik": 1815436,
        "title": "Advanced Health Intelligence Ltd"
    },
    "SZZL": {
        "cik": 1829322,
        "title": "Sizzle Acquisition Corp."
    },
    "ACAB": {
        "cik": 1893219,
        "title": "Atlantic Coastal Acquisition Corp. II"
    },
    "ATAK": {
        "cik": 1883788,
        "title": "Aurora Technology Acquisition Corp."
    },
    "DSGN": {
        "cik": 1807120,
        "title": "Design Therapeutics, Inc."
    },
    "CWBC": {
        "cik": 1051343,
        "title": "COMMUNITY WEST BANCSHARES /"
    },
    "FCAP": {
        "cik": 1070296,
        "title": "FIRST CAPITAL INC"
    },
    "MLEC": {
        "cik": 1937737,
        "title": "Moolec Science SA"
    },
    "ADER": {
        "cik": 1822912,
        "title": "26 Capital Acquisition Corp."
    },
    "OCGN": {
        "cik": 1372299,
        "title": "Ocugen, Inc."
    },
    "REEMF": {
        "cik": 1419806,
        "title": "RARE ELEMENT RESOURCES LTD"
    },
    "ANVS": {
        "cik": 1477845,
        "title": "Annovis Bio, Inc."
    },
    "PCF": {
        "cik": 810943,
        "title": "HIGH INCOME SECURITIES FUND"
    },
    "EMYB": {
        "cik": 1449794,
        "title": "Embassy Bancorp, Inc."
    },
    "VII": {
        "cik": 1826011,
        "title": "7GC & Co. Holdings Inc."
    },
    "IXAQ": {
        "cik": 1852019,
        "title": "IX Acquisition Corp."
    },
    "FFNW": {
        "cik": 1401564,
        "title": "First Financial Northwest, Inc."
    },
    "BODY": {
        "cik": 1826889,
        "title": "Beachbody Company, Inc."
    },
    "GLQ": {
        "cik": 1316463,
        "title": "Clough Global Equity Fund"
    },
    "BHAC": {
        "cik": 1851612,
        "title": "Crixus BH3 Acquisition Co"
    },
    "GEOS": {
        "cik": 1001115,
        "title": "GEOSPACE TECHNOLOGIES CORP"
    },
    "DFLI": {
        "cik": 1847986,
        "title": "Dragonfly Energy Holdings Corp."
    },
    "BSBK": {
        "cik": 1787414,
        "title": "Bogota Financial Corp."
    },
    "ADCT": {
        "cik": 1771910,
        "title": "ADC Therapeutics SA"
    },
    "SMID": {
        "cik": 924719,
        "title": "SMITH MIDLAND CORP"
    },
    "QFTA": {
        "cik": 1830795,
        "title": "Quantum FinTech Acquisition Corp"
    },
    "SCYX": {
        "cik": 1178253,
        "title": "SCYNEXIS INC"
    },
    "CHN": {
        "cik": 845379,
        "title": "CHINA FUND INC"
    },
    "ANIX": {
        "cik": 715446,
        "title": "Anixa Biosciences Inc"
    },
    "ENER": {
        "cik": 1855555,
        "title": "ACCRETION ACQUISITION CORP."
    },
    "PHD": {
        "cik": 1305767,
        "title": "Pioneer Floating Rate Fund, Inc."
    },
    "EML": {
        "cik": 31107,
        "title": "EASTERN CO"
    },
    "PEBK": {
        "cik": 1093672,
        "title": "PEOPLES BANCORP OF NORTH CAROLINA INC"
    },
    "XFIN": {
        "cik": 1852749,
        "title": "ExcelFin Acquisition Corp."
    },
    "BCTX": {
        "cik": 1610820,
        "title": "BriaCell Therapeutics Corp."
    },
    "PLNHF": {
        "cik": 1813452,
        "title": "Planet 13 Holdings Inc."
    },
    "SPRU": {
        "cik": 1772720,
        "title": "SPRUCE POWER HOLDING CORP"
    },
    "KACL": {
        "cik": 1865468,
        "title": "Kairous Acquisition Corp. Ltd"
    },
    "WWAC": {
        "cik": 1853044,
        "title": "Worldwide Webb Acquisition Corp."
    },
    "LNKB": {
        "cik": 1756701,
        "title": "LINKBANCORP, Inc."
    },
    "EFSI": {
        "cik": 880641,
        "title": "EAGLE FINANCIAL SERVICES INC"
    },
    "CATX": {
        "cik": 728387,
        "title": "Perspective Therapeutics, Inc."
    },
    "JHI": {
        "cik": 759828,
        "title": "JOHN HANCOCK INVESTORS TRUST"
    },
    "YGF": {
        "cik": 1875496,
        "title": "YanGuFang International Group Co., Ltd"
    },
    "DMAC": {
        "cik": 1401040,
        "title": "DiaMedica Therapeutics Inc."
    },
    "CBFV": {
        "cik": 1605301,
        "title": "CB Financial Services, Inc."
    },
    "ETON": {
        "cik": 1710340,
        "title": "Eton Pharmaceuticals, Inc."
    },
    "BATL": {
        "cik": 1282648,
        "title": "BATTALION OIL CORP"
    },
    "NIM": {
        "cik": 890119,
        "title": "NUVEEN SELECT MATURITIES MUNICIPAL FUND"
    },
    "BFIN": {
        "cik": 1303942,
        "title": "BankFinancial CORP"
    },
    "MNP": {
        "cik": 894351,
        "title": "WESTERN ASSET MUNICIPAL PARTNERS FUND INC."
    },
    "LTCH": {
        "cik": 1826000,
        "title": "Latch, Inc."
    },
    "FUNC": {
        "cik": 763907,
        "title": "FIRST UNITED CORP/MD/"
    },
    "PRSR": {
        "cik": 1825473,
        "title": "Prospector Capital Corp."
    },
    "SHAP": {
        "cik": 1881462,
        "title": "Spree Acquisition Corp. 1 Ltd"
    },
    "RGF": {
        "cik": 1871149,
        "title": "Real Good Food Company, Inc."
    },
    "TRX": {
        "cik": 1173643,
        "title": "TRX GOLD Corp"
    },
    "AREC": {
        "cik": 1590715,
        "title": "American Resources Corp"
    },
    "SOND": {
        "cik": 1819395,
        "title": "Sonder Holdings Inc."
    },
    "LFT": {
        "cik": 1547546,
        "title": "Lument Finance Trust, Inc."
    },
    "CPHC": {
        "cik": 1672909,
        "title": "Canterbury Park Holding Corp"
    },
    "ORN": {
        "cik": 1402829,
        "title": "Orion Group Holdings Inc"
    },
    "FONR": {
        "cik": 355019,
        "title": "FONAR CORP"
    },
    "PAI": {
        "cik": 75398,
        "title": "Western Asset Investment Grade Income Fund Inc."
    },
    "AAWH": {
        "cik": 1756390,
        "title": "Ascend Wellness Holdings, Inc."
    },
    "FOSL": {
        "cik": 883569,
        "title": "Fossil Group, Inc."
    },
    "BGSF": {
        "cik": 1474903,
        "title": "BGSF, INC."
    },
    "XNET": {
        "cik": 1510593,
        "title": "Xunlei Ltd"
    },
    "FXNC": {
        "cik": 719402,
        "title": "FIRST NATIONAL CORP /VA/"
    },
    "ECBK": {
        "cik": 1914605,
        "title": "ECB Bancorp, Inc. /MD/"
    },
    "GFOR": {
        "cik": 1845459,
        "title": "Graf Acquisition Corp. IV"
    },
    "AQMS": {
        "cik": 1621832,
        "title": "Aqua Metals, Inc."
    },
    "MRMD": {
        "cik": 1522767,
        "title": "MARIMED INC."
    },
    "PAYS": {
        "cik": 1496443,
        "title": "Paysign, Inc."
    },
    "BGXX": {
        "cik": 1886799,
        "title": "Bright Green Corp"
    },
    "ESAC": {
        "cik": 1865506,
        "title": "ESGEN Acquisition Corp"
    },
    "TWOA": {
        "cik": 1843988,
        "title": "two"
    },
    "FLAG": {
        "cik": 1855485,
        "title": "First Light Acquisition Group, Inc."
    },
    "NRT": {
        "cik": 72633,
        "title": "NORTH EUROPEAN OIL ROYALTY TRUST"
    },
    "CXE": {
        "cik": 845606,
        "title": "MFS HIGH INCOME MUNICIPAL TRUST"
    },
    "PCM": {
        "cik": 908187,
        "title": "PCM FUND, INC."
    },
    "ACU": {
        "cik": 2098,
        "title": "ACME UNITED CORP"
    },
    "BBXIA": {
        "cik": 1814974,
        "title": "BBX Capital, Inc."
    },
    "FSFG": {
        "cik": 1435508,
        "title": "First Savings Financial Group, Inc."
    },
    "TORO": {
        "cik": 1941131,
        "title": "TORO CORP."
    },
    "MPRA": {
        "cik": 1853436,
        "title": "Mercato Partners Acquisition Corp"
    },
    "GMGI": {
        "cik": 1437925,
        "title": "Golden Matrix Group, Inc."
    },
    "LAKE": {
        "cik": 798081,
        "title": "LAKELAND INDUSTRIES INC"
    },
    "KF": {
        "cik": 748691,
        "title": "KOREA FUND INC"
    },
    "DTOC": {
        "cik": 1839998,
        "title": "Digital Transformation Opportunities Corp."
    },
    "IPVF": {
        "cik": 1839610,
        "title": "InterPrivate III Financial Partners Inc."
    },
    "CMCA": {
        "cik": 1865248,
        "title": "Capitalworks Emerging Markets Acquisition Corp"
    },
    "WE": {
        "cik": 1813756,
        "title": "WeWork Inc."
    },
    "SBI": {
        "cik": 882300,
        "title": "WESTERN ASSET INTERMEDIATE MUNI FUND INC."
    },
    "VOXR": {
        "cik": 1907909,
        "title": "Vox Royalty Corp."
    },
    "TMKR": {
        "cik": 1821606,
        "title": "Priveterra Acquisition Corp. II"
    },
    "SLAC": {
        "cik": 1834755,
        "title": "Social Leverage Acquisition Corp I"
    },
    "LARK": {
        "cik": 1141688,
        "title": "LANDMARK BANCORP INC"
    },
    "CZWI": {
        "cik": 1367859,
        "title": "Citizens Community Bancorp Inc."
    },
    "SHIP": {
        "cik": 1448397,
        "title": "Seanergy Maritime Holdings Corp."
    },
    "SWZ": {
        "cik": 813623,
        "title": "SWISS HELVETIA FUND, INC."
    },
    "KNIT": {
        "cik": 1696195,
        "title": "KINETIC GROUP INC."
    },
    "ADIL": {
        "cik": 1513525,
        "title": "ADIAL PHARMACEUTICALS, INC."
    },
    "QUIK": {
        "cik": 882508,
        "title": "QUICKLOGIC Corp"
    },
    "GNTA": {
        "cik": 1838716,
        "title": "Genenta Science S.p.A."
    },
    "KVHI": {
        "cik": 1007587,
        "title": "KVH INDUSTRIES INC \\DE\\"
    },
    "BLUA": {
        "cik": 1831006,
        "title": "BlueRiver Acquisition Corp."
    },
    "PDRO": {
        "cik": 1627554,
        "title": "Pedro's List, Inc."
    },
    "ORRCF": {
        "cik": 1390352,
        "title": "OROCO RESOURCE CORP"
    },
    "GLYC": {
        "cik": 1253689,
        "title": "GLYCOMIMETICS INC"
    },
    "VERI": {
        "cik": 1615165,
        "title": "Veritone, Inc."
    },
    "ALOT": {
        "cik": 8146,
        "title": "AstroNova, Inc."
    },
    "BRID": {
        "cik": 14177,
        "title": "BRIDGFORD FOODS CORP"
    },
    "IAF": {
        "cik": 779336,
        "title": "ABRDN AUSTRALIA EQUITY FUND, INC."
    },
    "LIFE": {
        "cik": 1339970,
        "title": "aTYR PHARMA INC"
    },
    "FKYS": {
        "cik": 737875,
        "title": "FIRST KEYSTONE CORP"
    },
    "TZOO": {
        "cik": 1133311,
        "title": "TRAVELZOO"
    },
    "WHEN": {
        "cik": 943535,
        "title": "WORLD HEALTH ENERGY HOLDINGS, INC."
    },
    "BMBN": {
        "cik": 804563,
        "title": "BENCHMARK BANKSHARES INC"
    },
    "FRD": {
        "cik": 39092,
        "title": "FRIEDMAN INDUSTRIES INC"
    },
    "CRAWA": {
        "cik": 47307,
        "title": "CRAWFORD UNITED Corp"
    },
    "ACHV": {
        "cik": 949858,
        "title": "ACHIEVE LIFE SCIENCES, INC."
    },
    "MLGO": {
        "cik": 1800392,
        "title": "MicroAlgo Inc."
    },
    "ILLM": {
        "cik": 1861233,
        "title": "illumin Holdings Inc."
    },
    "LUXH": {
        "cik": 1893311,
        "title": "LUXURBAN HOTELS INC."
    },
    "THTX": {
        "cik": 1512717,
        "title": "Theratechnologies Inc."
    },
    "SPPP": {
        "cik": 1539190,
        "title": "SPROTT PHYSICAL PLATINUM & PALLADIUM TRUST"
    },
    "AXTI": {
        "cik": 1051627,
        "title": "AXT INC"
    },
    "EGGF": {
        "cik": 1843973,
        "title": "EG Acquisition Corp."
    },
    "CLLS": {
        "cik": 1627281,
        "title": "Cellectis S.A."
    },
    "CHAA": {
        "cik": 1838293,
        "title": "Catcha Investment Corp"
    },
    "CEN": {
        "cik": 1576340,
        "title": "CENTER COAST BROOKFIELD MLP & ENERGY INFRASTRUCTURE FUND"
    },
    "CRVS": {
        "cik": 1626971,
        "title": "Corvus Pharmaceuticals, Inc."
    },
    "PLBY": {
        "cik": 1803914,
        "title": "PLBY Group, Inc."
    },
    "PFSW": {
        "cik": 1095315,
        "title": "PFSWEB INC"
    },
    "JAQC": {
        "cik": 1817868,
        "title": "Jupiter Acquisition Corp"
    },
    "NCAC": {
        "cik": 1849475,
        "title": "Newcourt Acquisition Corp"
    },
    "GIA": {
        "cik": 1844505,
        "title": "GigCapital5, Inc."
    },
    "MGF": {
        "cik": 811922,
        "title": "MFS GOVERNMENT MARKETS INCOME TRUST"
    },
    "AUDA": {
        "cik": 1067837,
        "title": "AUDACY, INC."
    },
    "MITA": {
        "cik": 1847440,
        "title": "Coliseum Acquisition Corp."
    },
    "MMAT": {
        "cik": 1431959,
        "title": "META MATERIALS INC."
    },
    "EBMT": {
        "cik": 1478454,
        "title": "Eagle Bancorp Montana, Inc."
    },
    "AXDX": {
        "cik": 727207,
        "title": "Accelerate Diagnostics, Inc"
    },
    "GOSS": {
        "cik": 1728117,
        "title": "Gossamer Bio, Inc."
    },
    "TGLO": {
        "cik": 1066684,
        "title": "THEGLOBE COM INC"
    },
    "APEI": {
        "cik": 1201792,
        "title": "AMERICAN PUBLIC EDUCATION INC"
    },
    "VFF": {
        "cik": 1584549,
        "title": "Village Farms International, Inc."
    },
    "YCQH": {
        "cik": 1794276,
        "title": "YCQH Agricultural Technology Co. Ltd"
    },
    "CSBB": {
        "cik": 880417,
        "title": "CSB Bancorp, Inc."
    },
    "LVPA": {
        "cik": 831378,
        "title": "LVPAI GROUP Ltd"
    },
    "IZM": {
        "cik": 1854572,
        "title": "ICZOOM Group Inc."
    },
    "CSLM": {
        "cik": 1875493,
        "title": "CSLM ACQUISITION CORP."
    },
    "DLNG": {
        "cik": 1578453,
        "title": "Dynagas LNG Partners LP"
    },
    "GGZ": {
        "cik": 1585855,
        "title": "Gabelli Global Small & Mid Cap Value Trust"
    },
    "AQST": {
        "cik": 1398733,
        "title": "Aquestive Therapeutics, Inc."
    },
    "SMSI": {
        "cik": 948708,
        "title": "SMITH MICRO SOFTWARE, INC."
    },
    "BWAQ": {
        "cik": 1878074,
        "title": "Blue World Acquisition Corp"
    },
    "AHT": {
        "cik": 1232582,
        "title": "ASHFORD HOSPITALITY TRUST INC"
    },
    "ATHA": {
        "cik": 1620463,
        "title": "Athira Pharma, Inc."
    },
    "CCFN": {
        "cik": 731122,
        "title": "CCFNB BANCORP INC"
    },
    "BCV": {
        "cik": 9521,
        "title": "BANCROFT FUND LTD"
    },
    "BACA": {
        "cik": 1869673,
        "title": "Berenson Acquisition Corp. I"
    },
    "EVF": {
        "cik": 1070732,
        "title": "EATON VANCE SENIOR INCOME TRUST"
    },
    "DIST": {
        "cik": 1818605,
        "title": "Distoken Acquisition Corp"
    },
    "RMBL": {
        "cik": 1596961,
        "title": "RumbleOn, Inc."
    },
    "AACI": {
        "cik": 1844817,
        "title": "Armada Acquisition Corp. I"
    },
    "PFO": {
        "cik": 882071,
        "title": "Flaherty & Crumrine PREFERRED & INCOME OPPORTUNITY FUND INC"
    },
    "GDL": {
        "cik": 1378701,
        "title": "GDL FUND"
    },
    "HITI": {
        "cik": 1847409,
        "title": "High Tide Inc."
    },
    "TCRX": {
        "cik": 1783328,
        "title": "TScan Therapeutics, Inc."
    },
    "RMI": {
        "cik": 1746967,
        "title": "RiverNorth Opportunistic Municipal Income Fund, Inc."
    },
    "NOBH": {
        "cik": 72205,
        "title": "NOBILITY HOMES INC"
    },
    "KNTE": {
        "cik": 1797768,
        "title": "Kinnate Biopharma Inc."
    },
    "CTMX": {
        "cik": 1501989,
        "title": "CytomX Therapeutics, Inc."
    },
    "ADEX": {
        "cik": 1830029,
        "title": "Adit EdTech Acquisition Corp."
    },
    "SNCR": {
        "cik": 1131554,
        "title": "SYNCHRONOSS TECHNOLOGIES INC"
    },
    "IXHL": {
        "cik": 1873875,
        "title": "Incannex Healthcare Ltd"
    },
    "PWUP": {
        "cik": 1847345,
        "title": "PowerUp Acquisition Corp."
    },
    "SFBC": {
        "cik": 1541119,
        "title": "Sound Financial Bancorp, Inc."
    },
    "SRNEQ": {
        "cik": 850261,
        "title": "Sorrento Therapeutics, Inc."
    },
    "FNVT": {
        "cik": 1857855,
        "title": "Finnovate Acquisition Corp."
    },
    "CHMI": {
        "cik": 1571776,
        "title": "Cherry Hill Mortgage Investment Corp"
    },
    "VCXA": {
        "cik": 1848898,
        "title": "10X Capital Venture Acquisition Corp. II"
    },
    "MMLP": {
        "cik": 1176334,
        "title": "MARTIN MIDSTREAM PARTNERS L.P."
    },
    "MDWT": {
        "cik": 355379,
        "title": "MIDWEST HOLDING INC."
    },
    "SUP": {
        "cik": 95552,
        "title": "SUPERIOR INDUSTRIES INTERNATIONAL INC"
    },
    "WHG": {
        "cik": 1165002,
        "title": "WESTWOOD HOLDINGS GROUP INC"
    },
    "FNWD": {
        "cik": 919864,
        "title": "Finward Bancorp"
    },
    "ASFH": {
        "cik": 1828748,
        "title": "ASIAFIN HOLDINGS CORP."
    },
    "TRLM": {
        "cik": 855787,
        "title": "TRULEUM, INC."
    },
    "TBNK": {
        "cik": 1447051,
        "title": "Territorial Bancorp Inc."
    },
    "GAMC": {
        "cik": 1841125,
        "title": "Golden Arrow Merger Corp."
    },
    "PROV": {
        "cik": 1010470,
        "title": "PROVIDENT FINANCIAL HOLDINGS INC"
    },
    "PFIE": {
        "cik": 1289636,
        "title": "PROFIRE ENERGY INC"
    },
    "UCL": {
        "cik": 1775898,
        "title": "uCloudlink Group Inc."
    },
    "MDXH": {
        "cik": 1872529,
        "title": "MDxHealth SA"
    },
    "MIST": {
        "cik": 1408443,
        "title": "Milestone Pharmaceuticals Inc."
    },
    "CONN": {
        "cik": 1223389,
        "title": "CONNS INC"
    },
    "SBFG": {
        "cik": 767405,
        "title": "SB FINANCIAL GROUP, INC."
    },
    "MNTX": {
        "cik": 1302028,
        "title": "Manitex International, Inc."
    },
    "CYT": {
        "cik": 1662244,
        "title": "Cyteir Therapeutics, Inc."
    },
    "MARX": {
        "cik": 1892922,
        "title": "Mars Acquisition Corp."
    },
    "VNRX": {
        "cik": 93314,
        "title": "VOLITIONRX LTD"
    },
    "STIX": {
        "cik": 1896049,
        "title": "Semantix, Inc."
    },
    "STTK": {
        "cik": 1680367,
        "title": "Shattuck Labs, Inc."
    },
    "HSPO": {
        "cik": 1946021,
        "title": "Horizon Space Acquisition I Corp."
    },
    "JDVB": {
        "cik": 866643,
        "title": "JD BANCSHARES INC"
    },
    "CNGL": {
        "cik": 1867443,
        "title": "Canna-Global Acquisition Corp"
    },
    "ATMV": {
        "cik": 1937891,
        "title": "AlphaVest Acquisition Corp."
    },
    "GALT": {
        "cik": 1133416,
        "title": "GALECTIN THERAPEUTICS INC"
    },
    "HRBR": {
        "cik": 899394,
        "title": "HARBOR DIVERSIFIED, INC."
    },
    "AFBI": {
        "cik": 1823406,
        "title": "Affinity Bancshares, Inc."
    },
    "BRAC": {
        "cik": 1865120,
        "title": "Broad Capital Acquisition Corp"
    },
    "UTGN": {
        "cik": 832480,
        "title": "UTG INC"
    },
    "NPFC": {
        "cik": 1445831,
        "title": "Newpoint Financial Corp"
    },
    "MAYS": {
        "cik": 54187,
        "title": "MAYS J W INC"
    },
    "LATG": {
        "cik": 1868269,
        "title": "LatAmGrowth SPAC"
    },
    "BFGX": {
        "cik": 1741257,
        "title": "BANGFU TECHNOLOGY GROUP CO., LTD."
    },
    "WRAC": {
        "cik": 1855168,
        "title": "Williams Rowland Acquisition Corp."
    },
    "STG": {
        "cik": 1723935,
        "title": "Sunlands Technology Group"
    },
    "MSSA": {
        "cik": 1882464,
        "title": "Metal Sky Star Acquisition Corp"
    },
    "RFM": {
        "cik": 1790177,
        "title": "RiverNorth Flexible Municipal Income Fund, Inc."
    },
    "NNBR": {
        "cik": 918541,
        "title": "NN INC"
    },
    "OPOF": {
        "cik": 740971,
        "title": "OLD POINT FINANCIAL CORP"
    },
    "NMI": {
        "cik": 830271,
        "title": "NUVEEN MUNICIPAL INCOME FUND INC"
    },
    "ARIZ": {
        "cik": 1882078,
        "title": "Arisz Acquisition Corp."
    },
    "UNB": {
        "cik": 706863,
        "title": "UNION BANKSHARES INC"
    },
    "VERU": {
        "cik": 863894,
        "title": "VERU INC."
    },
    "NBST": {
        "cik": 1831978,
        "title": "Newbury Street Acquisition Corp"
    },
    "ATMC": {
        "cik": 1889106,
        "title": "ALPHATIME ACQUISITION CORP"
    },
    "CMCT": {
        "cik": 908311,
        "title": "Creative Media & Community Trust Corp"
    },
    "SLNG": {
        "cik": 1043186,
        "title": "Stabilis Solutions, Inc."
    },
    "IVAC": {
        "cik": 1001902,
        "title": "INTEVAC INC"
    },
    "CGEN": {
        "cik": 1119774,
        "title": "COMPUGEN LTD"
    },
    "IMAQ": {
        "cik": 1846235,
        "title": "International Media Acquisition Corp."
    },
    "GTHX": {
        "cik": 1560241,
        "title": "G1 Therapeutics, Inc."
    },
    "RWOD": {
        "cik": 1907223,
        "title": "Redwoods Acquisition Corp."
    },
    "BLAC": {
        "cik": 1840425,
        "title": "Bellevue Life Sciences Acquisition Corp."
    },
    "QDRO": {
        "cik": 1825962,
        "title": "Quadro Acquisition One Corp."
    },
    "GLT": {
        "cik": 41719,
        "title": "Glatfelter Corp"
    },
    "NMT": {
        "cik": 897419,
        "title": "NUVEEN MASSACHUSETTS QUALITY MUNICIPAL INCOME FUND"
    },
    "PRPH": {
        "cik": 868278,
        "title": "ProPhase Labs, Inc."
    },
    "AEON": {
        "cik": 1837607,
        "title": "AEON Biopharma, Inc."
    },
    "RVPH": {
        "cik": 1742927,
        "title": "REVIVA PHARMACEUTICALS HOLDINGS, INC."
    },
    "FFMGF": {
        "cik": 1641229,
        "title": "First Mining Gold Corp."
    },
    "LIVE": {
        "cik": 1045742,
        "title": "LIVE VENTURES Inc"
    },
    "INAQ": {
        "cik": 1862463,
        "title": "Insight Acquisition Corp. /DE"
    },
    "SPIR": {
        "cik": 1816017,
        "title": "Spire Global, Inc."
    },
    "EAC": {
        "cik": 1832765,
        "title": "Edify Acquisition Corp."
    },
    "CELL": {
        "cik": 1689657,
        "title": "PhenomeX Inc."
    },
    "OCCI": {
        "cik": 1716951,
        "title": "OFS Credit Company, Inc."
    },
    "TBMC": {
        "cik": 1934945,
        "title": "Trailblazer Merger Corp I"
    },
    "CMTV": {
        "cik": 718413,
        "title": "COMMUNITY BANCORP /VT"
    },
    "KZR": {
        "cik": 1645666,
        "title": "Kezar Life Sciences, Inc."
    },
    "MDV": {
        "cik": 1645873,
        "title": "Modiv Industrial, Inc."
    },
    "SSSS": {
        "cik": 1509470,
        "title": "SURO CAPITAL CORP."
    },
    "FGMC": {
        "cik": 1906133,
        "title": "FG Merger Corp."
    },
    "ADTX": {
        "cik": 1726711,
        "title": "Aditxt, Inc."
    },
    "CGO": {
        "cik": 1285650,
        "title": "CALAMOS GLOBAL TOTAL RETURN FUND"
    },
    "IHD": {
        "cik": 1496292,
        "title": "Voya Emerging Markets High Dividend Equity Fund"
    },
    "GODN": {
        "cik": 1895144,
        "title": "Golden Star Acquisition Corp"
    },
    "AREN": {
        "cik": 894871,
        "title": "Arena Group Holdings, Inc."
    },
    "RLMD": {
        "cik": 1553643,
        "title": "RELMADA THERAPEUTICS, INC."
    },
    "ACNT": {
        "cik": 95953,
        "title": "ASCENT INDUSTRIES CO."
    },
    "ORTX": {
        "cik": 1748907,
        "title": "Orchard Therapeutics plc"
    },
    "CSBR": {
        "cik": 771856,
        "title": "CHAMPIONS ONCOLOGY, INC."
    },
    "FRLA": {
        "cik": 1849294,
        "title": "Fortune Rise Acquisition Corp"
    },
    "CMU": {
        "cik": 809844,
        "title": "MFS HIGH YIELD MUNICIPAL TRUST"
    },
    "PSBQ": {
        "cik": 948368,
        "title": "PSB HOLDINGS INC /WI/"
    },
    "ERH": {
        "cik": 1279014,
        "title": "ALLSPRING UTILITIES & HIGH INCOME FUND"
    },
    "OHAA": {
        "cik": 1870778,
        "title": "Opy Acquisition Corp. I"
    },
    "DRRX": {
        "cik": 1082038,
        "title": "DURECT CORP"
    },
    "PRE": {
        "cik": 1876431,
        "title": "Prenetics Global Ltd"
    },
    "NXG": {
        "cik": 1506488,
        "title": "NXG NextGen Infrastructure Income Fund"
    },
    "NRAC": {
        "cik": 1831964,
        "title": "NORTHERN REVIVAL ACQUISITION Corp"
    },
    "RENT": {
        "cik": 1468327,
        "title": "Rent the Runway, Inc."
    },
    "GSIT": {
        "cik": 1126741,
        "title": "GSI TECHNOLOGY INC"
    },
    "OSI": {
        "cik": 1832136,
        "title": "Osiris Acquisition Corp."
    },
    "KITT": {
        "cik": 1849820,
        "title": "Nauticus Robotics, Inc."
    },
    "EARN": {
        "cik": 1560672,
        "title": "Ellington Residential Mortgage REIT"
    },
    "KSM": {
        "cik": 846596,
        "title": "DWS STRATEGIC MUNICIPAL INCOME TRUST"
    },
    "SPRB": {
        "cik": 1683553,
        "title": "SPRUCE BIOSCIENCES, INC."
    },
    "KLR": {
        "cik": 1719489,
        "title": "Kaleyra, Inc."
    },
    "NKTX": {
        "cik": 1787400,
        "title": "Nkarta, Inc."
    },
    "BITE": {
        "cik": 1831270,
        "title": "Bite Acquisition Corp."
    },
    "HUDA": {
        "cik": 1853047,
        "title": "Hudson Acquisition I Corp."
    },
    "SOLO": {
        "cik": 1637736,
        "title": "ELECTRAMECCANICA VEHICLES CORP."
    },
    "GP": {
        "cik": 1584547,
        "title": "GREENPOWER MOTOR Co INC."
    },
    "DISA": {
        "cik": 1838831,
        "title": "Disruptive Acquisition Corp I"
    },
    "STRT": {
        "cik": 933034,
        "title": "STRATTEC SECURITY CORP"
    },
    "SRV": {
        "cik": 1400897,
        "title": "NXG Cushing Midstream Energy Fund"
    },
    "ALTU": {
        "cik": 1822366,
        "title": "Altitude Acquisition Corp."
    },
    "AE": {
        "cik": 2178,
        "title": "ADAMS RESOURCES & ENERGY, INC."
    },
    "PICC": {
        "cik": 1835800,
        "title": "Pivotal Investment Corp III"
    },
    "GNT": {
        "cik": 1438893,
        "title": "GAMCO Natural Resources, Gold & Income Trust"
    },
    "NYMXF": {
        "cik": 1018735,
        "title": "NYMOX PHARMACEUTICAL CORP"
    },
    "RAD": {
        "cik": 84129,
        "title": "RITE AID CORP"
    },
    "QNBC": {
        "cik": 750558,
        "title": "QNB CORP"
    },
    "SRL": {
        "cik": 16859,
        "title": "Scully Royalty Ltd."
    },
    "HOWL": {
        "cik": 1785530,
        "title": "Werewolf Therapeutics, Inc."
    },
    "ASPS": {
        "cik": 1462418,
        "title": "ALTISOURCE PORTFOLIO SOLUTIONS S.A."
    },
    "JLS": {
        "cik": 1472215,
        "title": "Nuveen Mortgage & Income Fund/MA/"
    },
    "CLNN": {
        "cik": 1822791,
        "title": "Clene Inc."
    },
    "AWCA": {
        "cik": 1021917,
        "title": "Awaysis Capital, Inc."
    },
    "APAC": {
        "cik": 1844981,
        "title": "StoneBridge Acquisition Corp."
    },
    "HFUS": {
        "cik": 1482554,
        "title": "Hartford Great Health Corp."
    },
    "ELTP": {
        "cik": 1053369,
        "title": "ELITE PHARMACEUTICALS INC /NV/"
    },
    "CMRX": {
        "cik": 1117480,
        "title": "CHIMERIX INC"
    },
    "CENN": {
        "cik": 1707919,
        "title": "CENNTRO ELECTRIC GROUP Ltd"
    },
    "WMLLF": {
        "cik": 1077640,
        "title": "Wealth Minerals Ltd."
    },
    "XAIR": {
        "cik": 1641631,
        "title": "Beyond Air, Inc."
    },
    "IMNM": {
        "cik": 1472012,
        "title": "Immunome Inc."
    },
    "ELTX": {
        "cik": 1601485,
        "title": "Elicio Therapeutics, Inc."
    },
    "CFFE": {
        "cik": 1839530,
        "title": "CF Acquisition Corp. VIII"
    },
    "KULR": {
        "cik": 1662684,
        "title": "KULR Technology Group, Inc."
    },
    "PCCT": {
        "cik": 1844149,
        "title": "Perception Capital Corp. II"
    },
    "SRFM": {
        "cik": 1936224,
        "title": "SURF AIR MOBILITY INC."
    },
    "NOTV": {
        "cik": 720154,
        "title": "Inotiv, Inc."
    },
    "GLLI": {
        "cik": 1888734,
        "title": "GLOBALINK INVESTMENT INC."
    },
    "HMNF": {
        "cik": 921183,
        "title": "HMN FINANCIAL INC"
    },
    "CPTN": {
        "cik": 1498233,
        "title": "Cepton, Inc."
    },
    "PYXS": {
        "cik": 1782223,
        "title": "Pyxis Oncology, Inc."
    },
    "NEOV": {
        "cik": 1748137,
        "title": "NeoVolta Inc."
    },
    "IRAA": {
        "cik": 1831874,
        "title": "Iris Acquisition Corp"
    },
    "AXR": {
        "cik": 6207,
        "title": "AMREP CORP."
    },
    "PVL": {
        "cik": 1520048,
        "title": "Permianville Royalty Trust"
    },
    "VGI": {
        "cik": 1528811,
        "title": "Virtus Global Multi-Sector Income Fund"
    },
    "MDWD": {
        "cik": 1593984,
        "title": "MediWound Ltd."
    },
    "SIEB": {
        "cik": 65596,
        "title": "SIEBERT FINANCIAL CORP"
    },
    "CSLR": {
        "cik": 1838987,
        "title": "Complete Solaria, Inc."
    },
    "DKDCA": {
        "cik": 1849380,
        "title": "Data Knights Acquisition Corp."
    },
    "ABEO": {
        "cik": 318306,
        "title": "ABEONA THERAPEUTICS INC."
    },
    "HNW": {
        "cik": 1388126,
        "title": "Pioneer Diversified High Income Fund, Inc."
    },
    "UNG": {
        "cik": 1376227,
        "title": "United States Natural Gas Fund, LP"
    },
    "ZHYBF": {
        "cik": 1672886,
        "title": "Zhong Yuan Bio-Technology Holdings Ltd"
    },
    "TPZ": {
        "cik": 1408201,
        "title": "TORTOISE POWER & ENERGY INFRASTRUCTURE FUND INC"
    },
    "ARYD": {
        "cik": 1838821,
        "title": "ARYA Sciences Acquisition Corp IV"
    },
    "AZ": {
        "cik": 1866030,
        "title": "A2Z Smart Technologies Corp"
    },
    "CODA": {
        "cik": 1334325,
        "title": "Coda Octopus Group, Inc."
    },
    "PRCH": {
        "cik": 1784535,
        "title": "Porch Group, Inc."
    },
    "KRON": {
        "cik": 1741830,
        "title": "Kronos Bio, Inc."
    },
    "TMTC": {
        "cik": 1879851,
        "title": "TMT Acquisition Corp."
    },
    "AAGH": {
        "cik": 1098009,
        "title": "America Great Health"
    },
    "LVLU": {
        "cik": 1780201,
        "title": "Lulu's Fashion Lounge Holdings, Inc."
    },
    "ALLT": {
        "cik": 1365767,
        "title": "Allot Ltd."
    },
    "LEAT": {
        "cik": 1456189,
        "title": "Leatt Corp"
    },
    "GLU": {
        "cik": 1282957,
        "title": "GABELLI GLOBAL UTILITY & INCOME TRUST"
    },
    "PSNL": {
        "cik": 1527753,
        "title": "Personalis, Inc."
    },
    "LZGI": {
        "cik": 1126115,
        "title": "LZG INTERNATIONAL, INC."
    },
    "IVCP": {
        "cik": 1845123,
        "title": "Swiftmerge Acquisition Corp."
    },
    "CASA": {
        "cik": 1333835,
        "title": "Casa Systems Inc"
    },
    "USAS": {
        "cik": 1286973,
        "title": "Americas Gold & Silver Corp"
    },
    "SGII": {
        "cik": 1869824,
        "title": "Seaport Global Acquisition II Corp."
    },
    "ERDCF": {
        "cik": 1398972,
        "title": "Erdene Resource Development Corp"
    },
    "ACET": {
        "cik": 1720580,
        "title": "Adicet Bio, Inc."
    },
    "OCUP": {
        "cik": 1228627,
        "title": "Ocuphire Pharma, Inc."
    },
    "PPHP": {
        "cik": 1863460,
        "title": "PHP Ventures Acquisition Corp."
    },
    "SYRS": {
        "cik": 1556263,
        "title": "Syros Pharmaceuticals, Inc."
    },
    "SND": {
        "cik": 1529628,
        "title": "Smart Sand, Inc."
    },
    "PHCI": {
        "cik": 1620749,
        "title": "Panamera Holdings Corp"
    },
    "PED": {
        "cik": 1141197,
        "title": "PEDEVCO CORP"
    },
    "GEVI": {
        "cik": 894556,
        "title": "General Enterprise Ventures, Inc."
    },
    "BNTC": {
        "cik": 1808898,
        "title": "Benitec Biopharma Inc."
    },
    "PET": {
        "cik": 1842356,
        "title": "Wag! Group Co."
    },
    "DUO": {
        "cik": 1750593,
        "title": "Fangdd Network Group Ltd."
    },
    "PFX": {
        "cik": 1490349,
        "title": "PhenixFIN Corp"
    },
    "TRLEF": {
        "cik": 1648636,
        "title": "Trillion Energy International Inc."
    },
    "ITHUF": {
        "cik": 1643154,
        "title": "iANTHUS CAPITAL HOLDINGS, INC."
    },
    "ATAQ": {
        "cik": 1841004,
        "title": "Altimar Acquisition Corp. III"
    },
    "AOGO": {
        "cik": 1881741,
        "title": "Arogo Capital Acquisition Corp."
    },
    "CRDF": {
        "cik": 1213037,
        "title": "Cardiff Oncology, Inc."
    },
    "CRKR": {
        "cik": 1162896,
        "title": "Prairie Operating Co."
    },
    "INTS": {
        "cik": 1567264,
        "title": "INTENSITY THERAPEUTICS, INC."
    },
    "LPTV": {
        "cik": 1643988,
        "title": "Loop Media, Inc."
    },
    "OCAX": {
        "cik": 1820175,
        "title": "OCA Acquisition Corp."
    },
    "NXC": {
        "cik": 885732,
        "title": "NUVEEN CALIFORNIA SELECT TAX FREE INCOME PORTFOLIO"
    },
    "BLRX": {
        "cik": 1498403,
        "title": "BioLineRx Ltd."
    },
    "GTH": {
        "cik": 1782594,
        "title": "Genetron Holdings Ltd"
    },
    "FORA": {
        "cik": 1829280,
        "title": "Forian Inc."
    },
    "DUET": {
        "cik": 1890671,
        "title": "DUET Acquisition Corp."
    },
    "LUDG": {
        "cik": 1960262,
        "title": "LUDWIG ENTERPRISES, INC."
    },
    "SFDL": {
        "cik": 818677,
        "title": "SECURITY FEDERAL CORP"
    },
    "ISDR": {
        "cik": 843006,
        "title": "ISSUER DIRECT CORP"
    },
    "GDST": {
        "cik": 1858007,
        "title": "Goldenstone Acquisition Ltd."
    },
    "FICV": {
        "cik": 1855693,
        "title": "Frontier Investment Corp"
    },
    "PNI": {
        "cik": 1170311,
        "title": "PIMCO NEW YORK MUNICIPAL INCOME FUND II"
    },
    "UPLD": {
        "cik": 1505155,
        "title": "Upland Software, Inc."
    },
    "KANP": {
        "cik": 1230058,
        "title": "KAANAPALI LAND LLC"
    },
    "JUSHF": {
        "cik": 1909747,
        "title": "Jushi Holdings Inc."
    },
    "GSVRF": {
        "cik": 865400,
        "title": "GUANAJUATO SILVER CO LTD"
    },
    "ENZ": {
        "cik": 316253,
        "title": "ENZO BIOCHEM INC"
    },
    "PBHC": {
        "cik": 1609065,
        "title": "Pathfinder Bancorp, Inc."
    },
    "HNRA": {
        "cik": 1842556,
        "title": "HNR Acquisition Corp."
    },
    "BWEN": {
        "cik": 1120370,
        "title": "BROADWIND, INC."
    },
    "VERY": {
        "cik": 1575434,
        "title": "Vericity, Inc."
    },
    "CMLS": {
        "cik": 1058623,
        "title": "CUMULUS MEDIA INC"
    },
    "ANEB": {
        "cik": 1815974,
        "title": "Anebulo Pharmaceuticals, Inc."
    },
    "DAVE": {
        "cik": 1841408,
        "title": "Dave Inc./DE"
    },
    "SMX": {
        "cik": 1940674,
        "title": "SMX (Security Matters) Public Ltd Co"
    },
    "APLT": {
        "cik": 1697532,
        "title": "Applied Therapeutics Inc."
    },
    "STCB": {
        "cik": 1539850,
        "title": "Starco Brands, Inc."
    },
    "AUBN": {
        "cik": 750574,
        "title": "AUBURN NATIONAL BANCORPORATION, INC"
    },
    "MLSS": {
        "cik": 855683,
        "title": "MILESTONE SCIENTIFIC INC."
    },
    "CPTP": {
        "cik": 202947,
        "title": "CAPITAL PROPERTIES INC /RI/"
    },
    "ELMD": {
        "cik": 1488917,
        "title": "Electromed, Inc."
    },
    "PLTN": {
        "cik": 1929231,
        "title": "Plutonian Acquisition Corp."
    },
    "YS": {
        "cik": 1946399,
        "title": "YS Biopharma Co., Ltd."
    },
    "CULL": {
        "cik": 1845799,
        "title": "Cullman Bancorp, Inc. /MD/"
    },
    "SCX": {
        "cik": 93676,
        "title": "STARRETT L S CO"
    },
    "SNAX": {
        "cik": 1691936,
        "title": "STRYVE FOODS, INC."
    },
    "WFCF": {
        "cik": 1360565,
        "title": "Where Food Comes From, Inc."
    },
    "PRT": {
        "cik": 1724009,
        "title": "PermRock Royalty Trust"
    },
    "GCV": {
        "cik": 845611,
        "title": "GABELLI CONVERTIBLE & INCOME SECURITIES FUND INC"
    },
    "HAIA": {
        "cik": 1848861,
        "title": "Healthcare AI Acquisition Corp."
    },
    "CBAT": {
        "cik": 1117171,
        "title": "CBAK Energy Technology, Inc."
    },
    "LIBY": {
        "cik": 1880151,
        "title": "Liberty Resources Acquisition Corp."
    },
    "SCTH": {
        "cik": 1703157,
        "title": "Securetech Innovations, Inc."
    },
    "FCO": {
        "cik": 876717,
        "title": "ABRDN GLOBAL INCOME FUND, INC."
    },
    "PGP": {
        "cik": 1318025,
        "title": "PIMCO Global StocksPLUS & Income Fund"
    },
    "ASM": {
        "cik": 316888,
        "title": "AVINO SILVER & GOLD MINES LTD"
    },
    "CETU": {
        "cik": 1936702,
        "title": "Cetus Capital Acquisition Corp."
    },
    "OAKU": {
        "cik": 1945422,
        "title": "Oak Woods Acquisition Corp"
    },
    "LUNR": {
        "cik": 1844452,
        "title": "Intuitive Machines, Inc."
    },
    "GLG": {
        "cik": 1556266,
        "title": "TD Holdings, Inc."
    },
    "CDTX": {
        "cik": 1610618,
        "title": "Cidara Therapeutics, Inc."
    },
    "SOHO": {
        "cik": 1301236,
        "title": "Sotherly Hotels Inc."
    },
    "ALOR": {
        "cik": 1883962,
        "title": "ALSP Orchid Acquisition Corp I"
    },
    "PCTI": {
        "cik": 1057083,
        "title": "PC TEL INC"
    },
    "SWSS": {
        "cik": 1838000,
        "title": "Clean Energy Special Situations Corp."
    },
    "YOTA": {
        "cik": 1907730,
        "title": "Yotta Acquisition Corp"
    },
    "VHAQ": {
        "cik": 1823857,
        "title": "Viveon Health Acquisition Corp."
    },
    "RFAC": {
        "cik": 1847607,
        "title": "RF Acquisition Corp."
    },
    "OMEX": {
        "cik": 798528,
        "title": "ODYSSEY MARINE EXPLORATION INC"
    },
    "HPLT": {
        "cik": 1863181,
        "title": "Home Plate Acquisition Corp"
    },
    "EDF": {
        "cik": 1501103,
        "title": "Virtus Stone Harbor Emerging Markets Income Fund"
    },
    "INTG": {
        "cik": 69422,
        "title": "INTERGROUP CORP"
    },
    "TAYD": {
        "cik": 96536,
        "title": "TAYLOR DEVICES INC"
    },
    "DTF": {
        "cik": 879535,
        "title": "DTF TAX-FREE INCOME 2028 TERM FUND INC"
    },
    "VACC": {
        "cik": 1828185,
        "title": "Vaccitech plc"
    },
    "RDI": {
        "cik": 716634,
        "title": "READING INTERNATIONAL INC"
    },
    "ENBP": {
        "cik": 1437479,
        "title": "ENB Financial Corp"
    },
    "GECC": {
        "cik": 1675033,
        "title": "Great Elm Capital Corp."
    },
    "JEQ": {
        "cik": 866095,
        "title": "ABRDN JAPAN EQUITY FUND, INC."
    },
    "RCLF": {
        "cik": 1833498,
        "title": "Rosecliff Acquisition Corp I"
    },
    "MCHX": {
        "cik": 1224133,
        "title": "MARCHEX INC"
    },
    "RBKB": {
        "cik": 1751783,
        "title": "Rhinebeck Bancorp, Inc."
    },
    "AFMD": {
        "cik": 1608390,
        "title": "Affimed N.V."
    },
    "ACR": {
        "cik": 1332551,
        "title": "ACRES Commercial Realty Corp."
    },
    "BYRN": {
        "cik": 1354866,
        "title": "Byrna Technologies Inc."
    },
    "DRIO": {
        "cik": 1533998,
        "title": "DarioHealth Corp."
    },
    "FLUX": {
        "cik": 1083743,
        "title": "Flux Power Holdings, Inc."
    },
    "NTZ": {
        "cik": 900391,
        "title": "NATUZZI S P A"
    },
    "EGLX": {
        "cik": 1854233,
        "title": "Enthusiast Gaming Holdings Inc. / Canada"
    },
    "IGTA": {
        "cik": 1866838,
        "title": "Inception Growth Acquisition Ltd"
    },
    "VTSI": {
        "cik": 1085243,
        "title": "VirTra, Inc"
    },
    "CLGN": {
        "cik": 1631487,
        "title": "CollPlant Biotechnologies Ltd"
    },
    "MHUA": {
        "cik": 1835615,
        "title": "Meihua International Medical Technologies Co., Ltd."
    },
    "QOMO": {
        "cik": 1894210,
        "title": "Qomolangma Acquisition Corp."
    },
    "AQU": {
        "cik": 1861063,
        "title": "Aquaron Acquisition Corp."
    },
    "BNED": {
        "cik": 1634117,
        "title": "Barnes & Noble Education, Inc."
    },
    "OXBC": {
        "cik": 1473086,
        "title": "Oxford Bank Corp"
    },
    "THM": {
        "cik": 1134115,
        "title": "INTERNATIONAL TOWER HILL MINES LTD"
    },
    "GTAC": {
        "cik": 1848821,
        "title": "Global Technology Acquisition Corp. I"
    },
    "IMUX": {
        "cik": 1280776,
        "title": "IMMUNIC, INC."
    },
    "BKSC": {
        "cik": 1007273,
        "title": "BANK OF SOUTH CAROLINA CORP"
    },
    "MGYR": {
        "cik": 1337068,
        "title": "Magyar Bancorp, Inc."
    },
    "AUID": {
        "cik": 1534154,
        "title": "authID Inc."
    },
    "ELYM": {
        "cik": 1768446,
        "title": "Eliem Therapeutics, Inc."
    },
    "SURG": {
        "cik": 1392694,
        "title": "SurgePays, Inc."
    },
    "SLGL": {
        "cik": 1684693,
        "title": "Sol-Gel Technologies Ltd."
    },
    "KSCP": {
        "cik": 1600983,
        "title": "Knightscope, Inc."
    },
    "AKLI": {
        "cik": 1850266,
        "title": "Akili, Inc."
    },
    "TETE": {
        "cik": 1900679,
        "title": "Technology & Telecommunication Acquisition Corp"
    },
    "TMQ": {
        "cik": 1543418,
        "title": "Trilogy Metals Inc."
    },
    "JHAA": {
        "cik": 1753217,
        "title": "Nuveen Corporate Income 2023 Target Term Fund"
    },
    "UXIN": {
        "cik": 1729173,
        "title": "Uxin Ltd"
    },
    "FMBM": {
        "cik": 740806,
        "title": "F&M BANK CORP"
    },
    "QUBT": {
        "cik": 1758009,
        "title": "Quantum Computing Inc."
    },
    "DMTK": {
        "cik": 1651944,
        "title": "DermTech, Inc."
    },
    "VIRC": {
        "cik": 751365,
        "title": "VIRCO MFG CORPORATION"
    },
    "BFNH": {
        "cik": 1310488,
        "title": "BIOFORCE NANOSCIENCES HOLDINGS, INC."
    },
    "PMHG": {
        "cik": 1586454,
        "title": "Prime Meridian Holding Co"
    },
    "XLO": {
        "cik": 1840233,
        "title": "Xilio Therapeutics, Inc."
    },
    "BHG": {
        "cik": 1671284,
        "title": "Bright Health Group Inc."
    },
    "BVFL": {
        "cik": 1302387,
        "title": "BV Financial, Inc."
    },
    "GGAAF": {
        "cik": 1865697,
        "title": "Genesis Growth Tech Acquisition Corp."
    },
    "SLDB": {
        "cik": 1707502,
        "title": "Solid Biosciences Inc."
    },
    "KPEA": {
        "cik": 1502557,
        "title": "Kun Peng International Ltd."
    },
    "PPIH": {
        "cik": 914122,
        "title": "Perma-Pipe International Holdings, Inc."
    },
    "JUVF": {
        "cik": 714712,
        "title": "JUNIATA VALLEY FINANCIAL CORP"
    },
    "WIMI": {
        "cik": 1770088,
        "title": "WiMi Hologram Cloud Inc."
    },
    "LIVB": {
        "cik": 1875257,
        "title": "LIV Capital Acquisition Corp. II"
    },
    "FXCO": {
        "cik": 1817565,
        "title": "Financial Strategies Acquisition Corp."
    },
    "OXUS": {
        "cik": 1852973,
        "title": "Oxus Acquisition Corp."
    },
    "WRAP": {
        "cik": 1702924,
        "title": "WRAP TECHNOLOGIES, INC."
    },
    "HYMC": {
        "cik": 1718405,
        "title": "HYCROFT MINING HOLDING CORP"
    },
    "NSPR": {
        "cik": 1433607,
        "title": "InspireMD, Inc."
    },
    "EYEN": {
        "cik": 1682639,
        "title": "EYENOVIA, INC."
    },
    "PXLW": {
        "cik": 1040161,
        "title": "PIXELWORKS, INC"
    },
    "ZEPP": {
        "cik": 1720446,
        "title": "Zepp Health Corp"
    },
    "SOTK": {
        "cik": 806172,
        "title": "SONO TEK CORP"
    },
    "TRON": {
        "cik": 1847513,
        "title": "CORNER GROWTH ACQUISITION CORP. 2"
    },
    "STCN": {
        "cik": 914712,
        "title": "Steel Connect, Inc."
    },
    "SCOR": {
        "cik": 1158172,
        "title": "COMSCORE, INC."
    },
    "HCWB": {
        "cik": 1828673,
        "title": "HCW Biologics Inc."
    },
    "PWFL": {
        "cik": 1774170,
        "title": "PowerFleet, Inc."
    },
    "IRME": {
        "cik": 1839133,
        "title": "IR-Med, Inc."
    },
    "WNLV": {
        "cik": 1558740,
        "title": "Winvest Group Ltd"
    },
    "VBFC": {
        "cik": 1290476,
        "title": "Village Bank & Trust Financial Corp."
    },
    "BYFC": {
        "cik": 1001171,
        "title": "BROADWAY FINANCIAL CORP DE"
    },
    "TLSA": {
        "cik": 1723069,
        "title": "Tiziana Life Sciences Ltd"
    },
    "JPT": {
        "cik": 1679033,
        "title": "Nuveen Preferred & Income Fund"
    },
    "PNAC": {
        "cik": 1858180,
        "title": "Prime Number Acquisition I Corp."
    },
    "GGROU": {
        "cik": 1489874,
        "title": "Golden Growers Cooperative"
    },
    "STRM": {
        "cik": 1008586,
        "title": "STREAMLINE HEALTH SOLUTIONS INC."
    },
    "MAQC": {
        "cik": 1844419,
        "title": "Maquia Capital Acquisition Corp"
    },
    "TACT": {
        "cik": 1017303,
        "title": "TRANSACT TECHNOLOGIES INC"
    },
    "ASXC": {
        "cik": 876378,
        "title": "ASENSUS SURGICAL, INC."
    },
    "IDR": {
        "cik": 1030192,
        "title": "Idaho Strategic Resources, Inc."
    },
    "CTCX": {
        "cik": 1842939,
        "title": "Carmell Corp"
    },
    "FATH": {
        "cik": 1836176,
        "title": "Fathom Digital Manufacturing Corp"
    },
    "PSIX": {
        "cik": 1137091,
        "title": "POWER SOLUTIONS INTERNATIONAL, INC."
    },
    "CEV": {
        "cik": 1074692,
        "title": "EATON VANCE CALIFORNIA MUNICIPAL INCOME TRUST"
    },
    "CSPI": {
        "cik": 356037,
        "title": "CSP INC /MA/"
    },
    "GAN": {
        "cik": 1799332,
        "title": "GAN Ltd"
    },
    "UNIB": {
        "cik": 811211,
        "title": "UNIVERSITY BANCORP INC /DE/"
    },
    "SPRO": {
        "cik": 1701108,
        "title": "Spero Therapeutics, Inc."
    },
    "TCBC": {
        "cik": 1850398,
        "title": "TC Bancshares, Inc."
    },
    "ARAT": {
        "cik": 1566243,
        "title": "Arax Holdings Corp"
    },
    "GLXZ": {
        "cik": 13156,
        "title": "Galaxy Gaming, Inc."
    },
    "RFLFY": {
        "cik": 1448815,
        "title": "Raffles Education Corp Ltd"
    },
    "LBBB": {
        "cik": 1867287,
        "title": "Lakeshore Acquisition II Corp."
    },
    "FHLT": {
        "cik": 1851182,
        "title": "Future Health ESG Corp."
    },
    "CVM": {
        "cik": 725363,
        "title": "CEL SCI CORP"
    },
    "JOB": {
        "cik": 40570,
        "title": "GEE Group Inc."
    },
    "DOMA": {
        "cik": 1722438,
        "title": "Doma Holdings, Inc."
    },
    "ZYNE": {
        "cik": 1621443,
        "title": "Zynerba Pharmaceuticals, Inc."
    },
    "CULP": {
        "cik": 723603,
        "title": "CULP INC"
    },
    "FORL": {
        "cik": 1936255,
        "title": "Four Leaf Acquisition Corp"
    },
    "LEE": {
        "cik": 58361,
        "title": "LEE ENTERPRISES, Inc"
    },
    "GLV": {
        "cik": 1288795,
        "title": "Clough Global Dividend & Income Fund"
    },
    "CXAI": {
        "cik": 1820875,
        "title": "CXApp Inc."
    },
    "SLBK": {
        "cik": 1657642,
        "title": "Skyline Bankshares, Inc."
    },
    "KWIK": {
        "cik": 1884164,
        "title": "KwikClick, Inc."
    },
    "APCX": {
        "cik": 1070050,
        "title": "AppTech Payments Corp."
    },
    "DZSI": {
        "cik": 1101680,
        "title": "DZS INC."
    },
    "PBAX": {
        "cik": 1870404,
        "title": "PHOENIX BIOTECH ACQUISITION CORP."
    },
    "MURF": {
        "cik": 1896212,
        "title": "Murphy Canyon Acquisition Corp."
    },
    "BQ": {
        "cik": 1815021,
        "title": "Boqii Holding Ltd"
    },
    "SNDA": {
        "cik": 1043000,
        "title": "SONIDA SENIOR LIVING, INC."
    },
    "CLOE": {
        "cik": 1849058,
        "title": "Clover Leaf Capital Corp."
    },
    "VLT": {
        "cik": 846671,
        "title": "Invesco High Income Trust II"
    },
    "INCR": {
        "cik": 1857030,
        "title": "Intercure Ltd."
    },
    "UEEC": {
        "cik": 1096938,
        "title": "United Health Products, Inc."
    },
    "RMTI": {
        "cik": 1041024,
        "title": "ROCKWELL MEDICAL, INC."
    },
    "TKNO": {
        "cik": 1850902,
        "title": "Alpha Teknova, Inc."
    },
    "LFVN": {
        "cik": 849146,
        "title": "Lifevantage Corp"
    },
    "NVAC": {
        "cik": 1859807,
        "title": "NorthView Acquisition Corp"
    },
    "AVRO": {
        "cik": 1681087,
        "title": "AVROBIO, Inc."
    },
    "IAE": {
        "cik": 1385632,
        "title": "Voya Asia Pacific High Dividend Equity Income Fund"
    },
    "VIOT": {
        "cik": 1742770,
        "title": "Viomi Technology Co., Ltd"
    },
    "TPCS": {
        "cik": 1328792,
        "title": "TECHPRECISION CORP"
    },
    "BCLI": {
        "cik": 1137883,
        "title": "BRAINSTORM CELL THERAPEUTICS INC."
    },
    "LAES": {
        "cik": 1951222,
        "title": "SEALSQ Corp"
    },
    "LTCN": {
        "cik": 1732406,
        "title": "Grayscale Litecoin Trust (LTC)"
    },
    "VPLM": {
        "cik": 1410738,
        "title": "Voip-pal.com Inc"
    },
    "TATT": {
        "cik": 808439,
        "title": "TAT TECHNOLOGIES LTD"
    },
    "UBCP": {
        "cik": 731653,
        "title": "UNITED BANCORP INC /OH/"
    },
    "CXH": {
        "cik": 847411,
        "title": "MFS INVESTMENT GRADE MUNICIPAL TRUST"
    },
    "DMYY": {
        "cik": 1915380,
        "title": "dMY Squared Technology Group, Inc."
    },
    "RIDEQ": {
        "cik": 1759546,
        "title": "Lordstown Motors Corp."
    },
    "YBGJ": {
        "cik": 895464,
        "title": "Yubo International Biotech Ltd"
    },
    "MFD": {
        "cik": 1276469,
        "title": "MACQUARIE/FIRST TRUST GLOBAL INFRASTR/UTIL DIV & INC FUND"
    },
    "RSSS": {
        "cik": 1386301,
        "title": "Research Solutions, Inc."
    },
    "LINK": {
        "cik": 828146,
        "title": "INTERLINK ELECTRONICS INC"
    },
    "HUIZ": {
        "cik": 1778982,
        "title": "Huize Holding Ltd"
    },
    "PPSI": {
        "cik": 1449792,
        "title": "PIONEER POWER SOLUTIONS, INC."
    },
    "IPWR": {
        "cik": 1507957,
        "title": "Ideal Power Inc."
    },
    "ASTR": {
        "cik": 1814329,
        "title": "Astra Space, Inc."
    },
    "FTK": {
        "cik": 928054,
        "title": "FLOTEK INDUSTRIES INC/CN/"
    },
    "GNS": {
        "cik": 1847806,
        "title": "Genius Group Ltd"
    },
    "SERA": {
        "cik": 1534969,
        "title": "SERA PROGNOSTICS, INC."
    },
    "NERV": {
        "cik": 1598646,
        "title": "Minerva Neurosciences, Inc."
    },
    "GVXXF": {
        "cik": 1490596,
        "title": "GoviEx Uranium Inc."
    },
    "CRDL": {
        "cik": 1702123,
        "title": "Cardiol Therapeutics Inc."
    },
    "HYSR": {
        "cik": 1481028,
        "title": "SUNHYDROGEN, INC."
    },
    "MTC": {
        "cik": 1742518,
        "title": "MMTec, Inc."
    },
    "BGI": {
        "cik": 1179821,
        "title": "BIRKS GROUP INC."
    },
    "NUVR": {
        "cik": 71557,
        "title": "Nuvera Communications, Inc."
    },
    "MACA": {
        "cik": 1835416,
        "title": "Moringa Acquisition Corp"
    },
    "FOTB": {
        "cik": 1099668,
        "title": "FIRST OTTAWA BANCSHARES, INC"
    },
    "ESOA": {
        "cik": 1357971,
        "title": "Energy Services of America CORP"
    },
    "CYBN": {
        "cik": 1833141,
        "title": "CYBIN INC."
    },
    "BZFD": {
        "cik": 1828972,
        "title": "BuzzFeed, Inc."
    },
    "BCRD": {
        "cik": 1496690,
        "title": "BlueOne Card, Inc."
    },
    "GEG": {
        "cik": 1831096,
        "title": "Great Elm Group, Inc."
    },
    "ACAC": {
        "cik": 1914023,
        "title": "Acri Capital Acquisition Corp"
    },
    "PNF": {
        "cik": 1140410,
        "title": "PIMCO NEW YORK MUNICIPAL INCOME FUND"
    },
    "FIXX": {
        "cik": 1661998,
        "title": "Homology Medicines, Inc."
    },
    "INTE": {
        "cik": 1850262,
        "title": "Integral Acquisition Corp 1"
    },
    "PGZ": {
        "cik": 1557523,
        "title": "Principal Real Estate Income Fund"
    },
    "KORE": {
        "cik": 1855457,
        "title": "KORE Group Holdings, Inc."
    },
    "TIL": {
        "cik": 1789769,
        "title": "Instil Bio, Inc."
    },
    "MUGH": {
        "cik": 1746119,
        "title": "MU GLOBAL HOLDING Ltd"
    },
    "VIA": {
        "cik": 1606268,
        "title": "Via Renewables, Inc."
    },
    "JYD": {
        "cik": 1938186,
        "title": "Jayud Global Logistics Ltd"
    },
    "PMVC": {
        "cik": 1807765,
        "title": "PMV Consumer Acquisition Corp."
    },
    "MESA": {
        "cik": 810332,
        "title": "MESA AIR GROUP INC"
    },
    "IHTA": {
        "cik": 1698508,
        "title": "Invesco High Income 2024 Target Term Fund"
    },
    "FEIM": {
        "cik": 39020,
        "title": "FREQUENCY ELECTRONICS INC"
    },
    "TMRC": {
        "cik": 1445942,
        "title": "Texas Mineral Resources Corp."
    },
    "SEPA": {
        "cik": 1849902,
        "title": "SEP Acquisition Corp."
    },
    "FBIO": {
        "cik": 1429260,
        "title": "Fortress Biotech, Inc."
    },
    "PNYG": {
        "cik": 1784058,
        "title": "Pony Group Inc."
    },
    "INSG": {
        "cik": 1022652,
        "title": "INSEEGO CORP."
    },
    "GOLQ": {
        "cik": 1746278,
        "title": "GoLogiq, Inc."
    },
    "FFNTF": {
        "cik": 1783875,
        "title": "4Front Ventures Corp."
    },
    "OLIT": {
        "cik": 1866816,
        "title": "OmniLit Acquisition Corp."
    },
    "EAR": {
        "cik": 1719395,
        "title": "Eargo, Inc."
    },
    "ARBK": {
        "cik": 1841675,
        "title": "Argo Blockchain Plc"
    },
    "TOI": {
        "cik": 1799191,
        "title": "Oncology Institute, Inc."
    },
    "ROSE": {
        "cik": 1870129,
        "title": "Rose Hill Acquisition Corp"
    },
    "BUKS": {
        "cik": 15847,
        "title": "BUTLER NATIONAL CORP"
    },
    "NMS": {
        "cik": 1607997,
        "title": "Nuveen Minnesota Quality Municipal Income Fund"
    },
    "ICAD": {
        "cik": 749660,
        "title": "ICAD INC"
    },
    "MOVE": {
        "cik": 1734750,
        "title": "Movano Inc."
    },
    "CMCM": {
        "cik": 1597835,
        "title": "Cheetah Mobile Inc."
    },
    "TTP": {
        "cik": 1526329,
        "title": "TORTOISE PIPELINE & ENERGY FUND, INC."
    },
    "CCTS": {
        "cik": 1865861,
        "title": "Cactus Acquisition Corp. 1 Ltd"
    },
    "ITAQ": {
        "cik": 1841586,
        "title": "Industrial Tech Acquisitions II, Inc."
    },
    "WMC": {
        "cik": 1465885,
        "title": "Western Asset Mortgage Capital Corp"
    },
    "AP": {
        "cik": 6176,
        "title": "AMPCO PITTSBURGH CORP"
    },
    "KEYR": {
        "cik": 1832161,
        "title": "KeyStar Corp."
    },
    "REDW": {
        "cik": 942895,
        "title": "REDWOOD FINANCIAL INC /MN/"
    },
    "DARE": {
        "cik": 1401914,
        "title": "Dare Bioscience, Inc."
    },
    "HRGN": {
        "cik": 1563665,
        "title": "Harvard Apparatus Regenerative Technology, Inc."
    },
    "AIRT": {
        "cik": 353184,
        "title": "AIR T INC"
    },
    "ITRG": {
        "cik": 1722387,
        "title": "Integra Resources Corp."
    },
    "LPTH": {
        "cik": 889971,
        "title": "LIGHTPATH TECHNOLOGIES INC"
    },
    "DYNR": {
        "cik": 1111741,
        "title": "DYNARESOURCE INC"
    },
    "FAM": {
        "cik": 1302624,
        "title": "FIRST TRUST/ABRDN GLOBAL OPPORTUNITY INCOME FUND"
    },
    "APGT": {
        "cik": 1353538,
        "title": "Appgate, Inc."
    },
    "LSBK": {
        "cik": 1341318,
        "title": "LAKE SHORE BANCORP, INC."
    },
    "AYRWF": {
        "cik": 1847462,
        "title": "Ayr Wellness Inc."
    },
    "HSON": {
        "cik": 1210708,
        "title": "Hudson Global, Inc."
    },
    "NA": {
        "cik": 1872302,
        "title": "Nano Labs Ltd"
    },
    "CLSD": {
        "cik": 1539029,
        "title": "Clearside Biomedical, Inc."
    },
    "BAFN": {
        "cik": 1649739,
        "title": "BayFirst Financial Corp."
    },
    "QMCO": {
        "cik": 709283,
        "title": "QUANTUM CORP /DE/"
    },
    "SSIC": {
        "cik": 1843162,
        "title": "Silver Spike Investment Corp."
    },
    "BEAT": {
        "cik": 1779372,
        "title": "HeartBeam, Inc."
    },
    "LUCD": {
        "cik": 1799011,
        "title": "Lucid Diagnostics Inc."
    },
    "NHTC": {
        "cik": 912061,
        "title": "NATURAL HEALTH TRENDS CORP"
    },
    "PEPL": {
        "cik": 1873324,
        "title": "PepperLime Health Acquisition Corp"
    },
    "ENCP": {
        "cik": 1879373,
        "title": "Energem Corp"
    },
    "ARKR": {
        "cik": 779544,
        "title": "ARK RESTAURANTS CORP"
    },
    "CRIS": {
        "cik": 1108205,
        "title": "CURIS INC"
    },
    "KPLT": {
        "cik": 1785424,
        "title": "Katapult Holdings, Inc."
    },
    "KSBI": {
        "cik": 912764,
        "title": "KS BANCORP INC"
    },
    "NBW": {
        "cik": 1178840,
        "title": "NEUBERGER BERMAN CALIFORNIA MUNICIPAL FUND INC."
    },
    "FLNT": {
        "cik": 1460329,
        "title": "Fluent, Inc."
    },
    "ASCA": {
        "cik": 1868775,
        "title": "ASPAC I Acquisition Corp."
    },
    "HOUR": {
        "cik": 1874875,
        "title": "Hour Loop, Inc"
    },
    "LOGQ": {
        "cik": 768216,
        "title": "Coyni, Inc."
    },
    "INKT": {
        "cik": 1840229,
        "title": "MiNK Therapeutics, Inc."
    },
    "MBTC": {
        "cik": 1837344,
        "title": "Nocturne Acquisition Corp"
    },
    "PNPL": {
        "cik": 1654672,
        "title": "PINEAPPLE, INC."
    },
    "CIZN": {
        "cik": 1075706,
        "title": "CITIZENS HOLDING CO /MS/"
    },
    "BNIX": {
        "cik": 1845942,
        "title": "Bannix Acquisition Corp."
    },
    "MRKR": {
        "cik": 1094038,
        "title": "Marker Therapeutics, Inc."
    },
    "BDL": {
        "cik": 12040,
        "title": "FLANIGANS ENTERPRISES INC"
    },
    "LTBR": {
        "cik": 1084554,
        "title": "LIGHTBRIDGE Corp"
    },
    "CEE": {
        "cik": 860489,
        "title": "CENTRAL & EASTERN EUROPE FUND, INC."
    },
    "PTWO": {
        "cik": 1930313,
        "title": "Pono Capital Two, Inc."
    },
    "LRFC": {
        "cik": 1571329,
        "title": "Logan Ridge Finance Corp."
    },
    "HLTH": {
        "cik": 1628945,
        "title": "Cue Health Inc."
    },
    "ICMB": {
        "cik": 1578348,
        "title": "Investcorp Credit Management BDC, Inc."
    },
    "CLST": {
        "cik": 1849867,
        "title": "Catalyst Bancorp, Inc."
    },
    "AKA": {
        "cik": 1865107,
        "title": "A.K.A. BRANDS HOLDING CORP."
    },
    "PFBX": {
        "cik": 770460,
        "title": "PEOPLES FINANCIAL CORP /MS/"
    },
    "SHUA": {
        "cik": 1886268,
        "title": "SHUAA Partners Acquisition Corp I"
    },
    "EEA": {
        "cik": 791718,
        "title": "EUROPEAN EQUITY FUND, INC / MD"
    },
    "ZYRX": {
        "cik": 1957401,
        "title": "GLOBAL EARNINGS CAPITAL LTD."
    },
    "BDCO": {
        "cik": 793306,
        "title": "BLUE DOLPHIN ENERGY CO"
    },
    "SZSMF": {
        "cik": 1548536,
        "title": "Santacruz Silver Mining Ltd."
    },
    "MTMV": {
        "cik": 1393044,
        "title": "Motomova Inc"
    },
    "RGT": {
        "cik": 1514490,
        "title": "ROYCE GLOBAL VALUE TRUST, INC."
    },
    "PDEX": {
        "cik": 788920,
        "title": "PRO DEX INC"
    },
    "TOON": {
        "cik": 1355848,
        "title": "Kartoon Studios, Inc."
    },
    "SURF": {
        "cik": 1718108,
        "title": "Surface Oncology, Inc."
    },
    "AEYE": {
        "cik": 1362190,
        "title": "AUDIOEYE INC"
    },
    "HHGC": {
        "cik": 1822886,
        "title": "HHG Capital Corp"
    },
    "FDOC": {
        "cik": 1459188,
        "title": "FUEL DOCTOR HOLDINGS, INC."
    },
    "VTVT": {
        "cik": 1641489,
        "title": "vTv Therapeutics Inc."
    },
    "TRIQ": {
        "cik": 1514056,
        "title": "TRAQIQ, INC."
    },
    "VGZ": {
        "cik": 783324,
        "title": "VISTA GOLD CORP"
    },
    "SELF": {
        "cik": 1031235,
        "title": "Global Self Storage, Inc."
    },
    "NDP": {
        "cik": 1547158,
        "title": "TORTOISE ENERGY INDEPENDENCE FUND, INC."
    },
    "IBTN": {
        "cik": 1379329,
        "title": "InsCorp Inc"
    },
    "DUNE": {
        "cik": 1817232,
        "title": "Dune Acquisition Corp"
    },
    "ORPB": {
        "cik": 1216128,
        "title": "OREGON PACIFIC BANCORP"
    },
    "IOBT": {
        "cik": 1865494,
        "title": "IO Biotech, Inc."
    },
    "BWAY": {
        "cik": 1505065,
        "title": "Brainsway Ltd."
    },
    "RGS": {
        "cik": 716643,
        "title": "REGIS CORP"
    },
    "HOOK": {
        "cik": 1760542,
        "title": "HOOKIPA Pharma Inc."
    },
    "RSKIA": {
        "cik": 84112,
        "title": "GEORGE RISK INDUSTRIES, INC."
    },
    "MKTW": {
        "cik": 1805651,
        "title": "MARKETWISE, INC."
    },
    "CELU": {
        "cik": 1752828,
        "title": "Celularity Inc"
    },
    "JMM": {
        "cik": 838131,
        "title": "Nuveen Multi-Market Income Fund"
    },
    "CCM": {
        "cik": 1472072,
        "title": "Concord Medical Services Holdings Ltd"
    },
    "SMAP": {
        "cik": 1863990,
        "title": "Sportsmap Tech Acquisition Corp."
    },
    "PWM": {
        "cik": 1765850,
        "title": "Prestige Wealth Inc."
    },
    "RCAT": {
        "cik": 748268,
        "title": "Red Cat Holdings, Inc."
    },
    "BNET": {
        "cik": 875729,
        "title": "BION ENVIRONMENTAL TECHNOLOGIES INC"
    },
    "APRN": {
        "cik": 1701114,
        "title": "Blue Apron Holdings, Inc."
    },
    "SONX": {
        "cik": 1407973,
        "title": "Sonendo, Inc."
    },
    "REFR": {
        "cik": 793524,
        "title": "RESEARCH FRONTIERS INC"
    },
    "ZAPP": {
        "cik": 1955104,
        "title": "Zapp Electric Vehicles Group Ltd"
    },
    "AIXN": {
        "cik": 835662,
        "title": "AiXin Life International, Inc."
    },
    "DCTH": {
        "cik": 872912,
        "title": "DELCATH SYSTEMS, INC."
    },
    "ADAG": {
        "cik": 1818838,
        "title": "Adagene Inc."
    },
    "RACY": {
        "cik": 1860484,
        "title": "Relativity Acquisition Corp"
    },
    "ASRV": {
        "cik": 707605,
        "title": "AMERISERV FINANCIAL INC /PA/"
    },
    "MCAF": {
        "cik": 1853774,
        "title": "Mountain Crest Acquisition Corp. IV"
    },
    "CBKM": {
        "cik": 1006830,
        "title": "CONSUMERS BANCORP INC /OH/"
    },
    "HNNA": {
        "cik": 1145255,
        "title": "HENNESSY ADVISORS INC"
    },
    "RZLT": {
        "cik": 1509261,
        "title": "Rezolute, Inc."
    },
    "SRTS": {
        "cik": 1494891,
        "title": "Sensus Healthcare, Inc."
    },
    "NWPP": {
        "cik": 1163389,
        "title": "NEW PEOPLES BANKSHARES INC"
    },
    "DYAI": {
        "cik": 1213809,
        "title": "DYADIC INTERNATIONAL INC"
    },
    "DTIL": {
        "cik": 1357874,
        "title": "PRECISION BIOSCIENCES INC"
    },
    "RFL": {
        "cik": 1713863,
        "title": "Rafael Holdings, Inc."
    },
    "VASO": {
        "cik": 839087,
        "title": "VASO Corp"
    },
    "CETY": {
        "cik": 1329606,
        "title": "Clean Energy Technologies, Inc."
    },
    "LOAN": {
        "cik": 1080340,
        "title": "MANHATTAN BRIDGE CAPITAL, INC"
    },
    "CHKR": {
        "cik": 1524769,
        "title": "CHESAPEAKE GRANITE WASH TRUST"
    },
    "DMAQ": {
        "cik": 1857086,
        "title": "Deep Medicine Acquisition Corp."
    },
    "SLNA": {
        "cik": 1909417,
        "title": "SELINA HOSPITALITY PLC"
    },
    "EDI": {
        "cik": 1551040,
        "title": "Virtus Stone Harbor Emerging Markets Total Income Fund"
    },
    "GIFI": {
        "cik": 1031623,
        "title": "GULF ISLAND FABRICATION INC"
    },
    "AGSS": {
        "cik": 1514443,
        "title": "AMERIGUARD SECURITY SERVICES, INC."
    },
    "LGVN": {
        "cik": 1721484,
        "title": "Longeveron Inc."
    },
    "BHM": {
        "cik": 1903382,
        "title": "Bluerock Homes Trust, Inc."
    },
    "HUDI": {
        "cik": 1791725,
        "title": "Huadi International Group Co., Ltd."
    },
    "FURY": {
        "cik": 1514597,
        "title": "FURY GOLD MINES LTD"
    },
    "IPA": {
        "cik": 1715925,
        "title": "ImmunoPrecise Antibodies Ltd."
    },
    "ADES": {
        "cik": 1515156,
        "title": "Advanced Emissions Solutions, Inc."
    },
    "LQMT": {
        "cik": 1141240,
        "title": "LIQUIDMETAL TECHNOLOGIES INC"
    },
    "AURX": {
        "cik": 1091596,
        "title": "Nuo Therapeutics, Inc."
    },
    "KTCC": {
        "cik": 719733,
        "title": "KEY TRONIC CORP"
    },
    "APT": {
        "cik": 884269,
        "title": "ALPHA PRO TECH LTD"
    },
    "AIRRF": {
        "cik": 1476573,
        "title": "Aurion Resources Ltd."
    },
    "MFH": {
        "cik": 1527762,
        "title": "Mercurity Fintech Holding Inc."
    },
    "BTQQF": {
        "cik": 1821866,
        "title": "Sonora Gold & Silver Corp."
    },
    "MPIR": {
        "cik": 815577,
        "title": "Empire Diversified Energy Inc"
    },
    "NTIP": {
        "cik": 1065078,
        "title": "NETWORK-1 TECHNOLOGIES, INC."
    },
    "FUSB": {
        "cik": 717806,
        "title": "FIRST US BANCSHARES, INC."
    },
    "SCTL": {
        "cik": 1588972,
        "title": "Societal CDMO, Inc."
    },
    "SNAL": {
        "cik": 1886894,
        "title": "Snail, Inc."
    },
    "SMDRF": {
        "cik": 1939801,
        "title": "SIERRA MADRE GOLD & SILVER LTD."
    },
    "ELTK": {
        "cik": 1024672,
        "title": "ELTEK LTD"
    },
    "RAIL": {
        "cik": 1320854,
        "title": "FreightCar America, Inc."
    },
    "PNXP": {
        "cik": 1710495,
        "title": "PINEAPPLE EXPRESS CANNABIS Co"
    },
    "WKSP": {
        "cik": 1096275,
        "title": "Worksport Ltd"
    },
    "CRWS": {
        "cik": 25895,
        "title": "CROWN CRAFTS INC"
    },
    "XOS": {
        "cik": 1819493,
        "title": "Xos, Inc."
    },
    "RSF": {
        "cik": 1644771,
        "title": "RiverNorth Capital & Income Fund, Inc."
    },
    "ICCH": {
        "cik": 1681903,
        "title": "ICC Holdings, Inc."
    },
    "MTRY": {
        "cik": 1860663,
        "title": "Monterey Innovation Acquisition Corp"
    },
    "CFOO": {
        "cik": 1310630,
        "title": "China Foods Holdings Ltd."
    },
    "CLRC": {
        "cik": 1903392,
        "title": "ClimateRock"
    },
    "HTY": {
        "cik": 1396502,
        "title": "John Hancock Tax-Advantaged Global Shareholder Yield Fund"
    },
    "IROQ": {
        "cik": 1514743,
        "title": "IF Bancorp, Inc."
    },
    "SLNO": {
        "cik": 1484565,
        "title": "SOLENO THERAPEUTICS INC"
    },
    "OTEC": {
        "cik": 1846809,
        "title": "OceanTech Acquisitions I Corp."
    },
    "MKUL": {
        "cik": 1872356,
        "title": "Molekule Group, Inc."
    },
    "GRFX": {
        "cik": 1816723,
        "title": "Graphex Group Ltd"
    },
    "AUGG": {
        "cik": 1448597,
        "title": "AUGUSTA GOLD CORP."
    },
    "SPAZF": {
        "cik": 1337090,
        "title": "SPANISH MOUNTAIN GOLD LTD."
    },
    "UWHR": {
        "cik": 898171,
        "title": "UWHARRIE CAPITAL CORP"
    },
    "EPOW": {
        "cik": 1780731,
        "title": "Sunrise New Energy Co., Ltd."
    },
    "DHAC": {
        "cik": 1864531,
        "title": "DIGITAL HEALTH ACQUISITION CORP."
    },
    "VANI": {
        "cik": 1266806,
        "title": "Vivani Medical, Inc."
    },
    "IOR": {
        "cik": 949961,
        "title": "INCOME OPPORTUNITY REALTY INVESTORS INC /TX/"
    },
    "LTRN": {
        "cik": 1763950,
        "title": "Lantern Pharma Inc."
    },
    "TAOP": {
        "cik": 1552670,
        "title": "Taoping Inc."
    },
    "DLA": {
        "cik": 1101396,
        "title": "DELTA APPAREL, INC"
    },
    "HFBL": {
        "cik": 1500375,
        "title": "Home Federal Bancorp, Inc. of Louisiana"
    },
    "VSAC": {
        "cik": 1883983,
        "title": "VISION SENSING ACQUISITION CORP."
    },
    "VWE": {
        "cik": 1834045,
        "title": "Vintage Wine Estates, Inc."
    },
    "JRSS": {
        "cik": 1597892,
        "title": "JRSIS HEALTH CARE Corp"
    },
    "GROW": {
        "cik": 754811,
        "title": "U S GLOBAL INVESTORS INC"
    },
    "OTRK": {
        "cik": 1136174,
        "title": "Ontrak, Inc."
    },
    "JOAN": {
        "cik": 1834585,
        "title": "JOANN Inc."
    },
    "MFON": {
        "cik": 1447380,
        "title": "MOBIVITY HOLDINGS CORP."
    },
    "BEST": {
        "cik": 1709505,
        "title": "BEST Inc."
    },
    "BOTJ": {
        "cik": 1275101,
        "title": "BANK OF THE JAMES FINANCIAL GROUP INC"
    },
    "HUGE": {
        "cik": 1771885,
        "title": "FSD Pharma Inc."
    },
    "FGB": {
        "cik": 1392994,
        "title": "FIRST TRUST SPECIALTY FINANCE & FINANCIAL OPPORTUNITIES FUND"
    },
    "GGE": {
        "cik": 1158420,
        "title": "Green Giant Inc."
    },
    "BREZ": {
        "cik": 1817640,
        "title": "Breeze Holdings Acquisition Corp."
    },
    "DMA": {
        "cik": 1523289,
        "title": "Destra Multi-Alternative Fund"
    },
    "EBON": {
        "cik": 1799290,
        "title": "Ebang International Holdings Inc."
    },
    "IDN": {
        "cik": 1040896,
        "title": "Intellicheck, Inc."
    },
    "JZ": {
        "cik": 1852440,
        "title": "Jianzhi Education Technology Group Co Ltd"
    },
    "ONDS": {
        "cik": 1646188,
        "title": "Ondas Holdings Inc."
    },
    "SAGA": {
        "cik": 1855351,
        "title": "Sagaliam Acquisition Corp"
    },
    "ISPO": {
        "cik": 1820566,
        "title": "Inspirato Inc"
    },
    "CNTB": {
        "cik": 1835268,
        "title": "Connect Biopharma Holdings Ltd"
    },
    "AGBA": {
        "cik": 1769624,
        "title": "AGBA Group Holding Ltd."
    },
    "LIDR": {
        "cik": 1818644,
        "title": "AEye, Inc."
    },
    "ASMB": {
        "cik": 1426800,
        "title": "ASSEMBLY BIOSCIENCES, INC."
    },
    "JROOF": {
        "cik": 1602380,
        "title": "Jericho Energy Ventures Inc."
    },
    "OESX": {
        "cik": 1409375,
        "title": "ORION ENERGY SYSTEMS, INC."
    },
    "CFSB": {
        "cik": 1879103,
        "title": "CFSB Bancorp, Inc. /MA/"
    },
    "NSTS": {
        "cik": 1881592,
        "title": "NSTS Bancorp, Inc."
    },
    "GETR": {
        "cik": 1839608,
        "title": "Getaround, Inc"
    },
    "FARM": {
        "cik": 34563,
        "title": "FARMER BROTHERS CO"
    },
    "FMY": {
        "cik": 1319183,
        "title": "FIRST TRUST MORTGAGE INCOME FUND"
    },
    "CVV": {
        "cik": 766792,
        "title": "CVD EQUIPMENT CORP"
    },
    "MYMD": {
        "cik": 1321834,
        "title": "MyMD Pharmaceuticals, Inc."
    },
    "ENLV": {
        "cik": 1596812,
        "title": "Enlivex Therapeutics Ltd."
    },
    "ARBB": {
        "cik": 1930179,
        "title": "ARB IOT Group Ltd"
    },
    "BIOF": {
        "cik": 1549145,
        "title": "BLUE BIOFUELS, INC."
    },
    "LODE": {
        "cik": 1120970,
        "title": "Comstock Inc."
    },
    "INVU": {
        "cik": 862651,
        "title": "Investview, Inc."
    },
    "NBO": {
        "cik": 1178841,
        "title": "NEUBERGER BERMAN NEW YORK MUNICIPAL FUND INC."
    },
    "CCEL": {
        "cik": 862692,
        "title": "CRYO CELL INTERNATIONAL INC"
    },
    "LVTX": {
        "cik": 1840748,
        "title": "LAVA Therapeutics NV"
    },
    "CCAI": {
        "cik": 1846968,
        "title": "Cascadia Acquisition Corp."
    },
    "HYFM": {
        "cik": 1695295,
        "title": "HYDROFARM HOLDINGS GROUP, INC."
    },
    "MRDB": {
        "cik": 1929589,
        "title": "MariaDB plc"
    },
    "DXR": {
        "cik": 27367,
        "title": "DAXOR CORP"
    },
    "CURO": {
        "cik": 1711291,
        "title": "CURO Group Holdings Corp."
    },
    "CVU": {
        "cik": 889348,
        "title": "CPI AEROSTRUCTURES INC"
    },
    "VIRX": {
        "cik": 1061027,
        "title": "Viracta Therapeutics, Inc."
    },
    "FRBK": {
        "cik": 834285,
        "title": "REPUBLIC FIRST BANCORP INC"
    },
    "NXPL": {
        "cik": 1058307,
        "title": "NextPlat Corp"
    },
    "HLP": {
        "cik": 1855557,
        "title": "Hongli Group Inc."
    },
    "ICCM": {
        "cik": 1584371,
        "title": "IceCure Medical Ltd."
    },
    "STIM": {
        "cik": 1227636,
        "title": "Neuronetics, Inc."
    },
    "VEV": {
        "cik": 1834975,
        "title": "VICINITY MOTOR CORP"
    },
    "DWSN": {
        "cik": 799165,
        "title": "DAWSON GEOPHYSICAL CO"
    },
    "BLGO": {
        "cik": 880242,
        "title": "BIOLARGO, INC."
    },
    "MOXC": {
        "cik": 1864055,
        "title": "Moxian (BVI) Inc"
    },
    "RVYL": {
        "cik": 1419275,
        "title": "RYVYL Inc."
    },
    "PLAG": {
        "cik": 1117057,
        "title": "Planet Green Holdings Corp."
    },
    "GAIA": {
        "cik": 1089872,
        "title": "GAIA, INC"
    },
    "HHS": {
        "cik": 45919,
        "title": "HARTE HANKS INC"
    },
    "NXN": {
        "cik": 885731,
        "title": "NUVEEN NEW YORK SELECT TAX -FREE INCOME PORTFOLIO"
    },
    "BCOW": {
        "cik": 1847360,
        "title": "1895 Bancorp of Wisconsin, Inc. /MD/"
    },
    "BCAN": {
        "cik": 1888151,
        "title": "BYND CANNASOFT ENTERPRISES INC."
    },
    "NUKK": {
        "cik": 1592782,
        "title": "Nukkleus Inc."
    },
    "MYNZ": {
        "cik": 1874252,
        "title": "MAINZ BIOMED N.V."
    },
    "GSD": {
        "cik": 1843248,
        "title": "Global System Dynamics, Inc."
    },
    "KXIN": {
        "cik": 1713539,
        "title": "Kaixin Auto Holdings"
    },
    "UAMY": {
        "cik": 101538,
        "title": "UNITED STATES ANTIMONY CORP"
    },
    "MGTA": {
        "cik": 1690585,
        "title": "Magenta Therapeutics, Inc."
    },
    "BKTI": {
        "cik": 2186,
        "title": "BK Technologies Corp"
    },
    "MPTI": {
        "cik": 1902314,
        "title": "M-tron Industries, Inc."
    },
    "QNCX": {
        "cik": 1662774,
        "title": "Quince Therapeutics, Inc."
    },
    "MXE": {
        "cik": 863900,
        "title": "MEXICO EQUITY & INCOME FUND INC"
    },
    "KFFB": {
        "cik": 1297341,
        "title": "Kentucky First Federal Bancorp"
    },
    "REE": {
        "cik": 1843588,
        "title": "REE Automotive Ltd."
    },
    "SYPR": {
        "cik": 864240,
        "title": "SYPRIS SOLUTIONS INC"
    },
    "WINV": {
        "cik": 1854463,
        "title": "WinVest Acquisition Corp."
    },
    "BKRRF": {
        "cik": 1699906,
        "title": "BLACKROCK SILVER CORP."
    },
    "ICD": {
        "cik": 1537028,
        "title": "Independence Contract Drilling, Inc."
    },
    "MGLD": {
        "cik": 1005101,
        "title": "Marygold Companies, Inc."
    },
    "PRTG": {
        "cik": 1095435,
        "title": "PORTAGE BIOTECH INC."
    },
    "NANX": {
        "cik": 883107,
        "title": "NANOPHASE TECHNOLOGIES Corp"
    },
    "GANX": {
        "cik": 1819411,
        "title": "Gain Therapeutics, Inc."
    },
    "CURI": {
        "cik": 1776909,
        "title": "CuriosityStream Inc."
    },
    "NXTC": {
        "cik": 1661059,
        "title": "NextCure, Inc."
    },
    "MVLA": {
        "cik": 1839132,
        "title": "Movella Holdings Inc."
    },
    "GCEH": {
        "cik": 748790,
        "title": "Global Clean Energy Holdings, Inc."
    },
    "PPBN": {
        "cik": 1031233,
        "title": "PINNACLE BANKSHARES CORP"
    },
    "PXCLY": {
        "cik": 1888175,
        "title": "Phoenix Copper Limited/ADR"
    },
    "BSGM": {
        "cik": 1530766,
        "title": "BioSig Technologies, Inc."
    },
    "CGTX": {
        "cik": 1455365,
        "title": "COGNITION THERAPEUTICS INC"
    },
    "BOLT": {
        "cik": 1641281,
        "title": "Bolt Biotherapeutics, Inc."
    },
    "AIRG": {
        "cik": 1272842,
        "title": "AIRGAIN INC"
    },
    "KEQU": {
        "cik": 55529,
        "title": "KEWAUNEE SCIENTIFIC CORP /DE/"
    },
    "GDNR": {
        "cik": 1858912,
        "title": "Gardiner Healthcare Acquisitions Corp."
    },
    "MMTIF": {
        "cik": 1085921,
        "title": "MICROMEM TECHNOLOGIES INC"
    },
    "NCSM": {
        "cik": 1692427,
        "title": "NCS Multistage Holdings, Inc."
    },
    "SANW": {
        "cik": 1477246,
        "title": "S&W Seed Co"
    },
    "USIO": {
        "cik": 1088034,
        "title": "Usio, Inc."
    },
    "ALMU": {
        "cik": 1828805,
        "title": "Aeluma, Inc."
    },
    "HOFV": {
        "cik": 1708176,
        "title": "Hall of Fame Resort & Entertainment Co"
    },
    "BRSH": {
        "cik": 1913210,
        "title": "Bruush Oral Care Inc."
    },
    "TURN": {
        "cik": 893739,
        "title": "180 DEGREE CAPITAL CORP. /NY/"
    },
    "RVIV": {
        "cik": 1718500,
        "title": "Reviv3 Procare Co"
    },
    "XGN": {
        "cik": 1274737,
        "title": "EXAGEN INC."
    },
    "NVNO": {
        "cik": 1661053,
        "title": "enVVeno Medical Corp"
    },
    "ACBA": {
        "cik": 1844389,
        "title": "Ace Global Business Acquisition Ltd"
    },
    "CXDO": {
        "cik": 1075736,
        "title": "Crexendo, Inc."
    },
    "VTGN": {
        "cik": 1411685,
        "title": "Vistagen Therapeutics, Inc."
    },
    "GORO": {
        "cik": 1160791,
        "title": "GOLD RESOURCE CORP"
    },
    "IDEX": {
        "cik": 837852,
        "title": "IDEANOMICS, INC."
    },
    "EFTR": {
        "cik": 1828522,
        "title": "eFFECTOR Therapeutics, Inc."
    },
    "SLS": {
        "cik": 1390478,
        "title": "SELLAS Life Sciences Group, Inc."
    },
    "COE": {
        "cik": 1659494,
        "title": "51Talk Online Education Group"
    },
    "ETAO": {
        "cik": 1939696,
        "title": "ETAO International Co., Ltd."
    },
    "MEIP": {
        "cik": 1262104,
        "title": "MEI Pharma, Inc."
    },
    "CTRM": {
        "cik": 1720161,
        "title": "Castor Maritime Inc."
    },
    "HUBC": {
        "cik": 1905660,
        "title": "Hub Cyber Security Ltd."
    },
    "MPU": {
        "cik": 1036848,
        "title": "Mega Matrix Corp."
    },
    "PVCT": {
        "cik": 315545,
        "title": "PROVECTUS BIOPHARMACEUTICALS, INC."
    },
    "HLGN": {
        "cik": 1840292,
        "title": "Heliogen, Inc."
    },
    "PASG": {
        "cik": 1787297,
        "title": "Passage BIO, Inc."
    },
    "DPSI": {
        "cik": 1505611,
        "title": "DecisionPoint Systems, Inc."
    },
    "KWAC": {
        "cik": 1823086,
        "title": "Kingswood Acquisition Corp."
    },
    "VRAR": {
        "cik": 1854445,
        "title": "Glimpse Group, Inc."
    },
    "EXPR": {
        "cik": 1483510,
        "title": "EXPRESS, INC."
    },
    "BIOR": {
        "cik": 1580063,
        "title": "BIORA THERAPEUTICS, INC."
    },
    "GDTC": {
        "cik": 1873093,
        "title": "CytoMed Therapeutics Ltd"
    },
    "TCBS": {
        "cik": 1849466,
        "title": "Texas Community Bancshares, Inc."
    },
    "VGAS": {
        "cik": 1841425,
        "title": "Verde Clean Fuels, Inc."
    },
    "RSTN": {
        "cik": 1760233,
        "title": "RDE, Inc."
    },
    "ALGS": {
        "cik": 1799448,
        "title": "Aligos Therapeutics, Inc."
    },
    "JRSH": {
        "cik": 1696558,
        "title": "Jerash Holdings (US), Inc."
    },
    "ADOC": {
        "cik": 1824884,
        "title": "Edoc Acquisition Corp."
    },
    "RSCI": {
        "cik": 1634394,
        "title": "Redwood Scientific Technologies, Inc."
    },
    "OKYO": {
        "cik": 1849296,
        "title": "OKYO Pharma Ltd"
    },
    "CZOO": {
        "cik": 1859639,
        "title": "Cazoo Group Ltd"
    },
    "MRT": {
        "cik": 1852767,
        "title": "Marti Technologies, Inc."
    },
    "RMRI": {
        "cik": 1556179,
        "title": "Rocky Mountain Industrials, Inc."
    },
    "TECTP": {
        "cik": 1766526,
        "title": "Tectonic Financial, Inc."
    },
    "ESP": {
        "cik": 33533,
        "title": "ESPEY MFG & ELECTRONICS CORP"
    },
    "UMEWF": {
        "cik": 1114936,
        "title": "UMeWorld Ltd"
    },
    "DSWL": {
        "cik": 946936,
        "title": "DESWELL INDUSTRIES INC"
    },
    "TBIO": {
        "cik": 1850079,
        "title": "Telesis Bio Inc."
    },
    "AACG": {
        "cik": 1420529,
        "title": "ATA Creativity Global"
    },
    "YQ": {
        "cik": 1821468,
        "title": "17 Education & Technology Group Inc."
    },
    "ASPI": {
        "cik": 1921865,
        "title": "ASP Isotopes Inc."
    },
    "EDRY": {
        "cik": 1731388,
        "title": "EuroDry Ltd."
    },
    "NAII": {
        "cik": 787253,
        "title": "NATURAL ALTERNATIVES INTERNATIONAL INC"
    },
    "AGMH": {
        "cik": 1705402,
        "title": "AGM GROUP HOLDINGS, INC."
    },
    "PTZH": {
        "cik": 1627469,
        "title": "Photozou Holdings, Inc."
    },
    "CLIR": {
        "cik": 1434524,
        "title": "ClearSign Technologies Corp"
    },
    "AIB": {
        "cik": 1882963,
        "title": "AIB Acquisition Corp"
    },
    "RFIL": {
        "cik": 740664,
        "title": "R F INDUSTRIES LTD"
    },
    "XPL": {
        "cik": 917225,
        "title": "SOLITARIO RESOURCES CORP."
    },
    "SHWZ": {
        "cik": 1622879,
        "title": "Medicine Man Technologies, Inc."
    },
    "SABS": {
        "cik": 1833214,
        "title": "SAB Biotherapeutics, Inc."
    },
    "WAVS": {
        "cik": 1868419,
        "title": "Western Acquisition Ventures Corp."
    },
    "UTRS": {
        "cik": 1452965,
        "title": "MINERVA SURGICAL INC"
    },
    "CKPT": {
        "cik": 1651407,
        "title": "Checkpoint Therapeutics, Inc."
    },
    "NOVV": {
        "cik": 1858028,
        "title": "Nova Vision Acquisition Corp"
    },
    "TISI": {
        "cik": 318833,
        "title": "TEAM INC"
    },
    "TXMD": {
        "cik": 25743,
        "title": "TherapeuticsMD, Inc."
    },
    "NCNA": {
        "cik": 1709626,
        "title": "NuCana plc"
    },
    "MATH": {
        "cik": 1682241,
        "title": "Metalpha Technology Holding Ltd"
    },
    "FVTI": {
        "cik": 1626745,
        "title": "Fortune Valley Treasures, Inc."
    },
    "CTIB": {
        "cik": 1042187,
        "title": "Yunhong CTI Ltd."
    },
    "MTR": {
        "cik": 313364,
        "title": "MESA ROYALTY TRUST/TX"
    },
    "FKWL": {
        "cik": 722572,
        "title": "FRANKLIN WIRELESS CORP"
    },
    "RPID": {
        "cik": 1380106,
        "title": "RAPID MICRO BIOSYSTEMS, INC."
    },
    "PXS": {
        "cik": 1640043,
        "title": "Pyxis Tankers Inc."
    },
    "TKLF": {
        "cik": 1836242,
        "title": "Yoshitsu Co., Ltd"
    },
    "KNW": {
        "cik": 1074828,
        "title": "KNOW LABS, INC."
    },
    "BCHG": {
        "cik": 1732409,
        "title": "Grayscale Bitcoin Cash Trust (BCH)"
    },
    "BANL": {
        "cik": 1914805,
        "title": "CBL International Ltd"
    },
    "BFI": {
        "cik": 1723580,
        "title": "BurgerFi International, Inc."
    },
    "ICCC": {
        "cik": 811641,
        "title": "IMMUCELL CORP /DE/"
    },
    "EGF": {
        "cik": 1336050,
        "title": "BlackRock Enhanced Government Fund, Inc."
    },
    "AZREF": {
        "cik": 1633438,
        "title": "Azure Power Global Ltd"
    },
    "CPSH": {
        "cik": 814676,
        "title": "CPS TECHNOLOGIES CORP/DE/"
    },
    "MNDO": {
        "cik": 1119083,
        "title": "MIND CTI LTD"
    },
    "AGLE": {
        "cik": 1636282,
        "title": "Aeglea BioTherapeutics, Inc."
    },
    "WWR": {
        "cik": 839470,
        "title": "WESTWATER RESOURCES, INC."
    },
    "WHLR": {
        "cik": 1527541,
        "title": "Wheeler Real Estate Investment Trust, Inc."
    },
    "NM": {
        "cik": 1333172,
        "title": "Navios Maritime Holdings Inc."
    },
    "CODX": {
        "cik": 1692415,
        "title": "Co-Diagnostics, Inc."
    },
    "USEG": {
        "cik": 101594,
        "title": "US ENERGY CORP"
    },
    "GSTX": {
        "cik": 1497649,
        "title": "Graphene & Solar Technologies Ltd"
    },
    "BLTH": {
        "cik": 1487718,
        "title": "AMERICAN BATTERY MATERIALS, INC."
    },
    "SYBX": {
        "cik": 1527599,
        "title": "SYNLOGIC, INC."
    },
    "FSEA": {
        "cik": 1943802,
        "title": "First Seacoast Bancorp, Inc."
    },
    "MLYF": {
        "cik": 1801762,
        "title": "Western Magnesium Corp."
    },
    "CHCI": {
        "cik": 1299969,
        "title": "Comstock Holding Companies, Inc."
    },
    "RAIN": {
        "cik": 1724979,
        "title": "Rain Oncology Inc."
    },
    "ICCT": {
        "cik": 1408057,
        "title": "iCoreConnect Inc."
    },
    "BTM": {
        "cik": 1901799,
        "title": "Bitcoin Depot Inc."
    },
    "LNSR": {
        "cik": 1320350,
        "title": "LENSAR, Inc."
    },
    "FATP": {
        "cik": 1865045,
        "title": "FAT PROJECTS ACQUISITION CORP"
    },
    "BYSI": {
        "cik": 1677940,
        "title": "BeyondSpring Inc."
    },
    "RWLK": {
        "cik": 1607962,
        "title": "ReWalk Robotics Ltd."
    },
    "KTEL": {
        "cik": 845819,
        "title": "KonaTel, Inc."
    },
    "AITX": {
        "cik": 1498148,
        "title": "Artificial Intelligence Technology Solutions Inc."
    },
    "SGMA": {
        "cik": 915358,
        "title": "SIGMATRON INTERNATIONAL INC"
    },
    "MTNB": {
        "cik": 1582554,
        "title": "Matinas BioPharma Holdings, Inc."
    },
    "PBBK": {
        "cik": 1849670,
        "title": "PB Bankshares, Inc."
    },
    "APWC": {
        "cik": 1026980,
        "title": "ASIA PACIFIC WIRE & CABLE CORP LTD"
    },
    "BIMT": {
        "cik": 1678848,
        "title": "CAMBELL INTERNATIONAL HOLDING CORP."
    },
    "PYYX": {
        "cik": 939930,
        "title": "PYXUS INTERNATIONAL, INC."
    },
    "UURAF": {
        "cik": 1495651,
        "title": "Ucore Rare Metals Inc."
    },
    "BWVI": {
        "cik": 1310291,
        "title": "PSYCHECEUTICAL BIOSCIENCE, INC."
    },
    "SNCE": {
        "cik": 1819113,
        "title": "Science 37 Holdings, Inc."
    },
    "FGNV": {
        "cik": 1687919,
        "title": "FORGE INNOVATION DEVELOPMENT CORP."
    },
    "POCI": {
        "cik": 867840,
        "title": "PRECISION OPTICS CORPORATION, INC."
    },
    "DGHI": {
        "cik": 1854368,
        "title": "Digihost Technology Inc."
    },
    "WBQNL": {
        "cik": 1785494,
        "title": "Woodbridge Liquidation Trust"
    },
    "LIZI": {
        "cik": 1783407,
        "title": "LIZHI INC."
    },
    "AAME": {
        "cik": 8177,
        "title": "ATLANTIC AMERICAN CORP"
    },
    "ACAX": {
        "cik": 1897245,
        "title": "Alset Capital Acquisition Corp."
    },
    "EIGR": {
        "cik": 1305253,
        "title": "Eiger BioPharmaceuticals, Inc."
    },
    "ACHL": {
        "cik": 1830749,
        "title": "Achilles Therapeutics plc"
    },
    "OMIC": {
        "cik": 1850906,
        "title": "Singular Genomics Systems, Inc."
    },
    "VMAR": {
        "cik": 1813783,
        "title": "Vision Marine Technologies Inc."
    },
    "EVGN": {
        "cik": 1574565,
        "title": "Evogene Ltd."
    },
    "ZNOG": {
        "cik": 1131312,
        "title": "ZION OIL & GAS INC"
    },
    "LITM": {
        "cik": 1769697,
        "title": "Snow Lake Resources Ltd."
    },
    "QNTO": {
        "cik": 1391933,
        "title": "QUAINT OAK BANCORP INC"
    },
    "JANL": {
        "cik": 1133062,
        "title": "JANEL CORP"
    },
    "HSTI": {
        "cik": 1365388,
        "title": "High Sierra Technologies, Inc."
    },
    "OWLT": {
        "cik": 1816708,
        "title": "Owlet, Inc."
    },
    "SFRX": {
        "cik": 1106213,
        "title": "SEAFARER EXPLORATION CORP"
    },
    "ZENV": {
        "cik": 1836934,
        "title": "Zenvia Inc."
    },
    "USAU": {
        "cik": 27093,
        "title": "U.S. GOLD CORP."
    },
    "SUNW": {
        "cik": 1172631,
        "title": "Sunworks, Inc."
    },
    "TLF": {
        "cik": 909724,
        "title": "TANDY LEATHER FACTORY INC"
    },
    "TRBMF": {
        "cik": 1406944,
        "title": "TORQ RESOURCES INC."
    },
    "OSS": {
        "cik": 1394056,
        "title": "ONE STOP SYSTEMS, INC."
    },
    "GAME": {
        "cik": 1714562,
        "title": "GameSquare Holdings, Inc."
    },
    "NASO": {
        "cik": 1398172,
        "title": "Naples Soap Company, Inc."
    },
    "TCRT": {
        "cik": 1107421,
        "title": "Alaunos Therapeutics, Inc."
    },
    "MIRO": {
        "cik": 1527096,
        "title": "Miromatrix Medical Inc."
    },
    "DUOT": {
        "cik": 1396536,
        "title": "DUOS TECHNOLOGIES GROUP, INC."
    },
    "CVVUF": {
        "cik": 1023109,
        "title": "CANALASKA URANIUM LTD"
    },
    "RAND": {
        "cik": 81955,
        "title": "RAND CAPITAL CORP"
    },
    "NICK": {
        "cik": 1000045,
        "title": "NICHOLAS FINANCIAL INC"
    },
    "UP": {
        "cik": 1819516,
        "title": "Wheels Up Experience Inc."
    },
    "AMAO": {
        "cik": 1843656,
        "title": "American Acquisition Opportunity Inc."
    },
    "LONCF": {
        "cik": 1472619,
        "title": "Loncor Gold Inc."
    },
    "HCNWF": {
        "cik": 1887603,
        "title": "Hypercharge Networks Corp."
    },
    "GRF": {
        "cik": 850027,
        "title": "EAGLE CAPITAL GROWTH FUND, INC."
    },
    "INIS": {
        "cik": 1038277,
        "title": "INTERNATIONAL ISOTOPES INC"
    },
    "KIRK": {
        "cik": 1056285,
        "title": "KIRKLAND'S, INC"
    },
    "UG": {
        "cik": 101295,
        "title": "UNITED GUARDIAN INC"
    },
    "UBX": {
        "cik": 1463361,
        "title": "Unity Biotechnology, Inc."
    },
    "ASLN": {
        "cik": 1722926,
        "title": "ASLAN Pharmaceuticals Ltd"
    },
    "OMH": {
        "cik": 1944902,
        "title": "Ohmyhome Ltd"
    },
    "DRTT": {
        "cik": 1340476,
        "title": "DIRTT ENVIRONMENTAL SOLUTIONS LTD"
    },
    "PYN": {
        "cik": 1181505,
        "title": "PIMCO NEW YORK MUNICIPAL INCOME FUND III"
    },
    "SSVFF": {
        "cik": 1397616,
        "title": "SOUTHERN SILVER EXPLORATION CORP"
    },
    "AIH": {
        "cik": 1757143,
        "title": "Aesthetic Medical International Holdings Group Ltd"
    },
    "INDO": {
        "cik": 1757840,
        "title": "Indonesia Energy Corp Ltd"
    },
    "PHUN": {
        "cik": 1665300,
        "title": "Phunware, Inc."
    },
    "KRKR": {
        "cik": 1779476,
        "title": "36Kr Holdings Inc."
    },
    "DERM": {
        "cik": 1867066,
        "title": "Journey Medical Corp"
    },
    "XPON": {
        "cik": 1894954,
        "title": "Expion360 Inc."
    },
    "CGA": {
        "cik": 857949,
        "title": "China Green Agriculture, Inc."
    },
    "KOSS": {
        "cik": 56701,
        "title": "KOSS CORP"
    },
    "PNBK": {
        "cik": 1098146,
        "title": "PATRIOT NATIONAL BANCORP INC"
    },
    "COYA": {
        "cik": 1835022,
        "title": "Coya Therapeutics, Inc."
    },
    "INAB": {
        "cik": 1740279,
        "title": "IN8BIO, INC."
    },
    "EVTV": {
        "cik": 1563568,
        "title": "Envirotech Vehicles, Inc."
    },
    "MSCLF": {
        "cik": 1421642,
        "title": "Satellos Bioscience Inc."
    },
    "JETMF": {
        "cik": 1846084,
        "title": "Global Crossing Airlines Group Inc."
    },
    "RVP": {
        "cik": 946563,
        "title": "RETRACTABLE TECHNOLOGIES INC"
    },
    "PHXM": {
        "cik": 1624422,
        "title": "PHAXIAM Therapeutics S.A."
    },
    "FRCB": {
        "cik": 1132979,
        "title": "FIRST REPUBLIC BANK"
    },
    "JFU": {
        "cik": 1619544,
        "title": "9F Inc."
    },
    "CADL": {
        "cik": 1841387,
        "title": "Candel Therapeutics, Inc."
    },
    "FTEK": {
        "cik": 846913,
        "title": "FUEL TECH, INC."
    },
    "XXII": {
        "cik": 1347858,
        "title": "22nd Century Group, Inc."
    },
    "AVHI": {
        "cik": 1844507,
        "title": "Achari Ventures Holdings Corp. I"
    },
    "FSI": {
        "cik": 1069394,
        "title": "FLEXIBLE SOLUTIONS INTERNATIONAL INC"
    },
    "RMCF": {
        "cik": 1616262,
        "title": "Rocky Mountain Chocolate Factory, Inc."
    },
    "XELB": {
        "cik": 1083220,
        "title": "XCel Brands, Inc."
    },
    "DRCT": {
        "cik": 1880613,
        "title": "Direct Digital Holdings, Inc."
    },
    "AGAE": {
        "cik": 1708341,
        "title": "Allied Gaming & Entertainment Inc."
    },
    "PRKA": {
        "cik": 1297937,
        "title": "PARKS AMERICA, INC"
    },
    "UGEIF": {
        "cik": 1638298,
        "title": "UGE International Ltd."
    },
    "KALA": {
        "cik": 1479419,
        "title": "KALA BIO, Inc."
    },
    "NLTX": {
        "cik": 1404644,
        "title": "Neoleukin Therapeutics, Inc."
    },
    "UTSI": {
        "cik": 1030471,
        "title": "UTSTARCOM HOLDINGS CORP."
    },
    "SBEV": {
        "cik": 1553788,
        "title": "SPLASH BEVERAGE GROUP, INC."
    },
    "DAIO": {
        "cik": 351998,
        "title": "DATA I/O CORP"
    },
    "NOWG": {
        "cik": 1761911,
        "title": "Nowigence Inc."
    },
    "ASPA": {
        "cik": 1854583,
        "title": "Abri SPAC I, Inc."
    },
    "RETO": {
        "cik": 1687277,
        "title": "ReTo Eco-Solutions, Inc."
    },
    "VNCE": {
        "cik": 1579157,
        "title": "VINCE HOLDING CORP."
    },
    "RLFTY": {
        "cik": 1854078,
        "title": "Relief Therapeutics Holding SA"
    },
    "WKEY": {
        "cik": 1738699,
        "title": "Wisekey International Holding S.A."
    },
    "KBLB": {
        "cik": 1413119,
        "title": "Kraig Biocraft Laboratories, Inc"
    },
    "VICP": {
        "cik": 1468639,
        "title": "Vicapsys Life Sciences, Inc."
    },
    "HTOO": {
        "cik": 1819794,
        "title": "Fusion Fuel Green PLC"
    },
    "SATX": {
        "cik": 1915403,
        "title": "SatixFy Communications Ltd."
    },
    "UPC": {
        "cik": 1809616,
        "title": "Universe Pharmaceuticals INC"
    },
    "MMV": {
        "cik": 1874074,
        "title": "MultiMetaVerse Holdings Ltd"
    },
    "DSS": {
        "cik": 771999,
        "title": "DSS, INC."
    },
    "IMMX": {
        "cik": 1873835,
        "title": "Immix Biopharma, Inc."
    },
    "CWBHF": {
        "cik": 1750155,
        "title": "Charlotte's Web Holdings, Inc."
    },
    "FGH": {
        "cik": 946454,
        "title": "FG Group Holdings Inc."
    },
    "NGLD": {
        "cik": 1605481,
        "title": "Nevada Canyon Gold Corp."
    },
    "SPI": {
        "cik": 1210618,
        "title": "SPI Energy Co., Ltd."
    },
    "NLS": {
        "cik": 1078207,
        "title": "NAUTILUS, INC."
    },
    "ARVL": {
        "cik": 1835059,
        "title": "Arrival"
    },
    "PATI": {
        "cik": 1616741,
        "title": "PATRIOT TRANSPORTATION HOLDING, INC."
    },
    "IZEA": {
        "cik": 1495231,
        "title": "IZEA Worldwide, Inc."
    },
    "INUV": {
        "cik": 829323,
        "title": "Inuvo, Inc."
    },
    "SAI": {
        "cik": 1847075,
        "title": "SAI.TECH Global Corp"
    },
    "ADN": {
        "cik": 1744494,
        "title": "ADVENT TECHNOLOGIES HOLDINGS, INC."
    },
    "ELDN": {
        "cik": 1404281,
        "title": "Eledon Pharmaceuticals, Inc."
    },
    "VIAO": {
        "cik": 1769116,
        "title": "VIA optronics AG"
    },
    "ALPP": {
        "cik": 1606698,
        "title": "ALPINE 4 HOLDINGS, INC."
    },
    "IGXT": {
        "cik": 1098880,
        "title": "IntelGenx Technologies Corp."
    },
    "AWRE": {
        "cik": 1015739,
        "title": "AWARE INC /MA/"
    },
    "GFAI": {
        "cik": 1804469,
        "title": "Guardforce AI Co., Ltd."
    },
    "GSMG": {
        "cik": 1738758,
        "title": "GLORY STAR NEW MEDIA GROUP HOLDINGS Ltd"
    },
    "PIAC": {
        "cik": 845385,
        "title": "PRINCETON CAPITAL CORP"
    },
    "CLAY": {
        "cik": 1855467,
        "title": "Chavant Capital Acquisition Corp."
    },
    "AIM": {
        "cik": 946644,
        "title": "AIM ImmunoTech Inc."
    },
    "INFT": {
        "cik": 1962911,
        "title": "Infinity Bancorp"
    },
    "IQST": {
        "cik": 1527702,
        "title": "iQSTEL Inc"
    },
    "ARMV": {
        "cik": 1625285,
        "title": "Arma Services Inc"
    },
    "DWNX": {
        "cik": 927719,
        "title": "DELHI BANK CORP"
    },
    "BBGI": {
        "cik": 1099160,
        "title": "BEASLEY BROADCAST GROUP INC"
    },
    "CXXIF": {
        "cik": 831609,
        "title": "C21 Investments Inc."
    },
    "CIF": {
        "cik": 833021,
        "title": "MFS INTERMEDIATE HIGH INCOME FUND"
    },
    "MPAD": {
        "cik": 65759,
        "title": "MICROPAC INDUSTRIES INC"
    },
    "ATIP": {
        "cik": 1815849,
        "title": "ATI Physical Therapy, Inc."
    },
    "IPDN": {
        "cik": 1546296,
        "title": "Professional Diversity Network, Inc."
    },
    "HLRTF": {
        "cik": 1418149,
        "title": "Hillcrest Energy Technologies Ltd."
    },
    "GRUSF": {
        "cik": 1463000,
        "title": "Grown Rogue International Inc."
    },
    "BRST": {
        "cik": 764897,
        "title": "Broad Street Realty, Inc."
    },
    "QDMI": {
        "cik": 1094032,
        "title": "QDM International Inc."
    },
    "CACO": {
        "cik": 1928948,
        "title": "Caravelle International Group"
    },
    "OOGI": {
        "cik": 1160798,
        "title": "C2E ENERGY, INC."
    },
    "BMTX": {
        "cik": 1725872,
        "title": "BM Technologies, Inc."
    },
    "PGTK": {
        "cik": 1553404,
        "title": "Pacific Green Technologies Inc."
    },
    "ARRKF": {
        "cik": 1855743,
        "title": "ARRAS MINERALS CORP."
    },
    "XITO": {
        "cik": 1651932,
        "title": "Xenous Holdings, Inc."
    },
    "BCTF": {
        "cik": 1668340,
        "title": "Bancorp 34, Inc."
    },
    "ACHN": {
        "cik": 1672571,
        "title": "Antiaging Quantum Living Inc."
    },
    "MRM": {
        "cik": 1819704,
        "title": "Medirom Healthcare Technologies Inc."
    },
    "SCTC": {
        "cik": 1577445,
        "title": "Odysight.ai Inc."
    },
    "SDIG": {
        "cik": 1856028,
        "title": "Stronghold Digital Mining, Inc."
    },
    "SIEN": {
        "cik": 1551693,
        "title": "Sientra, Inc."
    },
    "CRBP": {
        "cik": 1595097,
        "title": "Corbus Pharmaceuticals Holdings, Inc."
    },
    "ANGH": {
        "cik": 1871983,
        "title": "Anghami Inc"
    },
    "IVFH": {
        "cik": 312257,
        "title": "INNOVATIVE FOOD HOLDINGS INC"
    },
    "CASI": {
        "cik": 1962738,
        "title": "CASI Pharmaceuticals, Inc."
    },
    "CNTG": {
        "cik": 1757097,
        "title": "Centogene N.V."
    },
    "STRC": {
        "cik": 1826681,
        "title": "Sarcos Technology & Robotics Corp"
    },
    "ALIM": {
        "cik": 1267602,
        "title": "ALIMERA SCIENCES INC"
    },
    "LISMF": {
        "cik": 1643715,
        "title": "LITHIUM SOUTH DEVELOPMENT Corp"
    },
    "HGTXU": {
        "cik": 862022,
        "title": "HUGOTON ROYALTY TRUST"
    },
    "WSTRF": {
        "cik": 1621906,
        "title": "Western Uranium & Vanadium Corp."
    },
    "AGE": {
        "cik": 1708599,
        "title": "AgeX Therapeutics, Inc."
    },
    "QYOUF": {
        "cik": 1650287,
        "title": "QYOU Media Inc."
    },
    "MAPPF": {
        "cik": 1493130,
        "title": "PROSTAR HOLDINGS INC. /BC"
    },
    "CISO": {
        "cik": 1777319,
        "title": "CISO Global, Inc."
    },
    "WVVI": {
        "cik": 838875,
        "title": "WILLAMETTE VALLEY VINEYARDS INC"
    },
    "BEDU": {
        "cik": 1696355,
        "title": "Bright Scholar Education Holdings Ltd"
    },
    "MSVB": {
        "cik": 1734875,
        "title": "Mid-Southern Bancorp, Inc."
    },
    "MFV": {
        "cik": 856128,
        "title": "MFS SPECIAL VALUE TRUST"
    },
    "SDPI": {
        "cik": 1600422,
        "title": "Superior Drilling Products, Inc."
    },
    "AINC": {
        "cik": 1604738,
        "title": "Ashford Inc."
    },
    "ABIO": {
        "cik": 907654,
        "title": "ARCA biopharma, Inc."
    },
    "EQ": {
        "cik": 1746466,
        "title": "Equillium, Inc."
    },
    "QIND": {
        "cik": 1393781,
        "title": "Quality Industrial Corp."
    },
    "CRVW": {
        "cik": 1377149,
        "title": "CareView Communications Inc"
    },
    "FRSX": {
        "cik": 1691221,
        "title": "Foresight Autonomous Holdings Ltd."
    },
    "HARP": {
        "cik": 1708493,
        "title": "Harpoon Therapeutics, Inc."
    },
    "QLI": {
        "cik": 1779578,
        "title": "Qilian International Holding Group Ltd"
    },
    "OZSC": {
        "cik": 1679817,
        "title": "OZOP ENERGY SOLUTIONS, INC."
    },
    "NEON": {
        "cik": 87050,
        "title": "Neonode Inc."
    },
    "ATER": {
        "cik": 1757715,
        "title": "Aterian, Inc."
    },
    "MCAG": {
        "cik": 1859035,
        "title": "Mountain Crest Acquisition Corp. V"
    },
    "ALZN": {
        "cik": 1677077,
        "title": "Alzamend Neuro, Inc."
    },
    "RAVE": {
        "cik": 718332,
        "title": "RAVE RESTAURANT GROUP, INC."
    },
    "BTCM": {
        "cik": 1517496,
        "title": "BIT Mining Ltd"
    },
    "NNUP": {
        "cik": 888981,
        "title": "NOCOPI TECHNOLOGIES INC/MD/"
    },
    "SHMP": {
        "cik": 1465470,
        "title": "NaturalShrimp Inc"
    },
    "ZCMD": {
        "cik": 1785566,
        "title": "Zhongchao Inc."
    },
    "UNCY": {
        "cik": 1766140,
        "title": "Unicycive Therapeutics, Inc."
    },
    "GTIM": {
        "cik": 825324,
        "title": "Good Times Restaurants Inc."
    },
    "VBIV": {
        "cik": 764195,
        "title": "VBI Vaccines Inc/BC"
    },
    "PLUR": {
        "cik": 1158780,
        "title": "Pluri Inc."
    },
    "UPXI": {
        "cik": 1775194,
        "title": "UPEXI, INC."
    },
    "MMNFF": {
        "cik": 1776932,
        "title": "MedMen Enterprises, Inc."
    },
    "TGEN": {
        "cik": 1537435,
        "title": "TECOGEN INC."
    },
    "PPBT": {
        "cik": 1614744,
        "title": "PURPLE BIOTECH LTD."
    },
    "TRIB": {
        "cik": 888721,
        "title": "TRINITY BIOTECH PLC"
    },
    "JUPW": {
        "cik": 1760903,
        "title": "Jupiter Wellness, Inc."
    },
    "SNTI": {
        "cik": 1854270,
        "title": "Senti Biosciences, Inc."
    },
    "OCC": {
        "cik": 1000230,
        "title": "OPTICAL CABLE CORP"
    },
    "GNPX": {
        "cik": 1595248,
        "title": "Genprex, Inc."
    },
    "SNT": {
        "cik": 896494,
        "title": "SENSTAR TECHNOLOGIES LTD."
    },
    "ANLDF": {
        "cik": 1519469,
        "title": "ANFIELD ENERGY INC."
    },
    "OCX": {
        "cik": 1642380,
        "title": "Oncocyte Corp"
    },
    "MXC": {
        "cik": 66418,
        "title": "MEXCO ENERGY CORP"
    },
    "BRQS": {
        "cik": 1650575,
        "title": "Borqs Technologies, Inc."
    },
    "SVT": {
        "cik": 89140,
        "title": "SERVOTRONICS INC /DE/"
    },
    "SCND": {
        "cik": 87802,
        "title": "SCIENTIFIC INDUSTRIES INC"
    },
    "APTO": {
        "cik": 882361,
        "title": "Aptose Biosciences Inc."
    },
    "XTGRF": {
        "cik": 1288770,
        "title": "XTRA-GOLD RESOURCES CORP"
    },
    "HEPA": {
        "cik": 1583771,
        "title": "Hepion Pharmaceuticals, Inc."
    },
    "PUBC": {
        "cik": 1575858,
        "title": "PureBase Corp"
    },
    "DOGZ": {
        "cik": 1707303,
        "title": "Dogness (International) Corp"
    },
    "PAVS": {
        "cik": 1751876,
        "title": "Paranovus Entertainment Technology Ltd."
    },
    "GUER": {
        "cik": 1832487,
        "title": "Guerrilla RF, Inc."
    },
    "GREE": {
        "cik": 1844971,
        "title": "Greenidge Generation Holdings Inc."
    },
    "SOBR": {
        "cik": 1425627,
        "title": "SOBR Safe, Inc."
    },
    "CWD": {
        "cik": 1627282,
        "title": "CaliberCos Inc."
    },
    "NVOS": {
        "cik": 1138978,
        "title": "Novo Integrated Sciences, Inc."
    },
    "LIFD": {
        "cik": 1391135,
        "title": "LFTD PARTNERS INC."
    },
    "AZTR": {
        "cik": 1701478,
        "title": "Azitra Inc"
    },
    "SNSE": {
        "cik": 1829802,
        "title": "Sensei Biotherapeutics, Inc."
    },
    "CRMZ": {
        "cik": 315958,
        "title": "CREDITRISKMONITOR COM INC"
    },
    "GWSO": {
        "cik": 1430300,
        "title": "Global Warming Solutions, Inc."
    },
    "LMNL": {
        "cik": 1351172,
        "title": "Liminal BioSciences Inc."
    },
    "NLSP": {
        "cik": 1783036,
        "title": "NLS Pharmaceutics Ltd."
    },
    "QMCI": {
        "cik": 1101433,
        "title": "QUOTEMEDIA INC"
    },
    "VHC": {
        "cik": 1082324,
        "title": "VirnetX Holding Corp"
    },
    "OPTT": {
        "cik": 1378140,
        "title": "Ocean Power Technologies, Inc."
    },
    "COCP": {
        "cik": 1412486,
        "title": "Cocrystal Pharma, Inc."
    },
    "CAMP": {
        "cik": 730255,
        "title": "CalAmp Corp."
    },
    "OSBK": {
        "cik": 1076691,
        "title": "OCONEE FINANCIAL CORP"
    },
    "PMD": {
        "cik": 806517,
        "title": "PSYCHEMEDICS CORP"
    },
    "MODD": {
        "cik": 1074871,
        "title": "Modular Medical, Inc."
    },
    "CDBMF": {
        "cik": 1545634,
        "title": "Cordoba Minerals Corp."
    },
    "MEGL": {
        "cik": 1881472,
        "title": "Magic Empire Global Ltd"
    },
    "ILUS": {
        "cik": 1496383,
        "title": "Ilustrato Pictures International Inc."
    },
    "RSRV": {
        "cik": 83350,
        "title": "RESERVE PETROLEUM CO"
    },
    "OCEL": {
        "cik": 1557376,
        "title": "Organicell Regenerative Medicine, Inc."
    },
    "TRT": {
        "cik": 732026,
        "title": "TRIO-TECH INTERNATIONAL"
    },
    "EVAX": {
        "cik": 1828253,
        "title": "Evaxion Biotech A/S"
    },
    "BRN": {
        "cik": 10048,
        "title": "BARNWELL INDUSTRIES INC"
    },
    "NSYS": {
        "cik": 722313,
        "title": "NORTECH SYSTEMS INC"
    },
    "SGRP": {
        "cik": 1004989,
        "title": "SPAR Group, Inc."
    },
    "LPTX": {
        "cik": 1509745,
        "title": "LEAP THERAPEUTICS, INC."
    },
    "NTRB": {
        "cik": 1676047,
        "title": "NutriBand Inc."
    },
    "CTHR": {
        "cik": 1015155,
        "title": "CHARLES & COLVARD LTD"
    },
    "TARA": {
        "cik": 1359931,
        "title": "Protara Therapeutics, Inc."
    },
    "KAVL": {
        "cik": 1762239,
        "title": "Kaival Brands Innovations Group, Inc."
    },
    "NTWK": {
        "cik": 1039280,
        "title": "NETSOL TECHNOLOGIES INC"
    },
    "PIRS": {
        "cik": 1583648,
        "title": "PIERIS PHARMACEUTICALS, INC."
    },
    "MDNA": {
        "cik": 1807983,
        "title": "Medicenna Therapeutics Corp."
    },
    "SRNW": {
        "cik": 1321517,
        "title": "Stratos Renewables Corp"
    },
    "OAKV": {
        "cik": 1865429,
        "title": "Oak View Bankshares, Inc."
    },
    "BRFH": {
        "cik": 1487197,
        "title": "BARFRESH FOOD GROUP INC."
    },
    "XELA": {
        "cik": 1620179,
        "title": "Exela Technologies, Inc."
    },
    "CTGL": {
        "cik": 1498067,
        "title": "CITRINE GLOBAL, CORP."
    },
    "LGL": {
        "cik": 61004,
        "title": "LGL GROUP INC"
    },
    "BBOP": {
        "cik": 1814102,
        "title": "BeBop Channel Corp"
    },
    "MAIA": {
        "cik": 1878313,
        "title": "MAIA Biotechnology, Inc."
    },
    "CCLD": {
        "cik": 1582982,
        "title": "CareCloud, Inc."
    },
    "ICLK": {
        "cik": 1697818,
        "title": "iClick Interactive Asia Group Ltd"
    },
    "PETV": {
        "cik": 1512922,
        "title": "PetVivo Holdings, Inc."
    },
    "JEWL": {
        "cik": 1884072,
        "title": "Adamas One Corp."
    },
    "MOBQ": {
        "cik": 1084267,
        "title": "Mobiquity Technologies, Inc."
    },
    "BHLL": {
        "cik": 1407583,
        "title": "Bunker Hill Mining Corp."
    },
    "EMKR": {
        "cik": 808326,
        "title": "EMCORE CORP"
    },
    "PTN": {
        "cik": 911216,
        "title": "PALATIN TECHNOLOGIES INC"
    },
    "OILY": {
        "cik": 1367408,
        "title": "Sino American Oil Co"
    },
    "LOCL": {
        "cik": 1840780,
        "title": "Local Bounti Corporation/DE"
    },
    "MNTS": {
        "cik": 1781162,
        "title": "Momentus Inc."
    },
    "CUBA": {
        "cik": 880406,
        "title": "HERZFELD CARIBBEAN BASIN FUND INC"
    },
    "TEDU": {
        "cik": 1592560,
        "title": "Tarena International, Inc."
    },
    "ZDGE": {
        "cik": 1667313,
        "title": "Zedge, Inc."
    },
    "NCTY": {
        "cik": 1296774,
        "title": "The9 LTD"
    },
    "VIVC": {
        "cik": 1703073,
        "title": "VIVIC CORP."
    },
    "AGXPF": {
        "cik": 1482436,
        "title": "SILVER X MINING CORP."
    },
    "CPIX": {
        "cik": 1087294,
        "title": "CUMBERLAND PHARMACEUTICALS INC"
    },
    "HWTR": {
        "cik": 1144546,
        "title": "HFactor, Inc."
    },
    "LEJU": {
        "cik": 1596856,
        "title": "Leju Holdings Ltd"
    },
    "ACXP": {
        "cik": 1736243,
        "title": "Acurx Pharmaceuticals, Inc."
    },
    "AKOM": {
        "cik": 1590496,
        "title": "Aerkomm Inc."
    },
    "CRYM": {
        "cik": 1533030,
        "title": "Cryomass Technologies, Inc."
    },
    "INVO": {
        "cik": 1417926,
        "title": "INVO Bioscience, Inc."
    },
    "RXMD": {
        "cik": 1402945,
        "title": "Progressive Care Inc."
    },
    "BSEM": {
        "cik": 1658678,
        "title": "BIOSTEM TECHNOLOGIES"
    },
    "GLGI": {
        "cik": 1088413,
        "title": "GREYSTONE LOGISTICS, INC."
    },
    "WRNT": {
        "cik": 1900564,
        "title": "WARRANTEE INC."
    },
    "COEP": {
        "cik": 1759186,
        "title": "Coeptis Therapeutics Holdings, Inc."
    },
    "CIPI": {
        "cik": 1108645,
        "title": "Correlate Energy Corp."
    },
    "LGIQ": {
        "cik": 1335112,
        "title": "LOGIQ, INC."
    },
    "MBIO": {
        "cik": 1680048,
        "title": "MUSTANG BIO, INC."
    },
    "MHUBF": {
        "cik": 1869137,
        "title": "MineHub Technologies Inc."
    },
    "UNXP": {
        "cik": 1751707,
        "title": "United Express Inc."
    },
    "MBOT": {
        "cik": 883975,
        "title": "Microbot Medical Inc."
    },
    "HTCR": {
        "cik": 1892322,
        "title": "HeartCore Enterprises, Inc."
    },
    "ELBM": {
        "cik": 1907184,
        "title": "Electra Battery Materials Corp"
    },
    "RGLS": {
        "cik": 1505512,
        "title": "Regulus Therapeutics Inc."
    },
    "VWFB": {
        "cik": 1913838,
        "title": "VWF Bancorp, Inc."
    },
    "AYRO": {
        "cik": 1086745,
        "title": "AYRO, Inc."
    },
    "DLPN": {
        "cik": 1282224,
        "title": "Dolphin Entertainment, Inc."
    },
    "IMUN": {
        "cik": 1559356,
        "title": "Immune Therapeutics, Inc."
    },
    "TOMZ": {
        "cik": 314227,
        "title": "TOMI Environmental Solutions, Inc."
    },
    "SNRG": {
        "cik": 1652539,
        "title": "SusGlobal Energy Corp."
    },
    "OPXS": {
        "cik": 1397016,
        "title": "Optex Systems Holdings Inc"
    },
    "ELWS": {
        "cik": 1944399,
        "title": "Earlyworks Co., Ltd."
    },
    "VIRI": {
        "cik": 1818844,
        "title": "Virios Therapeutics, Inc."
    },
    "MTBL": {
        "cik": 1509223,
        "title": "Moatable, Inc."
    },
    "FEDU": {
        "cik": 1709819,
        "title": "Four Seasons Education (Cayman) Inc."
    },
    "HMMR": {
        "cik": 1539680,
        "title": "HAMMER FIBER OPTICS HOLDINGS CORP"
    },
    "SSKN": {
        "cik": 1051514,
        "title": "STRATA Skin Sciences, Inc."
    },
    "BMR": {
        "cik": 1899005,
        "title": "Beamr Imaging Ltd."
    },
    "CLPS": {
        "cik": 1724542,
        "title": "CLPS Inc"
    },
    "PRSI": {
        "cik": 79661,
        "title": "PORTSMOUTH SQUARE INC"
    },
    "BSQR": {
        "cik": 1054721,
        "title": "BSQUARE CORP /WA"
    },
    "CHSN": {
        "cik": 1825349,
        "title": "Chanson International Holding"
    },
    "NOM": {
        "cik": 899782,
        "title": "NUVEEN MISSOURI QUALITY MUNICIPAL INCOME FUND"
    },
    "NMRD": {
        "cik": 1602078,
        "title": "Nemaura Medical Inc."
    },
    "CRCUF": {
        "cik": 868822,
        "title": "Canagold Resources Ltd."
    },
    "IPW": {
        "cik": 1830072,
        "title": "iPower Inc."
    },
    "SOWG": {
        "cik": 1490161,
        "title": "Sow Good Inc."
    },
    "PAVM": {
        "cik": 1624326,
        "title": "PAVmed Inc."
    },
    "EXDW": {
        "cik": 1634293,
        "title": "Exceed World, Inc."
    },
    "IDAI": {
        "cik": 1718939,
        "title": "T Stamp Inc"
    },
    "CYN": {
        "cik": 1874097,
        "title": "Cyngn Inc."
    },
    "AWH": {
        "cik": 926617,
        "title": "Aspira Women's Health Inc."
    },
    "SONM": {
        "cik": 1178697,
        "title": "SONIM TECHNOLOGIES INC"
    },
    "PNXLF": {
        "cik": 1689448,
        "title": "Argentina Lithium & Energy Corp."
    },
    "GBNY": {
        "cik": 1823365,
        "title": "Generations Bancorp NY, Inc."
    },
    "FAZE": {
        "cik": 1839360,
        "title": "FaZe Holdings Inc."
    },
    "ASRE": {
        "cik": 1231339,
        "title": "Astra Energy, Inc."
    },
    "FPAY": {
        "cik": 1397047,
        "title": "FlexShopper, Inc."
    },
    "NPLS": {
        "cik": 1781726,
        "title": "NP Life Sciences Health Industry Group Inc."
    },
    "JG": {
        "cik": 1737339,
        "title": "Aurora Mobile Ltd"
    },
    "MTEX": {
        "cik": 1056358,
        "title": "MANNATECH INC"
    },
    "UPH": {
        "cik": 1770141,
        "title": "UpHealth, Inc."
    },
    "SWAG": {
        "cik": 1872525,
        "title": "Stran & Company, Inc."
    },
    "GLBZ": {
        "cik": 890066,
        "title": "GLEN BURNIE BANCORP"
    },
    "JGLDF": {
        "cik": 1686000,
        "title": "Japan Gold Corp."
    },
    "LUMO": {
        "cik": 1126234,
        "title": "LUMOS PHARMA, INC."
    },
    "NIR": {
        "cik": 1826671,
        "title": "Near Intelligence, Inc."
    },
    "TAIT": {
        "cik": 942126,
        "title": "TAITRON COMPONENTS INC"
    },
    "CYTH": {
        "cik": 922247,
        "title": "Cyclo Therapeutics, Inc."
    },
    "BIXT": {
        "cik": 1445815,
        "title": "BIOXYTRAN, INC"
    },
    "KZIA": {
        "cik": 1075880,
        "title": "KAZIA THERAPEUTICS LTD"
    },
    "ECOR": {
        "cik": 1560258,
        "title": "electroCore, Inc."
    },
    "ORGS": {
        "cik": 1460602,
        "title": "Orgenesis Inc."
    },
    "ALID": {
        "cik": 1575295,
        "title": "Allied Corp."
    },
    "GTEC": {
        "cik": 1735041,
        "title": "Greenland Technologies Holding Corp."
    },
    "EWGFF": {
        "cik": 1518561,
        "title": "Eat Well Investment Group Inc."
    },
    "HWNI": {
        "cik": 1413891,
        "title": "HIGH WIRE NETWORKS, INC."
    },
    "USDP": {
        "cik": 1610682,
        "title": "USD Partners LP"
    },
    "RMSL": {
        "cik": 1412126,
        "title": "RemSleep Holdings Inc."
    },
    "CHUC": {
        "cik": 1134765,
        "title": "Charlie's Holdings, Inc."
    },
    "OPHC": {
        "cik": 1288855,
        "title": "OptimumBank Holdings, Inc."
    },
    "JT": {
        "cik": 1713923,
        "title": "Jianpu Technology Inc."
    },
    "PBSV": {
        "cik": 1304161,
        "title": "Pharma-Bio Serv, Inc."
    },
    "PHIL": {
        "cik": 704172,
        "title": "PHI GROUP INC"
    },
    "YJ": {
        "cik": 1759614,
        "title": "Yunji Inc."
    },
    "NRXP": {
        "cik": 1719406,
        "title": "NRX Pharmaceuticals, Inc."
    },
    "SODI": {
        "cik": 91668,
        "title": "SOLITRON DEVICES INC"
    },
    "LSTA": {
        "cik": 320017,
        "title": "LISATA THERAPEUTICS, INC."
    },
    "IRIX": {
        "cik": 1006045,
        "title": "IRIDEX CORP"
    },
    "LNBY": {
        "cik": 1672572,
        "title": "Landbay Inc"
    },
    "PFIN": {
        "cik": 75340,
        "title": "P&F INDUSTRIES INC"
    },
    "HANNF": {
        "cik": 1123267,
        "title": "Hannan Metals Ltd."
    },
    "EGSE": {
        "cik": 1527102,
        "title": "Evergreen Sustainable Enterprises, Inc."
    },
    "LPCN": {
        "cik": 1535955,
        "title": "Lipocine Inc."
    },
    "LICN": {
        "cik": 1876766,
        "title": "Lichen China Ltd"
    },
    "AZYO": {
        "cik": 1708527,
        "title": "AZIYO BIOLOGICS, INC."
    },
    "CBIO": {
        "cik": 1124105,
        "title": "CATALYST BIOSCIENCES, INC."
    },
    "SRRE": {
        "cik": 1083490,
        "title": "SUNRISE REAL ESTATE GROUP INC"
    },
    "IMPP": {
        "cik": 1876581,
        "title": "Imperial Petroleum Inc./Marshall Islands"
    },
    "IMVIQ": {
        "cik": 1734768,
        "title": "IMV Inc."
    },
    "DALN": {
        "cik": 1413898,
        "title": "DallasNews Corp"
    },
    "AUCUF": {
        "cik": 1813191,
        "title": "Inflection Resources Ltd."
    },
    "SCGY": {
        "cik": 1276531,
        "title": "SCIENTIFIC ENERGY, INC"
    },
    "SCIA": {
        "cik": 830616,
        "title": "SCI Engineered Materials, Inc."
    },
    "VYEY": {
        "cik": 700764,
        "title": "VICTORY OILFIELD TECH, INC."
    },
    "KDOZF": {
        "cik": 1318482,
        "title": "KIDOZ INC."
    },
    "TETOF": {
        "cik": 1783432,
        "title": "Tectonic Metals Inc."
    },
    "PMCB": {
        "cik": 1157075,
        "title": "PharmaCyte Biotech, Inc."
    },
    "DQWS": {
        "cik": 1652561,
        "title": "DSwiss Inc"
    },
    "SFT": {
        "cik": 1762322,
        "title": "SHIFT TECHNOLOGIES, INC."
    },
    "SPGX": {
        "cik": 1500305,
        "title": "Sustainable Projects Group Inc."
    },
    "BRLI": {
        "cik": 1787518,
        "title": "Brilliant Acquisition Corp"
    },
    "MEEC": {
        "cik": 728385,
        "title": "Midwest Energy Emissions Corp."
    },
    "EQS": {
        "cik": 878932,
        "title": "EQUUS TOTAL RETURN, INC."
    },
    "LCHD": {
        "cik": 1715433,
        "title": "Leader Capital Holdings Corp."
    },
    "PKKFF": {
        "cik": 1558924,
        "title": "Tenet Fintech Group Inc."
    },
    "USEA": {
        "cik": 1912847,
        "title": "United Maritime Corp"
    },
    "SMGI": {
        "cik": 1426506,
        "title": "SMG Industries Inc."
    },
    "LIQT": {
        "cik": 1307579,
        "title": "LIQTECH INTERNATIONAL INC"
    },
    "ACOR": {
        "cik": 1008848,
        "title": "Acorda Therapeutics, Inc."
    },
    "BREA": {
        "cik": 1939965,
        "title": "Brera Holdings PLC"
    },
    "CKX": {
        "cik": 352955,
        "title": "CKX LANDS, INC."
    },
    "HUSA": {
        "cik": 1156041,
        "title": "HOUSTON AMERICAN ENERGY CORP"
    },
    "BRVO": {
        "cik": 1444839,
        "title": "Bravo Multinational Inc."
    },
    "GURE": {
        "cik": 885462,
        "title": "GULF RESOURCES, INC."
    },
    "BOSC": {
        "cik": 1005516,
        "title": "BOS BETTER ONLINE SOLUTIONS LTD"
    },
    "FSRL": {
        "cik": 1172102,
        "title": "FIRST RELIANCE BANCSHARES INC"
    },
    "STLY": {
        "cik": 797465,
        "title": "HG Holdings, Inc."
    },
    "BMRA": {
        "cik": 73290,
        "title": "BIOMERICA INC"
    },
    "FTFT": {
        "cik": 1066923,
        "title": "Future FinTech Group Inc."
    },
    "BTCY": {
        "cik": 1630113,
        "title": "BIOTRICITY INC."
    },
    "INDP": {
        "cik": 1857044,
        "title": "Indaptus Therapeutics, Inc."
    },
    "SGBX": {
        "cik": 1023994,
        "title": "SAFE & GREEN HOLDINGS CORP."
    },
    "MGIH": {
        "cik": 1903995,
        "title": "Millennium Group International Holdings Ltd"
    },
    "BTTX": {
        "cik": 1832415,
        "title": "Better Therapeutics, Inc."
    },
    "HCTI": {
        "cik": 1839285,
        "title": "Healthcare Triangle, Inc."
    },
    "TRKA": {
        "cik": 1021096,
        "title": "Troika Media Group, Inc."
    },
    "SHFS": {
        "cik": 1854963,
        "title": "SHF Holdings, Inc."
    },
    "WLDS": {
        "cik": 1887673,
        "title": "Wearable Devices Ltd."
    },
    "STKH": {
        "cik": 1828098,
        "title": "Steakholder Foods Ltd."
    },
    "DRFS": {
        "cik": 1857910,
        "title": "Dr. Foods, Inc."
    },
    "WOWI": {
        "cik": 920990,
        "title": "METRO ONE TELECOMMUNICATIONS INC"
    },
    "OMQS": {
        "cik": 278165,
        "title": "OMNIQ Corp."
    },
    "CLRO": {
        "cik": 840715,
        "title": "CLEARONE INC"
    },
    "ILAG": {
        "cik": 1814963,
        "title": "Intelligent Living Application Group Inc."
    },
    "LCGMF": {
        "cik": 1339688,
        "title": "LION COPPER & GOLD CORP."
    },
    "ELEV": {
        "cik": 1783032,
        "title": "Elevation Oncology, Inc."
    },
    "SUND": {
        "cik": 1171838,
        "title": "Sundance Strategies, Inc."
    },
    "TBTC": {
        "cik": 1090396,
        "title": "TABLE TRAC INC"
    },
    "EUDA": {
        "cik": 1847846,
        "title": "EUDA Health Holdings Ltd"
    },
    "SSNT": {
        "cik": 1236275,
        "title": "SilverSun Technologies, Inc."
    },
    "GESI": {
        "cik": 1955083,
        "title": "General European Strategic Investments, Inc."
    },
    "MDJH": {
        "cik": 1741534,
        "title": "MDJM LTD"
    },
    "SALM": {
        "cik": 1050606,
        "title": "SALEM MEDIA GROUP, INC. /DE/"
    },
    "PT": {
        "cik": 1716338,
        "title": "Pintec Technology Holdings Ltd"
    },
    "QSEP": {
        "cik": 1103795,
        "title": "QS Energy, Inc."
    },
    "RDGL": {
        "cik": 1449349,
        "title": "VIVOS INC"
    },
    "SHPW": {
        "cik": 1784851,
        "title": "Shapeways Holdings, Inc."
    },
    "ZIVO": {
        "cik": 1101026,
        "title": "Zivo Bioscience, Inc."
    },
    "XWEL": {
        "cik": 1410428,
        "title": "XWELL, Inc."
    },
    "ENDI": {
        "cik": 1908984,
        "title": "ENDI Corp."
    },
    "SEED": {
        "cik": 1321851,
        "title": "Origin Agritech LTD"
    },
    "ARGC": {
        "cik": 1698702,
        "title": "ARION GROUP CORP."
    },
    "MGRX": {
        "cik": 1938046,
        "title": "MANGOCEUTICALS, INC."
    },
    "SFE": {
        "cik": 86115,
        "title": "SAFEGUARD SCIENTIFICS INC"
    },
    "SPFX": {
        "cik": 1807893,
        "title": "STANDARD PREMIUM FINANCE HOLDINGS, INC."
    },
    "ACRHF": {
        "cik": 1762359,
        "title": "Acreage Holdings, Inc."
    },
    "BMTM": {
        "cik": 1568385,
        "title": "Bright Mountain Media, Inc."
    },
    "BTTC": {
        "cik": 1066764,
        "title": "Bitech Technologies Corp"
    },
    "CLEV": {
        "cik": 1414382,
        "title": "Concrete Leveling Systems Inc"
    },
    "MXROF": {
        "cik": 1116548,
        "title": "MAX RESOURCE CORP."
    },
    "EDXC": {
        "cik": 1109486,
        "title": "Endexx Corp"
    },
    "FRLN": {
        "cik": 1810031,
        "title": "Freeline Therapeutics Holdings plc"
    },
    "AMPG": {
        "cik": 1518461,
        "title": "AmpliTech Group, Inc."
    },
    "DTST": {
        "cik": 1419951,
        "title": "Data Storage Corp"
    },
    "AUSI": {
        "cik": 826253,
        "title": "AURA SYSTEMS INC"
    },
    "RVLP": {
        "cik": 1739426,
        "title": "RVL Pharmaceuticals plc"
    },
    "VINC": {
        "cik": 1796129,
        "title": "Vincerx Pharma, Inc."
    },
    "SPRS": {
        "cik": 747540,
        "title": "SURGE COMPONENTS INC"
    },
    "GLBS": {
        "cik": 1499780,
        "title": "GLOBUS MARITIME LTD"
    },
    "TCJH": {
        "cik": 1938865,
        "title": "Top KingWin Ltd"
    },
    "DTSS": {
        "cik": 1631282,
        "title": "DATASEA INC."
    },
    "VIVK": {
        "cik": 1450704,
        "title": "Vivakor, Inc."
    },
    "OMHI": {
        "cik": 1403674,
        "title": "Portage Resources Inc."
    },
    "PALT": {
        "cik": 1355839,
        "title": "PALTALK, INC."
    },
    "MHHC": {
        "cik": 1826135,
        "title": "MHHC Enterprises Inc."
    },
    "CVR": {
        "cik": 19871,
        "title": "CHICAGO RIVET & MACHINE CO"
    },
    "TRNR": {
        "cik": 1785056,
        "title": "Interactive Strength, Inc."
    },
    "KA": {
        "cik": 1445283,
        "title": "KINETA, INC./DE"
    },
    "KINS": {
        "cik": 33992,
        "title": "KINGSTONE COMPANIES, INC."
    },
    "FBPI": {
        "cik": 1074543,
        "title": "FIRST BANCORP OF INDIANA INC"
    },
    "LKCO": {
        "cik": 1487839,
        "title": "Luokung Technology Corp."
    },
    "COSM": {
        "cik": 1474167,
        "title": "Cosmos Health Inc."
    },
    "FREQ": {
        "cik": 1703647,
        "title": "Frequency Therapeutics, Inc."
    },
    "CALC": {
        "cik": 1534133,
        "title": "CalciMedica, Inc."
    },
    "NMTC": {
        "cik": 1500198,
        "title": "NEUROONE MEDICAL TECHNOLOGIES Corp"
    },
    "BRCNF": {
        "cik": 1158399,
        "title": "Burcon NutraScience Corp"
    },
    "WHLM": {
        "cik": 1013706,
        "title": "Wilhelmina International, Inc."
    },
    "GEHI": {
        "cik": 1708441,
        "title": "Gravitas Education Holdings, Inc."
    },
    "ONCT": {
        "cik": 1260990,
        "title": "Oncternal Therapeutics, Inc."
    },
    "PSHG": {
        "cik": 1481241,
        "title": "Performance Shipping Inc."
    },
    "IGC": {
        "cik": 1326205,
        "title": "IGC Pharma, Inc."
    },
    "ADD": {
        "cik": 1747661,
        "title": "Color Star Technology Co., Ltd."
    },
    "UAVS": {
        "cik": 8504,
        "title": "AgEagle Aerial Systems Inc."
    },
    "SRZN": {
        "cik": 1824893,
        "title": "Surrozen, Inc./DE"
    },
    "EDTK": {
        "cik": 1782309,
        "title": "Skillful Craftsman Education Technology Ltd"
    },
    "EESH": {
        "cik": 1138867,
        "title": "EESTech, Inc."
    },
    "AVNI": {
        "cik": 1113313,
        "title": "ARVANA INC"
    },
    "INRD": {
        "cik": 719494,
        "title": "Inrad Optics, Inc."
    },
    "VEEE": {
        "cik": 1855509,
        "title": "Twin Vee PowerCats, Co."
    },
    "CFMS": {
        "cik": 1305773,
        "title": "Conformis Inc"
    },
    "CYCA": {
        "cik": 1383088,
        "title": "CYTTA CORP."
    },
    "NCRA": {
        "cik": 1756180,
        "title": "NOCERA, INC."
    },
    "YJGJ": {
        "cik": 1699709,
        "title": "YIJIA GROUP CORP."
    },
    "BFRG": {
        "cik": 1829247,
        "title": "BullFrog AI Holdings, Inc."
    },
    "BOXL": {
        "cik": 1624512,
        "title": "Boxlight Corp"
    },
    "BCDA": {
        "cik": 925741,
        "title": "BioCardia, Inc."
    },
    "UPYY": {
        "cik": 1677897,
        "title": "UPAY"
    },
    "EDSA": {
        "cik": 1540159,
        "title": "Edesa Biotech, Inc."
    },
    "UPTD": {
        "cik": 1844417,
        "title": "TradeUP Acquisition Corp."
    },
    "APDN": {
        "cik": 744452,
        "title": "APPLIED DNA SCIENCES INC"
    },
    "AMS": {
        "cik": 744825,
        "title": "AMERICAN SHARED HOSPITAL SERVICES"
    },
    "ENTX": {
        "cik": 1638097,
        "title": "Entera Bio Ltd."
    },
    "AAU": {
        "cik": 1015647,
        "title": "ALMADEN MINERALS LTD"
    },
    "FBRX": {
        "cik": 1419041,
        "title": "Forte Biosciences, Inc."
    },
    "RASP": {
        "cik": 1582249,
        "title": "Rasna Therapeutics Inc."
    },
    "ELYS": {
        "cik": 1080319,
        "title": "Elys Game Technology, Corp."
    },
    "POAI": {
        "cik": 1446159,
        "title": "Predictive Oncology Inc."
    },
    "FENG": {
        "cik": 1509646,
        "title": "Phoenix New Media Ltd"
    },
    "RNXT": {
        "cik": 1574094,
        "title": "RenovoRx, Inc."
    },
    "ACER": {
        "cik": 1069308,
        "title": "Acer Therapeutics Inc."
    },
    "CNFR": {
        "cik": 1502292,
        "title": "Conifer Holdings, Inc."
    },
    "ASTC": {
        "cik": 1001907,
        "title": "ASTROTECH Corp"
    },
    "DPLS": {
        "cik": 866439,
        "title": "DarkPulse, Inc."
    },
    "GOVB": {
        "cik": 1978811,
        "title": "Gouverneur Bancorp, Inc./MD/"
    },
    "MDIA": {
        "cik": 1784254,
        "title": "Mediaco Holding Inc."
    },
    "AGIL": {
        "cik": 1790625,
        "title": "AgileThought, Inc."
    },
    "ALRTF": {
        "cik": 1930419,
        "title": "ALR Technologies SG Ltd."
    },
    "CWPE": {
        "cik": 1741220,
        "title": "CW Petroleum Corp"
    },
    "IHT": {
        "cik": 82473,
        "title": "INNSUITES HOSPITALITY TRUST"
    },
    "POLA": {
        "cik": 1622345,
        "title": "Polar Power, Inc."
    },
    "BGLC": {
        "cik": 1737523,
        "title": "BioNexus Gene Lab Corp"
    },
    "NVGT": {
        "cik": 1089297,
        "title": "NOVAGANT CORP"
    },
    "EZFL": {
        "cik": 1817004,
        "title": "EzFill Holdings Inc"
    },
    "MBRX": {
        "cik": 1659617,
        "title": "Moleculin Biotech, Inc."
    },
    "HYEX": {
        "cik": 1630176,
        "title": "HEALTHY EXTRACTS INC."
    },
    "TPET": {
        "cik": 1898766,
        "title": "Trio Petroleum Corp."
    },
    "FAMI": {
        "cik": 1701261,
        "title": "Farmmi, Inc."
    },
    "NEPH": {
        "cik": 1196298,
        "title": "NEPHROS INC"
    },
    "JSDA": {
        "cik": 1083522,
        "title": "JONES SODA CO"
    },
    "OSA": {
        "cik": 1934064,
        "title": "ProSomnus, Inc."
    },
    "GEBRF": {
        "cik": 1570843,
        "title": "Greenbriar Capital Corp."
    },
    "MIGI": {
        "cik": 1218683,
        "title": "Mawson Infrastructure Group Inc."
    },
    "BHV": {
        "cik": 1169034,
        "title": "BLACKROCK VIRGINIA MUNICIPAL BOND TRUST"
    },
    "NNVC": {
        "cik": 1379006,
        "title": "NANOVIRICIDES, INC."
    },
    "SIF": {
        "cik": 90168,
        "title": "SIFCO INDUSTRIES INC"
    },
    "GFGSF": {
        "cik": 1684888,
        "title": "GFG Resources Inc."
    },
    "ONTX": {
        "cik": 1130598,
        "title": "Onconova Therapeutics, Inc."
    },
    "HLYK": {
        "cik": 1680139,
        "title": "HealthLynked Corp"
    },
    "GYRO": {
        "cik": 1589061,
        "title": "Gyrodyne, LLC"
    },
    "CNTX": {
        "cik": 1842952,
        "title": "Context Therapeutics Inc."
    },
    "CTM": {
        "cik": 1877939,
        "title": "Castellum, Inc."
    },
    "GLTO": {
        "cik": 1800315,
        "title": "Galecto, Inc."
    },
    "JCTCF": {
        "cik": 885307,
        "title": "JEWETT CAMERON TRADING CO LTD"
    },
    "AQB": {
        "cik": 1603978,
        "title": "AquaBounty Technologies, Inc."
    },
    "FZMD": {
        "cik": 319016,
        "title": "Fuse Medical, Inc."
    },
    "ANY": {
        "cik": 1591956,
        "title": "Sphere 3D Corp."
    },
    "CLRD": {
        "cik": 895665,
        "title": "Clearday, Inc."
    },
    "GRCYF": {
        "cik": 1768910,
        "title": "Greencity Acquisition Corp"
    },
    "CLRB": {
        "cik": 1279704,
        "title": "Cellectar Biosciences, Inc."
    },
    "FGI": {
        "cik": 1864943,
        "title": "FGI Industries Ltd."
    },
    "VBLT": {
        "cik": 1603207,
        "title": "Vascular Biogenics Ltd."
    },
    "TSRI": {
        "cik": 98338,
        "title": "TSR INC"
    },
    "WYY": {
        "cik": 1034760,
        "title": "WIDEPOINT CORP"
    },
    "BICX": {
        "cik": 1443863,
        "title": "BioCorRx Inc."
    },
    "TLCC": {
        "cik": 1590695,
        "title": "TWINLAB CONSOLIDATED HOLDINGS, INC."
    },
    "WNW": {
        "cik": 1787803,
        "title": "Meiwu Technology Co Ltd"
    },
    "ACST": {
        "cik": 1444192,
        "title": "Acasti Pharma Inc."
    },
    "FRZA": {
        "cik": 1901305,
        "title": "Forza X1, Inc."
    },
    "COHN": {
        "cik": 1270436,
        "title": "Cohen & Co Inc."
    },
    "SEAV": {
        "cik": 1763660,
        "title": "SEATech Ventures Corp."
    },
    "KUKE": {
        "cik": 1809158,
        "title": "Kuke Music Holding Ltd"
    },
    "DFCO": {
        "cik": 725394,
        "title": "DALRADA FINANCIAL CORP"
    },
    "GSHRF": {
        "cik": 1961592,
        "title": "GOLDSHORE RESOURCES INC."
    },
    "GSUN": {
        "cik": 1826376,
        "title": "Golden Sun Education Group Ltd"
    },
    "BCEL": {
        "cik": 1532346,
        "title": "Atreca, Inc."
    },
    "CHNR": {
        "cik": 793628,
        "title": "CHINA NATURAL RESOURCES INC"
    },
    "GIGM": {
        "cik": 1105101,
        "title": "GIGAMEDIA Ltd"
    },
    "CHEK": {
        "cik": 1610590,
        "title": "Check-Cap Ltd"
    },
    "TGCB": {
        "cik": 1815632,
        "title": "Tego Cyber, Inc."
    },
    "BURU": {
        "cik": 1814215,
        "title": "Nuburu, Inc."
    },
    "PHGE": {
        "cik": 1739174,
        "title": "BiomX Inc."
    },
    "DXYN": {
        "cik": 29332,
        "title": "DIXIE GROUP INC"
    },
    "LVRLF": {
        "cik": 1168981,
        "title": "CordovaCann Corp."
    },
    "NYC": {
        "cik": 1595527,
        "title": "American Strategic Investment Co."
    },
    "KTTA": {
        "cik": 1841330,
        "title": "Pasithea Therapeutics Corp."
    },
    "ZKIN": {
        "cik": 1687451,
        "title": "ZK International Group Co., Ltd."
    },
    "AAMC": {
        "cik": 1555074,
        "title": "Altisource Asset Management Corp"
    },
    "YTFD": {
        "cik": 1311673,
        "title": "Yale Transaction Finders, Inc."
    },
    "CREX": {
        "cik": 1356093,
        "title": "CREATIVE REALITIES, INC."
    },
    "PGID": {
        "cik": 1061164,
        "title": "PEREGRINE INDUSTRIES INC"
    },
    "BTBD": {
        "cik": 1718224,
        "title": "BT Brands, Inc."
    },
    "INTZ": {
        "cik": 736012,
        "title": "INTRUSION INC"
    },
    "NRBO": {
        "cik": 1638287,
        "title": "NeuroBo Pharmaceuticals, Inc."
    },
    "KCRD": {
        "cik": 1696025,
        "title": "Kindcard, Inc."
    },
    "CSKL": {
        "cik": 1384437,
        "title": "CATSKILL HUDSON BANCORP INC"
    },
    "ETST": {
        "cik": 1538495,
        "title": "Earth Science Tech, Inc."
    },
    "MGOL": {
        "cik": 1902794,
        "title": "MGO Global Inc."
    },
    "STRR": {
        "cik": 707388,
        "title": "STAR EQUITY HOLDINGS, INC."
    },
    "ITMSF": {
        "cik": 1285170,
        "title": "INTERMAP TECHNOLOGIES CORP"
    },
    "CYADY": {
        "cik": 1637890,
        "title": "Celyad Oncology SA"
    },
    "CORR": {
        "cik": 1347652,
        "title": "CorEnergy Infrastructure Trust, Inc."
    },
    "ACRG": {
        "cik": 773717,
        "title": "American Clean Resources Group, Inc."
    },
    "GENE": {
        "cik": 1166272,
        "title": "GENETIC TECHNOLOGIES LTD"
    },
    "MLCT": {
        "cik": 1438943,
        "title": "MALACHITE INNOVATIONS, INC."
    },
    "AFIB": {
        "cik": 1522860,
        "title": "Acutus Medical, Inc."
    },
    "IINN": {
        "cik": 1837493,
        "title": "Inspira Technologies OXY B.H.N. Ltd"
    },
    "EEIQ": {
        "cik": 1781397,
        "title": "EpicQuest Education Group International Ltd"
    },
    "SPND": {
        "cik": 867038,
        "title": "SPINDLETOP OIL & GAS CO"
    },
    "OHCS": {
        "cik": 1892025,
        "title": "Optimus Healthcare Services, Inc."
    },
    "GTAGF": {
        "cik": 1682056,
        "title": "GOLDEN TAG RESOURCES LTD."
    },
    "VCNX": {
        "cik": 1205922,
        "title": "VACCINEX, INC."
    },
    "FLGC": {
        "cik": 1790169,
        "title": "Flora Growth Corp."
    },
    "TOPS": {
        "cik": 1296484,
        "title": "TOP SHIPS INC."
    },
    "NVVE": {
        "cik": 1836875,
        "title": "Nuvve Holding Corp."
    },
    "RCON": {
        "cik": 1442620,
        "title": "Recon Technology, Ltd"
    },
    "VLCN": {
        "cik": 1829794,
        "title": "Volcon, Inc."
    },
    "CLAD": {
        "cik": 1501958,
        "title": "China Liaoning Dingxu Ecological Agriculture Development, Inc."
    },
    "BIAF": {
        "cik": 1712762,
        "title": "bioAffinity Technologies, Inc."
    },
    "BNRG": {
        "cik": 1901215,
        "title": "Brenmiller Energy Ltd."
    },
    "ACRX": {
        "cik": 1427925,
        "title": "ACELRX PHARMACEUTICALS INC"
    },
    "ELVG": {
        "cik": 1741489,
        "title": "Elvictor Group, Inc."
    },
    "NSGP": {
        "cik": 1445109,
        "title": "NewStream Energy Technologies Group Inc"
    },
    "UGHB": {
        "cik": 1552743,
        "title": "UNIVERSAL GLOBAL HUB INC."
    },
    "RLBD": {
        "cik": 1084133,
        "title": "Real Brands, Inc."
    },
    "MOGU": {
        "cik": 1743971,
        "title": "MOGU Inc."
    },
    "SGE": {
        "cik": 1893448,
        "title": "Strong Global Entertainment, Inc."
    },
    "VBIX": {
        "cik": 797542,
        "title": "Viewbix Inc."
    },
    "SKYE": {
        "cik": 1516551,
        "title": "Skye Bioscience, Inc."
    },
    "GFOO": {
        "cik": 1510518,
        "title": "Genufood Energy Enzymes Corp."
    },
    "VYNE": {
        "cik": 1566044,
        "title": "VYNE Therapeutics Inc."
    },
    "BRDS": {
        "cik": 1861449,
        "title": "Bird Global, Inc."
    },
    "IVDA": {
        "cik": 1397183,
        "title": "Iveda Solutions, Inc."
    },
    "ELRE": {
        "cik": 1438461,
        "title": "Yinfu Gold Corp."
    },
    "LYT": {
        "cik": 1816319,
        "title": "Lytus Technologies Holdings PTV. Ltd."
    },
    "PKBO": {
        "cik": 1834645,
        "title": "Peak Bio, Inc."
    },
    "NHWK": {
        "cik": 1476963,
        "title": "NightHawk Biosciences, Inc."
    },
    "PMN": {
        "cik": 1374339,
        "title": "ProMIS Neurosciences Inc."
    },
    "TFFP": {
        "cik": 1733413,
        "title": "TFF Pharmaceuticals, Inc."
    },
    "ATIF": {
        "cik": 1755058,
        "title": "ATIF Holdings Ltd"
    },
    "TTOO": {
        "cik": 1492674,
        "title": "T2 Biosystems, Inc."
    },
    "SUNL": {
        "cik": 1821850,
        "title": "Sunlight Financial Holdings Inc."
    },
    "POL": {
        "cik": 1810140,
        "title": "Polished.com Inc."
    },
    "ACFN": {
        "cik": 880984,
        "title": "ACORN ENERGY, INC."
    },
    "CGRN": {
        "cik": 1009759,
        "title": "Capstone Green Energy Corp"
    },
    "XIN": {
        "cik": 1398453,
        "title": "Xinyuan Real Estate Co., Ltd."
    },
    "EGYF": {
        "cik": 876235,
        "title": "ENERGY FINDERS INC"
    },
    "YGMZ": {
        "cik": 1782037,
        "title": "MingZhu Logistics Holdings Ltd"
    },
    "PZG": {
        "cik": 1629210,
        "title": "Paramount Gold Nevada Corp."
    },
    "ELSE": {
        "cik": 351789,
        "title": "ELECTRO SENSORS INC"
    },
    "BTCS": {
        "cik": 1436229,
        "title": "BTCS Inc."
    },
    "AWIN": {
        "cik": 1855631,
        "title": "AERWINS Technologies Inc."
    },
    "ZEV": {
        "cik": 1802749,
        "title": "Lightning eMotors, Inc."
    },
    "INLX": {
        "cik": 1081745,
        "title": "INTELLINETICS, INC."
    },
    "ECTM": {
        "cik": 1487798,
        "title": "ECA Marcellus Trust I"
    },
    "RSMXF": {
        "cik": 1858994,
        "title": "Regency Silver Corp."
    },
    "TPHS": {
        "cik": 724742,
        "title": "Trinity Place Holdings Inc."
    },
    "QSAM": {
        "cik": 1310527,
        "title": "QSAM Biosciences, Inc."
    },
    "GOVX": {
        "cik": 832489,
        "title": "GeoVax Labs, Inc."
    },
    "BWV": {
        "cik": 1782107,
        "title": "Blue Water Biotech, Inc."
    },
    "QOEG": {
        "cik": 1439237,
        "title": "Quality Online Education Group Inc."
    },
    "SOPA": {
        "cik": 1817511,
        "title": "SOCIETY PASS INCORPORATED."
    },
    "APRE": {
        "cik": 1781983,
        "title": "Aprea Therapeutics, Inc."
    },
    "SFR": {
        "cik": 1821075,
        "title": "Appreciate Holdings, Inc."
    },
    "CNVS": {
        "cik": 1173204,
        "title": "Cineverse Corp."
    },
    "KIQ": {
        "cik": 1161814,
        "title": "KELSO TECHNOLOGIES INC"
    },
    "VPRB": {
        "cik": 1376231,
        "title": "VPR Brands, LP."
    },
    "PYPD": {
        "cik": 1611842,
        "title": "PolyPid Ltd."
    },
    "CMRA": {
        "cik": 1907685,
        "title": "Comera Life Sciences Holdings, Inc."
    },
    "CSSE": {
        "cik": 1679063,
        "title": "Chicken Soup for the Soul Entertainment, Inc."
    },
    "LFLY": {
        "cik": 1785592,
        "title": "Leafly Holdings, Inc. /DE"
    },
    "DOMH": {
        "cik": 12239,
        "title": "Dominari Holdings Inc."
    },
    "FGF": {
        "cik": 1591890,
        "title": "FG Financial Group, Inc."
    },
    "NSFDF": {
        "cik": 1009922,
        "title": "NXT Energy Solutions Inc."
    },
    "JNVR": {
        "cik": 1805526,
        "title": "Janover Inc."
    },
    "AIMD": {
        "cik": 1014763,
        "title": "Ainos, Inc."
    },
    "ARTW": {
        "cik": 7623,
        "title": "ARTS WAY MANUFACTURING CO INC"
    },
    "MHPC": {
        "cik": 1277998,
        "title": "MANUFACTURED HOUSING PROPERTIES INC."
    },
    "VSOLF": {
        "cik": 1547660,
        "title": "THREE SIXTY SOLAR LTD."
    },
    "EDUC": {
        "cik": 31667,
        "title": "EDUCATIONAL DEVELOPMENT CORP"
    },
    "AKU": {
        "cik": 1776197,
        "title": "AKUMIN INC."
    },
    "MCVT": {
        "cik": 1425355,
        "title": "Mill City Ventures III, Ltd"
    },
    "WLGS": {
        "cik": 1899658,
        "title": "WANG & LEE GROUP, Inc."
    },
    "MWG": {
        "cik": 1941500,
        "title": "Multi Ways Holdings Ltd"
    },
    "AXREF": {
        "cik": 1175596,
        "title": "AMARC RESOURCES LTD"
    },
    "AEZS": {
        "cik": 1113423,
        "title": "Aeterna Zentaris Inc."
    },
    "XERI": {
        "cik": 1481504,
        "title": "XERIANT, INC."
    },
    "LSDI": {
        "cik": 1865127,
        "title": "Lucy Scientific Discovery, Inc."
    },
    "RCG": {
        "cik": 919567,
        "title": "RENN Fund, Inc."
    },
    "TC": {
        "cik": 1743340,
        "title": "TuanChe Ltd"
    },
    "EKSO": {
        "cik": 1549084,
        "title": "EKSO BIONICS HOLDINGS, INC."
    },
    "AVCRF": {
        "cik": 1355736,
        "title": "Avricore Health Inc."
    },
    "PEV": {
        "cik": 1879848,
        "title": "PHOENIX MOTOR INC."
    },
    "WAVE": {
        "cik": 1846715,
        "title": "Eco Wave Power Global AB (publ)"
    },
    "ARAV": {
        "cik": 1513818,
        "title": "Aravive, Inc."
    },
    "MYO": {
        "cik": 1369290,
        "title": "MYOMO, INC."
    },
    "ENG": {
        "cik": 933738,
        "title": "ENGLOBAL CORP"
    },
    "ITRM": {
        "cik": 1659323,
        "title": "Iterum Therapeutics plc"
    },
    "CEI": {
        "cik": 1309082,
        "title": "CAMBER ENERGY, INC."
    },
    "AEI": {
        "cik": 1750106,
        "title": "Alset Inc."
    },
    "BBLR": {
        "cik": 1873722,
        "title": "Bubblr Inc."
    },
    "VVPR": {
        "cik": 1681348,
        "title": "VivoPower International PLC"
    },
    "IKT": {
        "cik": 1750149,
        "title": "Inhibikase Therapeutics, Inc."
    },
    "ERNA": {
        "cik": 748592,
        "title": "Eterna Therapeutics Inc."
    },
    "GDNSF": {
        "cik": 1771706,
        "title": "Goodness Growth Holdings, Inc."
    },
    "VJET": {
        "cik": 1582581,
        "title": "voxeljet AG"
    },
    "LASE": {
        "cik": 1807887,
        "title": "Laser Photonics Corp"
    },
    "GPLL": {
        "cik": 1883083,
        "title": "GPL Holdings, Inc."
    },
    "GXSFF": {
        "cik": 1299865,
        "title": "Goldsource Mines Inc."
    },
    "AXLA": {
        "cik": 1633070,
        "title": "Axcella Health Inc."
    },
    "LVVV": {
        "cik": 1421289,
        "title": "LiveWire Ergogenics, Inc."
    },
    "UGRO": {
        "cik": 1706524,
        "title": "urban-gro, Inc."
    },
    "GBNH": {
        "cik": 1735948,
        "title": "Greenbrook TMS Inc."
    },
    "XRTX": {
        "cik": 1729214,
        "title": "XORTX Therapeutics Inc."
    },
    "IVDN": {
        "cik": 1190370,
        "title": "INNOVATIVE DESIGNS INC"
    },
    "RAYA": {
        "cik": 1825875,
        "title": "Erayak Power Solution Group Inc."
    },
    "CLWT": {
        "cik": 1026662,
        "title": "EURO TECH HOLDINGS CO LTD"
    },
    "AEHL": {
        "cik": 1470683,
        "title": "Antelope Enterprise Holdings Ltd"
    },
    "AIRO": {
        "cik": 1971544,
        "title": "AIRO Group, Inc."
    },
    "BIMI": {
        "cik": 1213660,
        "title": "BIMI International Medical Inc."
    },
    "ALBT": {
        "cik": 1630212,
        "title": "Avalon GloboCare Corp."
    },
    "PAYD": {
        "cik": 1017655,
        "title": "PAID INC"
    },
    "FRES": {
        "cik": 1786511,
        "title": "Fresh2 Group Ltd"
    },
    "NRSN": {
        "cik": 1875091,
        "title": "NeuroSense Therapeutics Ltd."
    },
    "WRPT": {
        "cik": 1842138,
        "title": "WARPSPEED TAXI INC."
    },
    "BHAT": {
        "cik": 1759136,
        "title": "Blue Hat Interactive Entertainment Technology"
    },
    "BNOX": {
        "cik": 1191070,
        "title": "BIONOMICS LIMITED/FI"
    },
    "CMMB": {
        "cik": 1534248,
        "title": "Chemomab Therapeutics Ltd."
    },
    "CARV": {
        "cik": 1016178,
        "title": "CARVER BANCORP INC"
    },
    "MSN": {
        "cik": 32621,
        "title": "EMERSON RADIO CORP"
    },
    "FXLV": {
        "cik": 1788717,
        "title": "F45 Training Holdings Inc."
    },
    "TLIS": {
        "cik": 1584751,
        "title": "Talis Biomedical Corp"
    },
    "FEMFF": {
        "cik": 1066130,
        "title": "FE Battery Metals Corp."
    },
    "FMFG": {
        "cik": 1698022,
        "title": "Farmers & Merchants Bancshares, Inc."
    },
    "MDRR": {
        "cik": 1654595,
        "title": "Medalist Diversified REIT, Inc."
    },
    "ENZN": {
        "cik": 727510,
        "title": "ENZON PHARMACEUTICALS, INC."
    },
    "MSGM": {
        "cik": 1821175,
        "title": "Motorsport Games Inc."
    },
    "LABP": {
        "cik": 1785345,
        "title": "Landos Biopharma, Inc."
    },
    "BFRI": {
        "cik": 1858685,
        "title": "Biofrontera Inc."
    },
    "BKUCF": {
        "cik": 1463978,
        "title": "BLUE SKY URANIUM CORP."
    },
    "NISN": {
        "cik": 1603993,
        "title": "Nisun International Enterprise Development Group Co., Ltd"
    },
    "NSTM": {
        "cik": 912544,
        "title": "NovelStem International Corp."
    },
    "OCG": {
        "cik": 1776067,
        "title": "Oriental Culture Holding LTD"
    },
    "SBFM": {
        "cik": 1402328,
        "title": "Sunshine Biopharma, Inc"
    },
    "UNRV": {
        "cik": 1451512,
        "title": "Unrivaled Brands, Inc."
    },
    "LIPO": {
        "cik": 1347242,
        "title": "LIPELLA PHARMACEUTICALS INC"
    },
    "MCLD": {
        "cik": 1756499,
        "title": "mCloud Technologies Corp."
    },
    "SCYYF": {
        "cik": 1408146,
        "title": "SCANDIUM INTERNATIONAL MINING CORP."
    },
    "DHCC": {
        "cik": 844887,
        "title": "DIAMONDHEAD CASINO CORP"
    },
    "MARPS": {
        "cik": 62362,
        "title": "MARINE PETROLEUM TRUST"
    },
    "WTER": {
        "cik": 1532390,
        "title": "ALKALINE WATER Co INC"
    },
    "WTRV": {
        "cik": 1589361,
        "title": "White River Energy Corp."
    },
    "PETZ": {
        "cik": 1684425,
        "title": "TDH Holdings, Inc."
    },
    "LXXGQ": {
        "cik": 1450416,
        "title": "LexaGene Holdings Inc."
    },
    "ONVO": {
        "cik": 1497253,
        "title": "ORGANOVO HOLDINGS, INC."
    },
    "ATHE": {
        "cik": 1131343,
        "title": "ALTERITY THERAPEUTICS LTD"
    },
    "PFHO": {
        "cik": 1138476,
        "title": "PACIFIC HEALTH CARE ORGANIZATION INC"
    },
    "AMTI": {
        "cik": 1801777,
        "title": "Applied Molecular Transport Inc."
    },
    "RLBY": {
        "cik": 34285,
        "title": "RELIABILITY INC"
    },
    "EBZT": {
        "cik": 1730869,
        "title": "Everything Blockchain, Inc."
    },
    "EQMEF": {
        "cik": 1792554,
        "title": "Equity Metals Corp"
    },
    "GWAV": {
        "cik": 1589149,
        "title": "Greenwave Technology Solutions, Inc."
    },
    "NXGL": {
        "cik": 1468929,
        "title": "NEXGEL, INC."
    },
    "BLBX": {
        "cik": 1567900,
        "title": "BLACKBOXSTOCKS INC."
    },
    "ACTX": {
        "cik": 1096950,
        "title": "ADVANCED CONTAINER TECHNOLOGIES, INC."
    },
    "SKKY": {
        "cik": 1546853,
        "title": "Skkynet Cloud Systems, Inc."
    },
    "MIMO": {
        "cik": 1823882,
        "title": "Airspan Networks Holdings Inc."
    },
    "AUST": {
        "cik": 1817740,
        "title": "Austin Gold Corp."
    },
    "PRPO": {
        "cik": 1043961,
        "title": "Precipio, Inc."
    },
    "DMS": {
        "cik": 1725134,
        "title": "Digital Media Solutions, Inc."
    },
    "ISPC": {
        "cik": 1558569,
        "title": "iSpecimen Inc."
    },
    "SPTY": {
        "cik": 1840102,
        "title": "SPECIFICITY, INC."
    },
    "VRPX": {
        "cik": 1708331,
        "title": "Virpax Pharmaceuticals, Inc."
    },
    "PEGY": {
        "cik": 22701,
        "title": "Pineapple Energy Inc."
    },
    "MOJO": {
        "cik": 1414953,
        "title": "EQUATOR Beverage Co"
    },
    "OTLC": {
        "cik": 908259,
        "title": "Oncotelic Therapeutics, Inc."
    },
    "ELOX": {
        "cik": 1035354,
        "title": "Eloxx Pharmaceuticals, Inc."
    },
    "CANF": {
        "cik": 1536196,
        "title": "Can-Fite BioPharma Ltd."
    },
    "OLB": {
        "cik": 1314196,
        "title": "OLB GROUP, INC."
    },
    "IMRN": {
        "cik": 1660046,
        "title": "Immuron Ltd"
    },
    "LSF": {
        "cik": 1650696,
        "title": "Laird Superfood, Inc."
    },
    "VRME": {
        "cik": 1104038,
        "title": "VerifyMe, Inc."
    },
    "OGBLY": {
        "cik": 1829949,
        "title": "Onion Global Ltd"
    },
    "CNEY": {
        "cik": 1780785,
        "title": "CN ENERGY GROUP. INC."
    },
    "SHPH": {
        "cik": 1757499,
        "title": "Shuttle Pharmaceuticals Holdings, Inc."
    },
    "OST": {
        "cik": 1803407,
        "title": "Ostin Technology Group Co., Ltd."
    },
    "RVSN": {
        "cik": 1743905,
        "title": "Rail Vision Ltd."
    },
    "TLLTF": {
        "cik": 1761510,
        "title": "TILT Holdings Inc."
    },
    "THER": {
        "cik": 1362703,
        "title": "THERALINK TECHNOLOGIES, INC."
    },
    "BASA": {
        "cik": 1448705,
        "title": "BASANITE, INC."
    },
    "YVR": {
        "cik": 884247,
        "title": "Liquid Media Group Ltd."
    },
    "LTUM": {
        "cik": 1415332,
        "title": "Lithium Corp"
    },
    "IMCC": {
        "cik": 1792030,
        "title": "IM Cannabis Corp."
    },
    "VERO": {
        "cik": 1409269,
        "title": "Venus Concept Inc."
    },
    "VISL": {
        "cik": 1565228,
        "title": "Vislink Technologies, Inc."
    },
    "JXJT": {
        "cik": 1546383,
        "title": "JX Luxventure Ltd"
    },
    "CYXTQ": {
        "cik": 1794905,
        "title": "Cyxtera Technologies, Inc."
    },
    "CLVR": {
        "cik": 1819615,
        "title": "Clever Leaves Holdings Inc."
    },
    "VSMR": {
        "cik": 1370292,
        "title": "VERIFY SMART CORP."
    },
    "ASST": {
        "cik": 1920406,
        "title": "Asset Entities Inc."
    },
    "PURE": {
        "cik": 1006028,
        "title": "PURE BIOSCIENCE, INC."
    },
    "IMNN": {
        "cik": 749647,
        "title": "Imunon, Inc."
    },
    "SONN": {
        "cik": 1106838,
        "title": "Sonnet BioTherapeutics Holdings, Inc."
    },
    "SNWV": {
        "cik": 1417663,
        "title": "SANUWAVE Health, Inc."
    },
    "CVKD": {
        "cik": 1937993,
        "title": "Cadrenal Therapeutics, Inc."
    },
    "FWFW": {
        "cik": 1492617,
        "title": "FLYWHEEL ADVANCED TECHNOLOGY, INC."
    },
    "MGAM": {
        "cik": 1886362,
        "title": "Mobile Global Esports, Inc."
    },
    "OLKR": {
        "cik": 924396,
        "title": "OpenLocker Holdings, Inc."
    },
    "DGLY": {
        "cik": 1342958,
        "title": "DIGITAL ALLY, INC."
    },
    "MMTRS": {
        "cik": 66496,
        "title": "MILLS MUSIC TRUST"
    },
    "CLEU": {
        "cik": 1775085,
        "title": "China Liberal Education Holdings Ltd"
    },
    "MARK": {
        "cik": 1368365,
        "title": "REMARK HOLDINGS, INC."
    },
    "GTBP": {
        "cik": 109657,
        "title": "GT Biopharma, Inc."
    },
    "GRTX": {
        "cik": 1563577,
        "title": "Galera Therapeutics, Inc."
    },
    "CLNV": {
        "cik": 1391426,
        "title": "Clean Vision Corp"
    },
    "SCKT": {
        "cik": 944075,
        "title": "SOCKET MOBILE, INC."
    },
    "ANTE": {
        "cik": 1413745,
        "title": "AIRNET TECHNOLOGY INC."
    },
    "AIRI": {
        "cik": 1009891,
        "title": "AIR INDUSTRIES GROUP"
    },
    "GIPR": {
        "cik": 1651721,
        "title": "GENERATION INCOME PROPERTIES, INC."
    },
    "FHLD": {
        "cik": 1386044,
        "title": "Freedom Holdings, Inc."
    },
    "SOFO": {
        "cik": 1029744,
        "title": "SONIC FOUNDRY INC"
    },
    "LEDS": {
        "cik": 1333822,
        "title": "SemiLEDs Corp"
    },
    "VEDU": {
        "cik": 1892274,
        "title": "Visionary Education Technology Holdings Group Inc."
    },
    "BAOS": {
        "cik": 1811216,
        "title": "Baosheng Media Group Holdings Ltd"
    },
    "KWE": {
        "cik": 1889823,
        "title": "KWESST Micro Systems Inc."
    },
    "OIG": {
        "cik": 1108967,
        "title": "Orbital Infrastructure Group, Inc."
    },
    "GHSI": {
        "cik": 1642375,
        "title": "Guardion Health Sciences, Inc."
    },
    "TNXP": {
        "cik": 1430306,
        "title": "Tonix Pharmaceuticals Holding Corp."
    },
    "DATS": {
        "cik": 1648960,
        "title": "DatChat, Inc."
    },
    "SDCH": {
        "cik": 1022505,
        "title": "SideChannel, Inc."
    },
    "MITQ": {
        "cik": 1770236,
        "title": "MOVING iMAGE TECHNOLOGIES INC."
    },
    "ADXN": {
        "cik": 1574232,
        "title": "Addex Therapeutics Ltd."
    },
    "BLIN": {
        "cik": 1378590,
        "title": "Bridgeline Digital, Inc."
    },
    "FDIT": {
        "cik": 1593184,
        "title": "FINDIT, INC."
    },
    "QH": {
        "cik": 1781193,
        "title": "QUHUO Ltd"
    },
    "DRUG": {
        "cik": 1827401,
        "title": "BRIGHT MINDS BIOSCIENCES INC."
    },
    "TRVN": {
        "cik": 1429560,
        "title": "TREVENA INC"
    },
    "SQFT": {
        "cik": 1080657,
        "title": "Presidio Property Trust, Inc."
    },
    "BUDZ": {
        "cik": 1393772,
        "title": "WEED, INC."
    },
    "FNCH": {
        "cik": 1733257,
        "title": "Finch Therapeutics Group, Inc."
    },
    "BRTX": {
        "cik": 1505497,
        "title": "BioRestorative Therapies, Inc."
    },
    "WAVD": {
        "cik": 803578,
        "title": "WAVEDANCER, INC."
    },
    "STSS": {
        "cik": 1737995,
        "title": "Sharps Technology Inc."
    },
    "AYTU": {
        "cik": 1385818,
        "title": "AYTU BIOPHARMA, INC"
    },
    "NAVB": {
        "cik": 810509,
        "title": "NAVIDEA BIOPHARMACEUTICALS, INC."
    },
    "VAUCF": {
        "cik": 1723047,
        "title": "Viva Gold Corp."
    },
    "GRNQ": {
        "cik": 1597846,
        "title": "Greenpro Capital Corp."
    },
    "TOWTF": {
        "cik": 1579026,
        "title": "TOWER ONE WIRELESS CORP."
    },
    "SPEV": {
        "cik": 764630,
        "title": "SHOREPOWER TECHNOLOGIES INC."
    },
    "CLOQ": {
        "cik": 1437517,
        "title": "CYBERLOQ TECHNOLOGIES, INC."
    },
    "AWX": {
        "cik": 1061069,
        "title": "AVALON HOLDINGS CORP"
    },
    "DBRM": {
        "cik": 1164256,
        "title": "DAYBREAK OIL & GAS, INC."
    },
    "JAGX": {
        "cik": 1585608,
        "title": "Jaguar Health, Inc."
    },
    "SXTP": {
        "cik": 1946563,
        "title": "60 DEGREES PHARMACEUTICALS, INC."
    },
    "SRAX": {
        "cik": 1538217,
        "title": "SRAX, Inc."
    },
    "OCLN": {
        "cik": 1419793,
        "title": "ORIGINCLEAR, INC."
    },
    "PULM": {
        "cik": 1574235,
        "title": "Pulmatrix, Inc."
    },
    "PCSA": {
        "cik": 1533743,
        "title": "Processa Pharmaceuticals, Inc."
    },
    "SLNH": {
        "cik": 64463,
        "title": "Soluna Holdings, Inc"
    },
    "CJAX": {
        "cik": 1763925,
        "title": "CoJax Oil & Gas Corp"
    },
    "VQS": {
        "cik": 1777765,
        "title": "VIQ Solutions Inc."
    },
    "NDRA": {
        "cik": 1681682,
        "title": "ENDRA Life Sciences Inc."
    },
    "WAFU": {
        "cik": 1716770,
        "title": "Wah Fu Education Group Ltd"
    },
    "LEAI": {
        "cik": 1561880,
        "title": "Legacy Education Alliance, Inc."
    },
    "LCFY": {
        "cik": 1875547,
        "title": "Locafy Ltd"
    },
    "HPCO": {
        "cik": 1892480,
        "title": "Hempacco Co., Inc."
    },
    "BOF": {
        "cik": 1962481,
        "title": "BranchOut Food Inc."
    },
    "ID": {
        "cik": 1698113,
        "title": "PARTS iD, Inc."
    },
    "BMNM": {
        "cik": 1275477,
        "title": "BIMINI CAPITAL MANAGEMENT, INC."
    },
    "TENX": {
        "cik": 34956,
        "title": "TENAX THERAPEUTICS, INC."
    },
    "SGLY": {
        "cik": 1422892,
        "title": "Singularity Future Technology Ltd."
    },
    "ODYY": {
        "cik": 1626644,
        "title": "Odyssey Health, Inc."
    },
    "APGN": {
        "cik": 1814140,
        "title": "Apexigen, Inc."
    },
    "IMPL": {
        "cik": 1445499,
        "title": "IMPEL PHARMACEUTICALS INC"
    },
    "MF": {
        "cik": 1851682,
        "title": "Missfresh Ltd"
    },
    "CYCN": {
        "cik": 1755237,
        "title": "Cyclerion Therapeutics, Inc."
    },
    "BPTS": {
        "cik": 1768946,
        "title": "Biophytis SA"
    },
    "LEXX": {
        "cik": 1348362,
        "title": "Lexaria Bioscience Corp."
    },
    "TMBR": {
        "cik": 1504167,
        "title": "Timber Pharmaceuticals, Inc."
    },
    "PKTX": {
        "cik": 1128189,
        "title": "ProtoKinetix, Inc."
    },
    "GVP": {
        "cik": 944480,
        "title": "GSE SYSTEMS INC"
    },
    "HIHO": {
        "cik": 1026785,
        "title": "HIGHWAY HOLDINGS LTD"
    },
    "REBN": {
        "cik": 1707910,
        "title": "Reborn Coffee, Inc."
    },
    "INBP": {
        "cik": 1016504,
        "title": "INTEGRATED BIOPHARMA INC"
    },
    "ELMSQ": {
        "cik": 1784168,
        "title": "Electric Last Mile Solutions, Inc."
    },
    "ALAR": {
        "cik": 1725332,
        "title": "Alarum Technologies Ltd."
    },
    "ADMT": {
        "cik": 849401,
        "title": "ADM TRONICS UNLIMITED, INC."
    },
    "SSCC": {
        "cik": 1881767,
        "title": "Spirits Capital Corp"
    },
    "ZMENY": {
        "cik": 1838937,
        "title": "Zhangmen Education Inc."
    },
    "SBIG": {
        "cik": 1801602,
        "title": "SpringBig Holdings, Inc."
    },
    "NBIO": {
        "cik": 1622057,
        "title": "Nascent Biotech Inc."
    },
    "MNPR": {
        "cik": 1645469,
        "title": "Monopar Therapeutics"
    },
    "CWBR": {
        "cik": 1522602,
        "title": "CohBar, Inc."
    },
    "CXXMF": {
        "cik": 1652452,
        "title": "CMX GOLD & SILVER CORP."
    },
    "APYP": {
        "cik": 1568969,
        "title": "APPYEA, INC"
    },
    "DSNY": {
        "cik": 1099369,
        "title": "DESTINY MEDIA TECHNOLOGIES INC"
    },
    "PXMD": {
        "cik": 1811623,
        "title": "PaxMedica, Inc."
    },
    "CPOP": {
        "cik": 1807389,
        "title": "Pop Culture Group Co., Ltd"
    },
    "MRIN": {
        "cik": 1389002,
        "title": "MARIN SOFTWARE INC"
    },
    "NORD": {
        "cik": 1011060,
        "title": "Nordicus Partners Corp"
    },
    "CNET": {
        "cik": 1376321,
        "title": "ZW Data Action Technologies Inc."
    },
    "LMFA": {
        "cik": 1640384,
        "title": "LM FUNDING AMERICA, INC."
    },
    "FLCX": {
        "cik": 1609988,
        "title": "flooidCX Corp."
    },
    "CUBT": {
        "cik": 1400271,
        "title": "Curative Biotechnology Inc"
    },
    "EVGDF": {
        "cik": 1518353,
        "title": "ELEVATION GOLD MINING Corp"
    },
    "MRAI": {
        "cik": 1844392,
        "title": "Marpai, Inc."
    },
    "ZDPY": {
        "cik": 1279620,
        "title": "Zoned Properties, Inc."
    },
    "INFI": {
        "cik": 1113148,
        "title": "INFINITY PHARMACEUTICALS, INC."
    },
    "PRKR": {
        "cik": 914139,
        "title": "PARKERVISION INC"
    },
    "CREG": {
        "cik": 721693,
        "title": "Smart Powerr Corp."
    },
    "LUCY": {
        "cik": 1808377,
        "title": "Innovative Eyewear Inc"
    },
    "BEOB": {
        "cik": 1480170,
        "title": "BEO BANCORP"
    },
    "VVOS": {
        "cik": 1716166,
        "title": "Vivos Therapeutics, Inc."
    },
    "CHHE": {
        "cik": 1309057,
        "title": "China Health Industries Holdings, Inc."
    },
    "MIND": {
        "cik": 926423,
        "title": "MIND TECHNOLOGY, INC"
    },
    "AMST": {
        "cik": 1807166,
        "title": "Amesite Inc."
    },
    "CRTG": {
        "cik": 1375195,
        "title": "CORETEC GROUP INC."
    },
    "BJDX": {
        "cik": 1704287,
        "title": "Bluejay Diagnostics, Inc."
    },
    "SENR": {
        "cik": 1576197,
        "title": "Strategic Environmental & Energy Resources, Inc."
    },
    "EMMA": {
        "cik": 822370,
        "title": "Emmaus Life Sciences, Inc."
    },
    "SIGY": {
        "cik": 1642159,
        "title": "Sigyn Therapeutics, Inc."
    },
    "GARWF": {
        "cik": 1403870,
        "title": "Golden Arrow Resources Corp"
    },
    "TMPO": {
        "cik": 1813658,
        "title": "Tempo Automation Holdings, Inc."
    },
    "FORD": {
        "cik": 38264,
        "title": "Forward Industries, Inc."
    },
    "SIDU": {
        "cik": 1879726,
        "title": "Sidus Space Inc."
    },
    "TOVX": {
        "cik": 894158,
        "title": "Theriva Biologics, Inc."
    },
    "PTIX": {
        "cik": 1022899,
        "title": "Protagenic Therapeutics, Inc.new"
    },
    "ACAN": {
        "cik": 1508348,
        "title": "AmeriCann, Inc."
    },
    "WETG": {
        "cik": 1784970,
        "title": "WeTrade Group Inc."
    },
    "IPIX": {
        "cik": 1355250,
        "title": "Innovation Pharmaceuticals Inc."
    },
    "NLSC": {
        "cik": 1342219,
        "title": "Namliong SkyCosmos, Inc."
    },
    "AIAD": {
        "cik": 743758,
        "title": "AiAdvertising, Inc."
    },
    "TGL": {
        "cik": 1905956,
        "title": "TREASURE GLOBAL INC"
    },
    "ATHX": {
        "cik": 1368148,
        "title": "ATHERSYS, INC / NEW"
    },
    "GRI": {
        "cik": 1824293,
        "title": "GRI BIO, Inc."
    },
    "HOTH": {
        "cik": 1711786,
        "title": "Hoth Therapeutics, Inc."
    },
    "NXU": {
        "cik": 1722969,
        "title": "Nxu, Inc."
    },
    "ATXG": {
        "cik": 1650101,
        "title": "ADDENTAX GROUP CORP."
    },
    "REED": {
        "cik": 1140215,
        "title": "REED'S, INC."
    },
    "BMMJ": {
        "cik": 1715611,
        "title": "BODY & MIND INC."
    },
    "CLRI": {
        "cik": 1362516,
        "title": "Cleartronic, Inc."
    },
    "NOGN": {
        "cik": 1841800,
        "title": "Nogin, Inc."
    },
    "REPCF": {
        "cik": 1205059,
        "title": "REPLICEL LIFE SCIENCES INC."
    },
    "BKTPF": {
        "cik": 1677522,
        "title": "CRUZ BATTERY METALS CORP."
    },
    "TTNP": {
        "cik": 910267,
        "title": "TITAN PHARMACEUTICALS INC"
    },
    "APM": {
        "cik": 1734005,
        "title": "Aptorum Group Ltd"
    },
    "MOB": {
        "cik": 1898643,
        "title": "Mobilicom Ltd"
    },
    "NMGX": {
        "cik": 891417,
        "title": "Nano Magic Inc."
    },
    "FUV": {
        "cik": 1558583,
        "title": "Arcimoto Inc"
    },
    "WLYW": {
        "cik": 1555214,
        "title": "Wally World Media, Inc"
    },
    "KBNT": {
        "cik": 1729750,
        "title": "Kubient, Inc."
    },
    "GTHP": {
        "cik": 924515,
        "title": "GUIDED THERAPEUTICS INC"
    },
    "INQD": {
        "cik": 1572565,
        "title": "Indoor Harvest Corp"
    },
    "ATXI": {
        "cik": 1644963,
        "title": "AVENUE THERAPEUTICS, INC."
    },
    "AHNR": {
        "cik": 1304409,
        "title": "ATHENA GOLD CORP"
    },
    "CJJD": {
        "cik": 1856084,
        "title": "China Jo-Jo Drugstores Holdings, Inc."
    },
    "HPTO": {
        "cik": 1021435,
        "title": "hopTo Inc."
    },
    "TPST": {
        "cik": 1544227,
        "title": "Tempest Therapeutics, Inc."
    },
    "OXBR": {
        "cik": 1584831,
        "title": "OXBRIDGE RE HOLDINGS Ltd"
    },
    "JUPGF": {
        "cik": 1684688,
        "title": "Jupiter Gold Corp"
    },
    "TIKK": {
        "cik": 96885,
        "title": "TEL INSTRUMENT ELECTRONICS CORP"
    },
    "MTEK": {
        "cik": 1872964,
        "title": "Maris Tech Ltd."
    },
    "NFTN": {
        "cik": 1544400,
        "title": "NFiniTi inc."
    },
    "MSNVF": {
        "cik": 1718817,
        "title": "MISSION READY SOLUTIONS INC"
    },
    "AEMD": {
        "cik": 882291,
        "title": "AETHLON MEDICAL INC"
    },
    "JVA": {
        "cik": 1007019,
        "title": "COFFEE HOLDING CO INC"
    },
    "NVSGF": {
        "cik": 1415758,
        "title": "Nevada Sunrise Gold Corp"
    },
    "TGLTY": {
        "cik": 1510178,
        "title": "GCDI S.A./ADR"
    },
    "PBMLF": {
        "cik": 1319150,
        "title": "Pacific Booker Minerals Inc."
    },
    "GDSI": {
        "cik": 1011662,
        "title": "GLOBAL DIGITAL SOLUTIONS INC"
    },
    "SRLZF": {
        "cik": 861972,
        "title": "Salazar Resources Ltd"
    },
    "SNTW": {
        "cik": 1619096,
        "title": "Summit Networks Inc."
    },
    "ALRN": {
        "cik": 1420565,
        "title": "AILERON THERAPEUTICS INC"
    },
    "TDCB": {
        "cik": 1282847,
        "title": "THIRD CENTURY BANCORP"
    },
    "CING": {
        "cik": 1862150,
        "title": "Cingulate Inc."
    },
    "MNK": {
        "cik": 1567892,
        "title": "Mallinckrodt plc"
    },
    "AUUD": {
        "cik": 1554818,
        "title": "AUDDIA INC."
    },
    "HSCS": {
        "cik": 1468492,
        "title": "Heart Test Laboratories, Inc."
    },
    "BUUZ": {
        "cik": 1174891,
        "title": "CalEthos, Inc."
    },
    "INPX": {
        "cik": 1529113,
        "title": "INPIXON"
    },
    "SMFL": {
        "cik": 1851860,
        "title": "SMART FOR LIFE, INC."
    },
    "PIXY": {
        "cik": 1675634,
        "title": "ShiftPixy, Inc."
    },
    "HLTT": {
        "cik": 1307624,
        "title": "Healthtech Solutions, Inc./UT"
    },
    "XCUR": {
        "cik": 1698530,
        "title": "EXICURE, INC."
    },
    "JWEL": {
        "cik": 1805594,
        "title": "Jowell Global Ltd."
    },
    "QZMRF": {
        "cik": 811522,
        "title": "QUARTZ MOUNTAIN RESOURCES LTD"
    },
    "TCON": {
        "cik": 1394319,
        "title": "Tracon Pharmaceuticals, Inc."
    },
    "CUEN": {
        "cik": 1424657,
        "title": "Cuentas Inc."
    },
    "SIVBQ": {
        "cik": 719739,
        "title": "SVB FINANCIAL GROUP"
    },
    "VMNT": {
        "cik": 1605057,
        "title": "Vemanti Group, Inc."
    },
    "TIVC": {
        "cik": 1787740,
        "title": "Tivic Health Systems, Inc."
    },
    "CDIO": {
        "cik": 1870144,
        "title": "Cardio Diagnostics Holdings, Inc."
    },
    "NXTP": {
        "cik": 1372183,
        "title": "NextPlay Technologies Inc."
    },
    "AUMN": {
        "cik": 1011509,
        "title": "Golden Minerals Co"
    },
    "IDXG": {
        "cik": 1054102,
        "title": "INTERPACE BIOSCIENCES, INC."
    },
    "UNQL": {
        "cik": 1281845,
        "title": "Unique Logistics International, Inc."
    },
    "AHG": {
        "cik": 1702318,
        "title": "Akso Health Group"
    },
    "MDGS": {
        "cik": 1618500,
        "title": "Medigus Ltd."
    },
    "RELV": {
        "cik": 768710,
        "title": "RELIV INTERNATIONAL INC"
    },
    "JUVAF": {
        "cik": 1778651,
        "title": "JUVA LIFE INC./Canada"
    },
    "ARAO": {
        "cik": 1083922,
        "title": "AuraSource, Inc."
    },
    "SBET": {
        "cik": 1025561,
        "title": "SharpLink Gaming Ltd."
    },
    "CMOT": {
        "cik": 1346346,
        "title": "Curtiss Motorcycle Company, Inc."
    },
    "EFOI": {
        "cik": 924168,
        "title": "ENERGY FOCUS, INC/DE"
    },
    "SSY": {
        "cik": 96793,
        "title": "SUNLINK HEALTH SYSTEMS INC"
    },
    "ABVC": {
        "cik": 1173313,
        "title": "ABVC BIOPHARMA, INC."
    },
    "TANH": {
        "cik": 1588084,
        "title": "TANTECH HOLDINGS LTD"
    },
    "FOXO": {
        "cik": 1812360,
        "title": "FOXO TECHNOLOGIES INC."
    },
    "COSG": {
        "cik": 1706509,
        "title": "Cosmos Group Holdings Inc."
    },
    "VIDE": {
        "cik": 758743,
        "title": "VIDEO DISPLAY CORP"
    },
    "CANN": {
        "cik": 1477009,
        "title": "TREES Corp (Colorado)"
    },
    "TNLX": {
        "cik": 99106,
        "title": "TRANS LUX Corp"
    },
    "GTMAY": {
        "cik": 1163560,
        "title": "GRUPO TMM SAB"
    },
    "RSCF": {
        "cik": 1103090,
        "title": "REFLECT SCIENTIFIC, INC."
    },
    "SUIC": {
        "cik": 1394108,
        "title": "SUIC Worldwide Holdings Ltd."
    },
    "HHSE": {
        "cik": 1069680,
        "title": "Hannover House, Inc."
    },
    "TSSI": {
        "cik": 1320760,
        "title": "TSS, Inc."
    },
    "GPOX": {
        "cik": 1673475,
        "title": "GPO Plus, Inc."
    },
    "ENSV": {
        "cik": 319458,
        "title": "Enservco Corp"
    },
    "SRSG": {
        "cik": 1434737,
        "title": "SPIRITS TIME INTERNATIONAL, INC."
    },
    "PRSO": {
        "cik": 890394,
        "title": "Peraso Inc."
    },
    "PGOL": {
        "cik": 1080448,
        "title": "PATRIOT GOLD CORP"
    },
    "BKYI": {
        "cik": 1019034,
        "title": "BIO KEY INTERNATIONAL INC"
    },
    "JPOTF": {
        "cik": 1061612,
        "title": "Jackpot Digital Inc."
    },
    "FXBY": {
        "cik": 1068897,
        "title": "FOXBY CORP."
    },
    "TLRS": {
        "cik": 1288750,
        "title": "Timberline Resources Corp"
    },
    "BON": {
        "cik": 1816815,
        "title": "Bon Natural Life Ltd"
    },
    "BZYR": {
        "cik": 724445,
        "title": "BURZYNSKI RESEARCH INSTITUTE INC"
    },
    "PRFX": {
        "cik": 1801834,
        "title": "PAINREFORM LTD."
    },
    "CELZ": {
        "cik": 1187953,
        "title": "CREATIVE MEDICAL TECHNOLOGY HOLDINGS, INC."
    },
    "SVRE": {
        "cik": 1894693,
        "title": "SaverOne 2014 Ltd."
    },
    "NFTG": {
        "cik": 1895618,
        "title": "NFT Gaming Co Inc."
    },
    "LUVU": {
        "cik": 1374567,
        "title": "Luvu Brands, Inc."
    },
    "ISUN": {
        "cik": 1634447,
        "title": "ISUN, INC."
    },
    "NEWH": {
        "cik": 1371128,
        "title": "NewHydrogen, Inc."
    },
    "FEMY": {
        "cik": 1339005,
        "title": "FEMASYS INC"
    },
    "LWLW": {
        "cik": 723533,
        "title": "Longwen Group Corp."
    },
    "VRAX": {
        "cik": 1885827,
        "title": "Virax Biolabs Group Ltd"
    },
    "AUVI": {
        "cik": 1811109,
        "title": "Applied UV, Inc."
    },
    "NUZE": {
        "cik": 1527613,
        "title": "NuZee, Inc."
    },
    "IPSI": {
        "cik": 1591913,
        "title": "Innovative Payment Solutions, Inc."
    },
    "VEII": {
        "cik": 1417664,
        "title": "Value Exchange International, Inc."
    },
    "VYND": {
        "cik": 1745078,
        "title": "Vynleads, Inc."
    },
    "WINT": {
        "cik": 946486,
        "title": "WINDTREE THERAPEUTICS INC /DE/"
    },
    "KTRA": {
        "cik": 1498382,
        "title": "Kintara Therapeutics, Inc."
    },
    "IBIO": {
        "cik": 1420720,
        "title": "iBio, Inc."
    },
    "KLNG": {
        "cik": 1110607,
        "title": "Koil Energy Solutions, Inc."
    },
    "IAALF": {
        "cik": 1450894,
        "title": "IBC Advanced Alloys Corp."
    },
    "TKAT": {
        "cik": 1491487,
        "title": "Takung Art Co., Ltd"
    },
    "PTPI": {
        "cik": 1815903,
        "title": "Petros Pharmaceuticals, Inc."
    },
    "INTI": {
        "cik": 1042418,
        "title": "Inhibitor Therapeutics, Inc."
    },
    "WNFT": {
        "cik": 1528188,
        "title": "Worldwide NFT Inc."
    },
    "FFLO": {
        "cik": 1543652,
        "title": "Free Flow, Inc."
    },
    "GCTK": {
        "cik": 1506983,
        "title": "GlucoTrack, Inc."
    },
    "LCTC": {
        "cik": 1493137,
        "title": "Lifeloc Technologies, Inc"
    },
    "SLGG": {
        "cik": 1621672,
        "title": "Super League Gaming, Inc."
    },
    "NROM": {
        "cik": 709005,
        "title": "NOBLE ROMANS INC"
    },
    "CNFN": {
        "cik": 1352952,
        "title": "CFN Enterprises Inc."
    },
    "AVGR": {
        "cik": 1506928,
        "title": "Avinger Inc"
    },
    "SILO": {
        "cik": 1514183,
        "title": "Silo Pharma, Inc."
    },
    "NEXI": {
        "cik": 1538210,
        "title": "NexImmune, Inc."
    },
    "KITL": {
        "cik": 1608092,
        "title": "Kisses From Italy Inc."
    },
    "SILEF": {
        "cik": 1545224,
        "title": "Silver Elephant Mining Corp."
    },
    "NURO": {
        "cik": 1289850,
        "title": "NeuroMetrix, Inc."
    },
    "OGEN": {
        "cik": 1174940,
        "title": "ORAGENICS INC"
    },
    "NAHD": {
        "cik": 1485029,
        "title": "New Asia Holdings, Inc."
    },
    "PBTS": {
        "cik": 1754323,
        "title": "Powerbridge Technologies Co., Ltd."
    },
    "BOPO": {
        "cik": 1510832,
        "title": "Biopower Operations Corp"
    },
    "ARDS": {
        "cik": 1614067,
        "title": "Aridis Pharmaceuticals, Inc."
    },
    "PSTV": {
        "cik": 1095981,
        "title": "PLUS THERAPEUTICS, INC."
    },
    "DBGI": {
        "cik": 1668010,
        "title": "Digital Brands Group, Inc."
    },
    "BTTR": {
        "cik": 1471727,
        "title": "Better Choice Co Inc."
    },
    "MWRK": {
        "cik": 1515139,
        "title": "METAWORKS PLATFORMS, INC."
    },
    "CEAD": {
        "cik": 1482541,
        "title": "CEA Industries Inc."
    },
    "BONZ": {
        "cik": 1439264,
        "title": "Marvion Inc."
    },
    "IMTE": {
        "cik": 1668438,
        "title": "Integrated Media Technology Ltd"
    },
    "VINE": {
        "cik": 1880343,
        "title": "Fresh Vine Wine, Inc."
    },
    "MCOM": {
        "cik": 1788841,
        "title": "micromobility.com Inc."
    },
    "TMBXF": {
        "cik": 1072772,
        "title": "TOMBSTONE EXPLORATION CORP"
    },
    "MACE": {
        "cik": 912607,
        "title": "MACE SECURITY INTERNATIONAL INC"
    },
    "BMXI": {
        "cik": 1122993,
        "title": "BROOKMOUNT EXPLORATIONS INC"
    },
    "METX": {
        "cik": 1796514,
        "title": "BTC Digital Ltd."
    },
    "BTB": {
        "cik": 1543268,
        "title": "Bit Brother Ltd"
    },
    "MICS": {
        "cik": 923601,
        "title": "SINGING MACHINE CO INC"
    },
    "OP": {
        "cik": 1869467,
        "title": "OceanPal Inc."
    },
    "CYCC": {
        "cik": 1130166,
        "title": "Cyclacel Pharmaceuticals, Inc."
    },
    "XBIO": {
        "cik": 1534525,
        "title": "Xenetic Biosciences, Inc."
    },
    "LDSN": {
        "cik": 1737193,
        "title": "Luduson G Inc."
    },
    "NRIS": {
        "cik": 1603793,
        "title": "Norris Industries, Inc."
    },
    "IMTH": {
        "cik": 1331612,
        "title": "INNOVATIVE MEDTECH, INC."
    },
    "BETRF": {
        "cik": 1464165,
        "title": "BetterLife Pharma Inc."
    },
    "IRNT": {
        "cik": 1777946,
        "title": "IronNet, Inc."
    },
    "BTOG": {
        "cik": 1735556,
        "title": "BIT ORIGIN Ltd"
    },
    "USLG": {
        "cik": 1536394,
        "title": "U.S. Lighting Group, Inc."
    },
    "TBLT": {
        "cik": 1668370,
        "title": "Toughbuilt Industries, Inc"
    },
    "AMBO": {
        "cik": 1494558,
        "title": "Ambow Education Holding Ltd."
    },
    "CVSI": {
        "cik": 1510964,
        "title": "CV Sciences, Inc."
    },
    "MNRLF": {
        "cik": 1555746,
        "title": "MINERAL MOUNTAIN RESOURCES LTD."
    },
    "SMTK": {
        "cik": 1817760,
        "title": "SmartKem, Inc."
    },
    "KOAN": {
        "cik": 897078,
        "title": "Resonate Blends, Inc."
    },
    "RYES": {
        "cik": 1424864,
        "title": "Rise Gold Corp."
    },
    "RHE": {
        "cik": 1004724,
        "title": "REGIONAL HEALTH PROPERTIES, INC"
    },
    "QRON": {
        "cik": 1689084,
        "title": "Qrons Inc."
    },
    "ABCFF": {
        "cik": 1284237,
        "title": "ABACUS MINING & EXPLORATION CORP"
    },
    "ENSC": {
        "cik": 1716947,
        "title": "Ensysce Biosciences, Inc."
    },
    "GDC": {
        "cik": 1641398,
        "title": "GD Culture Group Ltd"
    },
    "INTV": {
        "cik": 1520118,
        "title": "INTEGRATED VENTURES, INC."
    },
    "LOV": {
        "cik": 1705338,
        "title": "Spark Networks SE"
    },
    "SLGD": {
        "cik": 88000,
        "title": "Scott's Liquid Gold - Inc."
    },
    "ARTL": {
        "cik": 1621221,
        "title": "ARTELO BIOSCIENCES, INC."
    },
    "TCRI": {
        "cik": 1481443,
        "title": "TechCom, Inc."
    },
    "CNSP": {
        "cik": 1729427,
        "title": "CNS Pharmaceuticals, Inc."
    },
    "RGBP": {
        "cik": 1589150,
        "title": "Regen BioPharma Inc"
    },
    "UUU": {
        "cik": 102109,
        "title": "UNIVERSAL SECURITY INSTRUMENTS INC"
    },
    "GBR": {
        "cik": 105744,
        "title": "New Concept Energy, Inc."
    },
    "SKAS": {
        "cik": 1128281,
        "title": "Saker Aviation Services, Inc."
    },
    "SIPN": {
        "cik": 1128252,
        "title": "SIPP International Industries, Inc."
    },
    "GHST": {
        "cik": 1121795,
        "title": "GHST World Inc."
    },
    "QLGN": {
        "cik": 1460702,
        "title": "Qualigen Therapeutics, Inc."
    },
    "XTLB": {
        "cik": 1023549,
        "title": "XTL BIOPHARMACEUTICALS LTD"
    },
    "TIGCF": {
        "cik": 1387473,
        "title": "Triumph Gold Corp."
    },
    "KGKG": {
        "cik": 1802546,
        "title": "KONA GOLD BEVERAGE, INC."
    },
    "WISA": {
        "cik": 1682149,
        "title": "WISA TECHNOLOGIES, INC."
    },
    "MYSZ": {
        "cik": 1211805,
        "title": "My Size, Inc."
    },
    "TNON": {
        "cik": 1560293,
        "title": "Tenon Medical, Inc."
    },
    "HALL": {
        "cik": 819913,
        "title": "HALLMARK FINANCIAL SERVICES INC"
    },
    "AXIM": {
        "cik": 1514946,
        "title": "AXIM BIOTECHNOLOGIES, INC."
    },
    "PBIO": {
        "cik": 830656,
        "title": "PRESSURE BIOSCIENCES INC"
    },
    "ECIA": {
        "cik": 930775,
        "title": "ENCISION INC"
    },
    "SZLSF": {
        "cik": 1454263,
        "title": "STAGEZERO LIFE SCIENCES LTD."
    },
    "SING": {
        "cik": 1443611,
        "title": "SinglePoint Inc."
    },
    "LRDC": {
        "cik": 1442492,
        "title": "Laredo Oil, Inc."
    },
    "RMHB": {
        "cik": 1670869,
        "title": "Rocky Mountain High Brands, Inc."
    },
    "LBUY": {
        "cik": 1643721,
        "title": "LEAFBUYER TECHNOLOGIES, INC."
    },
    "CYAN": {
        "cik": 768408,
        "title": "CYANOTECH CORP"
    },
    "MLMN": {
        "cik": 1100779,
        "title": "Millennium Prime, Inc."
    },
    "FHSEY": {
        "cik": 1786182,
        "title": "First High-School Education Group Co., Ltd."
    },
    "SSOK": {
        "cik": 1559157,
        "title": "Sunstock, Inc."
    },
    "BABB": {
        "cik": 1123596,
        "title": "BAB, INC."
    },
    "SNTG": {
        "cik": 1810467,
        "title": "Sentage Holdings Inc."
    },
    "MMND": {
        "cik": 1088638,
        "title": "MASTERMIND, INC."
    },
    "MINM": {
        "cik": 1467761,
        "title": "MINIM, INC."
    },
    "ADXS": {
        "cik": 1100397,
        "title": "Ayala Pharmaceuticals, Inc."
    },
    "BWMG": {
        "cik": 1166708,
        "title": "Brownie's Marine Group, Inc"
    },
    "EEGI": {
        "cik": 1043150,
        "title": "Eline Entertainment Group, Inc."
    },
    "JCSE": {
        "cik": 1905511,
        "title": "JE Cleantech Holdings Ltd"
    },
    "QNRX": {
        "cik": 1671502,
        "title": "Quoin Pharmaceuticals, Ltd."
    },
    "CETX": {
        "cik": 1435064,
        "title": "CEMTREX INC"
    },
    "ICU": {
        "cik": 1831868,
        "title": "SeaStar Medical Holding Corp"
    },
    "BLNC": {
        "cik": 1632121,
        "title": "Balance Labs, Inc."
    },
    "PMCOF": {
        "cik": 1482753,
        "title": "Prospector Metals Corp."
    },
    "AEY": {
        "cik": 874292,
        "title": "ADDVANTAGE TECHNOLOGIES GROUP INC"
    },
    "CLSH": {
        "cik": 1522222,
        "title": "CLS Holdings USA, Inc."
    },
    "LXEH": {
        "cik": 1814067,
        "title": "Lixiang Education Holding Co. Ltd."
    },
    "NVNT": {
        "cik": 1282980,
        "title": "Dror Ortho-Design, Inc."
    },
    "ZPHYF": {
        "cik": 1613979,
        "title": "ZEPHYR MINERALS LTD."
    },
    "YOSH": {
        "cik": 1898604,
        "title": "Yoshiharu Global Co."
    },
    "BGAVF": {
        "cik": 1500620,
        "title": "Bravada Gold Corp"
    },
    "CGOLF": {
        "cik": 1759352,
        "title": "Contact Gold Corp."
    },
    "DTGI": {
        "cik": 1014052,
        "title": "Digerati Technologies, Inc."
    },
    "ABCP": {
        "cik": 20639,
        "title": "AmBase Corp"
    },
    "NCPL": {
        "cik": 1414767,
        "title": "Netcapital Inc."
    },
    "IPTK": {
        "cik": 1067873,
        "title": "AS-IP TECH INC"
    },
    "AVOI": {
        "cik": 1342936,
        "title": "Advanced Voice Recognition Systems, Inc"
    },
    "TLSS": {
        "cik": 1463208,
        "title": "Transportation & Logistics Systems, Inc."
    },
    "BVXV": {
        "cik": 1611747,
        "title": "BiondVax Pharmaceuticals Ltd."
    },
    "TARSF": {
        "cik": 1409036,
        "title": "Alianza Minerals Ltd."
    },
    "OVTZ": {
        "cik": 1107280,
        "title": "OCULUS VISIONTECH INC."
    },
    "APTX": {
        "cik": 1674365,
        "title": "Aptinyx Inc."
    },
    "RIBT": {
        "cik": 1063537,
        "title": "RiceBran Technologies"
    },
    "QURT": {
        "cik": 1549631,
        "title": "Quarta-Rad, Inc."
    },
    "AWON": {
        "cik": 1432290,
        "title": "A1 Group, Inc."
    },
    "MEDS": {
        "cik": 1382574,
        "title": "TRxADE HEALTH, INC"
    },
    "PIK": {
        "cik": 1861522,
        "title": "KIDPIK CORP."
    },
    "CPMV": {
        "cik": 836564,
        "title": "Mosaic ImmunoEngineering Inc."
    },
    "ITP": {
        "cik": 1358190,
        "title": "IT TECH PACKAGING, INC."
    },
    "SWVL": {
        "cik": 1875609,
        "title": "Swvl Holdings Corp"
    },
    "OWPC": {
        "cik": 1622244,
        "title": "One World Products, Inc."
    },
    "MRZM": {
        "cik": 1413754,
        "title": "MARIZYME, INC."
    },
    "HITC": {
        "cik": 1584693,
        "title": "Healthcare Integrated Technologies Inc."
    },
    "LIXT": {
        "cik": 1335105,
        "title": "LIXTE BIOTECHNOLOGY HOLDINGS, INC."
    },
    "NEPT": {
        "cik": 1401395,
        "title": "Neptune Wellness Solutions Inc."
    },
    "ONFO": {
        "cik": 1825452,
        "title": "Onfolio Holdings, Inc"
    },
    "KNGRF": {
        "cik": 1191832,
        "title": "Kingsmen Resources Ltd."
    },
    "RKFL": {
        "cik": 823546,
        "title": "ROCKETFUEL BLOCKCHAIN, INC."
    },
    "CDSG": {
        "cik": 946112,
        "title": "China Dongsheng International, Inc."
    },
    "JZXN": {
        "cik": 1816172,
        "title": "Jiuzi Holdings, Inc."
    },
    "DBMM": {
        "cik": 1127475,
        "title": "Digital Brand Media & Marketing Group, Inc."
    },
    "ENVB": {
        "cik": 890821,
        "title": "Enveric Biosciences, Inc."
    },
    "CBDY": {
        "cik": 1586554,
        "title": "Target Group Inc."
    },
    "WDLF": {
        "cik": 1281984,
        "title": "Decentral Life, Inc."
    },
    "OILCF": {
        "cik": 1922639,
        "title": "Permex Petroleum Corp"
    },
    "SITS": {
        "cik": 1468978,
        "title": "SOUTHERN ITS INTERNATIONAL, INC."
    },
    "ALXEF": {
        "cik": 1603519,
        "title": "ALX RESOURCES CORP."
    },
    "CMDRF": {
        "cik": 858043,
        "title": "COMMANDER RESOURCES LTD"
    },
    "ILAL": {
        "cik": 1657214,
        "title": "International Land Alliance Inc."
    },
    "JFBR": {
        "cik": 1885408,
        "title": "Jeffs' Brands Ltd"
    },
    "SQL": {
        "cik": 1605888,
        "title": "SeqLL, Inc."
    },
    "TIRX": {
        "cik": 1782941,
        "title": "TIAN RUIXIANG HOLDINGS LTD"
    },
    "TRCK": {
        "cik": 1045942,
        "title": "Track Group, Inc."
    },
    "TTCFQ": {
        "cik": 1741231,
        "title": "Tattooed Chef, Inc."
    },
    "EAWD": {
        "cik": 1563298,
        "title": "Energy & Water Development Corp"
    },
    "SMREF": {
        "cik": 1480313,
        "title": "SUN SUMMIT MINERALS CORP."
    },
    "PBLA": {
        "cik": 1029125,
        "title": "Panbela Therapeutics, Inc."
    },
    "REVB": {
        "cik": 1810560,
        "title": "REVELATION BIOSCIENCES, INC."
    },
    "TSOI": {
        "cik": 1419051,
        "title": "THERAPEUTIC SOLUTIONS INTERNATIONAL, INC."
    },
    "YQAI": {
        "cik": 1976923,
        "title": "YOUNEEQAI TECHNICAL SERVICES, INC."
    },
    "PHIO": {
        "cik": 1533040,
        "title": "Phio Pharmaceuticals Corp."
    },
    "NMEX": {
        "cik": 1415744,
        "title": "NORTHERN MINERALS & EXPLORATION LTD."
    },
    "SISI": {
        "cik": 1300734,
        "title": "SHINECO, INC."
    },
    "SNOA": {
        "cik": 1367083,
        "title": "Sonoma Pharmaceuticals, Inc."
    },
    "EVVL": {
        "cik": 1759424,
        "title": "Evil Empire Designs, Inc."
    },
    "HILS": {
        "cik": 1861657,
        "title": "Hillstream BioPharma Inc."
    },
    "HENC": {
        "cik": 1324736,
        "title": "Hero Technologies Inc."
    },
    "TPPM": {
        "cik": 1692068,
        "title": "Yotta Global, Inc."
    },
    "FCIC": {
        "cik": 730669,
        "title": "FCCC INC"
    },
    "BLPH": {
        "cik": 1600132,
        "title": "Bellerophon Therapeutics, Inc."
    },
    "PW": {
        "cik": 1532619,
        "title": "Power REIT"
    },
    "NXL": {
        "cik": 1527352,
        "title": "Nexalin Technology, Inc."
    },
    "FRGT": {
        "cik": 1687542,
        "title": "Freight Technologies, Inc."
    },
    "DSGT": {
        "cik": 1413909,
        "title": "DSG Global Inc."
    },
    "ACON": {
        "cik": 1635077,
        "title": "Aclarion, Inc."
    },
    "SVFD": {
        "cik": 1789192,
        "title": "Save Foods, Inc."
    },
    "GKIN": {
        "cik": 1509786,
        "title": "Guskin Gold Corp."
    },
    "LGHL": {
        "cik": 1806524,
        "title": "Lion Group Holding Ltd"
    },
    "ABTI": {
        "cik": 1442999,
        "title": "ALTEROLA BIOTECH INC."
    },
    "ADMG": {
        "cik": 1171008,
        "title": "ADAMANT DRI PROCESSING & MINERALS GROUP"
    },
    "RELI": {
        "cik": 1812727,
        "title": "Reliance Global Group, Inc."
    },
    "SNPW": {
        "cik": 1343465,
        "title": "Sun Pacific Holding Corp."
    },
    "XALL": {
        "cik": 1581220,
        "title": "Xalles Holdings Inc."
    },
    "INBS": {
        "cik": 1725430,
        "title": "INTELLIGENT BIO SOLUTIONS INC."
    },
    "SNPX": {
        "cik": 1571934,
        "title": "Synaptogenix, Inc."
    },
    "DWAY": {
        "cik": 1394638,
        "title": "Driveitaway Holdings, Inc."
    },
    "SINT": {
        "cik": 1269026,
        "title": "Sintx Technologies, Inc."
    },
    "EVOK": {
        "cik": 1403708,
        "title": "Evoke Pharma Inc"
    },
    "FULO": {
        "cik": 1092570,
        "title": "FULLNET COMMUNICATIONS INC"
    },
    "VERB": {
        "cik": 1566610,
        "title": "Verb Technology Company, Inc."
    },
    "CIIT": {
        "cik": 1557798,
        "title": "Tianci International, Inc."
    },
    "UTME": {
        "cik": 1789299,
        "title": "UTime Ltd"
    },
    "STAF": {
        "cik": 1499717,
        "title": "Staffing 360 Solutions, Inc."
    },
    "SVVC": {
        "cik": 1495584,
        "title": "Firsthand Technology Value Fund, Inc."
    },
    "USDR": {
        "cik": 1638911,
        "title": "UAS Drone Corp."
    },
    "AIHS": {
        "cik": 1711012,
        "title": "Senmiao Technology Ltd"
    },
    "PALI": {
        "cik": 1357459,
        "title": "PALISADE BIO, INC."
    },
    "ODII": {
        "cik": 1781405,
        "title": "Odyssey Semiconductor Technologies, Inc."
    },
    "GSAC": {
        "cik": 890725,
        "title": "GELSTAT CORP"
    },
    "KPRX": {
        "cik": 1372514,
        "title": "KIORA PHARMACEUTICALS INC"
    },
    "FTHWF": {
        "cik": 1941771,
        "title": "Field Trip Health & Wellness Ltd."
    },
    "DRMA": {
        "cik": 1853816,
        "title": "Dermata Therapeutics, Inc."
    },
    "VYBE": {
        "cik": 1803977,
        "title": "Limitless X Holdings Inc."
    },
    "NVFY": {
        "cik": 1473334,
        "title": "Nova Lifestyle, Inc."
    },
    "SECO": {
        "cik": 1633441,
        "title": "Secoo Holding Ltd"
    },
    "ZVSA": {
        "cik": 1859007,
        "title": "ZyVersa Therapeutics, Inc."
    },
    "CVAT": {
        "cik": 1376793,
        "title": "Cavitation Technologies, Inc."
    },
    "QLIS": {
        "cik": 1871181,
        "title": "Qualis Innovations, Inc."
    },
    "SNGX": {
        "cik": 812796,
        "title": "SOLIGENIX, INC."
    },
    "RDHL": {
        "cik": 1553846,
        "title": "RedHill Biopharma Ltd."
    },
    "VS": {
        "cik": 1701963,
        "title": "Versus Systems Inc."
    },
    "ICCO": {
        "cik": 1103310,
        "title": "INTERCARE DX INC"
    },
    "CNNC": {
        "cik": 1410187,
        "title": "Cannonau Corp."
    },
    "NAOV": {
        "cik": 1326706,
        "title": "NanoVibronix, Inc."
    },
    "FRTX": {
        "cik": 819050,
        "title": "Fresh Tracks Therapeutics, Inc."
    },
    "SHMY": {
        "cik": 1766267,
        "title": "Synergy Empire Ltd"
    },
    "COMS": {
        "cik": 1178727,
        "title": "COMSovereign Holding Corp."
    },
    "NVIV": {
        "cik": 1292519,
        "title": "INVIVO THERAPEUTICS HOLDINGS CORP."
    },
    "VCOR": {
        "cik": 1627041,
        "title": "VISIBER57 CORP."
    },
    "RKDA": {
        "cik": 1469443,
        "title": "Arcadia Biosciences, Inc."
    },
    "EDBL": {
        "cik": 1809750,
        "title": "Edible Garden AG Inc"
    },
    "PTCO": {
        "cik": 1609258,
        "title": "PetroGas Co"
    },
    "RSLS": {
        "cik": 1427570,
        "title": "ReShape Lifesciences Inc."
    },
    "AGFY": {
        "cik": 1800637,
        "title": "Agrify Corp"
    },
    "BACK": {
        "cik": 1729944,
        "title": "IMAC Holdings, Inc."
    },
    "SPCB": {
        "cik": 1291855,
        "title": "SuperCom Ltd"
    },
    "AUNFF": {
        "cik": 1507713,
        "title": "Aurcana Silver Corp"
    },
    "MGTI": {
        "cik": 1001601,
        "title": "MGT CAPITAL INVESTMENTS, INC."
    },
    "BXRX": {
        "cik": 1780097,
        "title": "Baudax Bio, Inc."
    },
    "ADAD": {
        "cik": 1593204,
        "title": "Huaizhong Health Group, Inc."
    },
    "GRHI": {
        "cik": 894501,
        "title": "GOLD ROCK HOLDINGS, INC."
    },
    "ALDS": {
        "cik": 1755101,
        "title": "APPlife Digital Solutions Inc"
    },
    "DCSX": {
        "cik": 1779303,
        "title": "Direct Communication Solutions, Inc."
    },
    "PTOS": {
        "cik": 1172069,
        "title": "P2 Solar, Inc."
    },
    "ENRT": {
        "cik": 1346022,
        "title": "Enertopia Corp."
    },
    "PRET": {
        "cik": 77281,
        "title": "PENNSYLVANIA REAL ESTATE INVESTMENT TRUST"
    },
    "WGMCF": {
        "cik": 1680962,
        "title": "WINSTON GOLD CORP."
    },
    "GLSH": {
        "cik": 1805087,
        "title": "GELESIS HOLDINGS, INC."
    },
    "AGTX": {
        "cik": 1603345,
        "title": "Agentix Corp."
    },
    "GNTOF": {
        "cik": 1346917,
        "title": "GENTOR RESOURCES INC."
    },
    "GRPS": {
        "cik": 1990446,
        "title": "Trans American Aquaculture, Inc"
    },
    "LOWLF": {
        "cik": 1838128,
        "title": "Lowell Farms Inc."
    },
    "CCCP": {
        "cik": 1696411,
        "title": "Crona Corp."
    },
    "CPHI": {
        "cik": 1106644,
        "title": "CHINA PHARMA HOLDINGS, INC."
    },
    "BITTF": {
        "cik": 1028357,
        "title": "BITTERROOT RESOURCES LTD"
    },
    "SRCO": {
        "cik": 318299,
        "title": "SPARTA COMMERCIAL SERVICES, INC."
    },
    "CFRX": {
        "cik": 1478069,
        "title": "CONTRAFECT Corp"
    },
    "GSBX": {
        "cik": 1651166,
        "title": "Golden State Bancorp"
    },
    "FDCT": {
        "cik": 1722731,
        "title": "FDCTECH, INC."
    },
    "CMND": {
        "cik": 1892500,
        "title": "Clearmind Medicine Inc."
    },
    "ATNF": {
        "cik": 1690080,
        "title": "180 Life Sciences Corp."
    },
    "GULTU": {
        "cik": 1565146,
        "title": "Gulf Coast Ultra Deep Royalty Trust"
    },
    "WORX": {
        "cik": 1674227,
        "title": "SCWorx Corp."
    },
    "CDJM": {
        "cik": 1024095,
        "title": "Carnegie Development, Inc"
    },
    "NUGN": {
        "cik": 1593549,
        "title": "Livento Group, Inc."
    },
    "GWTI": {
        "cik": 1572386,
        "title": "GREENWAY TECHNOLOGIES INC"
    },
    "EFSH": {
        "cik": 1599407,
        "title": "1847 Holdings LLC"
    },
    "YCBD": {
        "cik": 1644903,
        "title": "cbdMD, Inc."
    },
    "VRVR": {
        "cik": 1536089,
        "title": "VIRTUAL INTERACTIVE TECHNOLOGIES CORP."
    },
    "DYNT": {
        "cik": 720875,
        "title": "DYNATRONICS CORP"
    },
    "HSTO": {
        "cik": 1383701,
        "title": "Histogen Inc."
    },
    "APVO": {
        "cik": 1671584,
        "title": "Aptevo Therapeutics Inc."
    },
    "GBLX": {
        "cik": 1165320,
        "title": "GB SCIENCES INC"
    },
    "VYCO": {
        "cik": 1424768,
        "title": "VYCOR MEDICAL INC"
    },
    "BBIG": {
        "cik": 1717556,
        "title": "Vinco Ventures, Inc."
    },
    "SLRX": {
        "cik": 1615219,
        "title": "Salarius Pharmaceuticals, Inc."
    },
    "HMBL": {
        "cik": 1119190,
        "title": "HUMBL, INC."
    },
    "RSHN": {
        "cik": 1087329,
        "title": "RushNet, Inc."
    },
    "NIMU": {
        "cik": 720762,
        "title": "NON INVASIVE MONITORING SYSTEMS INC /FL/"
    },
    "IWSH": {
        "cik": 1279715,
        "title": "Wright Investors Service Holdings, Inc."
    },
    "TOFB": {
        "cik": 730349,
        "title": "TOFUTTI BRANDS INC"
    },
    "DUSYF": {
        "cik": 1551887,
        "title": "DUESENBERG TECHNOLOGIES INC."
    },
    "BPTH": {
        "cik": 1133818,
        "title": "BIO-PATH HOLDINGS INC"
    },
    "RCRT": {
        "cik": 1462223,
        "title": "Recruiter.com Group, Inc."
    },
    "NHIQ": {
        "cik": 1566469,
        "title": "NantHealth, Inc."
    },
    "RNVA": {
        "cik": 931059,
        "title": "Rennova Health, Inc."
    },
    "AMPE": {
        "cik": 1411906,
        "title": "Ampio Pharmaceuticals, Inc."
    },
    "IMII": {
        "cik": 1416090,
        "title": "INCEPTION MINING INC."
    },
    "CISS": {
        "cik": 1951067,
        "title": "C3is Inc."
    },
    "THMG": {
        "cik": 711034,
        "title": "THUNDER MOUNTAIN GOLD INC"
    },
    "MAGE": {
        "cik": 1515317,
        "title": "MAGELLAN GOLD Corp"
    },
    "IONI": {
        "cik": 1580490,
        "title": "I-ON Digital Corp."
    },
    "RNAZ": {
        "cik": 1829635,
        "title": "Transcode Therapeutics, Inc."
    },
    "ROYL": {
        "cik": 1694617,
        "title": "Royale Energy, Inc."
    },
    "INM": {
        "cik": 1728328,
        "title": "InMed Pharmaceuticals Inc."
    },
    "PLSH": {
        "cik": 1552189,
        "title": "PANACEA LIFE SCIENCES HOLDINGS, INC."
    },
    "CYTO": {
        "cik": 1601936,
        "title": "Altamira Therapeutics Ltd."
    },
    "VINO": {
        "cik": 1559998,
        "title": "Gaucho Group Holdings, Inc."
    },
    "TLLYF": {
        "cik": 1689382,
        "title": "Trilogy International Partners Inc."
    },
    "BLCM": {
        "cik": 1358403,
        "title": "BELLICUM PHARMACEUTICALS, INC"
    },
    "EJH": {
        "cik": 1769768,
        "title": "E-Home Household Service Holdings Ltd"
    },
    "TGGI": {
        "cik": 1891791,
        "title": "TRANS GLOBAL GROUP, INC."
    },
    "SXTC": {
        "cik": 1723980,
        "title": "China SXT Pharmaceuticals, Inc."
    },
    "ENDV": {
        "cik": 1528172,
        "title": "ENDONOVO THERAPEUTICS, INC."
    },
    "EBET": {
        "cik": 1829966,
        "title": "EBET, Inc."
    },
    "MHTX": {
        "cik": 1099132,
        "title": "MANHATTAN SCIENTIFICS INC"
    },
    "LGMK": {
        "cik": 1566826,
        "title": "LogicMark, Inc."
    },
    "INKW": {
        "cik": 1585380,
        "title": "Greene Concepts, Inc"
    },
    "MYMX": {
        "cik": 927761,
        "title": "MYMETICS CORP"
    },
    "YTEN": {
        "cik": 1121702,
        "title": "YIELD10 BIOSCIENCE, INC."
    },
    "SVBL": {
        "cik": 1031093,
        "title": "SILVER BULL RESOURCES, INC."
    },
    "ALDA": {
        "cik": 1062506,
        "title": "ATLANTICA INC"
    },
    "KERN": {
        "cik": 1755953,
        "title": "Akerna Corp."
    },
    "INUMF": {
        "cik": 1946335,
        "title": "Infinitum Copper Corp."
    },
    "MOTS": {
        "cik": 1686850,
        "title": "Motus GI Holdings, Inc."
    },
    "CDELF": {
        "cik": 1611831,
        "title": "CANDELARIA MINING CORP."
    },
    "VOCL": {
        "cik": 1357671,
        "title": "Creatd, Inc."
    },
    "KRBP": {
        "cik": 1792581,
        "title": "Kiromic Biopharma, Inc."
    },
    "ASTI": {
        "cik": 1350102,
        "title": "Ascent Solar Technologies, Inc."
    },
    "QWTR": {
        "cik": 1487091,
        "title": "Quest Water Global, Inc."
    },
    "FMNJ": {
        "cik": 1304077,
        "title": "Franklin Mining, Inc."
    },
    "KENS": {
        "cik": 55234,
        "title": "KENILWORTH SYSTEMS CORP"
    },
    "NXEN": {
        "cik": 1625288,
        "title": "NEXIEN BIOPHARMA, INC."
    },
    "UFAB": {
        "cik": 1617669,
        "title": "Unique Fabricating, Inc."
    },
    "PCOK": {
        "cik": 1452936,
        "title": "Pacific Oak Strategic Opportunity REIT, Inc."
    },
    "BMCS": {
        "cik": 1384066,
        "title": "BMCS SUMCOIN INDEX FUND, INC."
    },
    "REII": {
        "cik": 1725516,
        "title": "RENEWABLE INNOVATIONS, INC."
    },
    "NBY": {
        "cik": 1389545,
        "title": "NovaBay Pharmaceuticals, Inc."
    },
    "PTNYF": {
        "cik": 1819074,
        "title": "ParcelPal Logistics Inc."
    },
    "BBLG": {
        "cik": 1419554,
        "title": "Bone Biologics Corp"
    },
    "GROM": {
        "cik": 1662574,
        "title": "Grom Social Enterprises, Inc."
    },
    "AULT": {
        "cik": 896493,
        "title": "Ault Alliance, Inc."
    },
    "SASI": {
        "cik": 788611,
        "title": "SIGMA ADDITIVE SOLUTIONS, INC."
    },
    "TNRG": {
        "cik": 1524872,
        "title": "Thunder Energies Corp"
    },
    "ADMP": {
        "cik": 887247,
        "title": "Adamis Pharmaceuticals Corp"
    },
    "IPCIF": {
        "cik": 1474835,
        "title": "Intellipharmaceutics International Inc."
    },
    "ASNS": {
        "cik": 1141284,
        "title": "ACTELIS NETWORKS INC"
    },
    "RWGI": {
        "cik": 1867589,
        "title": "Rodedawg International Industries, Inc."
    },
    "SNBH": {
        "cik": 1358633,
        "title": "SENTIENT BRANDS HOLDINGS INC."
    },
    "SMKG": {
        "cik": 900475,
        "title": "SmartCard Marketing Systems Inc"
    },
    "CRDV": {
        "cik": 1084551,
        "title": "Community Redevelopment Inc."
    },
    "AGRX": {
        "cik": 1261249,
        "title": "AGILE THERAPEUTICS INC"
    },
    "LSMG": {
        "cik": 1319643,
        "title": "Lode-Star Mining Inc."
    },
    "FSTJ": {
        "cik": 1525306,
        "title": "First America Resources Corp"
    },
    "JAN": {
        "cik": 862861,
        "title": "JanOne Inc."
    },
    "THMO": {
        "cik": 811212,
        "title": "ThermoGenesis Holdings, Inc."
    },
    "STEK": {
        "cik": 1511820,
        "title": "Stemtech Corp"
    },
    "BSFC": {
        "cik": 1730773,
        "title": "Blue Star Foods Corp."
    },
    "UCLE": {
        "cik": 1543623,
        "title": "US NUCLEAR CORP."
    },
    "ESMC": {
        "cik": 862668,
        "title": "ESCALON MEDICAL CORP"
    },
    "NWCN": {
        "cik": 934796,
        "title": "NETWORK CN INC"
    },
    "STMH": {
        "cik": 1697834,
        "title": "Stem Holdings, Inc."
    },
    "WSCO": {
        "cik": 1473490,
        "title": "Wall Street Media Co, Inc."
    },
    "LTES": {
        "cik": 1586495,
        "title": "Leet Technology Inc."
    },
    "TCBP": {
        "cik": 1872812,
        "title": "TC BioPharm (Holdings) plc"
    },
    "WHLT": {
        "cik": 1025771,
        "title": "CHASE PACKAGING CORP"
    },
    "ASAP": {
        "cik": 1653247,
        "title": "Waitr Holdings Inc."
    },
    "CRCE": {
        "cik": 1911467,
        "title": "Circle Energy, Inc./NV"
    },
    "VPER": {
        "cik": 1133192,
        "title": "VIPER NETWORKS INC"
    },
    "IVBT": {
        "cik": 1629205,
        "title": "Innovation1 Biotech Inc."
    },
    "FCCN": {
        "cik": 1131903,
        "title": "SPECTRAL CAPITAL Corp"
    },
    "VNUE": {
        "cik": 1376804,
        "title": "VNUE, Inc."
    },
    "CRWE": {
        "cik": 1103833,
        "title": "Crown Equity Holdings, Inc."
    },
    "CBNT": {
        "cik": 1421636,
        "title": "C-Bond Systems, Inc"
    },
    "SNES": {
        "cik": 1680378,
        "title": "SenesTech, Inc."
    },
    "DREM": {
        "cik": 1518336,
        "title": "Dream Homes & Development Corp."
    },
    "BBUZ": {
        "cik": 1547521,
        "title": "Engage Mobility, Inc."
    },
    "TMIN": {
        "cik": 1613685,
        "title": "TRENDMAKER INC. LTD."
    },
    "CNNN": {
        "cik": 1182731,
        "title": "ConneXionONE Corp."
    },
    "HGEN": {
        "cik": 1293310,
        "title": "HUMANIGEN, INC"
    },
    "MDWK": {
        "cik": 1295514,
        "title": "MDWerks, Inc."
    },
    "SHRG": {
        "cik": 1644488,
        "title": "SHARING SERVICES GLOBAL Corp"
    },
    "AGRI": {
        "cik": 1826397,
        "title": "AGRIFORCE GROWING SYSTEMS LTD."
    },
    "OBLG": {
        "cik": 746210,
        "title": "Oblong, Inc."
    },
    "GMER": {
        "cik": 1454742,
        "title": "GOOD GAMING, INC."
    },
    "GSTC": {
        "cik": 1502152,
        "title": "GlobeStar Therapeutics Corp"
    },
    "CNXA": {
        "cik": 1674440,
        "title": "Connexa Sports Technologies Inc."
    },
    "WEJOQ": {
        "cik": 1864448,
        "title": "Wejo Group Ltd"
    },
    "XSNX": {
        "cik": 1039466,
        "title": "NovAccess Global Inc."
    },
    "COWI": {
        "cik": 1156784,
        "title": "CarbonMeta Technologies, Inc."
    },
    "STQN": {
        "cik": 847942,
        "title": "STRATEGIC ACQUISITIONS INC /NV/"
    },
    "IONM": {
        "cik": 1798270,
        "title": "Assure Holdings Corp."
    },
    "ENMI": {
        "cik": 1300781,
        "title": "DH ENCHANTMENT, INC."
    },
    "VNTRQ": {
        "cik": 1705682,
        "title": "Venator Materials PLC"
    },
    "GRST": {
        "cik": 792935,
        "title": "ETHEMA HEALTH Corp"
    },
    "NGTF": {
        "cik": 1593001,
        "title": "NightFood Holdings, Inc."
    },
    "BSPK": {
        "cik": 1409197,
        "title": "Bespoke Extracts, Inc."
    },
    "SRGZ": {
        "cik": 1401835,
        "title": "Star Gold Corp."
    },
    "FIFG": {
        "cik": 1648903,
        "title": "First Foods Group, Inc."
    },
    "PCST": {
        "cik": 1406434,
        "title": "PURE CAPITAL SOLUTIONS, INC."
    },
    "ARTH": {
        "cik": 1537561,
        "title": "Arch Therapeutics, Inc."
    },
    "OCTO": {
        "cik": 1892492,
        "title": "Eightco Holdings Inc."
    },
    "WESC": {
        "cik": 1368275,
        "title": "W&E Source Corp."
    },
    "IMHC": {
        "cik": 1349706,
        "title": "IMPERALIS HOLDING CORP."
    },
    "ECGR": {
        "cik": 1945619,
        "title": "Bellatora, Inc."
    },
    "DLOC": {
        "cik": 1407878,
        "title": "Digital Locations, Inc."
    },
    "NUMD": {
        "cik": 1543637,
        "title": "Nu-Med Plus, Inc."
    },
    "NXMR": {
        "cik": 1088005,
        "title": "NextMart Inc."
    },
    "FOMC": {
        "cik": 867028,
        "title": "FOMO WORLDWIDE, INC."
    },
    "SRMX": {
        "cik": 841533,
        "title": "SADDLE RANCH MEDIA, INC."
    },
    "NUWE": {
        "cik": 1506492,
        "title": "Nuwellis, Inc."
    },
    "AMMJ": {
        "cik": 945617,
        "title": "American Cannabis Company, Inc."
    },
    "GEGP": {
        "cik": 1081188,
        "title": "GOLD ENTERTAINMENT GROUP INC"
    },
    "FWBI": {
        "cik": 1604191,
        "title": "First Wave BioPharma, Inc."
    },
    "EGMCF": {
        "cik": 1199392,
        "title": "EMERGENT METALS CORP."
    },
    "ATVK": {
        "cik": 1530185,
        "title": "Ameritek Ventures, Inc."
    },
    "MITI": {
        "cik": 802257,
        "title": "Mitesco, Inc."
    },
    "AKAN": {
        "cik": 1888014,
        "title": "AKANDA CORP."
    },
    "EBYH": {
        "cik": 1666657,
        "title": "Strainsforpains, Inc."
    },
    "PCYN": {
        "cik": 812306,
        "title": "PROCYON CORP"
    },
    "WARM": {
        "cik": 1399352,
        "title": "COOL TECHNOLOGIES, INC."
    },
    "ATAO": {
        "cik": 1570937,
        "title": "ALTAIR INTERNATIONAL CORP."
    },
    "ELST": {
        "cik": 752294,
        "title": "ELECTRONIC SYSTEMS TECHNOLOGY INC"
    },
    "SCPS": {
        "cik": 1772028,
        "title": "Scopus BioPharma Inc."
    },
    "CMGR": {
        "cik": 1389518,
        "title": "Clubhouse Media Group, Inc."
    },
    "GNLN": {
        "cik": 1743745,
        "title": "Greenlane Holdings, Inc."
    },
    "MMMW": {
        "cik": 1117228,
        "title": "MASS MEGAWATTS WIND POWER INC"
    },
    "AHRO": {
        "cik": 1338929,
        "title": "Authentic Holdings, Inc."
    },
    "FMHS": {
        "cik": 1811999,
        "title": "FARMHOUSE, INC. /NV"
    },
    "EPGG": {
        "cik": 1501862,
        "title": "Empire Global Gaming, Inc."
    },
    "EAST": {
        "cik": 1534708,
        "title": "Eastside Distilling, Inc."
    },
    "GLMD": {
        "cik": 1595353,
        "title": "Galmed Pharmaceuticals Ltd."
    },
    "ASFT": {
        "cik": 1651992,
        "title": "Appsoft Technologies, Inc."
    },
    "KRFG": {
        "cik": 774415,
        "title": "KING RESOURCES, INC."
    },
    "BYOC": {
        "cik": 1386049,
        "title": "Beyond Commerce, Inc."
    },
    "TPTW": {
        "cik": 1661039,
        "title": "TPT GLOBAL TECH, INC."
    },
    "ALTX": {
        "cik": 775057,
        "title": "ALTEX INDUSTRIES INC"
    },
    "MMMM": {
        "cik": 66600,
        "title": "Quad M Solutions, Inc."
    },
    "XNDA": {
        "cik": 1624985,
        "title": "Tribal Rides International Corp."
    },
    "UK": {
        "cik": 1821424,
        "title": "Ucommune International Ltd"
    },
    "VRTC": {
        "cik": 773318,
        "title": "VERITEC INC"
    },
    "BNMV": {
        "cik": 1437491,
        "title": "BitNile Metaverse, Inc."
    },
    "YAYO": {
        "cik": 1691077,
        "title": "EVmo, Inc."
    },
    "HSTC": {
        "cik": 797564,
        "title": "HST Global, Inc."
    },
    "HBUV": {
        "cik": 1639068,
        "title": "Hubilu Venture Corp"
    },
    "AVTX": {
        "cik": 1534120,
        "title": "Avalo Therapeutics, Inc."
    },
    "WHSI": {
        "cik": 1443089,
        "title": "WEARABLE HEALTH SOLUTIONS, INC."
    },
    "FECOF": {
        "cik": 849997,
        "title": "FEC Resources Inc."
    },
    "WOLV": {
        "cik": 1424404,
        "title": "Wolverine Resources Corp."
    },
    "BIOC": {
        "cik": 1044378,
        "title": "BIOCEPT INC"
    },
    "TLIF": {
        "cik": 1633273,
        "title": "TOCCA LIFE HOLDINGS, INC."
    },
    "PCMC": {
        "cik": 1141964,
        "title": "PUBLIC CO MANAGEMENT CORP"
    },
    "ATYG": {
        "cik": 1093636,
        "title": "Saxon Capital Group, Inc./DE"
    },
    "GIGA": {
        "cik": 719274,
        "title": "GIGA TRONICS INC"
    },
    "NUGL": {
        "cik": 1096768,
        "title": "NUGL, INC."
    },
    "NBSE": {
        "cik": 1173281,
        "title": "NeuBase Therapeutics, Inc."
    },
    "TCCO": {
        "cik": 96699,
        "title": "TECHNICAL COMMUNICATIONS CORP"
    },
    "SMME": {
        "cik": 1301991,
        "title": "SmartMetric, Inc."
    },
    "ABNAF": {
        "cik": 873612,
        "title": "Aben Resources Ltd."
    },
    "AVPMF": {
        "cik": 1445467,
        "title": "AVRUPA MINERALS LTD."
    },
    "ALLR": {
        "cik": 1860657,
        "title": "Allarity Therapeutics, Inc."
    },
    "DXF": {
        "cik": 1499494,
        "title": "Dunxin Financial Holdings Ltd"
    },
    "NTRR": {
        "cik": 1512886,
        "title": "NEUTRA CORP."
    },
    "GTLL": {
        "cik": 932021,
        "title": "GLOBAL TECHNOLOGIES LTD"
    },
    "CLOW": {
        "cik": 1619227,
        "title": "Cloudweb, Inc."
    },
    "MNGG": {
        "cik": 1406588,
        "title": "Mining Global, Inc."
    },
    "ZRFY": {
        "cik": 1285543,
        "title": "Zerify, Inc."
    },
    "EMAX": {
        "cik": 1008653,
        "title": "Ecomax, Inc"
    },
    "BZWR": {
        "cik": 1830503,
        "title": "Business Warrior Corp"
    },
    "CSUI": {
        "cik": 1680132,
        "title": "CANNABIS SUISSE CORP."
    },
    "SILS": {
        "cik": 90391,
        "title": "SILVER SCOTT MINES INC"
    },
    "BWMY": {
        "cik": 1656501,
        "title": "BorrowMoney.com, Inc."
    },
    "WNDW": {
        "cik": 1071840,
        "title": "SolarWindow Technologies, Inc."
    },
    "RGMP": {
        "cik": 1716324,
        "title": "Regnum Corp."
    },
    "PRTYQ": {
        "cik": 1592058,
        "title": "Party City Holdco Inc."
    },
    "ECGI": {
        "cik": 1856416,
        "title": "ECGI Holdings, Inc."
    },
    "HCDI": {
        "cik": 1784567,
        "title": "Harbor Custom Development, Inc."
    },
    "AASP": {
        "cik": 930245,
        "title": "GLOBAL ACQUISITIONS Corp"
    },
    "SVSN": {
        "cik": 1099814,
        "title": "STEREO VISION ENTERTAINMENT INC"
    },
    "COUV": {
        "cik": 1450307,
        "title": "CORPORATE UNIVERSE INC"
    },
    "TTCM": {
        "cik": 1389067,
        "title": "TAUTACHROME INC."
    },
    "SIXWF": {
        "cik": 1515251,
        "title": "SIXTH WAVE INNOVATIONS INC."
    },
    "OGAA": {
        "cik": 1749849,
        "title": "Organic Agricultural Co Ltd"
    },
    "ELRA": {
        "cik": 1402371,
        "title": "ELRAY RESOURCES, INC."
    },
    "MXSG": {
        "cik": 1355677,
        "title": "Mexus Gold US"
    },
    "XESP": {
        "cik": 1709542,
        "title": "Electronic Servitor Publication Network Inc."
    },
    "OPGN": {
        "cik": 1293818,
        "title": "OPGEN INC"
    },
    "IFBD": {
        "cik": 1815566,
        "title": "Infobird Co., Ltd"
    },
    "SPRC": {
        "cik": 1611746,
        "title": "SciSparc Ltd."
    },
    "MJNE": {
        "cik": 1456857,
        "title": "MJ Holdings, Inc."
    },
    "RAYT": {
        "cik": 1539778,
        "title": "RAYONT INC."
    },
    "MLRT": {
        "cik": 1375793,
        "title": "Metalert, Inc."
    },
    "LBSR": {
        "cik": 1172178,
        "title": "LIBERTY STAR URANIUM & METALS CORP."
    },
    "ICNB": {
        "cik": 1350073,
        "title": "Iconic Brands, Inc."
    },
    "FLXT": {
        "cik": 925660,
        "title": "FLEXPOINT SENSOR SYSTEMS INC"
    },
    "SSOF": {
        "cik": 1935435,
        "title": "Sixty Six Oilfield Services, Inc."
    },
    "BDRX": {
        "cik": 1643918,
        "title": "Biodexa Pharmaceuticals Plc"
    },
    "WOEN": {
        "cik": 1043894,
        "title": "WOLF ENERGY SERVICES INC."
    },
    "USAQ": {
        "cik": 856984,
        "title": "QHSLab, Inc."
    },
    "INQR": {
        "cik": 1102942,
        "title": "InnovaQor, Inc."
    },
    "HGYN": {
        "cik": 1324759,
        "title": "HONG YUAN HOLDING GROUP"
    },
    "MEXGF": {
        "cik": 1609436,
        "title": "Mexican Gold Mining Corp."
    },
    "GMVD": {
        "cik": 1760764,
        "title": "G Medical Innovations Holdings Ltd."
    },
    "EDGM": {
        "cik": 1652958,
        "title": "Edgemode, Inc."
    },
    "LBWR": {
        "cik": 1426567,
        "title": "Labwire Inc"
    },
    "DIGP": {
        "cik": 1502966,
        "title": "Digipath, Inc."
    },
    "TRLFF": {
        "cik": 1698370,
        "title": "Maven Brands Inc."
    },
    "VBHI": {
        "cik": 1490054,
        "title": "VERDE BIO HOLDINGS, INC."
    },
    "GBUX": {
        "cik": 1169138,
        "title": "GIVBUX, INC."
    },
    "PAXH": {
        "cik": 1350156,
        "title": "PREAXIA HEALTH CARE PAYMENT SYSTEMS INC."
    },
    "ISCO": {
        "cik": 1355790,
        "title": "International Stem Cell CORP"
    },
    "BOTY": {
        "cik": 1407704,
        "title": "LINGERIE FIGHTING CHAMPIONSHIPS, INC."
    },
    "PVNNF": {
        "cik": 1627480,
        "title": "PV Nano Cell, Ltd."
    },
    "MTPP": {
        "cik": 1658521,
        "title": "MOUNTAIN TOP PROPERTIES, INC."
    },
    "CAPC": {
        "cik": 814926,
        "title": "CAPSTONE COMPANIES, INC."
    },
    "CBDW": {
        "cik": 1877461,
        "title": "1606 CORP."
    },
    "KATX": {
        "cik": 1474558,
        "title": "KAT EXPLORATION, INC."
    },
    "WINSF": {
        "cik": 1640251,
        "title": "Wins Finance Holdings Inc."
    },
    "INLB": {
        "cik": 1500123,
        "title": "Item 9 Labs Corp."
    },
    "JPPYY": {
        "cik": 1616291,
        "title": "Jupai Holdings Ltd"
    },
    "GMZP": {
        "cik": 1973160,
        "title": "GEMZ Corp. NV"
    },
    "STAL": {
        "cik": 1614556,
        "title": "Star Alliance International Corp."
    },
    "QPRC": {
        "cik": 824416,
        "title": "QUEST PATENT RESEARCH CORP"
    },
    "HHHEF": {
        "cik": 825171,
        "title": "37 CAPITAL INC"
    },
    "MJHI": {
        "cik": 1789330,
        "title": "MJ Harvest, Inc."
    },
    "DVLP": {
        "cik": 1736865,
        "title": "Golden Developing Solutions, Inc."
    },
    "RMESF": {
        "cik": 1358654,
        "title": "RED METAL RESOURCES, LTD."
    },
    "TRTK": {
        "cik": 1560905,
        "title": "TORtec Group Corp"
    },
    "VFRM": {
        "cik": 1669400,
        "title": "Veritas Farms, Inc."
    },
    "NVDEF": {
        "cik": 1398713,
        "title": "NEVADA EXPLORATION INC"
    },
    "HWKE": {
        "cik": 1750777,
        "title": "Hawkeye Systems, Inc."
    },
    "STRG": {
        "cik": 1803096,
        "title": "STARGUIDE GROUP, INC."
    },
    "KAYS": {
        "cik": 1530746,
        "title": "Kaya Holdings, Inc."
    },
    "RNWR": {
        "cik": 1467913,
        "title": "808 RENEWABLE ENERGY CORP"
    },
    "FRZT": {
        "cik": 1485074,
        "title": "Freeze Tag, Inc."
    },
    "CBDS": {
        "cik": 1360442,
        "title": "Cannabis Sativa, Inc."
    },
    "NAFS": {
        "cik": 1409253,
        "title": "North America Frac Sand, Inc."
    },
    "DUUO": {
        "cik": 1635136,
        "title": "DUO WORLD INC"
    },
    "CTKYY": {
        "cik": 1734262,
        "title": "CooTek(Cayman)Inc."
    },
    "BDPT": {
        "cik": 1575142,
        "title": "BIOADAPTIVES, INC."
    },
    "SEVCQ": {
        "cik": 1840416,
        "title": "Sono Group N.V."
    },
    "LADX": {
        "cik": 799698,
        "title": "LadRx Corp"
    },
    "GTCH": {
        "cik": 1471781,
        "title": "GBT Technologies Inc."
    },
    "TRXA": {
        "cik": 1437750,
        "title": "T-REX Acquisition Corp."
    },
    "HNOI": {
        "cik": 1342916,
        "title": "HNO International, Inc."
    },
    "MMEX": {
        "cik": 1440799,
        "title": "MMEX Resources Corp"
    },
    "AMNI": {
        "cik": 822746,
        "title": "AMERICAN NOBLE GAS, INC."
    },
    "GMPW": {
        "cik": 1064722,
        "title": "GIVEMEPOWER CORP"
    },
    "AREB": {
        "cik": 1648087,
        "title": "AMERICAN REBEL HOLDINGS INC"
    },
    "MGHL": {
        "cik": 1162283,
        "title": "MORGAN GROUP HOLDING CO"
    },
    "GMBL": {
        "cik": 1451448,
        "title": "ESPORTS ENTERTAINMENT GROUP, INC."
    },
    "SATT": {
        "cik": 1661600,
        "title": "SATIVUS TECH CORP."
    },
    "MTLK": {
        "cik": 1098462,
        "title": "METALINK LTD"
    },
    "GYGC": {
        "cik": 1983389,
        "title": "Guyana Gold Corp"
    },
    "REOS": {
        "cik": 1335288,
        "title": "ReoStar Energy CORP"
    },
    "JKSM": {
        "cik": 860543,
        "title": "Jacksam Corp"
    },
    "NIHK": {
        "cik": 1084475,
        "title": "Video River Networks, Inc."
    },
    "ONCI": {
        "cik": 1300867,
        "title": "ON4 COMMUNICATIONS INC."
    },
    "GSPE": {
        "cik": 1341726,
        "title": "GULFSLOPE ENERGY, INC."
    },
    "BLPG": {
        "cik": 1416697,
        "title": "Blue Line Protection Group, Inc."
    },
    "WEBB": {
        "cik": 1011901,
        "title": "Web Blockchain Media, Inc."
    },
    "TEVNF": {
        "cik": 1853718,
        "title": "Tevano Systems Holdings Inc."
    },
    "KSPN": {
        "cik": 795212,
        "title": "Kaspien Holdings Inc."
    },
    "AFHIF": {
        "cik": 1539894,
        "title": "Atlas Financial Holdings, Inc."
    },
    "SGBI": {
        "cik": 1104280,
        "title": "SANGUI BIOTECH INTERNATIONAL INC"
    },
    "BRBL": {
        "cik": 1399306,
        "title": "BrewBilt Brewing Co"
    },
    "HTGMQ": {
        "cik": 1169987,
        "title": "HTG MOLECULAR DIAGNOSTICS, INC"
    },
    "ETCK": {
        "cik": 1128353,
        "title": "ENERTECK CORP"
    },
    "SHGI": {
        "cik": 1874138,
        "title": "Sparx Holdings Group, Inc."
    },
    "USNU": {
        "cik": 1089815,
        "title": "U.S. NeuroSurgical Holdings, Inc."
    },
    "QTXB": {
        "cik": 820608,
        "title": "QUANTRX BIOMEDICAL CORP"
    },
    "BLIS": {
        "cik": 1703625,
        "title": "Treasure & Shipwreck Recovery, Inc."
    },
    "CANB": {
        "cik": 1509957,
        "title": "Can B Corp"
    },
    "ONEI": {
        "cik": 1388295,
        "title": "OneMeta Inc."
    },
    "IGEN": {
        "cik": 1393540,
        "title": "IGEN NETWORKS CORP"
    },
    "CMGO": {
        "cik": 1346655,
        "title": "CMG HOLDINGS GROUP, INC."
    },
    "ITOX": {
        "cik": 1290658,
        "title": "IIOT-OXYS, Inc."
    },
    "BFYW": {
        "cik": 1852707,
        "title": "Better For You Wellness, Inc."
    },
    "HADV": {
        "cik": 1531477,
        "title": "HEALTH ADVANCE INC."
    },
    "GNOLF": {
        "cik": 1261002,
        "title": "GENOIL INC"
    },
    "AOXY": {
        "cik": 352991,
        "title": "ADVANCED OXYGEN TECHNOLOGIES INC"
    },
    "LAAB": {
        "cik": 1584480,
        "title": "Startech Labs, Inc."
    },
    "IMCI": {
        "cik": 884650,
        "title": "INFINITE GROUP INC"
    },
    "PLYN": {
        "cik": 1612851,
        "title": "Palayan Resources, Inc."
    },
    "PRRY": {
        "cik": 1467505,
        "title": "Planet Resource Recovery, Inc."
    },
    "SSHT": {
        "cik": 1975222,
        "title": "SSHT S&T Group Ltd."
    },
    "RAHGF": {
        "cik": 1611852,
        "title": "Roan Holdings Group Co., Ltd."
    },
    "DLYT": {
        "cik": 1125699,
        "title": "DAIS Corp"
    },
    "ZICX": {
        "cik": 1465311,
        "title": "Zicix Corp"
    },
    "ISGN": {
        "cik": 727634,
        "title": "iSign Solutions Inc."
    },
    "FRTG": {
        "cik": 1602813,
        "title": "FRONTERA GROUP INC."
    },
    "MYCB": {
        "cik": 1556801,
        "title": "My City Builders, Inc."
    },
    "NNAX": {
        "cik": 1132509,
        "title": "New Momentum Corp."
    },
    "RDGA": {
        "cik": 812152,
        "title": "RIDGEFIELD ACQUISITION CORP"
    },
    "NSPDF": {
        "cik": 1590875,
        "title": "NATURALLY SPLENDID ENTERPRISES LTD."
    },
    "YBCN": {
        "cik": 1284454,
        "title": "Yong Bai Chao New Retail Corp"
    },
    "WDDD": {
        "cik": 1961,
        "title": "WORLDS INC"
    },
    "PHBI": {
        "cik": 1435181,
        "title": "Pharmagreen Biotech Inc."
    },
    "TQLB": {
        "cik": 1822529,
        "title": "Torque Lifestyle Brands, Inc."
    },
    "PSWW": {
        "cik": 1587476,
        "title": "Principal Solar, Inc."
    },
    "ARRT": {
        "cik": 1530425,
        "title": "Artisan Consumer Goods, Inc."
    },
    "WWSG": {
        "cik": 1342792,
        "title": "WORLDWIDE STRATEGIES INC"
    },
    "ROAG": {
        "cik": 1058330,
        "title": "Rogue One, Inc."
    },
    "TMGI": {
        "cik": 1434601,
        "title": "Marquie Group, Inc."
    },
    "OMTK": {
        "cik": 1404804,
        "title": "Omnitek Engineering Corp"
    },
    "MNTR": {
        "cik": 1599117,
        "title": "Mentor Capital, Inc."
    },
    "GRLF": {
        "cik": 915661,
        "title": "GREEN LEAF INNOVATIONS INC"
    },
    "GCAN": {
        "cik": 1695473,
        "title": "Greater Cannabis Company, Inc."
    },
    "BCNN": {
        "cik": 1946585,
        "title": "Balincan USA, Inc"
    },
    "GSFI": {
        "cik": 1437476,
        "title": "Green Stream Holdings Inc."
    },
    "SSET": {
        "cik": 1561686,
        "title": "STARSTREAM ENTERTAINMENT, INC."
    },
    "ABMC": {
        "cik": 896747,
        "title": "AMERICAN BIO MEDICA CORP"
    },
    "QBIO": {
        "cik": 1596062,
        "title": "Q BioMed Inc."
    },
    "RINO": {
        "cik": 1394220,
        "title": "JOIN Entertainment Holdings, Inc."
    },
    "SANP": {
        "cik": 1499275,
        "title": "SANTO MINING CORP."
    },
    "PACV": {
        "cik": 882800,
        "title": "Pacific Ventures Group, Inc."
    },
    "CYDX": {
        "cik": 1388994,
        "title": "CYduct Diagnostics, Inc."
    },
    "HCMC": {
        "cik": 844856,
        "title": "Healthier Choices Management Corp."
    },
    "NICH": {
        "cik": 772263,
        "title": "NITCHES INC"
    },
    "DCLT": {
        "cik": 1321828,
        "title": "Data Call Technologies"
    },
    "AURI": {
        "cik": 1092802,
        "title": "AURI INC"
    },
    "XCRT": {
        "cik": 1138586,
        "title": "Xcelerate, Inc."
    },
    "AMIH": {
        "cik": 1300524,
        "title": "AMERICAN INTERNATIONAL HOLDINGS CORP."
    },
    "TAMG": {
        "cik": 1158702,
        "title": "Transnational Group, Inc."
    },
    "GFMH": {
        "cik": 820771,
        "title": "Goliath Film & Media Holdings"
    },
    "TRMNF": {
        "cik": 1574553,
        "title": "NEW WAVE HOLDINGS CORP."
    },
    "JFIL": {
        "cik": 1517389,
        "title": "Jubilant Flame International, Ltd"
    },
    "EHVVF": {
        "cik": 1653606,
        "title": "Ehave, Inc."
    },
    "SKVI": {
        "cik": 1085277,
        "title": "SKINVISIBLE, INC."
    },
    "ASII": {
        "cik": 1464865,
        "title": "Accredited Solutions, Inc."
    },
    "QNGYQ": {
        "cik": 1794621,
        "title": "Quanergy Systems, Inc."
    },
    "MRNJ": {
        "cik": 1607004,
        "title": "METATRON APPS, INC."
    },
    "EVFM": {
        "cik": 1618835,
        "title": "Evofem Biosciences, Inc."
    },
    "EARI": {
        "cik": 1083468,
        "title": "ENTERTAINMENT ARTS RESEARCH, INC."
    },
    "CDXQ": {
        "cik": 1552979,
        "title": "China De Xiao Quan Care Group Co., Ltd"
    },
    "VMHG": {
        "cik": 895287,
        "title": "VICTORY MARINE HOLDINGS CORP"
    },
    "TPIA": {
        "cik": 1763329,
        "title": "Mycotopia Therapies, Inc."
    },
    "GNRS": {
        "cik": 1790665,
        "title": "Greenrose Holding Co Inc."
    },
    "GEGI": {
        "cik": 1302913,
        "title": "Genesis Electronics Group, Inc."
    },
    "NHMD": {
        "cik": 1409446,
        "title": "NATE'S FOOD CO."
    },
    "RBSH": {
        "cik": 1421204,
        "title": "Rebus Holdings, Inc."
    },
    "KDCE": {
        "cik": 1049011,
        "title": "KID CASTLE EDUCATIONAL CORP"
    },
    "RTSL": {
        "cik": 1575659,
        "title": "Rapid Therapeutic Science Laboratories, Inc."
    },
    "RGIN": {
        "cik": 1412659,
        "title": "Regenicin, Inc."
    },
    "MDEX": {
        "cik": 1318268,
        "title": "Madison Technologies Inc."
    },
    "EMED": {
        "cik": 1715819,
        "title": "Electromedical Technologies, Inc"
    },
    "MLFB": {
        "cik": 1308569,
        "title": "MAJOR LEAGUE FOOTBALL INC"
    },
    "OWVI": {
        "cik": 1763657,
        "title": "One World Ventures Inc"
    },
    "GMEV": {
        "cik": 1382112,
        "title": "GME INNOTAINMENT, INC."
    },
    "IINX": {
        "cik": 1528308,
        "title": "IONIX TECHNOLOGY, INC."
    },
    "CSSI": {
        "cik": 1178660,
        "title": "COSTAS INC"
    },
    "UVSS": {
        "cik": 1286768,
        "title": "UNIVERSAL SYSTEMS INC"
    },
    "MSYN": {
        "cik": 1693687,
        "title": "MS YOUNG ADVENTURE ENTERPRISE, INC."
    },
    "SQZB": {
        "cik": 1604477,
        "title": "SQZ Biotechnologies Co"
    },
    "GYST": {
        "cik": 1510524,
        "title": "GRAYSTONE COMPANY, INC."
    },
    "VEST": {
        "cik": 1594968,
        "title": "Vestiage, Inc."
    },
    "BOTH": {
        "cik": 894560,
        "title": "BIOETHICS LTD"
    },
    "CNBX": {
        "cik": 1343009,
        "title": "CNBX Pharmaceuticals Inc."
    },
    "RAKR": {
        "cik": 1872292,
        "title": "Rainmaker Worldwide Inc."
    },
    "NUVI": {
        "cik": 1410708,
        "title": "Emo Capital Corp."
    },
    "TPII": {
        "cik": 852447,
        "title": "Triad Pro Innovators, Inc."
    },
    "AMLH": {
        "cik": 1124197,
        "title": "AMERICAN LEISURE HOLDINGS, INC."
    },
    "GLAE": {
        "cik": 1014111,
        "title": "GlassBridge Enterprises, Inc."
    },
    "MCCX": {
        "cik": 1535079,
        "title": "MCX Technologies Corp"
    },
    "PTAM": {
        "cik": 1431880,
        "title": "POTASH AMERICA, INC."
    },
    "HLLK": {
        "cik": 1331421,
        "title": "HALLMARK VENTURE GROUP, INC."
    },
    "SGLA": {
        "cik": 1433551,
        "title": "Sino Green Land Corp."
    },
    "BISA": {
        "cik": 918545,
        "title": "BALTIC INTERNATIONAL USA INC"
    },
    "GTHR": {
        "cik": 1017110,
        "title": "GENETHERA INC"
    },
    "GAHC": {
        "cik": 1138724,
        "title": "Global Arena Holding, Inc."
    },
    "ATDS": {
        "cik": 1068689,
        "title": "Data443 Risk Mitigation, Inc."
    },
    "RSPI": {
        "cik": 849636,
        "title": "RespireRx Pharmaceuticals Inc."
    },
    "CONC": {
        "cik": 790273,
        "title": "CONECTISYS CORP"
    },
    "BBLNF": {
        "cik": 1866390,
        "title": "Babylon Holdings Ltd"
    },
    "PLTYF": {
        "cik": 1433309,
        "title": "Plastec Technologies, Ltd."
    },
    "QREE": {
        "cik": 1295961,
        "title": "QUANTUM ENERGY INC."
    },
    "MASN": {
        "cik": 1486452,
        "title": "Maison Luxe, Inc."
    },
    "PARG": {
        "cik": 1495648,
        "title": "Power Americas Resource Group Ltd."
    },
    "PMPG": {
        "cik": 1301838,
        "title": "Premier Product Group, Inc."
    },
    "SRGAQ": {
        "cik": 1760173,
        "title": "SURGALIGN HOLDINGS, INC."
    },
    "CDIX": {
        "cik": 811222,
        "title": "Cardiff Lexington Corp"
    },
    "VHLD": {
        "cik": 1916879,
        "title": "VECTOR 21 HOLDINGS, INC."
    },
    "MBGH": {
        "cik": 1488638,
        "title": "MBG Holdings, Inc."
    },
    "ABQQ": {
        "cik": 1605331,
        "title": "AB INTERNATIONAL GROUP CORP."
    },
    "UPDC": {
        "cik": 836937,
        "title": "UPD HOLDING CORP."
    },
    "BLMS": {
        "cik": 1138608,
        "title": "BLOOMIOS, INC."
    },
    "SCRH": {
        "cik": 831489,
        "title": "SCORES HOLDING CO INC"
    },
    "WLMSQ": {
        "cik": 1136294,
        "title": "Williams Industrial Services Group Inc."
    },
    "MSSV": {
        "cik": 1760026,
        "title": "MESO NUMISMATICS, INC."
    },
    "IVRN": {
        "cik": 1591165,
        "title": "Innoveren Scientific, Inc."
    },
    "GXXM": {
        "cik": 1681556,
        "title": "GEX MANAGEMENT, INC."
    },
    "PHOT": {
        "cik": 1161582,
        "title": "GROWLIFE, INC."
    },
    "MAPT": {
        "cik": 1697935,
        "title": "MAPTELLIGENT, INC."
    },
    "HMLA": {
        "cik": 1409624,
        "title": "HIMALAYA TECHNOLOGIES, INC"
    },
    "VIZC": {
        "cik": 1506295,
        "title": "VIZCONNECT, INC."
    },
    "LIVC": {
        "cik": 1108630,
        "title": "Live Current Media Inc."
    },
    "FLES": {
        "cik": 1438901,
        "title": "Auto Parts 4Less Group, Inc."
    },
    "JPEX": {
        "cik": 1506814,
        "title": "JPX Global Inc."
    },
    "BEGI": {
        "cik": 1483646,
        "title": "BLACKSTAR ENTERPRISE GROUP, INC."
    },
    "FORZ": {
        "cik": 1683131,
        "title": "Forza Innovations Inc"
    },
    "USRM": {
        "cik": 1388319,
        "title": "U.S. Stem Cell, Inc."
    },
    "PPCB": {
        "cik": 1517681,
        "title": "Propanc Biopharma, Inc."
    },
    "EMDF": {
        "cik": 894552,
        "title": "E Med Future, Inc."
    },
    "SAML": {
        "cik": 1530163,
        "title": "Samsara Luggage, Inc."
    },
    "ATRX": {
        "cik": 737207,
        "title": "Adhera Therapeutics, Inc."
    },
    "LFAP": {
        "cik": 1510247,
        "title": "LGBTQ Loyalty Holdings, Inc."
    },
    "XFCI": {
        "cik": 1379043,
        "title": "XTREME FIGHTING CHAMPIONSHIPS, INC."
    },
    "SNMN": {
        "cik": 1706907,
        "title": "SNM Global Holdings"
    },
    "DZGH": {
        "cik": 1883389,
        "title": "Da Zhong Trading Group Holding Co"
    },
    "VISM": {
        "cik": 1082733,
        "title": "VISIUM TECHNOLOGIES, INC."
    },
    "THCT": {
        "cik": 1404935,
        "title": "THC Therapeutics, Inc."
    },
    "SPOWF": {
        "cik": 1227282,
        "title": "Strata Power Corp"
    },
    "RWBYF": {
        "cik": 1744345,
        "title": "Red White & Bloom Brands Inc."
    },
    "LFEV": {
        "cik": 1916741,
        "title": "Life Electric Vehicles Holdings, Inc."
    },
    "WINR": {
        "cik": 1708410,
        "title": "SIMPLICITY ESPORTS & GAMING Co"
    },
    "BBBT": {
        "cik": 1409999,
        "title": "Black Bird Biotech, Inc."
    },
    "AHIX": {
        "cik": 747435,
        "title": "ALUF HOLDINGS, INC."
    },
    "GRMC": {
        "cik": 59860,
        "title": "GOLDRICH MINING CO"
    },
    "CLCS": {
        "cik": 1569340,
        "title": "Cell Source, Inc."
    },
    "PCNT": {
        "cik": 1504239,
        "title": "Point of Care Nano-Technology, Inc."
    },
    "WTKN": {
        "cik": 1456453,
        "title": "CLStv Corp."
    },
    "CIRX": {
        "cik": 813716,
        "title": "CIRTRAN CORP"
    },
    "VGFCQ": {
        "cik": 1878835,
        "title": "Very Good Food Co Inc."
    },
    "ATNXQ": {
        "cik": 1300699,
        "title": "Athenex, Inc."
    },
    "SEII": {
        "cik": 819926,
        "title": "SHARING ECONOMY INTERNATIONAL INC."
    },
    "SCGX": {
        "cik": 1277575,
        "title": "SAXON CAPITAL GROUP INC"
    },
    "CWNOF": {
        "cik": 1145898,
        "title": "CHINESEWORLDNET COM INC"
    },
    "SUWN": {
        "cik": 806592,
        "title": "SUNWIN STEVIA INTERNATIONAL, INC."
    },
    "RDAR": {
        "cik": 1384365,
        "title": "RAADR, INC."
    },
    "HSTA": {
        "cik": 1813603,
        "title": "Hestia Insight Inc."
    },
    "SNWR": {
        "cik": 1096759,
        "title": "Sanwire Corp"
    },
    "YGYI": {
        "cik": 1569329,
        "title": "Youngevity International, Inc."
    },
    "GTRL": {
        "cik": 1762546,
        "title": "Get Real USA, Inc."
    },
    "EWLU": {
        "cik": 1517498,
        "title": "Merion, Inc."
    },
    "GZIC": {
        "cik": 1286648,
        "title": "GZ6G Technologies Corp."
    },
    "ASCK": {
        "cik": 1492091,
        "title": "AUSCRETE Corp"
    },
    "CYAP": {
        "cik": 1230524,
        "title": "Cyber Apps World"
    },
    "STCC": {
        "cik": 1555972,
        "title": "STERLING CONSOLIDATED Corp"
    },
    "BZRD": {
        "cik": 1765826,
        "title": "Blubuzzard, Inc."
    },
    "CRCW": {
        "cik": 1688126,
        "title": "Crypto Co"
    },
    "CDAKQ": {
        "cik": 1659352,
        "title": "Codiak BioSciences, Inc."
    },
    "HSMD": {
        "cik": 1418115,
        "title": "Healthcare Solutions Management Group, Inc."
    },
    "CPWR": {
        "cik": 827099,
        "title": "Ocean Thermal Energy Corp"
    },
    "SOLS": {
        "cik": 1519177,
        "title": "SOLLENSYS CORP."
    },
    "UNAM": {
        "cik": 100716,
        "title": "UNICO AMERICAN CORP"
    },
    "NLBS": {
        "cik": 1563463,
        "title": "NUTRALIFE BIOSCIENCES, INC"
    },
    "YCRM": {
        "cik": 1624517,
        "title": "Yuenglings Ice Cream Corp"
    },
    "STRYQ": {
        "cik": 1884697,
        "title": "Starry Group Holdings, Inc."
    },
    "CRYO": {
        "cik": 1468679,
        "title": "American CryoStem Corp"
    },
    "IFMK": {
        "cik": 1681941,
        "title": "iFresh Inc"
    },
    "CSTF": {
        "cik": 1877788,
        "title": "CuraScientific Corp."
    },
    "VTXB": {
        "cik": 1373467,
        "title": "Vortex Brands Co."
    },
    "HDVY": {
        "cik": 1141788,
        "title": "HEALTH DISCOVERY CORP"
    },
    "AMNL": {
        "cik": 8328,
        "title": "Applied Minerals, Inc."
    },
    "XCPL": {
        "cik": 1331275,
        "title": "XCPCNL Business Services Corp"
    },
    "LBTI": {
        "cik": 1384135,
        "title": "Lithium & Boron Technology, Inc."
    },
    "DNAX": {
        "cik": 1419995,
        "title": "DNA BRANDS INC"
    },
    "HJGP": {
        "cik": 1421819,
        "title": "Hanjiao Group, Inc."
    },
    "NNRX": {
        "cik": 1451433,
        "title": "NUTRANOMICS, INC."
    },
    "PEARQ": {
        "cik": 1835567,
        "title": "Pear Therapeutics, Inc."
    },
    "ACUR": {
        "cik": 786947,
        "title": "ACURA PHARMACEUTICALS, INC"
    },
    "DPWW": {
        "cik": 1559172,
        "title": "DIEGO PELLICER WORLDWIDE, INC"
    },
    "BBRW": {
        "cik": 1641751,
        "title": "BrewBilt Manufacturing Inc."
    },
    "AFIIQ": {
        "cik": 1655075,
        "title": "Armstrong Flooring, Inc."
    },
    "GAXY": {
        "cik": 1127993,
        "title": "GALAXY NEXT GENERATION, INC."
    },
    "LFER": {
        "cik": 1579010,
        "title": "Life On Earth, Inc."
    },
    "STAB": {
        "cik": 1318641,
        "title": "Statera Biopharma, Inc."
    },
    "DTII": {
        "cik": 1533357,
        "title": "DEFENSE TECHNOLOGIES INTERNATIONAL CORP."
    },
    "SPUP": {
        "cik": 1563227,
        "title": "Sipup Corp"
    },
    "AQUI": {
        "cik": 1863976,
        "title": "Aquarius I Acquisition Corp."
    },
    "SLDC": {
        "cik": 1427644,
        "title": "Telco Cuba, Inc."
    },
    "TRFE": {
        "cik": 1265521,
        "title": "Trustfeed Corp."
    },
    "CGSI": {
        "cik": 1552358,
        "title": "CGS INTERNATIONAL, INC."
    },
    "EQOSQ": {
        "cik": 1790515,
        "title": "EQONEX Ltd"
    },
    "GWHP": {
        "cik": 1598308,
        "title": "Global Wholehealth Partners Corp"
    },
    "PDNLA": {
        "cik": 731245,
        "title": "PRESIDENTIAL REALTY CORP/DE/"
    },
    "ALNAQ": {
        "cik": 1624658,
        "title": "Allena Pharmaceuticals, Inc."
    },
    "BTIM": {
        "cik": 1622231,
        "title": "BOATIM INC."
    },
    "IMBIQ": {
        "cik": 870826,
        "title": "iMedia Brands, Inc."
    },
    "TDNT": {
        "cik": 1421907,
        "title": "Trident Brands Inc"
    },
    "CCOB": {
        "cik": 1456802,
        "title": "Century Cobalt Corp."
    },
    "FRFR": {
        "cik": 1622408,
        "title": "Fritzy Tech Inc."
    },
    "PHASQ": {
        "cik": 1169245,
        "title": "PhaseBio Pharmaceuticals Inc"
    },
    "EPWCF": {
        "cik": 1109504,
        "title": "Empower Clinics Inc."
    },
    "NNMX": {
        "cik": 1473579,
        "title": "NANOMIX Corp"
    },
    "BMXC": {
        "cik": 1613895,
        "title": "Bemax, Inc."
    },
    "VYST": {
        "cik": 1308027,
        "title": "Vystar Corp"
    },
    "BRGO": {
        "cik": 1431074,
        "title": "Bergio International, Inc."
    },
    "SFIO": {
        "cik": 1484703,
        "title": "Starfleet Innotech, Inc."
    },
    "FBCD": {
        "cik": 1370816,
        "title": "FBC Holding, Inc."
    },
    "LHDXQ": {
        "cik": 1652724,
        "title": "Lucira Health, Inc."
    },
    "CBIA": {
        "cik": 1404356,
        "title": "Blue Heaven Coffee, Inc."
    },
    "BTDG": {
        "cik": 725929,
        "title": "B2Digital, Inc."
    },
    "MAXD": {
        "cik": 1353499,
        "title": "Max Sound Corp"
    },
    "NPHC": {
        "cik": 1119643,
        "title": "NUTRA PHARMA CORP"
    },
    "BOXDQ": {
        "cik": 1828672,
        "title": "Boxed, Inc."
    },
    "GWSN": {
        "cik": 1592603,
        "title": "Gulf West Security Network, Inc."
    },
    "AMHG": {
        "cik": 1805024,
        "title": "Amergent Hospitality Group Inc."
    },
    "BLFE": {
        "cik": 1929281,
        "title": "BioLIfe Sciences Inc"
    },
    "PLXPQ": {
        "cik": 1497504,
        "title": "PLx Pharma Winddown Corp."
    },
    "NECA": {
        "cik": 1373853,
        "title": "NEW AMERICA ENERGY CORP."
    },
    "ANSU": {
        "cik": 1168663,
        "title": "AMANASU TECHNO HOLDINGS CORP"
    },
    "SDON": {
        "cik": 892832,
        "title": "SANDSTON CORP"
    },
    "FNHCQ": {
        "cik": 1069996,
        "title": "FedNat Holding Co"
    },
    "HYREQ": {
        "cik": 1713832,
        "title": "HC LIQUIDATING, INC."
    },
    "ATTOF": {
        "cik": 1606457,
        "title": "Atento S.A."
    },
    "FERN": {
        "cik": 1880419,
        "title": "Fernhill Corp"
    },
    "WEIDY": {
        "cik": 1734902,
        "title": "Weidai Ltd."
    },
    "KEGS": {
        "cik": 884380,
        "title": "1812 Brewing Company, Inc."
    },
    "RTON": {
        "cik": 1580262,
        "title": "Right On Brands, Inc."
    },
    "BNCM": {
        "cik": 1384939,
        "title": "BOUNCE MOBILE SYSTEMS, INC."
    },
    "TUEMQ": {
        "cik": 878726,
        "title": "TUESDAY MORNING CORP/DE"
    },
    "ALFIQ": {
        "cik": 1833908,
        "title": "Alfi, Inc."
    },
    "CGAC": {
        "cik": 1444403,
        "title": "CODE GREEN APPAREL CORP"
    },
    "MKDTY": {
        "cik": 1758736,
        "title": "Molecular Data Inc."
    },
    "ONCSQ": {
        "cik": 1444307,
        "title": "ONCOSEC MEDICAL Inc"
    },
    "PGAI": {
        "cik": 81157,
        "title": "PGI INC"
    },
    "MUSS": {
        "cik": 723733,
        "title": "MULTI SOLUTIONS II, INC"
    },
    "GPLDF": {
        "cik": 1300050,
        "title": "GREAT PANTHER MINING Ltd"
    },
    "VTNA": {
        "cik": 1280396,
        "title": "VetaNova Inc."
    },
    "KALRQ": {
        "cik": 1909152,
        "title": "Kalera Public Ltd Co"
    },
    "GTOR": {
        "cik": 1499855,
        "title": "GGTOOR, INC."
    },
    "NFEI": {
        "cik": 1140586,
        "title": "NEW FRONTIER ENERGY INC"
    },
    "CBDL": {
        "cik": 1776073,
        "title": "CBD Life Sciences Inc."
    },
    "CLIS": {
        "cik": 1393548,
        "title": "ClickStream Corp"
    },
    "TWOH": {
        "cik": 1494413,
        "title": "Two Hands Corp"
    },
    "CPMD": {
        "cik": 1081938,
        "title": "CANNAPHARMARX, INC."
    },
    "HBIS": {
        "cik": 1489588,
        "title": "Home Bistro, Inc. /NV/"
    },
    "AFOM": {
        "cik": 1286459,
        "title": "ALL FOR ONE MEDIA CORP."
    },
    "YUKA": {
        "cik": 1886958,
        "title": "Yuka Group Inc"
    },
    "EGOX": {
        "cik": 1942808,
        "title": "Next.e.GO B.V."
    },
    "ZXTY": {
        "cik": 1988979,
        "title": "ZHONGXING HOLDING GROUP LTD"
    },
    "CRML": {
        "cik": 1951089,
        "title": "Critical Metals Corp."
    },
    "SUNH": {
        "cik": 1946025,
        "title": "Xuhang Holdings Ltd"
    },
    "MTEN": {
        "cik": 1948099,
        "title": "Mingteng International Corp Inc."
    },
    "BUJA": {
        "cik": 1956055,
        "title": "Bukit Jalil Global Acquisition 1 Ltd."
    },
    "SPGC": {
        "cik": 1934245,
        "title": "Sacks Parente Golf, Inc."
    },
    "ZTOP": {
        "cik": 1869901,
        "title": "Zi Toprun Acquisition Corp."
    },
    "SN": {
        "cik": 1957132,
        "title": "SharkNinja, Inc."
    },
    "SESG": {
        "cik": 1837824,
        "title": "Sprott ESG Gold ETF"
    },
    "RCIAX": {
        "cik": 1628040,
        "title": "Alternative Credit Income Fund"
    },
    "VRAYQ": {
        "cik": 1597313,
        "title": "ViewRay, Inc."
    },
    "CADCX": {
        "cik": 1678124,
        "title": "CION Ares Diversified Credit Fund"
    },
    "TURO": {
        "cik": 1514587,
        "title": "Turo Inc."
    },
    "USL": {
        "cik": 1405528,
        "title": "United States 12 Month Oil Fund, LP"
    },
    "FDAN": {
        "cik": 1874137,
        "title": "FD TECHNOLOGY INC."
    },
    "NATL": {
        "cik": 1974138,
        "title": "NCR Atleos, LLC"
    },
    "GCGJ": {
        "cik": 1765048,
        "title": "GUOCHUN INTERNATIONAL INC."
    },
    "BGFDX": {
        "cik": 1710523,
        "title": "Blackstone Floating Rate Enhanced Income Fund"
    },
    "JETR": {
        "cik": 1908054,
        "title": "Star Jets International Inc."
    },
    "USEE": {
        "cik": 1970653,
        "title": "USEE ELECTRONIC COMMERCE LTD"
    },
    "ELEP": {
        "cik": 1865833,
        "title": "Elephant Oil Corp."
    },
    "HUHU": {
        "cik": 1945415,
        "title": "HUHUTECH International Group Inc."
    },
    "XPTFX": {
        "cik": 1677615,
        "title": "Federated Hermes Project & Trade Finance Tender Fund"
    },
    "EIC": {
        "cik": 1754836,
        "title": "Eagle Point Income Co Inc."
    },
    "CKHL": {
        "cik": 1923171,
        "title": "Chi Ko Holdings Ltd"
    },
    "BNTY": {
        "cik": 1935398,
        "title": "Bounty Minerals, Inc."
    },
    "YELLQ": {
        "cik": 716006,
        "title": "Yellow Corp"
    },
    "CTWO": {
        "cik": 1958928,
        "title": "COTWO ADVISORS PHYSICAL EUROPEAN CARBON ALLOWANCE TRUST"
    },
    "VACX": {
        "cik": 1865249,
        "title": "Vistas Acquisition Co II Inc."
    },
    "LOBO": {
        "cik": 1932072,
        "title": "LOBO EV TECHNOLOGIES LTD"
    },
    "NNAG": {
        "cik": 1950429,
        "title": "99 Acquisition Group Inc."
    },
    "UNFL": {
        "cik": 1965671,
        "title": "Unifoil Holdings, Inc."
    },
    "HMR": {
        "cik": 1970392,
        "title": "Heidmar Marine Inc."
    },
    "KLG": {
        "cik": 1959348,
        "title": "WK Kellogg Co"
    },
    "YZH": {
        "cik": 1964603,
        "title": "YUEZHONGHUI INTERNATIONAL HOLDINGS GROUP LTD"
    },
    "VITT": {
        "cik": 1960348,
        "title": "Vittoria Ltd"
    },
    "GRAM": {
        "cik": 1876945,
        "title": "Gold Flora Corp."
    },
    "SYRA": {
        "cik": 1922335,
        "title": "Syra Health Corp"
    },
    "UMAV": {
        "cik": 1843573,
        "title": "UAV Corp"
    },
    "ECLP": {
        "cik": 1946412,
        "title": "Eclipse Bancorp, Inc."
    },
    "NTCL": {
        "cik": 1927578,
        "title": "NetClass Technology Inc"
    },
    "ZLS": {
        "cik": 1853397,
        "title": "Zalatoris II Acquisition Corp"
    },
    "EPWK": {
        "cik": 1900720,
        "title": "EPWK Holdings Ltd."
    },
    "MTWO": {
        "cik": 1753373,
        "title": "M2i Global, Inc."
    },
    "XMTI": {
        "cik": 1469038,
        "title": "X Metaverse Inc."
    },
    "SEZL": {
        "cik": 1662991,
        "title": "Sezzle Inc."
    },
    "LNZNY": {
        "cik": 1592651,
        "title": "Lenzing AG/ADR"
    },
    "PFFLX": {
        "cik": 1688554,
        "title": "PIMCO Flexible Credit Income Fund"
    },
    "MXRX": {
        "cik": 1620704,
        "title": "MED-X, INC."
    },
    "EMTX": {
        "cik": 1254348,
        "title": "EMULATE THERAPEUTICS, INC."
    },
    "BNO": {
        "cik": 1472494,
        "title": "United States Brent Oil Fund, LP"
    },
    "GLNS": {
        "cik": 1375348,
        "title": "Golden Star Resource Corp."
    },
    "KTN": {
        "cik": 1283337,
        "title": "STRUCTURED PRODUCTS CORP CRED ENHANCE CORTS TR FOR AON CAP A"
    },
    "ELIQ": {
        "cik": 1827871,
        "title": "Electriq Power Holdings, Inc."
    },
    "WEIX": {
        "cik": 1771951,
        "title": "Dynamic Shares Trust"
    },
    "FTEL": {
        "cik": 1928581,
        "title": "Fitell Corp"
    },
    "NICHX": {
        "cik": 1736510,
        "title": "Variant Alternative Income Fund"
    },
    "ODRS": {
        "cik": 1610718,
        "title": "Outdoor Specialty Products, Inc."
    },
    "GJS": {
        "cik": 1356284,
        "title": "STRATS(SM) Trust for Goldman Sachs Group Securities, Series 2006-2"
    },
    "LBGJ": {
        "cik": 1896425,
        "title": "Li Bang International Corp Inc."
    },
    "MIRA": {
        "cik": 1904286,
        "title": "MIRA PHARMACEUTICALS, INC."
    },
    "PODC": {
        "cik": 1940177,
        "title": "Courtside Group, Inc."
    },
    "PSIG": {
        "cik": 1917890,
        "title": "PSI Group Holdings Ltd."
    },
    "IMSV": {
        "cik": 1936574,
        "title": "IMMRSIV Inc."
    },
    "ADVB": {
        "cik": 1941029,
        "title": "Advanced Biomed Inc."
    },
    "LEWY": {
        "cik": 1888780,
        "title": "LEEWAY SERVICES, INC."
    },
    "AGLY": {
        "cik": 1673504,
        "title": "Atlantis Glory Inc."
    },
    "LGCL": {
        "cik": 1954694,
        "title": "Lucas GC Ltd"
    },
    "UFND": {
        "cik": 1978124,
        "title": "Unifund Financial Technologies, Inc."
    },
    "DVGR": {
        "cik": 1960074,
        "title": "Digital Virgo Group S.A."
    },
    "SCIT": {
        "cik": 1803487,
        "title": "Sancai Holding Group Ltd."
    },
    "ACMSY": {
        "cik": 1850767,
        "title": "Accustem Sciences Inc."
    },
    "CDTG": {
        "cik": 1793895,
        "title": "CDT Environmental Technology Investment Holdings Ltd"
    },
    "STA": {
        "cik": 1975723,
        "title": "HWEL Holdings Corp."
    },
    "RYET": {
        "cik": 1873454,
        "title": "Ruanyun Edai Technology Inc."
    },
    "ALKD": {
        "cik": 1927309,
        "title": "Alkaid Acquisition Corp."
    },
    "DSWR": {
        "cik": 1670196,
        "title": "Deseo Swimwear Inc."
    },
    "BKV": {
        "cik": 1838406,
        "title": "BKV Corp"
    },
    "JTAI": {
        "cik": 1861622,
        "title": "Jet.AI Inc."
    },
    "UNL": {
        "cik": 1405513,
        "title": "United States 12 Month Natural Gas Fund, LP"
    },
    "LVDW": {
        "cik": 1503658,
        "title": "LiquidValue Development Inc."
    },
    "SONG": {
        "cik": 1671132,
        "title": "Music Licensing Inc."
    },
    "MADL": {
        "cik": 1052354,
        "title": "MAN AHL DIVERSIFIED I LP"
    },
    "COPR": {
        "cik": 1263364,
        "title": "Idaho Copper Corp"
    },
    "FXC": {
        "cik": 1353612,
        "title": "Invesco CurrencyShares Canadian Dollar Trust"
    },
    "OUNZ": {
        "cik": 1546652,
        "title": "VanEck Merk Gold Trust"
    },
    "VFS": {
        "cik": 1913510,
        "title": "VinFast Auto Ltd."
    },
    "HGRN": {
        "cik": 1923183,
        "title": "Healthy Green Group Holding Ltd"
    },
    "DCCA": {
        "cik": 1912472,
        "title": "Decca Investment Ltd"
    },
    "GLXY": {
        "cik": 1859392,
        "title": "Galaxy Digital Inc."
    },
    "CRGH": {
        "cik": 1798458,
        "title": "Carriage House Event Center, Inc."
    },
    "GLNK": {
        "cik": 1852025,
        "title": "Grayscale Chainlink Trust (LINK)"
    },
    "RADX": {
        "cik": 1949257,
        "title": "Radiopharm Theranostics Ltd"
    },
    "AEIB": {
        "cik": 1875655,
        "title": "AEI CapForce II Investment Corp"
    },
    "DBD": {
        "cik": 28823,
        "title": "DIEBOLD NIXDORF, Inc"
    },
    "AIMA": {
        "cik": 1903464,
        "title": "Aimfinity Investment Corp. I"
    },
    "PPLT": {
        "cik": 1460235,
        "title": "abrdn Platinum ETF Trust"
    },
    "LENDX": {
        "cik": 1658645,
        "title": "Stone Ridge Trust V"
    },
    "NBND": {
        "cik": 1725911,
        "title": "NetBrands Corp."
    },
    "NRHI": {
        "cik": 1680689,
        "title": "Natural Resource Holdings, Inc."
    },
    "GXLM": {
        "cik": 1761325,
        "title": "Grayscale Stellar Lumens Trust (XLM)"
    },
    "MANA": {
        "cik": 1852023,
        "title": "Grayscale Decentraland Trust (MANA)"
    },
    "GLXG": {
        "cik": 1905920,
        "title": "Galaxy Payroll Group Ltd"
    },
    "JYB": {
        "cik": 1954488,
        "title": "Jyong Biotech Ltd."
    },
    "EXTO": {
        "cik": 1957146,
        "title": "Almacenes Exito S.A."
    },
    "BOWN": {
        "cik": 1973056,
        "title": "Bowen Acquisition Corp"
    },
    "EVOH": {
        "cik": 1700844,
        "title": "EvoAir Holdings Inc."
    },
    "MALG": {
        "cik": 1309251,
        "title": "MICROALLIANCE GROUP INC."
    },
    "NOVNQ": {
        "cik": 1467154,
        "title": "Novan, Inc."
    },
    "GJH": {
        "cik": 1286405,
        "title": "STRATS SM TRUST FOR U S CELL CORP SEC SERIES 2004 6"
    },
    "BOMO": {
        "cik": 1381871,
        "title": "bowmo, Inc."
    },
    "FXB": {
        "cik": 1353611,
        "title": "Invesco CurrencyShares British Pound Sterling Trust"
    },
    "PYT": {
        "cik": 1294808,
        "title": "PPLUS Trust Series GSC-2"
    },
    "CVTO": {
        "cik": 1943661,
        "title": "Covalto Ltd."
    },
    "DEFG": {
        "cik": 1874907,
        "title": "Grayscale Decentralized Finance (DeFi) Fund LLC"
    },
    "TSIFX": {
        "cik": 1725295,
        "title": "Ecofin Tax-Exempt Private Credit Fund, Inc."
    },
    "RVR": {
        "cik": 1891367,
        "title": "REV Renewables, Inc."
    },
    "FPAQ": {
        "cik": 1946485,
        "title": "FPA ENERGY ACQUISITION CORP."
    },
    "LRHC": {
        "cik": 1879403,
        "title": "La Rosa Holdings Corp."
    },
    "BOUW": {
        "cik": 1909142,
        "title": "Boustead Wavefront Inc."
    },
    "MNX": {
        "cik": 1908233,
        "title": "MN8 Energy, Inc."
    },
    "HZEN": {
        "cik": 1748945,
        "title": "Grayscale Horizen Trust (ZEN)"
    },
    "FCCI": {
        "cik": 1807689,
        "title": "FAST CASUAL CONCEPTS, INC."
    },
    "DPUI": {
        "cik": 1791929,
        "title": "DISCOUNT PRINT USA, INC."
    },
    "SAVU": {
        "cik": 1714919,
        "title": "BioLife4D Corp"
    },
    "EXOD": {
        "cik": 1821534,
        "title": "Exodus Movement, Inc."
    },
    "QHI": {
        "cik": 1792799,
        "title": "QINHONG INTERNATIONAL GROUP"
    },
    "SFCO": {
        "cik": 1831523,
        "title": "Southern Financial Corp"
    },
    "KVAC": {
        "cik": 1889983,
        "title": "Keen Vision Acquisition Corp."
    },
    "AITR": {
        "cik": 1966734,
        "title": "AI Transportation Acquisition Corp"
    },
    "LGM": {
        "cik": 1981758,
        "title": "SIXGOMEOW LTD"
    },
    "LDWY": {
        "cik": 875355,
        "title": "LENDWAY, INC."
    },
    "WBUY": {
        "cik": 1946703,
        "title": "WEBUY GLOBAL LTD"
    },
    "CTNT": {
        "cik": 1951667,
        "title": "CHEETAH NET SUPPLY CHAIN SERVICE INC."
    },
    "WXT": {
        "cik": 1905448,
        "title": "Wuxin Technology Holdings, Inc."
    },
    "FXA": {
        "cik": 1353614,
        "title": "Invesco CurrencyShares Australian Dollar Trust"
    },
    "JBK": {
        "cik": 1284143,
        "title": "LEHMAN ABS CORP GOLDMAN SACHS CAP 1 SEC BACKED SER 2004-6"
    },
    "CCIF": {
        "cik": 1517767,
        "title": "Carlyle Credit Income Fund"
    },
    "SRRIX": {
        "cik": 1581005,
        "title": "Stone Ridge Trust II"
    },
    "PRDEX": {
        "cik": 1568905,
        "title": "PREDEX"
    },
    "GXXY": {
        "cik": 1481585,
        "title": "Galexxy Holdings, Inc."
    },
    "VCRRX": {
        "cik": 1687898,
        "title": "Versus Capital Real Assets Fund LLC"
    },
    "XYGJ": {
        "cik": 1885840,
        "title": "Fortune Joy International Acquisition Corp"
    },
    "RMSG": {
        "cik": 1983324,
        "title": "Real Messenger Corp"
    },
    "OMG": {
        "cik": 1970371,
        "title": "Broad Capital Acquisition Pty Ltd"
    },
    "EIOAX": {
        "cik": 1751156,
        "title": "ELLINGTON INCOME OPPORTUNITIES FUND"
    },
    "NISM": {
        "cik": 1956552,
        "title": "Newsight Imaging Ltd."
    },
    "SPPL": {
        "cik": 1948697,
        "title": "SIMPPLE LTD."
    },
    "ONS": {
        "cik": 1810200,
        "title": "ONS Acquisition Corp."
    },
    "TURB": {
        "cik": 1963439,
        "title": "Turbo Energy, S.A."
    },
    "ATCH": {
        "cik": 1963088,
        "title": "Calculator New Pubco, Inc."
    },
    "SGD": {
        "cik": 1959023,
        "title": "Safe & Green Development Corp"
    },
    "CHSCP": {
        "cik": 823277,
        "title": "CHS INC"
    },
    "NRUC": {
        "cik": 70502,
        "title": "NATIONAL RURAL UTILITIES COOPERATIVE FINANCE CORP /DC/"
    },
    "AGII": {
        "cik": 1932470,
        "title": "AgiiPlus Inc."
    },
    "CRVO": {
        "cik": 1053691,
        "title": "CervoMed Inc."
    },
    "ACRU": {
        "cik": 1407573,
        "title": "AmeriCrew Inc."
    },
    "VCMIX": {
        "cik": 1515001,
        "title": "Versus Capital Multi-Manager Real Estate Income Fund LLC"
    },
    "GEMZ": {
        "cik": 1104023,
        "title": "Gemxx Corp."
    },
    "ACIC": {
        "cik": 1401521,
        "title": "AMERICAN COASTAL INSURANCE Corp"
    },
    "NVNI": {
        "cik": 1965143,
        "title": "Nvni Group Ltd"
    },
    "FUPEY": {
        "cik": 1534043,
        "title": "Fuchs Petrolub SE/ADR"
    },
    "PTRAQ": {
        "cik": 1820630,
        "title": "Proterra Inc"
    },
    "ZKH": {
        "cik": 1862044,
        "title": "ZKH Group Ltd"
    },
    "PRZO": {
        "cik": 1916241,
        "title": "ParaZero Technologies Ltd."
    },
    "FMST": {
        "cik": 1935418,
        "title": "Foremost Lithium Resource & Technology Ltd."
    },
    "SUBL": {
        "cik": 1966522,
        "title": "BioLingus (Cayman) Ltd"
    },
    "PSGI": {
        "cik": 1880249,
        "title": "Perfect Solutions Group, Inc."
    },
    "CEAC": {
        "cik": 1916148,
        "title": "CE Energy Acquisition Corp."
    },
    "BCGF": {
        "cik": 1932629,
        "title": "BCGF Acquisition Corp."
    },
    "CJOY": {
        "cik": 1895159,
        "title": "Cine Top Culture Holdings Ltd."
    },
    "FLCT": {
        "cik": 1912287,
        "title": "Felicitex Therapeutics Inc."
    },
    "KPN": {
        "cik": 1826202,
        "title": "Kepuni Holdings Inc."
    },
    "GFR": {
        "cik": 1966287,
        "title": "Greenfire Resources Ltd."
    },
    "SPKL": {
        "cik": 1884046,
        "title": "Spark I Acquisition Corp"
    },
    "GBAT": {
        "cik": 1852040,
        "title": "Grayscale Basic Attention Token Trust (BAT)"
    },
    "VTRO": {
        "cik": 793171,
        "title": "Vitro Biopharma, Inc."
    },
    "BNPZY": {
        "cik": 310732,
        "title": "BNP PARIBAS"
    },
    "ICR-PA": {
        "cik": 1690012,
        "title": "InPoint Commercial Real Estate Income, Inc."
    },
    "YBZN": {
        "cik": 1885514,
        "title": "Yi Po International Holdings Ltd"
    },
    "GLIV": {
        "cik": 1852024,
        "title": "Grayscale Livepeer Trust (LPT)"
    },
    "BITW": {
        "cik": 1723788,
        "title": "Bitwise 10 Crypto Index Fund"
    },
    "AFJK": {
        "cik": 1979005,
        "title": "Aimei Health Technology Co., Ltd."
    },
    "GLDM": {
        "cik": 1618181,
        "title": "World Gold Trust"
    },
    "TIPLX": {
        "cik": 1551047,
        "title": "Bluerock Total Income (plus) Real Estate Fund"
    },
    "CEDAX": {
        "cik": 1722837,
        "title": "BlueBay Destra International Event-Driven Credit Fund"
    },
    "LGCP": {
        "cik": 1661166,
        "title": "Legion Capital Corp"
    },
    "KARX": {
        "cik": 1729637,
        "title": "Karbon-X Corp."
    },
    "WEFCX": {
        "cik": 1586009,
        "title": "Wildermuth Fund"
    },
    "RENB": {
        "cik": 1527728,
        "title": "RENOVARO BIOSCIENCES INC."
    },
    "CBIH": {
        "cik": 1411057,
        "title": "Cannabis Bioscience International Holdings, Inc."
    },
    "FXF": {
        "cik": 1353615,
        "title": "Invesco CurrencyShares Swiss Franc Trust"
    },
    "SAAYY": {
        "cik": 1062750,
        "title": "SAIPEM S P A /FI"
    },
    "CNCL": {
        "cik": 1130889,
        "title": "CANCER CAPITAL CORP"
    },
    "FSHP": {
        "cik": 1850059,
        "title": "Flag Ship Acquisition Corp"
    },
    "XALCX": {
        "cik": 1729678,
        "title": "BNY Mellon Alcentra Global Multi-Strategy Credit Fund, Inc."
    },
    "OPHV": {
        "cik": 1753945,
        "title": "Opti-Harvest, Inc."
    },
    "SKFG": {
        "cik": 1794942,
        "title": "Stark Focus Group, Inc."
    },
    "RVGO": {
        "cik": 1886444,
        "title": "RVELOCITY, INC."
    },
    "CCTG": {
        "cik": 1931717,
        "title": "CCSC Technology International Holdings Ltd"
    },
    "FBGL": {
        "cik": 1938534,
        "title": "FBS Global Ltd"
    },
    "ESGL": {
        "cik": 1957538,
        "title": "ESGL Holdings Ltd"
    },
    "BELR": {
        "cik": 1980034,
        "title": "Bell Rose Capital, Inc."
    },
    "SCRP": {
        "cik": 1912498,
        "title": "Scripps Safe, Inc."
    },
    "MDBH": {
        "cik": 1934642,
        "title": "MDB Capital Holdings, LLC"
    },
    "CDEX": {
        "cik": 1951005,
        "title": "CardieX Ltd"
    },
    "OWSCX": {
        "cik": 1748680,
        "title": "1WS Credit Income Fund"
    },
    "PDSKX": {
        "cik": 1756404,
        "title": "Principal Diversified Select Real Asset Fund"
    },
    "OSTX": {
        "cik": 1795091,
        "title": "OS Therapies Inc"
    },
    "XILSX": {
        "cik": 1616037,
        "title": "Pioneer ILS Interval Fund"
    },
    "RBNK": {
        "cik": 1535665,
        "title": "RiverBank Holding Co"
    },
    "ODDB": {
        "cik": 1949766,
        "title": "Odd Burger Corp"
    },
    "AUMB": {
        "cik": 1957252,
        "title": "AUM Biosciences Ltd"
    },
    "ETZ": {
        "cik": 1883934,
        "title": "Earntz Healthcare Products, Inc."
    },
    "GMM": {
        "cik": 1913749,
        "title": "Global Mofy Metaverse Ltd"
    },
    "CPBI": {
        "cik": 1979332,
        "title": "Central Plains Bancshares, Inc."
    },
    "HBER": {
        "cik": 1958839,
        "title": "HUBEIER GROUP LTD."
    },
    "WDSP": {
        "cik": 1813744,
        "title": "World Scan Project, Inc."
    },
    "CCLFX": {
        "cik": 1735964,
        "title": "Cliffwater Corporate Lending Fund"
    },
    "GC": {
        "cik": 1805586,
        "title": "Gladstone Companies, Inc."
    },
    "ANL": {
        "cik": 1944552,
        "title": "Adlai Nortye Ltd."
    },
    "NWGL": {
        "cik": 1948294,
        "title": "Nature Wood Group Ltd"
    },
    "SMXT": {
        "cik": 1519472,
        "title": "SolarMax Technology, Inc."
    },
    "NBRVF": {
        "cik": 1641640,
        "title": "Nabriva Therapeutics plc"
    },
    "BAR": {
        "cik": 1690437,
        "title": "GraniteShares Gold Trust"
    },
    "CBLO": {
        "cik": 1882781,
        "title": "C2 Blockchain,Inc."
    },
    "GJO": {
        "cik": 1340909,
        "title": "STRATS SM TRUST FOR WAL-MART STORES, INC. SECURITIES, SERIES 2005-4"
    },
    "NREG": {
        "cik": 1552164,
        "title": "Springs Rejuvenation, Inc."
    },
    "SIVR": {
        "cik": 1450922,
        "title": "abrdn Silver ETF Trust"
    },
    "IPB": {
        "cik": 1267332,
        "title": "MERRILL LYNCH DEPOSITOR INC INDEXPLUS TRUST SERIES 2003-1"
    },
    "HHH": {
        "cik": 1981792,
        "title": "Howard Hughes Holdings Inc."
    },
    "BCG": {
        "cik": 1953984,
        "title": "Binah Capital Group, Inc."
    },
    "SVMH": {
        "cik": 1973368,
        "title": "SRIVARU Holding Ltd"
    },
    "FLXG": {
        "cik": 1965044,
        "title": "Flexi Group Holdings Ltd"
    },
    "HIGR": {
        "cik": 1807616,
        "title": "Hi-Great Group Holding Co"
    },
    "QTM": {
        "cik": 1930207,
        "title": "CH AUTO Inc."
    },
    "PFAB": {
        "cik": 1975992,
        "title": "PreTam Holdings Inc."
    },
    "CMCZ": {
        "cik": 1673362,
        "title": "Curtis Mathes Corp"
    },
    "YMAT": {
        "cik": 1875016,
        "title": "J-Star Holding Co., Ltd."
    },
    "RPGL": {
        "cik": 1912884,
        "title": "Republic Power Group Ltd"
    },
    "ICGL": {
        "cik": 1598924,
        "title": "Image Chain Group Limited, Inc."
    },
    "CNRLX": {
        "cik": 1690996,
        "title": "City National Rochdale Select Strategies Fund"
    },
    "PSOIX": {
        "cik": 1608016,
        "title": "Palmer Square Opportunistic Income Fund"
    },
    "GSGG": {
        "cik": 1668523,
        "title": "GSG GROUP INC."
    },
    "SDOT": {
        "cik": 1701756,
        "title": "Sadot Group Inc."
    },
    "RR": {
        "cik": 1963685,
        "title": "RICHTECH ROBOTICS INC."
    },
    "INHD": {
        "cik": 1961847,
        "title": "INNO HOLDINGS INC."
    },
    "SAG": {
        "cik": 1933951,
        "title": "SAG Holdings Ltd"
    },
    "PMEC": {
        "cik": 1891944,
        "title": "Primech Holdings Ltd"
    },
    "FOGO": {
        "cik": 1883631,
        "title": "Fogo Hospitality, Inc."
    },
    "ROMA": {
        "cik": 1945240,
        "title": "Roma Green Finance Ltd"
    },
    "QSJC": {
        "cik": 1753391,
        "title": "TANCHENG GROUP CO., LTD."
    },
    "GPAK": {
        "cik": 1948884,
        "title": "Gamer Pakistan Inc"
    },
    "ALEH": {
        "cik": 1806905,
        "title": "ALE Group Holding Ltd"
    },
    "SRBK": {
        "cik": 1951276,
        "title": "SR Bancorp, Inc."
    },
    "MDLB": {
        "cik": 1940322,
        "title": "Medlab Clinical Ltd."
    },
    "NPCT": {
        "cik": 1835068,
        "title": "Nuveen Core Plus Impact Fund"
    },
    "YIBO": {
        "cik": 1868395,
        "title": "Planet Image International Ltd"
    },
    "SWIN": {
        "cik": 1959224,
        "title": "Solowin Holdings, Ltd."
    },
    "TWEN": {
        "cik": 1926451,
        "title": "T20 HOLDINGS LTD."
    },
    "LBIO": {
        "cik": 1964657,
        "title": "Denali SPAC Holdco, Inc."
    },
    "DDCIU": {
        "cik": 1867506,
        "title": "Diffuse Digital 30, LP"
    },
    "AMGS": {
        "cik": 1974952,
        "title": "Prospect Energy Holdings Corp."
    },
    "AZI": {
        "cik": 1959726,
        "title": "Autozi Internet Technology (Global) Ltd."
    },
    "TKO": {
        "cik": 1973266,
        "title": "New Whale Inc."
    },
    "IBG": {
        "cik": 1924482,
        "title": "Innovation Beverage Group Ltd"
    },
    "CGRD": {
        "cik": 1986500,
        "title": "GRD Biotechnology Acquisition Ltd"
    },
    "NETD": {
        "cik": 1975218,
        "title": "Nabors Energy Transition Corp. II"
    },
    "MSS": {
        "cik": 1892292,
        "title": "Maison Solutions Inc."
    },
    "DRPO": {
        "cik": 1786286,
        "title": "Draganfly Inc."
    },
    "CRGT": {
        "cik": 1958489,
        "title": "Cortigent, Inc."
    },
    "VFLEX": {
        "cik": 1681717,
        "title": "FIRST TRUST ALTERNATIVE OPPORTUNITIES FUND"
    },
    "NCL": {
        "cik": 1923780,
        "title": "Northann Corp."
    },
    "CETI": {
        "cik": 1935092,
        "title": "Cyber Enviro-Tech, Inc."
    },
    "HARD": {
        "cik": 1873723,
        "title": "Harden Technologies Inc."
    },
    "HRYU": {
        "cik": 1911545,
        "title": "Hanryu Holdings, Inc."
    },
    "WETO": {
        "cik": 1941158,
        "title": "Webus International Ltd."
    },
    "ELC": {
        "cik": 1348952,
        "title": "ENTERGY LOUISIANA, LLC"
    },
    "GJT": {
        "cik": 1357660,
        "title": "STRATS(SM) Trust for Allstate Corp Securities, Series 2006-3"
    },
    "MAMA": {
        "cik": 1520358,
        "title": "MamaMancini's Holdings, Inc."
    },
    "OLSI": {
        "cik": 1573901,
        "title": "Origin Life Sciences, Inc."
    },
    "CECL": {
        "cik": 926865,
        "title": "CECIL BANCORP INC"
    },
    "RYNL": {
        "cik": 1283789,
        "title": "Reynaldo's Mexican Food Company, Inc."
    },
    "PALL": {
        "cik": 1459862,
        "title": "abrdn Palladium ETF Trust"
    },
    "TFSA": {
        "cik": 1577134,
        "title": "Terra Income Fund 6, LLC"
    },
    "FCREX": {
        "cik": 1688897,
        "title": "FS Credit Income Fund"
    },
    "SFLM": {
        "cik": 1086313,
        "title": "SFLMaven Corp."
    },
    "AIDG": {
        "cik": 1702015,
        "title": "AIS Holdings Group, Inc."
    },
    "AAIDX": {
        "cik": 1754927,
        "title": "Axonic Alternative Income Fund"
    },
    "ANVI": {
        "cik": 1570132,
        "title": "ANVI GLOBAL HOLDINGS, INC."
    },
    "APPHQ": {
        "cik": 1807707,
        "title": "AppHarvest, Inc."
    },
    "WDHI": {
        "cik": 1826474,
        "title": "Worldwide Diversified Holdings, Inc"
    },
    "MYSN": {
        "cik": 1879293,
        "title": "Myson, Inc."
    },
    "HXHX": {
        "cik": 1936817,
        "title": "Haoxin Holdings Ltd"
    },
    "GOSC": {
        "cik": 1858939,
        "title": "Giant Oak Acquisition Corp"
    },
    "DAZS": {
        "cik": 1967078,
        "title": "DA AI ZHI SHUI INTERNATIONAL HOLDING GROUP LTD"
    },
    "CAPT": {
        "cik": 1967478,
        "title": "Captivision Inc."
    },
    "XYLB": {
        "cik": 1577351,
        "title": "XY Labs, Inc."
    },
    "PGFF": {
        "cik": 1902700,
        "title": "Pioneer Green Farms, Inc."
    },
    "CHRO": {
        "cik": 1919246,
        "title": "Chromocell Therapeutics Corp"
    },
    "PMFAX": {
        "cik": 1723701,
        "title": "PIMCO Flexible Municipal Income Fund"
    },
    "ALUR": {
        "cik": 1964979,
        "title": "ALLURION TECHNOLOGIES, INC."
    },
    "TSIO": {
        "cik": 1900830,
        "title": "Thornburg Strategic Income Opportunities Trust"
    },
    "XPASX": {
        "cik": 1682662,
        "title": "Peachtree Alternative Strategies Fund"
    },
    "NYX": {
        "cik": 1679379,
        "title": "NYIAX, INC."
    },
    "ZLME": {
        "cik": 1489300,
        "title": "Zhanling International Ltd"
    },
    "XCAPX": {
        "cik": 1467631,
        "title": "ACAP Strategic Fund"
    },
    "FLLZ": {
        "cik": 1659207,
        "title": "Fellazo Corp"
    },
    "USQIX": {
        "cik": 1691570,
        "title": "USQ Core Real Estate Fund"
    },
    "BZFL": {
        "cik": 1959304,
        "title": "BOZHI FANGLUE INTERNATIONAL INVESTMENT GROUP CO LTD"
    },
    "PMTM": {
        "cik": 1718271,
        "title": "Prometheum, Inc."
    },
    "ELGP": {
        "cik": 1885493,
        "title": "Elate Group, Inc."
    },
    "NEAT": {
        "cik": 1877332,
        "title": "Noble Education Acquisition Corp."
    },
    "BATXF": {
        "cik": 1883898,
        "title": "Straightup Resources Inc"
    },
    "ATGL": {
        "cik": 1967621,
        "title": "Alpha Technology Group Ltd"
    },
    "DRFY": {
        "cik": 1947971,
        "title": "Droneify Holdings Ltd"
    },
    "ZKGCF": {
        "cik": 1896511,
        "title": "ZKGC New Energy Ltd"
    },
    "JPO": {
        "cik": 1956410,
        "title": "JP Outfitters, Inc."
    },
    "ENGN": {
        "cik": 1980845,
        "title": "enGene Holdings Inc."
    },
    "NTV": {
        "cik": 1947654,
        "title": "Neotv Group Ltd"
    },
    "GSOL": {
        "cik": 1896677,
        "title": "Grayscale Solana Trust (SOL)"
    },
    "FLYF": {
        "cik": 1864776,
        "title": "Flewber Global Inc."
    },
    "SRM": {
        "cik": 1956744,
        "title": "SRM Entertainment, Inc."
    },
    "GELS": {
        "cik": 1920092,
        "title": "Gelteq Ltd"
    },
    "GFCX": {
        "cik": 1937692,
        "title": "GoodFaith Technology Inc."
    },
    "MSTH": {
        "cik": 1790320,
        "title": "Mystic Holdings Inc./NV"
    },
    "GOAI": {
        "cik": 1983736,
        "title": "Eva Live Inc"
    },
    "ILLR": {
        "cik": 1936037,
        "title": "Triller Corp."
    },
    "RPET": {
        "cik": 1841931,
        "title": "New Ruipeng Pet Group Inc."
    },
    "GDLT": {
        "cik": 1947250,
        "title": "Greifenberg Digital Ltd"
    },
    "MDLS": {
        "cik": 1645108,
        "title": "MDNA Life Sciences, Inc."
    },
    "LQR": {
        "cik": 1843165,
        "title": "LQR House Inc."
    },
    "BMNR": {
        "cik": 1829311,
        "title": "BITMINE IMMERSION TECHNOLOGIES, INC."
    },
    "ETHE": {
        "cik": 1725210,
        "title": "Grayscale Ethereum Trust (ETH)"
    },
    "AETHF": {
        "cik": 1639142,
        "title": "Aether Global Innovations Corp."
    },
    "AAAU": {
        "cik": 1708646,
        "title": "Goldman Sachs Physical Gold ETF"
    },
    "OBTC": {
        "cik": 1767057,
        "title": "Osprey Bitcoin Trust"
    },
    "GPLB": {
        "cik": 1392449,
        "title": "Green Planet Bio Engineering Co. Ltd."
    },
    "SGOL": {
        "cik": 1450923,
        "title": "abrdn Gold ETF Trust"
    },
    "UGA": {
        "cik": 1396878,
        "title": "United States Gasoline Fund, LP"
    },
    "OAK-PA": {
        "cik": 1403528,
        "title": "Oaktree Capital Group, LLC"
    },
    "QTTOY": {
        "cik": 1733298,
        "title": "Qutoutiao Inc."
    },
    "VTAK": {
        "cik": 1716621,
        "title": "Ra Medical Systems, Inc."
    },
    "CCG": {
        "cik": 1965473,
        "title": "Cheche Group Inc."
    },
    "ZCSH": {
        "cik": 1720265,
        "title": "Grayscale Zcash Trust (ZEC)"
    },
    "IVP": {
        "cik": 1939365,
        "title": "INSPIRE VETERINARY PARTNERS, INC."
    },
    "IAMR": {
        "cik": 1728162,
        "title": "Medical Industries of the Americas"
    },
    "SEQP": {
        "cik": 1880423,
        "title": "Santana Equestrian Private Financial, LLC"
    },
    "SFWJ": {
        "cik": 1919847,
        "title": "Software Effective Solutions, Corp."
    },
    "AIRE": {
        "cik": 1859199,
        "title": "reAlpha Tech Corp."
    },
    "PSE": {
        "cik": 1913715,
        "title": "Prime Skyline Ltd"
    },
    "MDRI": {
        "cik": 1910053,
        "title": "Midori Group Inc."
    },
    "NRXS": {
        "cik": 1933567,
        "title": "Neuraxis, INC"
    },
    "SLDX": {
        "cik": 1827620,
        "title": "Stella Diagnostics, Inc."
    },
    "FINR": {
        "cik": 1623590,
        "title": "Fintech Scion Ltd"
    },
    "CNROX": {
        "cik": 1737936,
        "title": "City National Rochdale Strategic Credit Fund"
    },
    "APHP": {
        "cik": 1771995,
        "title": "American Picture House Corp"
    },
    "HGIA": {
        "cik": 1868110,
        "title": "HENGGUANG HOLDING CO, Ltd"
    },
    "PLTM": {
        "cik": 1690842,
        "title": "GraniteShares Platinum Trust"
    },
    "ETCG": {
        "cik": 1705181,
        "title": "Grayscale Ethereum Classic Trust (ETC)"
    },
    "TRCC": {
        "cik": 1843875,
        "title": "TRACCOM INC."
    },
    "JDRR": {
        "cik": 1786888,
        "title": "F3 Platform Biologics INC"
    },
    "GTTJ": {
        "cik": 1368757,
        "title": "GTJ REIT, INC."
    },
    "AMRSQ": {
        "cik": 1365916,
        "title": "AMYRIS, INC."
    },
    "RUSA": {
        "cik": 1964801,
        "title": "IWAC HOLDINGS INC."
    },
    "PMC": {
        "cik": 1948370,
        "title": "PIMCO Municipal Credit Income Fund"
    },
    "HAND": {
        "cik": 1987176,
        "title": "Hand in Hand Metaverse Marriage Technology Co., Ltd"
    },
    "JJOC": {
        "cik": 1861733,
        "title": "JJ Opportunity Corp."
    },
    "ZBJ": {
        "cik": 1964246,
        "title": "ZBJ FINANCE GROUP LTD"
    },
    "MSBB": {
        "cik": 1967306,
        "title": "Mercer Bancorp, Inc."
    },
    "JZL": {
        "cik": 1987930,
        "title": "JIZHILONG HOLDING GROUP LTD"
    },
    "FROPX": {
        "cik": 1732078,
        "title": "Flat Rock Opportunity Fund"
    },
    "BDS": {
        "cik": 1831833,
        "title": "Building DreamStar Technology Inc."
    },
    "AVRW": {
        "cik": 1643301,
        "title": "Avenir Wellness Solutions, Inc."
    },
    "UBXG": {
        "cik": 1888525,
        "title": "U-BX Technology Ltd."
    },
    "WIN": {
        "cik": 1954269,
        "title": "Garden Stage Ltd"
    },
    "FGDL": {
        "cik": 1858258,
        "title": "Franklin Templeton Holdings Trust"
    },
    "AQUB": {
        "cik": 1863974,
        "title": "Aquarius II Acquisition Corp."
    },
    "TDRK": {
        "cik": 1282496,
        "title": "TIDEROCK COMPANIES, INC."
    },
    "KTH": {
        "cik": 1283464,
        "title": "STRUCTURED PRODUCTS CORP CORTS TR FOR PECO ENERGY CAP TR III"
    },
    "SMST": {
        "cik": 1585389,
        "title": "SmartStop Self Storage REIT, Inc."
    },
    "XGEIX": {
        "cik": 1642563,
        "title": "Guggenheim Energy & Income Fund"
    },
    "KBSG": {
        "cik": 1631256,
        "title": "KBS Growth & Income REIT, Inc."
    },
    "YAMHY": {
        "cik": 1447100,
        "title": "Yamaha Motor Co., Ltd."
    },
    "GJP": {
        "cik": 1343491,
        "title": "STRATS(SM) TRUST FOR DOMINION RESOURCES, INC. SECURITIES, SERIES 2005-6"
    },
    "GLTR": {
        "cik": 1483386,
        "title": "abrdn Precious Metals Basket ETF Trust"
    },
    "LQLY": {
        "cik": 1787123,
        "title": "QLY Biotech Group Corp."
    },
    "EAWC": {
        "cik": 1686515,
        "title": "Ecco Auto World Corp"
    },
    "TDAI": {
        "cik": 1904958,
        "title": "Thornburg Durable Allocation & Income Trust"
    },
    "DXYZ": {
        "cik": 1843974,
        "title": "Destiny Tech100 Inc."
    },
    "EEW": {
        "cik": 1949712,
        "title": "ClimateRock Holdings Ltd"
    },
    "LRE": {
        "cik": 1888980,
        "title": "LEAD REAL ESTATE CO., LTD"
    },
    "WETH": {
        "cik": 1826660,
        "title": "Wetouch Technology Inc."
    },
    "MDRN": {
        "cik": 1898722,
        "title": "Modern Mining Technology Corp."
    },
    "TLSI": {
        "cik": 1826667,
        "title": "TriSalus Life Sciences, Inc."
    },
    "BRNI": {
        "cik": 1851651,
        "title": "Beroni Group Ltd"
    },
    "NRSAX": {
        "cik": 1663712,
        "title": "NEXPOINT REAL ESTATE STRATEGIES FUND"
    },
    "THNK": {
        "cik": 1804189,
        "title": "T1V, Inc."
    },
    "LIAI": {
        "cik": 1887799,
        "title": "LEMENG HOLDINGS LTD"
    },
    "PGRM": {
        "cik": 1884434,
        "title": "Panagram Capital, LLC"
    },
    "WOK": {
        "cik": 1929783,
        "title": "WORK Medical Technology Group LTD"
    },
    "TRSG": {
        "cik": 1943444,
        "title": "Tungray Technologies Inc"
    },
    "IAUM": {
        "cik": 1759124,
        "title": "iShares Gold Trust Micro"
    },
    "NCNC": {
        "cik": 1964021,
        "title": "Prime Number Holding Ltd"
    },
    "NBBK": {
        "cik": 1979330,
        "title": "NB Bancorp, Inc."
    },
    "ULY": {
        "cik": 1603652,
        "title": "Urgent.ly Inc."
    },
    "ADOB": {
        "cik": 1726822,
        "title": "Soul Biotechnology Corp"
    },
    "GLE": {
        "cik": 1908705,
        "title": "Global Engine Group Holding Ltd"
    },
    "INTM": {
        "cik": 1835104,
        "title": "INTERMEDIA CLOUD COMMUNICATIONS, INC."
    },
    "LARAX": {
        "cik": 1753712,
        "title": "Lord Abbett Credit Opportunities Fund"
    },
    "MNGA": {
        "cik": 1956401,
        "title": "MNG Havayollari ve Tasimacilik A.S."
    },
    "ASPP": {
        "cik": 1906195,
        "title": "Abri SPAC 2, Inc."
    },
    "RLND": {
        "cik": 1924064,
        "title": "RoyaLand Co Ltd."
    },
    "ABLV": {
        "cik": 1957489,
        "title": "Able View Global Inc."
    },
    "VLTO": {
        "cik": 1967680,
        "title": "Veralto Corp"
    },
    "ETI-P": {
        "cik": 1427437,
        "title": "ENTERGY TEXAS, INC."
    },
    "GJR": {
        "cik": 1353226,
        "title": "STRATS(SM) Trust for Procter & Gamble Securities, Series 2006-1"
    },
    "UUP": {
        "cik": 1383151,
        "title": "Invesco DB US Dollar Index Bullish Fund"
    },
    "MNKA": {
        "cik": 1062128,
        "title": "Manuka, Inc."
    },
    "XSIAX": {
        "cik": 1124959,
        "title": "VOYA CREDIT INCOME FUND"
    },
    "MI": {
        "cik": 1958713,
        "title": "NFT Ltd"
    },
    "AVAI": {
        "cik": 1740797,
        "title": "AVANT TECHNOLOGIES INC."
    },
    "WEIB": {
        "cik": 1717976,
        "title": "Weiss Strategic Interval Fund"
    },
    "FBYD": {
        "cik": 1937987,
        "title": "Falcon's Beyond Global, Inc."
    },
    "SAGN": {
        "cik": 1639953,
        "title": "Sagoon Inc."
    },
    "LTAFX": {
        "cik": 1496254,
        "title": "Alternative Strategies Fund"
    },
    "HTIA": {
        "cik": 1561032,
        "title": "Healthcare Trust, Inc."
    },
    "XJET": {
        "cik": 1960081,
        "title": "XJet Ltd."
    },
    "EHGO": {
        "cik": 1879754,
        "title": "EShallGo Inc."
    },
    "JR": {
        "cik": 1952202,
        "title": "JINRONG HOLDINGS LTD."
    },
    "BSME": {
        "cik": 1905951,
        "title": "MED EIBY Holding Co., Ltd"
    },
    "DTCK": {
        "cik": 1949478,
        "title": "DAVIS COMMODITIES Ltd"
    },
    "TPTA": {
        "cik": 1674356,
        "title": "Terra Property Trust, Inc."
    },
    "ZAAG": {
        "cik": 1893124,
        "title": "ZA Group, Inc."
    },
    "VOCO": {
        "cik": 1880431,
        "title": "Vocodia Holdings Corp"
    },
    "FP": {
        "cik": 1900035,
        "title": "First Person Ltd."
    },
    "UMAC": {
        "cik": 1956955,
        "title": "Unusual Machines, Inc."
    },
    "NMTRQ": {
        "cik": 1551986,
        "title": "9 METERS BIOPHARMA, INC."
    },
    "VSME": {
        "cik": 1951294,
        "title": "VS MEDIA Holdings Ltd"
    },
    "PXDT": {
        "cik": 1962845,
        "title": "PIXIE DUST TECHNOLOGIES, INC."
    },
    "ASCIX": {
        "cik": 1716885,
        "title": "Angel Oak Strategic Credit Fund"
    },
    "PAPL": {
        "cik": 1938109,
        "title": "Pineapple Financial Inc."
    },
    "LVER": {
        "cik": 1932244,
        "title": "Lever Global Corp"
    },
    "SOSH": {
        "cik": 1861785,
        "title": "SOS Hydration Inc."
    },
    "CGTH": {
        "cik": 1967822,
        "title": "Creative Global Technology Holdings Ltd"
    },
    "MPH": {
        "cik": 1133519,
        "title": "MEDICURE INC"
    },
    "UDN": {
        "cik": 1383149,
        "title": "INVESCO DB US DOLLAR INDEX BEARISH FUND"
    },
    "QVCD": {
        "cik": 1254699,
        "title": "QVC INC"
    },
    "INTJ": {
        "cik": 1916416,
        "title": "Intelligent Group Ltd"
    },
    "ZDYM": {
        "cik": 1988932,
        "title": "ZHIDING YUEMEI TECHNOLOGY CO., LTD"
    },
    "MJID": {
        "cik": 1897532,
        "title": "Majestic Ideal Holdings Ltd"
    },
    "CPRDX": {
        "cik": 1762562,
        "title": "Clarion Partners Real Estate Income Fund Inc."
    },
    "RISE": {
        "cik": 1914513,
        "title": "Rise Oil & Gas, Inc."
    },
    "BGAC": {
        "cik": 1916902,
        "title": "Biotech Group Acquisition Corp"
    },
    "VSTE": {
        "cik": 1964630,
        "title": "Vast Solar Pty Ltd"
    },
    "JBS": {
        "cik": 1791942,
        "title": "JBS B.V."
    },
    "HLST": {
        "cik": 1944977,
        "title": "Holisto Ltd."
    },
    "PDPG": {
        "cik": 1902930,
        "title": "Performance Drink Group, Inc."
    },
    "BTRY": {
        "cik": 1857971,
        "title": "Clarios International Inc."
    },
    "SKUR": {
        "cik": 1771755,
        "title": "Sekur Private Data Ltd."
    },
    "CTBB": {
        "cik": 68622,
        "title": "QWEST CORP"
    },
    "GOOG": {
        "cik": 1652044,
        "title": "Alphabet Inc."
    },
    "USB-PA": {
        "cik": 36104,
        "title": "US BANCORP \\DE\\"
    },
    "BRK-A": {
        "cik": 1067983,
        "title": "BERKSHIRE HATHAWAY INC"
    },
    "LVMHF": {
        "cik": 824046,
        "title": "LVMH MOET HENNESSY LOUIS VUITTON"
    },
    "NONOF": {
        "cik": 353278,
        "title": "NOVO NORDISK A S"
    },
    "JPM-PD": {
        "cik": 19617,
        "title": "JPMORGAN CHASE & CO"
    },
    "BML-PG": {
        "cik": 70858,
        "title": "BANK OF AMERICA CORP /DE/"
    },
    "BML-PH": {
        "cik": 70858,
        "title": "BANK OF AMERICA CORP /DE/"
    },
    "ASMLF": {
        "cik": 937966,
        "title": "ASML HOLDING NV"
    },
    "BAC-PE": {
        "cik": 70858,
        "title": "BANK OF AMERICA CORP /DE/"
    },
    "BML-PJ": {
        "cik": 70858,
        "title": "BANK OF AMERICA CORP /DE/"
    },
    "BABAF": {
        "cik": 1577552,
        "title": "Alibaba Group Holding Ltd"
    },
    "NVSEF": {
        "cik": 1114448,
        "title": "NOVARTIS AG"
    },
    "AZNCF": {
        "cik": 901832,
        "title": "ASTRAZENECA PLC"
    },
    "RYDAF": {
        "cik": 1306965,
        "title": "Shell plc"
    },
    "WFC-PQ": {
        "cik": 72971,
        "title": "WELLS FARGO & COMPANY/MN"
    },
    "PCCYF": {
        "cik": 1108329,
        "title": "PETROCHINA CO LTD"
    },
    "WFC-PR": {
        "cik": 72971,
        "title": "WELLS FARGO & COMPANY/MN"
    },
    "WFC-PY": {
        "cik": 72971,
        "title": "WELLS FARGO & COMPANY/MN"
    },
    "SAPGF": {
        "cik": 1000184,
        "title": "SAP SE"
    },
    "TTFNF": {
        "cik": 879764,
        "title": "TotalEnergies SE"
    },
    "HBCYF": {
        "cik": 1089113,
        "title": "HSBC HOLDINGS PLC"
    },
    "BHPLF": {
        "cik": 811809,
        "title": "BHP Group Ltd"
    },
    "SNYNF": {
        "cik": 1121404,
        "title": "Sanofi"
    },
    "WFC-PC": {
        "cik": 72971,
        "title": "WELLS FARGO & COMPANY/MN"
    },
    "EADSF": {
        "cik": 1378580,
        "title": "Airbus SE/ADR"
    },
    "SNEJF": {
        "cik": 313838,
        "title": "Sony Group Corp"
    },
    "DGEAF": {
        "cik": 835403,
        "title": "DIAGEO PLC"
    },
    "RY-PT": {
        "cik": 1000275,
        "title": "ROYAL BANK OF CANADA"
    },
    "CILJF": {
        "cik": 1268896,
        "title": "CHINA LIFE INSURANCE CO LTD"
    },
    "CMXHF": {
        "cik": 1274152,
        "title": "CSL LTD"
    },
    "MBGAF": {
        "cik": 1067318,
        "title": "DAIMLER AG"
    },
    "BNPQY": {
        "cik": 310732,
        "title": "BNP PARIBAS"
    },
    "GS-PA": {
        "cik": 886982,
        "title": "GOLDMAN SACHS GROUP INC"
    },
    "MS-PA": {
        "cik": 895421,
        "title": "MORGAN STANLEY"
    },
    "BTAFF": {
        "cik": 1303523,
        "title": "British American Tobacco p.l.c."
    },
    "GS-PD": {
        "cik": 886982,
        "title": "GOLDMAN SACHS GROUP INC"
    },
    "GLAXF": {
        "cik": 1131399,
        "title": "GSK plc"
    },
    "GS-PJ": {
        "cik": 886982,
        "title": "GOLDMAN SACHS GROUP INC"
    },
    "TOELF": {
        "cik": 1443276,
        "title": "Tokyo Electron LTD"
    },
    "ABLZF": {
        "cik": 1091587,
        "title": "ABB LTD"
    },
    "ESOCF": {
        "cik": 1096200,
        "title": "ENEL SOCIETA PER AZIONI"
    },
    "MS-PI": {
        "cik": 895421,
        "title": "MORGAN STANLEY"
    },
    "MS-PF": {
        "cik": 895421,
        "title": "MORGAN STANLEY"
    },
    "BCDRF": {
        "cik": 891478,
        "title": "Banco Santander, S.A."
    },
    "GS-PK": {
        "cik": 886982,
        "title": "GOLDMAN SACHS GROUP INC"
    },
    "ATLCY": {
        "cik": 748954,
        "title": "ATLAS COPCO AB"
    },
    "DUK-PA": {
        "cik": 1326160,
        "title": "Duke Energy CORP"
    },
    "SCHW-PD": {
        "cik": 316709,
        "title": "SCHWAB CHARLES CORP"
    },
    "AIG-PA": {
        "cik": 5272,
        "title": "AMERICAN INTERNATIONAL GROUP, INC."
    },
    "BAESF": {
        "cik": 895564,
        "title": "BAE SYSTEMS PLC /FI/"
    },
    "PSA-PK": {
        "cik": 1393311,
        "title": "Public Storage"
    },
    "ALL-PH": {
        "cik": 899051,
        "title": "ALLSTATE CORP"
    },
    "ALL-PB": {
        "cik": 899051,
        "title": "ALLSTATE CORP"
    },
    "FNCTF": {
        "cik": 1038143,
        "title": "ORANGE"
    },
    "VODPF": {
        "cik": 839923,
        "title": "VODAFONE GROUP PUBLIC LTD CO"
    },
    "SOJC": {
        "cik": 92122,
        "title": "SOUTHERN CO"
    },
    "TEFOF": {
        "cik": 814052,
        "title": "TELEFONICA S A"
    },
    "DLR-PJ": {
        "cik": 1297996,
        "title": "DIGITAL REALTY TRUST, INC."
    },
    "NOKBF": {
        "cik": 924613,
        "title": "NOKIA CORP"
    },
    "FCNCB": {
        "cik": 798941,
        "title": "FIRST CITIZENS BANCSHARES INC /DE/"
    },
    "HEI-A": {
        "cik": 46619,
        "title": "HEICO CORP"
    },
    "HIG-PG": {
        "cik": 874766,
        "title": "HARTFORD FINANCIAL SERVICES GROUP, INC."
    },
    "FITBI": {
        "cik": 35527,
        "title": "FIFTH THIRD BANCORP"
    },
    "EBR-B": {
        "cik": 1439124,
        "title": "BRAZILIAN ELECTRIC POWER CO"
    },
    "FOX": {
        "cik": 1754301,
        "title": "Fox Corp"
    },
    "FWONK": {
        "cik": 1560385,
        "title": "Liberty Media Corp"
    },
    "HUNGF": {
        "cik": 929058,
        "title": "HUANENG POWER INTERNATIONAL INC"
    },
    "FWONA": {
        "cik": 1560385,
        "title": "Liberty Media Corp"
    },
    "CFG-PD": {
        "cik": 759944,
        "title": "CITIZENS FINANCIAL GROUP INC/RI"
    },
    "NLY-PG": {
        "cik": 1043219,
        "title": "ANNALY CAPITAL MANAGEMENT INC"
    },
    "NLY-PF": {
        "cik": 1043219,
        "title": "ANNALY CAPITAL MANAGEMENT INC"
    },
    "LNVGF": {
        "cik": 932477,
        "title": "LENOVO GROUP LTD"
    },
    "ACGLO": {
        "cik": 947484,
        "title": "ARCH CAPITAL GROUP LTD."
    },
    "FMCCT": {
        "cik": 1026214,
        "title": "FEDERAL HOME LOAN MORTGAGE CORP"
    },
    "KEY-PJ": {
        "cik": 91576,
        "title": "KEYCORP /NEW/"
    },
    "NWS": {
        "cik": 1564708,
        "title": "NEWS CORP"
    },
    "Z": {
        "cik": 1617640,
        "title": "ZILLOW GROUP, INC."
    },
    "CXMSF": {
        "cik": 1076378,
        "title": "CEMEX SAB DE CV"
    },
    "NI-PB": {
        "cik": 1111711,
        "title": "NISOURCE INC."
    },
    "VIVEF": {
        "cik": 1127055,
        "title": "VIVENDI"
    },
    "AGNCN": {
        "cik": 1423689,
        "title": "AGNC Investment Corp."
    },
    "CIG-C": {
        "cik": 1157557,
        "title": "ENERGY CO OF MINAS GERAIS"
    },
    "RZB": {
        "cik": 898174,
        "title": "REINSURANCE GROUP OF AMERICA INC"
    },
    "FRT-PC": {
        "cik": 34903,
        "title": "FEDERAL REALTY INVESTMENT TRUST"
    },
    "LBTYK": {
        "cik": 1570585,
        "title": "Liberty Global plc"
    },
    "GS-PC": {
        "cik": 886982,
        "title": "GOLDMAN SACHS GROUP INC"
    },
    "AGNCM": {
        "cik": 1423689,
        "title": "AGNC Investment Corp."
    },
    "LSXMK": {
        "cik": 1560385,
        "title": "Liberty Media Corp"
    },
    "AMH-PH": {
        "cik": 1562401,
        "title": "American Homes 4 Rent"
    },
    "AMH-PG": {
        "cik": 1562401,
        "title": "American Homes 4 Rent"
    },
    "KIM-PM": {
        "cik": 879101,
        "title": "KIMCO REALTY CORP"
    },
    "RNR-PF": {
        "cik": 913144,
        "title": "RENAISSANCERE HOLDINGS LTD"
    },
    "KIM-PL": {
        "cik": 879101,
        "title": "KIMCO REALTY CORP"
    },
    "VOYA-PB": {
        "cik": 1535929,
        "title": "Voya Financial, Inc."
    },
    "ATH-PA": {
        "cik": 1527469,
        "title": "Athene Holding Ltd"
    },
    "UNVR": {
        "cik": 1494319,
        "title": "Univar Solutions Inc."
    },
    "PCG-PA": {
        "cik": 1004980,
        "title": "PG&E Corp"
    },
    "OAK-PB": {
        "cik": 1403528,
        "title": "Oaktree Capital Group, LLC"
    },
    "UNMA": {
        "cik": 5513,
        "title": "Unum Group"
    },
    "SLG-PI": {
        "cik": 1040971,
        "title": "SL GREEN REALTY CORP"
    },
    "JSM": {
        "cik": 1593538,
        "title": "NAVIENT CORP"
    },
    "SNV-PD": {
        "cik": 18349,
        "title": "SYNOVUS FINANCIAL CORP"
    },
    "PCG-PB": {
        "cik": 1004980,
        "title": "PG&E Corp"
    },
    "CWEN-A": {
        "cik": 1567683,
        "title": "Clearway Energy, Inc."
    },
    "GAB-PG": {
        "cik": 794685,
        "title": "GABELLI EQUITY TRUST INC"
    },
    "EPR-PG": {
        "cik": 1045450,
        "title": "EPR PROPERTIES"
    },
    "PCG-PE": {
        "cik": 1004980,
        "title": "PG&E Corp"
    },
    "AUOTY": {
        "cik": 1172494,
        "title": "AU OPTRONICS CORP"
    },
    "THNPY": {
        "cik": 1792045,
        "title": "Technip Energies N.V."
    },
    "HHC": {
        "cik": 1498828,
        "title": "Howard Hughes Corp"
    },
    "SR-PA": {
        "cik": 1126956,
        "title": "SPIRE INC"
    },
    "REXR-PB": {
        "cik": 1571283,
        "title": "Rexford Industrial Realty, Inc."
    },
    "EQC-PD": {
        "cik": 803649,
        "title": "Equity Commonwealth"
    },
    "BHFAP": {
        "cik": 1685040,
        "title": "Brighthouse Financial, Inc."
    },
    "SAPMY": {
        "cik": 1062750,
        "title": "SAIPEM S P A /FI"
    },
    "ESGRO": {
        "cik": 1363829,
        "title": "Enstar Group LTD"
    },
    "SF-PB": {
        "cik": 720672,
        "title": "STIFEL FINANCIAL CORP"
    },
    "SRC-PA": {
        "cik": 1308606,
        "title": "SPIRIT REALTY CAPITAL, INC."
    },
    "RUSHB": {
        "cik": 1012019,
        "title": "RUSH ENTERPRISES INC TX"
    },
    "NS-PB": {
        "cik": 1110805,
        "title": "NuStar Energy L.P."
    },
    "PBI-PB": {
        "cik": 78814,
        "title": "PITNEY BOWES INC /DE/"
    },
    "GEF-B": {
        "cik": 43920,
        "title": "GREIF, INC"
    },
    "NS-PA": {
        "cik": 1110805,
        "title": "NuStar Energy L.P."
    },
    "FNMAH": {
        "cik": 310522,
        "title": "FEDERAL NATIONAL MORTGAGE ASSOCIATION FANNIE MAE"
    },
    "UA": {
        "cik": 1336917,
        "title": "Under Armour, Inc."
    },
    "WTFCM": {
        "cik": 1015328,
        "title": "WINTRUST FINANCIAL CORP"
    },
    "TWO-PC": {
        "cik": 1465740,
        "title": "TWO HARBORS INVESTMENT CORP."
    },
    "FNMAS": {
        "cik": 310522,
        "title": "FEDERAL NATIONAL MORTGAGE ASSOCIATION FANNIE MAE"
    },
    "FNMFN": {
        "cik": 310522,
        "title": "FEDERAL NATIONAL MORTGAGE ASSOCIATION FANNIE MAE"
    },
    "CIM-PB": {
        "cik": 1409493,
        "title": "CHIMERA INVESTMENT CORP"
    },
    "ARNC": {
        "cik": 1790982,
        "title": "Arconic Corp"
    },
    "CIM-PD": {
        "cik": 1409493,
        "title": "CHIMERA INVESTMENT CORP"
    },
    "FNMAJ": {
        "cik": 310522,
        "title": "FEDERAL NATIONAL MORTGAGE ASSOCIATION FANNIE MAE"
    },
    "CIM-PC": {
        "cik": 1409493,
        "title": "CHIMERA INVESTMENT CORP"
    },
    "TWO-PA": {
        "cik": 1465740,
        "title": "TWO HARBORS INVESTMENT CORP."
    },
    "TWO-PB": {
        "cik": 1465740,
        "title": "TWO HARBORS INVESTMENT CORP."
    },
    "FUPBY": {
        "cik": 1534043,
        "title": "Fuchs Petrolub SE/ADR"
    },
    "HOVNP": {
        "cik": 357294,
        "title": "HOVNANIAN ENTERPRISES INC"
    },
    "TY-P": {
        "cik": 99614,
        "title": "TRI-CONTINENTAL CORP"
    },
    "MFA-PB": {
        "cik": 1055160,
        "title": "MFA FINANCIAL, INC."
    },
    "VLYPP": {
        "cik": 714310,
        "title": "VALLEY NATIONAL BANCORP"
    },
    "AKO-B": {
        "cik": 925261,
        "title": "ANDINA BOTTLING CO INC"
    },
    "NS-PC": {
        "cik": 1110805,
        "title": "NuStar Energy L.P."
    },
    "BATRK": {
        "cik": 1958140,
        "title": "Atlanta Braves Holdings, Inc."
    },
    "CIXXF": {
        "cik": 1829948,
        "title": "CI Financial Corp."
    },
    "SRG-PA": {
        "cik": 1628063,
        "title": "Seritage Growth Properties"
    },
    "TRTN-PA": {
        "cik": 1660734,
        "title": "Triton International Ltd"
    },
    "CENTA": {
        "cik": 887733,
        "title": "CENTRAL GARDEN & PET CO"
    },
    "ASB-PE": {
        "cik": 7789,
        "title": "ASSOCIATED BANC-CORP"
    },
    "LDDD": {
        "cik": 1892316,
        "title": "Longduoduo Co Ltd"
    },
    "LILAK": {
        "cik": 1712184,
        "title": "Liberty Latin America Ltd."
    },
    "AGM-A": {
        "cik": 845877,
        "title": "FEDERAL AGRICULTURAL MORTGAGE CORP"
    },
    "NGL-PB": {
        "cik": 1504461,
        "title": "NGL Energy Partners LP"
    },
    "IVR-PC": {
        "cik": 1437071,
        "title": "Invesco Mortgage Capital Inc."
    },
    "FMCKL": {
        "cik": 1026214,
        "title": "FEDERAL HOME LOAN MORTGAGE CORP"
    },
    "LGF-B": {
        "cik": 929351,
        "title": "LIONS GATE ENTERTAINMENT CORP /CN/"
    },
    "FMCKI": {
        "cik": 1026214,
        "title": "FEDERAL HOME LOAN MORTGAGE CORP"
    },
    "FMCCI": {
        "cik": 1026214,
        "title": "FEDERAL HOME LOAN MORTGAGE CORP"
    },
    "FMCCG": {
        "cik": 1026214,
        "title": "FEDERAL HOME LOAN MORTGAGE CORP"
    },
    "FMCCL": {
        "cik": 1026214,
        "title": "FEDERAL HOME LOAN MORTGAGE CORP"
    },
    "FMCCJ": {
        "cik": 1026214,
        "title": "FEDERAL HOME LOAN MORTGAGE CORP"
    },
    "MHLA": {
        "cik": 1412100,
        "title": "Maiden Holdings, Ltd."
    },
    "GAB-PH": {
        "cik": 794685,
        "title": "GABELLI EQUITY TRUST INC"
    },
    "GLOG-PA": {
        "cik": 1534126,
        "title": "GasLog Ltd."
    },
    "GNL-PA": {
        "cik": 1526113,
        "title": "Global Net Lease, Inc."
    },
    "HCXY": {
        "cik": 1280784,
        "title": "Hercules Capital, Inc."
    },
    "CODI-PA": {
        "cik": 1345126,
        "title": "Compass Diversified Holdings"
    },
    "NYMTN": {
        "cik": 1273685,
        "title": "NEW YORK MORTGAGE TRUST INC"
    },
    "AHL-PD": {
        "cik": 1267395,
        "title": "ASPEN INSURANCE HOLDINGS LTD"
    },
    "GLOP-PB": {
        "cik": 1598655,
        "title": "GasLog Partners LP"
    },
    "FRG": {
        "cik": 1528930,
        "title": "Franchise Group, Inc."
    },
    "AHH-PA": {
        "cik": 1569187,
        "title": "Armada Hoffler Properties, Inc."
    },
    "GLOP-PC": {
        "cik": 1598655,
        "title": "GasLog Partners LP"
    },
    "IIPR-PA": {
        "cik": 1677576,
        "title": "INNOVATIVE INDUSTRIAL PROPERTIES INC"
    },
    "INN-PE": {
        "cik": 1497645,
        "title": "Summit Hotel Properties, Inc."
    },
    "GAM-PB": {
        "cik": 40417,
        "title": "GENERAL AMERICAN INVESTORS CO INC"
    },
    "UBP": {
        "cik": 1029800,
        "title": "URSTADT BIDDLE PROPERTIES INC"
    },
    "UBA": {
        "cik": 1029800,
        "title": "URSTADT BIDDLE PROPERTIES INC"
    },
    "FSUN": {
        "cik": 1709442,
        "title": "FIRSTSUN CAPITAL BANCORP"
    },
    "AGM-PC": {
        "cik": 845877,
        "title": "FEDERAL AGRICULTURAL MORTGAGE CORP"
    },
    "AGM-PD": {
        "cik": 845877,
        "title": "FEDERAL AGRICULTURAL MORTGAGE CORP"
    },
    "UBP-PH": {
        "cik": 1029800,
        "title": "URSTADT BIDDLE PROPERTIES INC"
    },
    "AIC": {
        "cik": 1209028,
        "title": "Arlington Asset Investment Corp."
    },
    "BELFB": {
        "cik": 729580,
        "title": "BEL FUSE INC /NJ"
    },
    "CMRE-PB": {
        "cik": 1503584,
        "title": "Costamare Inc."
    },
    "CMRE-PC": {
        "cik": 1503584,
        "title": "Costamare Inc."
    },
    "KDSKF": {
        "cik": 1339422,
        "title": "Royal DSM N.V."
    },
    "CMRE-PD": {
        "cik": 1503584,
        "title": "Costamare Inc."
    },
    "HT-PD": {
        "cik": 1063344,
        "title": "HERSHA HOSPITALITY TRUST"
    },
    "CMRE-PE": {
        "cik": 1503584,
        "title": "Costamare Inc."
    },
    "GGT-PE": {
        "cik": 921671,
        "title": "GABELLI MULTIMEDIA TRUST INC."
    },
    "GGN-PB": {
        "cik": 1313510,
        "title": "GAMCO Global Gold, Natural Resources & Income Trust"
    },
    "DGICB": {
        "cik": 800457,
        "title": "DONEGAL GROUP INC"
    },
    "BH": {
        "cik": 1726173,
        "title": "Biglari Holdings Inc."
    },
    "AIRTP": {
        "cik": 353184,
        "title": "AIR T INC"
    },
    "GAMI": {
        "cik": 1060349,
        "title": "GAMCO INVESTORS, INC. ET AL"
    },
    "CPAA": {
        "cik": 1841137,
        "title": "Conyers Park III Acquisition Corp."
    },
    "UMH-PD": {
        "cik": 752642,
        "title": "UMH PROPERTIES, INC."
    },
    "GOODO": {
        "cik": 1234006,
        "title": "GLADSTONE COMMERCIAL CORP"
    },
    "ECCX": {
        "cik": 1604174,
        "title": "Eagle Point Credit Co Inc."
    },
    "NCV-PA": {
        "cik": 1214935,
        "title": "Virtus Convertible & Income Fund"
    },
    "MBINP": {
        "cik": 1629019,
        "title": "Merchants Bancorp"
    },
    "OXLCO": {
        "cik": 1495222,
        "title": "Oxford Lane Capital Corp."
    },
    "GMRE-PA": {
        "cik": 1533615,
        "title": "Global Medical REIT Inc."
    },
    "QRTEB": {
        "cik": 1355096,
        "title": "Qurate Retail, Inc."
    },
    "MITT-PA": {
        "cik": 1514281,
        "title": "AG Mortgage Investment Trust, Inc."
    },
    "SPLP-PA": {
        "cik": 1452857,
        "title": "STEEL PARTNERS HOLDINGS L.P."
    },
    "BRCHF": {
        "cik": 1887388,
        "title": "Brainchip Holdings Limited/ADR"
    },
    "GSCCF": {
        "cik": 1896084,
        "title": "ioneer Ltd"
    },
    "GUT-PC": {
        "cik": 1080720,
        "title": "GABELLI UTILITY TRUST"
    },
    "UIHC": {
        "cik": 1401521,
        "title": "AMERICAN COASTAL INSURANCE Corp"
    },
    "MITT-PB": {
        "cik": 1514281,
        "title": "AG Mortgage Investment Trust, Inc."
    },
    "NVNXF": {
        "cik": 1859795,
        "title": "NOVONIX Ltd"
    },
    "TNP-PE": {
        "cik": 1166663,
        "title": "TSAKOS ENERGY NAVIGATION LTD"
    },
    "CIO-PA": {
        "cik": 1593222,
        "title": "City Office REIT, Inc."
    },
    "BHR-PD": {
        "cik": 1574085,
        "title": "Braemar Hotels & Resorts Inc."
    },
    "APLMW": {
        "cik": 1944885,
        "title": "Apollomics Inc."
    },
    "CHMI-PB": {
        "cik": 1571776,
        "title": "Cherry Hill Mortgage Investment Corp"
    },
    "BHR-PB": {
        "cik": 1574085,
        "title": "Braemar Hotels & Resorts Inc."
    },
    "FGPRB": {
        "cik": 922358,
        "title": "FERRELLGAS PARTNERS L P"
    },
    "UONEK": {
        "cik": 1041657,
        "title": "URBAN ONE, INC."
    },
    "AHT-PG": {
        "cik": 1232582,
        "title": "ASHFORD HOSPITALITY TRUST INC"
    },
    "BSAQ": {
        "cik": 1851908,
        "title": "Black Spade Acquisition Co"
    },
    "AHT-PH": {
        "cik": 1232582,
        "title": "ASHFORD HOSPITALITY TRUST INC"
    },
    "AHT-PF": {
        "cik": 1232582,
        "title": "ASHFORD HOSPITALITY TRUST INC"
    },
    "AHT-PI": {
        "cik": 1232582,
        "title": "ASHFORD HOSPITALITY TRUST INC"
    },
    "AHT-PD": {
        "cik": 1232582,
        "title": "ASHFORD HOSPITALITY TRUST INC"
    },
    "APMI": {
        "cik": 1857662,
        "title": "AxonPrime Infrastructure Acquisition Corp"
    },
    "SB-PD": {
        "cik": 1434754,
        "title": "SAFE BULKERS, INC."
    },
    "SAL": {
        "cik": 1060219,
        "title": "SALISBURY BANCORP, INC."
    },
    "CDR-PB": {
        "cik": 761648,
        "title": "CEDAR REALTY TRUST, INC."
    },
    "DLNG-PA": {
        "cik": 1578453,
        "title": "Dynagas LNG Partners LP"
    },
    "NSRCF": {
        "cik": 1302084,
        "title": "NextSource Materials Inc."
    },
    "SGTM": {
        "cik": 1895251,
        "title": "Sustainable Green Team, Ltd."
    },
    "CDR-PC": {
        "cik": 761648,
        "title": "CEDAR REALTY TRUST, INC."
    },
    "ACAH": {
        "cik": 1836274,
        "title": "Atlantic Coastal Acquisition Corp."
    },
    "ECF-PA": {
        "cik": 793040,
        "title": "ELLSWORTH GROWTH & INCOME FUND LTD"
    },
    "SOHON": {
        "cik": 1301236,
        "title": "Sotherly Hotels Inc."
    },
    "BCV-PA": {
        "cik": 9521,
        "title": "BANCROFT FUND LTD"
    },
    "SOHOB": {
        "cik": 1301236,
        "title": "Sotherly Hotels Inc."
    },
    "ZFOXW": {
        "cik": 1823575,
        "title": "ZeroFox Holdings, Inc."
    },
    "TLGA": {
        "cik": 1827871,
        "title": "Electriq Power Holdings, Inc."
    },
    "WONDF": {
        "cik": 1882839,
        "title": "WonderFi Technologies Inc."
    },
    "OFED": {
        "cik": 1501078,
        "title": "Oconee Federal Financial Corp."
    },
    "FBIOP": {
        "cik": 1429260,
        "title": "Fortress Biotech, Inc."
    },
    "FFBW": {
        "cik": 1787384,
        "title": "FFBW, Inc. /MD/"
    },
    "ARBKF": {
        "cik": 1841675,
        "title": "Argo Blockchain Plc"
    },
    "YELL": {
        "cik": 716006,
        "title": "Yellow Corp"
    },
    "HMAC": {
        "cik": 1894370,
        "title": "Hainan Manaslu Acquisition Corp."
    },
    "DEFTF": {
        "cik": 1888274,
        "title": "Defi Technologies, Inc."
    },
    "CNNB": {
        "cik": 1787005,
        "title": "Cincinnati Bancorp, Inc."
    },
    "CYCCP": {
        "cik": 1130166,
        "title": "Cyclacel Pharmaceuticals, Inc."
    },
    "DPRO": {
        "cik": 1786286,
        "title": "Draganfly Inc."
    },
    "WVVIP": {
        "cik": 838875,
        "title": "WILLAMETTE VALLEY VINEYARDS INC"
    },
    "AATC": {
        "cik": 943034,
        "title": "AUTOSCOPE TECHNOLOGIES CORP"
    },
    "NEXCF": {
        "cik": 1737270,
        "title": "NexTech AR Solutions Corp."
    },
    "SIOX": {
        "cik": 1636050,
        "title": "Sio Gene Therapies Inc."
    },
    "OCGSF": {
        "cik": 942149,
        "title": "Outcrop Silver & Gold Corp"
    },
    "ACRDF": {
        "cik": 1762359,
        "title": "Acreage Holdings, Inc."
    },
    "AFGC": {
        "cik": 1042046,
        "title": "AMERICAN FINANCIAL GROUP INC"
    },
    "WSTL": {
        "cik": 1002135,
        "title": "WESTELL TECHNOLOGIES INC"
    },
    "AMRS": {
        "cik": 1365916,
        "title": "AMYRIS, INC."
    },
    "ALPSQ": {
        "cik": 1882607,
        "title": "ALPINE SUMMIT ENERGY PARTNERS, INC."
    },
    "ODDAF": {
        "cik": 1949766,
        "title": "Odd Burger Corp"
    },
    "GTVI": {
        "cik": 1263364,
        "title": "Idaho Copper Corp"
    },
    "PTRA": {
        "cik": 1820630,
        "title": "Proterra Inc"
    },
    "MINDP": {
        "cik": 926423,
        "title": "MIND TECHNOLOGY, INC"
    },
    "TMDIF": {
        "cik": 840551,
        "title": "TITAN MEDICAL INC"
    },
    "BNSOF": {
        "cik": 846546,
        "title": "BONSO ELECTRONICS INTERNATIONAL INC"
    },
    "SEAC": {
        "cik": 1019671,
        "title": "SEACHANGE INTERNATIONAL INC"
    },
    "TVE": {
        "cik": 1376986,
        "title": "Tennessee Valley Authority"
    },
    "WHLRD": {
        "cik": 1527541,
        "title": "Wheeler Real Estate Investment Trust, Inc."
    },
    "PMEDF": {
        "cik": 1868079,
        "title": "Predictmedix Inc."
    },
    "SWISF": {
        "cik": 1771755,
        "title": "Sekur Private Data Ltd."
    },
    "DFFN": {
        "cik": 1053691,
        "title": "CervoMed Inc."
    },
    "SGLDF": {
        "cik": 1318482,
        "title": "KIDOZ INC."
    },
    "FALC": {
        "cik": 922521,
        "title": "FALCONSTOR SOFTWARE INC"
    },
    "SICP": {
        "cik": 1312109,
        "title": "Silvergate Capital Corp"
    },
    "GRDAF": {
        "cik": 1804469,
        "title": "Guardforce AI Co., Ltd."
    },
    "ADMQ": {
        "cik": 1588014,
        "title": "ADM ENDEAVORS, INC."
    },
    "GSPT": {
        "cik": 1076262,
        "title": "Golden Star Enterprises Ltd."
    },
    "SIRC": {
        "cik": 1756704,
        "title": "SOLAR INTEGRATED ROOFING CORP."
    },
    "GRVE": {
        "cik": 918573,
        "title": "GROOVE BOTANICALS INC."
    },
    "BNKL": {
        "cik": 1508381,
        "title": "Bionik Laboratories Corp."
    },
    "TKOI": {
        "cik": 1094084,
        "title": "TELKONET INC"
    },
    "RMED": {
        "cik": 1716621,
        "title": "Ra Medical Systems, Inc."
    },
    "RGRX": {
        "cik": 707511,
        "title": "REGENERX BIOPHARMACEUTICALS INC"
    },
    "ACGN": {
        "cik": 861838,
        "title": "Aceragen, Inc."
    },
    "BRLL": {
        "cik": 1631463,
        "title": "Barrel Energy Inc."
    },
    "ASPU": {
        "cik": 1487198,
        "title": "ASPEN GROUP, INC."
    },
    "BTZI": {
        "cik": 1525852,
        "title": "BOTS, Inc./PR"
    },
    "CETXP": {
        "cik": 1435064,
        "title": "CEMTREX INC"
    },
    "IMPM": {
        "cik": 1000298,
        "title": "IMPAC MORTGAGE HOLDINGS INC"
    },
    "WSRC": {
        "cik": 42050,
        "title": "WESTERN SIERRA RESOURCE Corp"
    },
    "ENDPQ": {
        "cik": 1593034,
        "title": "Endo International plc"
    },
    "MLLOF": {
        "cik": 1370496,
        "title": "Medallion Resources Ltd"
    },
    "EXNRF": {
        "cik": 1263011,
        "title": "EXCELLON RESOURCES INC"
    },
    "MKGP": {
        "cik": 1825270,
        "title": "Maverick Energy Group, Ltd."
    },
    "BDRL": {
        "cik": 1000683,
        "title": "BLONDER TONGUE LABORATORIES INC"
    },
    "AGNPF": {
        "cik": 1642178,
        "title": "Algernon Pharmaceuticals Inc."
    },
    "PCTL": {
        "cik": 1119897,
        "title": "PCT LTD"
    },
    "APSI": {
        "cik": 1553264,
        "title": "AQUA POWER SYSTEMS INC."
    },
    "VYNT": {
        "cik": 1349929,
        "title": "Vyant Bio, Inc."
    },
    "ONCR": {
        "cik": 1671818,
        "title": "Oncorus, Inc."
    },
    "GVSI": {
        "cik": 1068618,
        "title": "Good Vibrations Shoes, Inc."
    },
    "BLEG": {
        "cik": 1794311,
        "title": "Branded Legacy, Inc."
    },
    "IMUC": {
        "cik": 822411,
        "title": "EOM Pharmaceutical Holdings, Inc."
    },
    "SNNC": {
        "cik": 1313938,
        "title": "Sibannac, Inc."
    },
    "DROP": {
        "cik": 842722,
        "title": "Fuse Science, Inc."
    },
    "CENBF": {
        "cik": 1653821,
        "title": "CEN BIOTECH INC"
    },
    "RHE-PA": {
        "cik": 1004724,
        "title": "REGIONAL HEALTH PROPERTIES, INC"
    },
    "CBTC": {
        "cik": 1429859,
        "title": "XTRA Bitcoin Inc."
    },
    "PTEIQ": {
        "cik": 1076682,
        "title": "POLARITYTE, INC."
    },
    "GLUC": {
        "cik": 1420108,
        "title": "Glucose Health, Inc."
    },
    "KNOS": {
        "cik": 1108248,
        "title": "KRONOS ADVANCED TECHNOLOGIES INC"
    },
    "SLHGF": {
        "cik": 1839730,
        "title": "Skylight Health Group Inc."
    },
    "PHCG": {
        "cik": 1351573,
        "title": "Pure Harvest Corporate Group, Inc."
    },
    "VERBW": {
        "cik": 1566610,
        "title": "Verb Technology Company, Inc."
    },
    "FDBL": {
        "cik": 1414043,
        "title": "Friendable, Inc."
    },
    "RPT-PD": {
        "cik": 842183,
        "title": "RPT Realty"
    },
    "BAC-PL": {
        "cik": 70858,
        "title": "BANK OF AMERICA CORP /DE/"
    },
    "BAC-PM": {
        "cik": 70858,
        "title": "BANK OF AMERICA CORP /DE/"
    },
    "BAC-PN": {
        "cik": 70858,
        "title": "BANK OF AMERICA CORP /DE/"
    },
    "BAC-PP": {
        "cik": 70858,
        "title": "BANK OF AMERICA CORP /DE/"
    },
    "BAC-PO": {
        "cik": 70858,
        "title": "BANK OF AMERICA CORP /DE/"
    },
    "TBLAW": {
        "cik": 1840502,
        "title": "Taboola.com Ltd."
    },
    "MCOMW": {
        "cik": 1788841,
        "title": "micromobility.com Inc."
    },
    "AIMDW": {
        "cik": 1014763,
        "title": "Ainos, Inc."
    },
    "DCOMP": {
        "cik": 846617,
        "title": "Dime Community Bancshares, Inc. /NY/"
    },
    "ZIONO": {
        "cik": 109380,
        "title": "ZIONS BANCORPORATION, NATIONAL ASSOCIATION /UT/"
    },
    "ZIONL": {
        "cik": 109380,
        "title": "ZIONS BANCORPORATION, NATIONAL ASSOCIATION /UT/"
    },
    "ZIONP": {
        "cik": 109380,
        "title": "ZIONS BANCORPORATION, NATIONAL ASSOCIATION /UT/"
    },
    "UZE": {
        "cik": 821130,
        "title": "UNITED STATES CELLULAR CORP"
    },
    "UZF": {
        "cik": 821130,
        "title": "UNITED STATES CELLULAR CORP"
    },
    "PARAP": {
        "cik": 813828,
        "title": "Paramount Global"
    },
    "OPINL": {
        "cik": 1456772,
        "title": "OFFICE PROPERTIES INCOME TRUST"
    },
    "BIP-PB": {
        "cik": 1406234,
        "title": "Brookfield Infrastructure Partners L.P."
    },
    "PFXNZ": {
        "cik": 1490349,
        "title": "PhenixFIN Corp"
    },
    "OCFCP": {
        "cik": 1004702,
        "title": "OCEANFIRST FINANCIAL CORP"
    },
    "UKOMW": {
        "cik": 1821424,
        "title": "Ucommune International Ltd"
    },
    "WLDSW": {
        "cik": 1887673,
        "title": "Wearable Devices Ltd."
    },
    "LLAP-WT": {
        "cik": 1835512,
        "title": "Terran Orbital Corp"
    },
    "SF-PC": {
        "cik": 720672,
        "title": "STIFEL FINANCIAL CORP"
    },
    "AESC": {
        "cik": 874761,
        "title": "AES CORP"
    },
    "VXZ": {
        "cik": 312070,
        "title": "BARCLAYS BANK PLC"
    },
    "VXX": {
        "cik": 312070,
        "title": "BARCLAYS BANK PLC"
    },
    "DJP": {
        "cik": 312070,
        "title": "BARCLAYS BANK PLC"
    },
    "GRN": {
        "cik": 312070,
        "title": "BARCLAYS BANK PLC"
    },
    "SF-PD": {
        "cik": 720672,
        "title": "STIFEL FINANCIAL CORP"
    },
    "FRMEP": {
        "cik": 712534,
        "title": "FIRST MERCHANTS CORP"
    },
    "SFB": {
        "cik": 720672,
        "title": "STIFEL FINANCIAL CORP"
    },
    "TELZ": {
        "cik": 61398,
        "title": "TELLURIAN INC. /DE/"
    },
    "ADNWW": {
        "cik": 1744494,
        "title": "ADVENT TECHNOLOGIES HOLDINGS, INC."
    },
    "VIASP": {
        "cik": 1606268,
        "title": "Via Renewables, Inc."
    },
    "ACONW": {
        "cik": 1635077,
        "title": "Aclarion, Inc."
    },
    "AJXA": {
        "cik": 1614806,
        "title": "Great Ajax Corp."
    },
    "LUNRW": {
        "cik": 1844452,
        "title": "Intuitive Machines, Inc."
    },
    "CDROW": {
        "cik": 1866782,
        "title": "Codere Online Luxembourg, S.A."
    },
    "DNA-WT": {
        "cik": 1830214,
        "title": "Ginkgo Bioworks Holdings, Inc."
    },
    "BYNOW": {
        "cik": 1801417,
        "title": "byNordic Acquisition Corp"
    },
    "MYPSW": {
        "cik": 1823878,
        "title": "PLAYSTUDIOS, Inc."
    },
    "GL-PD": {
        "cik": 320335,
        "title": "GLOBE LIFE INC."
    },
    "FNMAP": {
        "cik": 310522,
        "title": "FEDERAL NATIONAL MORTGAGE ASSOCIATION FANNIE MAE"
    },
    "SCHW-PJ": {
        "cik": 316709,
        "title": "SCHWAB CHARLES CORP"
    },
    "XPDBW": {
        "cik": 1855474,
        "title": "Power & Digital Infrastructure Acquisition II Corp."
    },
    "AEPPZ": {
        "cik": 4904,
        "title": "AMERICAN ELECTRIC POWER CO INC"
    },
    "SVIIU": {
        "cik": 1843477,
        "title": "Spring Valley Acquisition Corp. II"
    },
    "IMPPP": {
        "cik": 1876581,
        "title": "Imperial Petroleum Inc./Marshall Islands"
    },
    "PETWW": {
        "cik": 1842356,
        "title": "Wag! Group Co."
    },
    "OPAD-WT": {
        "cik": 1825024,
        "title": "Offerpad Solutions Inc."
    },
    "SMXWW": {
        "cik": 1940674,
        "title": "SMX (Security Matters) Public Ltd Co"
    },
    "HUBCW": {
        "cik": 1905660,
        "title": "Hub Cyber Security Ltd."
    },
    "RBOT-WT": {
        "cik": 1812173,
        "title": "Vicarious Surgical Inc."
    },
    "RDW-WT": {
        "cik": 1819810,
        "title": "Redwire Corp"
    },
    "AGBAW": {
        "cik": 1769624,
        "title": "AGBA Group Holding Ltd."
    },
    "XELAP": {
        "cik": 1620179,
        "title": "Exela Technologies, Inc."
    },
    "GMVDW": {
        "cik": 1760764,
        "title": "G Medical Innovations Holdings Ltd."
    },
    "NVVEW": {
        "cik": 1836875,
        "title": "Nuvve Holding Corp."
    },
    "MBINM": {
        "cik": 1629019,
        "title": "Merchants Bancorp"
    },
    "MBINN": {
        "cik": 1629019,
        "title": "Merchants Bancorp"
    },
    "MBINO": {
        "cik": 1629019,
        "title": "Merchants Bancorp"
    },
    "SHCRW": {
        "cik": 1816233,
        "title": "Sharecare, Inc."
    },
    "ROIVW": {
        "cik": 1635088,
        "title": "Roivant Sciences Ltd."
    },
    "IINNW": {
        "cik": 1837493,
        "title": "Inspira Technologies OXY B.H.N. Ltd"
    },
    "LVWR-WT": {
        "cik": 1898795,
        "title": "LiveWire Group, Inc."
    },
    "DFLIW": {
        "cik": 1847986,
        "title": "Dragonfly Energy Holdings Corp."
    },
    "WALDW": {
        "cik": 1840199,
        "title": "Waldencast plc"
    },
    "MET-PF": {
        "cik": 1099219,
        "title": "METLIFE INC"
    },
    "PSEC-PA": {
        "cik": 1287032,
        "title": "PROSPECT CAPITAL CORP"
    },
    "FGBIP": {
        "cik": 1408534,
        "title": "First Guaranty Bancshares, Inc."
    },
    "DLR-PL": {
        "cik": 1297996,
        "title": "DIGITAL REALTY TRUST, INC."
    },
    "ET-PE": {
        "cik": 1276187,
        "title": "Energy Transfer LP"
    },
    "GDV-PK": {
        "cik": 1260729,
        "title": "GABELLI DIVIDEND & INCOME TRUST"
    },
    "WAL-PA": {
        "cik": 1212545,
        "title": "WESTERN ALLIANCE BANCORPORATION"
    },
    "ET-PD": {
        "cik": 1276187,
        "title": "Energy Transfer LP"
    },
    "ET-PC": {
        "cik": 1276187,
        "title": "Energy Transfer LP"
    },
    "OXLCZ": {
        "cik": 1495222,
        "title": "Oxford Lane Capital Corp."
    },
    "OXLCP": {
        "cik": 1495222,
        "title": "Oxford Lane Capital Corp."
    },
    "OXLCN": {
        "cik": 1495222,
        "title": "Oxford Lane Capital Corp."
    },
    "GAINN": {
        "cik": 1321741,
        "title": "GLADSTONE INVESTMENT CORPORATIONDE"
    },
    "NEWTZ": {
        "cik": 1587987,
        "title": "NewtekOne, Inc."
    },
    "NEWTL": {
        "cik": 1587987,
        "title": "NewtekOne, Inc."
    },
    "SAJ": {
        "cik": 1377936,
        "title": "SARATOGA INVESTMENT CORP."
    },
    "SAY": {
        "cik": 1377936,
        "title": "SARATOGA INVESTMENT CORP."
    },
    "SAT": {
        "cik": 1377936,
        "title": "SARATOGA INVESTMENT CORP."
    },
    "ACAHW": {
        "cik": 1836274,
        "title": "Atlantic Coastal Acquisition Corp."
    },
    "BHIL-WT": {
        "cik": 1830210,
        "title": "Benson Hill, Inc."
    },
    "SCCD": {
        "cik": 1682220,
        "title": "Sachem Capital Corp."
    },
    "SCCF": {
        "cik": 1682220,
        "title": "Sachem Capital Corp."
    },
    "SCCB": {
        "cik": 1682220,
        "title": "Sachem Capital Corp."
    },
    "SCCC": {
        "cik": 1682220,
        "title": "Sachem Capital Corp."
    },
    "SCCG": {
        "cik": 1682220,
        "title": "Sachem Capital Corp."
    },
    "ENERR": {
        "cik": 1855555,
        "title": "ACCRETION ACQUISITION CORP."
    },
    "CXAIW": {
        "cik": 1820875,
        "title": "CXApp Inc."
    },
    "BREZW": {
        "cik": 1817640,
        "title": "Breeze Holdings Acquisition Corp."
    },
    "HCMAW": {
        "cik": 1845368,
        "title": "HCM Acquisition Corp"
    },
    "PACI-WT": {
        "cik": 1853070,
        "title": "PROOF Acquisition Corp I"
    },
    "EGGF-WT": {
        "cik": 1843973,
        "title": "EG Acquisition Corp."
    },
    "CRGOW": {
        "cik": 1927719,
        "title": "Freightos Ltd"
    },
    "AFGB": {
        "cik": 1042046,
        "title": "AMERICAN FINANCIAL GROUP INC"
    },
    "AFGE": {
        "cik": 1042046,
        "title": "AMERICAN FINANCIAL GROUP INC"
    },
    "AFGD": {
        "cik": 1042046,
        "title": "AMERICAN FINANCIAL GROUP INC"
    },
    "RNR-PG": {
        "cik": 913144,
        "title": "RENAISSANCERE HOLDINGS LTD"
    },
    "WBS-PG": {
        "cik": 801337,
        "title": "WEBSTER FINANCIAL CORP"
    },
    "LFMDP": {
        "cik": 948320,
        "title": "LifeMD, Inc."
    },
    "DDT": {
        "cik": 28917,
        "title": "DILLARD'S, INC."
    },
    "WFC-PA": {
        "cik": 72971,
        "title": "WELLS FARGO & COMPANY/MN"
    },
    "WFC-PD": {
        "cik": 72971,
        "title": "WELLS FARGO & COMPANY/MN"
    },
    "BPOPM": {
        "cik": 763901,
        "title": "POPULAR, INC."
    },
    "EFC-PA": {
        "cik": 1411342,
        "title": "Ellington Financial Inc."
    },
    "EFC-PB": {
        "cik": 1411342,
        "title": "Ellington Financial Inc."
    },
    "EFC-PC": {
        "cik": 1411342,
        "title": "Ellington Financial Inc."
    },
    "SEAL-PA": {
        "cik": 1308106,
        "title": "Seapeak LLC"
    },
    "GDL-PC": {
        "cik": 1378701,
        "title": "GDL FUND"
    },
    "BNGOW": {
        "cik": 1411690,
        "title": "Bionano Genomics, Inc."
    },
    "KREF-PA": {
        "cik": 1631596,
        "title": "KKR Real Estate Finance Trust Inc."
    },
    "BEEMW": {
        "cik": 1398805,
        "title": "Beam Global"
    },
    "AHL-PE": {
        "cik": 1267395,
        "title": "ASPEN INSURANCE HOLDINGS LTD"
    },
    "TVIXF": {
        "cik": 1053092,
        "title": "CREDIT SUISSE AG"
    },
    "UGLDF": {
        "cik": 1053092,
        "title": "CREDIT SUISSE AG"
    },
    "USOI": {
        "cik": 1053092,
        "title": "CREDIT SUISSE AG"
    },
    "USLVF": {
        "cik": 1053092,
        "title": "CREDIT SUISSE AG"
    },
    "GLDI": {
        "cik": 1053092,
        "title": "CREDIT SUISSE AG"
    },
    "CHKEL": {
        "cik": 895126,
        "title": "CHESAPEAKE ENERGY CORP"
    },
    "XOMAO": {
        "cik": 791908,
        "title": "XOMA Corp"
    },
    "XOMAP": {
        "cik": 791908,
        "title": "XOMA Corp"
    },
    "AEAEW": {
        "cik": 1852016,
        "title": "AltEnergy Acquisition Corp"
    },
    "ECXWW": {
        "cik": 1861974,
        "title": "ECARX Holdings Inc."
    },
    "TALKW": {
        "cik": 1803901,
        "title": "Talkspace, Inc."
    },
    "PGYWW": {
        "cik": 1883085,
        "title": "Pagaya Technologies Ltd."
    },
    "ASTLW": {
        "cik": 1860805,
        "title": "Algoma Steel Group Inc."
    },
    "VIEWW": {
        "cik": 1811856,
        "title": "View, Inc."
    },
    "ALTUW": {
        "cik": 1822366,
        "title": "Altitude Acquisition Corp."
    },
    "CELUW": {
        "cik": 1752828,
        "title": "Celularity Inc"
    },
    "LVOXW": {
        "cik": 1723648,
        "title": "LiveVox Holdings, Inc."
    },
    "LFT-PA": {
        "cik": 1547546,
        "title": "Lument Finance Trust, Inc."
    },
    "WTFCP": {
        "cik": 1015328,
        "title": "WINTRUST FINANCIAL CORP"
    },
    "ADC-PA": {
        "cik": 917251,
        "title": "AGREE REALTY CORP"
    },
    "MS-PP": {
        "cik": 895421,
        "title": "MORGAN STANLEY"
    },
    "MS-PO": {
        "cik": 895421,
        "title": "MORGAN STANLEY"
    },
    "MS-PL": {
        "cik": 895421,
        "title": "MORGAN STANLEY"
    },
    "VAL-WT": {
        "cik": 314808,
        "title": "Valaris Ltd"
    },
    "CHSCN": {
        "cik": 823277,
        "title": "CHS INC"
    },
    "CHSCO": {
        "cik": 823277,
        "title": "CHS INC"
    },
    "CHSCM": {
        "cik": 823277,
        "title": "CHS INC"
    },
    "AP-WT": {
        "cik": 6176,
        "title": "AMPCO PITTSBURGH CORP"
    },
    "GGROW": {
        "cik": 1886190,
        "title": "Gogoro Inc."
    },
    "RGTIW": {
        "cik": 1838359,
        "title": "Rigetti Computing, Inc."
    },
    "PAYOW": {
        "cik": 1845815,
        "title": "Payoneer Global Inc."
    },
    "SLNHP": {
        "cik": 64463,
        "title": "Soluna Holdings, Inc"
    },
    "LNC-PD": {
        "cik": 59558,
        "title": "LINCOLN NATIONAL CORP"
    },
    "HBANM": {
        "cik": 49196,
        "title": "HUNTINGTON BANCSHARES INC /MD/"
    },
    "HBANP": {
        "cik": 49196,
        "title": "HUNTINGTON BANCSHARES INC /MD/"
    },
    "BFS-PE": {
        "cik": 907254,
        "title": "SAUL CENTERS, INC."
    },
    "SIGIP": {
        "cik": 230557,
        "title": "SELECTIVE INSURANCE GROUP INC"
    },
    "TBC": {
        "cik": 732717,
        "title": "AT&T INC."
    },
    "T-PC": {
        "cik": 732717,
        "title": "AT&T INC."
    },
    "T-PA": {
        "cik": 732717,
        "title": "AT&T INC."
    },
    "MFA-PC": {
        "cik": 1055160,
        "title": "MFA FINANCIAL, INC."
    },
    "EFTRW": {
        "cik": 1828522,
        "title": "eFFECTOR Therapeutics, Inc."
    },
    "MCAFR": {
        "cik": 1853774,
        "title": "Mountain Crest Acquisition Corp. IV"
    },
    "CMAXW": {
        "cik": 1813914,
        "title": "CareMax, Inc."
    },
    "BFRGW": {
        "cik": 1829247,
        "title": "BullFrog AI Holdings, Inc."
    },
    "GEGGL": {
        "cik": 1831096,
        "title": "Great Elm Group, Inc."
    },
    "CETUW": {
        "cik": 1936702,
        "title": "Cetus Capital Acquisition Corp."
    },
    "ATCO-PH": {
        "cik": 1794846,
        "title": "Atlas Corp."
    },
    "ATCOL": {
        "cik": 1794846,
        "title": "Atlas Corp."
    },
    "ATCO-PI": {
        "cik": 1794846,
        "title": "Atlas Corp."
    },
    "HPKEW": {
        "cik": 1792849,
        "title": "HighPeak Energy, Inc."
    },
    "NRXPW": {
        "cik": 1719406,
        "title": "NRX Pharmaceuticals, Inc."
    },
    "WBX-WT": {
        "cik": 1866501,
        "title": "Wallbox N.V."
    },
    "SLGCW": {
        "cik": 1837412,
        "title": "SomaLogic, Inc."
    },
    "PRSTW": {
        "cik": 1822145,
        "title": "Presto Automation Inc."
    },
    "RVPHW": {
        "cik": 1742927,
        "title": "REVIVA PHARMACEUTICALS HOLDINGS, INC."
    },
    "GLFC": {
        "cik": 1876945,
        "title": "Gold Flora Corp."
    },
    "MTB-PH": {
        "cik": 36270,
        "title": "M&T BANK CORP"
    },
    "LMND-WT": {
        "cik": 1691421,
        "title": "Lemonade, Inc."
    },
    "GSMGW": {
        "cik": 1738758,
        "title": "GLORY STAR NEW MEDIA GROUP HOLDINGS Ltd"
    },
    "MSBIP": {
        "cik": 1466026,
        "title": "Midland States Bancorp, Inc."
    },
    "FCNCP": {
        "cik": 798941,
        "title": "FIRST CITIZENS BANCSHARES INC /DE/"
    },
    "AEL-PB": {
        "cik": 1039828,
        "title": "AMERICAN EQUITY INVESTMENT LIFE HOLDING CO"
    },
    "UBP-PK": {
        "cik": 1029800,
        "title": "URSTADT BIDDLE PROPERTIES INC"
    },
    "ALL-PI": {
        "cik": 899051,
        "title": "ALLSTATE CORP"
    },
    "AUB-PA": {
        "cik": 883948,
        "title": "Atlantic Union Bankshares Corp"
    },
    "PSBZP": {
        "cik": 866368,
        "title": "PS BUSINESS PARKS, INC./MD"
    },
    "PSBXP": {
        "cik": 866368,
        "title": "PS BUSINESS PARKS, INC./MD"
    },
    "PSBYP": {
        "cik": 866368,
        "title": "PS BUSINESS PARKS, INC./MD"
    },
    "AEL-PA": {
        "cik": 1039828,
        "title": "AMERICAN EQUITY INVESTMENT LIFE HOLDING CO"
    },
    "MBNKP": {
        "cik": 1000209,
        "title": "MEDALLION FINANCIAL CORP"
    },
    "CRESW": {
        "cik": 1034957,
        "title": "CRESUD INC"
    },
    "TCBIO": {
        "cik": 1077428,
        "title": "TEXAS CAPITAL BANCSHARES INC/TX"
    },
    "SHO-PH": {
        "cik": 1295810,
        "title": "Sunstone Hotel Investors, Inc."
    },
    "MNSBP": {
        "cik": 1693577,
        "title": "MainStreet Bancshares, Inc."
    },
    "CCLDO": {
        "cik": 1582982,
        "title": "CareCloud, Inc."
    },
    "CCLDP": {
        "cik": 1582982,
        "title": "CareCloud, Inc."
    },
    "CIFRW": {
        "cik": 1819989,
        "title": "Cipher Mining Inc."
    },
    "ECC-PD": {
        "cik": 1604174,
        "title": "Eagle Point Credit Co Inc."
    },
    "ECCW": {
        "cik": 1604174,
        "title": "Eagle Point Credit Co Inc."
    },
    "CNOBP": {
        "cik": 712771,
        "title": "ConnectOne Bancorp, Inc."
    },
    "WRB-PH": {
        "cik": 11544,
        "title": "BERKLEY W R CORP"
    },
    "WRB-PF": {
        "cik": 11544,
        "title": "BERKLEY W R CORP"
    },
    "ROSEW": {
        "cik": 1870129,
        "title": "Rose Hill Acquisition Corp"
    },
    "FATH-WT": {
        "cik": 1836176,
        "title": "Fathom Digital Manufacturing Corp"
    },
    "LEV-WT": {
        "cik": 1834974,
        "title": "Lion Electric Co"
    },
    "SCRMW": {
        "cik": 1893325,
        "title": "Screaming Eagle Acquisition Corp."
    },
    "HUDAR": {
        "cik": 1853047,
        "title": "Hudson Acquisition I Corp."
    },
    "AAC-WT": {
        "cik": 1829432,
        "title": "Ares Acquisition Corp"
    },
    "AAC-UN": {
        "cik": 1829432,
        "title": "Ares Acquisition Corp"
    },
    "AEVA-WT": {
        "cik": 1789029,
        "title": "Aeva Technologies, Inc."
    },
    "OPFI-WT": {
        "cik": 1818502,
        "title": "OppFi Inc."
    },
    "ADVWW": {
        "cik": 1776661,
        "title": "Advantage Solutions Inc."
    },
    "SLND-WT": {
        "cik": 1883814,
        "title": "Southland Holdings, Inc."
    },
    "BLDEW": {
        "cik": 1779128,
        "title": "Blade Air Mobility, Inc."
    },
    "ASBA": {
        "cik": 7789,
        "title": "ASSOCIATED BANC-CORP"
    },
    "MIR-WT": {
        "cik": 1809987,
        "title": "Mirion Technologies, Inc."
    },
    "F-PC": {
        "cik": 37996,
        "title": "FORD MOTOR CO"
    },
    "F-PD": {
        "cik": 37996,
        "title": "FORD MOTOR CO"
    },
    "F-PB": {
        "cik": 37996,
        "title": "FORD MOTOR CO"
    },
    "HWCPZ": {
        "cik": 750577,
        "title": "HANCOCK WHITNEY CORP"
    },
    "AEFC": {
        "cik": 769218,
        "title": "AEGON NV"
    },
    "DUKB": {
        "cik": 1326160,
        "title": "Duke Energy CORP"
    },
    "AQNB": {
        "cik": 1174169,
        "title": "ALGONQUIN POWER & UTILITIES CORP."
    },
    "AQNA": {
        "cik": 1174169,
        "title": "ALGONQUIN POWER & UTILITIES CORP."
    },
    "AWINW": {
        "cik": 1855631,
        "title": "AERWINS Technologies Inc."
    },
    "HCDIP": {
        "cik": 1784567,
        "title": "Harbor Custom Development, Inc."
    },
    "ALTG-PA": {
        "cik": 1759824,
        "title": "ALTA EQUIPMENT GROUP INC."
    },
    "PEGRW": {
        "cik": 1847241,
        "title": "Project Energy Reimagined Acquisition Corp."
    },
    "ARIZW": {
        "cik": 1882078,
        "title": "Arisz Acquisition Corp."
    },
    "AACIW": {
        "cik": 1844817,
        "title": "Armada Acquisition Corp. I"
    },
    "BLEUR": {
        "cik": 1843370,
        "title": "bleuacacia ltd"
    },
    "NVACR": {
        "cik": 1859807,
        "title": "NorthView Acquisition Corp"
    },
    "ACUT": {
        "cik": 1850767,
        "title": "Accustem Sciences Inc."
    },
    "CCV-WT": {
        "cik": 1812234,
        "title": "Churchill Capital Corp V"
    },
    "VLN-WT": {
        "cik": 1863006,
        "title": "Valens Semiconductor Ltd."
    },
    "FREY-WT": {
        "cik": 1844224,
        "title": "FREYR Battery"
    },
    "GPACW": {
        "cik": 1831979,
        "title": "Global Partner Acquisition Corp II"
    },
    "INDIW": {
        "cik": 1841925,
        "title": "indie Semiconductor, Inc."
    },
    "UNOV": {
        "cik": 1538495,
        "title": "Earth Science Tech, Inc."
    },
    "VGASW": {
        "cik": 1841425,
        "title": "Verde Clean Fuels, Inc."
    },
    "AUVIP": {
        "cik": 1811109,
        "title": "Applied UV, Inc."
    },
    "REXR-PC": {
        "cik": 1571283,
        "title": "Rexford Industrial Realty, Inc."
    },
    "LTRYW": {
        "cik": 1673481,
        "title": "Lottery.com Inc."
    },
    "NYMTM": {
        "cik": 1273685,
        "title": "NEW YORK MORTGAGE TRUST INC"
    },
    "NYMTL": {
        "cik": 1273685,
        "title": "NEW YORK MORTGAGE TRUST INC"
    },
    "NYMTZ": {
        "cik": 1273685,
        "title": "NEW YORK MORTGAGE TRUST INC"
    },
    "PSA-PJ": {
        "cik": 1393311,
        "title": "Public Storage"
    },
    "PSA-PO": {
        "cik": 1393311,
        "title": "Public Storage"
    },
    "PSA-PG": {
        "cik": 1393311,
        "title": "Public Storage"
    },
    "PSA-PM": {
        "cik": 1393311,
        "title": "Public Storage"
    },
    "PSA-PP": {
        "cik": 1393311,
        "title": "Public Storage"
    },
    "PSA-PN": {
        "cik": 1393311,
        "title": "Public Storage"
    },
    "PSA-PQ": {
        "cik": 1393311,
        "title": "Public Storage"
    },
    "PSA-PF": {
        "cik": 1393311,
        "title": "Public Storage"
    },
    "PSA-PR": {
        "cik": 1393311,
        "title": "Public Storage"
    },
    "AGM-PE": {
        "cik": 845877,
        "title": "FEDERAL AGRICULTURAL MORTGAGE CORP"
    },
    "AGM-PF": {
        "cik": 845877,
        "title": "FEDERAL AGRICULTURAL MORTGAGE CORP"
    },
    "AGM-PG": {
        "cik": 845877,
        "title": "FEDERAL AGRICULTURAL MORTGAGE CORP"
    },
    "BULZ": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "WTIU": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "FNGU": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "OILD": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "BNKD": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "NRGU": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "GDXD": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "GDXU": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "NRGD": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "BNKU": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "FNGO": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "WTID": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "SHNY": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "FLYD": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "FNGS": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "FLYU": {
        "cik": 927971,
        "title": "BANK OF MONTREAL /CAN/"
    },
    "RCB": {
        "cik": 1527590,
        "title": "Ready Capital Corp"
    },
    "RCC": {
        "cik": 1527590,
        "title": "Ready Capital Corp"
    },
    "PSA-PL": {
        "cik": 1393311,
        "title": "Public Storage"
    },
    "PMT-PC": {
        "cik": 1464423,
        "title": "PennyMac Mortgage Investment Trust"
    },
    "TFINP": {
        "cik": 1539638,
        "title": "Triumph Financial, Inc."
    },
    "ABR-PE": {
        "cik": 1253986,
        "title": "ARBOR REALTY TRUST INC"
    },
    "ABR-PF": {
        "cik": 1253986,
        "title": "ARBOR REALTY TRUST INC"
    },
    "ABR-PD": {
        "cik": 1253986,
        "title": "ARBOR REALTY TRUST INC"
    },
    "TDS-PV": {
        "cik": 1051512,
        "title": "TELEPHONE & DATA SYSTEMS INC /DE/"
    },
    "MHNC": {
        "cik": 1412100,
        "title": "Maiden Holdings, Ltd."
    },
    "TRTN-PE": {
        "cik": 1660734,
        "title": "Triton International Ltd"
    },
    "TRTN-PB": {
        "cik": 1660734,
        "title": "Triton International Ltd"
    },
    "ATH-PB": {
        "cik": 1527469,
        "title": "Athene Holding Ltd"
    },
    "ATH-PD": {
        "cik": 1527469,
        "title": "Athene Holding Ltd"
    },
    "INBKZ": {
        "cik": 1562463,
        "title": "First Internet Bancorp"
    },
    "ATH-PE": {
        "cik": 1527469,
        "title": "Athene Holding Ltd"
    },
    "ATH-PC": {
        "cik": 1527469,
        "title": "Athene Holding Ltd"
    },
    "RBT-WT": {
        "cik": 1862068,
        "title": "Rubicon Technologies, Inc."
    },
    "NEOVW": {
        "cik": 1748137,
        "title": "NeoVolta Inc."
    },
    "NYCB-PU": {
        "cik": 910073,
        "title": "NEW YORK COMMUNITY BANCORP INC"
    },
    "SRCU": {
        "cik": 1126956,
        "title": "SPIRE INC"
    },
    "EPR-PC": {
        "cik": 1045450,
        "title": "EPR PROPERTIES"
    },
    "EPR-PE": {
        "cik": 1045450,
        "title": "EPR PROPERTIES"
    },
    "YSBPW": {
        "cik": 1946399,
        "title": "YS Biopharma Co., Ltd."
    },
    "GREEL": {
        "cik": 1844971,
        "title": "Greenidge Generation Holdings Inc."
    },
    "FREEW": {
        "cik": 1753706,
        "title": "Whole Earth Brands, Inc."
    },
    "ADTHW": {
        "cik": 1838672,
        "title": "AdTheorent Holding Company, Inc."
    },
    "TDW-WT": {
        "cik": 98222,
        "title": "TIDEWATER INC"
    },
    "FEXDR": {
        "cik": 1852407,
        "title": "Fintech Ecosystem Development Corp."
    },
    "MCAGR": {
        "cik": 1859035,
        "title": "Mountain Crest Acquisition Corp. V"
    },
    "COF-PN": {
        "cik": 927628,
        "title": "CAPITAL ONE FINANCIAL CORP"
    },
    "COF-PK": {
        "cik": 927628,
        "title": "CAPITAL ONE FINANCIAL CORP"
    },
    "COF-PJ": {
        "cik": 927628,
        "title": "CAPITAL ONE FINANCIAL CORP"
    },
    "WLLAW": {
        "cik": 1255474,
        "title": "Whiting Holdings LLC"
    },
    "USCI": {
        "cik": 1479247,
        "title": "United States Commodity Index Funds Trust"
    },
    "CPER": {
        "cik": 1479247,
        "title": "United States Commodity Index Funds Trust"
    },
    "HROWM": {
        "cik": 1360214,
        "title": "HARROW HEALTH, INC."
    },
    "RWAYL": {
        "cik": 1653384,
        "title": "Runway Growth Finance Corp."
    },
    "RWAYZ": {
        "cik": 1653384,
        "title": "Runway Growth Finance Corp."
    },
    "SBBA": {
        "cik": 1483934,
        "title": "Scorpio Tankers Inc."
    },
    "HTIBP": {
        "cik": 1561032,
        "title": "Healthcare Trust, Inc."
    },
    "LTCFX": {
        "cik": 1496254,
        "title": "Alternative Strategies Fund"
    },
    "OCCIO": {
        "cik": 1716951,
        "title": "OFS Credit Company, Inc."
    },
    "OCCIN": {
        "cik": 1716951,
        "title": "OFS Credit Company, Inc."
    },
    "PHUNW": {
        "cik": 1665300,
        "title": "Phunware, Inc."
    },
    "DRMAW": {
        "cik": 1853816,
        "title": "Dermata Therapeutics, Inc."
    },
    "SIVPQ": {
        "cik": 719739,
        "title": "SVB FINANCIAL GROUP"
    },
    "BANFP": {
        "cik": 760498,
        "title": "BANCFIRST CORP /OK/"
    },
    "CMSD": {
        "cik": 811156,
        "title": "CMS ENERGY CORP"
    },
    "CMS-PC": {
        "cik": 811156,
        "title": "CMS ENERGY CORP"
    },
    "ACHR-WT": {
        "cik": 1824502,
        "title": "Archer Aviation Inc."
    },
    "DBRG-PI": {
        "cik": 1679688,
        "title": "DigitalBridge Group, Inc."
    },
    "DBRG-PJ": {
        "cik": 1679688,
        "title": "DigitalBridge Group, Inc."
    },
    "FITBP": {
        "cik": 35527,
        "title": "FIFTH THIRD BANCORP"
    },
    "FITBO": {
        "cik": 35527,
        "title": "FIFTH THIRD BANCORP"
    },
    "RJF-PB": {
        "cik": 720005,
        "title": "RAYMOND JAMES FINANCIAL INC"
    },
    "GNL-PB": {
        "cik": 1526113,
        "title": "Global Net Lease, Inc."
    },
    "QRTEP": {
        "cik": 1355096,
        "title": "Qurate Retail, Inc."
    },
    "AIZN": {
        "cik": 1267238,
        "title": "ASSURANT, INC."
    },
    "AAIC-PB": {
        "cik": 1209028,
        "title": "Arlington Asset Investment Corp."
    },
    "AAIC-PC": {
        "cik": 1209028,
        "title": "Arlington Asset Investment Corp."
    },
    "AAIN": {
        "cik": 1209028,
        "title": "Arlington Asset Investment Corp."
    },
    "MITT-PC": {
        "cik": 1514281,
        "title": "AG Mortgage Investment Trust, Inc."
    },
    "ANZUW": {
        "cik": 1840877,
        "title": "Anzu Special Acquisition Corp I"
    },
    "SPNT-PB": {
        "cik": 1576018,
        "title": "SiriusPoint Ltd"
    },
    "WESTW": {
        "cik": 1806347,
        "title": "Westrock Coffee Co"
    },
    "NSTD-WT": {
        "cik": 1835814,
        "title": "Northern Star Investment Corp. IV"
    },
    "TBLTW": {
        "cik": 1668370,
        "title": "Toughbuilt Industries, Inc"
    },
    "AUROW": {
        "cik": 1828108,
        "title": "Aurora Innovation, Inc."
    },
    "ACABW": {
        "cik": 1893219,
        "title": "Atlantic Coastal Acquisition Corp. II"
    },
    "ADERW": {
        "cik": 1822912,
        "title": "26 Capital Acquisition Corp."
    },
    "RWT-PA": {
        "cik": 930236,
        "title": "REDWOOD TRUST INC"
    },
    "NLY-PI": {
        "cik": 1043219,
        "title": "ANNALY CAPITAL MANAGEMENT INC"
    },
    "ACGLN": {
        "cik": 947484,
        "title": "ARCH CAPITAL GROUP LTD."
    },
    "APCXW": {
        "cik": 1070050,
        "title": "AppTech Payments Corp."
    },
    "MOBQW": {
        "cik": 1084267,
        "title": "Mobiquity Technologies, Inc."
    },
    "CNO-PA": {
        "cik": 1224608,
        "title": "CNO Financial Group, Inc."
    },
    "ACP-PA": {
        "cik": 1503290,
        "title": "abrdn Income Credit Strategies Fund"
    },
    "HSCSW": {
        "cik": 1468492,
        "title": "Heart Test Laboratories, Inc."
    },
    "QVCC": {
        "cik": 1254699,
        "title": "QVC INC"
    },
    "MTEKW": {
        "cik": 1872964,
        "title": "Maris Tech Ltd."
    },
    "BRDS-WT": {
        "cik": 1861449,
        "title": "Bird Global, Inc."
    },
    "REVBW": {
        "cik": 1810560,
        "title": "REVELATION BIOSCIENCES, INC."
    },
    "SCLXW": {
        "cik": 1820190,
        "title": "Scilex Holding Co"
    },
    "LSEAW": {
        "cik": 1721386,
        "title": "Landsea Homes Corp"
    },
    "SLACW": {
        "cik": 1834755,
        "title": "Social Leverage Acquisition Corp I"
    },
    "SLACU": {
        "cik": 1834755,
        "title": "Social Leverage Acquisition Corp I"
    },
    "EACPW": {
        "cik": 1832765,
        "title": "Edify Acquisition Corp."
    },
    "GWH-WT": {
        "cik": 1819438,
        "title": "ESS Tech, Inc."
    },
    "BITE-WT": {
        "cik": 1831270,
        "title": "Bite Acquisition Corp."
    },
    "NBLWF": {
        "cik": 1895262,
        "title": "Noble Corp plc"
    },
    "XFLT-PA": {
        "cik": 1703079,
        "title": "XAI Octagon Floating Rate & Alternative Income Term Trust"
    },
    "DISAW": {
        "cik": 1838831,
        "title": "Disruptive Acquisition Corp I"
    },
    "LVROW": {
        "cik": 1945711,
        "title": "Lavoro Ltd"
    },
    "AMJ": {
        "cik": 19617,
        "title": "JPMORGAN CHASE & CO"
    },
    "JPM-PL": {
        "cik": 19617,
        "title": "JPMORGAN CHASE & CO"
    },
    "DRTSW": {
        "cik": 1871321,
        "title": "Alpha Tau Medical Ltd."
    },
    "ALLG-WT": {
        "cik": 1874474,
        "title": "Allego N.V."
    },
    "BPYPO": {
        "cik": 1545772,
        "title": "Brookfield Property Partners L.P."
    },
    "BPYPM": {
        "cik": 1545772,
        "title": "Brookfield Property Partners L.P."
    },
    "BPYPN": {
        "cik": 1545772,
        "title": "Brookfield Property Partners L.P."
    },
    "HTFC": {
        "cik": 1487428,
        "title": "Horizon Technology Finance Corp"
    },
    "RBCP": {
        "cik": 1324948,
        "title": "RBC Bearings INC"
    },
    "EQCDX": {
        "cik": 1582138,
        "title": "Equalize Community Development Fund"
    },
    "GECCM": {
        "cik": 1675033,
        "title": "Great Elm Capital Corp."
    },
    "GECCN": {
        "cik": 1675033,
        "title": "Great Elm Capital Corp."
    },
    "GECCO": {
        "cik": 1675033,
        "title": "Great Elm Capital Corp."
    },
    "UVXY": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "VIXY": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "ZSL": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "UCO": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "AGQ": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "ULE": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "GLL": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "SVXY": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "BOIL": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "VIXM": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "KOLD": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "YCL": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "EUO": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "SCO": {
        "cik": 1415311,
        "title": "ProShares Trust II"
    },
    "ATLCL": {
        "cik": 1464343,
        "title": "Atlanticus Holdings Corp"
    },
    "ATLCP": {
        "cik": 1464343,
        "title": "Atlanticus Holdings Corp"
    },
    "BEP-PA": {
        "cik": 1533232,
        "title": "Brookfield Renewable Partners L.P."
    },
    "JPM-PK": {
        "cik": 19617,
        "title": "JPMORGAN CHASE & CO"
    },
    "STRRP": {
        "cik": 707388,
        "title": "STAR EQUITY HOLDINGS, INC."
    },
    "DBGIW": {
        "cik": 1668010,
        "title": "Digital Brands Group, Inc."
    },
    "HTOOW": {
        "cik": 1819794,
        "title": "Fusion Fuel Green PLC"
    },
    "SPKX": {
        "cik": 1817218,
        "title": "ConvexityShares Trust"
    },
    "SPKY": {
        "cik": 1817218,
        "title": "ConvexityShares Trust"
    },
    "CVII-WT": {
        "cik": 1828248,
        "title": "Churchill Capital Corp VII"
    },
    "INVZW": {
        "cik": 1835654,
        "title": "Innoviz Technologies Ltd."
    },
    "CLBTW": {
        "cik": 1854587,
        "title": "Cellebrite DI Ltd."
    },
    "AUUDW": {
        "cik": 1554818,
        "title": "AUDDIA INC."
    },
    "SYF-PA": {
        "cik": 1601712,
        "title": "Synchrony Financial"
    },
    "SABRP": {
        "cik": 1597033,
        "title": "Sabre Corp"
    },
    "BWBBP": {
        "cik": 1341317,
        "title": "Bridgewater Bancshares Inc"
    },
    "PEB-PH": {
        "cik": 1474098,
        "title": "Pebblebrook Hotel Trust"
    },
    "ARGO-PA": {
        "cik": 1091748,
        "title": "Argo Group International Holdings, Ltd."
    },
    "VNO-PO": {
        "cik": 899689,
        "title": "VORNADO REALTY TRUST"
    },
    "NXPLW": {
        "cik": 1058307,
        "title": "NextPlat Corp"
    },
    "ADSEW": {
        "cik": 1879248,
        "title": "Ads-Tec Energy Public Ltd Co"
    },
    "BBAI-WT": {
        "cik": 1836981,
        "title": "BigBear.ai Holdings, Inc."
    },
    "ALVOW": {
        "cik": 1898416,
        "title": "Alvotech"
    },
    "DWACU": {
        "cik": 1849635,
        "title": "Digital World Acquisition Corp."
    },
    "JXN-PA": {
        "cik": 1822993,
        "title": "Jackson Financial Inc."
    },
    "DWACW": {
        "cik": 1849635,
        "title": "Digital World Acquisition Corp."
    },
    "PL-WT": {
        "cik": 1836833,
        "title": "Planet Labs PBC"
    },
    "BYTSW": {
        "cik": 1842566,
        "title": "BYTE Acquisition Corp."
    },
    "ASTSW": {
        "cik": 1780312,
        "title": "AST SpaceMobile, Inc."
    },
    "GROY-WT": {
        "cik": 1834026,
        "title": "Gold Royalty Corp."
    },
    "AMPX-WT": {
        "cik": 1899287,
        "title": "Amprius Technologies, Inc."
    },
    "EOSEW": {
        "cik": 1805077,
        "title": "Eos Energy Enterprises, Inc."
    },
    "PXSAW": {
        "cik": 1640043,
        "title": "Pyxis Tankers Inc."
    },
    "PXSAP": {
        "cik": 1640043,
        "title": "Pyxis Tankers Inc."
    },
    "KPLTW": {
        "cik": 1785424,
        "title": "Katapult Holdings, Inc."
    },
    "BC-PC": {
        "cik": 14930,
        "title": "BRUNSWICK CORP"
    },
    "BC-PB": {
        "cik": 14930,
        "title": "BRUNSWICK CORP"
    },
    "BC-PA": {
        "cik": 14930,
        "title": "BRUNSWICK CORP"
    },
    "RUMBW": {
        "cik": 1830081,
        "title": "Rumble Inc."
    },
    "ETWO-WT": {
        "cik": 1800347,
        "title": "E2open Parent Holdings, Inc."
    },
    "GOVXW": {
        "cik": 832489,
        "title": "GeoVax Labs, Inc."
    },
    "HTLFP": {
        "cik": 920112,
        "title": "HEARTLAND FINANCIAL USA INC"
    },
    "UGIC": {
        "cik": 884614,
        "title": "UGI CORP /PA/"
    },
    "C-PN": {
        "cik": 831001,
        "title": "CITIGROUP INC"
    },
    "NTRSO": {
        "cik": 73124,
        "title": "NORTHERN TRUST CORP"
    },
    "AGNCL": {
        "cik": 1423689,
        "title": "AGNC Investment Corp."
    },
    "AGNCP": {
        "cik": 1423689,
        "title": "AGNC Investment Corp."
    },
    "AGNCO": {
        "cik": 1423689,
        "title": "AGNC Investment Corp."
    },
    "PRSRU": {
        "cik": 1825473,
        "title": "Prospector Capital Corp."
    },
    "PRSRW": {
        "cik": 1825473,
        "title": "Prospector Capital Corp."
    },
    "SST-WT": {
        "cik": 1805833,
        "title": "System1, Inc."
    },
    "BEATW": {
        "cik": 1779372,
        "title": "HeartBeam, Inc."
    },
    "FCRX": {
        "cik": 1633336,
        "title": "Crescent Capital BDC, Inc."
    },
    "APXIW": {
        "cik": 1868573,
        "title": "APx Acquisition Corp. I"
    },
    "ANGHW": {
        "cik": 1871983,
        "title": "Anghami Inc"
    },
    "MVLAW": {
        "cik": 1839132,
        "title": "Movella Holdings Inc."
    },
    "PCTTW": {
        "cik": 1830033,
        "title": "PureCycle Technologies, Inc."
    },
    "BKSY-WT": {
        "cik": 1753539,
        "title": "BlackSky Technology Inc."
    },
    "LIDRW": {
        "cik": 1818644,
        "title": "AEye, Inc."
    },
    "UWMC-WT": {
        "cik": 1783398,
        "title": "UWM Holdings Corp"
    },
    "BDRY": {
        "cik": 1610940,
        "title": "ETF Managers Group Commodity Trust I"
    },
    "BCDAW": {
        "cik": 925741,
        "title": "BioCardia, Inc."
    },
    "DHCNL": {
        "cik": 1075415,
        "title": "DIVERSIFIED HEALTHCARE TRUST"
    },
    "MLPB": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "BDCX": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "AMUB": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "IWML": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "MVRL": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "SMHB": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "MLPR": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "CEFD": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "BDCZ": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "FBGX": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "UCIB": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "HDLB": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "SCDL": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "IFED": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "QULL": {
        "cik": 1114446,
        "title": "UBS AG"
    },
    "KEY-PL": {
        "cik": 91576,
        "title": "KEYCORP /NEW/"
    },
    "METXW": {
        "cik": 1796514,
        "title": "BTC Digital Ltd."
    },
    "XOSWW": {
        "cik": 1819493,
        "title": "Xos, Inc."
    },
    "LUCYW": {
        "cik": 1808377,
        "title": "Innovative Eyewear Inc"
    },
    "HPLTW": {
        "cik": 1863181,
        "title": "Home Plate Acquisition Corp"
    },
    "DATSW": {
        "cik": 1648960,
        "title": "DatChat, Inc."
    },
    "AMRLF": {
        "cik": 1699880,
        "title": "American Lithium Corp."
    },
    "BFIIW": {
        "cik": 1723580,
        "title": "BurgerFi International, Inc."
    },
    "SABSW": {
        "cik": 1833214,
        "title": "SAB Biotherapeutics, Inc."
    },
    "NWTNW": {
        "cik": 1932737,
        "title": "NWTN, Inc."
    },
    "LGHLW": {
        "cik": 1806524,
        "title": "Lion Group Holding Ltd"
    },
    "SUNL-WT": {
        "cik": 1821850,
        "title": "Sunlight Financial Holdings Inc."
    },
    "PRE-PJ": {
        "cik": 911421,
        "title": "PARTNERRE LTD"
    },
    "SPE-PC": {
        "cik": 897802,
        "title": "SPECIAL OPPORTUNITIES FUND, INC."
    },
    "GAB-PK": {
        "cik": 794685,
        "title": "GABELLI EQUITY TRUST INC"
    },
    "ONBPP": {
        "cik": 707179,
        "title": "OLD NATIONAL BANCORP /IN/"
    },
    "KMPB": {
        "cik": 860748,
        "title": "KEMPER Corp"
    },
    "HMLPF": {
        "cik": 1603016,
        "title": "Hoegh LNG Partners LP"
    },
    "FTAIP": {
        "cik": 1590364,
        "title": "FTAI Aviation Ltd."
    },
    "FTAIO": {
        "cik": 1590364,
        "title": "FTAI Aviation Ltd."
    },
    "FTAIM": {
        "cik": 1590364,
        "title": "FTAI Aviation Ltd."
    },
    "FTAIN": {
        "cik": 1590364,
        "title": "FTAI Aviation Ltd."
    },
    "SOYB": {
        "cik": 1471824,
        "title": "Teucrium Commodity Trust"
    },
    "WEAT": {
        "cik": 1471824,
        "title": "Teucrium Commodity Trust"
    },
    "DEFI": {
        "cik": 1471824,
        "title": "Teucrium Commodity Trust"
    },
    "CORN": {
        "cik": 1471824,
        "title": "Teucrium Commodity Trust"
    },
    "TAGS": {
        "cik": 1471824,
        "title": "Teucrium Commodity Trust"
    },
    "CANE": {
        "cik": 1471824,
        "title": "Teucrium Commodity Trust"
    },
    "PRS": {
        "cik": 1137774,
        "title": "PRUDENTIAL FINANCIAL INC"
    },
    "PRH": {
        "cik": 1137774,
        "title": "PRUDENTIAL FINANCIAL INC"
    },
    "CNFRL": {
        "cik": 1502292,
        "title": "Conifer Holdings, Inc."
    },
    "FOSLL": {
        "cik": 883569,
        "title": "Fossil Group, Inc."
    },
    "DGP": {
        "cik": 1159508,
        "title": "DEUTSCHE BANK AKTIENGESELLSCHAFT"
    },
    "RF-PE": {
        "cik": 1281761,
        "title": "REGIONS FINANCIAL CORP"
    },
    "ACR-PC": {
        "cik": 1332551,
        "title": "ACRES Commercial Realty Corp."
    },
    "ACR-PD": {
        "cik": 1332551,
        "title": "ACRES Commercial Realty Corp."
    },
    "RCFA-WT": {
        "cik": 1870143,
        "title": "RCF Acquisition Corp."
    },
    "OUST-WT": {
        "cik": 1816581,
        "title": "Ouster, Inc."
    },
    "OUST-WTA": {
        "cik": 1816581,
        "title": "Ouster, Inc."
    },
    "NETC-WT": {
        "cik": 1854458,
        "title": "Nabors Energy Transition Corp."
    },
    "GB-WT": {
        "cik": 1799983,
        "title": "Global Blue Group Holding AG"
    },
    "OCSAW": {
        "cik": 1953530,
        "title": "Oculis Holding AG"
    },
    "SLNAW": {
        "cik": 1909417,
        "title": "SELINA HOSPITALITY PLC"
    },
    "EVE-WT": {
        "cik": 1861121,
        "title": "EVe Mobility Acquisition Corp"
    },
    "FHN-PE": {
        "cik": 36966,
        "title": "FIRST HORIZON CORP"
    },
    "FHN-PB": {
        "cik": 36966,
        "title": "FIRST HORIZON CORP"
    },
    "FHN-PF": {
        "cik": 36966,
        "title": "FIRST HORIZON CORP"
    },
    "SNV-PE": {
        "cik": 18349,
        "title": "SYNOVUS FINANCIAL CORP"
    },
    "HFRO-PA": {
        "cik": 1710680,
        "title": "HIGHLAND OPPORTUNITIES & INCOME FUND"
    },
    "BTWNW": {
        "cik": 1815086,
        "title": "Bridgetown Holdings Ltd"
    },
    "SNAXW": {
        "cik": 1691936,
        "title": "STRYVE FOODS, INC."
    },
    "POL-WT": {
        "cik": 1810140,
        "title": "Polished.com Inc."
    },
    "OPP-PA": {
        "cik": 1678130,
        "title": "RiverNorth/DoubleLine Strategic Opportunity Fund, Inc."
    },
    "PRIF-PJ": {
        "cik": 1554625,
        "title": "Priority Income Fund, Inc."
    },
    "PRIF-PI": {
        "cik": 1554625,
        "title": "Priority Income Fund, Inc."
    },
    "PRIF-PK": {
        "cik": 1554625,
        "title": "Priority Income Fund, Inc."
    },
    "RTLPP": {
        "cik": 1568162,
        "title": "Necessity Retail REIT, Inc."
    },
    "RTLPO": {
        "cik": 1568162,
        "title": "Necessity Retail REIT, Inc."
    },
    "GNT-PA": {
        "cik": 1438893,
        "title": "GAMCO Natural Resources, Gold & Income Trust"
    },
    "EQH-PC": {
        "cik": 1333986,
        "title": "Equitable Holdings, Inc."
    },
    "ALSAW": {
        "cik": 1865111,
        "title": "Alpha Star Acquisition Corp"
    },
    "DMAQR": {
        "cik": 1857086,
        "title": "Deep Medicine Acquisition Corp."
    },
    "ADEX-WT": {
        "cik": 1830029,
        "title": "Adit EdTech Acquisition Corp."
    },
    "SHFSW": {
        "cik": 1854963,
        "title": "SHF Holdings, Inc."
    },
    "ADOCW": {
        "cik": 1824884,
        "title": "Edoc Acquisition Corp."
    },
    "ADOCR": {
        "cik": 1824884,
        "title": "Edoc Acquisition Corp."
    },
    "ARKOW": {
        "cik": 1823794,
        "title": "ARKO Corp."
    },
    "FILG": {
        "cik": 1852039,
        "title": "Grayscale Filecoin Trust (FIL)"
    },
    "SVIX": {
        "cik": 1793497,
        "title": "VS Trust"
    },
    "UVIX": {
        "cik": 1793497,
        "title": "VS Trust"
    },
    "TMCWW": {
        "cik": 1798562,
        "title": "TMC the metals Co Inc."
    },
    "CHRB": {
        "cik": 1730346,
        "title": "Charah Solutions, Inc."
    },
    "CSSEN": {
        "cik": 1679063,
        "title": "Chicken Soup for the Soul Entertainment, Inc."
    },
    "CVE-WT": {
        "cik": 1475260,
        "title": "CENOVUS ENERGY INC."
    },
    "RITM-PC": {
        "cik": 1556593,
        "title": "Rithm Capital Corp."
    },
    "SBFMW": {
        "cik": 1402328,
        "title": "Sunshine Biopharma, Inc"
    },
    "NIOBW": {
        "cik": 1512228,
        "title": "NIOCORP DEVELOPMENTS LTD"
    },
    "RITM-PB": {
        "cik": 1556593,
        "title": "Rithm Capital Corp."
    },
    "RITM-PA": {
        "cik": 1556593,
        "title": "Rithm Capital Corp."
    },
    "RITM-PD": {
        "cik": 1556593,
        "title": "Rithm Capital Corp."
    },
    "SMR-WT": {
        "cik": 1822966,
        "title": "NUSCALE POWER Corp"
    },
    "ZEV-WT": {
        "cik": 1802749,
        "title": "Lightning eMotors, Inc."
    },
    "APGNW": {
        "cik": 1814140,
        "title": "Apexigen, Inc."
    },
    "CFG-PE": {
        "cik": 759944,
        "title": "CITIZENS FINANCIAL GROUP INC/RI"
    },
    "AFRIW": {
        "cik": 1903870,
        "title": "Forafric Global PLC"
    },
    "EVTL-WT": {
        "cik": 1867102,
        "title": "Vertical Aerospace Ltd."
    },
    "BOH-PA": {
        "cik": 46195,
        "title": "BANK OF HAWAII CORP"
    },
    "PRETM": {
        "cik": 77281,
        "title": "PENNSYLVANIA REAL ESTATE INVESTMENT TRUST"
    },
    "PRETL": {
        "cik": 77281,
        "title": "PENNSYLVANIA REAL ESTATE INVESTMENT TRUST"
    },
    "SCE-PK": {
        "cik": 92103,
        "title": "SOUTHERN CALIFORNIA EDISON Co"
    },
    "SCE-PL": {
        "cik": 92103,
        "title": "SOUTHERN CALIFORNIA EDISON Co"
    },
    "TFC-PI": {
        "cik": 92230,
        "title": "TRUIST FINANCIAL CORP"
    },
    "TFC-PR": {
        "cik": 92230,
        "title": "TRUIST FINANCIAL CORP"
    },
    "TFC-PO": {
        "cik": 92230,
        "title": "TRUIST FINANCIAL CORP"
    },
    "LILMW": {
        "cik": 1855756,
        "title": "Lilium N.V."
    },
    "BURU-WT": {
        "cik": 1814215,
        "title": "Nuburu, Inc."
    },
    "PSFE-WT": {
        "cik": 1833835,
        "title": "Paysafe Ltd"
    },
    "PLTNW": {
        "cik": 1929231,
        "title": "Plutonian Acquisition Corp."
    },
    "DCFCW": {
        "cik": 1862490,
        "title": "Tritium DCFC Ltd"
    },
    "AGRIW": {
        "cik": 1826397,
        "title": "AGRIFORCE GROWING SYSTEMS LTD."
    },
    "PCGU": {
        "cik": 1004980,
        "title": "PG&E Corp"
    },
    "OTRKP": {
        "cik": 1136174,
        "title": "Ontrak, Inc."
    },
    "RILYG": {
        "cik": 1464790,
        "title": "B. Riley Financial, Inc."
    },
    "RILYT": {
        "cik": 1464790,
        "title": "B. Riley Financial, Inc."
    },
    "RILYM": {
        "cik": 1464790,
        "title": "B. Riley Financial, Inc."
    },
    "RILYP": {
        "cik": 1464790,
        "title": "B. Riley Financial, Inc."
    },
    "RILYN": {
        "cik": 1464790,
        "title": "B. Riley Financial, Inc."
    },
    "RILYZ": {
        "cik": 1464790,
        "title": "B. Riley Financial, Inc."
    },
    "RILYL": {
        "cik": 1464790,
        "title": "B. Riley Financial, Inc."
    },
    "AAM-PB": {
        "cik": 1411494,
        "title": "Apollo Asset Management, Inc."
    },
    "AAM-PA": {
        "cik": 1411494,
        "title": "Apollo Asset Management, Inc."
    },
    "JOBY-WT": {
        "cik": 1819848,
        "title": "Joby Aviation, Inc."
    },
    "TGH-PB": {
        "cik": 1413159,
        "title": "TEXTAINER GROUP HOLDINGS LTD"
    },
    "BWSN": {
        "cik": 1630805,
        "title": "Babcock & Wilcox Enterprises, Inc."
    },
    "CIVIW": {
        "cik": 1509589,
        "title": "CIVITAS RESOURCES, INC."
    }
}'''