#https://string-db.org/api/[output-format]/get_string_ids?identifiers=[your_identifiers]&[optional_parameters]
# import requests ## python -m pip install requests
# response = requests.get("https://string-db.org/api/image/network?identifiers=PTCH1%0dSHH%0dGLI1%0dSMO%0dGLI3")
# with open('string_network.png', 'wb') as fh:
#     fh.write(response.content)

#Some scratch code I got from chatGPT
import requests
import networkx as nx
import matplotlib.pyplot as plt

# Function to retrieve PPI data from STRING API
def get_ppi_data(proteins, confidence=0.7):
    url = "https://string-db.org/api/tsv/network"
    params = {
        "identifiers": "%0d".join(proteins),
        "species": "9606",  # Human species
        "caller_identity": "exampleCaller",
        "network_flavor": "confidence",
        "required_score": confidence,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.text

# Example proteins
proteins = ["ARF6", "BRCA1", "TP53"]

# Get PPI data
ppi_data = get_ppi_data(proteins)

# Create a graph
G = nx.Graph()

# Add nodes and edges from PPI data
for line in ppi_data.split("\n"):
    if line.startswith("#"):
        continue
    cols = line.strip().split("\t")
    if len(cols) < 3:
        continue
    protein1, protein2, _ = cols[:3]
    G.add_edge(protein1, protein2)

# Compute the layout using a grid layout algorithm
pos = nx.spring_layout(G)

# Plot the graph
plt.figure(figsize=(8, 8))
nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="skyblue")
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos)
plt.axis("off")
plt.title("Protein-Protein Interaction Network")
plt.show()
