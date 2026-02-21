# src/mathematiques.py
#
# Ce module implémente les concepts mathématiques fondamentaux
# de la théorie des graphes et de l'algèbre linéaire SANS utiliser
# de bibliothèques de haut niveau comme NetworkX.
#
# L'objectif est de montrer la compréhension mathématique derrière
# les algorithmes utilisés dans ce projet.

import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# 1. REPRÉSENTATION MATRICIELLE DU GRAPHE
# =============================================================================

def construire_matrice_adjacence(G):
    """
    Construit la matrice d'adjacence A du graphe G.

    Définition mathématique :
        A[i][j] = 1  si il existe une arête entre le nœud i et le nœud j
        A[i][j] = 0  sinon

    Pour un graphe non orienté : A est symétrique, i.e. A = A^T

    Propriétés :
        - La somme de la ligne i donne le degré du nœud i : deg(i) = Σ_j A[i][j]
        - Trace(A) = 0 (pas de boucles dans un graphe simple)
        - A^k[i][j] = nombre de chemins de longueur k entre i et j
    """
    nodes = list(G.nodes())
    n = len(nodes)
    node_index = {node: i for i, node in enumerate(nodes)}

    A = np.zeros((n, n), dtype=int)
    for u, v in G.edges():
        i, j = node_index[u], node_index[v]
        A[i][j] = 1
        A[j][i] = 1  # Graphe non orienté => symétrie

    return A, nodes, node_index


def construire_matrice_degre(A):
    """
    Construit la matrice de degré D à partir de la matrice d'adjacence A.

    Définition mathématique :
        D = diag(d_1, d_2, ..., d_n)
        où d_i = Σ_j A[i][j] est le degré du nœud i

    D est une matrice diagonale où chaque élément diagonal
    représente le nombre de connexions du nœud correspondant.
    """
    degrees = np.sum(A, axis=1)
    D = np.diag(degrees)
    return D


def construire_matrice_laplacienne(A, D):
    """
    Construit la matrice Laplacienne L du graphe.

    Définition mathématique :
        L = D - A

    où D est la matrice de degré et A la matrice d'adjacence.

    Propriétés de la matrice Laplacienne :
        1. L est semi-définie positive : toutes ses valeurs propres λ_i ≥ 0
        2. La plus petite valeur propre est toujours 0 : λ_1 = 0
        3. Le nombre de valeurs propres nulles = nombre de composantes connexes
        4. La deuxième plus petite valeur propre λ_2 (connectivité algébrique
           ou valeur de Fiedler) mesure à quel point le graphe est bien connecté
        5. Le vecteur propre associé à λ_2 (vecteur de Fiedler) permet
           de partitionner le graphe en deux communautés

    Forme explicite :
        L[i][j] = deg(i)    si i = j
        L[i][j] = -1        si i ≠ j et (i,j) ∈ E
        L[i][j] = 0         sinon
    """
    L = D - A
    return L


def construire_laplacienne_normalisee(A, D):
    """
    Construit la matrice Laplacienne normalisée L_norm.

    Définition mathématique :
        L_norm = D^{-1/2} · L · D^{-1/2}
               = I - D^{-1/2} · A · D^{-1/2}

    Avantage : les valeurs propres sont bornées dans [0, 2],
    ce qui facilite la comparaison entre graphes de tailles différentes.

    Utilisée dans le layout spectral et le clustering spectral.
    """
    degrees = np.diag(D).astype(float)
    # Éviter la division par zéro
    D_inv_sqrt = np.diag(np.where(degrees > 0, 1.0 / np.sqrt(degrees), 0.0))
    L = D - A
    L_norm = D_inv_sqrt @ L @ D_inv_sqrt
    return L_norm


# =============================================================================
# 2. CALCUL MANUEL DES MESURES DE CENTRALITÉ
# =============================================================================

def calculer_degre_centralite(A):
    """
    Calcule la centralité de degré de chaque nœud.

    Formule mathématique :
        C_D(v) = deg(v) / (n - 1)

    où deg(v) = Σ_j A[v][j] est le degré du nœud v
    et n est le nombre total de nœuds.

    Interprétation : proportion des nœuds auxquels v est directement connecté.
    Valeur dans [0, 1] où 1 signifie connecté à tous les autres nœuds.
    """
    n = A.shape[0]
    degrees = np.sum(A, axis=1)
    centralite = degrees / (n - 1)
    return centralite


