import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
plt.style.use("seaborn")
import seaborn

# ===============================================================================
# Analisi degli effetti della diversificazione usando molti titoli o pochi titoli
# Emerge che bastano poche decine di titoli per diversificare a sufficenza
# ===============================================================================

# USARE QUESTO PER AVERE S&P500
SeP500 = [["Apple Inc.","AAPL",5.972092],["Microsoft Corporation","MSFT",5.195264],["Amazon.com Inc.","AMZN",2.379241],["Berkshire Hathaway Inc. Class B","BRK-B",1.744472],["Alphabet Inc. Class A","GOOGL",1.613283],["Alphabet Inc. Class C","GOOG",1.442776],["Johnson & Johnson","JNJ",1.410177],["UnitedHealth Group Incorporated","UNH",1.405054],["Exxon Mobil Corporation","XOM",1.37076],["JPMorgan Chase & Co.","JPM",1.236438],["NVIDIA Corporation","NVDA",1.195415],["Procter & Gamble Company","PG",1.105573],["Visa Inc. Class A","V",1.096749],["Home Depot Inc.","HD",0.997795],["Tesla Inc","TSLA",0.986464],["Mastercard Incorporated Class A","MA",0.966856],["Chevron Corporation","CVX",0.956271],["Meta Platforms Inc. Class A","META",0.89337],["AbbVie Inc.","ABBV",0.877282],["Merck & Co. Inc.","MRK",0.858758],["Eli Lilly and Company","LLY",0.846603],["Pfizer Inc.","PFE",0.833512],["PepsiCo Inc.","PEP",0.758131],["Coca-Cola Company","KO",0.747755],["Bank of America Corp","BAC",0.725827],["Broadcom Inc.","AVGO",0.716962],["Thermo Fisher Scientific Inc.","TMO",0.657217],["Costco Wholesale Corporation","COST",0.650236],["Walmart Inc.","WMT",0.627775],["Cisco Systems Inc.","CSCO",0.612083],["McDonald's Corporation","MCD",0.600491],["Abbott Laboratories","ABT",0.59982],["Verizon Communications Inc.","VZ",0.533153],["Walt Disney Company","DIS",0.530158],["Accenture Plc Class A","ACN",0.528608],["Danaher Corporation","DHR",0.512754],["NextEra Energy Inc.","NEE",0.512642],["Comcast Corporation Class A","CMCSA",0.497075],["Wells Fargo & Company","WFC",0.495657],["Texas Instruments Incorporated","TXN",0.493682],["Adobe Incorporated","ADBE",0.489401],["Linde plc","LIN",0.48837],["Philip Morris International Inc.","PM",0.486636],["NIKE Inc. Class B","NKE",0.482411],["Bristol-Myers Squibb Company","BMY",0.463078],["Salesforce Inc.","CRM",0.451387],["Raytheon Technologies Corporation","RTX",0.44971],["ConocoPhillips","COP",0.448749],["Amgen Inc.","AMGN",0.441853],["Honeywell International Inc.","HON",0.433987],["Netflix Inc.","NFLX",0.430386],["AT&T Inc.","T",0.416399],["Oracle Corporation","ORCL",0.407548],["United Parcel Service Inc. Class B","UPS",0.406095],["Union Pacific Corporation","UNP",0.39893],["Charles Schwab Corp","SCHW",0.398872],["International Business Machines Corporation","IBM",0.398262],["Caterpillar Inc.","CAT",0.393825],["QUALCOMM Incorporated","QCOM",0.393572],["Lowe's Companies Inc.","LOW",0.379872],["Intel Corporation","INTC",0.371181],["Starbucks Corporation","SBUX",0.368938],["CVS Health Corporation","CVS",0.368887],["Goldman Sachs Group Inc.","GS",0.368308],["Deere & Company","DE",0.360904],["Boeing Company","BA",0.358554],["S&P Global Inc.","SPGI",0.357988],["Morgan Stanley","MS",0.354531],["BlackRock Inc.","BLK",0.347126],["Elevance Health Inc.","ELV",0.345529],["Intuit Inc.","INTU",0.341941],["Advanced Micro Devices Inc.","AMD",0.332127],["Prologis Inc.","PLD",0.328743],
          ["Lockheed Martin Corporation","LMT",0.328513],["Gilead Sciences Inc.","GILD",0.327529],["Medtronic Plc","MDT",0.316254],["American Tower Corporation","AMT",0.313324],["Automatic Data Processing Inc.","ADP",0.304246],["TJX Companies Inc","TJX",0.291838],["Intuitive Surgical Inc.","ISRG",0.289022],["Chubb Limited","CB",0.285456],["Cigna Corporation","CI",0.284308],["Citigroup Inc.","C",0.282546],["Mondelez International Inc. Class A","MDLZ",0.281817],["Applied Materials Inc.","AMAT",0.281125],["American Express Company","AXP",0.275858],["T-Mobile US Inc.","TMUS",0.273871],["PayPal Holdings Inc.","PYPL",0.269647],["Stryker Corporation","SYK",0.268699],["Analog Devices Inc.","ADI",0.26569],["Booking Holdings Inc.","BKNG",0.262864],["Marsh & McLennan Companies Inc.","MMC",0.259978],["Altria Group Inc","MO",0.253216],["Duke Energy Corporation","DUK",0.248565],["General Electric Company","GE",0.242898],["Schlumberger NV","SLB",0.242102],["Southern Company","SO",0.238857],["Progressive Corporation","PGR",0.237003],["ServiceNow Inc.","NOW",0.233859],["EOG Resources Inc.","EOG",0.23026],["Vertex Pharmaceuticals Incorporated","VRTX",0.223092],["Regeneron Pharmaceuticals Inc.","REGN",0.222935],["Target Corporation","TGT",0.221715],["Becton Dickinson and Company","BDX",0.220153],["Northrop Grumman Corp.","NOC",0.220079],["3M Company","MMM",0.215052],["Air Products and Chemicals Inc.","APD",0.212123],["Zoetis Inc. Class A","ZTS",0.210301],["CSX Corporation","CSX",0.207347],["PNC Financial Services Group Inc.","PNC",0.203314],["Colgate-Palmolive Company","CL",0.201143],["Boston Scientific Corporation","BSX",0.200375],["Fiserv Inc.","FISV",0.199639],["Eaton Corp. Plc","ETN",0.19594],["Illinois Tool Works Inc.","ITW",0.195523],["Aon Plc Class A","AON",0.194443],["CME Group Inc. Class A","CME",0.194055],["Equinix Inc.","EQIX",0.193415],["Crown Castle Inc.","CCI",0.193182],["U.S. Bancorp","USB",0.192707],["Lam Research Corporation","LRCX",0.18949],["Micron Technology Inc.","MU",0.18802],["Freeport-McMoRan Inc.","FCX",0.187285],["Humana Inc.","HUM",0.187147],["Moderna Inc.","MRNA",0.186492],["Truist Financial Corporation","TFC",0.186463],["Estee Lauder Companies Inc. Class A","EL",0.184866],["Waste Management Inc.","WM",0.182023],["Norfolk Southern Corporation","NSC",0.180603],["Intercontinental Exchange Inc.","ICE",0.179529],["KLA Corporation","KLAC",0.177062],["Emerson Electric Co.","EMR",0.176096],["Sherwin-Williams Company","SHW",0.170231],["General Dynamics Corporation","GD",0.1686],["Activision Blizzard Inc.","ATVI",0.168098],["Pioneer Natural Resources Company","PXD",0.167961],["McKesson Corporation","MCK",0.167932],["Dollar General Corporation","DG",0.167117],["Marathon Petroleum Corporation","MPC",0.166475],["HCA Healthcare Inc","HCA",0.164483],["O'Reilly Automotive Inc.","ORLY",0.159142],["Dominion Energy Inc","D",0.156789],["General Motors Company","GM",0.156594],
          ["American Electric Power Company Inc.","AEP",0.154449],["General Mills Inc.","GIS",0.15429],["Ford Motor Company","F",0.15325],["Valero Energy Corporation","VLO",0.152112],["Synopsys Inc.","SNPS",0.152103],["Sempra Energy","SRE",0.151562],["Phillips 66","PSX",0.149645],["MetLife Inc.","MET",0.146185],["American International Group Inc.","AIG",0.145617],["Edwards Lifesciences Corporation","EW",0.144928],["Amphenol Corporation Class A","APH",0.14448],["Roper Technologies Inc.","ROP",0.144299],["Archer-Daniels-Midland Company","ADM",0.143905],["Occidental Petroleum Corporation","OXY",0.142978],["AutoZone Inc.","AZO",0.142244],["Kimberly-Clark Corporation","KMB",0.141455],["Johnson Controls International plc","JCI",0.140653],["Moody's Corporation","MCO",0.140293],["FedEx Corporation","FDX",0.139394],["Cadence Design Systems Inc.","CDNS",0.13905],["Travelers Companies Inc.","TRV",0.137296],["Public Storage","PSA",0.135879],["Centene Corporation","CNC",0.135632],["Agilent Technologies Inc.","A",0.134541],["Corteva Inc","CTVA",0.134153],["Exelon Corporation","EXC",0.13388],["Motorola Solutions Inc.","MSI",0.132857],["DexCom Inc.","DXCM",0.131727],["NXP Semiconductors NV","NXPI",0.129153],["Autodesk Inc.","ADSK",0.127722],["Fidelity National Information Services Inc.","FIS",0.127459],["Ross Stores Inc.","ROST",0.126913],["Newmont Corporation","NEM",0.126425],["Trane Technologies plc","TT",0.126398],["Marriott International Inc. Class A","MAR",0.125934],["Aflac Incorporated","AFL",0.125663],["Devon Energy Corporation","DVN",0.124544],["Realty Income Corporation","O",0.124514],["Microchip Technology Incorporated","MCHP",0.124273],["Sysco Corporation","SYY",0.123393],["Arthur J. Gallagher & Co.","AJG",0.123355],["Chipotle Mexican Grill Inc.","CMG",0.122733],["Hess Corporation","HES",0.121821],["Biogen Inc.","BIIB",0.121754],["Williams Companies Inc.","WMB",0.121581],["Dow Inc.","DOW",0.121419],["Charter Communications Inc. Class A","CHTR",0.121023],["Parker-Hannifin Corporation","PH",0.121015],["Xcel Energy Inc.","XEL",0.120873],["Monster Beverage Corporation","MNST",0.118979],["IQVIA Holdings Inc","IQV",0.118883],["TE Connectivity Ltd.","TEL",0.118738],["MSCI Inc. Class A","MSCI",0.118715],["Simon Property Group Inc.","SPG",0.117793],["L3Harris Technologies Inc","LHX",0.117546],["Cintas Corporation","CTAS",0.116073],["Allstate Corporation","ALL",0.115739],["Paychex Inc.","PAYX",0.115561],["Capital One Financial Corp","COF",0.114384],["IDEXX Laboratories Inc.","IDXX",0.114092],["Kinder Morgan Inc Class P","KMI",0.11343],["Ecolab Inc.","ECL",0.113259],["Nucor Corporation","NUE",0.112968],["Yum! Brands Inc.","YUM",0.112868],["Halliburton Company","HAL",0.112683],["DuPont de Nemours Inc.","DD",0.11256],["Carrier Global Corp.","CARR",0.111964],["Prudential Financial Inc.","PRU",0.111664],["Bank of New York Mellon Corp","BK",0.108264],["Hilton Worldwide Holdings Inc","HLT",0.108158],
          ["Constellation Brands Inc. Class A","STZ",0.107346],["PACCAR Inc","PCAR",0.106491],["Consolidated Edison Inc.","ED",0.106409],["Ameriprise Financial Inc.","AMP",0.106264],["Cummins Inc.","CMI",0.105227],["Otis Worldwide Corporation","OTIS",0.104566],["Kraft Heinz Company","KHC",0.102786],["TransDigm Group Incorporated","TDG",0.102601],["Hershey Company","HSY",0.101227],["Welltower Inc","WELL",0.10044],["Electronic Arts Inc.","EA",0.100289],["Mettler-Toledo International Inc.","MTD",0.100162],["Illumina Inc.","ILMN",0.100063],["AMETEK Inc.","AME",0.099793],["Fortinet Inc.","FTNT",0.098895],["Public Service Enterprise Group Inc","PEG",0.097223],["Keysight Technologies Inc","KEYS",0.097182],["Cognizant Technology Solutions Corporation Class A","CTSH",0.096263],["CoStar Group Inc.","CSGP",0.096193],["SBA Communications Corp. Class A","SBAC",0.096004],["Rockwell Automation Inc.","ROK",0.09463],["Baker Hughes Company Class A","BKR",0.094491],["Enphase Energy Inc.","ENPH",0.094397],["ResMed Inc.","RMD",0.094257],["VICI Properties Inc","VICI",0.093879],["Keurig Dr Pepper Inc.","KDP",0.093603],["WEC Energy Group Inc","WEC",0.093462],["Dollar Tree Inc.","DLTR",0.092927],["ONEOK Inc.","OKE",0.092837],["PPG Industries Inc.","PPG",0.092623],
          ["Kroger Co.","KR",0.092355],["State Street Corporation","STT",0.091104],["Eversource Energy","ES",0.090788],["Global Payments Inc.","GPN",0.090246],["D.R. Horton Inc.","DHI",0.089688],["Digital Realty Trust Inc.","DLR",0.08888],["American Water Works Company Inc.","AWK",0.088404],["Verisk Analytics Inc","VRSK",0.087383],["International Flavors & Fragrances Inc.","IFF",0.087129],["Discover Financial Services","DFS",0.086772],["Arista Networks Inc.","ANET",0.086568],["Old Dominion Freight Line Inc.","ODFL",0.085819],["Willis Towers Watson Public Limited Company","WTW",0.085698],["ON Semiconductor Corporation","ON",0.085633],["Constellation Energy Corporation","CEG",0.084289],["Fastenal Company","FAST",0.08349],["Copart Inc.","CPRT",0.082106],["Corning Inc","GLW",0.082084],["AmerisourceBergen Corporation","ABC",0.081986],["Aptiv PLC","APTV",0.081465],["Zimmer Biomet Holdings Inc.","ZBH",0.081167],["Albemarle Corporation","ALB",0.08052],["United Rentals Inc.","URI",0.080435],["CBRE Group Inc. Class A","CBRE",0.08027],["Republic Services Inc.","RSG",0.080228],["Walgreens Boots Alliance Inc.","WBA",0.080065],["M&T Bank Corporation","MTB",0.0798],["HP Inc.","HPQ",0.079725],["Gartner Inc.","IT",0.079622],["Edison International","EIX",0.079437],
          ["T. Rowe Price Group","TROW",0.079182],["PG&E Corporation","PCG",0.07885],["Warner Bros. Discovery Inc. Series A","WBD",0.0779],["Ulta Beauty Inc.","ULTA",0.077217],["W.W. Grainger Inc.","GWW",0.077215],["Diamondback Energy Inc.","FANG",0.076901],["Equifax Inc.","EFX",0.076884],["Hartford Financial Services Group Inc.","HIG",0.075952],["CDW Corp.","CDW",0.075722],["Lennar Corporation Class A","LEN",0.07431],["Genuine Parts Company","GPC",0.07393],["Tractor Supply Company","TSCO",0.073814],["eBay Inc.","EBAY",0.073125],["Vulcan Materials Company","VMC",0.072605],["Fifth Third Bancorp","FITB",0.072077],["Fortive Corp.","FTV",0.071437],["Weyerhaeuser Company","WY",0.071345],["Delta Air Lines Inc.","DAL",0.071286],["Arch Capital Group Ltd.","ACGL",0.07113],["LyondellBasell Industries NV","LYB",0.071072],["Ameren Corporation","AEE",0.070927],["DTE Energy Company","DTE",0.070729],["FirstEnergy Corp.","FE",0.070382],["AvalonBay Communities Inc.","AVB",0.06975],["First Republic Bank","FRC",0.069522],["Baxter International Inc.","BAX",0.068614],["Ingersoll Rand Inc.","IR",0.068446],["PPL Corporation","PPL",0.067845],["Laboratory Corporation of America Holdings","LH",0.067336],["Entergy Corporation","ETR",0.067229],
          ["Hewlett Packard Enterprise Co.","HPE",0.067117],["Alexandria Real Estate Equities Inc.","ARE",0.066364],["Raymond James Financial Inc.","RJF",0.065583],["ANSYS Inc.","ANSS",0.065464],["Martin Marietta Materials Inc.","MLM",0.065241],["McCormick & Company Incorporated","MKC",0.065064],["Nasdaq Inc.","NDAQ",0.064904],["Southwest Airlines Co.","LUV",0.064881],["GE Healthcare Technologies Inc.","GEHC",0.064733],["Regions Financial Corporation","RF",0.063589],["Huntington Bancshares Incorporated","HBAN",0.06324],["Cardinal Health Inc.","CAH",0.062395],["Citizens Financial Group Inc.","CFG",0.061825],["Principal Financial Group Inc.","PFG",0.061525],["Hologic Inc.","HOLX",0.06115],["Xylem Inc.","XYL",0.061036],["Church & Dwight Co. Inc.","CHD",0.060911],["Dover Corporation","DOV",0.060577],["Equity Residential","EQR",0.060478],["Coterra Energy Inc.","CTRA",0.060251],["Quanta Services Inc.","PWR",0.060078],["Extra Space Storage Inc.","EXR",0.059711],["Northern Trust Corporation","NTRS",0.059481],["VeriSign Inc.","VRSN",0.059426],["Conagra Brands Inc.","CAG",0.058812],["Tyson Foods Inc. Class A","TSN",0.058676],["Waters Corporation","WAT",0.058632],["CenterPoint Energy Inc.","CNP",0.058168],["STERIS Plc","STE",0.058101],
          ["Ventas Inc.","VTR",0.057926],["Teledyne Technologies Incorporated","TDY",0.057838],["CMS Energy Corporation","CMS",0.057217],["EPAM Systems Inc.","EPAM",0.057009],["Westinghouse Air Brake Technologies Corporation","WAB",0.056127],["Amcor PLC","AMCR",0.05611],["Kellogg Company","K",0.056065],["Darden Restaurants Inc.","DRI",0.055523],["AES Corporation","AES",0.055017],["Expeditors International of Washington Inc.","EXPD",0.054957],["Quest Diagnostics Incorporated","DGX",0.054485],["Mid-America Apartment Communities Inc.","MAA",0.054357],["West Pharmaceutical Services Inc.","WST",0.053932],["IDEX Corporation","IEX",0.053837],["Omnicom Group Inc","OMC",0.053631],["Ball Corporation","BALL",0.053405],["Clorox Company","CLX",0.053085],["Las Vegas Sands Corp.","LVS",0.053033],["Cincinnati Financial Corporation","CINF",0.052906],["Invitation Homes Inc.","INVH",0.052831],["Molina Healthcare Inc.","MOH",0.052715],["Marathon Oil Corporation","MRO",0.052674],["J.M. Smucker Company","SJM",0.052602],["CF Industries Holdings Inc.","CF",0.052406],["Monolithic Power Systems Inc.","MPWR",0.052078],["Targa Resources Corp.","TRGP",0.051752],["Steel Dynamics Inc.","STLD",0.051639],["KeyCorp","KEY",0.051373],["Cooper Companies Inc.","COO",0.051345],
          ["PerkinElmer Inc.","PKI",0.05131],["Align Technology Inc.","ALGN",0.050664],["Best Buy Co. Inc.","BBY",0.050637],["Take-Two Interactive Software Inc.","TTWO",0.050468],["Broadridge Financial Solutions Inc.","BR",0.050063],["Mosaic Company","MOS",0.049843],["FMC Corporation","FMC",0.049682],["Jacobs Solutions Inc.","J",0.04961],["First Solar Inc.","FSLR",0.048424],["Atmos Energy Corporation","ATO",0.048239],["SolarEdge Technologies Inc.","SEDG",0.04798],["Avery Dennison Corporation","AVY",0.047566],["Skyworks Solutions Inc.","SWKS",0.047287],["Etsy Inc.","ETSY",0.046548],["FactSet Research Systems Inc.","FDS",0.046409],["Garmin Ltd.","GRMN",0.046339],["Textron Inc.","TXT",0.045601],["W. R. Berkley Corporation","WRB",0.045534],["Howmet Aerospace Inc.","HWM",0.045264],["J.B. Hunt Transport Services Inc.","JBHT",0.045239],["NVR Inc.","NVR",0.044976],["Incyte Corporation","INCY",0.04491],["Teradyne Inc.","TER",0.044697],["Synchrony Financial","SYF",0.044642],["Evergy Inc.","EVRG",0.044557],["Iron Mountain Inc.","IRM",0.044413],["LKQ Corporation","LKQ",0.044299],["SVB Financial Group","SIVB",0.044298],["Zebra Technologies Corporation Class A","ZBRA",0.04422],["Viatris Inc.","VTRS",0.04399],["FLEETCOR Technologies Inc.","FLT",0.043725],
          ["Paycom Software Inc.","PAYC",0.043642],["United Airlines Holdings Inc.","UAL",0.043487],["Lamb Weston Holdings Inc.","LW",0.043345],["NetApp Inc.","NTAP",0.043318],["APA Corp.","APA",0.043298],["Healthpeak Properties Inc.","PEAK",0.042893],["Expedia Group Inc.","EXPE",0.042841],["Everest Re Group Ltd.","RE",0.042568],["Interpublic Group of Companies Inc.","IPG",0.042389],["Akamai Technologies Inc.","AKAM",0.04219],["Alliant Energy Corp","LNT",0.042032],["Essex Property Trust Inc.","ESS",0.041888],["Leidos Holdings Inc.","LDOS",0.041849],["Brown & Brown Inc.","BRO",0.041666],["International Paper Company","IP",0.040931],["Hormel Foods Corporation","HRL",0.040784],["Tyler Technologies Inc.","TYL",0.040759],["PTC Inc.","PTC",0.040425],["Jack Henry & Associates Inc.","JKHY",0.039837],["Trimble Inc.","TRMB",0.039799],["Nordson Corporation","NDSN",0.039797],["Bio-Techne Corporation","TECH",0.039564],["Kimco Realty Corporation","KIM",0.039545],["Cboe Global Markets Inc","CBOE",0.039469],["Snap-on Incorporated","SNA",0.039297],["EQT Corporation","EQT",0.038698],["Pool Corporation","POOL",0.038572],["Royal Caribbean Group","RCL",0.038376],["Packaging Corporation of America","PKG",0.038135],["Gen Digital Inc.","GEN",0.037863],
          ["Match Group Inc.","MTCH",0.037692],["MGM Resorts International","MGM",0.03756],["Stanley Black & Decker Inc.","SWK",0.037092],["MarketAxess Holdings Inc.","MKTX",0.03671],["Camden Property Trust","CPT",0.036697],["Domino's Pizza Inc.","DPZ",0.036614],["Teleflex Incorporated","TFX",0.03642],["UDR Inc.","UDR",0.036124],["Brown-Forman Corporation Class B","BF-B",0.035797],["Western Digital Corporation","WDC",0.035754],["Celanese Corporation","CE",0.035601],["C.H. Robinson Worldwide Inc.","CHRW",0.035378],["Loews Corporation","L",0.03518],["Host Hotels & Resorts Inc.","HST",0.034877],["Masco Corporation","MAS",0.034733],["Charles River Laboratories International Inc.","CRL",0.034667],["Campbell Soup Company","CPB",0.034633],["NiSource Inc","NI",0.034486],["Henry Schein Inc.","HSIC",0.034064],["PulteGroup Inc.","PHM",0.034039],["Globe Life Inc.","GL",0.033289],["Eastman Chemical Company","EMN",0.033266],["CarMax Inc.","KMX",0.033087],["Seagate Technology Holdings PLC","STX",0.033013],["Tapestry Inc.","TPR",0.031763],["Live Nation Entertainment Inc.","LYV",0.03139],["Bath & Body Works Inc.","BBWI",0.031379],["Juniper Networks Inc.","JNPR",0.031345],["BorgWarner Inc.","BWA",0.030795],["Allegion Public Limited Company","ALLE",0.0305],
          ["Universal Health Services Inc. Class B","UHS",0.030292],["Wynn Resorts Limited","WYNN",0.030269],["Paramount Global Class B","PARA",0.030186],["Qorvo Inc.","QRVO",0.030059],["Ceridian HCM Holding Inc.","CDAY",0.029434],["Fox Corporation Class A","FOXA",0.029317],["V.F. Corporation","VFC",0.029],["Regency Centers Corporation","REG",0.028952],["Molson Coors Beverage Company Class B","TAP",0.028838],["American Airlines Group Inc.","AAL",0.028624],["WestRock Company","WRK",0.028472],["Boston Properties Inc.","BXP",0.028276],["Caesars Entertainment Inc","CZR",0.028275],["Advance Auto Parts Inc.","AAP",0.028202],["Carnival Corporation","CCL",0.028164],["Bio-Rad Laboratories Inc. Class A","BIO",0.027751],["Huntington Ingalls Industries Inc.","HII",0.026944],["Comerica Incorporated","CMA",0.026891],["Invesco Ltd.","IVZ",0.026802],["Catalent Inc","CTLT",0.026233],["F5 Inc.","FFIV",0.026084],["Pinnacle West Capital Corporation","PNW",0.025971],["Rollins Inc.","ROL",0.025945],["Robert Half International Inc.","RHI",0.025398],["Whirlpool Corporation","WHR",0.025367],["Hasbro Inc.","HAS",0.024835],["A. O. Smith Corporation","AOS",0.024133],["Sealed Air Corporation","SEE",0.023985],["Pentair plc","PNR",0.023847],["Franklin Resources Inc.","BEN",0.02376],
          ["Zions Bancorporation N.A.","ZION",0.023517],["NRG Energy Inc.","NRG",0.023479],["Federal Realty Investment Trust","FRT",0.023081],["Organon & Co.","OGN",0.022834],["News Corporation Class A","NWSA",0.022747],["Signature Bank","SBNY",0.022084],["DENTSPLY SIRONA Inc.","XRAY",0.021835],["Assurant Inc.","AIZ",0.020374],["Generac Holdings Inc.","GNRC",0.020031],["DXC Technology Co.","DXC",0.019866],["Mohawk Industries Inc.","MHK",0.01762],["Norwegian Cruise Line Holdings Ltd.","NCLH",0.017473],["Alaska Air Group Inc.","ALK",0.017329],["Newell Brands Inc","NWL",0.01676],["Lumen Technologies Inc.","LUMN",0.015085],["Ralph Lauren Corporation Class A","RL",0.015011],["Lincoln National Corp","LNC",0.01452],["DaVita Inc.","DVA",0.013406],["Fox Corporation Class B","FOX",0.01319],["DISH Network Corporation Class A","DISH",0.011947],["News Corporation Class B","NWS",0.007208]]
