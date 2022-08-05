import double_exp_ca_analysis as analysis
import storage
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm


gamma = 0.4
t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5

# fig, axs = plt.subplots(1, 5, sharey='all', label="lambda error")
lmbdas = [[[] for i in range(5)] for j in range(3)]
tau_ds = [[[] for i in range(5)] for j in range(3)]
for k,  gamma in enumerate((0.1, 0.4, 1)):
    for i in tqdm(range(10)):
        dir = f"/hdd1/rno040/experiment_data/N/gamma{gamma}_lambda0.1->0.5/{i}/"
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
            shape = analysis.iterate_least_sq(
                t_av, s_av, parameters, verbose=0)
            fit_times, fit, lmbda_guess, tau_d_guess, err = shape
            # print(lmbda_guess, tau_d_guess)

            lmbdas[k][j].append(lmbda_guess/lmbda)
            tau_ds[k][j].append(tau_d_guess)

lmbdas = np.array(lmbdas)
tau_ds = np.array(tau_ds)
fig, (lamfig, taufig) = plt.subplots(1, 2)

mrk = ['s', 'v', 'o']
col = ['r', 'g', 'b']
for i in range(3):
    lamfig.errorbar(np.arange(0.1, 0.6, 0.1),
                    lmbdas[i].mean(1), lmbdas[i].std(1), color=col[i], marker="", capsize=8, lw=1)
    taufig.errorbar(np.arange(0.1, 0.6, 0.1),
                    tau_ds[i].mean(1), tau_ds[i].std(1), linestyle="none", color=col[i], marker=mrk[i], markerfacecolor="w", markeredgecolor=col[i], capsize=10, lw=1)
lamfig.set_title("guesses for lambda")
taufig.set_title("guesses for tau_d")
# lamfig.set_ylim(bottom=0)
# taufig.set_ylim(bottom=0)

plt.show()
