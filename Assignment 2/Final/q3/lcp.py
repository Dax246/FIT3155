"""
Author: Damien Ambegoda 30594235
"""
import sys


class Node:
    NODE_NUMBER = 0

    def __init__(self, len_string1, len_string2):
        self.NODE_NUMBER = Node.NODE_NUMBER
        Node.NODE_NUMBER += 1
        self.edges = [None] * 27
        self.nodes = [None] * 27
        self.parent = None
        self.string_marker = []
        self.length_incoming_string = 0

def insert_strings(string1, len_string1, len_string2, root, leaf_list, string_type):
    """
    Naive suffix tree constructor
    """

    active_node = root
    if string_type == 1:
        marker = 'a'
    if string_type == 2:
        marker = 'b'
    active_node.string_marker.append(marker)
    i = 0
    j_shift = 0
    while i < len(string1):
        j = i
        active_node = root
        while j < len(string1):
            index = ord(string1[j]) - 96
            if index == -60:
                index = 0
            # Creating leaf from root
            if active_node.edges[index] is None:
                active_node.edges[index] = string1[j:len(string1)]
                new_node = Node(len_string1, len_string2)
                active_node.nodes[index] = new_node
                new_node.parent = active_node
                new_node.string_marker.append(marker)
                new_node.length_incoming_string = len(string1) - j
                leaf_list[i] = active_node.nodes[index]
                j_shift = 0
                break

            # Traverse down edge if edge with required character exists
            elif active_node.edges[index] is not None:
                while j_shift < len(active_node.edges[index]) and \
                        active_node.edges[index][j_shift] == string1[j + j_shift]:
                    j_shift += 1
                # Whole suffix already in tree
                if j_shift == len(string1) - j:
                    active_node.nodes[index].string_marker.append(marker)
                    leaf_list[i] = active_node.nodes[index]
                    break

                # reached end of edge without finishing suffix, look for new node
                if j_shift == len(active_node.edges[index]):

                    # Jump to next node if node exists
                    if active_node.nodes[index] is not None:
                        active_node = active_node.nodes[index]
                        active_node.string_marker.append(marker)

                    # Add new edge if no new node exists
                    else:
                        new_char_index = ord(string1[j+j_shift]) - 96
                        active_node.edges[new_char_index] = string1[j + j_shift:len(string1)]
                        new_node = Node(len_string1, len_string2)
                        active_node.nodes[new_char_index] = new_node
                        new_node.parent = active_node
                        new_node.string_marker.append(marker)
                        new_node.length_incoming_string = len(string1) - j
                        leaf_list[i] = active_node.nodes[index]
                        j_shift = 0
                        break


                # Character that is being searched for does not exist so a new internal node is to be created
                elif active_node.edges[index][j_shift] != string1[j + j_shift]:
                    new_internal_node = Node(len_string1, len_string2)

                    next_char_of_current_edge_index = ord(active_node.edges[index][j_shift]) - 96
                    if next_char_of_current_edge_index == -60:
                        next_char_of_current_edge_index = 0
                    new_internal_node.edges[next_char_of_current_edge_index] = active_node.edges[index][
                                                                               j_shift:len(active_node.edges[index])]
                    new_internal_node.nodes[next_char_of_current_edge_index] = active_node.nodes[index]
                    new_internal_node.parent = active_node
                    new_internal_node.string_marker.append(marker)
                    new_internal_node.length_incoming_string = new_internal_node.parent.length_incoming_string + j_shift
                    new_internal_node.nodes[next_char_of_current_edge_index].parent = new_internal_node

                    active_node.nodes[index] = new_internal_node
                    active_node.edges[index] = active_node.edges[index][0:j_shift]

                    next_new_char = ord(string1[j + j_shift]) - 96
                    if next_new_char == - 60:
                        next_new_char = 0
                    new_internal_node.edges[next_new_char] = string1[j + j_shift:len(string1)]

                    new_node = Node(len_string1, len_string2)
                    new_internal_node.nodes[next_new_char] = new_node
                    new_node.parent = new_internal_node
                    new_node.string_marker.append(marker)
                    new_node.length_incoming_string = len(string1) - i
                    leaf_list[i] = new_node
                    j_shift = 0
                    break

        i += 1
    return root, leaf_list


def suffix_tree_constructor(string1, string2, pairs):
    """
    Complexity: O(n^2 + m^2) where n is length of string1 and m is the length of string2. The complexity
    would be O(n + m) if ukkonen's algorithm was used to construct the tree as the processing after creating the tree
    takes linear time.
    """
    string1 += '$'
    string2 += '$'
    root = Node(len(string1), len(string2))
    each_suffixes_leaf_string1 = [None] * len(string1)
    each_suffixes_leaf_string2 = [None] * len(string2)


    # Inserts both strings into the tree
    # each_suffixes_leaf list contains the leaf node for each suffix in each string
    root, each_suffixes_leaf_string1 = insert_strings(string1, len(string1), len(string2), root, each_suffixes_leaf_string1, 1)
    root, each_suffixes_leaf_string2 = insert_strings(string2, len(string1), len(string2), root, each_suffixes_leaf_string2, 2)


    # This is used to find the lowest common ancestor of the two leaf nodes that contain the two suffixes represented
    # in the pair.
    # Works by traversing upwards until parents have the same incoming string length and were visited by both parents
    # which is represented by the string_marker.
    output = []
    for pair in pairs:
        pair_split = pair.split()
        string1_leaf = each_suffixes_leaf_string1[int(pair_split[0])]
        string2_leaf = each_suffixes_leaf_string2[int(pair_split[1])]

        curr_string1_length = string1_leaf.length_incoming_string
        curr_string2_length = string2_leaf.length_incoming_string
        active_node1 = string1_leaf
        active_node2 = string2_leaf
        while len(active_node1.string_marker) != 2 or len(active_node2.string_marker) != 2 or curr_string1_length != curr_string2_length:
            if len(active_node1.string_marker) != 2:
                active_node1 = active_node1.parent
                curr_string1_length = active_node1.length_incoming_string
            if len(active_node2.string_marker) != 2:
                active_node2 = active_node2.parent
                curr_string2_length = active_node2.length_incoming_string
            if curr_string1_length > curr_string2_length:
                active_node1 = active_node1.parent
                curr_string1_length = active_node1.length_incoming_string
            elif curr_string2_length > curr_string1_length:
                active_node2 = active_node2.parent
                curr_string2_length = active_node2.length_incoming_string

        if active_node1 == root:
            output.append([pair + " 0"])
        else:
            output.append([pair + " " + str(active_node1.length_incoming_string)])

    f = open("output_lcp.txt", "w")
    for list in output:
        f.write(str(list[0]) + "\n")
    f.close()
    return



def readFile(string1Filename, string2Filename, pairsFilename):
    f = open(string1Filename, "r")
    string1 = f.read()
    f.close()
    f = open(string2Filename, "r")
    string2 = f.read()
    f.close()
    f = open(pairsFilename, "r")
    pairs_list = []
    for line in f.readlines():
        pairs_list.append(line.strip())
    return string1, string2, pairs_list

#Following based on FIT3155 Lecture
if __name__ == "__main__":
    string1filename = sys.argv[0]
    string2filename = sys.argv[1]
    pairsfilename = sys.argv[2]
    string1, string2, pairs = readFile(string1filename, string2filename, pairsfilename)
    suffix_tree_constructor(string1, string2, pairs)