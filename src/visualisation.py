# src/visualisation.py

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def appliquer_layouts(G):
    layouts = {}
    layouts['spring'] = nx.spring_layout(G, k=2, iterations=50, seed=42)
    layouts['circular'] = nx.circular_layout(G)
    layouts['kamada_kawai'] = nx.kamada_kawai_layout(G)
    groupes = {}
    for node in G.nodes():
        groupe = G.nodes[node].get('groupe', 'Inconnu')
        if groupe not in groupes:
            groupes[groupe] = []
        groupes[groupe].append(node)
    shells = list(groupes.values())
    layouts['shell'] = nx.shell_layout(G, nlist=shells)
    layouts['spectral'] = nx.spectral_layout(G)
    return layouts

def visualiser_layout_unique(G, layout, titre, nom_fichier):
    plt.figure(figsize=(12, 10))
    couleurs_groupes = {
        'Etudiants': '#FF6B6B',
        'Professionnels': '#4ECDC4',
        'Artistes': '#FFE66D'
    }
    node_colors = [couleurs_groupes.get(G.nodes[n].get('groupe', 'Inconnu'), '#95A5A6') for n in G.nodes()]
    degrees = dict(G.degree())
    node_sizes = [300 + degrees[n] * 100 for n in G.nodes()]
    nx.draw_networkx_nodes(G, layout, node_color=node_colors, node_size=node_sizes, alpha=0.8)
    nx.draw_networkx_edges(G, layout, alpha=0.5, width=1.5, edge_color='gray')
    labels = {n: G.nodes[n].get('nom', str(n)) for n in G.nodes()}
    nx.draw_networkx_labels(G, layout, labels, font_size=8, font_weight='bold')
    plt.title(titre, fontsize=14, fontweight='bold')
    plt.axis('off')
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=color, label=groupe) for groupe, color in couleurs_groupes.items()]
    plt.legend(handles=legend_elements, loc='upper left')
    plt.tight_layout()
    plt.savefig(f"output/images/{nom_fichier}.png", dpi=300, bbox_inches='tight')
    plt.close()

def visualiser_tous_layouts(G, layouts):
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    couleurs_groupes = {
        'Etudiants': '#FF6B6B',
        'Professionnels': '#4ECDC4',
        'Artistes': '#FFE66D'
    }
    node_colors = [couleurs_groupes.get(G.nodes[n].get('groupe', 'Inconnu'), '#95A5A6') for n in G.nodes()]
    for idx, (nom, pos) in enumerate(layouts.items()):
        if idx >= 6:
            break
        ax = axes[idx]
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=200, alpha=0.8, ax=ax)
        nx.draw_networkx_edges(G, pos, alpha=0.4, width=1, edge_color='gray', ax=ax)
        ax.set_title(f"Layout: {nom.replace('_', ' ').title()}", fontsize=12)
        ax.axis('off')
    if len(layouts) < 6:
        axes[-1].axis('off')
    plt.suptitle("Comparaison des differentes techniques de Layout", fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig("output/images/comparaison_layouts.png", dpi=300, bbox_inches='tight')
    plt.close()
