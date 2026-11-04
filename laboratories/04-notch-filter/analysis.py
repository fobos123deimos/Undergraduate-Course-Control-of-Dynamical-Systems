r"""# 04 · Passive notch filter and component tolerance

The series network uses L=0.01 H, C=100 microfarad and R=10 ohm. Measuring across L+C produces a notch; measuring across C produces a different numerator despite identical poles.

![Physical system](assets/04-physical-system.png)

The equipment sketch identifies the physical signals and assumptions before
the mathematical reduction. It is an original conceptual diagram, not an
image of a measured apparatus.

## Governing model

$$
H(s)=\frac{LCs^2+1}{LCs^2+RCs+1},\qquad \omega_0=\frac{1}{\sqrt{LC}}.
$$

![Signal structure](assets/04-system-diagram.png)

## Computation and interpretation

Sweep capacitance factors 0.9, 1.0 and 1.1. Assert stable poles and zero response at each analytical notch. Frequency is in rad/s; the 1e-8 magnitude floor affects only the displayed decibel curve.

![Computed response](assets/04-response.png)

The response image is the committed output of this laboratory's Python
program. Execute `run()` to repeat the calculation and its assertions.

## Run the actual laboratory

From the repository root:

```bash
cd laboratories/04-notch-filter
python analysis.py
```

For an import-based session, use `importlib.util.spec_from_file_location`
with this file and call its `run()` function. The documentation name
`lab04_notch_filter` disambiguates the twelve files named `analysis.py`; it is not an
installed Python package. Importing the module does not run the experiment.

[Notebook and exercises](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/laboratories/04-notch-filter) ·
[Open in Colab](https://colab.research.google.com/github/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/04-notch-filter/notebook.ipynb) ·
[Worked derivation](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/04-notch-filter/report.pdf)

## Limits

Components and source are ideal. Parasitics, loading, inductance tolerance and measurement noise are not included.
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

    inductance, capacitance, resistance = .01,100e-6,10.
    angular=np.logspace(1,5,1600)
    curves=[]
    for factor in [.9,1.,1.1]:
        c=capacitance*factor
        model=ct.tf([inductance*c,0,1],[inductance*c,resistance*c,1])
        notch=1/np.sqrt(inductance*c)
        assert abs(ct.evalfr(model,1j*notch))<1e-12
        assert np.all(np.real(ct.poles(model))<0)
        response=np.array([abs(ct.evalfr(model,1j*w)) for w in angular])
        curves.append((factor,response))
        print(f'C factor={factor:.2f}: notch={notch:.6f} rad/s ({notch/(2*np.pi):.6f} Hz)')
    capacitor=ct.tf([1],[inductance*capacitance,resistance*capacitance,1])
    cap_response=np.array([abs(ct.evalfr(capacitor,1j*w)) for w in angular])

    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for factor,response in curves: axes[0].semilogx(angular,20*np.log10(np.maximum(response,1e-8)),label=f'C / Cnom = {factor:.1f}')
    axes[0].set(xlabel='Angular frequency (rad/s)',ylabel='Gain (dB)',title='Notch location and tolerance',xlim=(500,2000),ylim=(-60,3)); axes[0].legend()
    axes[1].semilogx(angular,20*np.log10(np.maximum(curves[1][1],1e-8)),label='Across L + C')
    axes[1].semilogx(angular,20*np.log10(cap_response),'--',label='Across C')
    axes[1].set(xlabel='Angular frequency (rad/s)',ylabel='Gain (dB)',title='Same poles, different output'); axes[1].legend()
    fig.tight_layout()

    fig.savefig("response.png",dpi=160,bbox_inches="tight")


if __name__ == "__main__":
    run()
