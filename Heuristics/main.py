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
parser.add_argument('-c', '--configFile', nargs='?', type=Path,
					default=Path(__file__).parent / 'blob.dat', help='specifies the config file')
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
	nodes.append(i)
	edges.append((i, links[i], g.graph[i][links[i]]))


MST = nx.Graph()
MST.add_nodes_from(nodes)
for node1, node2, weight in edges:
	MST.add_edge(node1, node2, weight=weight)
nx.draw_networkx(MST, node_size=50, font_size=4)
plt.savefig('Graph_MST_bloob.png', dpi=150)
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
for i, sg in enumerate(sub_graphs):
	print("subgraph {} has {} nodes".format(i, sg.number_of_nodes()))
	print("\tNodes:", sg.nodes(data=False))
	print("\tEdges:", sg.edges())
	pos = nx.spring_layout(sg)
	c = []
	c.append(center(sg)[0])
	for node in sg.nodes(data=False):
		total_cost += g.graph[c[0]][node]
	nx.draw_networkx_nodes(sg, pos, nodelist=set(sg.nodes) - set(c), node_size=50)
	nx.draw_networkx_edges(sg, pos)
	nx.draw_networkx_nodes(sg, pos, nodelist=c, node_color='r', node_size=50)
	nx.draw_networkx_labels(sg, pos, font_size=4)
	plt.savefig('Subgraph_'+str(i)+'_bloob.png', dpi=150)
	plt.close()


print('Total cost of the solution is: ', total_cost)
print('-----Checking using built in functions of networkx------')

G2 = nx.Graph()
i = 1
for row in D:
	j=1
	for item in row:
		G2.add_edge(i, j, weight=item)
		j+=1
	i+=1

T=nx.minimum_spanning_tree(G2)

edges2 = list(T.edges(data=True))
for i in range(config.k-1):
	edge_remove = max(edges2, key=lambda t: t[2]['weight'])
	edges2.remove(edge_remove)
	T.remove_edge(edge_remove[0], edge_remove[1])

# Extracting subgraphs from the MST - k-1 edges with largest weights
sub_graphs = (T.subgraph(c) for c in nx.connected_components(T))

# Printing the result and the graphs
for i, sg in enumerate(sub_graphs):
	print("subgraph {} has {} nodes".format(i, sg.number_of_nodes()))
	print("\tNodes:", sg.nodes(data=False))
	print("\tEdges:", sg.edges())
