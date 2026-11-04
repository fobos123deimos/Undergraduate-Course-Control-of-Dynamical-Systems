r"""# 07 · Feedback delay and phase reserve

A fixed communication delay adds phase lag without changing the loop magnitude. The exact gain crossover determines the delay at which the phase reserve reaches zero.

![Physical system](assets/07-physical-system.png)

The equipment sketch identifies the physical signals and assumptions before
the mathematical reduction. It is an original conceptual diagram, not an
image of a measured apparatus.

## Governing model

$$
L(s)=\frac{8}{s(s+3)},\qquad \phi_m(\theta)=\phi_m(0)-\omega_c\theta.
$$

![Signal structure](assets/07-system-diagram.png)

## Computation and interpretation

Evaluate delays 0, 0.10 and 0.30 s. Compare the exact phase-margin deduction against a fifth-order Padé model within 0.02 degrees. The time curves use the rational approximation; the margin curve uses the exact delay phase.

![Computed response](assets/07-response.png)

The response image is the committed output of this laboratory's Python
program. Execute `run()` to repeat the calculation and its assertions.

## Run the actual laboratory

From the repository root:

```bash
cd laboratories/07-delay-budget
python analysis.py
```

For an import-based session, use `importlib.util.spec_from_file_location`
with this file and call its `run()` function. The documentation name
`lab07_delay_budget` disambiguates the twelve files named `analysis.py`; it is not an
installed Python package. Importing the module does not run the experiment.

[Notebook and exercises](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/laboratories/07-delay-budget) ·
[Open in Colab](https://colab.research.google.com/github/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/07-delay-budget/notebook.ipynb) ·
[Worked derivation](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/07-delay-budget/report.pdf)

## Limits

Padé transients are approximations. The stated delay budget applies to a constant pure delay and the specified linear loop, not variable network latency or a sampled controller.
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

    loop=ct.tf([8],[1,3,0])
    crossover=np.sqrt((-9+np.sqrt(337))/2)
    margin0=90-np.degrees(np.arctan(crossover/3))
    budget=np.radians(margin0)/crossover
    assert abs(abs(ct.evalfr(loop,1j*crossover))-1)<1e-12
    time=np.linspace(0,12,4001)
    cases=[]
    for delay in [0.,.10,.30]:
        approximation=ct.tf(*ct.pade(delay,5)) if delay else ct.tf([1],[1])
        closed=ct.feedback(loop*approximation,1)
        _,output=ct.step_response(closed,time)
        exact_margin=margin0-np.degrees(crossover*delay)
        measured_margin=ct.margin(loop*approximation)[1]
        assert abs(measured_margin-exact_margin)<0.02
        cases.append((delay,output))
        print(f'Delay {delay:.2f} s: exact margin={exact_margin:.6f} deg; Pade margin={measured_margin:.6f} deg')
    print(f'Crossover={crossover:.6f} rad/s; ideal delay budget={budget:.6f} s')

    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for delay,output in cases: axes[0].plot(time,output,label=f'Delay {delay:.2f} s')
    axes[0].set(xlabel='Time (s)',ylabel='Output / unit reference',title='Pade-based simulated responses'); axes[0].legend()
    delays=np.linspace(0,budget*1.25,200)
    axes[1].plot(delays,margin0-np.degrees(crossover*delays)); axes[1].axhline(0,color='black',lw=.8)
    axes[1].axvline(budget,color='gray',ls=':'); axes[1].set(xlabel='Constant delay (s)',ylabel='Exact phase margin (deg)',title='Delay consumes the phase reserve')
    fig.tight_layout()

    fig.savefig("response.png",dpi=160,bbox_inches="tight")


if __name__ == "__main__":
    run()
