import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Separate list of sub-bins.')
parser.add_argument('list', type=str, help='Whole list filename.')
parser.add_argument('n', type=int, help='Number of parts.')
args = parser.parse_args()
args.n += 1

data = np.loadtxt(args.list, dtype=str)

idx = np.linspace(0, len(data), num=args.n).astype(int)
for i, item in enumerate(idx[:-1]):
    np.savetxt("sub_bin_list_{}.txt".format(i), data[item:idx[i + 1]], fmt="%s")
