import requests
import networkx as nx
import matplotlib.pyplot as plt

# Function to retrieve PPI data from STRING API
def get_ppi_data(proteins, confidence=0.1, save_to_file=True):
    url = "https://string-db.org/api/tsv/network"
    params = {
        "identifiers": "%0d".join(proteins),
        "species": "9606",  # Human species
        "caller_identity": "KSUBigDataGroup3",
        "network_flavor": "confidence",
        "required_score": confidence,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    tsv_data = response.text
    
    if save_to_file:
        with open('ppi_data.tsv', 'w') as f:
            f.write(tsv_data)
    
    return tsv_data

# Example proteins
proteins = ["TP53", "EGFR", "AKT1", "MAPK1", "PTEN", "MYC", "CDH1", "RB1", "JAK2"]

# Get PPI data
ppi_data = get_ppi_data(proteins)

# Create a graph
G = nx.Graph()

# Add nodes
G.add_nodes_from(proteins)

# Add edges
for line in ppi_data.split("\n"):
    if line.startswith("#"):
        continue
    cols = line.strip().split("\t")
    if len(cols) < 4:  # Ensure there are enough columns
        continue
    protein1, protein2 = cols[2], cols[3]  # Use the preferred name columns
    if protein1 in proteins and protein2 in proteins:
        G.add_edge(protein1, protein2)

# Create a 2D grid graph
G_grid = nx.grid_2d_graph(10, 10)


grid_size = 10  # Adjust grid size if necessary
pos_grid = {(i, j): (i, j) for i in range(grid_size) for j in range(grid_size)}
protein_positions = list(pos_grid.values())[:len(proteins)]
pos_overlay = {protein: position for protein, position in zip(proteins, protein_positions)}

# Draw the grid graph using the defined positions
nx.draw(G_grid, pos=pos_grid, with_labels=True, node_size=500, node_color="skyblue", edge_color='gray')

# Overlay the protein nodes from the PPI data onto the grid
# Adjust the positions to center them on the grid cells
# This will place each node in its own cell on the grid
for node, (x, y) in pos_overlay.items():
    pos_overlay[node] = (x + 0.5, y + 0.5)

# Draw the protein nodes with labels
nx.draw_networkx_nodes(G, pos=pos_overlay, node_size=500, node_color="red")
nx.draw_networkx_labels(G, pos=pos_overlay)

# Draw the edges of the PPI graph
nx.draw_networkx_edges(G, pos=pos_overlay, edge_color='black')

plt.axis("off")
plt.title("Protein-Protein Interaction Network on a Grid Layout")
plt.show()