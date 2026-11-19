"""Базова частина ЛР4: quicksort, обходи дерева, Фібоначчі з мемоізацією."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from functools import cache
from random import choice


def quicksort(xs: Sequence[int]) -> list[int]:
    """Чистий 3-шляховий quicksort з випадковим pivot (вхід не змінюється)."""
    if len(xs) <= 1:
        return list(xs)
    p = choice(xs)
    left = [x for x in xs if x < p]
    mid = [x for x in xs if x == p]
    right = [x for x in xs if x > p]
    return quicksort(left) + mid + quicksort(right)


@dataclass(frozen=True, slots=True)
class Node:
    key: int
    left: Node | None = None
    right: Node | None = None


def preorder(t: Node | None) -> Iterator[int]:
    if t is None:
        return
    yield t.key
    yield from preorder(t.left)
    yield from preorder(t.right)


def inorder(t: Node | None) -> Iterator[int]:
    if t is None:
        return
    yield from inorder(t.left)
    yield t.key
    yield from inorder(t.right)


def postorder(t: Node | None) -> Iterator[int]:
    if t is None:
        return
    yield from postorder(t.left)
    yield from postorder(t.right)
    yield t.key


def bfs_level_order(t: Node | None) -> list[int]:
    if t is None:
        return []
    q, out = deque([t]), []
    while q:
        n = q.popleft()
        out.append(n.key)
        q.extend(c for c in (n.left, n.right) if c is not None)
    return out


def dfs_preorder_iter(t: Node | None) -> list[int]:
    stack, out = ([t] if t else []), []
    while stack:
        n = stack.pop()
        out.append(n.key)
        stack.extend(c for c in (n.right, n.left) if c is not None)
    return out


def height(t: Node | None) -> int:
    return 0 if t is None else 1 + max(height(t.left), height(t.right))


@cache
def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def fib_naive(n: int) -> int:
    return n if n < 2 else fib_naive(n - 1) + fib_naive(n - 2)


def fib_iter(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
