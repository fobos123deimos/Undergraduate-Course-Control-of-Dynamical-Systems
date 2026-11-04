r"""# 05 · Motor speed and load rejection

A linear DC motor model couples current and flywheel speed. A 5 rad/s reference and 0.03 N m load step at 4 s compare proportional control with PI.

![Physical system](assets/05-physical-system.png)

The equipment sketch identifies the physical signals and assumptions before
the mathematical reduction. It is an original conceptual diagram, not an
image of a measured apparatus.

## Governing model

$$
G_v(s)=\frac{k_t}{(Ls+R)(Js+b)+k_tk_e},\qquad G_d(s)=\frac{-(Ls+R)}{(Ls+R)(Js+b)+k_tk_e}.
$$

![Signal structure](assets/05-system-diagram.png)

## Computation and interpretation

Use separate voltage and load-disturbance paths. Check stable closed-loop poles and the expected steady speeds: P retains offset, whereas PI returns to 5 rad/s. The required nominal steady voltage is 3.1 V.

![Computed response](assets/05-response.png)

The response image is the committed output of this laboratory's Python
program. Execute `run()` to repeat the calculation and its assertions.

## Run the actual laboratory

From the repository root:

```bash
cd laboratories/05-motor-load-rejection
python analysis.py
```

For an import-based session, use `importlib.util.spec_from_file_location`
with this file and call its `run()` function. The documentation name
`lab05_motor_load_rejection` disambiguates the twelve files named `analysis.py`; it is not an
installed Python package. Importing the module does not run the experiment.

[Notebook and exercises](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/laboratories/05-motor-load-rejection) ·
[Open in Colab](https://colab.research.google.com/github/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/05-motor-load-rejection/notebook.ipynb) ·
[Worked derivation](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/05-motor-load-rejection/report.pdf)

## Limits

The comparison assumes ideal voltage/current authority. Electrical saturation, friction nonlinearities and heating are absent; integral action alone does not prove actuator feasibility.
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

    R,L,J,b,kt,ke=2.,.02,.01,.02,.1,.1
    den=np.polymul([L,R],[J,b]); den[-1]+=kt*ke
    voltage_path=ct.tf([kt],den); disturbance_path=ct.tf([-L,-R],den)
    controllers=[('P',ct.tf([.8],[1])),('PI',ct.tf([.8,1.6],[1,0]))]
    time=np.linspace(0,18,9001); load=.03*(time>=4)
    responses=[]
    for label,controller in controllers:
        closed=ct.feedback(controller*voltage_path,1)
        disturbance=ct.feedback(disturbance_path,0) / (1+controller*voltage_path)
        disturbance=ct.minreal(disturbance,verbose=False)
        assert np.all(np.real(ct.poles(closed))<0)
        _,tracking=ct.step_response(5*closed,time)
        rejected=ct.forced_response(disturbance,time,load).outputs
        speed=tracking+rejected; responses.append((label,speed))
        print(f'{label}: final simulated speed={speed[-1]:.6f} rad/s')
    assert abs(responses[0][1][-1]-6.8/2.6)<1e-5
    assert abs(responses[1][1][-1]-5)<1e-4
    print('Required ideal steady voltage at 5 rad/s with load: 3.100000 V')

    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for label,speed in responses:
        axes[0].plot(time,speed,label=label); axes[1].plot(time,5-speed,label=label)
    axes[0].axhline(5,color='black',ls=':'); axes[0].set(xlabel='Time (s)',ylabel='Speed (rad/s)',title='Synthetic flywheel speed')
    axes[1].set(xlabel='Time (s)',ylabel='Tracking error (rad/s)',title='Load applied at 4 s')
    for ax in axes: ax.axvline(4,color='gray',ls=':'); ax.legend()
    fig.tight_layout()

    fig.savefig("response.png",dpi=160,bbox_inches="tight")


if __name__ == "__main__":
    run()
