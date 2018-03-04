import numpy as np
import matplotlib.pyplot as plt
import copy


def increment(array_inp, step):
    length = len(array_inp)
    if length < 2:
        ValueError()
        print("Argument list should have a length greater than 2.")
    array = list(array_inp)
    if array[-2] >= .95:
        array[-2] += .01
    elif array[-2] >= .9:
        array[-2] += .02
    else:
        array[-2] += step
    todo = True
    if array[-2] >= 1.:
        while todo:
            todo = False
            for i, item in enumerate(array[:-1]):
                if i == 0:
                    continue
                if item >= 1.:
                    todo = True
                    array[i] = 0
                    if i - 1 != -1:
                        if i - 1 != 0:
                            if array[i - 1] > .95:
                                array[i - 1] += .01
                            elif array[i - 1] > .90:
                                array[i - 1] += .02
                            else:
                                array[i - 1] += step
    return array


def my_diff(y):
    out = []
    for i, x in enumerate(y[:-1]):
        out.append(y[i + 1] - y[i])
    return out


def check_bin_size(x, diff):
    return True
    for i, item in enumerate(my_diff(x)[:-1]):
        if diff[i + 1] - item >= 0:
            return False
    return True


item = [0, 1]
end = []
dx = .04
initial = copy.copy(item)
#for i in range(int(1 / dx)**(len(item) - 2)):
for j in range(4):
    initial.insert(0, 0)
    item = copy.copy(initial)
    print("Number of possibilities: {}".format(int(28)**(len(item) - 2)))
    while not np.isclose(item[1], .99):
        if item not in end:
            bin_diff = my_diff(item)
            if not np.any(np.array(bin_diff) == 0):
                if check_bin_size(item, bin_diff):
                    end.append(item)
        item = increment(item, dx)
    print("After filtering: {}".format(len(end)))

np.save('end', end)

#colors = ['C{}'.format(x) for x in range(9)]
#f, ax = plt.subplots(1, figsize=(10, 10 / 1.61))
#for i, item in enumerate(end):
#    for j, value in enumerate(item[:-1]):
#        ax.fill_between([i, i + 1], value, item[j + 1], color=colors[j])
#





#length = []
#results = [[0, 0, 1 ]]
#for j in range(6):
#    end = []
#    for i in range(int(1 / .02)**(len(results[0]) - 2)):
#        results.append(increment(results[-1], .04))
#    for i, item in enumerate(results):
#        if item != item.sort() and item not in end:
#            if not np.any(np.diff(item) == 0):
#                if check_bin_size(item):
#                    end.append(item)
#    length.append(len(end))
#    results = [results[0]]
#    results[0].insert(0, 0)


