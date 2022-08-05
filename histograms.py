import double_exp_ca_analysis as analysis
import generate_series as datagen
import storage
import numpy as np
from matplotlib import pyplot as plt
from os import mkdir
from tqdm import tqdm


gamma = 0.4
t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5

# fig, axs = plt.subplots(1, 5, sharey='all', label="lambda error")
lmbdas = [[] for i in range(5)]
tau_ds = [[] for i in range(5)]
for i in tqdm(range(50)):
    dir = f"experiment_data/N/gamma{gamma}_lambda0.1->0.5/{i}/"
    for j, lmbda in enumerate((0.1, 0.2, 0.3, 0.4, 0.5)):
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
        shape = analysis.iterate_least_sq(t_av, s_av, parameters, verbose=0)
        fit_times, fit, lmbda_guess, tau_d_guess, err = shape
        # print(lmbda_guess, tau_d_guess)

        lmbdas[j].append(lmbda_guess/lmbda)
        tau_ds[j].append(tau_d_guess)

fig = plt.figure(constrained_layout=True)
subfigs = fig.subfigures(2, 1)
subfigs[0].suptitle("guesses for lambda")
subfigs[1].suptitle("guesses for tau_d")

l_axs = subfigs[0].subplots(1, 5, sharex='row')
t_axs = subfigs[1].subplots(1, 5, sharex='row')
for j, (lmbda, tau_d) in enumerate(zip(lmbdas, tau_ds)):
    l_axs[j].hist(lmbda)
    l_axs[j].axvline(x=1, c='r')
    t_axs[j].hist(tau_d)
    t_axs[j].axvline(x=1, c='r')
    l_axs[j].set_title(f'lambda={(j+1)*0.1:.1f}')
plt.show()