
# IMPORTATION DES BIBLIOTHÈQUES


import numpy as np                          # Manipulation de tableaux numériques
from sklearn.decomposition import PCA       # Algorithme PCA (réduction de dimension)
from sklearn.manifold import TSNE            # Algorithme t-SNE (visualisation)
import networkx as nx                       # Manipulation de graphes
import matplotlib.pyplot as plt             # Visualisation graphique



# CRÉATION DE LA MATRICE DE CARACTÉRISTIQUES DES NŒUDS

def creer_matrice_caracteristiques(G):
    """
    Transforme un graphe NetworkX en une matrice numérique
    où chaque ligne représente un nœud et chaque colonne
    une caractéristique du nœud.
    """

    # Calcul des mesures de centralité pour chaque nœud
    degree_centrality = nx.degree_centrality(G)        # Centralité de degré
    betweenness_centrality = nx.betweenness_centrality(G)  # Centralité d'intermédiarité
    closeness_centrality = nx.closeness_centrality(G)  # Centralité de proximité
    clustering_coef = nx.clustering(G)                 # Coefficient de clustering

    # Liste des nœuds du graphe
    nodes = list(G.nodes())

    # Liste qui contiendra les vecteurs de caractéristiques
    features = []

    # Construction du vecteur de caractéristiques pour chaque nœud
    for node in nodes:
        feature_vector = [
            degree_centrality[node],        # Importance selon le nombre de connexions
            betweenness_centrality[node],   # Rôle de pont dans le graphe
            closeness_centrality[node],     # Proximité avec les autres nœuds
            clustering_coef[node],          # Niveau de regroupement local
            G.degree(node)                  # Nombre réel de connexions
        ]
        features.append(feature_vector)

    # Retourne la matrice des caractéristiques et la liste des nœuds
    return np.array(features), nodes



# APPLICATION DE LA PCA (RÉDUCTION LINÉAIRE)

def appliquer_pca(G, n_components=2):
    """
    Applique la PCA pour réduire la dimension des données du graphe.
    """

    # Création de la matrice de caractéristiques
    features, nodes = creer_matrice_caracteristiques(G)

    # Initialisation de la PCA
    pca = PCA(n_components=n_components)

    # Réduction de dimension (projection en 2D)
    positions_pca = pca.fit_transform(features)

    # Association de chaque nœud à ses coordonnées PCA
    pos = {nodes[i]: positions_pca[i] for i in range(len(nodes))}

    # Pourcentage de variance expliquée par chaque composante
    variance_expliquee = pca.explained_variance_ratio_

    return pos, variance_expliquee



# APPLICATION DU t-SNE (RÉDUCTION NON LINÉAIRE)

def appliquer_tsne(G, n_components=2, perplexity=5):
    """
    Applique t-SNE pour une visualisation basée sur
    la similarité locale entre les nœuds.
    """

    # Création de la matrice de caractéristiques
    features, nodes = creer_matrice_caracteristiques(G)

    # Initialisation de t-SNE
    tsne = TSNE(
        n_components=n_components,   # Dimension finale (2D)
        perplexity=perplexity,       # Taille du voisinage
        random_state=42,              # Résultats reproductibles
        max_iter=1000                 # Nombre d'itérations
    )

    # Réduction de dimension
    positions_tsne = tsne.fit_transform(features)

    # Association de chaque nœud à ses coordonnées t-SNE
    pos = {nodes[i]: positions_tsne[i] for i in range(len(nodes))}

    return pos



# VISUALISATION PCA VS t-SNE

def visualiser_reduction_dimension(G, pos_pca, pos_tsne, variance_pca):
    """
    Affiche le graphe avec deux méthodes de réduction
    de dimension : PCA et t-SNE.
    """

    # Création de deux graphiques côte à côte
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # Définition des couleurs selon les groupes
    couleurs_groupes = {
        'Etudiants': '#FF6B6B',
        'Professionnels': '#4ECDC4',
        'Artistes': '#FFE66D'
    }

    # Attribution d'une couleur à chaque nœud
    node_colors = [
        couleurs_groupes.get(G.nodes[n].get('groupe', 'Inconnu'), '#95A5A6')
        for n in G.nodes()
    ]


    # GRAPHE AVEC PCA

    nx.draw_networkx_nodes(G, pos_pca, node_color=node_colors,
                           node_size=300, alpha=0.8, ax=ax1)

    nx.draw_networkx_edges(G, pos_pca, alpha=0.4,
                           width=1, edge_color='gray', ax=ax1)

    # Labels des nœuds (nom si disponible, sinon ID)
    labels = {n: G.nodes[n].get('nom', str(n)) for n in G.nodes()}
    nx.draw_networkx_labels(G, pos_pca, labels, font_size=7, ax=ax1)

    # Titre avec la variance expliquée
    ax1.set_title(
        f"PCA Layout\nVariance expliquée : {sum(variance_pca)*100:.1f}%",
        fontsize=12
    )
    ax1.axis('off')

    
    # GRAPHE AVEC t-SNE
    
    nx.draw_networkx_nodes(G, pos_tsne, node_color=node_colors,
                           node_size=300, alpha=0.8, ax=ax2)

    nx.draw_networkx_edges(G, pos_tsne, alpha=0.4,
                           width=1, edge_color='gray', ax=ax2)

    nx.draw_networkx_labels(G, pos_tsne, labels, font_size=7, ax=ax2)

    ax2.set_title("t-SNE Layout", fontsize=12)
    ax2.axis('off')

    # Titre général
    plt.suptitle("Réduction de Dimension : PCA vs t-SNE",
                 fontsize=14, fontweight='bold')

    # Ajustement et sauvegarde
    plt.tight_layout()
    plt.savefig("output/images/reduction_dimension.png",
                dpi=300, bbox_inches='tight')
    plt.close()
