import numpy as np

filtr = np.loadtxt('filtr_org')

for i in np.arange(0, .2, .01):
    mask = filtr[:, 1] > i
    mask = np.argwhere(mask).flatten()
    np.savetxt('filtr_{}'.format(int(i * 100)), filtr[mask[0]:mask[-1]])
