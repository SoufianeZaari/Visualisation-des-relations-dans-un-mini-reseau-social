
# Ce fichier contient des fonctions pour visualiser un graphe
# en utilisant différents layouts (agencement des nœuds)
# et en colorant les nœuds selon leurs groupes.

import networkx as nx           # Bibliothèque pour manipuler des graphes
import matplotlib.pyplot as plt # Bibliothèque pour visualisation graphique
import numpy as np              # Bibliothèque pour calcul numérique (non utilisée ici mais utile)



# Fonction pour créer plusieurs layouts pour un graphe

def appliquer_layouts(G):
    """
    Crée différents agencements (layouts) pour le graphe G.
    Retourne un dictionnaire {nom_layout: positions_des_noeuds}.
    """

    layouts = {}

    # Layout "spring" : positions calculées avec un modèle physique de ressorts
    layouts['spring'] = nx.spring_layout(G, k=2, iterations=50, seed=42)

    # Layout "circular" : positions disposées en cercle
    layouts['circular'] = nx.circular_layout(G)

    # Layout "kamada_kawai" : layout basé sur distances géométriques optimisées
    layouts['kamada_kawai'] = nx.kamada_kawai_layout(G)

    # Préparer le layout "shell" par groupes
    groupes = {}
    for node in G.nodes():
        # Récupère le groupe du nœud ou 'Inconnu' si absent
        groupe = G.nodes[node].get('groupe', 'Inconnu')
        if groupe not in groupes:
            groupes[groupe] = []
        groupes[groupe].append(node)

    # Crée une liste de "couches" pour shell_layout
    shells = list(groupes.values())
    layouts['shell'] = nx.shell_layout(G, nlist=shells)

    # Layout "spectral" : basé sur les valeurs propres de la matrice Laplacienne
    layouts['spectral'] = nx.spectral_layout(G)

    return layouts


# Fonction pour visualiser un layout unique

def visualiser_layout_unique(G, layout, titre, nom_fichier):
    """
    Affiche le graphe G avec un layout donné.
    - layout : positions des nœuds
    - titre : titre du graphique
    - nom_fichier : nom du fichier PNG à sauvegarder
    """

    # Taille de la figure
    plt.figure(figsize=(12, 10))

    # Couleurs attribuées aux différents groupes
    couleurs_groupes = {
        'Etudiants': '#FF6B6B',
        'Professionnels': '#4ECDC4',
        'Artistes': '#FFE66D'
    }

    # Liste des couleurs des nœuds selon leur groupe
    node_colors = [
        couleurs_groupes.get(G.nodes[n].get('groupe', 'Inconnu'), '#95A5A6')
        for n in G.nodes()
    ]

    # Calcul de la taille des nœuds proportionnelle à leur degré
    degrees = dict(G.degree())
    node_sizes = [300 + degrees[n] * 100 for n in G.nodes()]

    # Dessin des nœuds
    nx.draw_networkx_nodes(G, layout, node_color=node_colors,
                           node_size=node_sizes, alpha=0.8)

    # Dessin des arêtes
    nx.draw_networkx_edges(G, layout, alpha=0.5, width=1.5, edge_color='gray')

    # Labels des nœuds (nom si disponible, sinon ID)
    labels = {n: G.nodes[n].get('nom', str(n)) for n in G.nodes()}
    nx.draw_networkx_labels(G, layout, labels, font_size=8, font_weight='bold')

    # Titre du graphique
    plt.title(titre, fontsize=14, fontweight='bold')

    # Masquer les axes
    plt.axis('off')

    # Création d’une légende pour les groupes
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=color, label=groupe) for groupe, color in couleurs_groupes.items()
    ]
    plt.legend(handles=legend_elements, loc='upper left')

    # Ajustement automatique
    plt.tight_layout()

    # Sauvegarde de l’image
    plt.savefig(f"output/images/{nom_fichier}.png", dpi=300, bbox_inches='tight')
    plt.close()



# Fonction pour visualiser tous les layouts

def visualiser_tous_layouts(G, layouts):
    """
    Affiche une figure avec tous les layouts fournis dans un tableau 2x3.
    - layouts : dictionnaire {nom_layout: positions}
    """

    # Création de la figure avec 2 lignes et 3 colonnes
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()  # Transformation en liste pour itérer facilement

    # Couleurs des groupes
    couleurs_groupes = {
        'Etudiants': '#FF6B6B',
        'Professionnels': '#4ECDC4',
        'Artistes': '#FFE66D'
    }

    # Liste des couleurs pour tous les nœuds
    node_colors = [
        couleurs_groupes.get(G.nodes[n].get('groupe', 'Inconnu'), '#95A5A6')
        for n in G.nodes()
    ]

    # Boucle sur tous les layouts
    for idx, (nom, pos) in enumerate(layouts.items()):
        if idx >= 6:  # On affiche seulement 6 layouts maximum
            break
        ax = axes[idx]

        # Dessin des nœuds
        nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                               node_size=200, alpha=0.8, ax=ax)

        # Dessin des arêtes
        nx.draw_networkx_edges(G, pos, alpha=0.4, width=1, edge_color='gray', ax=ax)

        # Titre de chaque subplot
        ax.set_title(f"Layout: {nom.replace('_', ' ').title()}", fontsize=12)

        # Masquer les axes
        ax.axis('off')

    # Si moins de 6 layouts, masquer les axes restants
    if len(layouts) < 6:
        axes[-1].axis('off')

    # Titre général
    plt.suptitle("Comparaison des differentes techniques de Layout",
                 fontsize=16, fontweight='bold')

    # Ajustement automatique
    plt.tight_layout()

    # Sauvegarde de l’image
    plt.savefig("output/images/comparaison_layouts.png", dpi=300, bbox_inches='tight')
    plt.close()
