# RAPPORT DE PROJET
## Visualisation des Relations dans un Mini Réseau Social

---

## 1. Introduction

Ce projet a pour objectif d'explorer et de visualiser les relations au sein d'un mini réseau social simulé. En utilisant des techniques de théorie des graphes, de réduction de dimension et de visualisation, nous cherchons à :

- Comprendre la structure du réseau
- Identifier les utilisateurs les plus influents
- Détecter les communautés naturelles
- Comparer différentes méthodes de visualisation

Les outils utilisés incluent **NetworkX** pour la manipulation des graphes, **Matplotlib** et **Plotly** pour la visualisation, ainsi que **scikit-learn** pour les techniques de réduction de dimension (PCA et t-SNE).

---

## 2. Description du Graphe

### 2.1 Structure du réseau

| Propriété | Valeur |
|-----------|--------|
| Type | Graphe simple non orienté |
| Nombre de nœuds | 25 utilisateurs |
| Nombre d'arêtes | 40 relations d'amitié |
| Densité | 0.1333 |

### 2.2 Les utilisateurs

Le réseau est composé de 25 personnes réparties en 3 groupes sociaux :

**Étudiants (10 personnes)** - Couleur rouge
- Alice (25 ans), Charlie (22 ans), Eve (24 ans), Grace (21 ans), Ivy (23 ans)
- Mia (24 ans), Olivia (22 ans), Quinn (25 ans), Tina (23 ans), Wendy (24 ans)

**Professionnels (9 personnes)** - Couleur cyan
- Bob (30 ans), Diana (28 ans), Frank (35 ans), Henry (27 ans), Jack (32 ans)
- Nathan (31 ans), Rachel (33 ans), Uma (30 ans), Xavier (29 ans)

**Artistes (6 personnes)** - Couleur jaune
- Kate (26 ans), Leo (29 ans), Paul (28 ans), Sam (27 ans), Victor (26 ans), Yara (25 ans)

### 2.3 Les relations

Les connexions sont organisées selon deux types :

1. **Connexions intra-groupe** : Relations au sein d'un même groupe social
2. **Connexions inter-groupes** : Ponts entre différents groupes (ex: Alice↔Bob, Charlie↔Kate)

---

## 3. Méthodes de Visualisation

### 3.1 Techniques de Layout

Nous avons appliqué 5 algorithmes de positionnement différents :

| Layout | Description | Caractéristique |
|--------|-------------|-----------------|
| **Spring (Fruchterman-Reingold)** | Simulation de forces d'attraction/répulsion | Nœuds connectés sont proches |
| **Circular** | Disposition en cercle | Vue d'ensemble symétrique |
| **Kamada-Kawai** | Minimisation de l'énergie du système | Distances proportionnelles |
| **Shell** | Cercles concentriques par groupe | Séparation par catégorie |
| **Spectral** | Basé sur les valeurs propres de la matrice | Structure algébrique |

### 3.2 Réduction de Dimension

#### PCA (Analyse en Composantes Principales)
- Réduit les caractéristiques de chaque nœud de 5 dimensions à 2D
- **Variance expliquée : 99.8%**
- Méthode linéaire, préserve la variance globale

#### t-SNE (t-Distributed Stochastic Neighbor Embedding)
- Réduit également à 2D
- Méthode non-linéaire
- Préserve les structures locales et les voisinages

**Caractéristiques utilisées pour chaque nœud :**
1. Centralité de degré
2. Centralité d'intermédiarité
3. Centralité de proximité
4. Coefficient de clustering
5. Nombre de connexions

### 3.3 Visualisation 3D

Une visualisation 3D interactive a été créée avec Plotly, permettant :
- Rotation et zoom
- Survol pour voir les informations de chaque utilisateur
- Export en fichier HTML autonome

---

## 4. Résultats et Visualisations

### 4.1 Métriques Globales du Réseau

| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| Densité | 0.1333 | Réseau peu dense (13.3% des connexions possibles) |
| Diamètre | 6 | Maximum 6 étapes pour relier deux personnes |
| Rayon | 4 | Au moins 4 étapes depuis le centre |
| Degré moyen | 3.20 | Chaque personne a ~3 amis en moyenne |
| Clustering moyen | 0.0240 | Peu de triangles (amis communs) |
| Clustering global | 0.0309 | Structure peu clusterisée |

### 4.2 Utilisateurs les Plus Influents

**Par centralité de degré** (nombre de connexions) :

| Rang | Nom | Score |
|------|-----|-------|
| 1 | Alice | 0.208 |
| 2 | Bob | 0.167 |
| 3 | Diana | 0.167 |
| 4 | Frank | 0.167 |
| 5 | Henry | 0.167 |

**Par centralité d'intermédiarité** (rôle de pont) :

| Rang | Nom | Score |
|------|-----|-------|
| 1 | Alice | 0.194 |
| 2 | Bob | 0.186 |
| 3 | Henry | 0.163 |
| 4 | Jack | 0.140 |
| 5 | Victor | 0.139 |

### 4.3 Communautés Détectées

