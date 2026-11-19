"""Варіант 3. Алгоритм Евкліда: рекурсивний, ітеративний, розширений.

База рекурсії:  gcd(a, 0) = |a|
Крок рекурсії:  gcd(a, b) = gcd(b, a mod b)
"""

from __future__ import annotations

from collections.abc import Callable
from functools import cache
from typing import TypeVar, Union

T = TypeVar("T")


def gcd_rec(a: int, b: int) -> int:
    if b == 0:  # база
        return abs(a)
    return gcd_rec(b, a % b)  # хвостовий виклик, але TCO у CPython немає


def gcd_iter(a: int, b: int) -> int:
    """Ітеративна альтернатива: стек не росте взагалі."""
    while b:
        a, b = b, a % b
    return abs(a)


@cache
def gcd_memo(a: int, b: int) -> int:
    """Мемоізована версія - корисна, якщо ті самі пари запитуються багато разів."""
    return abs(a) if b == 0 else gcd_memo(b, a % b)


def gcd_depth(a: int, b: int) -> int:
    """Кількість рекурсивних кроків (глибина стеку) для пари (a, b)."""
    return 0 if b == 0 else 1 + gcd_depth(b, a % b)


def ext_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Розширений Евклід: повертає (g, x, y) такі, що a*x + b*y = g = gcd(a, b).

    База: ext_gcd(a, 0) = (a, 1, 0)
    Крок: якщо (g, x1, y1) = ext_gcd(b, a mod b), то x = y1, y = x1 - (a // b) * y1
    """
    if b == 0:
        return (abs(a), 1 if a >= 0 else -1, 0)
    g, x1, y1 = ext_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def ext_gcd_iter(a: int, b: int) -> tuple[int, int, int]:
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y
    if old_r < 0:
        return -old_r, -old_x, -old_y
    return old_r, old_x, old_y


def lcm(a: int, b: int) -> int:
    return 0 if a == 0 or b == 0 else abs(a * b) // gcd_rec(a, b)


def mod_inverse(a: int, m: int) -> int:
    """Обернений елемент за модулем через розширений Евклід."""
    g, x, _ = ext_gcd(a, m)
    if g != 1:
        raise ValueError(f"{a} has no inverse modulo {m}")
    return x % m


# --- трамплін: моделювання TCO -------------------------------------------------
Thunk = Callable[[], "Bounce[T]"]
Bounce = Union[T, Callable[[], "Bounce[T]"]]  # noqa: UP007 (рекурсивний alias)


def trampoline(fn: Callable[..., Bounce[T]], *args: int) -> T:
    """Виконує «наступні кроки» у циклі, тож стек не росте."""
    result = fn(*args)
    while callable(result):
        result = result()
    return result


def gcd_tramp(a: int, b: int) -> Bounce[int]:
    if b == 0:
        return abs(a)
    return lambda: gcd_tramp(b, a % b)
