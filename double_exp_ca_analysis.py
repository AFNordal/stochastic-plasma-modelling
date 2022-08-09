import fppanalysis.conditional_averaging as ca
import matplotlib.pyplot as plt
import numpy as np
import double_exponential_fit as dxfit


# Wrapper for conditional_averaging.py
def ca_analysis(times, series, P, illustrate=False):
    return ca.cond_av(series, times, P["thresh"], delta=P["delta"], window=P["window"],
                      normalize_amplitude=P["normalize_amplitude"], illustrate=illustrate)


def iterate_least_sq(times, series, P, verbose=1, return_raw=False):
    dt = P["dt"]
    tau_d_guess = None
    p_tau_d_guess = None
    # begin fit with whole pulse as domain
    domain = None
    iterations = 0

    # Iteratively estimate domain [tau_r, tau_f]
    while (p_tau_d_guess is None or abs(p_tau_d_guess-tau_d_guess) > 1e-10) and iterations < 100:
        fit_times, fit, params, err = dxfit.d_exp_fit(
            times, series, domain=domain)
        p_tau_d_guess = tau_d_guess
        lmbda_guess, tau_d_guess, tau_r_guess, tau_f_guess = calculate_params(
            params)
        domain = (int(tau_r_guess/dt), int(tau_f_guess/dt))
        iterations += 1

    if verbose >= 1:
        if iterations < 100:
            print(f"Least squares converged after {iterations} iterations")
        else:
            print(
                f"Least squares did not converge. Last step was {abs(p_tau_d_guess-tau_d_guess):.5f}")

    if verbose >= 2:
        print("""/ {2:.2f}*exp(t/{0:.2f}){3:+.2f},  \tt<0
\ {2:.2f}*exp(t/{1:.2f}){3:+.2f}, \tt>=0
lambda={4:.3f}, tau_d={5:.3f}
mean_dev={6:.5f}""".format(*params[:4], lmbda_guess, tau_d_guess, np.mean(err)))

    if verbose >= 3:
        plt.plot(times, series)
        plt.plot(fit_times, fit)
        plt.show()

    if return_raw:
        return fit_times, fit, lmbda_guess, tau_d_guess, np.mean(err), params
    else:
        return fit_times, fit, lmbda_guess, tau_d_guess, np.mean(err)


# calculate lambda, tau_d, tau_r and tau_f from the raw optimized parameters
def calculate_params(params):
    lmbda = params[0] / (params[0]-params[1])
    tau_d = params[0] - params[1]
    tau_r = tau_d*lmbda
    tau_f = tau_d-tau_r
    return lmbda, tau_d, tau_r, tau_f
