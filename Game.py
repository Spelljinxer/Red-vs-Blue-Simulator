import networkx as nx
import matplotlib.pyplot as plt
# import csv

# with open('tests/network-2.csv', 'r') as csvfile:
#     reader = csv.reader(csvfile)
#     network = list(reader)

# node_num = len(network)
# G = nx.erdos_renyi_graph(node_num, 0.1)
# nx.draw(G, with_labels=True, font_weight='bold')
# plt.show()

num_nodes = int(input("Enter number of nodes: "))
num_edges = int(input("Enter number of edges: "))

G = nx.erdos_renyi_graph(num_nodes, num_edges)
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()