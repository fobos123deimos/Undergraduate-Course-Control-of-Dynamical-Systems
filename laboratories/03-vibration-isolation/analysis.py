import numpy as np
import matplotlib.pyplot as plt
import control as ct
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares
plt.ioff()
plt.rcParams.update({'figure.figsize': (9,4.5), 'font.size': 10, 'axes.grid': True, 'grid.alpha': .25})

mass, stiffness = 8., 3200.
natural=np.sqrt(stiffness/mass)
angular=np.logspace(-1,3,1000)
curves=[]
for damping_ratio in [0.08,0.40]:
    damping=2*damping_ratio*np.sqrt(mass*stiffness)
    model=ct.tf([damping,stiffness],[mass,damping,stiffness])
    response=np.array([abs(ct.evalfr(model,1j*w)) for w in angular])
    crossing=abs(ct.evalfr(model,1j*np.sqrt(2)*natural))
    assert abs(crossing-1)<1e-12
    assert np.all(np.real(ct.poles(model))<0)
    print(f'zeta={damping_ratio:.2f}, b={damping:.3f} N s/m, transmissibility at 2 wn={abs(ct.evalfr(model,2j*natural)):.6f}')
    curves.append((damping_ratio,response))
print(f'Isolation threshold: {np.sqrt(2)*natural:.6f} rad/s; static compliance: {1/stiffness:.8f} m/N')

fig,ax=plt.subplots(figsize=(9,4.5))
for ratio,response in curves: ax.semilogx(angular,20*np.log10(response),label=f'Damping ratio {ratio:.2f}')
ax.axhline(0,color='black',lw=.8); ax.axvline(np.sqrt(2)*natural,color='gray',ls=':')
ax.set(xlabel='Angular frequency (rad/s)',ylabel='Displacement transmissibility (dB)',title='Synthetic platform: resonance versus isolation'); ax.legend()
fig.tight_layout()

fig.savefig("response.png",dpi=160,bbox_inches="tight")
