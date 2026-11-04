r"""# 08 · Lead-lag compensation for a camera axis

A normalized camera axis is shaped for a 3 rad/s crossover and 55-degree lead-only phase margin. A lag stage raises low-frequency gain while approximately preserving crossover.

![Physical system](assets/08-physical-system.png)

The equipment sketch identifies the physical signals and assumptions before
the mathematical reduction. It is an original conceptual diagram, not an
image of a measured apparatus.

## Governing model

$$
G(s)=\frac{1}{s(s+1)},\qquad C_{\rm lead}(s)=K\frac{Ts+1}{\alpha Ts+1}.
$$

![Signal structure](assets/08-system-diagram.png)

## Computation and interpretation

Check all poles, the 55-degree lead margin and a final margin between 54 and 55 degrees after lag. Compare the step transient with the long-horizon unit-ramp tracking error; the lag design raises velocity gain by approximately a factor of five.

![Computed response](assets/08-response.png)

The response image is the committed output of this laboratory's Python
program. Execute `run()` to repeat the calculation and its assertions.

## Run the actual laboratory

From the repository root:

```bash
cd laboratories/08-camera-compensation
python analysis.py
```

For an import-based session, use `importlib.util.spec_from_file_location`
with this file and call its `run()` function. The documentation name
`lab08_camera_compensation` disambiguates the twelve files named `analysis.py`; it is not an
installed Python package. Importing the module does not run the experiment.

[Notebook and exercises](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/laboratories/08-camera-compensation) ·
[Open in Colab](https://colab.research.google.com/github/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/08-camera-compensation/notebook.ipynb) ·
[Worked derivation](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/08-camera-compensation/report.pdf)

## Limits

The normalized plant omits motor current limits, camera inertia variation, backlash and image-processing delay. The ramp-error result is a linear steady-state statement.
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

    plant=ct.tf([1],[1,1,0]); crossover=3.; desired_margin=55.
    phase=np.angle(ct.evalfr(plant,1j*crossover),deg=True)
    needed=np.radians(desired_margin-180-phase)
    alpha=(1-np.sin(needed))/(1+np.sin(needed))
    lead_time=1/(crossover*np.sqrt(alpha)); gain=np.sqrt(alpha)/abs(ct.evalfr(plant,1j*crossover))
    lead=ct.tf(gain*np.array([lead_time,1]),[alpha*lead_time,1])
    lag=ct.tf([1/.03,1],[1/.006,1])
    scale=1/abs(ct.evalfr(lead*lag*plant,1j*crossover))
    controllers=[('Lead',lead),('Lead + lag',scale*lead*lag)]
    time=np.linspace(0,160,16001); responses=[]
    for label,controller in controllers:
        closed=ct.feedback(controller*plant,1)
        margin=ct.margin(controller*plant)[1]; kv=float(ct.dcgain(controller))
        assert np.all(ct.poles(closed).real<0)
        _,step=ct.step_response(closed,time)
        ramp=ct.forced_response(closed,time,time).outputs
        responses.append((label,step,time-ramp))
        print(f'{label}: phase margin={margin:.6f} deg, Kv={kv:.6f}, limiting unit-ramp error={1/kv:.6f}')
    assert abs(ct.margin(lead*plant)[1]-55)<1e-7
    assert 54 < ct.margin(scale*lead*lag*plant)[1] <55
    assert 4.9 < float(ct.dcgain(scale*lead*lag)/ct.dcgain(lead)) <5.1

    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for label,step,error in responses:
        axes[0].plot(time,step,label=label); axes[1].plot(time,error,label=label)
    axes[0].set(xlabel='Time (s)',ylabel='Output / unit reference',title='Reference-step transient',xlim=(0,10))
    axes[1].set(xlabel='Time (s)',ylabel='Unit-ramp tracking error',title='Low-frequency accuracy')
    for ax in axes: ax.legend()
    fig.tight_layout()

    fig.savefig("response.png",dpi=160,bbox_inches="tight")


if __name__ == "__main__":
    run()
