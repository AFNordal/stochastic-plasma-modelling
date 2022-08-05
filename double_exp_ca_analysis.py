import fppanalysis.conditional_averaging as ca
import matplotlib.pyplot as plt
import numpy as np
import double_exponential_fit as dxfit


def ca_analysis(times, series, P):
    return ca.cond_av(series, times, P["thresh"], delta=P["delta"], window=P["window"],
                      normalize_amplitude=P["normalize_amplitude"], illustrate=False)


def iterate_least_sq(times, series, P, verbose=1):
    dt = P["dt"]
    tau_d_guess = None
    p_tau_d_guess = None
    domain = None
    iterations = 0
    while (p_tau_d_guess is None or abs(p_tau_d_guess-tau_d_guess) > 1e-10) and iterations < 100:
        fit_times, fit, params, err = dxfit.d_exp_fit(
            times, series, domain=domain, shared_params=True)
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
\ {4:.2f}*exp(t/{1:.2f}){5:+.2f}, \tt>=0
lambda={6:.3f}, tau_d={7:.3f}
mean_dev={8:.5f}""".format(*params, lmbda_guess, tau_d_guess, np.mean(err)))

    if verbose >= 3:
        plt.plot(times, series)
        plt.plot(fit_times, fit)
        plt.show()

    return fit_times, fit, lmbda_guess, tau_d_guess, np.mean(err)


def calculate_params(params):
    lmbda = params[0] / (params[0]-params[1])
    tau_d = params[0] - params[1]
    tau_r = tau_d*lmbda
    tau_f = tau_d-tau_r
    return lmbda, tau_d, tau_r, tau_f
