from typing import Iterable
import numpy as np
from scipy.optimize import curve_fit


# fit double exponential to numerical data
def d_exp_fit(T, S, domain):

    # determine peak
    peak = np.argmax(S)
    # select T and S according to domain
    if isinstance(domain, int):
        T = T[peak-int(domain/2):peak+int(domain/2)]
        S = S[peak-int(domain/2):peak+int(domain/2)]
        peak = int(domain/2)
    elif isinstance(domain, Iterable):
        assert len(domain) == 2
        T = T[peak-domain[0]:peak+domain[1]]
        S = S[peak-domain[0]:peak+domain[1]]
        peak = domain[0]

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


# Template for double exponential
def double_exponential(peak, t, a, b, c, d):
    return np.append(c*np.exp(t[:peak]/a)+d, c*np.exp(t[peak:]/b)+d)
