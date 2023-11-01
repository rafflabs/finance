import pandas as pd
import numpy as np
import yfinance as yf
import random
from matplotlib import pyplot as plt
plt.style.use("seaborn")
import seaborn

# ========================================================================
# Vivere di rendita con la filosofia FIRE
# Simulazione basata su investimenti nell'indice S&P500
# Da modificare per simulare un portafoglio di ETF con asset diversificati
# E' un calcolo semplificato
# Aggiornato dal file pension_fire_2.py
# ========================================================================

giorni_anno = 253
df = yf.download("^SP500TR")["Adj Close"].pct_change(giorni_anno).dropna()

primo_estratto = random.randint(0, len(df) - 3*giorni_anno - 1)
secondo_estratto = primo_estratto + giorni_anno
terzo_estratto = secondo_estratto + giorni_anno
print(df.index[primo_estratto], "->" ,round(df[primo_estratto]*100), "%")
print(df.index[secondo_estratto], "->", round(df[secondo_estratto]*100), "%")
print(df.index[terzo_estratto], "->", round(df[terzo_estratto]*100), "%")

quante_simulazioni = 100
upper = len(df) - 3*giorni_anno - 1
m = np.zeros((100, quante_simulazioni))
m[0,:] = 1
for c in range(quante_simulazioni):
    for t in range(1, 100, 3):
        e1 = random.randint(487, upper)
        e2 = e1 + giorni_anno
        e3 = e2 + giorni_anno
        # print(t,c)
        m[t, c] = m[t-1, c] * (1 + df[e1])
        m[t+1, c] = m[t, c] * (1 + df[e2])
        m[t+2, c] = m[t+1, c] * (1 + df[e3])

pd.DataFrame(m).plot(legend=None, logy=True, fontsize=16, figsize=(25, 15))

quante_simulazioni = 10000
upper = len(df) - 3*giorni_anno - 1
md = np.zeros((100, quante_simulazioni))
md[0,:] = 1
m = np.zeros((100, quante_simulazioni))
m[0,:] = 1
for c in range(quante_simulazioni):
    for t in range(1, 100, 3):
        e1 = random.randint(0, upper)
        e2 = e1 + giorni_anno
        e3 = e2 + giorni_anno
        # print(t, c)
        md[t, c] = 1 + df[e1]
        md[t+1, c] = 1 + df[e2]
        md[t+2, c] = 1 + df[e3]
        m[t, c] = m[t-1, c] * (1 + df[e1])
        m[t+1, c] = m[t, c] * (1 + df[e2])
        m[t+2, c] = m[t+1, c] * (1 + df[e3])

# HERE STARTS THE ANALYSIS

capitale = 700000
prelievo = 2000 * 13
inflazione = 0.03
anni_rendita = 51 # per quanti anni resti in pensione, massimo 99!

prelievi = np.zeros((100, ))
prelievi[0] = prelievo
for t in range(1, 100):
    prelievi[t] = prelievo * (1 + inflazione)**t

fire = np.zeros((100, quante_simulazioni))
fire[0, :] = capitale - prelievi[0]
for t in range(1, 100):
    tassa = np.zeros((quante_simulazioni, ))
    tassa = (m[t, :] > m[0, :]) * (prelievi[t] - prelievi[t] / m[t, :] * m[0, :]) * 0.26
    fire[t, :] = fire[t-1, :] * md[t, :] - prelievi[t] - tassa[:]

pd.Series(fire[anni_rendita, :] >= 0).value_counts() / quante_simulazioni * 100

summaryTable = pd.DataFrame(np.zeros((50, 20)), columns=list(range(100000, 2000001, 100000)), index=list(range(1, 51)))

for c in range(100000, 2000001, 100000):
    fire[0, :] = c
    for t in range(1, 100):
        tassa = np.zeros((quante_simulazioni, ))
        tassa = (m[t, :] > m[0, :]) * (prelievi[t] - prelievi[t] / m[t, :] * m[0, :]) * 0.26
        fire[t, :] = fire[t-1, :] * md[t, :] - prelievi[t] - tassa[:]
    
    for a in range(1, 51):
        summaryTable.loc[[a], [c]] = round((fire[a, :] >= 0).mean(), 2)

plt.figure(figsize=(25,25))
seaborn.set(font_scale=1.3)
seaborn.heatmap(summaryTable,cmap="Reds", annot=True, annot_kws={"size":16})

# E inseriamo anche la pensione

capitale = 700000
prelievo = 2000 * 13
inflazione = 0.03
anni_rendita = 20 # la somma dei due anni_rendita massimo 99
prelievo2 = 800 * 13
anni_rendita2 = 30 # la somma dei due anni_rendita massimo 99

prelievi = np.zeros((100, ))
prelievi[0] = prelievo
for t in range(1, anni_rendita):
    prelievi[t] = prelievo * (1 + inflazione)**t
for t in range(anni_rendita, 100):
    prelievi[t] = prelievo2 * (1 + inflazione)**t

fire = np.zeros((100, quante_simulazioni))
fire[0, :] = capitale
for t in range(1, 100):
    tassa = np.zeros((quante_simulazioni, ))
    tassa = (m[t,:] > m[0,:]) * (prelievi[t] - prelievi[t] /m[t, :] * m[0, :]) * 0.26
    fire[t, :] = fire[t-1, :] * md[t, :] - prelievi[t] - tassa[:]

pd.Series(fire[anni_rendita + anni_rendita2, :] >= 0).value_counts() / quante_simulazioni * 100

summaryTable = pd.DataFrame(np.zeros((50, 20)), columns=list(range(100000, 2000001, 100000)), index=list(range(1, 51)))

for c in range(100000, 2000001, 100000):
    fire[0, :] = c
    for t in range(1, 100):
        tassa = np.zeros((quante_simulazioni, ))
        tassa = (m[t, :] > m[0, :]) * (prelievi[t] - prelievi[t] / m[t, :] * m[0, :]) * 0.26
        fire[t, :] = fire[t-1, :] * md[t, :] - prelievi[t] - tassa[:]
    
    for a in range(1, 51):
        summaryTable.loc[[a], [c]] = round((fire[a, :] >= 0).mean(), 2)

plt.figure(figsize=(25, 25))
seaborn.set(font_scale=1.3)
seaborn.heatmap(summaryTable, cmap="Reds", annot=True, annot_kws={"size":16})
