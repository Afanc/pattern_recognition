#!/usr/bin/python
import xml.etree.ElementTree as ET
import os
import numpy as np


class Molecule_object:
    def __init__(self, name, label, adj_matrix):
        self.name = name
        self.label = label 
        self.adj_matrix = adj_matrix
    
    def get_name(self):
        return self.name

    def get_label(self):
        return self.label

    def get_matrix(self):
        return self.adj_matrix


class Molecules:
    def __init__(self, folder, filename):

        self.filename = os.path.join(folder, filename)
        self.tree = ET.parse(self.filename)  # with ET.parse we can read in the gxl file
        self.node = [node.text.strip(" ") for node in self.tree.findall(".//node/attr/string")] #gets the lable of all the nodes
        self.edge_values = [edge.text for edge in self.tree.findall(".//edge/attr/int")] #gets the value of each edge (corresponding to the number of bonds between two atoms)

        # creats a nested list
        # for each edge the two corresponding nodes will be extracted from the file saved in a nested list.
        # e.g [[0,2],[0,5],[0,7].....]   --> means node 0 is connected with node 2, 5, and 7
        # we subtract by -1 because we want to use the nodes as indices later--> e.g.  the first node should be node 0
        self.start_end = [[int(edge.get('from').strip("_"))-1, int(edge.get('to').strip("_"))-1] for edge in self.tree.findall(".//edge")] #

    def get_adj_matrix(self):
        # creates an empty adjacency matrix in form of a nested list
        # size of the matrix is equal to the number of nodes --> len(self.node)
        adjacency_matrix = [[0 for i in range(len(self.node))] for j in range(len(self.node))]

        # iterates over the node pairs connected by edges
        for counter, node_pair in enumerate(self.start_end):
            # fills the edge values of the corresponding node pairs into the adjacency matrix
            adjacency_matrix[node_pair[0]][node_pair[1]] = int(self.edge_values[counter])
            adjacency_matrix[node_pair[1]][node_pair[0]] = int(self.edge_values[counter])
        # inserts the node lables into the diagonal of the adjacency matrix
        for i in range(len(self.node)):
            adjacency_matrix[i][i] = self.node[i]
        return adjacency_matrix

    def get_bipartite(self):
        def _int(si):
            return si if isinstance(si, int) else int(si) if si.isdigit() else 0
        adjm = self.get_adj_matrix()
        bplen = len(adjm)
        bp = []
        for i in range(bplen):
            node = adjm[i][i]   # nodes: atoms
            edges = sum(np.array([_int(xi) for xi in adjm[i]]))   #  sum(np.apply_along_axis(_int, 0, adjm[i]))   # edges: covalent bonds
            bp.append([node, edges])
        return bp


def adj_matrix(folder_of_gxl_files):
    """
    :param folder_of_gxl_files: folder which contains the gxl files
    :return: dictionary with filename as key and adjacency matrix as value
    Additionally instances for all the gxl files are created
    example: instance M16 is created for file 16.gxl
    """
    # get all .gxl files
    list_of_molecules = os.listdir(folder_of_gxl_files)

    d = {}
    # iterate over every .gxl file
    for file in list_of_molecules:
        file_num = int(file.strip(".gxl"))

        # creats an instance for a molecule
        # example for file 16.gxl:
        # globals()["M%s" % file_num] = Molecules(16.gxl) would correspond to M16 = Molecules(16.gxl)
        d[str(file_num)] = Molecules(folder_of_gxl_files, file)
        globals()["M%s" % file_num] = d[str(file_num)]

        # add key value pair to dictionary. Key is the filename (e.g. "16.gxl") and the value is the adjacency Matrix for this file
        # d[file] = globals()["M%s" % file_num].get_adj_matrix()

    return d


#######################################################################
if __name__ == "__main__":
    # working directory should be "src/main/py/mol"
    input_path = "data/gxl"

    #apply function to create instances and to get dictionary containing the adjacency matrix
    d = adj_matrix(input_path)

    #print(adjacency matrix for instance M16 (corresponding to file 16.gxl)
    print("adjacency matrix for 16.gxl")
    print(M16.get_adj_matrix(), "\n")

    # print adjacency matrix for Molecule 9770
    print("adjacency matrix for 9770.gxl, nice representation")
    for i in d["9770"].get_adj_matrix():
        print(i)


