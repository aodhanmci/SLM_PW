import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
from scipy.special import jv

# Define the size of the SLM
SLMsize = 512
# Define the size of the beam
beamsize = 512

# Define the coordinates of the SLM and the beam
xSLM = np.linspace(-128, 128, SLMsize)
ySLM = np.linspace(-128, 128, SLMsize)
x, y = np.meshgrid(np.linspace(-128, 128, beamsize), np.linspace(-128, 128, beamsize))

# Define the parameters of the beam
beam_center = [0, 0]
beam_width = 100

# Generate a random phase pattern for the SLM
SLMphase = np.random.uniform(low=-np.pi, high=np.pi, size=(SLMsize, SLMsize))

def phase_function(xx, yy):
    grating_period = beam_width/2  # half the beam width
    k = 2*np.pi / 1
    # return np.exp(1j * k * (xx + yy) / grating_period)*np.random.uniform(low=-1, high=1, size=(SLMsize, SLMsize))

# SLMphase = phase_function(x, y).real

# Generate the beam
def gaussian_beam(x, y, x0, wx, hot_spot_width):
    r2 = (x**2 + y**2)/wx**2 
    hotspot = ((x-x0)**2 + y**2)/hot_spot_width**2
    return np.exp(-r2**2) + 1*np.exp(-hotspot)



beam = gaussian_beam(x, y, x0=50, wx=150, hot_spot_width=20)
energy = np.sum(beam**2)
# Define the function that calculates the Fourier transform of the SLM phase
def SLM_FT(phase):
    FT = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(phase)))
    return FT

# Define the function that calculates the Fourier transform of the beam
def beam_FT(beam):
    FT = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(beam)))
    return FT

# Calculate the Fourier transforms of the SLM phase and the beam
SLM_FT = SLM_FT(SLMphase)
beam_FT = beam_FT(beam)

# Multiply the Fourier transforms of the SLM phase and the beam
output_FT = np.multiply(SLM_FT, beam_FT)

# Calculate the inverse Fourier transform of the product
output = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(output_FT)))

# Calculate the amplitude of the output
output_amplitude = np.abs(output)
homogenized_energy = np.sum(output_amplitude**2)
homongenized_beam_normalised = output_amplitude*np.sqrt(energy/homogenized_energy)
# Display the output amplitude
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
ax1.imshow(beam, cmap='gray', extent=(xSLM[0], xSLM[-1], ySLM[0], ySLM[-1]), vmin=0, vmax=2)
ax1.set_title('input beam')
ax2.imshow(SLMphase, cmap='gray', extent=(xSLM[0], xSLM[-1], ySLM[0], ySLM[-1]))
ax2.set_title('phase_map')
ax3.imshow(homongenized_beam_normalised, extent=(xSLM[0], xSLM[-1], ySLM[0], ySLM[-1]), cmap='gray', vmin=0, vmax=2)
ax3.set_title('output beam')
ax4.plot(xSLM, beam[int(SLMsize/2), :], label='input')
ax4.plot(xSLM, homongenized_beam_normalised[int(SLMsize/2), :], label='output')
ax4.set_ylim(0, 2)
ax4.set_title('profiles')
fig.tight_layout()
plt.show()

print(energy)
print(np.sum(homogenized_energy))
print(np.sum(homongenized_beam_normalised**2))
