from copy import copy
from math import inf
import fit_analysis as analysis
import storage
from os import mkdir

n = 100
gamma = 10
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

savedirs = (
    f"/hdd1/rno040/experiments/win_0/gamma{gamma}/",
    f"/hdd1/rno040/experiments/normamp_0/gamma{gamma}/",
    f"/hdd1/rno040/experiments/delta_6/gamma{gamma}/"
)


for i in range(n):
    dir = f"/hdd1/rno040/experiments/n100_gamma{gamma}_lambda0-0.5/{i}/"
    for j in range(len(paramlist)):
        savedir = f"{savedirs[j]}{i}/"
        mkdir(savedir)
        for lmbda in (0, 0.1, 0.2, 0.3, 0.4, 0.5):

            print(f"{i=} \t{lmbda=} \t{gamma=}")

            # load series, anlyze and save analysis
            paramlist[j]["lmbda"] = lmbda
            times, series = storage.load_series(dir, paramlist[j])
            data = analysis.ca_analysis(times, series, paramlist[j])
            storage.save_ca_data(data, savedir, paramlist[j])