tickers = list(np.array(SeP500)[:, 1])
nomi = list(np.array(SeP500)[:, 0])
pesi = list(np.array(SeP500)[:, 2].astype(float))

# resetta i pesi a uguale a 1
pesi = list(np.array([1]*len(tickers)))

dati = yf.download(tickers)["Adj Close"]

# rimetto a posto le colonne che non ho capito perché me le scombina
dati = dati.reindex(tickers, axis=1)

# Qui dobbiamo buttare quelli con più di 50 missing nelle ultime 1000 osservazioni (circa 4 anni)

toglici = list(dati.columns[dati.iloc[-1000:].isnull().sum(axis = 0) > 50])
print("TOGLIAMO: ")
for x in toglici:
    j = tickers.index(x)
    pesi.pop(j)
    print(tickers.pop(j), end=": ")
    print(nomi.pop(j))
dati.drop(toglici, axis=1, inplace=True)

rendimenti = dati.pct_change(1)
# normalizziamo i pesi a somma 1
pesi = np.divide(pesi, sum(pesi))

rendimentiPortafoglio = np.dot(rendimenti.dropna(), pesi) # numpy.dot is the matrix multiplication 
rendimentoPortafoglioAnnuale = (rendimentiPortafoglio.mean() + 1)**264 -1
print("Rendimento annuo medio", round(rendimentoPortafoglioAnnuale*100, 2), "%")

