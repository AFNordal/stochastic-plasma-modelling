import double_exp_ca_analysis as analysis
import generate_series as datagen
import storage
import numpy as np
from matplotlib import pyplot as plt
from os import mkdir
from tqdm import tqdm


gamma = 10
t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5


for i in range(100):
    dir = f"experiment_data/N/gamma{gamma}_lambda0.1-0.5/{i}/"
    mkdir(dir)
    for lmbda in (0.1, 0.2, 0.3, 0.4, 0.5):
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

        print(i, lmbda)

        times, series = datagen.generate_data(parameters)
        data = analysis.ca_analysis(
            times, series, parameters)
        storage.save_ca_data(data, dir, parameters)
        storage.save_series(times, series, dir, parameters)


# plt.show()


# svals, s_av, s_var, t_av, peaks, wait = ca_data
