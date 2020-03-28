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
    return df["Dia Ano"], df["Suspeitos"], df["Confirmados"], len(df)


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


def fitGompertz(x, y, dias):  # fit a logistic function~
    def Gompertz(a, b, c, x):
        return a * np.exp(-1 * np.exp(-b * (x - c)))

    model = Model(Gompertz, independent_vars=["x"])

    params = model.make_params()
    params["a"].value = 10000
    params["b"].value = 0.05
    params["c"].value = 100
    output = model.fit(y, params, x=x)
    amplitude = output.params["a"].value
    amplitude = math.floor(amplitude)
    center = output.params["c"].value
    sigma = output.params["b"].value
    fit = []
    xfit = []
    cumulative = []
    for i in range(61, dias):
        if i == 61:
            xfit.append(i)
            value = amplitude * np.exp(-1 * np.exp(-sigma * (i - center)))
            fit.append(value)
            cumulative.append(0)
        else:
            xfit.append(i)
            value = amplitude * np.exp(-1 * np.exp(-sigma * (i - center)))
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
    date,
    yconfirmados,
    outputconf,
    erfoutputconf,
    cumconf,
    erfcumconf,
    ysuspeitos,
    Diamaxconf,
    amplitudeconf,
):
    fig = plt.figure(1)
    fig.suptitle("Casos de COVID-19 em portugal", fontsize=14, fontweight="bold")

    ax1 = fig.add_subplot(411)
    ax2 = fig.add_subplot(412)
    ax3 = fig.add_subplot(413)
    ax4 = fig.add_subplot(414)

    fig.subplots_adjust(top=0.80)

    ax1.set_title(
        "Ajustes logístico e de Gompertz"
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
    ax1.set_ylim(-5, 15000)
    ax1.legend()

    ax2.set_ylabel("Casos")
    ax2.bar(date, cumconf, width=0.8, label="Casos novos", color="g")
    ax2.xaxis.set_visible(False)
    ax2.legend()

    ax3.plot(x, yconfirmados, "mo", label="Casos confirmados")
    ax3.plot(xconf, erfoutputconf, label="Fit Gompertz")
    ax3.xaxis.set_visible(False)
    # ax3.set_ylim(-5, 10000)
    ax3.legend()

    ax4.set_ylabel("Casos")
    bars = ax4.bar(date, erfcumconf, width=0.8, label="Gompertz Casos novos", color="g")
    ax4.legend()

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
    plt.gcf().autofmt_xdate()
    plt.savefig("prediction.pdf")
    plt.savefig("prediction.png")
    plt.show()


def export(x, out, erfout, cumu, erfcumu, dias, data, diaspassados, yconfirmados):

    file = open("Previsoes.csv", "w")
    file.write(
        "Dia do ano, Data, Dados_dgs, Fit_Logistico_Confirmados,Novos_Casos,Fit_Gompertz_Confirmados,Gompertz_Novos_casos"
        + "\n"
    )
    for i in range(61, dias):
        if i - 61 < diaspassados:
            line = (
                str(i)
                + ","
                + str(data[i - 61])
                + ","
                + str(yconfirmados.loc[i - 61])
                + ","
                + str(out[i - 61])
                + ","
                + str(cumu[i - 61])
                + ","
                + str(erfout[i - 61])
                + ","
                + str(erfcumu[i - 61])
            )
            file.write(line + "\n")
        else:
            line = (
                str(i)
                + ","
                + str(data[i - 61])
                + ","
                + ","
                + str(out[i - 61])
                + ","
                + str(cumu[i - 61])
                + ","
                + str(erfout[i - 61])
                + ","
                + str(erfcumu[i - 61])
            )
            file.write(line + "\n")

    file.close()


def predictions(df, dias):  # make everything
    x, ysuspeitos, yconfirmados, diaspassado = generate_data(df)
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
        erfamplitudeconf,
        erfcenterconf,
        erfsigmaconf,
        erfxconf,
        erfoutputconf,
        erfcumconf,
        erfoutputconfreport,
    ) = fitGompertz(x, yconfirmados, dias)
    Diaconf, Diamaxconf = convertdateconf(centerconf)
    dateplot, dateexport = datas(xconf)
    plot(
        x,
        xconf,
        dateplot,
        yconfirmados,
        outputconf,
        erfoutputconf,
        cumconf,
        erfcumconf,
        ysuspeitos,
        Diamaxconf,
        amplitudeconf,
    )
    export(
        xconf,
        outputconf,
        erfoutputconf,
        cumconf,
        erfcumconf,
        dias,
        dateexport,
        diaspassado,
        yconfirmados,
    )


#%%
# Running
if __name__ == "__main__":
    df = pd.read_excel(r"D:\PC\Desktop\Corona\coronadata.xlsx")
    diasdeprevisao = 50  # previsão para quantos dias?
    dias = 61 + diasdeprevisao
    predictions(df, dias)


# %%
