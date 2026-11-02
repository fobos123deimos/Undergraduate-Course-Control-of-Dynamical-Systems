import numpy as np
import matplotlib.pyplot as plt
import control as ct
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares
plt.ioff()
plt.rcParams.update({'figure.figsize': (9,4.5), 'font.size': 10, 'axes.grid': True, 'grid.alpha': .25})

plant=ct.tf([1],[1,8,12,0])
time=np.linspace(0,20,6001)
responses=[]
for gain in [12.,60.,100.]:
    closed=ct.feedback(gain*plant,1)
    poles=ct.poles(closed)
    assert (np.max(poles.real)<0)==(gain<96)
    _,output=ct.step_response(closed,time)
    responses.append((gain,output))
    print(f'K={gain:.0f}: largest pole real part={poles.real.max():.6f}')
breakaway=(-8+2*np.sqrt(7))/3
break_gain=-breakaway*(breakaway+2)*(breakaway+6)
print(f'Breakaway={breakaway:.8f}; gain={break_gain:.8f}; boundary frequency={np.sqrt(12):.8f} rad/s')
gains=np.linspace(0,130,600)
all_poles=np.array([np.roots([1,8,12,g]) for g in gains])

fig,axes=plt.subplots(1,2,figsize=(11,4))
for gain,output in responses: axes[0].plot(time,output,label=f'K={gain:g}')
axes[0].set(xlabel='Time (s)',ylabel='Output / unit reference',title='Stable and unstable gains'); axes[0].legend()
axes[1].scatter(all_poles.real,all_poles.imag,s=3,c=np.repeat(gains,3),cmap='viridis')
axes[1].axvline(0,color='black',lw=.8); axes[1].set(xlabel='Real pole part (1/s)',ylabel='Imaginary pole part (rad/s)',title='Root locations over K = 0...130')
fig.tight_layout()

fig.savefig("response.png",dpi=160,bbox_inches="tight")
