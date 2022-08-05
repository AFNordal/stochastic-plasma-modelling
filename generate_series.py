import model.point_model as pm
import numpy as np

folder = "experiment_data/gamma10_lambda0.1->0.5/"


def generate_data(P):
    ts_generator = pm.PointModel(P["gamma"], P["t"], P["dt"])
    pulse_generator = pm.ExponentialShortPulseGenerator(P["lmbda"])
    forcing_generator = pm.StandardForcingGenerator()
    forcing_generator.set_duration_distribution(lambda k: np.ones(k))
    ts_generator.set_pulse_shape(pulse_generator)
    ts_generator.set_custom_forcing_generator(forcing_generator)

    times, series = ts_generator.make_realization()
    series = (series-np.mean(series))/np.sqrt(np.mean(series**2))
    return times, series
