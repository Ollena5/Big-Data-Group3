from flask import Flask, render_template, request
import requests
import networkx as nx
import matplotlib.pyplot as plt
import mpld3

app = Flask(__name__)

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

@app.route('/')
def index():
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
            G.add_edge(protein1, protein2)

    # Draw the graph with a grid layout
    plt.figure(figsize=(10, 10))
    if(nx.is_eulerian(G)):
        nx.eulerize(G)
    pos = nx.spring_layout(G, seed=42)  # Use a low k value for grid-like layout

    # Select a protein
    selected_protein = request.args.get('selected_protein', default='TP53')

    # Adjust node and edge alpha values based on connectivity to the selected protein
    node_alpha = {node: 1.0 if node == selected_protein else 0.2 for node in G.nodes()}
    edge_alpha = {edge: 1 if edge == selected_protein else 0.2 for edge in G.edges()}
    edge_color = ["skyblue" if selected_protein in edge else "lightgray" for edge in G.edges()]
    edge_width = [3.0 if selected_protein in edge else 1.0 for edge in G.edges()]
    

    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="skyblue", alpha=node_alpha.values())
    nx.draw_networkx_edges(G, pos, edge_color=edge_color, width=edge_width, alpha=1)
    nx.draw_networkx_labels(G, pos)

    plt.axis("off")
    plt.title("Protein-Protein Interaction Network (Grid Layout)")
    plt.savefig('static/graph.png')  # Save the graph as a static file

    # Render the template with the graph and the list of buttons
    return render_template('index.html', proteins=proteins, selected_protein=selected_protein)

if __name__ == '__main__':
    app.run(debug=True)
