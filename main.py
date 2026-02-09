import os #pour la gestion des dossiers et fichiers
# Importation des fonctions depuis les modules src/
from src.construction_graphe import creer_reseau_social, sauvegarder_graphe
from src.visualisation import (appliquer_layouts, visualiser_layout_unique, 
                                visualiser_tous_layouts)
from src.reduction_dimension import (appliquer_pca, appliquer_tsne, 
                                     visualiser_reduction_dimension)
from src.analyse import analyser_reseau, afficher_rapport_analyse, visualiser_metriques
from src.visualisation_3d import visualisation_3d

def main():
    
    # Création des dossiers de sortie
    os.makedirs("output/images", exist_ok=True) # Pour sauvegarder les images
    os.makedirs("data", exist_ok=True) # Pour sauvegarder le graphe

    
    print("PROJET: Visualisation des Relations dans un Mini Reseau Social")
    print("=" * 70)
    
    print("\nEtape 1: Construction du graphe...")
    G = creer_reseau_social()
    sauvegarder_graphe(G)
    print(f"   Graphe cree: {G.number_of_nodes()} noeuds, {G.number_of_edges()} aretes")
    
    print("\nEtape 2: Application des techniques de layout...")
    layouts = appliquer_layouts(G)
    print(f"   {len(layouts)} layouts generes")
    
    for nom, pos in layouts.items():
        visualiser_layout_unique(G, pos, f"Layout {nom.title()}", f"layout_{nom}")
    
    visualiser_tous_layouts(G, layouts)
    
    print("\nEtape 3: Reduction de dimension (PCA & t-SNE)...")
    pos_pca, variance_pca = appliquer_pca(G)
    pos_tsne = appliquer_tsne(G)
    visualiser_reduction_dimension(G, pos_pca, pos_tsne, variance_pca)
    print(f"   Variance expliquee par PCA: {sum(variance_pca)*100:.1f}%")
    
    print("\nEtape 4: Analyse des patterns du reseau...")
    analyse = analyser_reseau(G)
    afficher_rapport_analyse(analyse, G)
    visualiser_metriques(G, analyse)
    
    print("\nEtape 5: Creation de la visualisation 3D...")
    visualisation_3d(G)
    print("   Visualisation 3D sauvegardee (reseau_3d.html)")
    
    print("\n" + "=" * 70)
    print("Projet termine! Toutes les images sont dans output/images/")
    print("=" * 70)

if __name__ == "__main__":
    main()