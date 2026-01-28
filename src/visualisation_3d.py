# src/visualisation_3d.py

import plotly.graph_objects as go
import networkx as nx
import numpy as np

def visualisation_3d(G):
    pos_3d = nx.spring_layout(G, dim=3, seed=42)
    edge_x, edge_y, edge_z = [], [], []
    for edge in G.edges():
        x0, y0, z0 = pos_3d[edge[0]]
        x1, y1, z1 = pos_3d[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])
    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    node_x = [pos_3d[node][0] for node in G.nodes()]
    node_y = [pos_3d[node][1] for node in G.nodes()]
    node_z = [pos_3d[node][2] for node in G.nodes()]
    couleurs_groupes = {
        'Etudiants': '#FF6B6B',
        'Professionnels': '#4ECDC4',
        'Artistes': '#FFE66D'
    }
    node_colors = [couleurs_groupes.get(G.nodes[n].get('groupe', 'Inconnu'), '#95A5A6') for n in G.nodes()]
    node_text = [f"{G.nodes[n]['nom']}<br>Groupe: {G.nodes[n]['groupe']}<br>Degre: {G.degree(n)}" for n in G.nodes()]
    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers+text',
        hoverinfo='text',
        text=[G.nodes[n]['nom'] for n in G.nodes()],
        textposition='top center',
        hovertext=node_text,
        marker=dict(
            size=10,
            color=node_colors,
            line=dict(width=2, color='white')
        )
    )
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Visualisation 3D du Reseau Social",
        showlegend=False,
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, title=''),
            yaxis=dict(showbackground=False, showticklabels=False, title=''),
            zaxis=dict(showbackground=False, showticklabels=False, title=''),
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.write_html("output/images/reseau_3d.html")
    return fig
