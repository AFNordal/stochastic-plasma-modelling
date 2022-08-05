import fppanalysis.conditional_averaging as ca
import model.point_model as pm
import matplotlib.pyplot as plt
import numpy as np
import double_exponential_fit as dxfit
from pandas import DataFrame, read_feather
import pickle


def save_series(times, series, dir, P):
    DataFrame(np.array((times, series)).transpose(), columns=['t', 'x']).to_feather(
        series_filename(dir, P))


def load_series(dir, P):
    return read_feather(series_filename(dir, P)).to_numpy().transpose()


def save_ca_data(data, dir, P):
    with open(ca_data_filename(dir, P), 'wb') as file:
        pickle.dump(data, file)


def load_ca_data(dir, P):
    with open(ca_data_filename(dir, P), 'rb') as file:
        return pickle.load(file)


def series_filename(dir, P):
    return f"{dir}gamma{P['gamma']}_lambda{P['lmbda']}_dt{P['dt']}_t{P['t']}.feather"


def ca_data_filename(dir, P):
    return f"{dir}gamma{P['gamma']}_lambda{P['lmbda']}_dt{P['dt']}_t{P['t']}_thresh{P['thresh']}" \
        f"_delta{P['delta']}_win{int(P['window'])}_normamp{int(P['normalize_amplitude'])}.pickle"
