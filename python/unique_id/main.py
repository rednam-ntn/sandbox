#%%
import string
import uuid
import random
from time import time
from tqdm import tqdm


def truncated_uuid1_str():
    return str(uuid.uuid1())[:8]


def truncated_uuid1():
    return f"{str(uuid.uuid1())[:8]}"


def test_collisions(fun):
    out = set()
    count = 0
    begin = time()
    for _ in tqdm(range(10**6)):
        new = fun()
        if new in out:
            count += 1
        else:
            out.add(new)
    
    print(f"\n{count:<5}", time() - begin)


test_collisions(truncated_uuid1_str)
test_collisions(truncated_uuid1)

# %%
