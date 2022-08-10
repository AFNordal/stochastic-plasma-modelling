import double_exp_ca_analysis as analysis
import storage

display_t = [48, 93]
gamma = 1
lmbda = 0.2
t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2

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

dir = f"/hdd1/rno040/experiments/n100_gamma{gamma}_lambda0.1-0.5/2/"

times, series = storage.load_series(dir, parameters)
t0, t1 = tuple(map(lambda x: int(x/dt), display_t))
analysis.ca_analysis(times[0:t1-t0], series[t0:t1],
                     parameters, illustrate=True)
