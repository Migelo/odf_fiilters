import numpy as np
from glob import glob
import scipy.interpolate as interp
from multiprocessing import Pool
import argparse

parser = argparse.ArgumentParser(description='Apply filter function \
                                 to opacities (segment files).')
# parser.add_argument('strech', type=bool, default=False, help='Strech bins to
# their original size.')
parser.add_argument('filter', type=str, help='Filter function filename.')
parser.add_argument('suffix', type=str, help='Output filename suffix.')
args = parser.parse_args()

file_list = sorted(glob("*.segment"))

# load filter transmission curve
b = np.loadtxt(args.filter)

# create an interpolation object for the ftc
cs = interp.interp1d(b[:, 0], b[:, 1])


def stromgen(f):
    print(f)
    # load data
    data = np.loadtxt(f)

    # mask all data to the wavelength range of the filter transmission curve
    mask = (data[:, 0] > b[0, 0]) & (data[:, 0] < b[-1, 0])
    data = data[mask]
    original_interval_length = data[:, 2].sum()
    original_wavelengths = data[:, 0] * 1.

    # interpolate the filter transmission curve to match the grid of our data
    b_intrp = cs(data[:, 0])
    b_intrp[b_intrp < 0] = 0

    # modified_dlam = b_intrp * data[:, 2]
    # modified_dlam *= np.sum(data[mask][:, 2]) / np.sum(modified_dlam)
    # calculate modified delta lambda values while preserving the sum

    # apply the interpolated values to data[:, 2]
    data[:, 2] *= b_intrp

    start = data[0, 0] * 1.
    data[:, 0] = np.ones(data[:, 0].shape[0]) * start
    data[1:, 0] += np.cumsum(data[:, 2])[:-1]
    data[0, 0] = start

    stretch_factor = original_interval_length / (data[-1, 0] - data[0, 0])
    data[:, 2] = data[:, 2] * stretch_factor
    data[:, 0] = original_wavelengths

    np.savetxt("{}.segment_{}".format(f.split('.')[0], args.suffix), data)
    return stretch_factor


p = Pool(36)
stretch_factors = p.map(stromgen, file_list)

np.savetxt("stretch_factor_{}".format(args.suffix), [stretch_factors[0]])
