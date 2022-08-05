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

For the experiments that make n realizations for each value of lambda, the experiment directory has n subdirectories, each with data from one realization for each value of lambda. Sounds complicated? Just take a look and it'll make sense:) 

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

---

### `storage.py`

A script to manage writing and reading data to and from files. This is documented in [the section on data storage](#Storage).

---

### `double_exp_ca_analysis.py`

A script that wraps `conditional_averaging.py` and `double_exponential_fit.py`. Contains:

#### `ca_analysis`

Runs conditional averaging on time series

Inputs:  
Time and data arrays from series, dictionary of parameters and optionally a verbosity level. The dictionary must contain gamma, lambda, t, dt, delta, window, normalize_amplitude, thresh. These parameters are explained in `conditional_averaging.py`.

Returns:
A tuple of analysis data, `(svals, s_av, s_var, t_av, peaks, wait)`.

#### `iterate_least_sq`

Fits a double exponential function numerical data. Begins by doing the fit over all of the data. A new analysis domain is then calculated as `[peak_time-rise_time, peak_time+fall_time]` where rise and fall time are estimated from the previous fit. This is iterated until it converges on values for rise and fall time.

Inputs:  
Time and data arrays from series, dictionary of parameters and optionally a verbosity level. The dictionary must contain dt

Returns:
A tuple of `time array from fit, data array from fit, lambda_guess, tau_d_guess, error from fit`. The error is the mean of the square rooted diagonals of the covariance of the fitted parameters.

---

### `double_exponential_fit.py`
Executes least squares fit of double exponential. Is most easily used with its wrapper, [`double_exp_ca_analysis.py`](#double_exp_ca_analysis.py). Contains:

#### `d_exp_fit`

Inputs:  
Time and data arrays from series, a domain and `shared_params`. The domain can be an int, in which case the fit is done over `[peak_time-domain, peak_time+domain]`, or a list of two elements, in which case the fit is done over `[peak_time-domain[0], peak_time+domain[1]]`. `shared_params` is a boolean that decides whether or not to use the same scaling factor and constant term for the falling and rising curve.

Returns:  
Time and data arrays of numerical realization of fitted curve, optimal parameters and error.

---

### `generate_n.py`

Generates and analyzes n realizations for each value of lambda in `(0.1, 0.2, 0.3, 0.4, 0.5)`. This is just run as a script. Gamma and data directory is modified manually in the variable declaration.

---

### `generate_gamma_lambda_scan.py`

Generates and analyzes one realization for each lambda-gamma combination in a range. The ranges are adjusted manually in the for-loops. It is run as a script.

---

### `histograms.py`

Plots histograms of lambda and tau_d estimates. This is run as a script.

---

### `2d_map.py`

Plots a map of estimate errors for lambda and tau_d.

