import numpy as np
import matplotlib.pyplot as plt
import control as ct
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares
plt.ioff()
plt.rcParams.update({'figure.figsize': (9,4.5), 'font.size': 10, 'axes.grid': True, 'grid.alpha': .25})

rng=np.random.default_rng(2026)
true=np.array([1.8,4.,.6]); time=np.arange(0,30.0001,.05)
def step_model(t,gain,tau,delay,amplitude=2.,start=2.):
    elapsed=np.maximum(t-start-delay,0.)
    return amplitude*gain*(-np.expm1(-elapsed/tau))
training_true=step_model(time,*true)
training=training_true+rng.normal(0,.015,time.size)
fit=least_squares(lambda parameters:step_model(time,*parameters)-training,[1.,2.,.2],bounds=([.2,.2,0.],[4.,12.,2.]))
estimated=fit.x
assert fit.success
def multistep(parameters):
    return sum(step_model(time,*parameters,amplitude=change,start=start) for start,change in [(1.,1.),(8.,-.6),(15.,1.1),(22.,-.8)])
validation_true=multistep(true); validation=validation_true+rng.normal(0,.015,time.size)
validation_prediction=multistep(estimated)
training_rmse=np.sqrt(np.mean((step_model(time,*estimated)-training)**2))
validation_rmse=np.sqrt(np.mean((validation_prediction-validation)**2))
assert np.all(np.abs(estimated-true)/true <.08)
assert validation_rmse<.03
lam=2.; kp=estimated[1]/(estimated[0]*(lam+estimated[2])); ki=kp/estimated[1]
dt=.01; control_time=np.arange(0,35+dt/2,dt); delay_steps=round(true[2]/dt)
a=np.exp(-dt/true[1]); output=np.zeros(control_time.size); effort=np.zeros_like(output); integral=0.
for k in range(control_time.size-1):
    error=1-output[k]; request=kp*error+integral; effort[k]=np.clip(request,0,2)
    integral+=dt*(ki*error+2*(effort[k]-request))
    delayed=effort[k-delay_steps] if k>=delay_steps else 0.
    disturbance=-.2 if control_time[k]>=15 else 0.
    output[k+1]=a*output[k]+(1-a)*(true[0]*delayed+disturbance)
effort[-1]=effort[-2]
assert abs(output[-1]-1)<.01
print('Declared true [gain, tau, delay]:',true)
print('Estimated [gain, tau, delay]:',estimated.round(8))
print(f'Training RMSE={training_rmse:.6f}; independent-input validation RMSE={validation_rmse:.6f}')
print(f'PI: Kp={kp:.8f}, Ki={ki:.8f}; final regulated output={output[-1]:.6f}')

fig,axes=plt.subplots(2,2,figsize=(11,7))
axes[0,0].plot(time,training,'.',ms=2,alpha=.35,label='Synthetic noisy samples'); axes[0,0].plot(time,step_model(time,*estimated),label='Fitted model')
axes[0,0].set(xlabel='Time (s)',ylabel='Output',title='Training: one step'); axes[0,0].legend(fontsize=8)
axes[0,1].plot(time,validation,'.',ms=2,alpha=.35,label='Independent-input samples'); axes[0,1].plot(time,validation_prediction,label='Prediction without refitting')
axes[0,1].set(xlabel='Time (s)',ylabel='Output',title='Validation: multiple steps'); axes[0,1].legend(fontsize=8)
axes[1,0].plot(control_time,output); axes[1,0].axhline(1,color='black',ls=':'); axes[1,0].axvline(15,color='gray',ls=':')
axes[1,0].set(xlabel='Time (s)',ylabel='Controlled output',title='Delayed plant with disturbance at 15 s')
axes[1,1].plot(control_time,effort); axes[1,1].set(xlabel='Time (s)',ylabel='Actuator command',title='Bounded actuator: 0 to 2')
fig.tight_layout()

fig.savefig("response.png",dpi=160,bbox_inches="tight")
