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
