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
lmbdas = [[[[] for i in range(6)] for j in range(4)] for k in range(3)]
tau_ds = [[[[] for i in range(6)] for j in range(4)] for k in range(3)]
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

            shape = analysis.iterated_dexp(t_av, s_av, parameters)
            fit_times, fit, lmbda, tau_d, tau_r, tau_f, err = shape
            lmbdas[0][k][j].append(lmbda)
            tau_ds[0][k][j].append(tau_d)

            shape = analysis.simple_dexp(t_av, s_av)
            fit_times, fit, lmbda, tau_d, tau_r, tau_f, err = shape
            lmbdas[1][k][j].append(lmbda)
            tau_ds[1][k][j].append(tau_d)

            shape = analysis.simple_risefall(t_av, s_av)
            fit_times, fit, lmbda, tau_d, tau_r, tau_f, err = shape
            lmbdas[2][k][j].append(lmbda)
            tau_ds[2][k][j].append(tau_d)

lmbdas = np.array(lmbdas)
tau_ds = np.array(tau_ds)
fig, (lamfig, taufig) = plt.subplots(1, 2, sharey='none')

col = ['r', 'g', 'b', 'm']
styles = ['-', '--', ':']

lamfig.axline((0, 0), (0.5, 0.5), linestyle="--", color="k", lw=1)
taufig.axline((0, 1), (0.5, 1), linestyle="--", color="k", lw=1)
for i in range(3):
    for j in range(4):
        lamfig.errorbar(true_lambdas, lmbdas[i][j].mean(1), lmbdas[i][j].std(1), color=col[j],
                        marker="", linestyle=styles[i], capsize=8, lw=1)
        taufig.errorbar(true_lambdas, tau_ds[i][j].mean(1), tau_ds[i][j].std(1), color=col[j],
                        marker="", linestyle=styles[i], capsize=8, lw=1)

colorlines = [Line2D((0, 0), (1, 1), color=c) for c in col]
stylelines = [Line2D((0, 0), (1, 1), linestyle=s, color="k") for s in styles]
lamfig.legend(colorlines, gammas)
taufig.legend(stylelines, ("connected iterated", "connected", "disconnected"))

fig.suptitle("Mean pulse parameter estimates")
lamfig.set_title("lambda")
taufig.set_title("tau_d")


plt.show()
