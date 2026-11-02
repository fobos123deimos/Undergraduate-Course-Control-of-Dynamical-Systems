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
