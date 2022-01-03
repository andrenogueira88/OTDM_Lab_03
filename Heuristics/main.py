import MST_prim
from argparse import ArgumentParser
from datParser import DATParser
from pathlib import Path
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

parser = ArgumentParser(description='OTDM Lab Heuristics')
parser.add_argument('-c', '--configFile', nargs='?', type=Path,
					default=Path(__file__).parent / 'Iris_data.dat', help='specifies the config file')
args = parser.parse_args()
config = DATParser.parse(args.configFile)

A = []
for row in config.A:
	A.append(np.array(list(row)))

D = []
for row in A:
	d = []
	for row2 in A:
		d.append(np.linalg.norm(row - row2))
	D.append(d)

# Initialize an empty graph as an adjacent matrix with size m x m
g = MST_prim.Graph(config.m)
# Include the matrix D as the adjacent matrix of the graph - Euclidian distances
g.graph = D
# Find all links in the Minimum Spanning Tree
links = g.remaining_links_MST()

# Create a graph for the Minimum Spanning Tree using the networkx
nodes = []
edges = []
for i in range(1, g.V):
	nodes.append(links[i])
	edges.append((i, links[i], g.graph[i][links[i]]))

MST = nx.Graph()
MST.add_nodes_from(nodes)
for node1, node2, weight in edges:
	MST.add_edge(node1, node2, weight=weight)
nx.draw_networkx(MST, node_size=50, font_size=4)
plt.savefig('Graph_MST.png', dpi=150)
plt.close()

# Remove the k-1 edges with largest weights in the MST
for i in range(config.k-1):
	edge_remove = max(edges, key=lambda t: t[2])
	edges.remove(edge_remove)
	MST.remove_edge(edge_remove[0], edge_remove[1])

# Extracting subgraphs from the MST - k-1 edges with largest weights
sub_graphs = (MST.subgraph(c) for c in nx.connected_components(MST))

# Printing the result and the graphs
for i, sg in enumerate(sub_graphs):
	print("subgraph {} has {} nodes".format(i, sg.number_of_nodes()))
	print("\tNodes:", sg.nodes(data=False))
	print("\tEdges:", sg.edges())
	nx.draw_networkx(sg, node_size=50, font_size=4)
	plt.savefig('Subgraph_'+str(i)+'.png', dpi=150)
	plt.close()


print('-----Checking using built in functions of scipy------')

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

X = csr_matrix(D)
Tcsr = minimum_spanning_tree(X)
newD = Tcsr.toarray()

edgesCheck = []
nodesCheck = []
for i in range(config.m):
	nodesCheck.append(i)
	for j in range(config.m):
		if newD[i][j] > 0:
			edgesCheck.append((i, j, newD[i][j]))

MSTCheck = nx.Graph()
MSTCheck.add_nodes_from(nodesCheck)
for node1, node2, weight in edgesCheck:
	MSTCheck.add_edge(node1, node2, weight=weight)
nx.draw_networkx(MSTCheck, node_size=50, font_size=4)
plt.savefig('Graph_MST_check.png', dpi=150)
plt.close()

# Remove the k-1 edges with largest weights in the MST
for i in range(config.k-1):
	edge_remove = max(edgesCheck, key=lambda t: t[2])
	edgesCheck.remove(edge_remove)
	MSTCheck.remove_edge(edge_remove[0], edge_remove[1])

# Extracting subgraphs from the MST - k-1 edges with largest weights
sub_graphsCheck = (MSTCheck.subgraph(c) for c in nx.connected_components(MSTCheck))

# Printing the result and the graphs
for i, sg in enumerate(sub_graphsCheck):
	print("subgraph {} has {} nodes".format(i, sg.number_of_nodes()))
	print("\tNodes:", sg.nodes(data=False))
	print("\tEdges:", sg.edges())
	nx.draw_networkx(sg, node_size=50, font_size=4)
	plt.savefig('Subgraph_'+str(i)+'_check.png', dpi=150)
	plt.close()


