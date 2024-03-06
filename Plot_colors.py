from mdp import run as run_mdp
import pandas as pd
from graphviz import Digraph
import numpy as np
import random

printer = run_mdp(path = "mdp_examples//Teste_grande_v1.mdp", return_printer=True, print_transactions=True)

df = printer.transactions_prob

# Inicializa o objeto Graphviz para o gráfico direcionado
dot = Digraph(comment='MDP', format='png')

# Configurações do gráfico
dot.attr(size='50,50')
dot.attr('node', shape='circle', width='1', height='1', fontsize='12')
dot.attr('edge', fontsize='10', style='solid')

# Definindo um conjunto de cores para usar nas arestas
colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']

# Mapeamento de ações para cores
action_colors = {}
actions = df['Action'].unique()
for i, action in enumerate(actions):
    action_colors[action] = colors[i % len(colors)]  # Reutiliza cores se houver mais ações do que cores disponíveis

# Adiciona os nós (estados)
unique_states = set(df['Origin'].unique()).union(df.columns[3:])
for state in unique_states:
    dot.node(state, state)

# Adiciona as arestas (transições)
for index, row in df.iterrows():
    origin = row['Origin']
    action = row['Action']
    color = action_colors[action]  # Obtém a cor da ação
    for destination in df.columns[2:]:  # Ajuste para começar da 4ª coluna, incluindo todos os estados de destino
        probability = row[destination]
        if probability > 0:  # Apenas cria arestas para probabilidades maiores que 0
            label = f"{action}, {probability:.2f}"
            dot.edge(origin, destination, label=label, color=color)

# Renderiza e visualiza o gráfico
dot.render('mdp_graph_colored', view=True)