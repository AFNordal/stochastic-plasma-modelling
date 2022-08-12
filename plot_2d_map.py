import fit_analysis as analysis
import storage
import numpy as np
from matplotlib import pyplot as plt


gamma = 1
t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5

dir = "/hdd1/rno040/experiments/10x10/"

lmbdas = []
tau_ds = []
for gamma in np.round(np.logspace(-1, 1, 11), 2):
    lmbdas.insert(0, [])
    tau_ds.insert(0, [])
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

        ca_data = storage.load_ca_data(dir, parameters)
        svals, s_av, s_var, t_av, peaks, wait = ca_data
        shape_data = analysis.simple_dexp(
            t_av, s_av)
        fit_times, fit, lmbda_guess, tau_d_guess, tau_r, tau_f, err = shape_data
        lmbdas[0].append(lmbda_guess-lmbda)
        tau_ds[0].append(tau_d_guess-1)

fig, axs = plt.subplots(1, 2, sharex=True, sharey=True)
im0 = axs[0].imshow(lmbdas, extent=[0, 0.5, -1, 1], cmap="terrain",
                    aspect=0.25, vmin=-0.16, vmax=0.3)
axs[0].set_xlabel('lambda')
axs[0].set_ylabel('log(gamma)')
axs[0].set_title('lambda: estimate-true')
fig.colorbar(im0, ax=axs[0])

im1 = axs[1].imshow(tau_ds, extent=[0, 0.5, -1, 1], cmap="terrain",
                    aspect=0.25, vmin=-0.35, vmax=0.65)
axs[1].set_xlabel('lambda')
axs[1].set_ylabel('log(gamma)')
axs[1].set_title('tau_d: estimate-true')
fig.colorbar(im1, ax=axs[1])

plt.show()


# svals, s_av, s_var, t_av, peaks, wait = ca_data
