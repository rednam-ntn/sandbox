def gen_yield(n):
    for idx, val in enumerate(n):
        if val % 2 == 0:
            yield idx


test_list = [1, 2, 3, 4, 5, 6]

gen_express = (
    idx
    for idx, val in enumerate(test_list)
    if val % 2 == 0
)

list_comp = (
    idx
    for idx, val in enumerate(test_list)
    if val % 2 == 0
)


if __name__ == "__main__":
    # for i in gen_yield(test_list):
    print(next(gen_yield(test_list)))
    print(next(gen_yield(test_list)))
    print(next(gen_yield(test_list)))
    print("".center(50, "~"))
    print(next(gen_express))
    print(next(gen_express))
    print(next(gen_express))
    print(next(gen_express))
    print("".center(50, "~"))
    print(next(list_comp))
    print(next(list_comp))
    print(next(list_comp))
    print(next(list_comp))
