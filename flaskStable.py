from flask import Flask, render_template, request, session
import requests
import py4cytoscape as p4c
import networkx as nx 

app = Flask(__name__)
app.secret_key = 'KSUBigDataGroup3'

# Default array of proteins
defaultProteins = [
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

setupCompleted = False

# Function to retrieve PPI data from STRING API
def getPpiData(proteins, species="9606", confidence=0.1, saveToFile=True):
    url = "https://string-db.org/api/tsv/network"
    params = {
        "identifiers": "%0d".join(proteins),
        "species": species,  # Human species
        "caller_identity": "KSUBigDataGroup3",
        "network_flavor": "confidence",
        "required_score": confidence,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    tsvData = response.text
    
    if saveToFile:
        with open('ppi_data.tsv', 'w') as f:
            f.write(tsvData)
    
    return tsvData

def visualizeNetwork(G, selectedProtein):
    p4c.create_network_from_networkx(G, title='baseNetwork')
    p4c.set_node_color_default(new_color='#D20103')
    p4c.set_node_fill_opacity_default(new_opacity=175)
    p4c.scale_layout(axis='Both Axes', scale_factor=100)
    suid = p4c.get_network_suid()
    if(selectedProtein == 'all'):
        p4c.layout_network(layout_name='grid', network=suid)
    elif(selectedProtein == "prune"):
        p4c.select_all_edges(network=suid)
        p4c.create_subnetwork(edges='selected', subnetwork_name='prunedNetwork', network=suid)
        pruneSuid = p4c.get_network_suid()
        p4c.layout_network(layout_name='grid', network=pruneSuid)
    else:
        nodeSUID = p4c.node_name_to_node_suid(selectedProtein, network=suid)
        p4c.select_nodes(nodeSUID, network=suid)
        p4c.set_node_color_bypass(nodeSUID, network=suid, new_colors='#0DB801')
        p4c.select_edges_adjacent_to_selected_nodes(network=suid)
        p4c.create_subnetwork(edges='selected', nodes='selected', nodes_by_col='COMMON',subnetwork_name='selectedNetwork', network=suid)
        selectedSuid = p4c.get_network_suid()
        p4c.layout_network(layout_name='grid', network=selectedSuid)
    
    # Display the network in Cytoscape
    p4c.export_image(filename='static/graph.png', overwrite_file=True, hide_labels=False, transparent_background=True)
    p4c.delete_all_networks()


@app.before_request
def setup():
    global setupCompleted
    if not setupCompleted:
        session['proteins'] = defaultProteins
        setupCompleted = True


@app.route('/')
def index():
    proteins = session.get('proteins', [])
    enteredProtein = request.args.get('enteredProtein', '')
    if enteredProtein:
        if ',' in enteredProtein:
            enteredProteins = enteredProtein.split(',')
            for protein in enteredProteins:
                if protein.strip() not in proteins:
                    proteins.append(protein.strip())
        else:
            if enteredProtein.strip() not in proteins:
                proteins.append(enteredProtein.strip())
        session['proteins'] = proteins
    # Get PPI data
    ppiData = getPpiData(session['proteins'])

    # Create a graph
    G = nx.Graph()

    # Add nodes
    G.add_nodes_from(session['proteins'])
        
    # Add edges based on PPI data
    for line in ppiData.split("\n"):
        if line.startswith("#"):
            continue
        cols = line.strip().split("\t")
        if len(cols) < 4:  # Ensure there are enough columns
            continue
        protein1, protein2 = cols[2], cols[3]  # Use the preferred name columns
        if protein1 in session['proteins'] and protein2 in session['proteins']:
            G.add_edge(protein1, protein2)

    # Visualize the network using Cytoscape and the grid layout algorithm
    selectedProtein = request.args.get('selectedProtein', default='all') 
    visualizeNetwork(G, selectedProtein)

    return render_template('index.html', proteins=session['proteins'], G=G)


if __name__ == '__main__':
    app.run(debug=True)
