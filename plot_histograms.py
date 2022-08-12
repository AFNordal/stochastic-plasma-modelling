from math import inf
import fit_analysis as analysis
import storage
from matplotlib import pyplot as plt
from tqdm import tqdm
import numpy as np


gamma = inf
t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5


lmbdas = [[] for i in range(6)]
tau_ds = [[] for i in range(6)]
for i in tqdm(range(100)):
    dir = f"/hdd1/rno040/experiments/base/gamma{gamma}/{i}/"
    for j, lmbda in enumerate((0, 0.1, 0.2, 0.3, 0.4, 0.5)):
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

        data = storage.load_ca_data(dir, parameters)
        svals, s_av, s_var, t_av, peaks, wait = data
        shape = analysis.simple_dexp(t_av, s_av)
        fit_times, fit, lmbda_guess, tau_d_guess, tau_r, tau_f, err = shape

        lmbdas[j].append(lmbda_guess)
        tau_ds[j].append(tau_d_guess)

lmbdas = np.array(lmbdas)
tau_d = np.array(tau_ds)

fig = plt.figure(constrained_layout=True)
fig.suptitle(f"Shapes of pulse parameter estimates for {gamma=}")
subfigs = fig.subfigures(2, 1)
subfigs[0].suptitle("lambda")
subfigs[1].suptitle("tau_d")

l_axs = subfigs[0].subplots(1, 6, sharex='row')
t_axs = subfigs[1].subplots(1, 6, sharex='row')
for j, (lmbda, tau_d) in enumerate(zip(lmbdas, tau_ds)):
    l_axs[j].hist((lmbda-np.mean(lmbda))/np.std(lmbda))
    t_axs[j].hist((tau_d-np.mean(tau_d))/np.std(tau_d))
    l_axs[j].set_title(f'lambda={(j)*0.1:.1f}')
plt.show()
