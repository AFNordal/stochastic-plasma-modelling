import double_exp_ca_analysis as analysis
from double_exponential_fit import double_exponential
import storage
import numpy as np
from matplotlib import pyplot as plt


gamma = 1
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


colors = ['blue', 'magenta', 'green']

for gamma, color in zip((0.1, 1, 10), colors):
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

    dir = f"/hdd1/rno040/experiments/n100_gamma{gamma}_lambda0.1-0.5/50/"

    ca_data = storage.load_ca_data(dir, parameters)
    svals, s_av, s_var, t_av, peaks, wait = ca_data
    fit_data = analysis.iterate_least_sq(
        t_av, s_av, parameters)

    line, = plt.plot(t_av, s_av, color=color, linestyle="-", lw=1)
    plt.plot(t_av, s_var, color=color, linestyle=":", lw=1)

    lines.append(line)

plt.legend(lines, ("true", 0.1, 1, 10))
plt.show()