def calculer_closeness_centralite(A):
    """
    Calcule la centralité de proximité (closeness) de chaque nœud.

    Formule mathématique :
        C_C(v) = (n - 1) / Σ_{u≠v} d(v, u)

    où d(v, u) est la distance du plus court chemin entre v et u.

    Algorithme utilisé : BFS (Breadth-First Search) pour calculer
    les distances depuis chaque nœud (complexité O(n·(n+m))).

    Interprétation : inverse de la distance moyenne aux autres nœuds.
    Un nœud central peut atteindre tous les autres rapidement.
    """
    n = A.shape[0]
    closeness = np.zeros(n)

    for source in range(n):
        # BFS pour calculer les distances depuis le nœud source
        distances = _bfs_distances(A, source)
        total_dist = np.sum(distances)
        if total_dist > 0:
            closeness[source] = (n - 1) / total_dist
        else:
            closeness[source] = 0.0

    return closeness


def _bfs_distances(A, source):
    """
    Calcule les distances du plus court chemin depuis un nœud source
    vers tous les autres nœuds en utilisant BFS (parcours en largeur).

    Complexité : O(n + m) où n = nœuds, m = arêtes
    """
    n = A.shape[0]
    distances = np.full(n, -1)
    distances[source] = 0
    queue = [source]

    while queue:
        current = queue.pop(0)
        for neighbor in range(n):
            if A[current][neighbor] == 1 and distances[neighbor] == -1:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    # Remplacer les -1 (nœuds non atteignables) par l'infini
    distances = np.where(distances == -1, np.inf, distances)
    return distances


def calculer_betweenness_centralite(A):
    """
    Calcule la centralité d'intermédiarité (betweenness) de chaque nœud.

    Formule mathématique :
        C_B(v) = Σ_{s≠v≠t} σ_{st}(v) / σ_{st}

    où :
        σ_{st}    = nombre total de plus courts chemins entre s et t
        σ_{st}(v) = nombre de ces chemins passant par v

    Normalisation : C_B(v) / ((n-1)(n-2)/2) pour un graphe non orienté.

    Algorithme de Brandes (2001) : complexité O(n·m)

    Interprétation : mesure à quel point un nœud sert de pont
    entre différentes parties du réseau.
    """
    n = A.shape[0]
    betweenness = np.zeros(n)

    for s in range(n):
        # Phase 1 : BFS depuis s pour trouver les plus courts chemins
        stack = []
        predecessors = [[] for _ in range(n)]
        sigma = np.zeros(n)  # nombre de plus courts chemins
        sigma[s] = 1
        dist = np.full(n, -1)
        dist[s] = 0
        queue = [s]

        while queue:
            v = queue.pop(0)
            stack.append(v)
            for w in range(n):
                if A[v][w] == 1:
                    # w trouvé pour la première fois
                    if dist[w] < 0:
                        queue.append(w)
                        dist[w] = dist[v] + 1
                    # Plus court chemin vers w via v ?
                    if dist[w] == dist[v] + 1:
                        sigma[w] += sigma[v]
                        predecessors[w].append(v)

        # Phase 2 : Accumulation (back-propagation)
        delta = np.zeros(n)
        while stack:
            w = stack.pop()
            for v in predecessors[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != s:
                betweenness[w] += delta[w]

    # Normalisation pour graphe non orienté
    norm = (n - 1) * (n - 2)
    if norm > 0:
        betweenness = betweenness / norm

    return betweenness


# =============================================================================
# 3. IMPLÉMENTATION MANUELLE DE LA PCA
# =============================================================================

def pca_manuelle(X, n_components=2):
    """
    Implémentation manuelle de l'Analyse en Composantes Principales (PCA).

    Étapes mathématiques :

    1. CENTRAGE des données :
       X_centré = X - μ
       où μ = (1/n) Σ_i X_i est le vecteur moyen

    2. MATRICE DE COVARIANCE :
       C = (1/(n-1)) · X_centré^T · X_centré
       C[i][j] = Cov(X_i, X_j) = E[(X_i - μ_i)(X_j - μ_j)]

    3. DÉCOMPOSITION EN VALEURS PROPRES :
       C · v_k = λ_k · v_k
       où λ_k sont les valeurs propres (variance expliquée)
       et v_k les vecteurs propres (directions principales)

    4. PROJECTION :
       Y = X_centré · V_k
       où V_k contient les k premiers vecteurs propres
       (ceux associés aux plus grandes valeurs propres)

    Théorème : PCA minimise l'erreur de reconstruction
    et maximise la variance projetée.
    """
    # Étape 1 : Centrage des données
    n_samples = X.shape[0]
    mean = np.mean(X, axis=0)
    X_centered = X - mean

    # Étape 2 : Calcul de la matrice de covariance
    # C = (1/(n-1)) * X^T * X
    cov_matrix = (1 / (n_samples - 1)) * X_centered.T @ X_centered

    # Étape 3 : Décomposition en valeurs propres
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

    # Tri par valeurs propres décroissantes
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]

    # Étape 4 : Sélection des k premières composantes
    V_k = eigenvectors[:, :n_components]
    lambda_k = eigenvalues[:n_components]

    # Projection des données
    X_projected = X_centered @ V_k

    # Variance expliquée par chaque composante
    total_variance = np.sum(eigenvalues)
    variance_ratio = lambda_k / total_variance

    return X_projected, variance_ratio, eigenvalues, eigenvectors


