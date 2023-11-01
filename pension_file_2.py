import pandas as pd
import numpy as np
import yfinance as yf
import random
from matplotlib import pyplot as plt
plt.style.use("seaborn")
import seaborn

# ============================================
# ANALISI RENDITA PER DECUMULO DI INVESTIMENTI
# UTILE PER PROGETTI FIRE RETIREMENT
# SI TIENE CONTO DELL'INFLAZIONE:
#   - "inflazione fissa": l'inflazione è sempre uguale a inflazione_media
#   - "inflazione reale": l'inflazione è quella italiana basata su dati reali dal 1954 al 2022, estratta casualmente
#   - "inflazione reale riscalata": come sopra, ma viene riscalata in modo che la sua media (solitamente sopra al 5%) sia pari a inflazione_media
#   - "inflazione lognormale": l'inflazione è presa da una distribuzione lognormale con media inflazione_media e sigma la deviazione standard dell'inflazione reale (circa 0.53)
# ============================================

giorni_anno = 253
df = yf.download("^SP500TR")["Adj Close"].pct_change(giorni_anno).dropna()

df.plot()

primo_estratto = random.randint(0, len(df) - 3*giorni_anno - 1)
secondo_estratto = primo_estratto + giorni_anno
terzo_estratto = secondo_estratto + giorni_anno
print(df.index[primo_estratto], "->", round(df[primo_estratto]*100), "%")
print(df.index[secondo_estratto], "->", round(df[secondo_estratto]*100), "%")
print(df.index[terzo_estratto], "->", round(df[terzo_estratto]*100), "%")

quante_simulazioni = 100
upper = len(df) - 3 * giorni_anno - 1
m = np.zeros((100, quante_simulazioni))
# print(m)
m[0, :] = 1
# print(m)
for c in range(quante_simulazioni):
    for t in range(1, 100, 3):
        e1 = random.randint(0, upper)
        e2 = e1 + giorni_anno
        e3 = e2 + giorni_anno
        # print(t, t + 1, t + 2, c)
        m[t, c] = m[t - 1, c] * (1 + df[e1])
        m[t + 1, c] = m[t, c] * (1 + df[e2])
        m[t + 2, c] = m[t + 1, c] * (1 + df[e3])
# print(m)

pd.DataFrame(m).plot(legend=None, logy=True, fontsize=16, figsize=(25,15))

quante_simulazioni = 10000
upper = len(df) - 3 * giorni_anno-1
md = np.zeros((100,quante_simulazioni))
md[0,:] = 1
m = np.zeros((100, quante_simulazioni))
m[0,:] = 1
for c in range(quante_simulazioni):
    for t in range(1, 100, 3):
        e1 = random.randint(0, upper)
        e2 = e1 + giorni_anno
        e3 = e2 + giorni_anno
        # print(t,c)
        md[t,c] = 1 + df[e1]
        md[t+1,c] = 1 + df[e2]
        md[t+2,c] = 1 + df[e3]
        m[t,c] = m[t-1,c]*(1 + df[e1])
        m[t+1,c] = m[t,c]*(1 + df[e2])
        m[t+2,c] = m[t+1,c]*(1 + df[e3])
        
# Iniziamo finalmente l'analisi
capitale = 500000
percentuale_carico = 1.0 # percentuale che il capitale è costato
capitale_carico = percentuale_carico * capitale
prelievo = 2000 * 13
# possibili stime dell'inflazione:  "fissa", "reale", "reale riscalata", "lognormale"
inflazione_stima = "fissa"
inflazione_media = 0.03
# valori possibili sono 
# "fissa": l'inflazione è sempre uguale a inflazione_media
# "reale": l'inflazione è quella italiana basata su dati reali dal 1954 al 2022, estratta casualmente
# "reale riscalata": come sopra, ma viene riscalata in modo che la sua media (solitamente sopra al 5%) sia pari a inflazione_media
# "lognormale": l'inflazione è presa da una distribuzione lognormale con media inflazione_media e sigma la deviazione standard dell'inflazione reale (circa 0.53)
bollo = 0.002
aliquota = 0.26
anni_rendita = 51 # per quanti anni resti in pensione, massimo 99!
anni_buffer = 3 # numero di anni di buffer da usare per tasse e periodi di rendimenti negativi, MAI MENO DI 1

