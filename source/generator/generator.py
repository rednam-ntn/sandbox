def numberGenerator(n):
    # if n < 20:
    number = 0
    while number < n:
        yield number
        number += 1
    # else:
    #     return

def gen():
    i = 1
    while True:
        i += 1
        x = yield i
        print(f"x:{x}, i:{i}")

m = gen()
# m
next(m)
next(m)
# m.send(4)
# print((another_gen().__next__()))

# print(next(another_gen()))
# another_gen().send("ABC")

# gen = numberGenerator(50)

# print(gen.__iter__())
# for n in gen:
#     print(n)