# =============================================================================
# 4. LAYOUT SPECTRAL MANUEL
# =============================================================================

def layout_spectral_manuel(A):
    """
    Calcule le layout spectral d'un graphe manuellement.

    Principe mathématique :
        Utilise les vecteurs propres de la matrice Laplacienne L = D - A
        pour positionner les nœuds en 2D.

        Les coordonnées (x, y) de chaque nœud sont données par
        les composantes des 2ème et 3ème plus petits vecteurs propres
        de L (on ignore le 1er car il correspond à λ_1 = 0).

    Justification :
        Minimise Σ_{(i,j)∈E} ||pos(i) - pos(j)||²
        sous la contrainte que les positions sont orthogonales
        et de norme unitaire.

        C'est un problème de Rayleigh : min x^T L x / x^T x
        dont la solution est le vecteur propre de Fiedler.

    Le vecteur de Fiedler (associé à λ_2) donne la meilleure
    partition bipartie du graphe, et les vecteurs propres suivants
    donnent des raffinements successifs.
    """
    D = construire_matrice_degre(A)
    L = A.astype(float)
    L = D - L

    # Décomposition en valeurs propres de la Laplacienne
    eigenvalues, eigenvectors = np.linalg.eigh(L)

    # Les coordonnées sont les 2ème et 3ème vecteurs propres
    # (le 1er vecteur propre est constant, associé à λ_1 = 0)
    x_coords = eigenvectors[:, 1]  # Vecteur de Fiedler
    y_coords = eigenvectors[:, 2]

    positions = np.column_stack([x_coords, y_coords])
    return positions, eigenvalues, eigenvectors


# =============================================================================
# 5. ALGORITHME DE FORCE (FRUCHTERMAN-REINGOLD) SIMPLIFIÉ
# =============================================================================

def layout_force_manuel(A, iterations=50, k=None, temperature=1.0):
    """
    Implémentation simplifiée de l'algorithme de Fruchterman-Reingold (1991).

    Principe physique :
        Modélise le graphe comme un système de particules avec :
        - Forces d'ATTRACTION entre nœuds connectés (comme des ressorts)
        - Forces de RÉPULSION entre tous les nœuds (comme des charges électriques)

    Formules des forces :
        Force d'attraction :  f_a(d) = d² / k
        Force de répulsion :  f_r(d) = -k² / d

    où d est la distance entre deux nœuds et k est la distance idéale :
        k = C · √(aire / n)

    Algorithme itératif :
        1. Initialiser les positions aléatoirement
        2. Pour chaque itération :
           a. Calculer les forces de répulsion entre toutes les paires
           b. Calculer les forces d'attraction entre nœuds connectés
           c. Mettre à jour les positions : pos += déplacement
           d. Limiter le déplacement par la température
           e. Réduire la température (refroidissement simulé)
    """
    n = A.shape[0]
    np.random.seed(42)

    # Distance idéale entre nœuds
    if k is None:
        k = np.sqrt(1.0 / n)

    # Positions initiales aléatoires
    pos = np.random.rand(n, 2) - 0.5

    t = temperature  # Température initiale

    for iteration in range(iterations):
        displacement = np.zeros((n, 2))

        # Forces de répulsion (entre toutes les paires)
        for i in range(n):
            for j in range(i + 1, n):
                delta = pos[i] - pos[j]
                distance = max(np.linalg.norm(delta), 0.01)
                # f_r(d) = k² / d
                force = (k ** 2) / distance
                direction = delta / distance
                displacement[i] += direction * force
                displacement[j] -= direction * force

        # Forces d'attraction (entre nœuds connectés seulement)
        for i in range(n):
            for j in range(i + 1, n):
                if A[i][j] == 1:
                    delta = pos[i] - pos[j]
                    distance = max(np.linalg.norm(delta), 0.01)
                    # f_a(d) = d² / k
                    force = (distance ** 2) / k
                    direction = delta / distance
                    displacement[i] -= direction * force
                    displacement[j] += direction * force

        # Limiter le déplacement par la température
        for i in range(n):
            disp_norm = np.linalg.norm(displacement[i])
            if disp_norm > 0:
                pos[i] += displacement[i] / disp_norm * min(disp_norm, t)

        # Refroidissement
        t *= 0.95

    return pos