# sistemiamo l'inflazione
inflazione_reale = np.array([2.3,3.4,1.3,2.8,-0.4,2.3,2.1,4.7,7.5,5.9,4.6,2.3,3.7,1.4,2.6,5.0,4.8,5.7,10.8,19.1,17.0,16.8,17.0,12.1,14.8,21.2,17.8,16.5,14.7,10.8,9.2,5.8,4.8,5.0,6.3,6.5,6.2,5.3,4.7,4.1,5.3,4.0,2.0,2.0,1.7,2.5,2.7,2.5,2.7,2.2,1.9,2.1,1.8,3.3,0.8,1.5,2.7,3.0,1.2,0.2,0.1,-0.1,1.2,1.2,0.6,-0.2,1.9,8.1,8.7])/100
if inflazione_stima=="fissa":
    inflazione=np.ones((100,quante_simulazioni))*inflazione_media 
elif inflazione_stima=="reale":
    inflazione=inflazione_reale[np.random.randint(0,len(inflazione_reale),(100,quante_simulazioni))]
elif inflazione_stima=="reale riscalata":
    inflazione=inflazione=(inflazione_reale*(inflazione_media/inflazione_reale.mean()))[np.random.randint(0,len(inflazione_reale),(100,quante_simulazioni))]
elif inflazione_stima=="lognormale":
    mu=np.log(inflazione_media)
    sigma=np.log((1+np.sqrt(1+4*inflazione_reale.var()/np.exp(2*mu)))/2)
    mu=np.log(inflazione_media)-sigma**2/2
    sigma=np.log((1+np.sqrt(1+4*inflazione_reale.var()/np.exp(2*mu)))/2)
    mu=np.log(inflazione_media)-sigma**2/2
    inflazione=np.random.lognormal(mean=mu,sigma=sigma,size=(100,quante_simulazioni))
else:
    print("Ciccio, guarda che non so come gestire l'inflazione!")
    inflazione=np.array[inflazione_media,inflazione_media,inflazione_media]    
print("Media:",inflazione.mean(),"Dev st:",inflazione.std())

prelievi = np.zeros( (100,quante_simulazioni) )
prelievi[0,:] = prelievo
for t in range(1,100):
    prelievi[t,:] = prelievi[t-1,:] * ( 1 + inflazione[t,:] )

buffer = np.zeros( (100,quante_simulazioni) )
fire = np.zeros( (100,quante_simulazioni) )
capitale_carico = np.ones( (quante_simulazioni) )* percentuale_carico * capitale 

# iniziamo
t=0
fire[0,:] = capitale
# sistemazione buffer obbligatoria all'inizio
new_buffer = np.minimum(fire[t,:]+buffer[t,:],prelievi[t,:] * anni_buffer)
prendo = np.maximum(0,new_buffer - buffer[t,:])
tassa = np.where(fire[t,:]*prendo>0, prendo * ( 1 - capitale_carico / fire[t,:] ) * aliquota,0)
capitale_carico = np.where(tassa==0,capitale_carico,capitale_carico*(1-prendo/fire[t,:]) )
fire[t,:] = fire[t,:] - prendo
buffer[t,:] = buffer[t,:]+prendo - tassa
# sistemo il buffer anche se non ho più soldi nel buffer per pagare i prelievi (al primo anno succede solo se avete messo anni_buffer<=1)
new_buffer = np.minimum(fire[t,:]+buffer[t,:],np.maximum(buffer[t,:],prelievi[t,:]))
prendo = np.maximum(0,new_buffer - buffer[t,:])
tassa = np.where(fire[t,:]*prendo>0, prendo * ( 1 - capitale_carico / fire[t,:] ) * aliquota,0)
capitale_carico = np.where(tassa==0,capitale_carico,capitale_carico*(1-prendo/fire[t,:]) )
fire[t,:] = fire[t,:] - prendo
buffer[t,:] = buffer[t,:]+prendo - tassa
# faccio il primo prelievo
buffer[t,:] = buffer[t,:] - prelievi[t,:]

