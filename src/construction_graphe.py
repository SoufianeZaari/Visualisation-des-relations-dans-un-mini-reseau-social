# src/construction_graphe.py

import networkx as nx
import random
import pandas as pd

def creer_reseau_social():
    G = nx.Graph()
    utilisateurs = [
        {"id": 1, "nom": "Alice", "age": 25, "groupe": "Etudiants"},
        {"id": 2, "nom": "Bob", "age": 30, "groupe": "Professionnels"},
        {"id": 3, "nom": "Charlie", "age": 22, "groupe": "Etudiants"},
        {"id": 4, "nom": "Diana", "age": 28, "groupe": "Professionnels"},
        {"id": 5, "nom": "Eve", "age": 24, "groupe": "Etudiants"},
        {"id": 6, "nom": "Frank", "age": 35, "groupe": "Professionnels"},
        {"id": 7, "nom": "Grace", "age": 21, "groupe": "Etudiants"},
        {"id": 8, "nom": "Henry", "age": 27, "groupe": "Professionnels"},
        {"id": 9, "nom": "Ivy", "age": 23, "groupe": "Etudiants"},
        {"id": 10, "nom": "Jack", "age": 32, "groupe": "Professionnels"},
        {"id": 11, "nom": "Kate", "age": 26, "groupe": "Artistes"},
        {"id": 12, "nom": "Leo", "age": 29, "groupe": "Artistes"},
        {"id": 13, "nom": "Mia", "age": 24, "groupe": "Etudiants"},
        {"id": 14, "nom": "Nathan", "age": 31, "groupe": "Professionnels"},
        {"id": 15, "nom": "Olivia", "age": 22, "groupe": "Etudiants"},
        {"id": 16, "nom": "Paul", "age": 28, "groupe": "Artistes"},
        {"id": 17, "nom": "Quinn", "age": 25, "groupe": "Etudiants"},
        {"id": 18, "nom": "Rachel", "age": 33, "groupe": "Professionnels"},
        {"id": 19, "nom": "Sam", "age": 27, "groupe": "Artistes"},
        {"id": 20, "nom": "Tina", "age": 23, "groupe": "Etudiants"},
        {"id": 21, "nom": "Uma", "age": 30, "groupe": "Professionnels"},
        {"id": 22, "nom": "Victor", "age": 26, "groupe": "Artistes"},
        {"id": 23, "nom": "Wendy", "age": 24, "groupe": "Etudiants"},
        {"id": 24, "nom": "Xavier", "age": 29, "groupe": "Professionnels"},
        {"id": 25, "nom": "Yara", "age": 25, "groupe": "Artistes"},
    ]
    for user in utilisateurs:
        G.add_node(user["id"], nom=user["nom"], age=user["age"], groupe=user["groupe"])
    relations = [
        (1, 3), (1, 5), (3, 7), (5, 9), (7, 13), (9, 15),
        (13, 17), (15, 20), (17, 23), (1, 20),
        (2, 4), (4, 6), (6, 8), (8, 10), (10, 14),
        (14, 18), (18, 21), (21, 24), (2, 24),
        (11, 12), (12, 16), (16, 19), (19, 22), (22, 25), (11, 25),
        (1, 2), (3, 11), (5, 4), (7, 12), (9, 6),
        (13, 16), (15, 8), (17, 19), (20, 10), (23, 22),
        (1, 11), (2, 12), (4, 16), (6, 19), (8, 22),
    ]
    G.add_edges_from(relations)
    return G

def sauvegarder_graphe(G, chemin="data/reseau_social.csv"):
    edges_data = [(u, v) for u, v in G.edges()]
    df = pd.DataFrame(edges_data, columns=["source", "cible"])
    df.to_csv(chemin, index=False)
    print(f"Graphe sauvegarde dans {chemin}")

def charger_graphe(chemin="data/reseau_social.csv"):
    df = pd.read_csv(chemin)
    G = nx.from_pandas_edgelist(df, "source", "cible")
    return G
