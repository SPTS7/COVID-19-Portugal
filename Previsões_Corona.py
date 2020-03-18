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

#%%
#import data

df = pd.read_excel(r'D:\PC\Desktop\Corona\coronadata.xlsx')
#print(df)
x = df['Dia Ano']
ysuspeitos = df['Suspeitos']
yconfirmados = df['Confirmados']

#%%
# fit data to confirmed

coronaconf = StepModel(form='logistic')

parameters = coronaconf.make_params()
parameters.add('amplitude', value=15000  )#, min=10000, max=20000)
parameters.add('center', value=100)
parameters.add('sigma', value=1.10  )#, max=3)

#pars = coronaconf.guess(yconfirmados, x=x)

outputconf = coronaconf.fit(yconfirmados, parameters, x=x)
print(outputconf.fit_report())

# fit data to suspects 

coronasusp = StepModel(form='logistic')
'''
param = coronasusp.make_params()
param.add('amplitude', value=15000  )#, min=10000, max=20000)
param.add('center', value=100)
param.add('sigma', value=1.10  )#, max=3)
'''
param = coronasusp.guess(ysuspeitos, x=x)

outputsusp = coronasusp.fit(ysuspeitos, param, x=x)
print(outputsusp.fit_report())

# figures

plt.figure('Corona')
plt.subplot(1,2,1)
plt.plot(x, yconfirmados)
plt.plot(x, outputconf.best_fit)
plt.subplot(1,2,2)
plt.plot(x, ysuspeitos)
plt.plot(x, outputsusp.best_fit)
plt.show()
# %%
