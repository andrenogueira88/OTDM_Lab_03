import MST_prim
from argparse import ArgumentParser
from datParser import DATParser
from pathlib import Path
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.distance_measures import center
import time
start_time = time.time()

parser = ArgumentParser(description='OTDM Lab Heuristics')
parser.add_argument('-d', '--data', nargs='?', default='blob.dat', help='specifies the data file')
args = parser.parse_args()
# config = DATParser.parse(args.configFile)
config = DATParser.parse(Path(args.data))


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
	nodes.append(i)
	edges.append((i, links[i], g.graph[i][links[i]]))


MST = nx.Graph()
MST.add_nodes_from(nodes)
for node1, node2, weight in edges:
	MST.add_edge(node1, node2, weight=weight)
nx.draw_networkx(MST, node_size=50, font_size=4)
plt.savefig('Graph_MST_blob.png', dpi=150)
plt.close()

# Remove the k-1 edges with largest weights in the MST
for i in range(config.k-1):
	edge_remove = max(edges, key=lambda t: t[2])
	edges.remove(edge_remove)
	MST.remove_edge(edge_remove[0], edge_remove[1])

# Extracting subgraphs from the MST - k-1 edges with largest weights
sub_graphs = (MST.subgraph(c) for c in nx.connected_components(MST))

print("--- %s seconds ---" % (time.time() - start_time))

total_cost = 0
# Printing the result and the graphs
sub_graphs_nodes = {}
for i, sg in enumerate(sub_graphs):
	print("subgraph {} has {} nodes".format(i, sg.number_of_nodes()))
	print("\tNodes:", sg.nodes(data=False))
	print("\tEdges:", sg.edges())
	sub_graphs_nodes[i] = list(sg.nodes(data=False))
	pos = nx.spring_layout(sg)
	c = []
	c.append(center(sg)[0])
	for node in sg.nodes(data=False):
		total_cost += g.graph[c[0]][node]
	nx.draw_networkx_nodes(sg, pos, nodelist=set(sg.nodes) - set(c), node_size=50)
	nx.draw_networkx_edges(sg, pos)
	nx.draw_networkx_nodes(sg, pos, nodelist=c, node_color='r', node_size=50)
	nx.draw_networkx_labels(sg, pos, font_size=4)
	plt.savefig('Subgraph_'+str(i)+'_blob.png', dpi=150)
	plt.close()


print('Total cost of the solution is: ', total_cost)

print('\n-----Checking using built-in functions of Networkx------')

G_check = nx.from_numpy_array(np.array(D))
MST_check = nx.algorithms.tree.mst.minimum_spanning_tree(G_check, algorithm='prim')
edges_check = list(MST_check.edges.data("weight"))

# Remove the k-1 edges with largest weights in the MST
for i in range(config.k-1):
	edge_remove = max(edges_check, key=lambda t: t[2])
	edges_check.remove(edge_remove)
	MST_check.remove_edge(edge_remove[0], edge_remove[1])

# Extracting subgraphs from the MST - k-1 edges with largest weights
sub_graphs_check = (MST_check.subgraph(c) for c in nx.connected_components(MST_check))

# Printing the result and the graphs
sg_nodes = {}
for i, sg in enumerate(sub_graphs_check):
	sg_nodes[i] = list(sg.nodes(data=False))
	print("subgraph {} has {} nodes".format(i, sg.number_of_nodes()))
	print("\tNodes:", sg.nodes(data=False))
	print("\tEdges:", sg.edges())

# Printing check result
checker = 0
for k, v in sg_nodes.items():
	checker += bool(set(v).difference(sub_graphs_nodes[k]))
if checker == 0:
	print('\n-----MST subpgraphs checks passed-----')
else:
	print('\n-----WARNING: MST subgraphs checks failed!-----')

