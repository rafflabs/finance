import plotly.express as px
import pandas_datareader
import datetime
import pandas_datareader.data as web
import plotly.graph_objects as go


#Extract 2019 and 2020 YTD data
start = datetime.datetime(2009, 9, 26)
end = datetime.datetime(2022, 9, 7)
# MSCI_World_EUR = web.DataReader('SWDA.MI', 'yahoo', start, end)
VTI = web.DataReader('VTI', 'yahoo', start, end)
SPTL = web.DataReader('SPTL', 'yahoo', start, end)
IEF = web.DataReader('IEF', 'yahoo', start, end)
SPIP = web.DataReader('SPIP', 'yahoo', start, end)
DGL = web.DataReader('DGL', 'yahoo', start, end)

# print("\nMSCI_World_EUR\n", MSCI_World_EUR)
print("\nVTI\n", VTI)
print("\nSPTL\n", SPTL)
print("\nIEF\n", IEF)
print("\SPIP\n", SPIP)
print("\DGL\n", DGL)
# exit()

import plotly.graph_objects as go
fig = go.Figure()
# fig.add_trace(go.Scatter(x = MSCI_World_EUR.index, y = MSCI_World_EUR['Adj Close'], name = 'MSCI_World_EUR'))
fig.add_trace(go.Scatter(x = VTI.index, y = VTI['Adj Close'], name = 'VTI'))
fig.add_trace(go.Scatter(x = SPTL.index, y = SPTL['Adj Close'], name = 'SPTL'))
fig.add_trace(go.Scatter(x = IEF.index, y = IEF['Adj Close'], name = 'IEF'))
fig.add_trace(go.Scatter(x = SPIP.index, y = SPIP['Adj Close'], name = 'SPIP'))
fig.add_trace(go.Scatter(x = DGL.index, y = DGL['Adj Close'], name = 'DGL'))
fig.update_layout(title="ALL WEATHER PORTFOLIO")
fig.show()

exit()
