from flask import Flask, render_template, request
import requests
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import math

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
    proteins = [
        "TP53", "EGFR", "AKT1", "MAPK1", "PTEN", "MYC", "CDH1", "RB1", "JAK2",
        "BCL2", "VEGFA"
    ]
    # proteins = [
    #     "TP53", "EGFR", "AKT1", "MAPK1", "PTEN", "MYC", "CDH1", "RB1", "JAK2",
    #     "BCL2", "VEGFA", "KRAS", "PIK3CA", "STAT3", "BRCA1", "BRCA2", "ERBB2", "MTOR",
    #     "FLT3", "CTNNB1", "EGF", "FGFR1", "FGF2", "FGF7", "FGFR2", "FGF8", "FGFR3",
    #     "FGF9", "FGFR4", "FOXP3", "FOXL2", "FOXO1", "FOXO3", "FOXO4", "FOXO6", "FOXP1",
    #     "HGF", "MET", "HRAS", "KRAS", "NRAS", "RET", "RAF1", "MAP2K1", "MAP2K2", "MAPK3",
    #     "MAPK8", "MAPK9", "MAPK10", "MAPK11", "MAPK12", "MAPK13", "MAPK14", "MAP3K1", "MAP3K3",
    #     "MAP3K7", "MAP3K14", "MAP3K15", "MAP3K20", "MAP4K4", "MAP4K5", "MAP4K1", "MAP4K3", "MAP4K2",
    #     "MAP4K6", "MAP4K7", "MAP4K8", "MAP4K9", "MAP4K10", "MAP4K11", "MAP4K12", "MAP4K13", "MAP4K14",
    #     "MAP4K15", "MAP4K16", "MAP4K17", "MAP4K18", "MAP4K19", "MAP4K20", "MAP4K21", "MAP4K22", "MAP4K23",
    #     "MAP4K24", "MAP4K25", "MAP4K26", "MAP4K27", "MAP4K28", "MAP4K29", "MAP4K30", "MAP4K31", "MAP4K32",
    #     "MAP4K33", "MAP4K34", "MAP4K35", "MAP4K36", "MAP4K37", "MAP4K38", "MAP4K39", "MAP4K40", "MAP4K41",
    #     "MAP4K42", "MAP4K43", "MAP4K44", "MAP4K45", "MAP4K46", "MAP4K47", "MAP4K48", "MAP4K49", "MAP4K50"
    # ]

    # Get PPI data
    ppi_data = get_ppi_data(proteins)
    
    # Create a graph
    n = 3
    G = nx.sudoku_graph(n)
    mapping = dict(zip(G.nodes(), proteins))
    pos = dict(zip(list(G.nodes()), nx.grid_2d_graph(n * n, n * n)))

    # Draw the graph with a grid layout
    plt.figure(figsize=(12, 12))

    # Create a graph
    G = nx.Graph()

    # Add nodes
    G.add_nodes_from(proteins)

    # Add edges based on PPI data
    for line in ppi_data.split("\n"):
        if line.startswith("#"):
            continue
        cols = line.strip().split("\t")
        if len(cols) < 4:
            continue
        protein1, protein2 = cols[2], cols[3]
        if protein1 in proteins and protein2 in proteins:
            G.add_edge(protein1, protein2)

    # Filter out proteins with no edge connections
    G.add_nodes_from(node for node, degree in G.degree() if degree > 0)

       
    # Select a protein
    selected_protein = request.args.get('selected_protein', default='All Proteins')

    # Adjust node and edge alpha values based on connectivity to the selected protein
    node_alpha = {node: 1.0 if node == selected_protein else 0.2 for node in G.nodes()}
    edge_color = ["skyblue" if selected_protein in edge else "lightgray" for edge in G.edges()]
    edge_width = [3.0 if selected_protein in edge else 1.0 for edge in G.edges()]
    
    # Draw the network
    nx.draw(
        G,
        labels=mapping,
        pos=pos,
        with_labels=True,
        node_color="skyblue",
        alpha=list(node_alpha.values()),
        edge_color=edge_color,
        width=edge_width,
        node_size=1000,
    )

    plt.axis("off")
    plt.title("Protein-Protein Interaction Network (Grid Layout)")
    plt.savefig('static/graph.png')  # Save the graph as a static file

    # Render the template with the graph and the list of buttons
    return render_template('index.html', proteins=proteins, G=G)



if __name__ == '__main__':
    app.run(debug=True)
