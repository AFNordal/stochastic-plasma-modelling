import double_exp_ca_analysis as analysis
import storage
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm


gamma = 1
t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5

paramlist = (
    {
        "gamma": gamma,
        "t": t,
        "dt": dt,
        "delta": delta,
        "window": window,
        "normalize_amplitude": normalize_amplitude,
        "thresh": thresh
    },

    {
        "gamma": gamma,
        "t": t,
        "dt": dt,
        "delta": delta,
        "window": not window,
        "normalize_amplitude": normalize_amplitude,
        "thresh": thresh
    },

    {
        "gamma": gamma,
        "t": t,
        "dt": dt,
        "delta": delta,
        "window": window,
        "normalize_amplitude": not normalize_amplitude,
        "thresh": thresh
    },

    {
        "gamma": gamma,
        "t": t,
        "dt": dt,
        "delta": 6,
        "window": window,
        "normalize_amplitude": normalize_amplitude,
        "thresh": thresh
    }
)

dirs = (
    "/hdd1/rno040/experiments/n100_gamma1_lambda0.1-0.5/",
    "/hdd1/rno040/experiments/win_0/",
    "/hdd1/rno040/experiments/normamp_0/",
    "/hdd1/rno040/experiments/delta_6/"
)

# fig, axs = plt.subplots(1, 5, sharey='all', label="lambda error")
lmbdas = [[[] for i in range(5)] for j in paramlist]
tau_ds = [[[] for i in range(5)] for j in paramlist]
for k, (parameters, dir_) in enumerate(zip(paramlist, dirs)):
    for i in tqdm(range(100)):
        dir = f"{dir_}{i}/"
        for j, lmbda in enumerate((0.1, 0.2, 0.3, 0.4, 0.5)):
            parameters["lmbda"] = lmbda

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

col = ['r', 'g', 'b', 'm']

lines = []
for i in range(4):
    artists = lamfig.errorbar(np.arange(0.1, 0.6, 0.1),
                              lmbdas[i].mean(1), lmbdas[i].std(1), color=col[i], marker="", capsize=8, lw=1)
    lines.append(artists[0])
    taufig.errorbar(np.arange(0.1, 0.6, 0.1),
                    tau_ds[i].mean(1), tau_ds[i].std(1), color=col[i], marker="", capsize=8, lw=1)

lamfig.legend(lines, ("base", "win false", "normamp false", "delta 6"))
fig.suptitle("Mean pulse parameter estimates")
lamfig.set_title("lambda")
taufig.set_title("tau_d")

# lamfig.set_ylim(bottom=0)
# taufig.set_ylim(bottom=0)

plt.show()
