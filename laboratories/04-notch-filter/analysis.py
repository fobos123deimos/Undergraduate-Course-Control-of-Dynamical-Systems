import numpy as np
import matplotlib.pyplot as plt
import control as ct
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares
plt.ioff()
plt.rcParams.update({'figure.figsize': (9,4.5), 'font.size': 10, 'axes.grid': True, 'grid.alpha': .25})

inductance, capacitance, resistance = .01,100e-6,10.
angular=np.logspace(1,5,1600)
curves=[]
for factor in [.9,1.,1.1]:
    c=capacitance*factor
    model=ct.tf([inductance*c,0,1],[inductance*c,resistance*c,1])
    notch=1/np.sqrt(inductance*c)
    assert abs(ct.evalfr(model,1j*notch))<1e-12
    assert np.all(np.real(ct.poles(model))<0)
    response=np.array([abs(ct.evalfr(model,1j*w)) for w in angular])
    curves.append((factor,response))
    print(f'C factor={factor:.2f}: notch={notch:.6f} rad/s ({notch/(2*np.pi):.6f} Hz)')
capacitor=ct.tf([1],[inductance*capacitance,resistance*capacitance,1])
cap_response=np.array([abs(ct.evalfr(capacitor,1j*w)) for w in angular])

fig,axes=plt.subplots(1,2,figsize=(11,4))
for factor,response in curves: axes[0].semilogx(angular,20*np.log10(np.maximum(response,1e-8)),label=f'C / Cnom = {factor:.1f}')
axes[0].set(xlabel='Angular frequency (rad/s)',ylabel='Gain (dB)',title='Notch location and tolerance',xlim=(500,2000),ylim=(-60,3)); axes[0].legend()
axes[1].semilogx(angular,20*np.log10(np.maximum(curves[1][1],1e-8)),label='Across L + C')
axes[1].semilogx(angular,20*np.log10(cap_response),'--',label='Across C')
axes[1].set(xlabel='Angular frequency (rad/s)',ylabel='Gain (dB)',title='Same poles, different output'); axes[1].legend()
fig.tight_layout()

fig.savefig("response.png",dpi=160,bbox_inches="tight")
