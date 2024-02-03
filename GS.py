import numpy as np
from matplotlib import pyplot as plt
import numpy.fft as fft
from PIL import Image

### Define constants
w_i = 3.24*10**-3  # input waist
# w_i = 3.24*10**-3
w_o = 960*10**-6  # output waist
wavelength = 632*10**-9  # wavelength
SLM_h, SLM_w = 512, 512  # SLM resolution
SLM_pixelsize = 8*10**-6  # SLM pixel size
w = w_i/SLM_pixelsize  # w in the equation
F = 350*10**-3  # Fourier lens focal distance
p = wavelength*F/SLM_h/SLM_pixelsize  # pixel size in output plane
l = 2*w_o/p  # total diffraction order
c1 = l*np.pi/(4*SLM_h*w)
c2 = l*np.pi/(SLM_h*w)


def gs(img, target, initial_pm, max_iter):

    am_in = np.sqrt(img)
    am_fp = np.sqrt(target)
    E_in = am_in * np.exp(1j*initial_pm)
    E_fp = fft.fftshift(fft.fft2(fft.fftshift(E_in)))
    E_cor = am_fp * np.exp(1j * np.angle(E_fp))
    E_out = fft.fftshift(fft.ifft2(fft.fftshift(E_cor)))

    for ii in range(max_iter):
        E_in = am_in * np.exp(1j*np.angle(E_out))
        E_fp = fft.fftshift(fft.fft2(fft.fftshift(E_in)))
        E_cor = am_fp * np.exp(1j*np.angle(E_fp))
        E_out = fft.fftshift(fft.ifft2(fft.fftshift(E_cor)))

    pm = np.angle(E_out)
    pm = np.where(pm < 0, 2*np.pi+pm, pm)

    return pm


def rmse(result, target):
    return np.sqrt(np.sum(np.square(result-target))/np.sum(np.square(target)))

file = r'C:\Users\loasis\Documents\GitHub\SLM_PW\Tests\Diode\original.png'
image = np.array(Image.open(file))

x = np.linspace(-0.005, 0.005, 1600)
y = np.linspace(-0.005, 0.005, 1200)
X, Y = np.meshgrid(x, y)

x2 = np.linspace(-255, 256, 1600)
y2 = np.linspace(-255, 256, 1200)
X2, Y2 = np.meshgrid(x2, y2)

input_beam = np.exp(-2*(X**2+Y**2)/w_i**2)
output_beam = np.exp(-2*(X/w_o)**40-2*(Y/w_o)**40)

pm = gs(image, output_beam, 0.0025*(X2**2+Y2**2), 200)
pmN = pm/2/np.pi*255
# pmN = (pm+np.pi)/2/np.pi*255
E_f = fft.fftshift(fft.fft2(fft.fftshift(np.sqrt(image)*np.exp(pm * 1j))))
recovery = np.absolute(E_f)
recoveryN = recovery/np.amax(recovery)

fig = plt.figure()

ax1 = fig.add_subplot(221)
ax1.imshow(image, cmap='gray')

ax2 = fig.add_subplot(222)
ax2.imshow(output_beam*255, cmap='gray')

ax3 = fig.add_subplot(223)
ax3.imshow(pmN, cmap='gray')

ax4 = fig.add_subplot(224)
ax4.imshow(np.uint8(recoveryN*255), 'gray')

plt.show()

fig3 = plt.figure()
ax = fig3.add_subplot(111)
ax.imshow(pmN, cmap='gray')
ax.axis('off')
fig3.savefig('phasemap.png')

#
# fig2 = plt.figure()
# ax = fig2.add_subplot(111)
# ax.plot(x2, 255*recoveryN[256, :])
#
# fig2.show()

# rmse_list = []
#
# for i in np.arange(c1, c2, 0.0001):
#     pm = gs(input_beam, output_beam, 0.004 * (X2 ** 2 + Y2 ** 2), 100)
#     pmN = (pm + np.pi) / 2 / np.pi * 255
#     E_f = fft.fftshift(fft.fft2(fft.fftshift(np.sqrt(input_beam) * np.exp(pm * 1j))))
#     recovery = np.absolute(E_f)
#     recoveryN = recovery/np.amax(recovery)
#     rmse_list.append(rmse(recoveryN[220:300], output_beam[220:300]))
#
# fig2 = plt.figure()
# ax5 = fig2.add_subplot(111)
# ax5.plot(np.arange(c1, c2, 0.0001), rmse_list)
#
# plt.show()
#
# fig = plt.figure()
#
# ax1 = fig.add_subplot(221)
# ax1.imshow(input_beam*255, cmap='gray')
#
# ax2 = fig.add_subplot(222)
# ax2.imshow(output_beam*255, cmap='gray')
#
# ax3 = fig.add_subplot(223)
# ax3.imshow(pmN, cmap='gray')
#
# ax4 = fig.add_subplot(224)
# ax4.imshow(np.uint8(recoveryN*255), 'gray')
#
# plt.show()
#
# print()
