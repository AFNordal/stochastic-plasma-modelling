from distutils.util import subst_vars
from math import inf
import fit_analysis as analysis
from double_exponential_fit import double_exponential
import storage
import numpy as np
from matplotlib import pyplot as plt


gamma = inf
lmbda = 0.2
t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5

lines = []

true_time = np.arange(-delta/2, delta/2, dt)
true_curve = double_exponential(
    len(true_time)//2, true_time, lmbda, lmbda-1, 1, 0)

line, = (plt.plot(true_time, true_curve,
                  color="red", linestyle="--", lw=2))
lines.append(line)

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
    f"/hdd1/rno040/experiments/base/gamma{gamma}/0/",
    f"/hdd1/rno040/experiments/win_0/gamma{gamma}/0/",
    f"/hdd1/rno040/experiments/normamp_0/gamma{gamma}/0/",
    f"/hdd1/rno040/experiments/delta_6/gamma{gamma}/0/"
)


colors = ['blue', 'magenta', 'green', 'cyan']

for parameters, dir, color in zip(paramlist, dirs, colors):

    ca_data = storage.load_ca_data(dir, parameters)
    svals, s_av, s_var, t_av, peaks, wait = ca_data

    line, = plt.plot(t_av[int(len(t_av)/2-delta/(2*dt)):int(len(t_av)/2+delta/(2*dt))],
                     s_av[int(len(t_av)/2-delta/(2*dt))
                              :int(len(t_av)/2+delta/(2*dt))]/max(s_av),
                     color=color, linestyle="-", lw=1)
    plt.plot(t_av[int(len(t_av)/2-delta/(2*dt)):int(len(t_av)/2+delta/(2*dt))],
             s_var[int(len(t_av)/2-delta/(2*dt))
                       :int(len(t_av)/2+delta/(2*dt))],
             color=color, linestyle=":", lw=1)

    lines.append(line)

plt.legend(lines, ("true", "base", "win false", "normamp false", "delta 6"))
plt.suptitle(
    f"Conditionally averaged waveforms with variance\n{gamma=} lambda={lmbda}")
plt.show()
