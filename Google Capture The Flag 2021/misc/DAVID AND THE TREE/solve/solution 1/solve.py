#!/usr/bin/env python3

# huffman tree decoding adapted from Paul Tan's source code at https://pyokagan.name/blog/2019-10-18-zlibinflate/
import zipfile
import networkx as nx

# extract raw compressed data from zip file
def carve(zip_name, metadata_size):
    # list of tuples, (offset, size)
    files = []
    # parse zip file
    with zipfile.ZipFile(zip_name, 'r') as zip_file:
        # iterate over each file in zip
        for elem in zip_file.infolist():
            offset = elem.header_offset + metadata_size
            compress_size = elem.compress_size
            files.append((offset, compress_size))

    compressed_data = []
    with open(zip_name, 'rb') as raw_zip:
        for f in files:
            # seek to offset and read compressed_size bytes
            raw_zip.seek(f[0])
            compressed_data.append(raw_zip.read(f[1]))

    return compressed_data

# parse raw compressed data to get huffman tree (ignore distance tree)
def get_huffman_tree(raw):
    r = BitReader(raw)
    # read BFINAL and BTYPE
    BFINAL = r.read_bit()
    BTYPE = r.read_bits(2)
    literal_length_tree, distance_tree = decode_trees(r)
    return literal_length_tree 

### from https://pyokagan.name/blog/2019-10-18-zlibinflate/ ###
class BitReader:
    def __init__(self, mem):
        self.mem = mem
        self.pos = 0
        self.b = 0
        self.numbits = 0

    def read_byte(self):
        self.numbits = 0 # discard unread bits
        b = self.mem[self.pos]
        self.pos += 1
        return b

    def read_bit(self):
        if self.numbits <= 0:
            self.b = self.read_byte()
            self.numbits = 8
        self.numbits -= 1
        # shift bit out of byte
        bit = self.b & 1
        self.b >>= 1
        return bit

    def read_bits(self, n):
        o = 0
        for i in range(n):
            o |= self.read_bit() << i
        return o

class Node:
    def __init__(self):
        self.symbol = '' 
        self.left = None
        self.right = None

class HuffmanTree:
    def __init__(self):
        self.root = Node()
   
    def make_graph(self):
        g = nx.DiGraph()
        g = self.walk_graph(self.root, None, g)
        return g

    def make_tree(self):
        tree = Tree()
        tree = self.walk(self.root, None, tree)
        return tree

    def walk_graph(self, node, parent, g, edge_label=None):
        if not parent:
            g.add_node(id(node), label='root') 
        else:
            if node.symbol != '':
                label = node.symbol
            else:
                label = ''
            g.add_node(id(node), label=label)
            g.add_edge(id(parent), id(node), label=edge_label)
        if node.left:
            self.walk_graph(node.left, node, g, '0')
        if node.right:
            self.walk_graph(node.right, node, g, '1')
        return g

    def walk(self, node, parent, tree):
        if not parent:
            tree.create_node(node.symbol, node.symbol) 
        else:
            tree.create_node(node.symbol, node.symbol, parent=parent.symbol)
        if node.left:
            self.walk(node.left, node, tree)
        if node.right:
            self.walk(node.right, node, tree)
        return tree

    def insert(self, codeword, n, symbol):
        # Insert an entry into the tree mapping `codeword` of len `n` to `symbol`
        node = self.root

        # if inserting symbol 69 ('E'), follow bit path
        p = False
        bits = b''
        if symbol == 69:
            p = True
        for i in range(n-1, -1, -1):
            b = codeword & (1 << i)
            if b:
                bits += b'1'
                next_node = node.right
                if next_node is None:
                    node.right = Node()
                    next_node = node.right
            else:
                bits += b'0'
                next_node = node.left
                if next_node is None:
                    node.left = Node()
                    next_node = node.left
            node = next_node
        # print bit path in reverse to get character of flag
        if p:
            print(chr(int(bits[::-1], 2)), end='')
        
        node.symbol = symbol

def decode_symbol(r, t):
    "Decodes one symbol from bitstream `r` using HuffmanTree `t`"
    node = t.root
    while node.left or node.right: 
        b = r.read_bit()
        node = node.right if b else node.left
    return node.symbol

LengthExtraBits = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3,
        3, 4, 4, 4, 4, 5, 5, 5, 5, 0]
LengthBase = [3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 23, 27, 31, 35, 43,
        51, 59, 67, 83, 99, 115, 131, 163, 195, 227, 258]
DistanceExtraBits = [0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7,
        8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13]
DistanceBase = [1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193, 257,
        385, 513, 769, 1025, 1537, 2049, 3073, 4097, 6145, 8193, 12289, 16385,
        24577]

def bl_list_to_tree(bl, alphabet):
    MAX_BITS = max(bl)
    bl_count = [sum(1 for x in bl if x == y and y != 0) for y in range(MAX_BITS+1)]
    next_code = [0, 0]
    for bits in range(2, MAX_BITS+1):
        next_code.append((next_code[bits-1] + bl_count[bits-1]) << 1)
    t = HuffmanTree()
    test = []
    for c, bitlen in zip(alphabet, bl):
        if bitlen != 0:
            if c < 256:
                test.append(c)
            t.insert(next_code[bitlen], bitlen, c)
            next_code[bitlen] += 1
    if len(alphabet) == 286:
        a = []
        for b in range(0, 256):
            if b not in test:
                a.append(b)
    return t

CodeLengthCodesOrder = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]

def decode_trees(r):
    # The number of literal/length codes
    HLIT = r.read_bits(5) + 257

    # The number of distance codes
    HDIST = r.read_bits(5) + 1

    # The number of code length codes
    HCLEN = r.read_bits(4) + 4

    # Read code lengths for the code length alphabet
    code_length_tree_bl = [0 for _ in range(19)]
    for i in range(HCLEN):
        code_length_tree_bl[CodeLengthCodesOrder[i]] = r.read_bits(3)

    # Construct code length tree
    code_length_tree = bl_list_to_tree(code_length_tree_bl, range(19))

    # Read literal/length + distance code length list
    bl = []
    while len(bl) < HLIT + HDIST:
        sym = decode_symbol(r, code_length_tree)
        if 0 <= sym <= 15: # literal value
            bl.append(sym)
        elif sym == 16:
            # copy the previous code length 3..6 times.
            # the next 2 bits indicate repeat length ( 0 = 3, ..., 3 = 6 )
            prev_code_length = bl[-1]
            repeat_length = r.read_bits(2) + 3
            bl.extend(prev_code_length for _ in range(repeat_length))
        elif sym == 17:
            # repeat code length 0 for 3..10 times. (3 bits of length)
            repeat_length = r.read_bits(3) + 3
            bl.extend(0 for _ in range(repeat_length))
        elif sym == 18:
            # repeat code length 0 for 11..138 times. (7 bits of length)
            repeat_length = r.read_bits(7) + 11
            bl.extend(0 for _ in range(repeat_length))
        else:
            raise Exception('invalid symbol')

    # Construct trees
    literal_length_tree = bl_list_to_tree(bl[:HLIT], range(286))
    distance_tree = bl_list_to_tree(bl[HLIT:], range(30))
    return literal_length_tree, distance_tree


if __name__ == "__main__":
    # get raw compressed data from challenge.zip
    challenge_data = carve('challenge.zip', 0x24)

    # extract huffman tree, inserter will print when 'E' character is inserted 
    for i, f in enumerate(challenge_data):
        get_huffman_tree(f)