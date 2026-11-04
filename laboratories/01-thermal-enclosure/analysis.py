r"""# 01 · Thermal enclosure and sensor lag

A 900 J/K enclosure loses heat through 15 W/K conductance. A 40 W heat step drives the physical temperature; a separate 12 s sensor lag drives the indicated temperature. The physical time constant is 60 s.

![Physical system](assets/01-physical-system.png)

The equipment sketch identifies the physical signals and assumptions before
the mathematical reduction. It is an original conceptual diagram, not an
image of a measured apparatus.

## Governing model

$$
C\dot{\Delta T}+G\Delta T=P,\qquad \tau_s\dot y+y=\Delta T.
$$

![Signal structure](assets/01-system-diagram.png)

## Computation and interpretation

Compare the analytical cascade response with python-control to a 1e-9 absolute tolerance. The two panels distinguish actual temperature rise from the positive sensor under-reading. Time is in seconds and temperature deviations are in kelvin.

![Computed response](assets/01-response.png)

The response image is the committed output of this laboratory's Python
program. Execute `run()` to repeat the calculation and its assertions.

## Run the actual laboratory

From the repository root:

```bash
cd laboratories/01-thermal-enclosure
python analysis.py
```

For an import-based session, use `importlib.util.spec_from_file_location`
with this file and call its `run()` function. The documentation name
`lab01_thermal_enclosure` disambiguates the twelve files named `analysis.py`; it is not an
installed Python package. Importing the module does not run the experiment.

[Notebook and exercises](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/laboratories/01-thermal-enclosure) ·
[Open in Colab](https://colab.research.google.com/github/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/01-thermal-enclosure/notebook.ipynb) ·
[Worked derivation](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/01-thermal-enclosure/report.pdf)

## Limits

The two poles describe a lumped linear thermal model and a first-order sensor. Radiation, saturation, varying ambient conditions and measurement noise are omitted.
"""


def run():
    """Execute the fixed laboratory, check its assertions and write response.png.

    No arguments are accepted and the return value is None. Parameters,
    initial conditions and plotting commands are the inspectable source
    below. Numerical checks raise AssertionError on a failed expectation.
    Running the function prints the laboratory metrics, creates a Matplotlib
    figure and replaces response.png in the current working directory.
    Use the laboratory directory to reproduce the repository layout.
    Scientific dependencies are imported only when this function is called.
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import control as ct
    from scipy.integrate import solve_ivp
    from scipy.optimize import brentq, least_squares
    plt.ioff()
    plt.rcParams.update({'figure.figsize': (9,4.5), 'font.size': 10, 'axes.grid': True, 'grid.alpha': .25})

    capacity, conductance, sensor_tau, power = 900., 15., 12., 40.
    tau = capacity / conductance
    time = np.linspace(0, 420, 4201)
    temperature = power/conductance*(1-np.exp(-time/tau))
    indication = power/conductance*(1-(tau*np.exp(-time/tau)-sensor_tau*np.exp(-time/sensor_tau))/(tau-sensor_tau))
    measured_model = ct.tf([1/conductance], np.convolve([tau,1],[sensor_tau,1]))
    _, simulated = ct.step_response(power*measured_model, time)
    assert np.max(np.abs(simulated-indication)) < 1e-9
    error_at_tau = np.interp(tau,time,temperature-indication)
    print(f'Thermal time constant: {tau:.3f} s; final rise: {power/conductance:.6f} K')
    print(f'Sensor under-reading at 60 s: {error_at_tau:.6f} K')
    assert error_at_tau > 0

    fig, axes = plt.subplots(1,2,figsize=(11,4))
    axes[0].plot(time,temperature,label='Enclosure'); axes[0].plot(time,indication,'--',label='Sensor')
    axes[0].set(xlabel='Time (s)',ylabel='Temperature rise (K)',title='Synthetic heat-step response'); axes[0].legend()
    axes[1].plot(time,temperature-indication,color='tab:purple')
    axes[1].set(xlabel='Time (s)',ylabel='Under-reading (K)',title='Sensor lag error')
    fig.tight_layout()

    fig.savefig("response.png",dpi=160,bbox_inches="tight")


if __name__ == "__main__":
    run()
