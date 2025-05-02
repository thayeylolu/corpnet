# scripts/demo.py

import networkx as nx
from pyvis.network import Network

def visualize_graph(graph_path, output_html="output/corpnet_viz.html"):
    print(f"📂 Loading graph from {graph_path}")
    G = nx.read_graphml(graph_path)

    net = Network(height="800px", width="100%", notebook=False, directed=True)
    net.force_atlas_2based()

    for node, attrs in G.nodes(data=True):
        label = attrs.get("name", node)
        group = attrs.get("type", "unknown")
        title = f"{group.upper()}: {label}"
        net.add_node(node, label=label, title=title, group=group)

    for src, tgt, edge_attrs in G.edges(data=True):
        role = edge_attrs.get("role", "relation")
        net.add_edge(src, tgt, title=role, label=role)

    print(f"🖼️  Saving visualization to {output_html}")
    net.show(output_html)

if __name__ == "__main__":
    visualize_graph("output/corpnet.graphml")
