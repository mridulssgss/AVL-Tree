#implementing a rudimentry AVL Tree for implementing range index

import random
#from circuit2 import *
class BST_Node:
    """Implementing a BST Node"""

    def __init__(self, value, parent=None, lc=None, rc=None):
        self.value=value
        self.parent=parent
        self.left_child = lc
        self.right_child = rc

    def _hgt(self, node):
        if (node is None):
            return -1
        else:        
            return 1 + max(self._hgt(node.left_child), self._hgt(node.right_child))

    def insert(self, keyNode):
        """insert the Node in the BST"""

        if (self.value >= keyNode.value):
            if (self.left_child is None):
                self.left_child = keyNode
                keyNode.parent = self
            else:
                self.left_child.insert(keyNode)
        else:
            if (self.right_child is None):
                self.right_child = keyNode
                keyNode.parent = self
            else:
                self.right_child.insert(keyNode)

    def find_node(self, key):
        """finds the node with the given key"""
        
        if self.value == key:
            return self
        elif self.value < key:
            if self.right_child is not None:
               return self.right_child.find_node(key)
        else:
            if self.left_child is not None:
                return self.left_child.find_node(key)
        
        return None

    def find_min(self):
        """returns the min Node"""
        min = self
        while min.left_child is not None:
            min = min.left_child
        return min

    def find_max(self):
        """return the max Node"""
        max = self
        while max.right_child is not None:
            max = max.right_child
        return max   
            
    def to_parent(self):
        """return the root of tree"""
         
        n = self

        while n.parent is not None:
            n = n.parent
        return  n

    def delete(self):
        """
        delete an node and returns the node replaced by it if it exist. 
        Else parent node is returned
        """

        inode = None
        if (self.left_child is not None):
            inode=self.left_child.find_max()
            inode.delete()
        elif(self.right_child is not None):
            inode=self.right_child.find_min()
            inode.delete()
                
        parent = self.parent
        if inode is None and parent is not None:
            if self.value <= parent.value:
                parent.left_child = None
            else:
                parent.right_child = None
        elif inode is not None:
            Node_swap(self, inode)
        self.left_child = None
        self.right_child = None
        self.parent = None
        return inode if inode is not None else parent
     

    def pre_order_traversal(self):
        print(self.value, end=" ")
        
        if self.left_child is not None:
            self.left_child.pre_order_traversal()

        if self.right_child is not None:
            self.right_child.pre_order_traversal()
    
    def height(self):
        return self._hgt(self)
    
    def sucessor(self):
        """returns the sucessor of the given node"""
        s = None
        if self.right_child is not None:
            s = self.right_child.find_min()
        
        if s is None:
            tnode = self.parent
            while tnode is not None and tnode.value < self.value:
                tnode = tnode.parent
            s = tnode
        return s
    
    def predecessor(self):
        """returns the predecessor of the give node"""
        s = None
        if self.left_child is not None:
            s = self.left_child.find_max()
        if s is None:
            tnode = self.parent
            while tnode is not None and tnode.value > self.value:
                tnode = tnode.parent
            s = tnode

        return s
    
    def smallest_greater_than(self, x):
        """find the smallest num larger than x"""
        r = None
        if self.value >= x:
            r = self
            if self.left_child is not None:
                t = self.left_child.smallest_greater_than(x)
                if t is not None:
                    r = t
        elif self.right_child is not None:
            r = self.right_child.smallest_greater_than(x)
        
        return r
        
    def list_range(self, left_key, right_key, lst):
        if left_key <= self.value <= right_key:
            lst.append(self.value)
        if self.left_child is not None and left_key <= self.value:
            self.left_child.list_range(left_key, right_key, lst)
        if self.right_child is not None and  self.value <= right_key:
            self.right_child.list_range(left_key, right_key, lst)

    def list_range2(self, left_key, right_key, lst):
        x = self.smallest_greater_than(left_key)
        while x is not None and x.value <= right_key:
            lst.append(x.value)
            x = x.sucessor()

