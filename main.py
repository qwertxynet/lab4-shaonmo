import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6) 

BinaryTree : TypeAlias = Union["BTNode", None]


@dataclass(frozen=True)
class BTNode:
    head: Any
    left: BinaryTree
    right: BinaryTree

@dataclass(frozen=True)

class BinarySearchTree:
    tree: BinaryTree
    comes_before: Callable[[Any, Any], bool]


def is_empty(BST: BinarySearchTree) -> bool:
    match BST.tree:
        case None:
            return True
        case BTNode(h, l, r):
            return False
        

def insert_helper(tree: BinaryTree, val: int, comes_before: Callable[[Any, Any], bool]) -> BinaryTree:
    match tree:
        case None:
            return BTNode(val, None, None)
        case BTNode(h, l, r):
            if comes_before(val, h):
                return BTNode(h, insert_helper(l, val,comes_before), r)
            else:
                return BTNode(h, l, insert_helper(r, val,comes_before))
 
        
def insert(BST: BinarySearchTree, val: int) -> BinarySearchTree:
    new_tree : BinarySearchTree = BinarySearchTree(insert_helper(BST.tree, val, BST.comes_before), BST. comes_before)
    return new_tree


def lookup_helper(tree: BinaryTree, val: int, comes_before: Callable[[Any, Any], bool]) -> bool:
    match tree:
        case None:
            return False
        case BTNode(h, l, r):
            if (not comes_before(val, h) and not comes_before(h, val)):
                return True
            elif comes_before(val, h):
                return lookup_helper(l, val, comes_before)
            elif comes_before(h, val):
                return lookup_helper(r, val, comes_before)
            



def lookup(BST: BinarySearchTree, val: int) -> bool:
    return lookup_helper(BST.tree, val, BST.comes_before)




def delete_helper(tree: BinaryTree, val: int, comes_before: Callable[[Any, Any], bool]) -> BinaryTree:
    match tree:
        case None:
            return tree
        case BTNode(h, l ,r):
            # if we identify that the value is less, just search left 
            if comes_before(val, h):
                return BTNode(h, delete_helper(l, val, comes_before),r)
            #  if we identify that the value is more, just search right 
            elif comes_before(h, val):
                return BTNode(h, l, delete_helper(r, val, comes_before))
            else:
                match(l,r):
                    case(None, None):
                        return None
                    case(l, None):
                        return r
                    case(None, r):
                        return l
                    case (l, r):
                        return BTNode(delete_helper_helper(r), l, delete_helper(r, delete_helper_helper(r), comes_before))


                    
#given a binary tree return the smallest value in the tree
                    
def delete_helper_helper(tree: BinaryTree) -> int:
    match tree:
        case BTNode(f, l, _):
            if l is not None:
                return delete_helper_helper(l)
            else:
                return f
        case None:
            return 0

