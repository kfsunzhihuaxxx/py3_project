from typing import List


def fib():
    current, nxt = 0, 1
    while True:
        current, nxt = nxt, current + nxt
        yield current

# 1,1,2,3,5,8,13,21,37...
# TODO:Try it with generators!

result = fib()

for n in result:
    print(n, end=',')
    if n > 100000:
        break


