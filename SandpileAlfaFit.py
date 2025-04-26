import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress
from scipy.optimize import curve_fit
import os
import time
import glob
import re
from SandpileData import sim



def log_func(x, a, b):
    return a * np.log10(x) + b

def exp_func(x, a, b):
    return a * np.exp(b * -x)

def alfasim():
    start_time = time.time()

    start = 50
    end = 300
    N = 20
    filenames, size = sim(start,end,N)

    alfa = []

    for i in range(len(filenames)):
        with open(filenames[i], 'r') as plik:
            dane = [float(linia.strip()) for linia in plik if linia.strip()]

        dane = dane[1:]
        podstawa = 2
        bin_end = 4
        bin_front = 0
        min_bin = 0
        max_bin = int(np.ceil(np.log(max(dane)) / np.log(podstawa)))

        # Obliczenie nieregularnych krawędzi binów
        bin_edges = [podstawa**i for i in range(min_bin, max_bin)] 

        hist_values, bins = np.histogram(dane, bins=bin_edges, density=True)

        # Obliczanie środków binów
        bin_centers = 0.5 * (bins[:-1] + bins[1:])

        hist_values = np.array(hist_values[bin_front:-bin_end])
        bin_centers = np.array(bin_centers[bin_front:-bin_end]) 


        mask = hist_values > 0
        x_log = np.log(bin_centers[mask]) / np.log(podstawa)
        y_log = np.log(hist_values[mask]) / np.log(podstawa)

        # Dopasowanie prostej do histogramu
        slope, intercept, *_ = linregress(x_log, y_log)

        alfa.append(-slope)


    params1, covariance1 = curve_fit(log_func, size, alfa)

    #params2, covariance2 = curve_fit(exp_func, size, alfa)

    x_fit = np.linspace(min(size), max(size), 100)
    y_fit1 = log_func(x_fit, *params1)
    #y_fit2 = exp_func(x_fit, *params2)


    plt.scatter(size, alfa, color='red', label='log-log alfa')
    plt.plot(x_fit, y_fit1, color='blue', label='Dopasowanie log')
    #plt.plot(x_fit, y_fit2, color='green', label='Dopasowanie exp')
    plt.legend()
    #plt.xscale('log', base=10)
    #plt.yscale('log', base=10)
    plt.xlabel('Rozmiar siatki')
    plt.ylabel('Alfa')
    plt.title('Histogram log-log ')
    plt.savefig('SandpileAlfa.png', dpi=300, bbox_inches='tight')

    end_time = time.time()
    elapsed_time = end_time - start_time

    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"\nCzas działania: {minutes} min {seconds} s")


def alfaread():
    start_time = time.time()
    filelist = glob.glob("SandpileData_size*txt")
    alfa = []
    size = []

    for filename in filelist:
        match = re.search(r"size(\d+)x\d+", filename)
        if match:
            size.append(int(match.group(1)))
        with open(filename, 'r') as plik:
            dane = [float(linia.strip()) for linia in plik if linia.strip()]

        dane = dane[1:]
        podstawa = 2
        bin_end = 4
        bin_front = 0
        min_bin = 0
        max_bin = int(np.ceil(np.log(max(dane)) / np.log(podstawa)))

        # Obliczenie nieregularnych krawędzi binów
        bin_edges = [podstawa**i for i in range(min_bin, max_bin)] 

        hist_values, bins = np.histogram(dane, bins=bin_edges, density=True)

        # Obliczanie środków binów
        bin_centers = 0.5 * (bins[:-1] + bins[1:])

        hist_values = np.array(hist_values[bin_front:-bin_end])
        bin_centers = np.array(bin_centers[bin_front:-bin_end]) 


        mask = hist_values > 0
        x_log = np.log(bin_centers[mask]) / np.log(podstawa)
        y_log = np.log(hist_values[mask]) / np.log(podstawa)

        # Dopasowanie prostej do histogramu
        slope, intercept, *_ = linregress(x_log, y_log)

        alfa.append(-slope)

    params1, covariance1 = curve_fit(log_func, size, alfa)

    #params2, covariance2 = curve_fit(exp_func, size, alfa)

    x_fit = np.linspace(min(size), max(size), 100)
    y_fit1 = log_func(x_fit, *params1)
    #y_fit2 = exp_func(x_fit, *params2)
    print(params1)
    print(10**((1.22 - params1[1])/params1[0]))

    plt.scatter(size, alfa, color='red', label='log-log alfa')
    plt.plot(x_fit, y_fit1, color='blue', label='Dopasowanie log')
    #plt.plot(x_fit, y_fit2, color='green', label='Dopasowanie exp')
    plt.legend()
    plt.xscale('log', base=10)
    plt.yscale('log', base=10)
    plt.xlabel('Rozmiar siatki')
    plt.ylabel('Alfa')
    plt.title('Histogram log-log ')
    plt.savefig('SandpileAlfa.png', dpi=300, bbox_inches='tight')

    end_time = time.time()
    elapsed_time = end_time - start_time

    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"\nCzas działania: {minutes} min {seconds} s")

alfaread()