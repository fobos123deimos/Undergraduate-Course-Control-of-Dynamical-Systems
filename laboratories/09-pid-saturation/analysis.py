r"""# 09 · PID saturation and back-calculation

A normalized second-order actuator is controlled by a filtered derivative-on-measurement PID. The target is 3 until 6 s and 0.2 afterwards; the first target is infeasible under the ±2 actuator limit.

![Physical system](assets/09-physical-system.png)

The equipment sketch identifies the physical signals and assumptions before
the mathematical reduction. It is an original conceptual diagram, not an
image of a measured apparatus.

## Governing model

$$
u={\rm clip}(u_{\rm raw},-2,2),\qquad \dot I=K_i(r-x)+K_{aw}(u-u_{\rm raw}).
$$

![Signal structure](assets/09-system-diagram.png)

## Computation and interpretation

Compare back-calculation gains 0 and 8. Integrate position, velocity, integral contribution and filtered position with tight tolerances. The recovery IAE after 6 s must decrease with back-calculation. Three panels show output, integral state and saturated effort.

![Computed response](assets/09-response.png)

The response image is the committed output of this laboratory's Python
program. Execute `run()` to repeat the calculation and its assertions.

## Run the actual laboratory

From the repository root:

```bash
cd laboratories/09-pid-saturation
python analysis.py
```

For an import-based session, use `importlib.util.spec_from_file_location`
with this file and call its `run()` function. The documentation name
`lab09_pid_saturation` disambiguates the twelve files named `analysis.py`; it is not an
installed Python package. Importing the module does not run the experiment.

[Notebook and exercises](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/tree/main/laboratories/09-pid-saturation) ·
[Open in Colab](https://colab.research.google.com/github/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/09-pid-saturation/notebook.ipynb) ·
[Worked derivation](https://github.com/fobos123deimos/Undergraduate-Course-Control-of-Dynamical-Systems/blob/main/laboratories/09-pid-saturation/report.pdf)

## Limits

The linear polynomial check is for the unsaturated loop; it does not certify global behavior with saturation. The nested dynamics callback is internal to run(), with the declared fixed gains.
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

    kp,ki,kd,filter_tau=25.,24.,7.,.03
    linear_den=[filter_tau,1+2*filter_tau,2+filter_tau*(1+kp)+kd,1+kp+ki*filter_tau,ki]
    assert np.max(np.roots(linear_den).real)<0
    def dynamics(reference,antiwindup):
        def derivative(t,state):
            position,velocity,integral,filtered=state
            error=reference-position
            request=kp*error+integral-kd*(position-filtered)/filter_tau
            effort=np.clip(request,-2,2)
            return [velocity,effort-2*velocity-position,ki*error+antiwindup*(effort-request),(position-filtered)/filter_tau]
        return derivative
    cases=[]; recovery=[]
    for antiwindup in [0.,8.]:
        first=solve_ivp(dynamics(3.,antiwindup),[0,6],np.zeros(4),t_eval=np.linspace(0,6,3001),rtol=1e-8,atol=1e-10,max_step=.01)
        second=solve_ivp(dynamics(.2,antiwindup),[6,12],first.y[:,-1],t_eval=np.linspace(6,12,3001),rtol=1e-8,atol=1e-10,max_step=.01)
        time=np.r_[first.t,second.t[1:]]; states=np.c_[first.y,second.y[:,1:]]
        reference=np.where(time<6,3.,.2)
        request=kp*(reference-states[0])+states[2]-kd*(states[0]-states[3])/filter_tau
        effort=np.clip(request,-2,2)
        iae=np.trapezoid(np.abs(.2-second.y[0]),second.t)
        recovery.append(iae); cases.append((antiwindup,time,states,effort))
        print(f'Back-calculation gain {antiwindup:g}: recovery IAE={iae:.6f}, final x={states[0,-1]:.6f}')
    assert recovery[1] < recovery[0]

    fig,axes=plt.subplots(1,3,figsize=(13,3.8))
    for gain,time,states,effort in cases:
        label=f'Back-calculation {gain:g}'
        axes[0].plot(time,states[0],label=label); axes[1].plot(time,states[2],label=label); axes[2].plot(time,effort,label=label)
    axes[0].plot(time,np.where(time<6,3.,.2),'k:',label='Reference')
    for ax,title,ylabel in zip(axes,['Position recovery','Integral contribution','Limited actuator'],['Position','Actuator units','Actuator units']):
        ax.set(xlabel='Time (s)',ylabel=ylabel,title=title); ax.axvline(6,color='gray',ls=':')
    axes[0].legend(fontsize=8); fig.tight_layout()

    fig.savefig("response.png",dpi=160,bbox_inches="tight")


if __name__ == "__main__":
    run()
