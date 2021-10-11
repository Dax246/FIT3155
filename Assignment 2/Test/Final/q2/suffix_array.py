"""
Author: Damien Ambegoda 30594235
"""
import sys


class Node():
    node_number = 0

    # Edges stored as [a,b] where a and b are indexes of string
    def __init__(self):
        self.edges = [None] * 27
        self.nodes = [None] * 27
        self.suffix_link = None
        self.leaf_node_check = False
        Node.node_number += 1

        # Suffix_number needed to create the suffix_array
        self.suffix_number = None
        return

class global_pointer():
    """ This class contains the global pointer that is required for rule 1
    """

    def __init__(self):
        self.value = -1

    def increment(self):
        self.value += 1

    def __int__(self):
        return self.value

    def __repr__(self):
        return "GP at " + str(int(self))

def suffix_tree_constructor(string):
    string = string + "$"

    i = - 1
    # Remainder stored as [a,b] where a and b are indexes of string
    # [-1, -2] indicates an empty remainder
    remainder = [-1, -2]
    GP = global_pointer()
    lastJ = -1
    root = Node()
    root.suffix_link = root
    active_node = root

    # using a dummy node until the first internal node is created
    new_internal_node = Node()

    reduce_remainder_check = False
    # i represents the phase
    while i+1 < len(string):
        # lastJ is used to identify where the next J should start from.
        j = lastJ + 1
        # Incrementing global pointer to apply rule 1 to the edges that require it
        GP.increment()

        # j represents the extension
        while j <= i + 1:

            # Remove the first character of remainder if last extension, a suffix link was taken from the root back to the root
            if reduce_remainder_check:
                remainder[0] = remainder[0] + 1
                if remainder[0] > remainder[1]:
                    remainder = [-1, -2]

            rule_3_check = False
            length_of_remainder = max(0, remainder[-1] - remainder[0] + 1)

            # Keeps track of how far along the edge has been traversed
            traverse_amount = max(0, remainder[1] - remainder[0] + 1)


            # If there is a remainder, only needs to check edge for the last character of remainder
            if length_of_remainder > 0:
                index = ord(string[remainder[0]]) - 96
                # If edge has remainder then move to position after the last character in remainder
                curr_letter = remainder[-1] + 1
            # When no remainder, just check next character from j
            else:
                index = ord(string[j + traverse_amount]) - 96
                curr_letter = j


            len_remaining_remainder = length_of_remainder
            starting_active_node = active_node

            skipcount_counter = 0

            # Create new leaf from root - Rule 2
            if active_node.edges[index] is None:
                root.edges[index] = [j, GP]
                new_node = Node()
                new_node.leaf_node_check = True
                root.nodes[index] = new_node
                lastJ = j
                new_node.suffix_number = j

                # Previously created node has suffix link to the parent of the leaf node
                new_internal_node.suffix_link = active_node
                new_internal_node = Node()

            # Skip Count
            # Checks if next edge's length is <= to the rest of remainder
            # This will get you to the correct internal node
            elif len_remaining_remainder >= (int(active_node.edges[index][1]) - active_node.edges[index][0] + 1):
                while len_remaining_remainder >= (int(active_node.edges[index][1]) - active_node.edges[index][0] + 1):

                    # skipcount_counter removes the edge from remainder as it has already been dealt when skipcounting
                    # without deleting the remainder
                    skipcount_counter += (int(active_node.edges[index][1]) - active_node.edges[index][0] + 1)
                    len_remaining_remainder -= skipcount_counter
                    active_node = active_node.nodes[index]
                    active_node.suffix_number = j
                    remainder[0] = remainder[0] + skipcount_counter

                    # If remainder[1] < remainder[0] then remainder is empty so reset to the empty representation
                    if remainder[1] < remainder[0]:
                        remainder = [-1, -2]
                    if remainder[0] != -1:
                        index = ord(string[remainder[0]]) - 96
                    else:
                        index = ord(string[curr_letter]) - 96
                    continue

            # After skipcount, it is at the correct internal node to check the character after remainder or j if no remainder
            else:
                while curr_letter <= i + 1:


                    # First checks that there is a character after the rest of remainder on this edge to do a comparison on
                    # Second checks if curr_letter is in the edge
                    if active_node.edges[index][0] + len_remaining_remainder <= int(active_node.edges[index][1]) and \
                            string[active_node.edges[index][0] + len_remaining_remainder] == string[curr_letter]:

                        # Next character is on the edge so update remainder

                        # remainder is empty
                        if remainder[0] == -1:
                            remainder = [curr_letter, curr_letter]

                        else:
                            remainder[1] = curr_letter
                        traverse_amount += 1
                        curr_letter += 1


                    # Next character is not in the current edge so rule 2
                    else:

                        # Rule 2 with new internal node
                        new_node = Node()
                        # the new internal node's edge will contain the rest of the old edge
                        char_after_current_on_edge = ord(string[active_node.edges[index][0] + traverse_amount]) - 96
                        new_node.edges[char_after_current_on_edge] = [active_node.edges[index][0] + traverse_amount, active_node.edges[index][1]]

                        # Creates the new leaf edge to account for new char
                        new_char = ord(string[curr_letter]) - 96
                        new_node.edges[new_char] = [curr_letter, GP]

                        # Adds leaf node from new edge
                        new_leaf_node = Node()
                        new_leaf_node.leaf_node_check = True
                        new_node.nodes[new_char] = new_leaf_node

                        # Moves old next node to this node
                        new_node.nodes[char_after_current_on_edge] = active_node.nodes[index]

                        # Cuts down old edge
                        active_node.edges[index][1] = active_node.edges[index][0]+traverse_amount - 1
                        active_node.nodes[index] = new_node


                        # Makes the previously created node have suffix link to newly created node
                        new_internal_node.suffix_link = new_node
                        new_internal_node = active_node.nodes[index]

                        # Updates Active node to be the suffix link of the active node from the start of this extension
                        active_node = starting_active_node.suffix_link

                        # Check used in next extension to determine if remainder needs to be reduced by one character
                        # as taken a suffix link from the rot back to the root
                        if starting_active_node == root and active_node == root:
                            reduce_remainder_check = True
                        else:
                            reduce_remainder_check = False

                        lastJ = j
                        break


                    # Character is in the edge so rule 3 (showstopper)
                    if curr_letter > i + 1:
                        rule_3_check = True

                        # Previously created node has suffix link to closest internal node to where rule 3 took place
                        new_internal_node.suffix_link = active_node
                        new_internal_node = Node()
                        reduce_remainder_check = False
                        break

                # Don't incremenet j and curr_letter if rule 3 and just start the next phase (increment i)
                if rule_3_check == True:
                    break

            j += 1
            curr_letter += 1

        i += 1

    # Depth first search used to create suffix array from suffix tree
    suffix_array = []
    nodes_stack = []
    nodes_stack.append(root)
    while len(nodes_stack) != 0:
        curr_node = nodes_stack.pop()
        for i in range(len(curr_node.nodes)):
            if curr_node.nodes[i] != None:
                nodes_stack.append(curr_node.nodes[i])
        if curr_node.leaf_node_check == True:
            suffix_array.append(curr_node.suffix_number)

    f = open("output_suffix_array.txt", "w")
    for suffix in suffix_array:
        f.write(str(suffix) + "\n")
    f.close()
    return


def read_File(stringFilename):
    f = open(stringFilename, "r")
    string = f.read()
    return string


#Following based on FIT3155 Lecture
if __name__ == "__main__":
    stringFileeName = sys.argv[1]
    string = read_File(stringFileeName)
    suffix_tree_constructor(string)