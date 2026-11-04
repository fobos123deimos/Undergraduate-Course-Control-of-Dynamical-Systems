r"""# 10 · State feedback with one thermal measurement

Two coupled thermal deviations are controlled through the first zone, while only the second is measured. Both controllability and observability ranks are two.

![Physical system](assets/10-physical-system.png)

The equipment sketch identifies the physical signals and assumptions before
the mathematical reduction. It is an original conceptual diagram, not an
image of a measured apparatus.

## Governing model

$$
\dot x=Ax+Bu,\quad y=Cx,\quad u=-K\hat x+Nr,\quad \dot{\hat x}=A\hat x+Bu+L(y-C\hat x).
$$

![Signal structure](assets/10-system-diagram.png)

## Computation and interpretation

Place feedback poles at -0.20 and -0.35 per second and observer poles at -0.8 and -1.0 per second. Integrate the augmented [x, x-estimate] system and verify pole placement, estimation-error decay and unit output tracking.

![Computed response](assets/10-response.png)

The response image is the committed output of this laboratory's Python
program. Execute `run()` to repeat the calculation and its assertions.

## Run the actual laboratory

From the repository root:

```bash
cd laboratories/10-observer-control
python analysis.py
```

For an import-based session, use `importlib.util.spec_from_file_location`
with this file and call its `run()` function. The documentation name
`lab10_observer_control` disambiguates the twelve files named `analysis.py`; it is not an
installed Python package. Importing the module does not run the experiment.

[Notebook and exercises](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/laboratories/10-observer-control) ·
[Open in Colab](https://colab.research.google.com/github/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/10-observer-control/notebook.ipynb) ·
[Worked derivation](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/10-observer-control/report.pdf)

## Limits

The separation principle here applies to the nominal linear continuous-time model. No sensor noise, input limits, robustness guarantee or discrete implementation is included.
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

    A=np.array([[-.15,.05],[.05,-.10]]); B=np.array([[.1],[0.]]); C=np.array([[0.,1.]])
    assert np.linalg.matrix_rank(ct.ctrb(A,B))==2
    assert np.linalg.matrix_rank(ct.obsv(A,C))==2
    K=ct.place(A,B,[-.20,-.35]); observer=ct.place(A.T,C.T,[-.8,-1.]).T
    prefilter=-1/float((C@np.linalg.solve(A-B@K,B))[0,0])
    augmented=np.block([[A-B@K,B@K],[np.zeros((2,2)),A-observer@C]])
    input_vector=np.r_[B[:,0]*prefilter,np.zeros(2)]
    initial=np.array([.6,-.4,.6,-.4])
    time=np.linspace(0,80,4001)
    solution=solve_ivp(lambda t,z:augmented@z+input_vector,[0,80],initial,t_eval=time,rtol=1e-10,atol=1e-11).y
    estimate=solution[:2]-solution[2:]
    assert np.max(np.abs(np.poly(A-B@K)-np.poly([-.2,-.35])))<1e-10
    assert np.max(np.abs(np.poly(A-observer@C)-np.poly([-.8,-1.])))<1e-10
    assert np.linalg.norm(solution[2:,-1])<1e-8
    assert abs(solution[1,-1]-1)<1e-5
    print('Feedback K:',K.round(8)); print('Observer L:',observer.ravel().round(8)); print(f'Reference prefilter N={prefilter:.8f}')

    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for state in range(2):
        axes[0].plot(time,solution[state],label=f'Zone {state+1} actual'); axes[0].plot(time,estimate[state],'--',label=f'Zone {state+1} estimate')
        axes[1].plot(time,solution[state+2],label=f'Zone {state+1}')
    axes[0].set(xlabel='Time (s)',ylabel='Temperature deviation (K)',title='Nominal output regulation'); axes[0].legend(fontsize=8)
    axes[1].set(xlabel='Time (s)',ylabel='Estimation error (K)',title='Observer convergence',xlim=(0,12)); axes[1].legend()
    fig.tight_layout()

    fig.savefig("response.png",dpi=160,bbox_inches="tight")


if __name__ == "__main__":
    run()
