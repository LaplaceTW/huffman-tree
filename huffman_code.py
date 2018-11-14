#!/usr/bin/env python3
# *** coding : utf-8 ***
from graphviz import Digraph
from graphviz import render
from collections import OrderedDict


class Node(object):
    def __init__(self, _data=None, _weight=None, _left=None, _right=None):
        self.data = _data
        self.weight = _weight
        self.left = _left
        self.right = _right
        self.code = ""


def freq_count(txt):
    freq = {}
    for t in txt:
        if t in freq.keys():
            freq[t] += 1
        else:
            freq[t] = 1
    return freq


def huffman_coding(freq):
    key = []
    nodes = OrderedDict()
    while len(freq) > 1:  # create binary tree
        s_freq = sorted(freq.items(), key=lambda x: x[1])
        left, l_data = s_freq[0][0], s_freq[0][1]
        right, r_data = s_freq[1][0], s_freq[1][1]
        root, rt_data = left + right, freq.pop(left) + freq.pop(right)
        freq[root] = rt_data

        if left not in nodes.keys():
            key.append(left)
            nodes[left] = Node(left, l_data)
        if right not in nodes.keys():
            key.append(right)
            nodes[right] = Node(right, r_data)
        key.append(root)
        nodes[root] = Node(root, rt_data, nodes[left], nodes[right])

    index = len(key)
    rev_nodes = OrderedDict()
    while index > 0:  # reverse order of node
        node_obj = nodes[key[index - 1]]
        k = node_obj.data
        rev_nodes[k] = node_obj
        index -= 1

    for n in rev_nodes:  # assign code
        if rev_nodes[n].left is not None:
            rev_nodes[n].left.code = rev_nodes[n].code + '0'
        if rev_nodes[n].right is not None:
            rev_nodes[n].right.code = rev_nodes[n].code + '1'
    return rev_nodes


def get_code_table(tree):
    for n in tree:
        if len(n) == 1:
            print('[' + n + ']:' + tree[n].code)


def draw_tree(b_tree):
    dot = Digraph(comment='The Binary Tree of Huffman code')
    for n in b_tree:  # generate graphviz script
        data = b_tree[n].data
        code = b_tree[n].code
        root = 'N' + code
        if len(n) > 1:
            dot.node(root, code)
        else:
            dot.node(root, '[' + data + '] : ' + code, fontcolor='blue', shape='box')

        if b_tree[n].left is not None:
            left = 'N' + b_tree[n].left.code
            right = 'N' + b_tree[n].right.code
            dot.edge(root, left)
            dot.edge(root, right)
    dot.render('Huffman_code.gv', view=True)


def main():
    txt = input('input:')
    freq = freq_count(txt)
    tree = huffman_coding(freq)
    get_code_table(tree)
    draw_tree(tree)


if __name__ == "__main__":
    main()
