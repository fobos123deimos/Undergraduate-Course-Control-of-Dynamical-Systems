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