volatilitaPortafoglio = rendimentiPortafoglio.std()*np.sqrt(264)
print("Volatilità giornaliera media annualizzata", round(volatilitaPortafoglio*100, 2), "%")

pd.Series(rendimentiPortafoglio).plot(kind="hist", bins=100, figsize=(20, 10))

r = []
v = []
d = []
count = 0
for x in range(1, len(dati.columns) + 1):
    limite = list(range(0, x))
    rendimentiL = rendimenti.iloc[:, limite]
    pesiL = pesi[limite]
    pesiL = np.divide(pesiL, sum(pesiL))
    tickersL = tickers[limite[0]:limite[-1]]
    if len(rendimentiL.dropna()) < 264*5:
        break
    count = count + 1
    rendimentiPortafoglioL = np.dot(rendimentiL.dropna(), pesiL) # numpy.dot is the matrix multiplication 
    rendimentoPortafoglioAnnualeL = (rendimentiPortafoglioL.mean() + 1)**264 - 1
    # print("Rendimento annuo medio L", round(rendimentoPortafoglioAnnualeL*100, 2), "%")
    volatilitaPortafoglioL = rendimentiPortafoglioL.std() * np.sqrt(264)
    # print("Volatilità giornaliera media annualizzata L", round(volatilitaPortafoglioL * 100, 2), "%")
    r.append(rendimentoPortafoglioAnnualeL)
    v.append(volatilitaPortafoglioL)
    d.append(len(rendimentiL.dropna()))
