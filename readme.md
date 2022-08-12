# Conditional averaging and least squares


## Storage

---

### Time series

Each series is saved in single files in the feather file format. The file name has the form `gamma{gamma}_lambda{lambda}_dt{dt}_t{t}.feather`. 

These files are easily written and read by the script `storage.py`. Writing is done with the function `save_series`, which takes the time array, data array, the directory to write in and a dictionary of experiment parameters as input. Reading is done with the function `load_series`, which takes the directory to read from and a dictionary of experiment parameters as input. It returns a tuple of (time, data) The directory string needs to end with a "/". 

---

### Analysis results

Similarily, data from the conditional averaging analysis of one series is stored in one file in the pickle format. The file name takes the form `{dir}gamma{gamma}_lambda{lambda}_dt{dt}_t{t}_thresh{thresh}_delta{delta}_win{window}_normamp{normalize_amplitude}.pickle`, where `window` and `normalize_amplitude` are booleans represented by 1 or 0. 

Analysis data is handled in a tuple of `(svals, s_av, s_var, t_av, peaks, wait)`, which is how the `cond_av` function returns it. Writing is done with the function `save_ca_data`, which takes result tuple, the directory to write in and a dictionary of experiment parameters as input. Reading is done with the function `load_ca_data`, which takes the directory to read from and a dictionary of experiment parameters as input. It returns the result tuple. The directory string needs to end with a "/". 

---

### Directory structure

All of the data is stored on `/hdd1/rno040/experiments`. Each experiment keeps its data in one directory. 

For the experiments that make n realizations for each value of lambda, the experiment directory has n subdirectories, each with data from one realization for each value of lambda.

---

## Scripts

---

### `generate_series.py`

A wrapper for the `superposed-pulses` module. Contains:

#### `generate_data`  

Creates a realization of the time series.

Inputs:  
A dictionary containing gamma, lambda, t and dt

Returns:  
A tuple of (time array, data array)

#### `by_convolution`  

Creates a realization of the time series by convolution. Suitable for high gammas.

Inputs:  
A dictionary containing lambda, t and dt

Returns:  
A tuple of (time array, data array)

---

### `storage.py`

A script to manage writing and reading data to and from files. This is documented in [the section on data storage](#Storage).

---

### `fit_analysis.py`

A script that wraps `conditional_averaging.py` and `double_exponential_fit.py`. Contains:

#### `ca_analysis`

Runs conditional averaging on time series

Inputs:  
Time and data arrays from series, dictionary of parameters and optionally a verbosity level. The dictionary must contain gamma, lambda, t, dt, delta, window, normalize_amplitude, thresh. These parameters are explained in `conditional_averaging.py`.

Returns:
A tuple of analysis data, `(svals, s_av, s_var, t_av, peaks, wait)`.

#### `iterated_dexp`

Fits a double exponential function to numerical data. Begins by doing the fit over all of the data. A new analysis domain is then calculated as `[peak_time-rise_time, peak_time+fall_time]` where rise and fall time are estimated from the previous fit. This is iterated until it converges on values for rise and fall time.

Inputs:  
Time and data arrays from series, dictionary of parameters and optionally a verbosity level. The dictionary must contain dt.

Returns:
A tuple of `(time array from fit, data array from fit, lambda_guess, tau_d_guess, tau_r_guess, tau_f_guess, error from fit)`. The error is the mean of the square rooted diagonals of the covariance of the fitted parameters.

#### `simple_dexp`

Fits a double exponential function to numerical data. Performs fit on all input data.

Inputs:  
Time and data arrays from series.

Returns:
A tuple of `(time array from fit, data array from fit, lambda_guess, tau_d_guess, tau_r_guess, tau_f_guess, error from fit)`. The error is the mean of the square rooted diagonals of the covariance of the fitted parameters.

#### `simple_risefall`

Individually fits an exponential function to both sides of a peak waveform. Performs fit on all input data.

Inputs:  
Time and data arrays from series.

Returns:
A tuple of `(time array from fit, data array from fit, lambda_guess, tau_d_guess, tau_r_guess, tau_f_guess, error from fit)`. The error is the mean of the square rooted diagonals of the covariance of the fitted parameters.
#### `calculate_params`

Calculates waveform parameters from raw function parameters

Inputs:  
list of raw function parameters

Returns:
A tuple of `(lambda_guess, tau_d_guess, tau_r_guess, tau_f_guess)`

---
### `double_exponential_fit.py`

Executes least squares fit of double exponential. Is most easily used with its wrapper, `fit_analysis.py`. Contains:

#### `d_exp_fit`

Fits a double exponential function to numerical data.

Inputs:  
Time and data arrays from series and a domain. The domain can be an int, in which case the fit is done over `[peak_time-domain, peak_time+domain]`, or a list of two elements, in which case the fit is done over `[peak_time-domain[0], peak_time+domain[1]]`. `shared_params` is a boolean that decides whether or not to use the same scaling factor and constant term for the falling and rising curve.

Returns:  
Time and data arrays of numerical realization of fitted curve, optimal parameters and error.

#### `rise_fall_fit`

Individually fits an exponential function to both sides of a peak waveform.

Inputs:
Time and data arrays to perform fit on.

Outputs:
Time and data arrays of fitted curve, fitted parameters and error.

#### `double_exponential`

A template for a double exponential function

#### `rise_fall_exponential`

A template "containing" two independent exponentials.

---

### `generate_n.py`

Generates and analyzes n realizations for each value of lambda in `(0, 0.1, 0.2, 0.3, 0.4, 0.5)`. This is just run as a script. Gamma and data directory is modified manually in the variable declaration.

---

### `generate_gamma_lambda_scan.py`

Generates and analyzes one realization for each lambda-gamma combination in a range. The ranges are adjusted manually in the for-loops. This is run as a script.

---

### `plot_histograms.py`

Plots the shape of the histograms of lambda and tau_d estimates for one value of gamma. The mean is subtracted from the estimate sets before they are rescaled by their standard deviation.

---

### `plot_2d_map.py`

Plots a map of estimate errors for lambda and tau_d. errors are represented as difference between estimated and true value.

---

### `plot_base_box.py`

Plots the mean estimated lambda and tau_d with standard deviation with base parameters for conditional averaging.

---

### `plot_methods_box.py`

Plots the mean estimated lambda and tau_d with standard deviation with base parameters for conditional averaging. Does this for the three different fit methods.

---

### `plot_variations_box.py`

Plots the mean estimated lambda and tau_d with standard deviation with all variations of parameters for conditional averaging.

---

### `plot_series.py`

Plots an example of the time series.

---

### `analyze_variations.py`

Performs conditional averaging on series data from file.

---

### `plot_dexp_fit.py`

Plots the estimated pulse shape, the true pulse shape and the conditionally averaged pulse shape. For double exponential fit.

---

### `plot_risefall_fit.py`

Plots the estimated pulse shape, the true pulse shape and the conditionally averaged pulse shape. For individual fits to rise and fall curve.

---

### `plot_cond_var.py`

Plots the conditional variance, the true pulse shape and the conditionally averaged pulse shape for one value of lambda and a range of gammas.

---

### `plot_variations_cond_var.py`

Plots the conditional variance, the true pulse shape and the conditionally averaged pulse shape for one value of lambda, one value of gamma and a range of conditional averaging parameters.

---

### `plot_cond_av.py`

Illustrates the conditional averaging process with a plot of the time series with each valid peak highlighted.
