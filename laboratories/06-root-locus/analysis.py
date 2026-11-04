r"""# 06 · Gain selection and the stability boundary

A normalized third-order plant illustrates root-locus reasoning. Routh stability gives 0<K<96, with the boundary frequency sqrt(12) rad/s.

![Physical system](assets/06-physical-system.png)

The equipment sketch identifies the physical signals and assumptions before
the mathematical reduction. It is an original conceptual diagram, not an
image of a measured apparatus.

## Governing model

$$
G(s)=\frac{1}{s(s+2)(s+6)},\qquad p(s)=s^3+8s^2+12s+K.
$$

![Signal structure](assets/06-system-diagram.png)

## Computation and interpretation

Compare gains 12, 60 and 100, verifying that the largest pole real part agrees with the analytical stability classification. The second panel traces roots for 600 gains between 0 and 130.

![Computed response](assets/06-response.png)

The response image is the committed output of this laboratory's Python
program. Execute `run()` to repeat the calculation and its assertions.

## Run the actual laboratory

From the repository root:

```bash
cd laboratories/06-root-locus
python analysis.py
```

For an import-based session, use `importlib.util.spec_from_file_location`
with this file and call its `run()` function. The documentation name
`lab06_root_locus` disambiguates the twelve files named `analysis.py`; it is not an
installed Python package. Importing the module does not run the experiment.

[Notebook and exercises](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/laboratories/06-root-locus) ·
[Open in Colab](https://colab.research.google.com/github/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/06-root-locus/notebook.ipynb) ·
[Worked derivation](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/06-root-locus/report.pdf)

## Limits

The unstable response at K=100 is intentional. Root locations are scatter samples, not continuous branch tracking; no nonlinear saturation or uncertainty is represented.
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

    plant=ct.tf([1],[1,8,12,0])
    time=np.linspace(0,20,6001)
    responses=[]
    for gain in [12.,60.,100.]:
        closed=ct.feedback(gain*plant,1)
        poles=ct.poles(closed)
        assert (np.max(poles.real)<0)==(gain<96)
        _,output=ct.step_response(closed,time)
        responses.append((gain,output))
        print(f'K={gain:.0f}: largest pole real part={poles.real.max():.6f}')
    breakaway=(-8+2*np.sqrt(7))/3
    break_gain=-breakaway*(breakaway+2)*(breakaway+6)
    print(f'Breakaway={breakaway:.8f}; gain={break_gain:.8f}; boundary frequency={np.sqrt(12):.8f} rad/s')
    gains=np.linspace(0,130,600)
    all_poles=np.array([np.roots([1,8,12,g]) for g in gains])

    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for gain,output in responses: axes[0].plot(time,output,label=f'K={gain:g}')
    axes[0].set(xlabel='Time (s)',ylabel='Output / unit reference',title='Stable and unstable gains'); axes[0].legend()
    axes[1].scatter(all_poles.real,all_poles.imag,s=3,c=np.repeat(gains,3),cmap='viridis')
    axes[1].axvline(0,color='black',lw=.8); axes[1].set(xlabel='Real pole part (1/s)',ylabel='Imaginary pole part (rad/s)',title='Root locations over K = 0...130')
    fig.tight_layout()

    fig.savefig("response.png",dpi=160,bbox_inches="tight")


if __name__ == "__main__":
    run()
