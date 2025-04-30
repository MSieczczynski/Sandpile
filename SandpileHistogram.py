import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress
import os


with open('SandpileData_size106x106.txt', 'r') as plik:
    dane = [float(linia.strip()) for linia in plik if linia.strip()]

baselog = 2
bin_end = 4
bin_front = 0
min_bin = 0
dane = dane[1:]
max_bin = int(np.ceil(np.log(max(dane)) / np.log(baselog)))
# Obliczenie nieregularnych krawędzi binów
bin_edges = [baselog**i for i in range(min_bin, max_bin)] 


hist_values, bins, patches = plt.hist(dane, bins=bin_edges, edgecolor='black', density=True)

# Obliczanie środków binów
bin_centers = 0.5 * (bins[:-1] + bins[1:])

hist_values = np.array(hist_values[bin_front:-bin_end])
bin_centers = np.array(bin_centers[bin_front:-bin_end]) 


mask = hist_values > 0
x_log = np.log(bin_centers[mask]) / np.log(baselog)
y_log = np.log(hist_values[mask]) / np.log(baselog)

# Dopasowanie prostej do histogramu
slope, intercept, *_ = linregress(x_log, y_log)


# Generowanie dopasowanej prostej
x_fit = np.linspace(np.log(min(bin_centers[mask]))/np.log(baselog), np.log(max(bin_centers[mask]))/np.log(baselog), 100)
y_fit = slope * x_fit + intercept

print(slope)
# Rysowanie dopasowanej prostej na istniejącym wykresie
plt.plot(baselog**x_fit, baselog**y_fit, color='red', label=f'log-log fit: y ∝ x^{slope:.2f}')
plt.legend()
plt.xscale('log', base = baselog)
plt.yscale('log', base = baselog)
plt.xlabel('Rozmiary lawin')
plt.ylabel('Ilości lawin')
plt.title('Histogram log-log ')
plt.savefig('SandpileHist_size106x106.png', dpi=300, bbox_inches='tight')
plt.show()

