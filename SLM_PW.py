##############################
# code to look at the effect of an SLM on the amplitude and phase of a beam
# originally written by Jeroen, converted by Aodhan
##############################

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from scipy import signal\
# setup the grid
x=np.linspace(-4000, 4000, 8000)
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

PhaseMapX = signal.sawtooth(2 * np.pi * 100 * MeshX/np.max(MeshX)) # sawtooth pattern
# PhaseMapX = ((np.sin(((2*3np.pi/0.05))*MeshX))) # sinusoidal grating
# PhaseMapX=MeshX/np.max(np.max(MeshX)) # linear ramp
# PhaseMapX = np.zeros_like(MeshX) # zero phase
# PhaseMapX = np.exp(-((MeshX**2+MeshY**2)/100**2)**2)

am = np.pi # amplitude
E_initial= E_initial*np.exp(PhaseMapX*am*1j)# mutiply the 2 phases together
# E_initial = np.multiply(E_initial, np.exp(PhaseMapX*am*1j))
E_fourier=np.fft.fft2(E_initial) #  fourier transform is like looking at the far field
E_fourier=np.fft.fftshift(E_fourier)
I_fourier=(np.abs(E_fourier))**2

###############
# spatial filter
###############
radius=50
xcenter=200
ycenter=0
SignMask=np.sign(1-np.sign((MeshX-xcenter)**2+(MeshY-ycenter)**2-radius**2))
th=np.linspace(0, 2*np.pi, 90) 
xunit=radius*np.cos(th)+xcenter
yunit=radius*np.sin(th)+ycenter
E_fourier_after_filter=E_fourier*SignMask
################


E_final=np.fft.ifft2(E_fourier_after_filter)
I_final=np.abs(E_final)**2
I_fourier_after_filter=(np.abs(E_fourier_after_filter))**2

output_total = np.sum(I_final)

maxmax=np.max(np.max(I_fourier))
minmin=np.min(np.min(I_fourier))



fig, ax = plt.subplots(3, 2, figsize=(6, 8))
ax[0, 0].imshow(I_initial, vmin = 0, vmax = 255, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[0, 0].set_xlim(-500, 500)
ax[0, 0].set_ylim(-500, 500)
ax[0, 0].set_xlabel('x')
ax[0, 0].set_ylabel('y')
ax[0, 0].set_title('2D Intensity Profile')

ax[0, 1].imshow(np.angle(E_initial), extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[0, 1].set_title('2D Phase Structure SLM')
ax[0, 1].set_xlim(-500, 500)
ax[0, 1].set_ylim(-500, 500)

ax[1, 0].plot(x,np.angle(E_initial[mid, :]),'-or')
ax[1, 0].set_xlim(-50, 50)
ax[1, 0].set_ylim(-4, 4)
ax[1, 0].set_title('Phase Lineout [radians]')

ax[1, 1].imshow(I_fourier, vmin=minmin, vmax=maxmax, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[1, 1].plot(xunit, yunit,  c='k')
ax[1, 1].set_title('fourier plane no filter')
ax[1,1].set_xlim(-0, 500)
ax[1,1].set_ylim(-100, 100)

ax[2, 0].imshow(I_fourier_after_filter, vmin=minmin, vmax=maxmax, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[2, 0].set_title('fourier plane after filter')
ax[2,0].set_xlim(-500, 500)
ax[2,0].set_ylim(-100, 100)

ax[2, 1].imshow(I_final, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[2, 1].set_title('2D Intensity Profile after filtering')
ax[2, 1].set_xlim(-500, 500)
ax[2, 1].set_ylim(-500, 500)
fig.tight_layout()
plt.show()
print(f'Energy throughput={np.round(output_total/input_total,2)*100}%')



# plt.close()
# # plt.plot(I_initial[540, :])
# # plt.plot(I_final[540, :])
# # plt.plot(E_initial[540, :])
# plt.show()


























































