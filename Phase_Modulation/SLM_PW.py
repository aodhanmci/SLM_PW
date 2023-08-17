##############################
# code to look at the effect of an SLM on the amplitude and phase of a beam
# originally written by Jeroen, converted by Aodhan
##############################

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from scipy import signal
import scipy.ndimage as ndimage

# setup the grid
x=np.linspace(-4000, 4000, 4000)
y=x

[MeshX, MeshY]=np.meshgrid(x,y) 
[sy,sx]=np.shape(MeshX)
mid=int(np.fix(sx/2))

sigma1=400 # just the standard deviation for the gaussian profile i.e create a gaussian near field
Efield_amplitude=np.exp(-(MeshX**2+MeshY**2)/sigma1**2) # amplitude of the electric field. i.e. real component

E_initial_phase = np.zeros_like(Efield_amplitude) # assuming the initial beam has zero phase everywhere
E_initial = Efield_amplitude + 1j*E_initial_phase # full description of the electric field with real and imaginary (amplitude and phase)

I_initial=np.abs(E_initial)**2 # intensity
input_total = np.sum(I_initial)

### adding a mask on top of SLM ###
MeshR = np.sqrt(MeshX**2+MeshY**2)
radius_of_mask = 80
MeshR_mask = MeshR
MeshR_mask[MeshR<radius_of_mask] = 1
MeshR_mask[MeshR>radius_of_mask] = 0
### end of mask ###

### checkerboard
# PhaseMapX = np.zeros((4000, 4000), dtype=int)
# PhaseMapX[1::2, ::2] = 1
# PhaseMapX[::2, 1::2] = 1
###

PhaseMapX = signal.sawtooth(2 * np.pi * 50 * MeshX/np.max(MeshX)) # sawtooth pattern
# PhaseMapX = np.random.uniform(low=0, high=2*np.pi, size=(4000, 4000))
# PhaseMapX = np.exp(-(MeshR/100**2)**2)
# PhaseMapX = signal.sawtooth(2 * np.pi * 100 * MeshX/np.max(MeshX))*MeshR_mask
# PhaseMapX = np.sin(((2*np.pi/0.01))*MeshX) # sinusoidal grating
# PhaseMapX=MeshX/np.max(np.max(MeshX)) # linear ramp
# PhaseMapX = np.zeros_like(MeshX) # zero phase

am = np.pi/4 # amplitude

E_initial= E_initial*np.exp(PhaseMapX*am*1j)# mutiply the 2 phases together
SLM_phase = np.angle(E_initial)
SLM_phase_x = SLM_phase[mid, :]
E_fourier=np.fft.fftshift(np.fft.fft2(E_initial)) #  fourier transform is like looking at the far field
I_fourier=(np.abs(E_fourier))**2

###############
# spatial filter
###############
radius=20
xcenter=0
ycenter=0
SignMask=np.sign(1-np.sign((MeshX-xcenter)**2+(MeshY-ycenter)**2-radius**2))
th=np.linspace(0, 2*np.pi, 90) 
xunit=radius*np.cos(th)+xcenter
yunit=radius*np.sin(th)+ycenter
E_fourier_after_filter=E_fourier*SignMask
# E_fourier_after_filter = E_fourier
################


E_final=np.fft.ifft2(E_fourier_after_filter)
I_final=np.abs(E_final)**2
I_fourier_after_filter=(np.abs(E_fourier_after_filter))**2

E_final_phase =np.angle(E_final)
output_total = np.sum(I_final)

maxmax=np.max(np.max(I_fourier))
minmin=np.min(np.min(I_fourier))

fig, ax = plt.subplots(3, 2, figsize=(6, 8))
ax[0, 0].imshow(I_initial, vmin=0, vmax=1, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[0, 0].set_xlim(-500, 500)
ax[0, 0].set_ylim(-500, 500)
ax[0, 0].set_xlabel('x')
ax[0, 0].set_ylabel('y')
ax[0, 0].set_title('2D Intensity Profile')

ax[0, 1].imshow(SLM_phase, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto', cmap='RdBu')
ax[0, 1].set_title('2D Phase Structure SLM')
ax[0, 1].set_xlim(-500, 500)
ax[0, 1].set_ylim(-500, 500)

ax[1, 0].plot(x,SLM_phase_x,'-or')
ax[1, 0].set_xlim(-50, 50)
ax[1, 0].set_ylim(-4, 4)
ax[1, 0].set_title('Phase Lineout [radians]')

ax[1, 1].imshow(I_fourier, norm=colors.LogNorm(vmin=minmin, vmax=maxmax), extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[1, 1].plot(xunit, yunit,  c='k')
ax[1, 1].set_title('fourier plane no filter')
ax[1,1].set_xlim(-0, 500)
ax[1,1].set_ylim(-100, 100)

ax[2, 0].imshow(I_fourier_after_filter, norm=colors.LogNorm(vmin=minmin, vmax=maxmax), extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[2, 0].set_title('fourier plane after filter')
ax[2,0].set_xlim(-500, 500)
ax[2,0].set_ylim(-100, 100)

ax[2, 1].imshow(I_final, vmin=0, vmax=1, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[2, 1].set_title('2D Intensity Profile after filtering')
ax[2, 1].set_xlim(-500, 500)
ax[2, 1].set_ylim(-500, 500)
fig.tight_layout()
plt.savefig('intensity.pdf')
print(f'Energy throughput={np.round(output_total/input_total,2)*100}%')
plt.close()

fig2, ax2, =plt.subplots()
# ax2.plot(x, I_initial[mid, :], label='input')
# ax2.plot(x, I_final[mid, :], label='output')

ax2.plot(x, SLM_phase_x, label='SLM')
ax2.plot(x,(E_final_phase[mid, :]/np.mean(E_final_phase[mid, :]))-1, label='output')
ax2.legend()
ax2.set_xlim(-500, 500)
# ax2[1].legend()
# ax2[1].set_xlim(-50, 50)

# cax = ax2[2].imshow(E_final_phase, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto', cmap='RdBu')
# ax2[2].set_xlim(-4000, 4000)
# ax2[2].set_ylim(-4000, 4000)
# fig2.colorbar(cax, ax=ax2[2])
ax2.legend()
plt.savefig('phase.pdf')
plt.close()
