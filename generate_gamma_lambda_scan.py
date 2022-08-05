import double_exp_ca_analysis as analysis
import generate_series as datagen
import storage
import numpy as np


t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5

dir = "experiment/10x10/"

for gamma in np.round(np.logspace(-1, 1, 11), 2):
    for lmbda in np.round(np.linspace(0.1, 0.5, 9), 2):
        parameters = {
            "gamma": gamma,
            "lmbda": lmbda,
            "t": t,
            "dt": dt,
            "delta": delta,
            "window": window,
            "normalize_amplitude": normalize_amplitude,
            "thresh": thresh
        }
        print(gamma, lmbda)

        times, series = datagen.generate_data(parameters)
        ca_data = analysis.ca_analysis(times, series, parameters)
        storage.save_ca_data(ca_data, dir, parameters)
        storage.save_series(times, series, dir, parameters)
