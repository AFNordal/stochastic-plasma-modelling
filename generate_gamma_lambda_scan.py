import fit_analysis as analysis
import generate_series as datagen
import storage
import numpy as np


t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5

dir = "/hdd1/rno040/new_experiments/10x10/"

for gamma in np.round(np.logspace(-1, 1, 11), 2):
    for lmbda in np.round(np.linspace(0, 0.5, 11), 2):
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

        # generate and save series and analysis
        times, series = datagen.generate_data(parameters)
        storage.save_series(times, series, dir, parameters)
        ca_data = analysis.ca_analysis(times, series, parameters)
        storage.save_ca_data(ca_data, dir, parameters)
