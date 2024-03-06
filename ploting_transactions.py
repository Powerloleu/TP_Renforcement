import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from mdp import run as run_mdp
"""
Draw up to 10 couples states-actions in the same figure
"""

def plot_transactions(printer):
    G = nx.DiGraph()
    subgraphs = []

    for _, row in printer.transactions_prob.iterrows():
        origin = row['Origin']
        action = row['Action']
        
        subgraph = G.copy()    
        for target in printer.declared_states:
            weight = row[target]
            if weight > 0:
                subgraph.add_edge(origin, target, weight=round(weight, 2))

        subgraphs.append((subgraph, origin, action))

    plt.figure(figsize=(10, 20))
    subgraphs = subgraphs[:min(10, len(subgraphs))] 
    for i, (subgraph, origin, action) in enumerate(subgraphs, start=1):
        plt.subplot(len(subgraphs)//2+1, 2, i, frame_on=True)  # Add border around the subplot
        pos = nx.spring_layout(subgraph)
        nx.draw(subgraph, pos, with_labels=True, 
                font_weight='bold', node_size=500, 
                node_color="skyblue", edge_color='black', 
                linewidths=0.5)
        edge_labels = {(i, j): f"(p = {d['weight']})" for i, j, d in subgraph.edges(data=True)}
        nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels)
        plt.title(f"State {origin}, action {action}")

    plt.tight_layout(pad=5.0)
    plt.show()

def main():
    printer = run_mdp(path="prof_examples//fichier3-mdp.mdp", return_printer=True)
    plot_transactions(printer)

if __name__=="__main__":
    main()