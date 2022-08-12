import fppanalysis.conditional_averaging as ca
import matplotlib.pyplot as plt
import numpy as np
import double_exponential_fit as dxfit


# Wrapper for conditional_averaging.py
def ca_analysis(times, series, P, illustrate=False):
    return ca.cond_av(series, times, P["thresh"], delta=P["delta"], window=P["window"],
                      normalize_amplitude=P["normalize_amplitude"], illustrate=illustrate)


def iterated_dexp(times, series, P, verbose=0):
    dt = P["dt"]
    tau_d = None
    p_tau_d = None
    # begin fit with whole pulse as domain
    domain = None
    iterations = 0
    invalid = False

    # Iteratively estimate domain [tau_r, tau_f]
    while (p_tau_d is None or abs(p_tau_d-tau_d) > 1e-10) and iterations < 100:
        try:
            fit_times, fit, params, err = dxfit.d_exp_fit(
                times, series, domain=domain)
        except RuntimeError:
            fit_times, fit, params, err = dxfit.d_exp_fit(
                times, series)
            invalid = True
        p_tau_d = tau_d
        lmbda, tau_d, tau_r, tau_f = calculate_params(
            params)

        domain = (int(tau_r/dt), int(tau_f/dt))

        iterations += 1

        if invalid:
            break
        if tau_d < 50*dt or domain[0] < 10:
            domain = None
            invalid = True

    if verbose >= 1:
        if invalid:
            print(f"Iteration stopped due to invalid domain; {domain}")
        elif iterations < 100:
            print(f"Least squares converged after {iterations} iterations")
        else:
            print(
                f"Least squares did not converge. Last step was {abs(p_tau_d-tau_d):.5f}")

    if verbose >= 2:
        print("""/ {2:.2f}*exp(t/{0:.2f}){3:+.2f},  \tt<0
\ {2:.2f}*exp(t/{1:.2f}){3:+.2f}, \tt>=0
lambda={4:.3f}, tau_d={5:.3f}
mean_dev={6:.5f}""".format(*params[:4], lmbda, tau_d, np.mean(err)))

    if verbose >= 3:
        plt.plot(times, series)
        plt.plot(fit_times, fit)
        plt.show()

    return fit_times, fit, lmbda, tau_d, tau_r, tau_f, np.mean(err)


def simple_dexp(times, series):
    fit_times, fit, params, err = dxfit.d_exp_fit(times, series)
    lmbda, tau_d, tau_r, tau_f = calculate_params(params)
    return fit_times, fit, lmbda, tau_d, tau_r, tau_f, np.mean(err)


def simple_risefall(times, series):
    fit_times, fit, params, err = dxfit.rise_fall_fit(times, series)
    lmbda, tau_d, tau_r, tau_f = calculate_params(params)
    return fit_times, fit, lmbda, tau_d, tau_r, tau_f, np.mean(err)


# calculate lambda, tau_d, tau_r and tau_f from the raw optimized parameters
def calculate_params(params):
    lmbda = params[0] / (params[0]-params[1])
    tau_d = params[0] - params[1]
    tau_r = tau_d*lmbda
    tau_f = tau_d-tau_r
    return lmbda, tau_d, tau_r, tau_f
