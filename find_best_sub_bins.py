# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

data = {}
sub_bins = sorted(np.loadtxt('sub_bin_list.txt.bckp', dtype=str))
results = np.genfromtxt('results.txt',
                        dtype=[('name', 'U10'), ('value', 'f8')],
                        usecols=np.arange(2))
for item in sub_bins:
    if '2b_{}'.format(item[8:]) not in results['name']:
        print(item)
        continue
argsort = np.argsort(results['value'])
results = results[argsort]

sub_bin_values = []
for item in results['name']:
    item = 'sub_bins/sub_bin{}'.format(item[2:])  # sub_bin_4_72
    sub_bin_values.append(np.loadtxt(item))


colors = ['C{}'.format(x) for x in range(9)]
f, ax = plt.subplots(1, figsize=(10, 10 / 1.61))
for i, item in enumerate(sub_bin_values[::-1]):
    for j, value in enumerate(item[:-1]):
        ax.fill_between([i, i + 1], value, item[j + 1], color=colors[j])
ax2 = ax.twinx()
ax2.plot(range(len(sub_bin_values)), results['value'][::-1], c='k')

# find best for each number of sub-bins
temp = []
for i in range(5, 7):
    j = 0
    for item in results[::-1]:
        if item['name'][3] == '{}'.format(i):
#            temp[item['name']] = item['value']
            temp.append(item)
            print(item)
            j += 1
            if j > 10:
                break

temp = np.array(temp, dtype=[('name', 'U10'), ('value', 'f8')])

f, ax = plt.subplots(1, figsize=(10, 10 / 1.61))
for i, item in enumerate(temp[::-1]):
    for j, value in enumerate(item[:-1]):
        ax.fill_between([i, i + 1], value, item[j + 1], color=colors[j])
ax2 = ax.twinx()
ax2.plot(range(len(sub_bin_values)), results['value'][::-1], c='k')
