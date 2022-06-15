#%%
from itertools import combinations

list_a = ['JAPAN', 'NAGOYA', 'PORT', 'VUNG', 'VIETNAM', 'TAU']
list_b = ['ORIGIN', 'VIET', 'NAM']


#%%
list(combinations(list_b, 2))

#%%
for word in combinations(list_b, 1):
    print(word)

#%%
for i in range(2,3):
    print(i)

#%%
a = []
a += ["b", "c"]
print(a)

#%%
