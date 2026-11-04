r"""# 11 · Sampling and closed-loop stability

An exact held-input first-order plant with tau=0.5 s is paired with the specified discrete PI update (Kp=2, Ki=4). The recurrence state is [output, integral contribution].

![Physical system](assets/11-physical-system.png)

The equipment sketch identifies the physical signals and assumptions before
the mathematical reduction. It is an original conceptual diagram, not an
image of a measured apparatus.

## Governing model

$$
A_d(T_s)=\begin{bmatrix}a-bK_p&b\\-K_iT_s&1\end{bmatrix},\quad a=e^{-T_s/\tau},\ b=1-a.
$$

![Signal structure](assets/11-system-diagram.png)

## Computation and interpretation

Compare sample periods 0.05, 0.5 and 1.0 s. Compute spectral radii and solve the first unit-circle crossing at 0.75 s. The unstable one-second response illustrates why a continuous-time design cannot be copied blindly into a digital implementation.

![Computed response](assets/11-response.png)

The response image is the committed output of this laboratory's Python
program. Execute `run()` to repeat the calculation and its assertions.

## Run the actual laboratory

From the repository root:

```bash
cd laboratories/11-digital-control
python analysis.py
```

For an import-based session, use `importlib.util.spec_from_file_location`
with this file and call its `run()` function. The documentation name
`lab11_digital_control` disambiguates the twelve files named `analysis.py`; it is not an
installed Python package. Importing the module does not run the experiment.

[Notebook and exercises](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/laboratories/11-digital-control) ·
[Open in Colab](https://colab.research.google.com/github/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/11-digital-control/notebook.ipynb) ·
[Worked derivation](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/11-digital-control/report.pdf)

## Limits

The bound belongs to this exact update ordering, zero-order-hold plant and gains. A computational delay, another integrator discretization or saturation changes the matrix and stability boundary.
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

    kp,ki,tau=2.,4.,.5
    def closed_matrix(period):
        a=np.exp(-period/tau); b=1-a
        return np.array([[a-b*kp,b],[-ki*period,1.]])
    periods=[.05,.5,1.]; responses=[]
    for period in periods:
        a=np.exp(-period/tau); b=1-a
        state=np.zeros(2); time=np.arange(0,16+period/2,period); values=[]
        matrix=closed_matrix(period)
        for instant in time:
            values.append(state[0]); state=matrix@state+np.array([b*kp,ki*period])
        radius=np.max(np.abs(np.linalg.eigvals(matrix)))
        assert (radius<1)==(period<.75)
        responses.append((period,time,np.array(values)))
        print(f'Ts={period:.2f} s: spectral radius={radius:.8f}')
    boundary=brentq(lambda period:np.max(np.abs(np.linalg.eigvals(closed_matrix(period))))-1,.6,.9)
    assert abs(boundary-.75)<1e-10
    print(f'First unit-circle crossing: {boundary:.8f} s')
    grid=np.linspace(.005,1.1,300); radii=[np.max(np.abs(np.linalg.eigvals(closed_matrix(p)))) for p in grid]

    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for period,time,values in responses: axes[0].plot(time,values,'.-',label=f'Ts={period:g} s',markersize=3)
    axes[0].set(xlabel='Time (s)',ylabel='Sampled output',title='Digital implementation response'); axes[0].legend()
    axes[1].plot(grid,radii); axes[1].axhline(1,color='black',lw=.8); axes[1].axvline(.75,color='gray',ls=':')
    axes[1].set(xlabel='Sampling period (s)',ylabel='Closed-loop spectral radius',title='Stability requires radius < 1')
    fig.tight_layout()

    fig.savefig("response.png",dpi=160,bbox_inches="tight")


if __name__ == "__main__":
    run()
