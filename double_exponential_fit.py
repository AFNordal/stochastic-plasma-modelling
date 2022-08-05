from typing import Iterable
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def d_exp_fit(T, S, domain, shared_params=True):

    peak = np.argmax(S)
    if isinstance(domain, int):
        T = T[peak-int(domain/2):peak+int(domain/2)]
        S = S[peak-int(domain/2):peak+int(domain/2)]
        peak = int(domain/2)
    elif isinstance(domain, Iterable):
        assert len(domain) == 2
        T = T[peak-domain[0]:peak+domain[1]]
        S = S[peak-domain[0]:peak+domain[1]]
        peak = domain[0]

    rise = np.arange(0, peak+1, 1, int)
    fall = np.arange(peak, len(S), 1, int)
    # plt.plot(T[rise], S[rise])
    # plt.plot(T[fall], S[fall])

    if shared_params:
        def exponential(t, a, b, c, d):
            return np.append(c*np.exp(t[:peak]/a)+d, c*np.exp(t[peak:]/b)+d)
    else:
        def exponential(t, a, b, c, d, e, f):
            return np.append(c*np.exp(t[:peak]/a)+d, e*np.exp(t[peak:]/b)+f)

    if shared_params:
        guess = (1, -1, S[peak], 0)
    else:
        guess = (1, -1, S[peak], 0, S[peak], 0)

    params, cov = curve_fit(
        exponential, T, S, p0=guess)

    err = np.sqrt(np.diag(cov))

    fit = exponential(T, *params)

    if shared_params:
        params = np.append(params, params[-2:])
    return T, fit, params, err
