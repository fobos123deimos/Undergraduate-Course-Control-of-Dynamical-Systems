r"""# 02 · Ventilation and local linearization

The hypothetical well-mixed enclosure has volume 120 m³, nominal airflow 3 m³/min and excess-tracer equilibrium 120 ppm. Changing airflow multiplies concentration, giving a bilinear balance.

![Physical system](assets/02-physical-system.png)

The equipment sketch identifies the physical signals and assumptions before
the mathematical reduction. It is an original conceptual diagram, not an
image of a measured apparatus.

## Governing model

$$
V\dot c=q_s-fc,\qquad V\dot{\delta c}=-f_0\delta c-c_0\delta f.
$$

![Signal structure](assets/02-system-diagram.png)

## Computation and interpretation

Apply airflow increases of 10% and 100%, then compare exact exponential solutions, numerical ODE integration and the local linearization. The 100% case exposes the invalid zero-concentration steady prediction of a large-signal linear extrapolation.

![Computed response](assets/02-response.png)

The response image is the committed output of this laboratory's Python
program. Execute `run()` to repeat the calculation and its assertions.

## Run the actual laboratory

From the repository root:

```bash
cd laboratories/02-ventilation
python analysis.py
```

For an import-based session, use `importlib.util.spec_from_file_location`
with this file and call its `run()` function. The documentation name
`lab02_ventilation` disambiguates the twelve files named `analysis.py`; it is not an
installed Python package. Importing the module does not run the experiment.

[Notebook and exercises](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/laboratories/02-ventilation) ·
[Open in Colab](https://colab.research.google.com/github/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/02-ventilation/notebook.ipynb) ·
[Worked derivation](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/02-ventilation/report.pdf)

## Limits

Concentration is a synthetic well-mixed tracer. The local model assumes small deviations; its poor large-step accuracy is a reported result, not a failed integrator.
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

    volume, source, flow0 = 120., 360., 3.
    concentration0 = source/flow0
    time = np.linspace(0,240,2401)
    cases=[]
    for fraction in [0.1,1.0]:
        change=flow0*fraction
        exact_final=source/(flow0+change)
        exact=exact_final+(concentration0-exact_final)*np.exp(-(flow0+change)*time/volume)
        linear=concentration0-concentration0/flow0*change*(1-np.exp(-flow0*time/volume))
        numerical=solve_ivp(lambda t,c:(source-(flow0+change)*c)/volume,[0,time[-1]],[concentration0],t_eval=time,rtol=1e-10,atol=1e-11).y[0]
        assert np.max(np.abs(exact-numerical))<1e-6
        cases.append((fraction,exact,linear))
        print(f'Airflow +{100*fraction:.0f}%: exact final {exact_final:.6f} ppm; linear final {concentration0*(1-fraction):.6f} ppm')

    fig, axes=plt.subplots(1,2,figsize=(11,4))
    for ax,(fraction,exact,linear) in zip(axes,cases):
        ax.plot(time,exact,label='Bilinear balance'); ax.plot(time,linear,'--',label='Local linearization')
        ax.set(xlabel='Time (min)',ylabel='Excess tracer (ppm)',title=f'Airflow increase: {fraction:.0%}'); ax.legend()
    fig.tight_layout()

    fig.savefig("response.png",dpi=160,bbox_inches="tight")


if __name__ == "__main__":
    run()
