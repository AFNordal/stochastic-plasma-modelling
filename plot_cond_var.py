from math import inf
from double_exponential_fit import double_exponential
import storage
import numpy as np
from matplotlib import pyplot as plt

gammas = (0.1, 1, 10, inf)
lmbda = 0
t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5


fig, subfigs = plt.subplots(1, 2, sharey=True)
lmbdas = (0, 0.2)


colors = ['blue', 'magenta', 'green', 'orange']

for i, (lmbda, subfig) in enumerate(zip(lmbdas, subfigs)):
    true_time = np.arange(-delta/2, delta/2, dt)
    true_curve = double_exponential(
        len(true_time)//2, true_time, lmbda, lmbda-1, 1, 0)
    line, = (subfig.plot(true_time, true_curve,
                         color="red", linestyle="--", lw=2))
    lines = []
    lines.append(line)

    for gamma, color in zip(gammas, colors):
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

        dir = f"/hdd1/rno040/experiments/base/gamma{gamma}/0/"

        ca_data = storage.load_ca_data(dir, parameters)
        svals, s_av, s_var, t_av, peaks, wait = ca_data

        line, = subfig.plot(t_av, s_av/max(s_av),
                            color=color, linestyle="-", lw=1)
        subfig.plot(t_av, s_var, color=color, linestyle=":", lw=1)

        lines.append(line)

    if i == 0:
        subfig.legend(lines, ("True",)+gammas, loc="upper right")
    subfig.set_title(f"lambda={lmbda}")
    subfig.set_ylim([None, 1.05])

fig.suptitle(f"Conditionally averaged waveforms with variance")
plt.show()
