import double_exp_ca_analysis as analysis
from double_exponential_fit import double_exponential
import storage
import numpy as np
import matplotlib
from matplotlib import pyplot as plt


gamma = 1
lmbda = 0.2
t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5

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
fit_time, fit, lmbda_guess, tau_d_guess, err = fit_data

true_time = np.arange(-delta/2, delta/2, dt)
true_curve = double_exponential(
    len(true_time)//2, true_time, lmbda, lmbda-1, 1, 0)

plt.plot(true_time, true_curve, color="g", linestyle="--", lw=1)
plt.plot(t_av, s_av, color="b", lw=2)
plt.plot(t_av, s_var, color="r", linestyle="--", lw=1)
plt.show()
