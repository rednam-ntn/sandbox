import numpy as np
import pysnooper


@pysnooper.snoop()
def getDistance(A, B):
    newA = np.copy(A)
    newB = np.copy(B)
    if len(newA.shape) != 1:
        newA = A.flatten()
    if len(newB.shape) != 1:
        newB = B.flatten()
    if newA.shape == newB.shape:
        return np.linalg.norm(newA - newB) / len(newA)
    else:
        return None


A = np.arange(0, 100, 0.2)
B = np.arange(0, 200, 0.4)
getDistance(A, B)

#%%
import numpy as np
import random
import math

def np_linalgNorm(x):
    return np.linalg.norm(x)

def linalgNorm(x):
    subPower = np.power(x,2)
    return math.sqrt(np.sum(subPower))

#%%
for __ in range(5):
    dump_x = random.randrange(1, 10000)
    dump_y = random.randrange(1, 10000)
    dump_array = np.random.normal(size=[dump_x, dump_y])
    result = linalgNorm(dump_array)
    np_result = np_linalgNorm(dump_array)
    if round(np_result, 5) != round(result, 5):
        print("np_result:", np_result)
        print("result:", result)

#%%
