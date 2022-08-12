from math import inf
import fit_analysis as analysis
import storage
import numpy as np
from matplotlib.lines import Line2D
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
lmbdas = [[[[] for i in range(6)] for j in range(4)] for k in range(4)]
tau_ds = [[[[] for i in range(6)] for j in range(4)] for k in range(4)]
for k,  gamma in enumerate(gammas):
    for i in tqdm(range(5)):
        for j, lmbda in enumerate(true_lambdas):
            paramlist = (
                {
                    "gamma": gamma,
                    "lmbda": lmbda,
                    "t": t,
                    "dt": dt,
                    "delta": delta,
                    "window": window,
                    "normalize_amplitude": normalize_amplitude,
                    "thresh": thresh
                },

                {
                    "gamma": gamma,
                    "lmbda": lmbda,
                    "t": t,
                    "dt": dt,
                    "delta": delta,
                    "window": not window,
                    "normalize_amplitude": normalize_amplitude,
                    "thresh": thresh
                },

                {
                    "gamma": gamma,
                    "lmbda": lmbda,
                    "t": t,
                    "dt": dt,
                    "delta": delta,
                    "window": window,
                    "normalize_amplitude": not normalize_amplitude,
                    "thresh": thresh
                },

                {
                    "gamma": gamma,
                    "lmbda": lmbda,
                    "t": t,
                    "dt": dt,
                    "delta": 6,
                    "window": window,
                    "normalize_amplitude": normalize_amplitude,
                    "thresh": thresh
                }
            )

            dirs = (
                f"/hdd1/rno040/experiments/base/gamma{gamma}/{i}/",
                f"/hdd1/rno040/experiments/win_0/gamma{gamma}/{i}/",
                f"/hdd1/rno040/experiments/normamp_0/gamma{gamma}/{i}/",
                f"/hdd1/rno040/experiments/delta_6/gamma{gamma}/{i}/"
            )

            for l, (parameters, dir) in enumerate(zip(paramlist, dirs)):
                data = storage.load_ca_data(dir, parameters)
                svals, s_av, s_var, t_av, peaks, wait = data

                shape = analysis.simple_dexp(t_av, s_av)
                fit_times, fit, lmbda, tau_d, tau_r, tau_f, err = shape
                lmbdas[l][k][j].append(lmbda)
                tau_ds[l][k][j].append(tau_d)

lmbdas = np.array(lmbdas)
tau_ds = np.array(tau_ds)
fig, (lamfig, taufig) = plt.subplots(1, 2)

col = ['r', 'g', 'b', 'm']
styles = ['-', '--', ':', '-.']

lamfig.axline((0, 0), (0.5, 0.5), linestyle="--", color="k", lw=1)
taufig.axline((0, 1), (0.5, 1), linestyle="--", color="k", lw=1)
for i in range(4):
    for j in range(4):
        lamfig.errorbar(true_lambdas, lmbdas[i][j].mean(1), lmbdas[i][j].std(1), color=col[j],
                        marker="", linestyle=styles[i], capsize=8, lw=1)
        taufig.errorbar(true_lambdas, tau_ds[i][j].mean(1), tau_ds[i][j].std(1), color=col[j],
                        marker="", linestyle=styles[i], capsize=8, lw=1)

colorlines = [Line2D((0, 0), (1, 1), color=c) for c in col]
stylelines = [Line2D((0, 0), (1, 1), linestyle=s, color="k") for s in styles]
lamfig.legend(colorlines, gammas)
taufig.legend(stylelines, ("base", "window=0", "normamp=0", "delta=6"))

fig.suptitle("Mean pulse parameter estimates")
lamfig.set_title("lambda")
taufig.set_title("tau_d")


plt.show()
