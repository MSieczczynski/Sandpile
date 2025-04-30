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
from matplotlib.scale import ScaleBase
from matplotlib.transforms import Transform
from matplotlib import scale as mscale
from matplotlib import ticker



def log_func(x, a, b):
    return b - a / np.log(x) 

def log_func2(x,a,b):
    return b - a * np.log(x)

class InvertedLnTransform(Transform):
    input_dims = output_dims = 1
    is_separable = True

    def transform_non_affine(self, x):
        x = np.array(x)
        return 1 / np.log(x)

    def inverted(self):
        return LnInverseTransform()

class LnInverseTransform(Transform):
    input_dims = output_dims = 1
    is_separable = True

    def transform_non_affine(self, x):
        x = np.array(x)
        return np.exp(1 / x)

    def inverted(self):
        return InvertedLnTransform()

class InvLnScale(ScaleBase):
    name = 'invln'

    def __init__(self, axis, **kwargs):
        super().__init__(axis)

    def get_transform(self):
        return InvertedLnTransform()

    def set_default_locators_and_formatters(self, axis):
        invln_ticks = np.linspace(0.0, 0.26, 8) 
        x_ticks = np.exp(1 / invln_ticks)  
        axis.set_major_locator(ticker.FixedLocator(x_ticks))
        axis.set_major_formatter(ticker.FixedFormatter([f"{tick:.2f}" for tick in invln_ticks]))

    def limit_range_for_scale(self, vmin, vmax, minpos):
        return max(vmin, 1.01), vmax


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
        baselog = 2
        bin_end = 4
        bin_front = 0
        min_bin = 0
        max_bin = int(np.ceil(np.log(max(dane)) / np.log(baselog)))

        # Obliczenie nieregularnych krawędzi binów
        bin_edges = [baselog**i for i in range(min_bin, max_bin)] 

        hist_values, bins = np.histogram(dane, bins=bin_edges, density=True)

        # Obliczanie środków binów
        bin_centers = 0.5 * (bins[:-1] + bins[1:])

        hist_values = np.array(hist_values[bin_front:-bin_end])
        bin_centers = np.array(bin_centers[bin_front:-bin_end]) 


        mask = hist_values > 0
        x_log = np.log(bin_centers[mask]) / np.log(baselog)
        y_log = np.log(hist_values[mask]) / np.log(baselog)

        # Dopasowanie prostej do histogramu
        slope, intercept, *_ = linregress(x_log, y_log)

        alfa.append(-slope)


    params1, covariance1 = curve_fit(log_func, size, alfa)

    x_fit = np.linspace(min(size), max(size), 100)
    y_fit = log_func(x_fit, *params1)


    plt.scatter(size, alfa, color='red', label='log-log alfa')
    plt.plot(x_fit, y_fit, color='blue', label='Dopasowanie log')
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

    # ------------- Wykres lnx -------------
    params, covariance  = curve_fit(log_func2,size, alfa)
    x_fit = np.linspace(min(size), max(size), 100)
    y_fit = log_func2(x_fit, *params)
    print(params)
    plt.scatter(size, alfa, color='red', label='log-log alfa')
    plt.plot(x_fit, y_fit, color='blue', label='Dopasowanie log')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Rozmiar siatki')
    plt.ylabel('Alfa')
    plt.title('Histogram log-log ')
    plt.savefig('SandpileAlfa_Ln.png', dpi=300, bbox_inches='tight')
    # ------------- // -------------

    # ------------- Wykres 1/lnx -------------
    # params, covariance  = curve_fit(log_func,size, alfa)
    # print(params)
    # x_fit = np.linspace(min(size), max(size), 100)
    # maxlog = np.float64(10**300)
    # x_fit = np.append(x_fit, maxlog)
    # y_fit = log_func(x_fit, *params)
    # #alfa.append(params[1])
    # #size.append(maxlog)
    # mscale.register_scale(InvLnScale)
    # plt.scatter(size, alfa, color='red', label='alfa')
    # plt.plot(x_fit, y_fit, color='blue', label='Dopasowanie 1/lnx')
    # plt.legend()
    # plt.xscale('invln')
    # plt.xlabel('Rozmiar siatki 1/lnL')
    # plt.xlim(40,maxlog)
    # plt.ylim(1,1.4)
    # plt.ylabel('Alfa')
    # plt.title('Histogram alfa')
    # plt.savefig('SandpileAlfa_uLn.png', dpi=300, bbox_inches='tight')
    # ------------- // -------------

alfaread()