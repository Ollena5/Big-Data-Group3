# #https://string-db.org/api/[output-format]/get_string_ids?identifiers=[your_identifiers]&[optional_parameters]
# # import requests ## python -m pip install requests
# # response = requests.get("https://string-db.org/api/image/network?identifiers=PTCH1%0dSHH%0dGLI1%0dSMO%0dGLI3")
# # with open('string_network.png', 'wb') as fh:
# #     fh.write(response.content)

# #Some scratch code I got from chatGPT
# import requests
# import networkx as nx
# import matplotlib.pyplot as plt
# import mpld3
# from mpld3 import plugins

# # Function to retrieve PPI data from STRING API
# def get_ppi_data(proteins, confidence=0.1, save_to_file=True):
#     url = "https://string-db.org/api/tsv/network"
#     params = {
#         "identifiers": "%0d".join(proteins),
#         "species": "9606",  # Human species
#         "caller_identity": "KSUBigDataGroup3",
#         "network_flavor": "confidence",
#         "required_score": confidence,
#     }
#     response = requests.post(url, params=params)
#     response.raise_for_status()
#     tsv_data = response.text
    
#     if save_to_file:
#         with open('ppi_data.tsv', 'w') as f:
#             f.write(tsv_data)
    
#     return tsv_data
# #, "VEGFA"
# # Example proteins
# proteins = ["TP53", "EGFR", "AKT1", "MAPK1", "PTEN", "MYC", "CDH1", "RB1", "JAK2"]


# # Get PPI data
# ppi_data = get_ppi_data(proteins)

# # Create a graph
# G = nx.Graph()

# # Add nodes
# G.add_nodes_from(proteins)

# # Add edges based on PPI data
# for line in ppi_data.split("\n"):
#     if line.startswith("#"):
#         continue
#     cols = line.strip().split("\t")
#     if len(cols) < 4:  # Ensure there are enough columns
#         continue
#     protein1, protein2 = cols[2], cols[3]  # Use the preferred name columns
#     if protein1 in proteins and protein2 in proteins:
#         print(f"Adding edge between {protein1} and {protein2}")
#         G.add_edge(protein1, protein2)


# # Draw the graph with a grid layout
# plt.figure(figsize=(10, 10))
# print(f"Is G eulerian? {nx.is_eulerian(G)}" )
# if(nx.is_eulerian(G)):
#     nx.eulerize(G)
# pos = nx.spring_layout(G, seed=42)  # Use a low k value for grid-like layout

# nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="skyblue")
# nx.draw_networkx_edges(G, pos, alpha=0.5)
# nx.draw_networkx_labels(G, pos)

# plt.axis("off")
# plt.title("Protein-Protein Interaction Network (Grid Layout)")
# plt.show()
import requests
import networkx as nx
import matplotlib.pyplot as plt
import mpld3
import scipy as sp
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

# Example proteins
# proteins = ["TP53", "EGFR", "AKT1", "MAPK1", "PTEN", "MYC", "CDH1", "RB1", "JAK2"]
proteins = [
        "TP53", "EGFR", "AKT1", "MAPK1", "PTEN", "MYC", "CDH1", "RB1", "JAK2",
        "BCL2", "VEGFA", "KRAS", "PIK3CA", "STAT3", "BRCA1", "BRCA2", "ERBB2", "MTOR",
        "FLT3", "CTNNB1", "EGF", "FGFR1", "FGF2", "FGF7", "FGFR2", "FGF8", "FGFR3",
        "FGF9", "FGFR4", "FOXP3", "FOXL2", "FOXO1", "FOXO3", "FOXO4", "FOXO6", "FOXP1",
        "HGF", "MET", "HRAS", "KRAS", "NRAS", "RET", "RAF1", "MAP2K1", "MAP2K2", "MAPK3",
        "MAPK8", "MAPK9", "MAPK10", "MAPK11", "MAPK12", "MAPK13", "MAPK14", "MAP3K1", "MAP3K3",
        "MAP3K7", "MAP3K14", "MAP3K15", "MAP3K20", "MAP4K4", "MAP4K5", "MAP4K1", "MAP4K3", "MAP4K2",
        "MAP4K6", "MAP4K7", "MAP4K8", "MAP4K9", "MAP4K10", "MAP4K11", "MAP4K12", "MAP4K13", "MAP4K14",
        "MAP4K15", "MAP4K16", "MAP4K17", "MAP4K18", "MAP4K19", "MAP4K20", "MAP4K21", "MAP4K22", "MAP4K23",
        "MAP4K24", "MAP4K25", "MAP4K26", "MAP4K27", "MAP4K28", "MAP4K29", "MAP4K30", "MAP4K31", "MAP4K32",
        "MAP4K33", "MAP4K34", "MAP4K35", "MAP4K36", "MAP4K37", "MAP4K38", "MAP4K39", "MAP4K40", "MAP4K41",
        "MAP4K42", "MAP4K43", "MAP4K44", "MAP4K45", "MAP4K46", "MAP4K47", "MAP4K48", "MAP4K49", "MAP4K50"
    ]
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
        G.add_edge(protein1, protein2)
        
G.add_nodes_from(node for node, degree in G.degree() if degree > 0)

# Draw the graph with a grid layout
plt.figure(figsize=(10, 10))
if(nx.is_eulerian(G)):
    nx.eulerize(G)
pos = nx.kamada_kawai_layout(G)  # Use a low k value for grid-like layout

# Select a protein
selected_protein = "TP53"

# Adjust node and edge alpha values based on connectivity to the selected protein
node_alpha = {node: 1.0 if node == selected_protein else 0.2 for node in G.nodes()}
edge_alpha = {edge: 1.0 if selected_protein in edge else 0.2 for edge in G.edges()}

nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="skyblue", alpha=node_alpha.values())
nx.draw_networkx_edges(G, pos, alpha=0.2)  # Use a single scalar value for alpha
nx.draw_networkx_labels(G, pos)

plt.axis("off")
plt.title("Protein-Protein Interaction Network (Grid Layout)")
plt.show()

