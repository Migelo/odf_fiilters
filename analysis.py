# -*- coding: utf-8 -*-
import numpy as np
import argparse
from multiprocessing import Pool
# import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Calculate errors.')
parser.add_argument('suffix', type=str, nargs='+', help='Filename(s).')
parser.add_argument('-nb', type=str, help='Number of bins.')
parser.add_argument('--nproc', type=int, default=20, help='Number of cpus.')
parser.add_argument('--outfile', type=str, default='results.txt',
                    help='Output filename.')
args = parser.parse_args()

# load all files
detailed_spectra = np.load('spectra_transmitted.npy')


def compare(filename):
    if args.nb == '2b':
        bins = np.loadtxt('bins_cut_1', ndmin=2)
        odf_spectra = np.load('{}'.format(filename))
        filtr = np.loadtxt('filtr_cut_1')
    elif args.nb == '2':
        bins = np.loadtxt('bins_{}'.format(args.suffix), ndmin=2)
        odf_spectra = np.loadtxt('odf_spectra/odf_spectra_{}'.format(args.suffix))
        filtr = np.loadtxt('filtr_cut_1')
    elif args.nb == '1':
        bins = np.loadtxt('bins_{}'.format(args.suffix), ndmin=2)
        odf_spectra = np.loadtxt('odf_spectra/odf_spectra_{}'.format(args.suffix))
        filtr = np.loadtxt('filtr_{}'.format(args.suffix))
    else:
        odf_spectra = np.loadtxt('odf_spectra_{}'.format(args.suffix))
        filtr = np.loadtxt('filtr_{}'.format(args.suffix))
        bins = np.loadtxt('bins_{}'.format(args.suffix), ndmin=2)


    # create a mask to only consider wavelength interval from the bins
    # as the ODF files get automatically extended for numerical reasons
    # mask = (filtr[-1, 0] > detailed_spectra[:, 0]) & (filtr[0, 0] < detailed_spectra[:, 0])
    odf_mask = (bins[0, 0] < odf_spectra[:, 0]) & (bins[-1, 1] > odf_spectra[:, 0])
    # if args.nb != '1' and args.nb != '2b':
    #     detailed_spectra = detailed_spectra[mask]

    odf_spectra = odf_spectra[odf_mask]

    # calculate original interval length from the filter functions
    # orig_interval = filtr[-1, 0] - filtr[0, 0]

    # using the upper result calculate the stretch factor
    if args.nb == '2b':
        stretch_factor = np.loadtxt('stretch_factor_cut_1')
    else:
        stretch_factor = np.loadtxt('stretch_factor_{}'.format(args.suffix))

    # calculate integrals
    detailed_integral = np.sum(np.diff(detailed_spectra[:, 0]) * detailed_spectra[:-1, 1])
    odf_integral = np.sum(np.diff(odf_spectra[:, 0]) * odf_spectra[:-1, 1])

    # plt.plot(detailed_spectra[:, 0], detailed_spectra[:, 1])
    # plt.plot(odf_spectra[:, 0], odf_spectra[:, 1])
    # plt.show()

    print('stretch_factor: {}'.format(stretch_factor))

    print('ODF / stretch_factor / detailed for {}: {}'
          .format(filename.split('/')[-1][15:],
                  odf_integral / stretch_factor / detailed_integral))
    return('{} {}\n'.format(filename[:-4].split('/')[-1][15:],
                          odf_integral / stretch_factor / detailed_integral))

p = Pool(args.nproc)
results = p.map(compare, args.suffix)

f = open(args.outfile, 'a+')
for result in results:
    # f.write('{} {}\n'.format(filename, odf_integral / stretch_factor /
    # detailed_integral))
    f.write(result)
f.close()
