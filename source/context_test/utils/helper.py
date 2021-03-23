#%%
# from .process import process_2
# EQUAL the func below
# from utils.process import process_2


def helper_1():
    print("HELLO 1")


#%%
x1 = []
x2 = []
y1 = [1, 2, 3]
y2 = [4, 5, 6]

for x, y in [x1, y1], [x2, y2]:
    print(x, y, "\n")
    for i in y:
        if i % 2 == 0:
            x.append(i)

print(x1)
print(x2)
# %%
"\n".join(["1", "", "2"])

# %%
