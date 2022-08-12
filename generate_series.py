from math import inf
from double_exponential_fit import double_exponential
import model.point_model as pm
import numpy as np
from scipy.signal import fftconvolve

folder = "experiment_data/gamma10_lambda0.1->0.5/"


# wrapper for superimposed-pulses
def generate_data(P):
    if P['gamma'] == inf:
        return by_convolution(P)
    else:
        ts_generator = pm.PointModel(P["gamma"], P["t"], P["dt"])
        pulse_generator = pm.ExponentialShortPulseGenerator(P["lmbda"])
        forcing_generator = pm.StandardForcingGenerator()
        # Set tau_d to 1
        forcing_generator.set_duration_distribution(lambda k: np.ones(k))
        ts_generator.set_pulse_shape(pulse_generator)
        ts_generator.set_custom_forcing_generator(forcing_generator)

        times, series = ts_generator.make_realization()
        return times, series


def by_convolution(P):
    N = np.random.default_rng().standard_normal(int(P['t']/P['dt']))
    cutoff = -int(np.log(1e-50)/P['dt'])
    phi_t = np.arange(-cutoff, cutoff + 1) * P['dt']
    phi = double_exponential(int(len(phi_t)/2), phi_t,
                             P['lmbda'], P['lmbda']-1, 1, 0)
    series = fftconvolve(N, phi, mode='same')
    times = np.linspace(0, P['t'], int(P['t']/P['dt']))
    return times, series
