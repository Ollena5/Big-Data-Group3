import networkx as nx
import matplotlib.pyplot as plt

# Create a 3x3 grid graph
G = nx.grid_2d_graph(3, 3)

# Add diagonal edges
for i in range(3):
    for j in range(3):
        if (i + 1 < 3) and (j + 1 < 3):
            G.add_edge((i, j), (i + 1, j + 1))
        if (i - 1 >= 0) and (j + 1 < 3):
            G.add_edge((i, j), (i - 1, j + 1))
        if (i + 1 < 3) and (j - 1 >= 0):
            G.add_edge((i, j), (i + 1, j - 1))
        if (i - 1 >= 0) and (j - 1 >= 0):
            G.add_edge((i, j), (i - 1, j - 1))

# Draw the graph
pos = {(x, y): (y, -x) for x, y in G.nodes()}  # Adjusting positions for better visualization
nx.draw(G, pos, with_labels=True, node_size=300, node_color='lightblue', font_size=10)

# Display the graph
plt.show()