fire[t,:] = np.where(fire[t,:]<prelievi[t,:]*1e-6,0,fire[t,:]) # per evitare errori di arrotondamento che non mi mandano fire a 0
for t in range(1,100):
    # finisce l'anno precedente e ho incremento di valore 
    fire[t,:] = fire[t-1,:] * md[t,:]
    buffer[t,:] = buffer[t,:] * ( 1 + inflazione[t,:] )
    # e pago il bollo
    buffer[t,:] = buffer[t-1,:] - (fire[t,:]+buffer[t-1,:]) * bollo
    # sistemo il buffer solo se sono cresciuto rispetto all'anno scorso
    new_buffer = np.where(m[t,:] > m[t-1,:], np.minimum(fire[t,:]+buffer[t,:],prelievi[t,:] * anni_buffer) , buffer[t,:])
    prendo = np.maximum(0,new_buffer - buffer[t,:])
    tassa = np.where(fire[t,:]*prendo>0, prendo * ( 1 - capitale_carico / fire[t,:] ) * aliquota,0)
    capitale_carico = np.where(tassa==0,capitale_carico,capitale_carico*(1-prendo/fire[t,:]) )
    fire[t,:] = fire[t,:] - prendo
    buffer[t,:] = buffer[t,:]+prendo - tassa
    # sistemo il buffer anche se non ho più soldi nel buffer per pagare i prelievi
    new_buffer = np.minimum(fire[t,:]+buffer[t,:],np.maximum(buffer[t,:],prelievi[t,:]))
    prendo = np.maximum(0,new_buffer - buffer[t,:])
    tassa = np.where(fire[t,:]*prendo>0, prendo * ( 1 - capitale_carico / fire[t,:] ) * aliquota,0)
    capitale_carico = np.where(tassa==0,capitale_carico,capitale_carico*(1-prendo/fire[t,:]) )
    fire[t,:] = fire[t,:] - prendo
    buffer[t,:] = buffer[t,:]+prendo - tassa
    # faccio il prelievo
    buffer[t,:] = buffer[t,:] - prelievi[t,:]
    fire[t,:] = np.where(fire[t,:]<prelievi[t,:]*1e-6,0,fire[t,:]) # per evitare errori di arrotondamento che non mi mandano fire a 0
    
  print(prelievi)
  
  print(fire)
  
  print(buffer)
  
  pd.Series((fire[anni_rendita,:]+buffer[anni_rendita,:])>0).value_counts()/quante_simulazioni*100
  
  # Proviamo tutti i possibili capitali iniziali
summaryTable=pd.DataFrame(np.zeros((50,20)),columns=list(range(100000,2000001,100000)),index=list(range(1,51)))
prelievi = np.zeros( (100,quante_simulazioni) )
prelievi[0,:] = prelievo
for t in range(1,100):
    prelievi[t,:] = prelievi[t-1,:] * ( 1 + inflazione[t,:] )

