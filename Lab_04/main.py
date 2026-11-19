"""Демо + порівняння глибини рекурсії та часу."""

from __future__ import annotations

import sys
from collections.abc import Callable
from functools import partial
from timeit import timeit

from algorithms import fib, fib_iter, fib_naive
from euclid import (
    ext_gcd,
    gcd_depth,
    gcd_iter,
    gcd_memo,
    gcd_rec,
    gcd_tramp,
    trampoline,
)


def main() -> None:
    print("Ліміт рекурсії CPython:", sys.getrecursionlimit())
    print("gcd(252, 105) =", gcd_rec(252, 105))
    g, x, y = ext_gcd(240, 46)
    print(f"ext_gcd(240, 46) = {g}; 240*{x} + 46*{y} = {240 * x + 46 * y}")

    print("\nГлибина рекурсії gcd для різних пар:")
    pairs = [
        (10**6, 10),
        (1071, 462),
        (2**40, 3**25),
        (fib(30), fib(29)),
        (fib(90), fib(89)),
    ]
    for a, b in pairs:
        print(f"  gcd({a}, {b}) = {gcd_rec(a, b):<6} глибина = {gcd_depth(a, b)}")
    print("  (сусідні числа Фібоначчі - найгірший випадок, теорема Ламе)")

    print("\nЧас (10000 викликів на пару fib(90), fib(89)):")
    a, b = fib(90), fib(89)
    impls: list[tuple[str, Callable[[int, int], int]]] = [
        ("rec", gcd_rec),
        ("iter", gcd_iter),
        ("memo", gcd_memo),
    ]
    for name, fn in impls:
        t = timeit(partial(fn, a, b), number=10_000)
        print(f"  {name:<5} {t * 1000:7.2f} ms")
    t = timeit(lambda: trampoline(gcd_tramp, a, b), number=10_000)
    print(f"  tramp {t * 1000:7.2f} ms")
    print("  gcd_memo.cache_info():", gcd_memo.cache_info())

    print("\nФібоначчі n=25:")
    print(f"  naive {timeit(lambda: fib_naive(25), number=1) * 1000:8.2f} ms")
    fib.cache_clear()
    print(f"  memo  {timeit(lambda: fib(25), number=1) * 1000:8.4f} ms")
    print(f"  iter  {timeit(lambda: fib_iter(25), number=1) * 1000:8.4f} ms")


if __name__ == "__main__":
    main()
