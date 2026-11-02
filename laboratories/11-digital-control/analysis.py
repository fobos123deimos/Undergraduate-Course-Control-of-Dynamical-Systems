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