L'algorithme de détection de communautés (Greedy Modularity) a identifié **5 communautés** avec une **modularité de 0.3991** :

| Communauté | Membres |
|------------|---------|
| 1 | Paul, Quinn, Sam, Frank, Wendy, Victor, Mia |
| 2 | Alice, Charlie, Grace, Yara, Kate, Leo |
| 3 | Ivy, Bob, Diana, Eve |
| 4 | Henry, Jack, Tina, Olivia |
| 5 | Xavier, Rachel, Uma, Nathan |

### 4.4 Fichiers de Sortie Générés

```
output/images/
├── layout_spring.png          # Layout force-directed
├── layout_circular.png        # Layout circulaire
├── layout_kamada_kawai.png    # Layout Kamada-Kawai
├── layout_shell.png           # Layout en coquilles
├── layout_spectral.png        # Layout spectral
├── comparaison_layouts.png    # Comparaison des 5 layouts
├── reduction_dimension.png    # PCA vs t-SNE
├── analyse_metriques.png      # 4 graphiques d'analyse
└── reseau_3d.html             # Visualisation 3D interactive
```

---

## 5. Analyse

### 5.1 Structure du Réseau

Le réseau présente une **structure décentralisée** avec plusieurs observations clés :

1. **Faible densité (13.3%)** : Le réseau n'est pas saturé de connexions, ce qui est réaliste pour un réseau social où les gens ont un nombre limité d'amis proches.

2. **Diamètre de 6** : Confirme la théorie des "six degrés de séparation" - tout le monde peut être atteint en maximum 6 étapes.

3. **Clustering faible** : Peu de triangles dans le réseau, suggérant que les amis d'une personne ne sont pas nécessairement amis entre eux.

### 5.2 Rôle des Utilisateurs Clés

**Alice** se distingue comme l'utilisateur le plus central :
- Plus haut degré de connexion (5 amis)
- Plus haute intermédiarité (fait le pont entre les groupes)
- Connectée aux trois groupes : Étudiants, Professionnels, et Artistes

**Bob** est le second utilisateur clé :
- Fort rôle d'intermédiarité
- Pont principal entre Professionnels et autres groupes

### 5.3 Communautés vs Groupes Originaux

Les 5 communautés détectées **ne correspondent pas exactement** aux 3 groupes sociaux définis :
- Cela montre que les connexions inter-groupes créent des sous-communautés hybrides
- Par exemple, la communauté 2 mélange Étudiants (Alice, Charlie, Grace) et Artistes (Kate, Leo, Yara)

### 5.4 Comparaison des Layouts

| Layout | Avantage | Inconvénient |
|--------|----------|--------------|
| Spring | Montre les clusters naturels | Peut être chaotique |
| Circular | Vue symétrique claire | Perd l'info de proximité |
| Kamada-Kawai | Distances significatives | Calcul plus lent |
| Shell | Séparation par groupe visible | Rigide |
| Spectral | Base mathématique solide | Moins intuitif |

### 5.5 PCA vs t-SNE

- **PCA** avec 99.8% de variance expliquée montre que 2 dimensions suffisent à représenter la structure
- **t-SNE** révèle mieux les groupements locaux mais peut créer des artefacts

---

## 6. Conclusion

Ce projet a permis de :

1. **Construire et visualiser** un réseau social de 25 utilisateurs avec 40 relations

2. **Comparer 5 techniques de layout** différentes, chacune révélant des aspects différents de la structure

3. **Appliquer des techniques de réduction de dimension** (PCA et t-SNE) pour positionner les nœuds selon leurs caractéristiques

4. **Identifier les utilisateurs centraux** : Alice et Bob sont les plus influents du réseau

5. **Détecter 5 communautés** qui transcendent les groupes sociaux originaux

6. **Créer une visualisation 3D interactive** pour une exploration approfondie

### Points clés à retenir :

- Les réseaux sociaux ne sont pas homogènes : certains individus (comme Alice) jouent un rôle de connecteur crucial
- Les communautés réelles ne suivent pas toujours les catégories sociales prédéfinies
- Différentes visualisations révèlent différents aspects de la même donnée
- La combinaison de métriques quantitatives et de visualisations qualitatives offre une compréhension complète

### Perspectives d'amélioration :

- Ajouter des poids aux arêtes (force de l'amitié)
- Inclure une dimension temporelle (évolution du réseau)
- Tester d'autres algorithmes de détection de communautés
- Ajouter des attributs supplémentaires (intérêts, localisation)

---

## Annexe : Technologies Utilisées

| Outil | Version | Utilisation |
|-------|---------|-------------|
| Python | 3.12 | Langage principal |
| NetworkX | 3.2.1 | Manipulation de graphes |
| Matplotlib | 3.8.2 | Visualisation 2D |
| Plotly | 5.17.0 | Visualisation 3D |
| NumPy | 1.24.3 | Calculs numériques |
| Pandas | 2.1.3 | Manipulation de données |
| scikit-learn | 1.3.2 | PCA et t-SNE |

---

*Rapport généré automatiquement - Projet de Visualisation de Réseau Social*
