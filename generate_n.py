import double_exp_ca_analysis as analysis
import generate_series as datagen
import storage
from os import mkdir

n = 100
gamma = 1
t = 100000
dt = 0.01
delta = 3
window = True
normalize_amplitude = True
thresh = 2.5


for i in range(n):
    dir = f"/hdd1/rno040/experiments/n{n}_gamma{gamma}_lambda0.1-0.5/{i}/"
    mkdir(dir)
    for lmbda in (0.1, 0.2, 0.3, 0.4, 0.5):
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

        print(f"{i=} \t{lmbda=} \t{gamma=}")

        times, series = datagen.generate_data(parameters)
        data = analysis.ca_analysis(
            times, series, parameters)
        storage.save_ca_data(data, dir, parameters)
        storage.save_series(times, series, dir, parameters)
