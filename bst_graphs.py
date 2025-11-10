
import sys
import unittest
from typing import *
from dataclasses import dataclass
import math
import matplotlib.pyplot as plt
from bst import BinarySearchTree, height, insert
import numpy as np
import random
import time

sys.setrecursionlimit(10**6)

from bst import *

TREES_PER_RUN: int = 10000 


# helper functions to generate trees

def default_comes_before(a: Any, b: Any) -> bool:
    return a < b

def random_tree(n: int) -> BinarySearchTree:
    bst = BinarySearchTree(None, default_comes_before)
    for _ in range(n):
        bst = insert(bst, random.random())  # random float in [0,1)
    return bst

def average_height(N: int, runs: int = TREES_PER_RUN) -> float:
    total = 0
    for _ in range(runs):
        bst = random_tree(N)
        total += height(bst.tree)
    return total / runs if runs > 0 else float('nan')

def time_insert_into_random_tree(N: int, runs: int = TREES_PER_RUN) -> float:
    # Purpose: return average time (in seconds) to insert one random value into a random tree of size N.

    total_time = 0.0
    for _ in range(runs):
        bst = random_tree(N)
        val = random.random()
        t0 = time.perf_counter()
        _ = insert(bst, val)
        t1 = time.perf_counter()
        total_time += (t1 - t0)
    return total_time / runs if runs > 0 else float('nan')


def choose_n_max_for_height(target_low: float = 1.5, target_high: float = 2.5) -> int:
    # Purpose: find n_max such that creating TREES_PER_RUN random trees of size n_max and computing their heights takes ~1.5-2.5 seconds.
    candidates = [50, 100, 200, 400, 800, 1200, 1600, 2000]
    for n in candidates:
        t0 = time.perf_counter()
        for _ in range(TREES_PER_RUN):
            bst = random_tree(n)
            _ = height(bst.tree)
        t1 = time.perf_counter()
        elapsed = t1 - t0
        if target_low <= elapsed <= target_high:
            return n
    return candidates[-1]


def choose_n_max_for_insert(target_low: float = 1.5, target_high: float = 2.5) -> int:
    # Purpose: find n_max such that generating TREES_PER_RUN trees and inserting one value takes ~1.5-2.5 seconds.
    candidates = [50, 100, 200, 400, 800, 1200, 1600, 2000]
    for n in candidates:
        t0 = time.perf_counter()
        for _ in range(TREES_PER_RUN):
            bst = random_tree(n)
            val = random.random()
            _ = insert(bst, val)
        t1 = time.perf_counter()
        elapsed = t1 - t0
        if target_low <= elapsed <= target_high:
            return n
    return candidates[-1]


def graph_average_height(n_max: Optional[int] = None) -> None:
    if n_max is None:
        n_max = choose_n_max_for_height()
    Ns = np.linspace(0, n_max, 50, dtype=int)
    y_vals = [average_height(int(N)) for N in Ns]

    x_np = np.array(Ns, dtype=float)
    y_np = np.array(y_vals, dtype=float)

    plt.plot(x_np, y_np, label='Average BST Height')
    plt.xlabel("N (number of nodes)")
    plt.ylabel("Average height (edges)")
    plt.title("Average Height of Random BST vs N")
    plt.grid(True)
    plt.legend()
    plt.show()


def graph_insert_time(n_max: Optional[int] = None) -> None:
    if n_max is None:
        n_max = choose_n_max_for_insert()
    Ns = np.linspace(0, n_max, 50, dtype=int)
    y_vals = [time_insert_into_random_tree(int(N)) for N in Ns]

    x_np = np.array(Ns, dtype=float)
    y_np = np.array(y_vals, dtype=float)

    plt.plot(x_np, y_np, label='Insert One Value (seconds)')
    plt.xlabel("N (tree size)")
    plt.ylabel("Average time (s)")
    plt.title("Time to Insert a Value into Random BST vs N")
    plt.grid(True)
    plt.legend()
    plt.show()


if (__name__ == '__main__'):
    # example:
    # graph_average_height()
    # graph_insert_time()
    pass

