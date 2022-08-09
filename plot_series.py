import double_exp_ca_analysis as analysis
import generate_series as datagen
import storage
import numpy as np
import matplotlib.pyplot as plt

gamma = 1
lmbda = 0.2
t = 25
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5

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

times, series = datagen.generate_data(parameters)
plt.plot(times, series)
plt.show()
