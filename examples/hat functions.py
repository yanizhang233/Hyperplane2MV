
'''
g1 hat function
g2 two hats
g3 four hats
gs 2^(s-1) hats

apply the hyperplane method to g1, ..., g5

s is the fold of self-composition
'''
import numpy as np
import pandas as pd
from hyperplane2MV import hyperplane2MV
from matplotlib import pyplot as plt
from NN2MV import NN2MV
from schauderhat2mv import schauderhat2mv
from helper import calc_length_symbol, calc_length_symbol_bracket

sStart = 1
sEnd = 5
slist = list(range(sStart, sEnd+1, 1))


# method 1: hyperplane method
mvs_hyperplane = [None]*len(slist)
mvps_hyperplane = [None]*len(slist)

length_hyperplane = [0] * len(slist)
lengthp_hyperplane = [0] * len(slist)

for s in range(sStart, sEnd+1, 1):
    xcords = np.linspace(0, 1, 2**s+1)
    ycords = [0,1] * (2**(s-1))
    ycords.append(0)
    print(f"s: {s}")
    test = hyperplane2MV(xcords, ycords)
    test.extract(method='aguzzoli')
    mvs_hyperplane[s-1] = test.overallMV
    mvps_hyperplane[s-1] = test.overallMVp
    length_hyperplane[s-1] = mvs_hyperplane[s-1].count('x')
    lengthp_hyperplane[s-1] = mvps_hyperplane[s-1].count('p')


