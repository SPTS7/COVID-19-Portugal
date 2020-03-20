#%%

import math, scipy, pylab
import glob, os
import matplotlib.pyplot as plt
import re, operator
import time
from lmfit.models import StepModel, Model
from tqdm import tqdm
import numpy as np
from numpy import loadtxt
import pandas as pd
import datetime

#%%
# import data

df = pd.read_excel(r"D:\PC\Desktop\Corona\coronadata.xlsx")
# print(df)
x = df["Dia Ano"]
ysuspeitos = df["Suspeitos"]
yconfirmados = df["Confirmados"]

#%%
# fit data to confirmed cases
coronaconf = StepModel(form="logistic")
# parameters to fit guesses by lmfit
parameters = coronaconf.guess(yconfirmados, x=x)

outputconf = coronaconf.fit(yconfirmados, parameters, x=x)
# print(outputconf.fit_report())

amplitudeconf = outputconf.params["amplitude"].value
amplitudeconf = math.floor(amplitudeconf)
centerconf = outputconf.params["center"].value

# -------------------------------------------------------------------
# fit data to suspect cases
coronasusp = StepModel(form="logistic")
# parameters to fit guesses by lmfit
param = coronasusp.guess(ysuspeitos, x=x)

outputsusp = coronasusp.fit(ysuspeitos, param, x=x)
# print(outputsusp.fit_report())

amplitudesusp = outputsusp.params["amplitude"].value
centersusp = outputsusp.params["center"].value


#%%
# Conversão dos dias e datas
Diaconf = centerconf - 72 + centerconf
Diasusp = centersusp - 67 + centersusp
Diamaxconf = datetime.datetime(2020, 1, 1) + datetime.timedelta(Diaconf - 1)
Diamaxsusp = datetime.datetime(2020, 1, 1) + datetime.timedelta(Diasusp - 1)

#%%
# Previsão de 1/3. 1/3 entre os suspeitos e os confirmados

a = amplitudesusp - amplitudeconf
b = a / 3
pred = amplitudeconf + b
pred = math.floor(pred)

aa = Diasusp - Diaconf
bb = aa / 3
predia = Diaconf + bb
Diamaxpre = datetime.datetime(2020, 1, 1) + datetime.timedelta(predia - 1)

#%%
# figures
fig = plt.figure()
fig.suptitle("Casos de COVID-19 em portugal", fontsize=14, fontweight="bold")
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.85)


ax.set_xlabel("Dia do ano")
ax.set_ylabel("Casos")
ax.text(
    60.2,
    6700,
    r"Pelo fit dos dados o numero máximo de infectados "
    + "\n"
    + "será atingido no dia "
    + str(Diamaxconf.strftime("%d/%m/%Y"))
    + " em que se esperam "
    + "\n"
    + str(amplitudeconf)
    + " casos.",
    fontsize=10,
)

ax.text(
    60.2,
    4500,
    r"Fazendo uma previsão (adicionando 1/3 da diferença"
    + "\n"
    + "entre os suspeitos e confirmados) com base nos dados"
    + "\n"
    + "o numero máximo de infectados será atingido no dia "
    + "\n"
    + str(Diamaxpre.strftime("%d/%m/%Y"))
    + " em que se esperam "
    + str(pred)
    + " casos.",
    fontsize=10,
)

ax.plot(x, yconfirmados, "ro", label="Casos confirmados")
ax.plot(x, outputconf.best_fit, label="Fit casos confirmados")
ax.plot(x, ysuspeitos, "bo", label="Casos suspeitos")
ax.plot(x, outputsusp.best_fit, label="Fit casos suspeitos")
ax.legend(loc="center left", bbox_to_anchor=(0.02, 0.3))
plt.show()
# %%
