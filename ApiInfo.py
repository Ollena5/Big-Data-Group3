#https://string-db.org/api/[output-format]/get_string_ids?identifiers=[your_identifiers]&[optional_parameters]
# import requests ## python -m pip install requests
# response = requests.get("https://string-db.org/api/image/network?identifiers=PTCH1%0dSHH%0dGLI1%0dSMO%0dGLI3")
# with open('string_network.png', 'wb') as fh:
#     fh.write(response.content)

#Some scratch code I got from chatGPT
import requests
import networkx as nx
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins

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
#, "VEGFA"
# Example proteins
proteins = ["TP53", "EGFR", "AKT1", "MAPK1", "PTEN", "MYC", "CDH1", "RB1", "JAK2"]


# Get PPI data
ppi_data = get_ppi_data(proteins)

# Create a graph
G = nx.Graph()

# Add nodes
G.add_nodes_from(proteins)

# Add edges based on PPI data
for line in ppi_data.split("\n"):
    if line.startswith("#"):
        continue
    cols = line.strip().split("\t")
    if len(cols) < 4:  # Ensure there are enough columns
        continue
    protein1, protein2 = cols[2], cols[3]  # Use the preferred name columns
    if protein1 in proteins and protein2 in proteins:
        print(f"Adding edge between {protein1} and {protein2}")
        G.add_edge(protein1, protein2)


# Draw the graph with a grid layout
plt.figure(figsize=(10, 10))
print(f"Is G eulerian? {nx.is_eulerian(G)}" )
if(nx.is_eulerian(G)):
    nx.eulerize(G)
pos = nx.spring_layout(G, seed=42)  # Use a low k value for grid-like layout

nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="skyblue")
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos)

plt.axis("off")
plt.title("Protein-Protein Interaction Network (Grid Layout)")
plt.show()