for capitale in range(100000,2000001,100000):
    buffer = np.zeros( (100,quante_simulazioni) )
    fire = np.zeros( (100,quante_simulazioni) )
    capitale_carico = np.ones( (quante_simulazioni) )* percentuale_carico * capitale 

    # iniziamo
    t=0
    fire[0,:] = capitale
    # sistemazione buffer obbligatoria all'inizio
    new_buffer = np.minimum(fire[t,:]+buffer[t,:],prelievi[t,:] * anni_buffer)
    prendo = np.maximum(0,new_buffer - buffer[t,:])
    tassa = np.where(fire[t,:]*prendo>0, prendo * ( 1 - capitale_carico / fire[t,:] ) * aliquota,0)
    capitale_carico = np.where(tassa==0,capitale_carico,capitale_carico*(1-prendo/fire[t,:]) )
    fire[t,:] = fire[t,:] - prendo
    buffer[t,:] = buffer[t,:]+prendo - tassa
    # sistemo il buffer anche se non ho più soldi nel buffer per pagare i prelievi (al primo anno succede solo se avete messo anni_buffer<=1)
    new_buffer = np.minimum(fire[t,:]+buffer[t,:],np.maximum(buffer[t,:],prelievi[t,:]))
    prendo = np.maximum(0,new_buffer - buffer[t,:])
    tassa = np.where(fire[t,:]*prendo>0, prendo * ( 1 - capitale_carico / fire[t,:] ) * aliquota,0)
    capitale_carico = np.where(tassa==0,capitale_carico,capitale_carico*(1-prendo/fire[t,:]) )
    fire[t,:] = fire[t,:] - prendo
    buffer[t,:] = buffer[t,:]+prendo - tassa
    # faccio il primo prelievo
    buffer[t,:] = buffer[t,:] - prelievi[t,:]

    fire[t,:] = np.where(fire[t,:]<prelievi[t,:]*1e-6,0,fire[t,:]) # per evitare errori di arrotondamento che non mi mandano fire a 0
    for t in range(1,100):
        # finisce l'anno precedente e ho incremento di valore 
        fire[t,:] = fire[t-1,:] * md[t,:]
        buffer[t,:] = buffer[t,:] * ( 1 + inflazione[t,:] )
        # e pago il bollo
        buffer[t,:] = buffer[t-1,:] - fire[t,:] * bollo
        # sistemo il buffer solo se sono cresciuto rispetto all'anno scorso
        new_buffer = np.where(m[t,:] > m[t-1,:], np.minimum(fire[t,:]+buffer[t,:],prelievi[t,:] * anni_buffer) , buffer[t,:])
        prendo = np.maximum(0,new_buffer - buffer[t,:])
        tassa = np.where(fire[t,:]*prendo>0, prendo * ( 1 - capitale_carico / fire[t,:] ) * aliquota,0)
        capitale_carico = np.where(tassa==0,capitale_carico,capitale_carico*(1-prendo/fire[t,:]) )
        fire[t,:] = fire[t,:] - prendo
        buffer[t,:] = buffer[t,:]+prendo - tassa
        # sistemo il buffer anche se non ho più soldi nel buffer per pagare i prelievi
        new_buffer = np.minimum(fire[t,:]+buffer[t,:],np.maximum(buffer[t,:],prelievi[t,:]))
        prendo = np.maximum(0,new_buffer - buffer[t,:])
        tassa = np.where(fire[t,:]*prendo>0, prendo * ( 1 - capitale_carico / fire[t,:] ) * aliquota,0)
        capitale_carico = np.where(tassa==0,capitale_carico,capitale_carico*(1-prendo/fire[t,:]) )
        fire[t,:] = fire[t,:] - prendo
        buffer[t,:] = buffer[t,:]+prendo - tassa
        # faccio il prelievo
        buffer[t,:] = buffer[t,:] - prelievi[t,:]
        fire[t,:] = np.where(fire[t,:]<prelievi[t,:]*1e-6,0,fire[t,:]) # per evitare errori di arrotondamento che non mi mandano fire a 0
    
    for a in range(1,51):
        summaryTable.loc[[a],[capitale]]=round(((fire[a,:]+buffer[a,:])>=0).mean(),2)
        
plt.figure(figsize=(25,25))
seaborn.set(font_scale=1.3)
seaborn.heatmap(summaryTable,cmap="Reds", annot=True, annot_kws={"size":16})

# E inseriamo anche la pensione
capitale = 700000
percentuale_carico = 1.0 # percentuale che il capitale è costato
capitale_carico = percentuale_carico * capitale
inflazione_stima = "reale" 
inflazione_media = 0.03 
# valori possibili sono 
# "fissa": l'inflazione è sempre uguale a inflazione_media
# "reale": l'inflazione è quella italiana basata su dati reali dal 1954 al 2022, estratta casualmente
# "reale riscalata": come sopra, ma viene riscalata in modo che la sua media (solitamente sopra al 5%) sia pari a inflazione_media
# "lognormale": l'inflazione è presa da una distribuzione lognormale con media inflazione_media e sigma la deviazione standard dell'inflazione reale (circa 0.53)
bollo = 0.002
aliquota = 0.26
anni_buffer = 3 # numero di anni di buffer da usare per tasse e periodi di rendimenti negativi

prelievo = 4000 * 13
anni_rendita = 20 # la somma dei due anni_rendita massimo 99

prelievo2 = 2800 * 13
anni_rendita2 = 30 # la somma dei due anni_rendita massimo 99

summaryTable=pd.DataFrame(np.zeros((anni_rendita+anni_rendita2,20)),columns=list(range(100000,2000001,100000)),index=list(range(1,anni_rendita+anni_rendita2+1)))

prelievi = np.zeros( (100,quante_simulazioni) )
prelievi[0,:] = prelievo
coef = np.ones( (quante_simulazioni) )
for t in range(1,anni_rendita+1):
    prelievi[t,:] = prelievi[t-1,:] * ( 1 + inflazione[t,:] )
    coef = coef * ( 1 + inflazione[t,:] )

prelievi[anni_rendita+1] = prelievo2 * coef * ( 1 + inflazione[anni_rendita+1,:] )
for t in range(anni_rendita+2,100):
    prelievi[t,:] = prelievi[t-1,:] * ( 1 + inflazione[t,:] )

