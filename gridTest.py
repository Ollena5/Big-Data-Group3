

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

# Check if all proteins in the `proteins` list have at least one interaction
for protein in proteins:
    if not any(protein in edge for edge in G.edges):
        print(f"Protein {protein} does not have any interactions in the PPI data.")

# Select a protein
selected_protein = "TP53"

# Adjust node and edge alpha values based on connectivity to the selected protein
node_alpha = {node: 1.0 if node == selected_protein else 0.2 for node in G.nodes()}
edge_alpha = {edge: 1.0 if selected_protein in edge else 0.2 for edge in G.edges()}
pos = nx.grid_2d_graph(10, 10)


nx.draw_networkx_nodes(G, pos=pos, node_size=2000, node_color="skyblue", alpha=node_alpha.values())
nx.draw_networkx_edges(G, pos, alpha=0.2)  # Use a single scalar value for alpha
nx.draw_networkx_labels(G, pos)


plt.axis("off")
plt.title("Protein-Protein Interaction Network on a Grid Layout")
plt.show()

