r"""# 03 · Base-excited vibration isolation

An 8 kg platform on a 3200 N/m support is excited by floor displacement. Damping ratios 0.08 and 0.40 illustrate the resonance-isolation tradeoff.

![Physical system](assets/03-physical-system.png)

The equipment sketch identifies the physical signals and assumptions before
the mathematical reduction. It is an original conceptual diagram, not an
image of a measured apparatus.

## Governing model

$$
\frac{X(s)}{Y(s)}=\frac{bs+k}{ms^2+bs+k},\qquad \omega_n=\sqrt{k/m}.
$$

![Signal structure](assets/03-system-diagram.png)

## Computation and interpretation

Check stable poles and the unit-transmissibility crossing at sqrt(2) times the natural frequency. The plot uses angular frequency in rad/s and displacement transmissibility in dB; increased damping reduces resonance but worsens high-frequency isolation.

![Computed response](assets/03-response.png)

The response image is the committed output of this laboratory's Python
program. Execute `run()` to repeat the calculation and its assertions.

## Run the actual laboratory

From the repository root:

```bash
cd laboratories/03-vibration-isolation
python analysis.py
```

For an import-based session, use `importlib.util.spec_from_file_location`
with this file and call its `run()` function. The documentation name
`lab03_vibration_isolation` disambiguates the twelve files named `analysis.py`; it is not an
installed Python package. Importing the module does not run the experiment.

[Notebook and exercises](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/laboratories/03-vibration-isolation) ·
[Open in Colab](https://colab.research.google.com/github/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/03-vibration-isolation/notebook.ipynb) ·
[Worked derivation](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/03-vibration-isolation/report.pdf)

## Limits

The model is linear, passive and single-axis. It excludes travel limits, nonlinear damping and the internal flexibility of the platform.
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

    mass, stiffness = 8., 3200.
    natural=np.sqrt(stiffness/mass)
    angular=np.logspace(-1,3,1000)
    curves=[]
    for damping_ratio in [0.08,0.40]:
        damping=2*damping_ratio*np.sqrt(mass*stiffness)
        model=ct.tf([damping,stiffness],[mass,damping,stiffness])
        response=np.array([abs(ct.evalfr(model,1j*w)) for w in angular])
        crossing=abs(ct.evalfr(model,1j*np.sqrt(2)*natural))
        assert abs(crossing-1)<1e-12
        assert np.all(np.real(ct.poles(model))<0)
        print(f'zeta={damping_ratio:.2f}, b={damping:.3f} N s/m, transmissibility at 2 wn={abs(ct.evalfr(model,2j*natural)):.6f}')
        curves.append((damping_ratio,response))
    print(f'Isolation threshold: {np.sqrt(2)*natural:.6f} rad/s; static compliance: {1/stiffness:.8f} m/N')

    fig,ax=plt.subplots(figsize=(9,4.5))
    for ratio,response in curves: ax.semilogx(angular,20*np.log10(response),label=f'Damping ratio {ratio:.2f}')
    ax.axhline(0,color='black',lw=.8); ax.axvline(np.sqrt(2)*natural,color='gray',ls=':')
    ax.set(xlabel='Angular frequency (rad/s)',ylabel='Displacement transmissibility (dB)',title='Synthetic platform: resonance versus isolation'); ax.legend()
    fig.tight_layout()

    fig.savefig("response.png",dpi=160,bbox_inches="tight")


if __name__ == "__main__":
    run()
