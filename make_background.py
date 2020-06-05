import numpy as np

class empty: pass


class Background():
    def __init__(self, zeropoint, pixel_scale, aperture_f_limit, aperture_significance, aperture_radius, verbose = False):

        '''
        :param zeropoint:               Observation instrument/filter AB magnitude zeropoint / Not needed for img.bkg in nJy
        :param pixel_scale:             Pixel scale (arcsec/pixel)
        :param aperture_f_limit:        Aperture flux limit (nJy) (The flux detected at aperture_significance)
        :param aperture_significance:   Aperture significance (S/N)
        :param aperture_radius:         Aperture radius (in arcsec)
        :param verbose:                 Verbose mode toggle
        '''



        self.pixel_scale = pixel_scale
        self.zeropoint = zeropoint # AB magnitude zeropoint # AB magnitude zeropoint
        self.nJy_to_es = 1E-9 * 10**(0.4*(self.zeropoint-8.9)) # conversion from nJy to e/s

        self.aperture = empty()
        self.aperture.flux_limit = aperture_f_limit
        self.aperture.radius = aperture_radius / self.pixel_scale      # aperture radius in pixels
        self.aperture.significance = aperture_significance
        self.aperture.noise = self.aperture.flux_limit/self.aperture.significance # nJy
        self.aperture.background = self.aperture.noise**2
        self.aperture.area = np.pi * self.aperture.radius**2
        self.aperture.noise_es = self.aperture.noise * self.nJy_to_es # convert from nJy to e/s

        self.pixel = empty()
        self.pixel.background = self.aperture.background/self.aperture.area
        self.pixel.noise = np.sqrt(self.pixel.background) # nJy
        self.pixel.noise_es = self.pixel.noise * self.nJy_to_es # convert from nJy to e/s

        if verbose:
            print('assumed aperture radius: {0:.2f} pix'.format(self.aperture.radius))
            print('noise in aperture: {0:.2f} nJy, {1:.4f} e/s'.format(self.aperture.noise, self.aperture.noise_es))
            print('noise in pixel: {0:.2f} nJy, {1:.4f} e/s'.format(self.pixel.noise, self.pixel.noise_es))
            print('zeropoint: {0}'.format(self.zeropoint))
            print('nJy_to_es: {0}'.format(self.nJy_to_es))


    def create_background_image(self, CutoutWidth):
        '''
        :param CutoutWidth:             Cutout image size in pixels

        returns:                        image object: img.bkg gives the background noise map
        '''

        img = empty()
        img.nJy_to_es = self.nJy_to_es
        img.pixel_scale = self.pixel_scale
        img.noise = self.pixel.noise * np.ones((CutoutWidth,CutoutWidth))
        img.noise_es = self.pixel.noise_es * np.ones((CutoutWidth, CutoutWidth))
        img.wht = 1./img.noise**2

        random_map = np.random.randn(*img.noise.shape)

        img.bkg = self.pixel.noise * random_map
        img.bkg_es = self.pixel.noise_es * random_map

        return img