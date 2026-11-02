import numpy as np
import matplotlib.pyplot as plt
import control as ct
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares
plt.ioff()
plt.rcParams.update({'figure.figsize': (9,4.5), 'font.size': 10, 'axes.grid': True, 'grid.alpha': .25})

capacity, conductance, sensor_tau, power = 900., 15., 12., 40.
tau = capacity / conductance
time = np.linspace(0, 420, 4201)
temperature = power/conductance*(1-np.exp(-time/tau))
indication = power/conductance*(1-(tau*np.exp(-time/tau)-sensor_tau*np.exp(-time/sensor_tau))/(tau-sensor_tau))
measured_model = ct.tf([1/conductance], np.convolve([tau,1],[sensor_tau,1]))
_, simulated = ct.step_response(power*measured_model, time)
assert np.max(np.abs(simulated-indication)) < 1e-9
error_at_tau = np.interp(tau,time,temperature-indication)
print(f'Thermal time constant: {tau:.3f} s; final rise: {power/conductance:.6f} K')
print(f'Sensor under-reading at 60 s: {error_at_tau:.6f} K')
assert error_at_tau > 0

fig, axes = plt.subplots(1,2,figsize=(11,4))
axes[0].plot(time,temperature,label='Enclosure'); axes[0].plot(time,indication,'--',label='Sensor')
axes[0].set(xlabel='Time (s)',ylabel='Temperature rise (K)',title='Synthetic heat-step response'); axes[0].legend()
axes[1].plot(time,temperature-indication,color='tab:purple')
axes[1].set(xlabel='Time (s)',ylabel='Under-reading (K)',title='Sensor lag error')
fig.tight_layout()

fig.savefig("response.png",dpi=160,bbox_inches="tight")
