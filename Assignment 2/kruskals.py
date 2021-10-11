"""
Author: Damien Ambegoda 30594235
"""
import heapq
import sys
from operator import itemgetter

class Disjoint():
    parent_array = []

    def __init__(self, no_of_vertices):
        self.parent_array = [-1] * no_of_vertices
        # height of tree is -1 * (height + 1)

    def find(self, vertex):
        if self.parent_array[vertex] < 0:
            return vertex
        else:
            self.parent_array[vertex] = self.find(self.parent_array[vertex])
            return self.parent_array[vertex]


    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return
        height_a = -1 * self.parent_array[root_a]
        height_b = -1 * self.parent_array[root_b]

        if height_a > height_b:
            self.parent_array[root_b] = root_a
            self.parent_array[root_a] = -1 * (height_a + height_b)

        else:
            self.parent_array[root_a] = root_b
            self.parent_array[root_b] = -1 * (height_a + height_b)

    def union_with_root(self, a, b, root_a, root_b):
        if root_a == root_b:
            return
        height_a = -1 * self.parent_array[root_a]
        height_b = -1 * self.parent_array[root_b]

        if height_a > height_b:
            self.parent_array[root_b] = root_a
            self.parent_array[root_a] = -1 * (height_a + height_b)

        else:
            self.parent_array[root_a] = root_b
            self.parent_array[root_b] = -1 * (height_a + height_b)


def kruskals(no_of_vertices, edges):
    no_of_vertices = int(no_of_vertices)
    edges.sort(key = lambda  edges: int(edges[2]))
    kruskal_disjoint = Disjoint(no_of_vertices)
    Tree = []
    total_weight = 0
    for edge in edges:
        root_a = kruskal_disjoint.find(int(edge[0]))
        root_b = kruskal_disjoint.find(int(edge[1]))
        if root_a != root_b:
            kruskal_disjoint.union_with_root(int(edge[0]), int(edge[1]), root_a, root_b)
            Tree.append(edge)
            total_weight += int(edge[2])

    f = open("output_kruskals.txt", "w")
    f.write(str(total_weight) + "\n")
    for edge in Tree:
        edge_string = edge[0] + " " + edge[1] + " " + edge[2]
        f.write(str(edge_string) + "\n")
    f.close()

    return


def read_File(edge_file):
    f = open(edge_file, "r")
    edge_list = []
    for line in f.readlines():
        edge_list.append([line.strip()])
    final_edge_list = []
    for edge in edge_list:
        final_edge_list.append(edge[0].split())
    return final_edge_list


#Following based on FIT3155 Lecture
if __name__ == "__main__":
    vertexes = sys.argv[1]
    edgeFilename = sys.argv[2]
    edges = read_File(edgeFilename)
    kruskals(vertexes, edges)