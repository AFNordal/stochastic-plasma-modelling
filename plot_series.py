import generate_series as datagen
import storage
import numpy as np
import matplotlib.pyplot as plt

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

# times, series = datagen.generate_data(parameters)
t0, t1 = tuple(map(lambda x: int(x/dt), display_t))
series = (series-series.mean())/series.std()
plt.plot(times[0:t1-t0], series[t0:t1], 'k')

plt.show()
