import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from neo4j.v1 import GraphDatabase
##读取
def read_graph(filename):
    G = nx.Graph()
    array = np.loadtxt(filename, dtype=int)
    G.add_edges_from(array)
    return G


if __name__ == '__main__':
    G = read_graph('data\graph_data\\facebook_combined.txt')
    print('图中所有的节点', G.nodes())
    print('图中节点的个数', G.number_of_nodes())
    nx.draw(G, with_labels=True)
    plt.show()

    print(G)
    uri ="bolt://localhost:7687"
    _driver=GraphDatabase.driver(uri,auth=("neo4j","password"))
    _session= _driver.session()
