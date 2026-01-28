# src/analyse.py

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def analyser_reseau(G):
    analyse = {}
    analyse['nb_noeuds'] = G.number_of_nodes()
    analyse['nb_aretes'] = G.number_of_edges()
    analyse['densite'] = nx.density(G)
    analyse['diametre'] = nx.diameter(G) if nx.is_connected(G) else "Non connexe"
    analyse['rayon'] = nx.radius(G) if nx.is_connected(G) else "Non connexe"
    analyse['degre_moyen'] = sum(dict(G.degree()).values()) / G.number_of_nodes()
    analyse['clustering_moyen'] = nx.average_clustering(G)
    analyse['clustering_global'] = nx.transitivity(G)
    analyse['degree_centrality'] = nx.degree_centrality(G)
    analyse['betweenness_centrality'] = nx.betweenness_centrality(G)
    analyse['closeness_centrality'] = nx.closeness_centrality(G)
    analyse['eigenvector_centrality'] = nx.eigenvector_centrality(G, max_iter=1000)
    from networkx.algorithms import community
    communities = community.greedy_modularity_communities(G)
    analyse['communautes'] = [list(c) for c in communities]
    analyse['nb_communautes'] = len(communities)
    analyse['modularite'] = community.modularity(G, communities)
    top_degree = sorted(analyse['degree_centrality'].items(), key=lambda x: x[1], reverse=True)[:5]
    top_betweenness = sorted(analyse['betweenness_centrality'].items(), key=lambda x: x[1], reverse=True)[:5]
    analyse['top_degree'] = [(G.nodes[n]['nom'], round(v, 3)) for n, v in top_degree]
    analyse['top_betweenness'] = [(G.nodes[n]['nom'], round(v, 3)) for n, v in top_betweenness]
    return analyse

def afficher_rapport_analyse(analyse, G):
    print("=" * 60)
    print("RAPPORT D'ANALYSE DU RESEAU SOCIAL")
    print("=" * 60)
    print("\nMETRIQUES GLOBALES")
    print("-" * 40)
    print(f"Nombre de noeuds (utilisateurs): {analyse['nb_noeuds']}")
    print(f"Nombre d'aretes (relations): {analyse['nb_aretes']}")
    print(f"Densite du reseau: {analyse['densite']:.4f}")
    print(f"Diametre: {analyse['diametre']}")
    print(f"Rayon: {analyse['rayon']}")
    print(f"Degre moyen: {analyse['degre_moyen']:.2f}")
    print("\nCLUSTERING")
    print("-" * 40)
    print(f"Coefficient de clustering moyen: {analyse['clustering_moyen']:.4f}")
    print(f"Coefficient de clustering global: {analyse['clustering_global']:.4f}")
    print("\nCOMMUNAUTES DETECTEES")
    print("-" * 40)
    print(f"Nombre de communautes: {analyse['nb_communautes']}")
    print(f"Modularite: {analyse['modularite']:.4f}")
    for i, comm in enumerate(analyse['communautes']):
        noms = [G.nodes[n]['nom'] for n in comm]
        print(f"  Communaute {i+1}: {', '.join(noms)}")
    print("\nUTILISATEURS LES PLUS INFLUENTS")
    print("-" * 40)
    print("Par degre de connexion:")
    for nom, score in analyse['top_degree']:
        print(f"  - {nom}: {score}")
    print("\nPar centralite d'intermediarite:")
    for nom, score in analyse['top_betweenness']:
        print(f"  - {nom}: {score}")
    print("\n" + "=" * 60)

def visualiser_metriques(G, analyse):
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    ax1 = axes[0, 0]
    degrees = [d for n, d in G.degree()]
    ax1.hist(degrees, bins=range(min(degrees), max(degrees)+2), edgecolor='black', alpha=0.7, color='#3498db')
    ax1.set_xlabel('Degre')
    ax1.set_ylabel('Frequence')
    ax1.set_title('Distribution des Degres')
    ax1.axvline(np.mean(degrees), color='red', linestyle='--', label=f'Moyenne: {np.mean(degrees):.2f}')
    ax1.legend()
    ax2 = axes[0, 1]
    nodes = list(G.nodes())
    noms = [G.nodes[n]['nom'] for n in nodes]
    x = range(len(nodes))
    dc = [analyse['degree_centrality'][n] for n in nodes]
    bc = [analyse['betweenness_centrality'][n] for n in nodes]
    width = 0.35
    ax2.bar([i - width/2 for i in x], dc, width, label='Degre', alpha=0.8)
    ax2.bar([i + width/2 for i in x], bc, width, label='Intermediarite', alpha=0.8)
    ax2.set_xticks(x)
    ax2.set_xticklabels(noms, rotation=45, ha='right', fontsize=7)
    ax2.set_ylabel('Centralite')
    ax2.set_title('Comparaison des Centralites')
    ax2.legend()
    ax3 = axes[1, 0]
    clustering = nx.clustering(G)
    clust_values = [clustering[n] for n in nodes]
    colors = ['#FF6B6B' if G.nodes[n]['groupe'] == 'Etudiants' else '#4ECDC4' if G.nodes[n]['groupe'] == 'Professionnels' else '#FFE66D' for n in nodes]
    ax3.bar(x, clust_values, color=colors, alpha=0.8, edgecolor='black')
    ax3.set_xticks(x)
    ax3.set_xticklabels(noms, rotation=45, ha='right', fontsize=7)
    ax3.set_ylabel('Coefficient de Clustering')
    ax3.set_title('Clustering par Utilisateur')
    ax3.axhline(analyse['clustering_moyen'], color='red', linestyle='--', label=f"Moyenne: {analyse['clustering_moyen']:.2f}")
    ax3.legend()
    ax4 = axes[1, 1]
    pos = nx.spring_layout(G, seed=42)
    couleurs_comm = plt.cm.Set3(np.linspace(0, 1, len(analyse['communautes'])))
    node_colors = []
    for node in G.nodes():
        for i, comm in enumerate(analyse['communautes']):
            if node in comm:
                node_colors.append(couleurs_comm[i])
                break
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=300, alpha=0.8, ax=ax4)
    nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax4)
    labels = {n: G.nodes[n]['nom'] for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=6, ax=ax4)
    ax4.set_title(f"Communautes Detectees ({analyse['nb_communautes']} communautes)")
    ax4.axis('off')
    plt.tight_layout()
    plt.savefig("output/images/analyse_metriques.png", dpi=300, bbox_inches='tight')
    plt.close()
