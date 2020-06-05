import make_background

import numpy as np
import matplotlib.pyplot as plt


pixel_scale = 0.031             # arcsec/pixel
aperture_radius = 0.175         # aperture radius in arcsec
zeropoint = 25.946              # AB mag zeropoint  / This doesn't matter if only interested in the noise background in nJy
aperture_f_limit = 4.365        # aperture flux limit (nJy)

r = aperture_radius/pixel_scale # aperture radius in pixels


# Initialise background(s)
background_object = make_background.Background(zeropoint=zeropoint, pixel_scale=pixel_scale, aperture_f_limit=aperture_f_limit, aperture_significance=5, aperture_radius=aperture_radius, verbose = True)


# create background image object (cutoutwidth in pixels)
cutoutwidth = 1001
img = background_object.create_background_image(cutoutwidth)


'''img.bkg gives the background (random normally distributed) noise'''

sig = (img.bkg/img.noise) # gives the significance image (used here just for plotting)


plt.figure()
plt.imshow(sig, cmap='Greys', vmin=-5.0, vmax=5.0, origin='lower')
plt.xlabel('x / pix')
plt.ylabel('y / pix')
#plt.show()


# --------------------------

# Calculating flux in random apertures as check.

from photutils import aperture_photometry
from photutils import CircularAperture


N = 1000       # Number of apertures

# Random aperture positions
positions = [np.random.randint(0+int(np.ceil(r)), cutoutwidth-int(np.ceil(r)), N), np.random.randint(0+int(np.ceil(r)), cutoutwidth-int(np.ceil(r)), N)]

# Creating apertures
aperture = CircularAperture(positions, r=r)

aperture.plot(color='red', lw=1., alpha=0.5)

plt.show()


# Measuring photometry in the random apertures
phot_table = aperture_photometry(img.bkg, aperture, method='subpixel')
phot_table['aperture_sum'].info.format = '%.8g'

print('')
print('Printout of random aperture values (nJy)')

#print(phot_table)

aperture_sums = np.asarray(phot_table['aperture_sum'])

print(f'mean aperture flux = {np.mean(aperture_sums):.2f}, std = {np.std(aperture_sums):.2f}')


# plotting a normalised histogram of the aperture fluxes

import scipy.stats

x = np.linspace(-5, 5, 1000)
plt.hist(aperture_sums, bins=100, normed=True, range=[-5, 5])
plt.plot(x, scipy.stats.norm.pdf(x, 0, (aperture_f_limit/5)), 'r--')
plt.axvline(0, color='black')
plt.ylabel('PDF')
plt.xlabel('aperture flux (nJy)')
plt.show()