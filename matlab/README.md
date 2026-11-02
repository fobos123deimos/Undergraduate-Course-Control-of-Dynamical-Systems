# MATLAB and GNU Octave

Run `addpath('matlab'); run_lesson(number)` for any number from 1 through 12. MATLAB needs Control System Toolbox. GNU Octave needs its control package and a working graphics backend; the function loads the package automatically.

The portable implementation covers each original scenario's core calculation, selected assertions and a plot. The Python notebooks contain the fuller narrative and complementary figures. This is newly implemented code for the current scenarios, not a port of a supplied worksheet.

The capstone uses log-parameterized `fminsearch` to keep its three fitted parameters positive, whereas Python uses bounded nonlinear least squares. MATLAB/Octave and NumPy also produce different seeded Gaussian samples. Each backend runs its own reproducible synthetic experiment; their fitted coefficients need not match bit for bit. Nominal equations, tuning formulas, held-input propagation and validation criteria agree.

The saturated PID experiment uses `ode45`, split at the reference discontinuity. All data are simulated. See [actual validation](../docs/VALIDATION.md) for which runtimes were executed.
