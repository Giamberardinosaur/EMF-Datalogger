import folium
import pandas as pd
import numpy as np
import branca.colormap as cmp
import matplotlib.pyplot as plt
import os

def loadFiles(files):
    data = pd.read_csv(files[0])
    for file in files[1:]:
        data = data.append(pd.read_csv(file))

    data["Datetime"] = pd.to_datetime(data["Datetime"])

    return data

def save(data, desc):
    timeString= data.iloc[0, 0].strftime("%Y-%m-%dT%H%M")
    filename = "./SortedData/{}-{}.csv".format(desc, timeString)

    data.to_csv(filename, index=False)
    return filename

def findFiles(date, dir):
    files = os.listdir(dir)
    validFiles = []

    for f in files:
        if date in f:
            validFiles.append(dir+'/'+f)

    return validFiles

def plotGaussHist(histData, filename=None):
    col="Gauss Total [mG]"
    mu = histData[col].mean()
    median = histData[col].median()
    sigma = histData[col].std()
    maxVal = histData[col].max()
    textstr = '\n'.join((
        r'$\mu=%.2f$ mG' % (mu, ),
        r'$\mathrm{median}=%.2f$ mG' % (median, ),
        r'$\sigma=%.2f$ mG' % (sigma, ),
        r'$\mathrm{max}=%.2f$ mG' % (maxVal, )))


    fig, ax = plt.subplots(figsize=(12, 8), dpi=80)
    ax.hist(histData[col], bins=40, color='xkcd:periwinkle')
    ax.set_xlabel("Gauss Reading [mG]")
    ax.set_ylabel("Count")

    props = dict(facecolor='w', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props, multialignment='right')

    if filename is not None:
        fig.savefig(filename)
        plt.show()

def plotRFHist(histData, filename=None):
    col="RF [μW/m²]"
    mu = histData[col].mean()
    median = histData[col].median()
    sigma = histData[col].std()
    maxVal = histData[col].max()
    textstr = '\n'.join((
        r'$\mu=%.2f$ μW/m²' % (mu, ),
        r'$\mathrm{median}=%.2f$ μW/m²' % (median, ),
        r'$\sigma=%.2f$ μW/m²' % (sigma, ),
        r'$\mathrm{max}=%.2f$ μW/m²' % (maxVal, )))


    fig, ax = plt.subplots(figsize=(12, 8), dpi=80)
    ax.hist(histData[col], bins=40, color='xkcd:light red')
    ax.set_xlabel("RF Strength [μW/m²]")
    ax.set_ylabel("Count")

    props = dict(facecolor='w', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props, multialignment='right')

    if filename is not None:
        fig.savefig(filename)
        plt.show()


dir = "./logs"     # Directory to search for logfiles

day = '2021-07-30' # Day to search for YYYY-DD-MM format
start = '12:57'    # Start time to slice - 24H MM:HH format
end = '13:13'      # End time

# Filename to save CSV files and graphs with
desc = "PrincessBagotPylonhetr"

files = findFiles(day, dir)
data = loadFiles(files)

t1 = np.datetime64(day+'T'+start)
t2 = np.datetime64(day+'T'+end)
slicedData = data[(data['Datetime'] > t1) & (data['Datetime'] < t2)]
print("{} datapoints found".format(slicedData["Datetime"].size))

filename = save(slicedData, desc)
print("Saved to {}".format(filename))

# Save a histogram of the gauss meter data
plotGaussHist(slicedData, filename[:-4] + ".png") 

# Save a histogram of the rf meter data
plotRFHist(slicedData, filename[:-4] + "-RF.png")


