##############################
# code to look at the effect of an SLM on the amplitude and phase of a beam
# originally written by Jeroen, converted by Aodhan
##############################

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors

x=np.arange(-500, 500) 
y=x

[MeshX, MeshY]=np.meshgrid(x,y) 
[sy,sx]=np.shape(MeshX)
mid=int(np.fix(sx/2))

sigma1=400
Efield_amplitude=np.exp(-(MeshX**2+MeshY**2)/sigma1**2) # amplitude of the electric field. i.e. real component

am=np.pi/6 # this the amplitude of the phase mask
ERaw_phase = np.zeros_like(Efield_amplitude) # assuming the initial beam has zero phase everywhere
ERaw = np.array(Efield_amplitude+ERaw_phase, dtype=complex) # full description of the electric field with real and imaginary. amplitude and phase
IRaw=np.real(ERaw)**2 # intensity
PhaseMapX=np.mod(np.fix(MeshX), 2) # creates a phase mask of alternating 0 and 1s due to add or even
PhaseMapY=np.mod(np.fix(MeshY), 2)

ERaw[mid:,mid:] = (ERaw[mid:,mid:])*np.exp(PhaseMapX[mid:,mid:]*am*1j)
ERaw[mid:,mid:] = (ERaw[mid:,mid:])*np.exp(PhaseMapY[mid:,mid:]*am*1j)
EFocusRaw=np.fft.fft2(ERaw)
EFocusRaw=np.fft.fftshift(EFocusRaw)
IFocusRaw=(np.abs(EFocusRaw))**2

fig, ax = plt.subplots(3, 2, figsize=(6, 8))
ax[0, 0].imshow(IRaw.T, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[0, 0].set_xlabel('x')
ax[0, 0].set_ylabel('y')
ax[0, 0].set_title('2D Intensity Profile')

ax[0, 1].imshow(np.angle(ERaw).T, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[0, 1].set_title('2D Phase Structure SLM')

ax[1, 0].plot(x,np.angle(ERaw[:, mid+1]),'-or')
ax[1, 0].set_xlim(-20, 20)
ax[1, 0].set_ylim(-4, 4)
ax[1, 0].set_title('Phase Lineout')

maxmax=np.max(np.max(IFocusRaw))
minmin=np.min(np.min(IFocusRaw))
ax[1, 1].imshow(IFocusRaw, norm=colors.LogNorm(vmin=minmin, vmax=maxmax), extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[1, 1].set_title('Intensity at Focus')

SignMask=np.sign(0.5-0.5*np.sign(MeshX**2+MeshY**2-(500/2)**2))
EFocusRawNew=EFocusRaw*SignMask

IFocusRawNew=(abs(EFocusRawNew))**2
maxmax=np.max(np.max(IFocusRawNew))
ax[2, 0].imshow(IFocusRawNew, norm=colors.LogNorm(vmin=1e-9*maxmax, vmax=maxmax), extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[2, 0].set_title('Intensity at Focus after Filter')

EFocusInv=np.fft.ifft2(EFocusRawNew)
IFocusInv=(np.abs(EFocusInv))**2
ax[2, 1].imshow(IFocusInv, extent=[x[0], x[-1], y[0], y[-1]], interpolation='nearest', origin='lower', aspect='auto')
ax[2,1].set_title('2D Intensity Profile after filtering')
fig.tight_layout()
plt.savefig('phase_mask.pdf')
plt.close()