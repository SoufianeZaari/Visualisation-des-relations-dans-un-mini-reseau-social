# src/reduction_dimension.py

import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import networkx as nx
import matplotlib.pyplot as plt

def creer_matrice_caracteristiques(G):
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    clustering_coef = nx.clustering(G)
    nodes = list(G.nodes())
    features = []
    for node in nodes:
        feature_vector = [
            degree_centrality[node],
            betweenness_centrality[node],
            closeness_centrality[node],
            clustering_coef[node],
            G.degree(node),
        ]
        features.append(feature_vector)
    return np.array(features), nodes

def appliquer_pca(G, n_components=2):
    features, nodes = creer_matrice_caracteristiques(G)
    pca = PCA(n_components=n_components)
    positions_pca = pca.fit_transform(features)
    pos = {nodes[i]: positions_pca[i] for i in range(len(nodes))}
    variance_expliquee = pca.explained_variance_ratio_
    return pos, variance_expliquee

def appliquer_tsne(G, n_components=2, perplexity=5):
    features, nodes = creer_matrice_caracteristiques(G)
    tsne = TSNE(n_components=n_components, perplexity=perplexity, random_state=42, max_iter=1000)
    positions_tsne = tsne.fit_transform(features)
    pos = {nodes[i]: positions_tsne[i] for i in range(len(nodes))}
    return pos

def visualiser_reduction_dimension(G, pos_pca, pos_tsne, variance_pca):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    couleurs_groupes = {
        'Etudiants': '#FF6B6B',
        'Professionnels': '#4ECDC4',
        'Artistes': '#FFE66D'
    }
    node_colors = [couleurs_groupes.get(G.nodes[n].get('groupe', 'Inconnu'), '#95A5A6') for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos_pca, node_color=node_colors, node_size=300, alpha=0.8, ax=ax1)
    nx.draw_networkx_edges(G, pos_pca, alpha=0.4, width=1, edge_color='gray', ax=ax1)
    labels = {n: G.nodes[n].get('nom', str(n)) for n in G.nodes()}
    nx.draw_networkx_labels(G, pos_pca, labels, font_size=7, ax=ax1)
    ax1.set_title(f"PCA Layout\nVariance expliquee: {sum(variance_pca)*100:.1f}%", fontsize=12)
    ax1.axis('off')
    nx.draw_networkx_nodes(G, pos_tsne, node_color=node_colors, node_size=300, alpha=0.8, ax=ax2)
    nx.draw_networkx_edges(G, pos_tsne, alpha=0.4, width=1, edge_color='gray', ax=ax2)
    nx.draw_networkx_labels(G, pos_tsne, labels, font_size=7, ax=ax2)
    ax2.set_title("t-SNE Layout", fontsize=12)
    ax2.axis('off')
    plt.suptitle("Reduction de Dimension : PCA vs t-SNE", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig("output/images/reduction_dimension.png", dpi=300, bbox_inches='tight')
    plt.close()
