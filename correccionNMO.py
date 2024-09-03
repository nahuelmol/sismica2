import numpy as np
import matplotlib.pyplot as plt 

from scipy.interpolate import CubicSpline #para interpolar
from google.colab import drive

drive.mount('/content/drive')
data =np.load('/content/drive/MyDrive/sismica2/synthetic_cmp.npz')

dt = data['dt']
offsets = data['offsets']
cmp = data['CMP'] #este es el gather
nsamples = cmp.shape[0]
noffsets = cmp.shape[1]

#################GRAFICA del gather###################################
fig = plt.figure(figsize=(6, 5))
ax = plt.subplot(111)
ax.set_title('Synthetic CMP')
ax.set_xlabel('trace number')
ax.set_ylabel('time (s)')
cutoff = 0.1
ax.imshow(cmp, extent=[0.5, noffsets + 0.5, dt*nsamples, 0], 
          aspect=20, cmap='Greys', vmin=-cutoff, vmax=cutoff, 
          interpolation='none')
trace_numbers = list(range(1, noffsets + 1))
ax.set_xticks(trace_numbers)
fig.tight_layout()


#################funciones para la correccion NMO###################################
def reflection_time(t0, x, vnmo):
  t = np.sqrt(t0**2 + x**2/vnmo**2)
  return t

def nmo_correction(cmp, dt, offsets, velocities):
  nmo = np.zeros_like(cmp)
  nsamples = cmp.shape[0]
  times = np.arange(0, nsamples*dt, dt)
  for i, t0 in enumerate(times):
      for j, x in enumerate(offsets):
          t = reflection_time(t0, x, velocities[i])
          amplitude = sample_trace(cmp[:, j], t, dt)
          if amplitude is not None:
              nmo[i, j] = amplitude
  return nmo

def sample_trace(trace, time, dt):
    before = int(np.floor(time/dt))
    N = trace.size
    samples = np.arange(before - 1, before + 3)
    if any(samples < 0) or any(samples >= N):
        amplitude = None
    else:
        times = dt*samples #los tiempos de las muestras
        amps = trace[samples] #las amplitudes de las muestras
        interpolator = CubicSpline(times, amps) #interpolo
        amplitude = interpolator(time) #amplitud encontrada para un tiempo especif
    return amplitude

times = np.arange(nsamples)*dt
v1, t1 = 3800, 0.22
v2, t2 = 4500, 0.46
v_nmo = v1 + ((v2 - v1)/(t2 - t1))*(times - t1)

nmo = nmo_correction(cmp, dt, offsets, v_nmo)

#################GRAFICA de velocidades NMO, CMP y corregido###################################
fig = plt.figure(figsize=(9, 5.1))

ax = plt.subplot(131)
ax.set_title(r'$v_\mathrm{NMO}$ profile')
ax.plot(v_nmo, np.arange(nsamples)*dt, '-k')
ax.plot([v1, v2], [t1, t2], 'sk')
ax.set_xlabel('velocity (m/s)')
ax.set_ylabel('time (s)')
ax.set_xlim(3000, 5000)
ax.set_ylim(nsamples*dt, 0)
ax.grid()
ax.set_xticks(ax.get_xticks()[1:-1])

ax = plt.subplot(132)
ax.set_title('Synthetic CMP')
ax.set_xlabel('trace number')
cutoff = 0.1
aspect = 40
ax.imshow(cmp, extent=[0.5, noffsets + 0.5, dt*nsamples, 0], 
          aspect=aspect, cmap='Greys', vmin=-cutoff, vmax=cutoff, 
          interpolation='none')
trace_numbers = list(range(1, noffsets + 1))
ax.set_xticks(trace_numbers)
ax.set_yticklabels([])
ax.grid(axis='y')

ax = plt.subplot(133)
ax.set_title('NMO corrected gather')
ax.set_xlabel('trace number')
ax.imshow(nmo, extent=[0.5, noffsets + 0.5, dt*nsamples, 0], 
          aspect=aspect, cmap='Greys', vmin=-cutoff, vmax=cutoff, 
          interpolation='none')
trace_numbers = list(range(1, noffsets + 1))
ax.set_xticks(trace_numbers)
ax.set_yticklabels([])
ax.grid(axis='y')

plt.tight_layout(pad=0.2, w_pad=0)
