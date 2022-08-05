import double_exp_ca_analysis as analysis
import generate_series as datagen
import storage
import numpy as np
from matplotlib import pyplot as plt
from os import mkdir
from tqdm import tqdm


gamma = 1
t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5

dir = "experiment_data/10x10/"

lmbdas = []
tau_ds = []
for gamma in np.round(np.logspace(-1, 1, 11), 2):
    lmbdas.insert(0, [])
    tau_ds.insert(0, [])
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

        ca_data = storage.load_ca_data(dir, parameters)
        svals, s_av, s_var, t_av, peaks, wait = ca_data
        shape_data = analysis.iterate_least_sq(
            t_av, s_av, parameters, verbose=0)
        fit_times, fit, lmbda_guess, tau_d_guess, err = shape_data
        lmbdas[0].append(abs(lmbda_guess-lmbda)/lmbda)
        tau_ds[0].append(abs(tau_d_guess-1))

fig, axs = plt.subplots(1, 2)
im0 = axs[0].imshow(lmbdas, extent=[0.1, 0.5, -1, 1], aspect=0.25)
axs[0].set_xlabel('lambda')
axs[0].set_ylabel('log(gamma)')
axs[0].set_title('lambda estimation error')
fig.colorbar(im0, ax=axs[0])

im1 = axs[1].imshow(tau_ds, extent=[0.1, 0.5, -1, 1], aspect=0.25)
axs[1].set_xlabel('lambda')
axs[1].set_ylabel('log(gamma)')
axs[1].set_title('tau_d estimation error')
fig.colorbar(im1, ax=axs[1])

plt.show()


# svals, s_av, s_var, t_av, peaks, wait = ca_data
