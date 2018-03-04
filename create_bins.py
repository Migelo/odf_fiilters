import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Create bins based on min-max wavelength.')
parser.add_argument('suffix', type=str, help='Output filename suffix.')
parser.add_argument('-bn', type=int, default=1, help='Number of bins.')
args = parser.parse_args()

# load the file and extract the min and max values
data = np.loadtxt('01.segment_{}'.format(args.suffix))


if args.bn == 2:
    for j in np.arange(.02, 1., .02):
        midpoint = (data[-1, 0] - data[0, 0]) * j + data[0, 0]
        bins = [[data[0, 0], midpoint], [midpoint, data[-1, 0]]]
        np.savetxt('bins_2_{}'.format(int(j * 100)), bins)

elif args.bn == 1:
    bins = np.linspace(data[0, 0], data[-1, 0], 1 + args.bn)
    # bins = bins[1:-1]
    bins_list = []
    for i, item in enumerate(bins[:-1]):
        bins_list.append([item, bins[i + 1]])
    np.savetxt('bins_{}'.format(args.suffix), bins_list)
else:
    bins = np.array([data[0, 0], data[-1, 0]])
    np.savetxt('bins_{}'.format(args.suffix), bins.reshape(1, bins.shape[0]))