for capitale in range(100000,2000001,100000):
    buffer = np.zeros( (100,quante_simulazioni) )
    fire = np.zeros( (100,quante_simulazioni) )
    capitale_carico = np.ones( (quante_simulazioni) )* percentuale_carico * capitale 

    # iniziamo
    t=0
    fire[0,:] = capitale
    # sistemazione buffer obbligatoria all'inizio
    new_buffer = np.minimum(fire[t,:]+buffer[t,:],prelievi[t,:] * anni_buffer)
    prendo = np.maximum(0,new_buffer - buffer[t,:])
    tassa = np.where(fire[t,:]*prendo>0, prendo * ( 1 - capitale_carico / fire[t,:] ) * aliquota,0)
    capitale_carico = np.where(tassa==0,capitale_carico,capitale_carico*(1-prendo/fire[t,:]) )
    fire[t,:] = fire[t,:] - prendo
    buffer[t,:] = buffer[t,:]+prendo - tassa
    # sistemo il buffer anche se non ho più soldi nel buffer per pagare i prelievi (al primo anno succede solo se avete messo anni_buffer<=1)
    new_buffer = np.minimum(fire[t,:]+buffer[t,:],np.maximum(buffer[t,:],prelievi[t,:]))
    prendo = np.maximum(0,new_buffer - buffer[t,:])
    tassa = np.where(fire[t,:]*prendo>0, prendo * ( 1 - capitale_carico / fire[t,:] ) * aliquota,0)
    capitale_carico = np.where(tassa==0,capitale_carico,capitale_carico*(1-prendo/fire[t,:]) )
    fire[t,:] = fire[t,:] - prendo
    buffer[t,:] = buffer[t,:]+prendo - tassa
    # faccio il primo prelievo
    buffer[t,:] = buffer[t,:] - prelievi[t,:]

    fire[t,:] = np.where(fire[t,:]<prelievi[t,:]*1e-6,0,fire[t,:]) # per evitare errori di arrotondamento che non mi mandano fire a 0
    for t in range(1,100):
        # finisce l'anno precedente e ho incremento di valore 
        fire[t,:] = fire[t-1,:] * md[t,:]
        buffer[t,:] = buffer[t,:] * ( 1 + inflazione[t,:] )
        # e pago il bollo
        buffer[t,:] = buffer[t-1,:] - (fire[t,:]+buffer[t-1,:]) * bollo
        # sistemo il buffer solo se sono cresciuto rispetto all'anno scorso
        new_buffer = np.where(m[t,:] > m[t-1,:], np.minimum(fire[t,:]+buffer[t,:],prelievi[t,:] * anni_buffer) , buffer[t,:])
        prendo = np.maximum(0,new_buffer - buffer[t,:])
        tassa = np.where(fire[t,:]*prendo>0, prendo * ( 1 - capitale_carico / fire[t,:] ) * aliquota,0)
        capitale_carico = np.where(tassa==0,capitale_carico,capitale_carico*(1-prendo/fire[t,:]) )
        fire[t,:] = fire[t,:] - prendo
        buffer[t,:] = buffer[t,:]+prendo - tassa
        # sistemo il buffer anche se non ho più soldi nel buffer per pagare i prelievi
        new_buffer = np.minimum(fire[t,:]+buffer[t,:],np.maximum(buffer[t,:],prelievi[t,:]))
        prendo = np.maximum(0,new_buffer - buffer[t,:])
        tassa = np.where(fire[t,:]*prendo>0, prendo * ( 1 - capitale_carico / fire[t,:] ) * aliquota,0)
        capitale_carico = np.where(tassa==0,capitale_carico,capitale_carico*(1-prendo/fire[t,:]) )
        fire[t,:] = fire[t,:] - prendo
        buffer[t,:] = buffer[t,:]+prendo - tassa
        # faccio il prelievo
        buffer[t,:] = buffer[t,:] - prelievi[t,:]
        fire[t,:] = np.where(fire[t,:]<prelievi[t,:]*1e-6,0,fire[t,:]) # per evitare errori di arrotondamento che non mi mandano fire a 0
    
    for a in range(1,anni_rendita+anni_rendita2+1):
        summaryTable.loc[[a],[capitale]]=round(((fire[a,:]+buffer[a,:])>=0).mean(),2)
        
plt.figure(figsize=(25,25))
seaborn.set(font_scale=1.3)
seaborn.heatmap(summaryTable,cmap="Reds", annot=True, annot_kws={"size":16})
