import numpy as np
import matplotlib.pyplot as plt
import control as ct
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares
plt.ioff()
plt.rcParams.update({'figure.figsize': (9,4.5), 'font.size': 10, 'axes.grid': True, 'grid.alpha': .25})

plant=ct.tf([1],[1,1,0]); crossover=3.; desired_margin=55.
phase=np.angle(ct.evalfr(plant,1j*crossover),deg=True)
needed=np.radians(desired_margin-180-phase)
alpha=(1-np.sin(needed))/(1+np.sin(needed))
lead_time=1/(crossover*np.sqrt(alpha)); gain=np.sqrt(alpha)/abs(ct.evalfr(plant,1j*crossover))
lead=ct.tf(gain*np.array([lead_time,1]),[alpha*lead_time,1])
lag=ct.tf([1/.03,1],[1/.006,1])
scale=1/abs(ct.evalfr(lead*lag*plant,1j*crossover))
controllers=[('Lead',lead),('Lead + lag',scale*lead*lag)]
time=np.linspace(0,160,16001); responses=[]
for label,controller in controllers:
    closed=ct.feedback(controller*plant,1)
    margin=ct.margin(controller*plant)[1]; kv=float(ct.dcgain(controller))
    assert np.all(ct.poles(closed).real<0)
    _,step=ct.step_response(closed,time)
    ramp=ct.forced_response(closed,time,time).outputs
    responses.append((label,step,time-ramp))
    print(f'{label}: phase margin={margin:.6f} deg, Kv={kv:.6f}, limiting unit-ramp error={1/kv:.6f}')
assert abs(ct.margin(lead*plant)[1]-55)<1e-7
assert 54 < ct.margin(scale*lead*lag*plant)[1] <55
assert 4.9 < float(ct.dcgain(scale*lead*lag)/ct.dcgain(lead)) <5.1

fig,axes=plt.subplots(1,2,figsize=(11,4))
for label,step,error in responses:
    axes[0].plot(time,step,label=label); axes[1].plot(time,error,label=label)
axes[0].set(xlabel='Time (s)',ylabel='Output / unit reference',title='Reference-step transient',xlim=(0,10))
axes[1].set(xlabel='Time (s)',ylabel='Unit-ramp tracking error',title='Low-frequency accuracy')
for ax in axes: ax.legend()
fig.tight_layout()

fig.savefig("response.png",dpi=160,bbox_inches="tight")
