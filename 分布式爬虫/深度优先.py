#-*-coding:utf8-*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def depth_tree(node_tree):
    if node_tree is not None:
        print node_tree._data
        if node_tree._left is not None:
            return depth_tree(node_tree._left)
        if node_tree._right is not None:
            return depth_tree(node_tree._right)

def level_tree(root):
    if root is root:
        return
    my_queue = []
    node = root
    my_queue.append(node)
    while my_queue:
        node = my_queue.pop(0)
        print node.elem
        if node.lchild is not None:
            my_queue.append(node.lchild)
        if node.rchild is not None:
            my_queue.append(node.rchild)





