import datetime
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go

start = datetime.datetime(2009, 9, 26)
end = datetime.datetime(2022, 9, 7)

# Download data for the assets using their tickers
# MSCI_World_EUR = yf.download('SWDA.MI', start=start, end=end)
VTI = yf.download('VTI', start=start, end=end)
SPTL = yf.download('SPTL', start=start, end=end)
IEF = yf.download('IEF', start=start, end=end)
SPIP = yf.download('SPIP', start=start, end=end)
DGL = yf.download('DGL', start=start, end=end)

print("\nVTI\n", VTI)

# GRAPH OF THE ASSETS IN THE "ALL WEATHER PORTFOLIO"
# NOTE: PORTFOLIO VALID FOR US INVESTORS, EUROPEAN INVESTORS SHOULD PREFER BONDS IN EUR CURRENCY
fig = go.Figure()
# fig.add_trace(go.Scatter(x = MSCI_World_EUR.index, y = MSCI_World_EUR['Adj Close'], name = 'MSCI_World_EUR'))
fig.add_trace(go.Scatter(x = VTI.index, y = VTI['Adj Close'], name = 'VTI'))
fig.add_trace(go.Scatter(x = SPTL.index, y = SPTL['Adj Close'], name = 'SPTL'))
fig.add_trace(go.Scatter(x = IEF.index, y = IEF['Adj Close'], name = 'IEF'))
fig.add_trace(go.Scatter(x = SPIP.index, y = SPIP['Adj Close'], name = 'SPIP'))
fig.add_trace(go.Scatter(x = DGL.index, y = DGL['Adj Close'], name = 'DGL'))
fig.update_layout(title="ALL WEATHER PORTFOLIO")
fig.show()