summaryTable = pd.DataFrame({"Rendimento":np.array(r) * 100,"Volatilita":np.array(v) * 100, "Quanti":np.array(d), "Adding":tickers[:count]}, range(1, count + 1))
summaryTable

summaryTable.plot.scatter(x="Volatilita", y="Rendimento", figsize=(15,10), fontsize=18, s=1, color="r")
for i in summaryTable.index:
    plt.annotate(i, xy=(summaryTable.loc[i,"Volatilita"], summaryTable.loc[i, "Rendimento"]), size=12)
    
nomi[0:20]

plt.figure(figsize=(15,10))
seaborn.set(font_scale=1.4)
#seaborn.heatmap(rendimenti.iloc[:,0:14].corr(), cmap="Reds", annot=True, vmin=0.2, vmax=1, annot_kws={"size":14})
seaborn.heatmap(rendimenti.iloc[:,0:20].corr(), cmap="Reds", annot=True, annot_kws={"size":14})

# Analisi a 5 anni!
r = []
v = []
d = []
rendimenti10 = dati.pct_change(264*5)
count = 0
for x in range(1,len(dati.columns)+1):
    limite = list(range(0, x))
    rendimentiL = rendimenti10.iloc[:, limite]
    rendimentiL = rendimenti10.iloc[:, limite]
    if len(rendimentiL.dropna()) < 264*5:
        break
    count = count + 1
    pesiL = pesi[limite]
    pesiL = np.divide(pesiL, sum(pesiL))
    tickersL = tickers[limite[0]:limite[-1]]
    rendimentiPortafoglioL = np.dot(rendimentiL.dropna(), pesiL) # numpy.dot is the matrix multiplication 
    rendimentoPortafoglioL = rendimentiPortafoglioL.mean()
    # print("Rendimento annuo medio L", round(rendimentoPortafoglioAnnualeL*100, 2), "%")
    volatilitaPortafoglioL = rendimentiPortafoglioL.std()
    # print("Volatilità giornaliera media annualizzata L", round(volatilitaPortafoglioL*100,2), "%")
    r.append(rendimentoPortafoglioL)
    v.append(volatilitaPortafoglioL)
    d.append(len(rendimentiL.dropna()))
