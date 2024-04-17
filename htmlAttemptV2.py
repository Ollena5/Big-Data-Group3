
import requests
import matplotlib.pyplot as plt
import networkx as nx
import mpld3
from mpld3 import plugins

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
proteins = ["TP53", "EGFR", "AKT1", "MAPK1", "PTEN", "MYC", "CDH1", "RB1", "VEGFA", "JAK2"]

# Get PPI data
ppi_data = get_ppi_data(proteins)

# Create a graph
G = nx.Graph()

# Add edges based on PPI data
for line in ppi_data.split("\n"):
    if line.startswith("#"):
        continue
    cols = line.strip().split("\t")
    if len(cols) < 3:
        continue
    protein1, protein2, _ = cols[:3]
    if protein1 in proteins and protein2 in proteins:
        G.add_edge(protein1, protein2)

# Draw the graph with a spring layout
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=12, font_color="black", font_weight="bold")
plt.title("Protein-Protein Interaction Network (Spring Layout)")

# Store node positions in a dictionary
pos_dict = {node: (pos[node][0], pos[node][1]) for node in G.nodes()}

# Convert the plot to an interactive HTML page with preserved positions
fig_html = mpld3.fig_to_html(plt.gcf(), d3_url=None, mpld3_url=None, no_extras=True, figid=None, use_http=False, template_type='general')

# Create JavaScript for filtering graph based on selected protein
js_code = """
<script>
function filterGraph(protein) {
    var nodes = document.getElementsByClassName("node");
    for (var i = 0; i < nodes.length; i++) {
        if (protein !== 'All' && nodes[i].textContent !== protein && nodes[i].style.display !== 'none') {
            nodes[i].style.display = 'none';
        } else if (protein === 'All' && nodes[i].style.display === 'none') {
            nodes[i].style.display = 'inline';
        } else if (protein !== 'All' && nodes[i].textContent === protein && nodes[i].style.display === 'none') {
            nodes[i].style.display = 'inline';
        }
    }
}
</script>
"""

# Create buttons for each protein and an "All" button to show all nodes
buttons = "<button onclick='filterGraph(\"All\")'>All</button>"
for protein in proteins:
    buttons += f"<button onclick='filterGraph(\"{protein}\")'>{protein}</button>"

# Create HTML page with graph and buttons
html_page = f"""
<html>
<head>
{js_code}
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
{fig_html}
<div id="graph-container">
{buttons}
</div>
</body>
</html>
"""

# Save the HTML page
with open("protein_interactions.html", "w") as f:
    f.write(html_page)

# Display the HTML page
mpld3.display()
