import json
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# ==========================================================
# PATHS
# ==========================================================

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    ROOT
    / "data"
    / "processed"
    / "dialogues_v5_semantic_clusters.parquet"
)

OUTPUT_DIR = (
    ROOT
    / "outputs"
    / "graphs"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================================
# LOAD DATA
# ==========================================================

print("Loading corpus...")

df = pd.read_parquet(INPUT_FILE)

print("Rows:", len(df))

# ==========================================================
# GRAPH
# ==========================================================

G = nx.Graph()

# ==========================================================
# CHARACTER -> EMOTION
# ==========================================================

for _, row in df.iterrows():

    character = str(row["character"])
    emotion = str(row["emotion"])

    if character == "unknown":
        continue

    G.add_node(
        character,
        node_type="character"
    )

    G.add_node(
        emotion,
        node_type="emotion"
    )

    if G.has_edge(character, emotion):

        G[character][emotion]["weight"] += 1

    else:

        G.add_edge(
            character,
            emotion,
            relation="expresses",
            weight=1
        )

# ==========================================================
# CHARACTER -> CLUSTER
# ==========================================================

for _, row in df.iterrows():

    character = str(row["character"])

    if character == "unknown":
        continue

    cluster = f"cluster_{row['semantic_cluster']}"

    G.add_node(
        cluster,
        node_type="cluster"
    )

    if G.has_edge(character, cluster):

        G[character][cluster]["weight"] += 1

    else:

        G.add_edge(
            character,
            cluster,
            relation="appears_in",
            weight=1
        )

# ==========================================================
# EMOTION -> CLUSTER
# ==========================================================

for _, row in df.iterrows():

    emotion = str(row["emotion"])
    cluster = f"cluster_{row['semantic_cluster']}"

    if G.has_edge(emotion, cluster):

        G[emotion][cluster]["weight"] += 1

    else:

        G.add_edge(
            emotion,
            cluster,
            relation="associated_with",
            weight=1
        )

# ==========================================================
# METRICS
# ==========================================================

print("Computing graph metrics...")

pagerank = nx.pagerank(G)

betweenness = nx.betweenness_centrality(G)

degree = dict(G.degree())

metrics = {
    "nodes": G.number_of_nodes(),
    "edges": G.number_of_edges(),
    "density": nx.density(G),
    "connected_components": nx.number_connected_components(G),
    "top_pagerank": sorted(
        pagerank.items(),
        key=lambda x: x[1],
        reverse=True
    )[:20],
    "top_betweenness": sorted(
        betweenness.items(),
        key=lambda x: x[1],
        reverse=True
    )[:20],
    "top_degree": sorted(
        degree.items(),
        key=lambda x: x[1],
        reverse=True
    )[:20]
}

# ==========================================================
# SAVE METRICS
# ==========================================================

metrics_file = (
    OUTPUT_DIR
    / "graph_metrics.json"
)

with open(
    metrics_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        metrics,
        f,
        indent=2,
        ensure_ascii=False
    )

# ==========================================================
# EXPORT GRAPH
# ==========================================================

print("Saving GraphML...")

nx.write_graphml(
    G,
    OUTPUT_DIR / "narrative_graph.graphml"
)

print("Saving GEXF...")

nx.write_gexf(
    G,
    OUTPUT_DIR / "narrative_graph.gexf"
)

# ==========================================================
# DRAW PNG
# ==========================================================

print("Drawing graph...")

plt.figure(
    figsize=(18, 18)
)

pos = nx.spring_layout(
    G,
    seed=42,
    k=0.5
)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=700,
    font_size=8
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "narrative_graph.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==========================================================
# SUMMARY
# ==========================================================

print("\nGraph generated successfully")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

print("\nOutputs:")

print(
    OUTPUT_DIR / "narrative_graph.graphml"
)

print(
    OUTPUT_DIR / "narrative_graph.gexf"
)

print(
    OUTPUT_DIR / "narrative_graph.png"
)

print(
    OUTPUT_DIR / "graph_metrics.json"
)