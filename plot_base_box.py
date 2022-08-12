from math import inf
import double_exp_ca_analysis as analysis
import storage
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm


t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5

gammas = (0.1, 1, 10, inf)
true_lambdas = (0, 0.1, 0.2, 0.3, 0.4, 0.5)

# fig, axs = plt.subplots(1, 5, sharey='all', label="lambda error")
lmbdas = [[[] for i in range(6)] for j in range(4)]
tau_ds = [[[] for i in range(6)] for j in range(4)]
for k,  gamma in enumerate(gammas):
    for i in tqdm(range(100)):
        dir = f"/hdd1/rno040/experiments/base/gamma{gamma}/{i}/"
        for j, lmbda in enumerate(true_lambdas):
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
            shape = analysis.simple_dexp(
                t_av, s_av)
            fit_times, fit, lmbda, tau_d, tau_r, tau_f, err = shape

            lmbdas[k][j].append(lmbda)
            tau_ds[k][j].append(tau_d)

lmbdas = np.array(lmbdas)
tau_ds = np.array(tau_ds)
fig, (lamfig, taufig) = plt.subplots(1, 2)

col = ['r', 'g', 'b', 'm']

lines = []
lamfig.axline((0.5, 0.5), slope=1, linestyle="--", color="k", lw=1)
taufig.axhline(1, linestyle="--", color="k", lw=1)
for i in range(4):
    artists = lamfig.errorbar(true_lambdas,
                              lmbdas[i].mean(1), lmbdas[i].std(1), color=col[i], marker="", capsize=8, lw=1)
    lines.append(artists[0])
    taufig.errorbar(true_lambdas,
                    tau_ds[i].mean(1), tau_ds[i].std(1), color=col[i], marker="", capsize=8, lw=1)

lamfig.legend(lines, gammas)
fig.suptitle("Mean pulse parameter estimates")
lamfig.set_title("lambda")
taufig.set_title("tau_d")


plt.show()
