def pow(n: int) -> int:
    return n ** 2


def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def factorial_(n: int) -> int:
    res = 1
    for i in range(2, n + 1):
        res *= i
    return res
