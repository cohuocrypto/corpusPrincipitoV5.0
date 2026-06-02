import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from src.config import DATA_PROCESSED, OUTPUT_GRAPHS


def add_edge_weighted(G, a, b, relation):
    if G.has_edge(a, b):
        G[a][b]["weight"] += 1
    else:
        G.add_edge(a, b, relation=relation, weight=1)


def main():
    path = DATA_PROCESSED / "dialogues_analytic_matrix.parquet"
    if not path.exists():
        raise FileNotFoundError("Ejecuta primero scripts/03_embeddings_clusters.py")
    df = pd.read_parquet(path)
    G = nx.Graph()
    for _, row in df.iterrows():
        char = f"character:{row['character']}"
        emo = f"emotion:{row['emotion']}"
        cons = f"construct:{row['primary_construct']}"
        socio = f"sociotech:{row['sociotechnical_variable']}"
        cluster = f"cluster:{int(row['semantic_cluster'])}"
        for node, ntype in [(char, "character"), (emo, "emotion"), (cons, "construct"), (socio, "sociotechnical"), (cluster, "semantic_cluster")]:
            if node not in G:
                G.add_node(node, type=ntype)
        add_edge_weighted(G, char, emo, "expresses")
        add_edge_weighted(G, char, cons, "evokes_construct")
        add_edge_weighted(G, cons, socio, "maps_to_sociotechnical")
        add_edge_weighted(G, char, cluster, "belongs_to_cluster")
    graphml = OUTPUT_GRAPHS / "narrative_sociotechnical_graph.graphml"
    png = OUTPUT_GRAPHS / "narrative_sociotechnical_graph.png"
    nx.write_graphml(G, graphml)
    plt.figure(figsize=(16, 12))
    pos = nx.spring_layout(G, k=0.8, seed=42)
    sizes = [200 + 60 * G.degree(n) for n in G.nodes]
    widths = [max(0.5, G[u][v].get("weight", 1) / 3) for u, v in G.edges]
    nx.draw_networkx_nodes(G, pos, node_size=sizes, alpha=0.85)
    nx.draw_networkx_edges(G, pos, width=widths, alpha=0.35)
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(png, dpi=220)
    plt.close()
    print("OK 06_draw_graph")
    print("nodes:", G.number_of_nodes(), "edges:", G.number_of_edges())
    print("graphml:", graphml)
    print("png:", png)

if __name__ == "__main__":
    main()
