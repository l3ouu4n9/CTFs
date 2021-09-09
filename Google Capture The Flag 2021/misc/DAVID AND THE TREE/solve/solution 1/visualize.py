#!/usr/bin/env python3

# huffman tree decoding adapted from Paul Tan's source code at https://pyokagan.name/blog/2019-10-18-zlibinflate/

from solve import carve, get_huffman_tree
import networkx as nx

# graph a given huffman tree
def visualize(huffman_tree, output_name):
    g = huffman_tree.make_graph()
    A = nx.drawing.nx_agraph.to_agraph(g)
    A.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
    A.draw(output_name)
    print(f'Graph generated: {output_name}')

# get raw compressed data from challenge and example
challenge_data = carve('challenge.zip', 0x24)
example_data = carve('compression_test.zip', 0x40)

# build tree for challenge and example
challenge00 = get_huffman_tree(challenge_data[0])
print()
example00 = get_huffman_tree(example_data[0])

# graph challenge and example
visualize(challenge00, 'img/00_challenge_tree.png')
visualize(example00, 'img/00_example_tree.png')