#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

filters = [['filtr_org', 'original'], ['filtr_wing', 'wingless + 0.1'],
           ['filtr_5354', '5300 - 5400 + 0.2']]
# filters = [['filtr_5354', '5300 - 5400 + 0.2']]
spectra = np.loadtxt('spectra')
spectra_bkp = spectra * 1.

f, ax = plt.subplots(2, figsize=(8, 8 / 1.61 * 2))
ax[1].set_xlabel('Wavelength [angstrom]')
ax[0].set_ylabel('Filter function value')
ax[0].set_title('Original filter values')
ax[1].set_title('Interpolated filter values')

for i, filtr in enumerate(filters):
    data = np.loadtxt(filtr[0])
    ax[0].plot(data[:, 0], data[:, 1] + i / 10, label=filtr[1])

    spectra = spectra_bkp * 1.
    wavelength_mask = (spectra[:, 0] >= data[0, 0]) & (spectra[:, 0] <= data[-1, 0])
    spectra = spectra[wavelength_mask]
    interp = interpolate.interp1d(data[:, 0], data[:, 1])
    tf_full = interp(spectra[:, 0])
    ax[1].plot(spectra[:, 0], tf_full + i / 10)


ax[0].legend(loc='best')
f.tight_layout()
plt.savefig('filters.jpg', bbox_inches='tight')
