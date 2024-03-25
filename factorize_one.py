import time


def factorize(*number):
    start_time = time.time()
    result = [None for i in range(len(number))]
    for i in range(len(number)):
        num = number[i]
        res = {1, num}
        for divisor in range(2, num // 2 + 1):
            if num % divisor == 0:
                res.add(divisor)
        result[i] = sorted(res)
    def_time = time.time() - start_time
    print(f"Время исполнения: {def_time} сек")
    return result


a, b, c, d = factorize(128, 255, 99999, 10651060)

assert a == [1, 2, 4, 8, 16, 32, 64, 128]
assert b == [1, 3, 5, 15, 17, 51, 85, 255]
assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
assert d == [
    1,
    2,
    4,
    5,
    7,
    10,
    14,
    20,
    28,
    35,
    70,
    140,
    76079,
    152158,
    304316,
    380395,
    532553,
    760790,
    1065106,
    1521580,
    2130212,
    2662765,
    5325530,
    10651060,
]


# print(
#     factorize(
#         128,
#         255,
#         99999,
#         10651060,
#         345642,
#         234532,
#         7543324,
#         10651060,
#         3456421,
#         7890432,
#         3423432,
#     )
# )
