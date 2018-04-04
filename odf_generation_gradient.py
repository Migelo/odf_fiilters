#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import common

segment = np.loadtxt('./66.segment')
mask = (segment[:, 0] > 5000) & (segment[:, 0] < 6000)
segment = segment[mask]

sorted_segment = segment[np.argsort(segment[:, 1])]
sorted_segment[:, 0] = segment[0, 0]
sorted_segment[1:, 0] += np.cumsum(sorted_segment[:-1, 2])


def odf_integral(wavelength, opacity, dx, n=4):
    idx = [0]
    opacity = np.log10(opacity)

    dy = np.zeros(opacity.shape, np.float)
    dy[0:-1] = np.diff(opacity) / np.diff(wavelength)
    dy[-1] = (opacity[-1] - opacity[-2]) / (wavelength[-1] - wavelength[-2])

    integral = opacity * dy
    cum_sum_integral = np.cumsum(integral)
    sum_integral = integral.sum()

    for i in range(n - 1):
        idx.append(
            np.argwhere(cum_sum_integral < sum_integral / n * (i + 1))[0, 0]
            )
    idx.append(-1)
    return wavelength[idx]


f, ax = plt.subplots(10, figsize=(10, 20))
for i in range(2, 10):

    edges = odf_integral(sorted_segment[:, 0], sorted_segment[:, 1],
                         sorted_segment[:, 2],  n=i)
    ax[i - 2].plot(sorted_segment[:, 0], np.log10(sorted_segment[:, 1]),
                   label='sorted opacity')
    for item in edges:
        ax[i - 2].axvline(x=item)
    print((edges - edges[0]) / (edges[-1] - edges[0]))