# =============================================================================
# 6. VISUALISATION DES RÉSULTATS MATHÉMATIQUES
# =============================================================================

def visualiser_analyse_mathematique(G, A, nodes, node_index):
    """
    Crée une figure montrant les fondements mathématiques :
    - Matrice d'adjacence
    - Spectre de la matrice Laplacienne
    - Comparaison centralités manuelles vs NetworkX
    - Layout spectral manuel
    """
    import networkx as nx

    fig, axes = plt.subplots(2, 2, figsize=(16, 14))

    # --- 1. Matrice d'adjacence ---
    ax1 = axes[0, 0]
    noms = [G.nodes[n]['nom'] for n in nodes]
    im = ax1.imshow(A, cmap='Blues', interpolation='nearest')
    ax1.set_xticks(range(len(noms)))
    ax1.set_yticks(range(len(noms)))
    ax1.set_xticklabels(noms, rotation=90, fontsize=5)
    ax1.set_yticklabels(noms, fontsize=5)
    ax1.set_title('Matrice d\'Adjacence A', fontsize=12, fontweight='bold')
    plt.colorbar(im, ax=ax1, shrink=0.8)

    # --- 2. Spectre de la Laplacienne ---
    ax2 = axes[0, 1]
    D = construire_matrice_degre(A)
    L = construire_matrice_laplacienne(A, D)
    eigenvalues = np.sort(np.linalg.eigvalsh(L))
    ax2.bar(range(len(eigenvalues)), eigenvalues, color='#3498db', alpha=0.8,
            edgecolor='black')
    ax2.set_xlabel('Index i', fontsize=10)
    ax2.set_ylabel('Valeur propre λᵢ', fontsize=10)
    ax2.set_title('Spectre de la Matrice Laplacienne L = D - A',
                  fontsize=12, fontweight='bold')
    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
    # Annoter λ₂ (connectivité algébrique)
    ax2.annotate(f'λ₂ = {eigenvalues[1]:.3f}\n(Fiedler)',
                 xy=(1, eigenvalues[1]),
                 xytext=(3, eigenvalues[1] + 0.5),
                 arrowprops=dict(arrowstyle='->', color='red'),
                 fontsize=9, color='red')

    # --- 3. Centralités manuelles vs NetworkX ---
    ax3 = axes[1, 0]
    dc_manual = calculer_degre_centralite(A)
    dc_nx = np.array([nx.degree_centrality(G)[n] for n in nodes])
    x = np.arange(len(noms))
    width = 0.35
    ax3.bar(x - width / 2, dc_manual, width, label='Manuel', alpha=0.8,
            color='#e74c3c')
    ax3.bar(x + width / 2, dc_nx, width, label='NetworkX', alpha=0.8,
            color='#2ecc71')
    ax3.set_xticks(x)
    ax3.set_xticklabels(noms, rotation=45, ha='right', fontsize=6)
    ax3.set_ylabel('Centralité de Degré')
    ax3.set_title('Vérification : Centralité Manuelle vs NetworkX',
                  fontsize=12, fontweight='bold')
    ax3.legend()

    # --- 4. Layout spectral manuel ---
    ax4 = axes[1, 1]
    positions, _, _ = layout_spectral_manuel(A)

    couleurs_groupes = {
        'Etudiants': '#FF6B6B',
        'Professionnels': '#4ECDC4',
        'Artistes': '#FFE66D'
    }
    colors = [couleurs_groupes.get(G.nodes[n].get('groupe', ''), '#95A5A6')
              for n in nodes]

    ax4.scatter(positions[:, 0], positions[:, 1], c=colors, s=200,
                edgecolors='black', linewidths=1, zorder=5)

    # Dessiner les arêtes
    for i in range(A.shape[0]):
        for j in range(i + 1, A.shape[0]):
            if A[i][j] == 1:
                ax4.plot([positions[i, 0], positions[j, 0]],
                         [positions[i, 1], positions[j, 1]],
                         'gray', alpha=0.3, linewidth=0.8)

    for i, nom in enumerate(noms):
        ax4.annotate(nom, positions[i], fontsize=6, ha='center', va='bottom')

    ax4.set_title('Layout Spectral Manuel\n(vecteurs propres de L)',
                  fontsize=12, fontweight='bold')
    ax4.set_xlabel('Vecteur propre v₂ (Fiedler)')
    ax4.set_ylabel('Vecteur propre v₃')

    plt.suptitle('Fondements Mathématiques du Projet',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('output/images/analyse_mathematique.png', dpi=300,
                bbox_inches='tight')
    plt.close()
    print("   Analyse mathématique sauvegardée (analyse_mathematique.png)")


def visualiser_pca_manuelle(G, features, nodes):
    """
    Compare la PCA manuelle avec la PCA de scikit-learn et
    montre les étapes mathématiques intermédiaires.
    """
    from sklearn.decomposition import PCA

    fig, axes = plt.subplots(2, 2, figsize=(16, 14))

    noms = [G.nodes[n]['nom'] for n in nodes]
    couleurs_groupes = {
        'Etudiants': '#FF6B6B',
        'Professionnels': '#4ECDC4',
        'Artistes': '#FFE66D'
    }
    colors = [couleurs_groupes.get(G.nodes[n].get('groupe', ''), '#95A5A6')
              for n in nodes]

    # --- 1. Matrice de covariance ---
    ax1 = axes[0, 0]
    X_centered = features - np.mean(features, axis=0)
    cov_matrix = (1 / (features.shape[0] - 1)) * X_centered.T @ X_centered
    feature_names = ['Deg.C', 'Betw.C', 'Close.C', 'Clust.', 'Degré']
    im = ax1.imshow(cov_matrix, cmap='RdBu_r', interpolation='nearest')
    ax1.set_xticks(range(len(feature_names)))
    ax1.set_yticks(range(len(feature_names)))
    ax1.set_xticklabels(feature_names, fontsize=9)
    ax1.set_yticklabels(feature_names, fontsize=9)
    ax1.set_title('Matrice de Covariance C', fontsize=12, fontweight='bold')
    plt.colorbar(im, ax=ax1, shrink=0.8)
    # Annoter les valeurs
    for i in range(cov_matrix.shape[0]):
        for j in range(cov_matrix.shape[1]):
            ax1.text(j, i, f'{cov_matrix[i, j]:.3f}',
                     ha='center', va='center', fontsize=7)

    # --- 2. Valeurs propres (variance expliquée) ---
    ax2 = axes[0, 1]
    projected, variance_ratio, eigenvalues, eigenvectors = pca_manuelle(features)
    eigenvalues_sorted = eigenvalues[eigenvalues > 0]
    cum_variance = np.cumsum(variance_ratio)

    ax2.bar(range(len(variance_ratio)), variance_ratio * 100,
            color='#3498db', alpha=0.8, label='Individuelle')
    all_ratios = eigenvalues / np.sum(eigenvalues)
    cum_all = np.cumsum(all_ratios)
    ax2.plot(range(len(all_ratios)), cum_all * 100,
             'ro-', label='Cumulative')
    ax2.set_xlabel('Composante Principale')
    ax2.set_ylabel('Variance Expliquée (%)')
    ax2.set_title('Décomposition de la Variance (PCA)',
                  fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.set_xticks(range(len(all_ratios)))
    ax2.set_xticklabels([f'PC{i + 1}' for i in range(len(all_ratios))])

    # --- 3. PCA manuelle ---
    ax3 = axes[1, 0]
    ax3.scatter(projected[:, 0], projected[:, 1], c=colors, s=200,
                edgecolors='black', linewidths=1)
    for i, nom in enumerate(noms):
        ax3.annotate(nom, (projected[i, 0], projected[i, 1]),
                     fontsize=6, ha='center', va='bottom')
    ax3.set_xlabel(f'PC1 ({variance_ratio[0] * 100:.1f}%)')
    ax3.set_ylabel(f'PC2 ({variance_ratio[1] * 100:.1f}%)')
    ax3.set_title('PCA Manuelle (implémentation propre)',
                  fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)

    # --- 4. PCA scikit-learn (vérification) ---
    ax4 = axes[1, 1]
    pca_sklearn = PCA(n_components=2)
    projected_sklearn = pca_sklearn.fit_transform(features)
    ax4.scatter(projected_sklearn[:, 0], projected_sklearn[:, 1], c=colors,
                s=200, edgecolors='black', linewidths=1)
    for i, nom in enumerate(noms):
        ax4.annotate(nom, (projected_sklearn[i, 0], projected_sklearn[i, 1]),
                     fontsize=6, ha='center', va='bottom')
    ax4.set_xlabel(f'PC1 ({pca_sklearn.explained_variance_ratio_[0] * 100:.1f}%)')
    ax4.set_ylabel(f'PC2 ({pca_sklearn.explained_variance_ratio_[1] * 100:.1f}%)')
    ax4.set_title('PCA scikit-learn (vérification)',
                  fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)

    plt.suptitle('Analyse en Composantes Principales : Étapes Mathématiques',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('output/images/pca_mathematique.png', dpi=300,
                bbox_inches='tight')
    plt.close()
    print("   Analyse PCA mathématique sauvegardée (pca_mathematique.png)")


def afficher_rapport_mathematique(G, A, nodes):
    """
    Affiche un rapport détaillé des calculs mathématiques
    effectués manuellement.
    """
    import networkx as nx

    print("\n" + "=" * 70)
    print("RAPPORT MATHÉMATIQUE - CALCULS MANUELS")
    print("=" * 70)

    # Matrices
    D = construire_matrice_degre(A)
    L = construire_matrice_laplacienne(A, D)
    n = A.shape[0]

    print(f"\n1. MATRICE D'ADJACENCE A ({n}×{n})")
    print(f"   - Symétrique : {np.allclose(A, A.T)}")
    print(f"   - Trace(A) = {np.trace(A)} (pas de boucles)")
    print(f"   - Somme(A) = {np.sum(A)} (= 2 × nombre d'arêtes = {2 * G.number_of_edges()})")

    print(f"\n2. MATRICE LAPLACIENNE L = D - A")
    eigenvalues = np.sort(np.linalg.eigvalsh(L))
    print(f"   - Valeurs propres : {', '.join([f'{v:.3f}' for v in eigenvalues[:5]])}...")
    print(f"   - λ₁ = {eigenvalues[0]:.6f} (≈ 0, car graphe connexe)")
    print(f"   - λ₂ = {eigenvalues[1]:.6f} (connectivité algébrique de Fiedler)")
    print(f"   - λ_max = {eigenvalues[-1]:.6f}")

    print(f"\n3. CENTRALITÉS (calcul manuel)")
    dc = calculer_degre_centralite(A)
    cc = calculer_closeness_centralite(A)
    bc = calculer_betweenness_centralite(A)

    noms = [G.nodes[n_id]['nom'] for n_id in nodes]

    # Vérification avec NetworkX
    dc_nx = [nx.degree_centrality(G)[n_id] for n_id in nodes]
    cc_nx = [nx.closeness_centrality(G)[n_id] for n_id in nodes]
    bc_nx = [nx.betweenness_centrality(G)[n_id] for n_id in nodes]

    print(f"\n   Centralité de degré C_D(v) = deg(v)/(n-1) :")
    top5 = sorted(range(n), key=lambda i: dc[i], reverse=True)[:5]
    for i in top5:
        match = "✓" if abs(dc[i] - dc_nx[i]) < 1e-6 else "✗"
        print(f"     {noms[i]:10s}: {dc[i]:.4f}  (NetworkX: {dc_nx[i]:.4f}) {match}")

    print(f"\n   Centralité de proximité C_C(v) = (n-1)/Σd(v,u) :")
    top5 = sorted(range(n), key=lambda i: cc[i], reverse=True)[:5]
    for i in top5:
        match = "✓" if abs(cc[i] - cc_nx[i]) < 1e-6 else "✗"
        print(f"     {noms[i]:10s}: {cc[i]:.4f}  (NetworkX: {cc_nx[i]:.4f}) {match}")

    print(f"\n   Centralité d'intermédiarité C_B(v) = Σ σ_st(v)/σ_st :")
    top5 = sorted(range(n), key=lambda i: bc[i], reverse=True)[:5]
    for i in top5:
        match = "✓" if abs(bc[i] - bc_nx[i]) < 1e-3 else "≈"
        print(f"     {noms[i]:10s}: {bc[i]:.4f}  (NetworkX: {bc_nx[i]:.4f}) {match}")

    print("\n" + "=" * 70)