summaryTable = pd.DataFrame({"Rendimento":np.array(r)*100, "Volatilita":np.array(v)*100, "Quanti":np.array(d), "Adding":tickers[:count]}, range(1, count+1))
summaryTable

summaryTable.plot.scatter(x="Volatilita", y="Rendimento", figsize=(15,10), fontsize=18, s=1, color="r")
for i in summaryTable.index:
    plt.annotate(i, xy=(summaryTable.loc[i,"Volatilita"], summaryTable.loc[i,"Rendimento"]), size=12)
    
nomi[0:20]

# This is our portafoglio
# USARE QUESTO PER SCEGLIERE I TICKERS
#tickers = ["AMZN","BRK-B","JNJ","GOOGL","XOM"]
#tickers = ["AMZN","JNJ","GOOGL","XOM"]
tickers = ["AMZN","JNJ","GOOGL","XOM","SGLD.L"]
#tickers = ["^GSPC","G.MI"]

# resetta i pesi a uguale a 1
pesi = np.array([1]*len(tickers))
# normalizziamo i pesi a somma 1
pesi = np.divide(pesi, sum(pesi))

dati = yf.download(tickers)["Adj Close"]

# rimetto a posto le colonne che non ho capito perché me le scombina
dati = dati.reindex(tickers, axis=1)

