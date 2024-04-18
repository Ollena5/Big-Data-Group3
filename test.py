import networkx as nx
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins

# Create a graph
G = nx.Graph()
G.add_nodes_from(["A", "B", "C"])
G.add_edges_from([("A", "B"), ("B", "C")])

# Create a plot
fig, ax = plt.subplots(figsize=(6, 4))

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, ax=ax)

# Add interactive tooltip
tooltip = plugins.PointHTMLTooltip(G, labels=[f"{node}" for node in G.nodes()])
plugins.connect(fig, tooltip)

plt.show()
