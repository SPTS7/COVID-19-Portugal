#%%
# imports
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
import matplotlib.dates as mdates

#%%
# Functions


def generate_data(df):  # generate dataframes from csv file
    return df["Dia Ano"], df["Suspeitos"], df["Confirmados"]


def fitlogistic(x, y, dias):  # fit a logistic function
    model = StepModel(form="logistic")
    # parameters to fit guesses by lmfit
    parameters = model.guess(y, x=x)
    output = model.fit(y, parameters, x=x)
    amplitude = output.params["amplitude"].value
    amplitude = math.floor(amplitude)
    center = output.params["center"].value
    sigma = output.params["sigma"].value
    fit = []
    xfit = []
    cumulative = []
    for i in range(61, dias):
        if i == 61:
            xfit.append(i)
            alpha = (i - center) / sigma
            value = amplitude * (1 - (1 / (1 + math.exp(alpha))))
            fit.append(value)
            cumulative.append(0)
        else:
            xfit.append(i)
            alpha = (i - center) / sigma
            value = amplitude * (1 - (1 / (1 + math.exp(alpha))))
            fit.append(value)
            c = value - fit[i - 62]
            cumulative.append(c)
    return amplitude, center, sigma, xfit, fit, cumulative, output.fit_report()


def convertdateconf(centerc):  # convert date for confirmed cases
    diac = centerc - 70 + centerc
    diamaxc = datetime.datetime(2020, 1, 1) + datetime.timedelta(diac - 1)
    return diac, diamaxc


def convertdatesusp(centers):  # convert date for suspected cases
    dias = centers - 63 + centers
    diamaxs = datetime.datetime(2020, 1, 1) + datetime.timedelta(dias - 1)
    return dias, diamaxs


def datas(x):
    date = []
    data = []
    for n in x:
        a = datetime.datetime(2020, 1, 1) + datetime.timedelta(n - 1)
        date.append(a)
        data.append(a.strftime("%d/%m/%Y"))
    return date, data


def plot(  # plot all the data
    x,
    xconf,
    xsusp,
    date,
    yconfirmados,
    outputconf,
    cumconf,
    ysuspeitos,
    outputsusp,
    Diamaxconf,
    amplitudeconf,
):
    fig = plt.figure()
    fig.suptitle("Casos de COVID-19 em portugal", fontsize=14, fontweight="bold")

    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    # ax3 = fig.add_subplot(313)
    fig.subplots_adjust(top=0.80)
    ax1.set_title(
        "Ajustes logísticos"
        + "\n"
        + "Confirmados: máximo a "
        + str(Diamaxconf.strftime("%d/%m/%Y"))
        + " com "
        + str(amplitudeconf)
        + " casos."
    )

    # ax1.set_ylabel("Casos")
    ax1.plot(x, yconfirmados, "ro", label="Casos confirmados")
    ax1.plot(xconf, outputconf, label="Fit Logístico")
    ax1.xaxis.set_visible(False)
    ax1.legend()

    ax2.set_ylabel("Casos")
    ax2.bar(date, cumconf, width=0.8, label="Cumulativo", color="g")
    ax2.legend()

    # ax3.set_xlabel("Dia do ano")
    # ax3.set_ylabel("Casos")
    # ax3.plot(x, ysuspeitos, "mo", label="Casos suspeitos")
    # ax3.plot(date, outputsusp, label="Fit Logístico")
    # ax3.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=4))
    plt.gcf().autofmt_xdate()
    plt.savefig("prediction.pdf")
    plt.savefig("prediction.png")
    plt.show()


def export(x, out, cumu, dias, data):

    file = open("Previsoes.csv", "w")
    file.write("Dia do ano, Data ,Fit_Logistico_Confirmados,Cumulativo" + "\n")
    for i in range(61, dias):
        line = (
            str(i)
            + ","
            + str(data[i - 61])
            + ","
            + str(out[i - 61])
            + ","
            + str(cumu[i - 61])
        )
        file.write(line + "\n")

    file.close()


def predictions(df, dias):  # make everything
    x, ysuspeitos, yconfirmados = generate_data(df)
    (
        amplitudeconf,
        centerconf,
        sigmaconf,
        xconf,
        outputconf,
        cumconf,
        outputconfreport,
    ) = fitlogistic(x, yconfirmados, dias)
    (
        amplitudesusp,
        centersusp,
        sigmasusp,
        xsusp,
        outputsusp,
        cumsusp,
        outputsuspreport,
    ) = fitlogistic(x, ysuspeitos, dias)
    Diaconf, Diamaxconf = convertdateconf(centerconf)
    Diasusp, Diamaxsusp = convertdatesusp(centersusp)
    dateplot, dateexport = datas(xconf)
    plot(
        x,
        xconf,
        xsusp,
        dateplot,
        yconfirmados,
        outputconf,
        cumconf,
        ysuspeitos,
        outputsusp,
        Diamaxconf,
        amplitudeconf,
    )
    export(xconf, outputconf, cumconf, dias, dateexport)


#%%
# Running
if __name__ == "__main__":
    df = pd.read_excel(r"D:\PC\Desktop\Corona\coronadata.xlsx")
    diasdeprevisao = 50  # previsão para quantos dias?
    dias = 61 + diasdeprevisao
    predictions(df, dias)


# %%
