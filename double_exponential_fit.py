from typing import Iterable
import numpy as np
from scipy.optimize import curve_fit


# fit double exponential to numerical data
def d_exp_fit(T, S, domain=None):

    # determine peak
    peak = np.argmax(S)
    # select T and S according to domain
    if isinstance(domain, int):
        T = T[peak-int(domain/2):peak+int(domain/2)]
        S = S[peak-int(domain/2):peak+int(domain/2)]
        peak = int(domain/2)
    elif isinstance(domain, Iterable):
        assert len(domain) == 2
        T = T[max(0, peak-domain[0]):min(peak+domain[1], len(S))]
        S = S[max(0, peak-domain[0]):min(peak+domain[1], len(S))]
        peak = np.argmax(S)
    # The function to be optimized

    def fit_func(*args):
        return double_exponential(peak, *args)

    # Initial conditions
    guess = (1, -1, S[peak], 0)

    params, cov = curve_fit(
        fit_func, T, S, p0=guess)

    err = np.sqrt(np.diag(cov))

    fit = fit_func(T, *params)

    return T, fit, params, err


# fit independent exponentails to each side of peak
def rise_fall_fit(T, S):

    # determine peak
    peak = np.argmax(S)

    # The function to be optimized
    def fit_func(*args):
        return rise_fall_exponential(peak, *args)

    # Initial conditions
    guess = (0.1, -1, S[peak], 0, S[peak], 0)

    params, cov = curve_fit(
        fit_func, T, S, p0=guess)

    err = np.sqrt(np.diag(cov))

    fit = fit_func(T, *params)

    return T, fit, params, err


# Template for double exponential
def double_exponential(peak, t, a, b, c, d):
    if a == 0:
        return np.append(np.zeros(peak), c*np.exp(t[peak:]/b)+d)
    else:
        return np.append(c*np.exp(t[:peak]/a)+d, c*np.exp(t[peak:]/b)+d)


def rise_fall_exponential(peak, t, a, b, c, d, e, f):
    return np.append(c*np.exp(t[:peak]/a)+d, e*np.exp(t[peak:]/b)+f)