dati.info()

r = []
v = []
d = []
rendimenti10 = dati.pct_change(264*5)
count = 0
for x in range(1, len(dati.columns) + 1):
    limite = list(range(0,x))
    rendimentiL = rendimenti10.iloc[:, limite]
    if len(rendimentiL.dropna()) < 264*5:
        break
    count = count + 1
    pesiL = pesi[limite]
    pesiL = np.divide(pesiL, sum(pesiL))
    tickersL = tickers[limite[0]:limite[-1]]
    rendimentiPortafoglioL = np.dot(rendimentiL.dropna(), pesiL) # numpy.dot is the matrix multiplication 
    rendimentoPortafoglioL = rendimentiPortafoglioL.mean()
    # print("Rendimento annuo medio L", round(rendimentoPortafoglioAnnualeL*100, 2), "%")
    volatilitaPortafoglioL = rendimentiPortafoglioL.std()
    # print("Volatilità giornaliera media annualizzata L", round(volatilitaPortafoglioL*100, 2), "%")
    r.append(rendimentoPortafoglioL)
    v.append(volatilitaPortafoglioL)
    d.append(len(rendimentiL.dropna()))
summaryTable = pd.DataFrame({"Rendimento":np.array(r)*100, "Volatilita":np.array(v)*100, "Quanti":np.array(d), "Adding":tickers[:count]}, range(1, count + 1))
print(summaryTable)
summaryTable.plot.scatter(x="Volatilita", y="Rendimento", figsize=(15,10), fontsize=18, s=1, color="r")
for i in summaryTable.index:
    plt.annotate(i, xy=(summaryTable.loc[i, "Volatilita"], summaryTable.loc[i, "Rendimento"]), size=12)
    
plt.figure(figsize=(15,10))
seaborn.set(font_scale=1.4)
#seaborn.heatmap(rendimenti10.iloc[:,0:14].corr(), cmap="Reds", annot=True, vmin=0.2, vmax=1, annot_kws={"size":14})
seaborn.heatmap(rendimenti10.iloc[:,0:20].corr(), cmap="Reds", annot=True, annot_kws={"size":14})