def draw_lst(node_lst, nos_left_spaces, nos_inner_spaces):
    """draws the ascii art of tree at a particular"""
        
    print(" " * nos_left_spaces, end = "")
    new_node_lst = []
    for el in node_lst:
        print(el.value, end="")
        if (el.left_child is not None):
            new_node_lst.append(el.left_child)
        else:
            new_node_lst.append(BST_Node(" "))
        if (el.right_child is not None):
            new_node_lst.append(el.right_child)
        else:
            new_node_lst.append(BST_Node(" "))
        print(" " * nos_inner_spaces, end="")

    print(" ")

    spaces = len([i for i in new_node_lst if i.value == " "])

    if((len(new_node_lst) - spaces)  >  0):
        draw_lst(new_node_lst, (nos_left_spaces // 2), nos_left_spaces)
    
def draw(node):
    """draw a rooted tree at node"""
    draw_lst([node], int((2 ** node.height()) - 1), 0)

            

def Node_swap(A, B):
    """Put the node B in place of A. Both should be not null"""

    parent = A.parent
    lc = A.left_child
    rc = A.right_child

    if (lc is not None):
        B.left_child = lc
        lc.parent = B
    
    if (rc is not None):
        B.right_child = rc
        rc.parent = B
    
    if (parent is not None and parent.value < B.value):
        parent.right_child = B
        B.parent = parent
    elif (parent is not None and parent.value >= B.value):
        parent.left_child = B
        B.parent = parent


class AVL_Node(BST_Node):
    """make an AVL Node"""
    
    def __init__(self, value, parent = None, lc = None, rc= None):
        self.__height = 0
        super().__init__(value, parent, lc,  rc)
        
    
    def insert(self, Node):
        """insert to the node and update the ancestry and return the root node"""
        super().insert(Node)
        
        n = self._rebalance(Node)
        return n.to_parent() if n is not None else n
    
        
    def _rebalance(self, n):
        """rebalancing the node"""
        hg = lambda x: x.__height if x is not None else -1
        
        while n.parent is not None:    
            n.height()
            if(abs( hg(n.left_child) - hg(n.right_child) ) > 1):
               n = self._balance(n)          #balances the tree
            n = n.parent
        
        if(abs(hg(n.left_child) - hg(n.right_child)) > 1):
            n = self._balance(n)
        return n
        

    def _balance(self, n):
        """balances the tree and return the new node at the positon of n"""
        
        hg = lambda x: x.height() if x is not None else -1
        if(hg(n.right_child) > hg(n.left_child)):
            if(hg(n.right_child.left_child) > hg(n.right_child.right_child)):
                self._right_rotate(n.right_child)
            n = self._left_rotate(n)
        else:
            if(hg(n.left_child.right_child) > hg(n.left_child.left_child)):
                self._left_rotate(n.left_child)
            n = self._right_rotate(n)
        return n


    def _left_rotate(self, n):
        """left rotation of AVL tree"""

        p = n.parent
        rc = n.right_child

        n.right_child = rc.left_child
        if(n.right_child is not None):
            n.right_child.parent = n
        
        rc.left_child = n
        rc.left_child.parent = rc
        
        rc.parent = p
        if p is not None:
            if (rc.value <= p.value):
                p.left_child = rc
            else:
                p.right_child = rc
        
        n.height()
        rc.height()
        return rc


    def _right_rotate(self, n):
        """left rotation of AVL tree"""

        p = n.parent
        lc = n.left_child

        n.left_child = lc.right_child
        
        if(n.left_child is not None):
            n.left_child.parent = n
        
        lc.right_child = n
        lc.right_child.parent = lc
        
        lc.parent = p
        if p is not None:
            if (lc.value <= p.value):
                p.left_child = lc
            else:
                p.right_child = lc
        
        n.height()
        lc.height()
        return lc


    def height(self):
        """calc height and saves it in __height slot"""
        self.__height = super().height()
        return self.__height
    

    def delete(self):
       """delete and update the height and returns the updated node if it exist"""
       n = super().delete()
       if n is not None:
           n = self._rebalance(n)
       return n



def remove(tree, key):
    """removes a node from the tree is it exist and return the new root fo the tree"""
    qnode = tree.find_node(key)
    if qnode is not None:
        return qnode.delete()
        
        

def put(tree, key):
    """takes a key as input and insert it"""
    tree = tree.insert(AVL_Node(key))



nums = AVL_Node(99)



for i in [50, 101, 0, 0, 0, 1, 3, 5, 8]:
   nums = nums.insert(AVL_Node(i))    

draw(nums)
print(" ")
lst1 = []
nums.list_range(-1, 9, lst1)
lst2 = []
nums.list_range2(-1, 9, lst2)
print(" ")
print(f"lst1 = {lst1} and lst2 = {lst2}")



