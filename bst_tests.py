
import sys
import unittest
from typing import *
from dataclasses import dataclass
from bst import BinarySearchTree, delete, height, insert, is_empty, lookup

sys.setrecursionlimit(10**6)


# helper functions

def num_comes_before(a: Any, b: Any) -> bool:
    return a < b

def alpha_comes_before(a: Any, b: Any) -> bool:
    return a < b

@dataclass(frozen=True)
class Point2:
    x: float
    y: float

def dist2(p: Point2) -> float:
    return p.x * p.x + p.y * p.y

def point_comes_before(a: Point2, b: Point2) -> bool:
    return dist2(a) < dist2(b)


class BSTTests(unittest.TestCase):

    def test_is_empty(self):
        bst = BinarySearchTree(None, num_comes_before)
        self.assertTrue(is_empty(bst))
        bst = insert(bst, 10)
        self.assertFalse(is_empty(bst))

    def test_insert_lookup_integers(self):
        bst = BinarySearchTree(None, num_comes_before)
        for v in [5, 3, 7, 1, 4, 6, 9, 7, 5]:
            bst = insert(bst, v)
        for present in [1, 3, 4, 5, 6, 7, 9]:
            self.assertTrue(lookup(bst, present))
        for absent in [0, 2, 8, 10]:
            self.assertFalse(lookup(bst, absent))

    def test_delete_leaf(self):
        bst = BinarySearchTree(None, num_comes_before)
        for v in [5, 3, 7]:
            bst = insert(bst, v)
        bst = delete(bst, 3)  # delete leaf
        self.assertFalse(lookup(bst, 3))
        self.assertTrue(lookup(bst, 5))
        self.assertTrue(lookup(bst, 7))

    def test_delete_one_child(self):
        bst = BinarySearchTree(None, num_comes_before)
        for v in [5, 3, 7, 6]:
            bst = insert(bst, v)
        bst = delete(bst, 7)  # node 7 has one child (6)
        self.assertFalse(lookup(bst, 7))
        self.assertTrue(lookup(bst, 6))

    def test_delete_two_children(self):
        bst = BinarySearchTree(None, num_comes_before)
        for v in [5, 3, 7, 6, 8]:
            bst = insert(bst, v)
        bst = delete(bst, 7)
        self.assertFalse(lookup(bst, 7))
        self.assertTrue(lookup(bst, 6))
        self.assertTrue(lookup(bst, 8))

    def test_delete_nonexistent(self):
        bst = BinarySearchTree(None, num_comes_before)
        for v in [5, 2, 8]:
            bst = insert(bst, v)
        bst2 = delete(bst, 100)  # should be unchanged structurally
        self.assertTrue(lookup(bst2, 5))
        self.assertTrue(lookup(bst2, 2))
        self.assertTrue(lookup(bst2, 8))

    def test_strings_alphabetic(self):
        bst = BinarySearchTree(None, alpha_comes_before)
        for s in ["delta", "alpha", "charlie", "bravo", "echo"]:
            bst = insert(bst, s)
        for present in ["alpha", "bravo", "charlie", "delta", "echo"]:
            self.assertTrue(lookup(bst, present))
        for absent in ["al", "zulu"]:
            self.assertFalse(lookup(bst, absent))
        # delete a middle element
        bst = delete(bst, "charlie")
        self.assertFalse(lookup(bst, "charlie"))

    def test_points_distance(self):
        bst = BinarySearchTree(None, point_comes_before)
        pts = [Point2(1,0), Point2(0,1), Point2(1,1), Point2(2,0)]
        for p in pts:
            bst = insert(bst, p)

        # check lookups by distance equivalence definition
        self.assertTrue(lookup(bst, Point2(1,0)))   # r^2 = 1
        self.assertTrue(lookup(bst, Point2(0,1)))   # r^2 = 1
        self.assertTrue(lookup(bst, Point2(1,1)))   # r^2 = 2
        self.assertFalse(lookup(bst, Point2(3,0)))  # r^2 = 9 not present

        # delete one of the distance-1 points
        bst = delete(bst, Point2(1,0))
        self.assertFalse(lookup(bst, Point2(1,0))) or self.assertTrue(lookup(bst, Point2(0,1)))

    def test_height_utility(self):
        bst = BinarySearchTree(None, num_comes_before)
        self.assertEqual(height(bst.tree), -1)
        bst = insert(bst, 10)
        self.assertEqual(height(bst.tree), 0)
        bst = insert(bst, 5)
        bst = insert(bst, 15)
        self.assertEqual(height(bst.tree), 1)


if (__name__ == '__main__'):
    unittest.main()

