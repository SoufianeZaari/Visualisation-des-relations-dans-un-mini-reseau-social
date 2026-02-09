# IMPORTATION DES BIBLIOTHÈQUES
import plotly.graph_objects as go  # Pour les graphiques interactifs 3D
import networkx as nx              # Pour manipuler les graphes
import numpy as np                 # Bibliothèque pour calculs numériques (ici optionnel)


# Fonction : visualisation_3d
# Paramètre :
#   G : Graphe NetworkX représentant le réseau social
# Retour :
#   fig : figure Plotly 3D interactive

def visualisation_3d(G):
    
  
    # Calcul des positions 3D des nœuds
  
    # Utilise l'algorithme "spring_layout" de NetworkX en 3 dimensions
    # Les nœuds liés s’attirent et les autres se repoussent pour éviter le chevauchement
    pos_3d = nx.spring_layout(G, dim=3, seed=42)  # seed pour reproductibilité

    # Préparation des coordonnées des arêtes (liens)
    edge_x, edge_y, edge_z = [], [], []  # Listes pour stocker les coordonnées des arêtes
    for edge in G.edges():
        x0, y0, z0 = pos_3d[edge[0]]  # Coordonnées du premier nœud
        x1, y1, z1 = pos_3d[edge[1]]  # Coordonnées du deuxième nœud
        # On ajoute None pour séparer chaque arête dans Plotly
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])

    # Tracé des arêtes (lignes)
    edge_trace = go.Scatter3d(
        x=edge_x,
        y=edge_y,
        z=edge_z,
        line=dict(width=2, color='#888'),  # Couleur grise pour les liens
        hoverinfo='none',                  # Pas d’infos au survol
        mode='lines'
    )

    # Préparation des coordonnées des nœuds
    node_x = [pos_3d[node][0] for node in G.nodes()]
    node_y = [pos_3d[node][1] for node in G.nodes()]
    node_z = [pos_3d[node][2] for node in G.nodes()]

    # Définition des couleurs selon le groupe
    couleurs_groupes = {
        'Etudiants': '#FF6B6B',       # Rouge
        'Professionnels': '#4ECDC4',  # Bleu/vert
        'Artistes': '#FFE66D'         # Jaune
    }

    # Attribution d'une couleur à chaque nœud selon son groupe
    node_colors = [
        couleurs_groupes.get(G.nodes[n].get('groupe', 'Inconnu'), '#95A5A6') 
        for n in G.nodes()
    ]

    # Préparation du texte au survol des nœuds
    # Affiche nom, groupe et degré (nombre de connexions)
    node_text = [
        f"{G.nodes[n]['nom']}<br>Groupe: {G.nodes[n]['groupe']}<br>Degre: {G.degree(n)}"
        for n in G.nodes()
    ]

    # Tracé des nœuds
    node_trace = go.Scatter3d(
        x=node_x,
        y=node_y,
        z=node_z,
        mode='markers+text',          # Affiche les points et le texte
        hoverinfo='text',             # Affiche les infos au survol
        text=[G.nodes[n]['nom'] for n in G.nodes()],  # Texte des nœuds
        textposition='top center',    # Position du texte
        hovertext=node_text,          # Texte complet au survol
        marker=dict(
            size=10,                  # Taille des nœuds
            color=node_colors,        # Couleur selon le groupe
            line=dict(width=2, color='white')  # Contour blanc
        )
    )

    # Création de la figure Plotly
    fig = go.Figure(data=[edge_trace, node_trace])

    # Mise en forme de la figure
    fig.update_layout(
        title="Visualisation 3D du Reseau Social",  # Titre principal
        showlegend=False,                           # Pas de légende
        scene=dict(                                 # Paramètres des axes 3D
            xaxis=dict(showbackground=False, showticklabels=False, title=''),
            yaxis=dict(showbackground=False, showticklabels=False, title=''),
            zaxis=dict(showbackground=False, showticklabels=False, title=''),
        ),
        margin=dict(l=0, r=0, b=0, t=40),           # Marges
        paper_bgcolor='rgba(0,0,0,0)',              # Fond transparent
        plot_bgcolor='rgba(0,0,0,0)'                # Fond transparent
    )

    # Sauvegarde de la visualisation
    fig.write_html("output/images/reseau_3d.html")  # Fichier HTML interactif

    # Retour de la figure pour affichage ou manipulation ultérieure
    return fig