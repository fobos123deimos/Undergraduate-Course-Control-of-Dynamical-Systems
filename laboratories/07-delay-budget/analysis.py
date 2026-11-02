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
