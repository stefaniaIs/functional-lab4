import math
import random
import sys

import pytest

from algorithms import fib_iter
from euclid import (
    ext_gcd,
    ext_gcd_iter,
    gcd_depth,
    gcd_iter,
    gcd_memo,
    gcd_rec,
    gcd_tramp,
    lcm,
    mod_inverse,
    trampoline,
)

RNG = random.Random(42)
PAIRS = [
    (RNG.randint(-(10**6), 10**6), RNG.randint(-(10**6), 10**6)) for _ in range(300)
]


@pytest.mark.parametrize(
    ("a", "b", "g"),
    [(252, 105, 21), (17, 5, 1), (0, 7, 7), (7, 0, 7), (0, 0, 0), (-12, 18, 6)],
)
def test_gcd_known(a: int, b: int, g: int) -> None:
    assert gcd_rec(a, b) == gcd_iter(a, b) == gcd_memo(a, b) == g


def test_gcd_matches_math() -> None:
    for a, b in PAIRS:
        assert gcd_rec(a, b) == gcd_iter(a, b) == math.gcd(a, b)


def test_gcd_properties() -> None:
    for a, b in PAIRS:
        g = gcd_rec(a, b)
        assert gcd_rec(a, b) == gcd_rec(b, a)  # симетрія
        if g:
            assert a % g == 0 and b % g == 0  # g ділить обидва
            assert gcd_rec(a // g, b // g) == 1  # частки взаємно прості
        assert gcd_rec(a, gcd_rec(b, 30)) == gcd_rec(gcd_rec(a, b), 30)  # асоціат.


def test_ext_gcd_bezout() -> None:
    for a, b in PAIRS + [(240, 46), (0, 5), (5, 0), (-7, 3)]:
        g, x, y = ext_gcd(a, b)
        assert g == math.gcd(a, b)
        assert a * x + b * y == g
        g2, x2, y2 = ext_gcd_iter(a, b)
        assert g2 == g and a * x2 + b * y2 == g2


def test_lcm_and_inverse() -> None:
    assert lcm(4, 6) == 12 and lcm(0, 5) == 0
    assert (3 * mod_inverse(3, 11)) % 11 == 1
    with pytest.raises(ValueError):
        mod_inverse(4, 8)


def test_depth_worst_case_fibonacci() -> None:
    # для сусідніх чисел Фібоначчі глибина максимальна і росте лінійно від n
    assert gcd_depth(fib_iter(20), fib_iter(19)) == 18
    assert gcd_depth(fib_iter(20), fib_iter(19)) > gcd_depth(10**6, 10)
    assert gcd_depth(5, 0) == 0


def test_depth_is_logarithmic() -> None:
    a, b = fib_iter(500), fib_iter(499)  # величезні числа (~100 цифр)
    depth = gcd_depth(a, b)
    assert depth < sys.getrecursionlimit()
    assert depth <= 5 * len(str(min(a, b)))  # теорема Ламе


def test_cache_info_and_clear() -> None:
    gcd_memo.cache_clear()
    gcd_memo(48, 18)
    misses = gcd_memo.cache_info().misses
    gcd_memo(48, 18)
    assert gcd_memo.cache_info().hits >= 1
    assert gcd_memo.cache_info().misses == misses
    gcd_memo.cache_clear()
    assert gcd_memo.cache_info().currsize == 0


def test_trampoline_matches() -> None:
    for a, b in PAIRS[:50]:
        assert trampoline(gcd_tramp, a, b) == math.gcd(a, b)
