import random

import pytest

from algorithms import (
    Node,
    bfs_level_order,
    dfs_preorder_iter,
    fib,
    fib_iter,
    height,
    inorder,
    postorder,
    preorder,
    quicksort,
)


def test_quicksort_basic() -> None:
    assert quicksort([]) == []
    assert quicksort([1]) == [1]
    assert quicksort([3, 2, 1]) == [1, 2, 3]
    assert quicksort([2, 2, 1, 3, 2]) == [1, 2, 2, 2, 3]


def test_quicksort_random_and_pure() -> None:
    xs = [random.randint(-1000, 1000) for _ in range(1000)]
    copy = xs[:]
    assert quicksort(xs) == sorted(xs)
    assert xs == copy


def sample_tree() -> Node:
    return Node(4, Node(2, Node(1), Node(3)), Node(6, None, Node(7)))


def test_traversals() -> None:
    t = sample_tree()
    assert list(preorder(t)) == [4, 2, 1, 3, 6, 7]
    assert list(inorder(t)) == [1, 2, 3, 4, 6, 7]
    assert list(postorder(t)) == [1, 3, 2, 7, 6, 4]
    assert bfs_level_order(t) == [4, 2, 6, 1, 3, 7]
    assert dfs_preorder_iter(t) == [4, 2, 1, 3, 6, 7]
    assert height(t) == 3
    assert bfs_level_order(None) == [] and list(inorder(None)) == []


def test_fib() -> None:
    assert [fib(i) for i in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert all(fib(n) == fib_iter(n) for n in range(80))
    fib.cache_clear()
    assert fib(0) == 0
    with pytest.raises(ValueError):
        fib_iter(-1)
