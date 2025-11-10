
import sys
import unittest
from typing import *
from dataclasses import dataclass

sys.setrecursionlimit(10**6)


BinTree: TypeAlias = Optional["Node"]


@dataclass(frozen=True)
class Node:
    value: Any
    left: BinTree
    right: BinTree


@dataclass(frozen=True)
class BinarySearchTree:
    tree: BinTree
    comes_before: Callable[[Any, Any], bool]


def is_empty(BST: BinarySearchTree) -> bool:
    match BST.tree:
        case None:
            return True
        case Node(_, _, _):
            return False


def _insert_helper(tree: BinTree, val: Any, comes_before: Callable[[Any, Any], bool]) -> BinTree:
    match tree:
        case None:
            return Node(val, None, None)
        case Node(h, l, r):
            if comes_before(val, h):
                return Node(h, _insert_helper(l, val, comes_before), r)
            else:
                # Values that are "equal" or come after go to the right
                return Node(h, l, _insert_helper(r, val, comes_before))


def insert(BST: BinarySearchTree, val: Any) -> BinarySearchTree:
    return BinarySearchTree(_insert_helper(BST.tree, val, BST.comes_before), BST.comes_before)


def _equal(a: Any, b: Any, comes_before: Callable[[Any, Any], bool]) -> bool:
    # a == b if neither comes before the other
    return (not comes_before(a, b)) and (not comes_before(b, a))


def _lookup_helper(tree: BinTree, val: Any, comes_before: Callable[[Any, Any], bool]) -> bool:
    match tree:
        case None:
            return False
        case Node(h, l, r):
            if _equal(val, h, comes_before):
                return True
            elif comes_before(val, h):
                return _lookup_helper(l, val, comes_before)
            else:
                return _lookup_helper(r, val, comes_before)


def lookup(BST: BinarySearchTree, val: Any) -> bool:
    return _lookup_helper(BST.tree, val, BST.comes_before)


def _min_value(tree: BinTree) -> Any:
    # Precondition: tree is not None
    match tree:
        case None:
            raise ValueError("min_value on empty tree")
        case Node(h, None, _):
            return h
        case Node(_, l, _):
            return _min_value(l)


def _delete_helper(tree: BinTree, val: Any, comes_before: Callable[[Any, Any], bool]) -> BinTree:
    match tree:
        case None:
            return None
        case Node(h, l, r):
            if comes_before(val, h):
                return Node(h, _delete_helper(l, val, comes_before), r)
            elif comes_before(h, val):
                return Node(h, l, _delete_helper(r, val, comes_before))
            else:
                # We found a node to delete (treat "equals" via _equal rules)
                # Three cases: 0, 1, or 2 children
                if l is None and r is None:
                    return None
                if l is None:
                    return r
                if r is None:
                    return l
                # Two children: replace with min in right subtree
                successor = _min_value(r)
                # Delete one occurrence of successor in right subtree
                new_right = _delete_helper(r, successor, comes_before)
                return Node(successor, l, new_right)


def delete(BST: BinarySearchTree, val: Any) -> BinarySearchTree:
# Purpose: Delete from a BST following the ordering property
    return BinarySearchTree(_delete_helper(BST.tree, val, BST.comes_before), BST.comes_before)

def height(tree: BinTree) -> int:
 # Purpose: Height defined as number of edges on the longest path from this node to a leaf.
    match tree:
        case None:
            return -1
        case Node(_, l, r):
            return 1 + max(height(l), height(r))

