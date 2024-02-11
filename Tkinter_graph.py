from matplotlib.patches import FancyArrowPatch
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mdp import run as run_mdp

# data = {
#     "Origin": ["S0", "S1", "S1", "S2"],
#     "Action": ["NA", "a", "b", "NA"],
#     "S0": [0.1, 0.2, 0.4, 0.3],
#     "S1": [0.5, 0.3, 0.4, 0.3],
#     "S2": [0.4, 0.5, 0.2, 0.4]
# }

'''# Estados e ações disponíveis
estados = ["S6", "S1", "S2", "S3", "S4", "S5"]
acoes = ["NA", "a", "b", "c"]

# Criando o DataFrame com estados como colunas e uma coluna adicional para ações
df = pd.DataFrame(columns=["Origin", "Action"] + estados)

# Adicionando as linhas ao DataFrame
for estado_origem in estados:
    # Decidindo aleatoriamente as ações disponíveis para cada estado, exceto S0
    # Garantindo que pelo menos uma ação seja selecionada e sem repetição
    acoes_disponiveis = np.random.choice(acoes[1:], np.random.randint(1, 4), replace=False).tolist()

    for acao in acoes_disponiveis:
        # Gerando probabilidades aleatórias para cada estado de chegada
        probabilidades = np.random.dirichlet(np.ones(len(estados)), size=1)[0]
        # Adicionando estado de origem, ação e probabilidades ao DataFrame
        linha = [estado_origem, acao] + probabilidades.tolist()
        df.loc[len(df)] = linha

# Ajustando o index para melhor visualização
df.reset_index(drop=True, inplace=True)
'''


# Puxando df do mdp
printer = run_mdp(path = "mdp_graph.mdp", return_printer=True)
df = printer.transactions_prob


class RandomWalkApp(tk.Tk):
    def __init__(self, df):
        super().__init__()
        self.title("Random Walk Visualization")
        self.geometry("800x600")

        self.df = df  # O DataFrame deve ser passado como argumento

        # Determina o estado inicial como o menor 'S' se 'S0' não existir
        # TODO Lembrar de alterar essa parte para algo mais robusto, e se o estado virar "state0"? 
        if "S0" not in printer.declared_states:
            # Extrai os números dos estados, assume que o formato é sempre 'S' seguido por um número
            state_numbers = [int(s[1:]) for s in printer.declared_states if s.startswith('S')]
            min_state_number = min(state_numbers)
            self.current_state = f"S{min_state_number}"
        else:
            self.current_state = "S0"
            

        self.path = [self.current_state]
        self.total_probability = 1.0
        self.transition_count = 0
        
        self.create_widgets()
        self.create_graph()

        # Inicializa a aplicação com as ações disponíveis para o estado inicial
        self.initialize_actions()

    def create_widgets(self):
        self.current_state_label = tk.Label(self, text=f"Current State: {self.current_state}")
        self.current_state_label.pack(pady=10)
        
        self.path_label = tk.Label(self, text=f"Path: {self.current_state}")
        self.path_label.pack(pady=10)

        self.action_buttons_frame = tk.Frame(self)
        self.action_buttons_frame.pack(pady=20)
        
        self.start_button = tk.Button(self, text="Start Random Walk", command=self.start_random_walk)
        self.start_button.pack(pady=10)
        
        self.quit_button = tk.Button(self, text="Quit", command=self.destroy)
        self.quit_button.pack(pady=10)

    def create_graph(self):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.figure.add_subplot(111)
        self.plot.axis('off')  # Esconda os eixos para focar nos estados
        
        self.canvas = FigureCanvasTkAgg(self.figure, self)  # Crie um canvas de matplotlib no Tkinter
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.update_graph()
    
    def draw_arrow(self, start_pos, end_pos, radius=0.05):
        """
        Desenha uma seta do start_pos ao limite externo do círculo em end_pos,
        considerando o raio do círculo.
        """
        # Calcula a direção da seta
        direction = np.array(end_pos) - np.array(start_pos)
        norm = np.linalg.norm(direction)

        if norm == 0:
            return

        direction = direction / norm

        # Ajusta o ponto final para terminar no contorno do círculo, não no centro
        adjusted_start_pos = np.array(start_pos) + direction * radius
        adjusted_end_pos = np.array(end_pos) - direction * radius

        # Cria e adiciona a seta ao plot
        arrow = FancyArrowPatch(adjusted_start_pos, adjusted_end_pos, arrowstyle='->', color='k', mutation_scale=20, linewidth=2)
        self.plot.add_patch(arrow)

    def update_graph(self):
        self.plot.clear()
        self.plot.axis('off')

        radius = 0.2  # Valor ajustado do raio de distancia do centro às bolinhas dos estados.
        circle_radius = 0.06 # raio de cada bolinha.

        num_states = len(self.df['Origin'].unique())
        angles = np.linspace(0, 2 * np.pi, num_states, endpoint=False)
        state_positions = {f"S{i}": (radius * np.cos(ang), radius * np.sin(ang)) for i, ang in enumerate(angles)}

        for state, pos in state_positions.items():
            self.plot.scatter(*pos, s=1000, label=state if state == self.current_state else "")
            self.plot.text(pos[0], pos[1], state, horizontalalignment='center', verticalalignment='center')

        # Desenhar apenas a última seta de transição
        if len(self.path) > 1:
            # Pegue os dois últimos estados no caminho para desenhar a seta
            start_pos = state_positions[self.path[-2]]
            end_pos = state_positions[self.path[-1]]
            
            # Desenhe a seta da última transição
            self.draw_arrow(start_pos, end_pos, circle_radius)


        # Ou defina os limites manualmente para centralizar melhor os estados
        self.plot.set_xlim(-0.3, 0.3)
        self.plot.set_ylim(-0.3, 0.3)

        self.canvas.draw()

    def update_action_buttons(self, actions):
        for widget in self.action_buttons_frame.winfo_children():
            widget.destroy()
        
        for action in actions:
            action_button = tk.Button(self.action_buttons_frame, text=f"Action: {action}", command=lambda a=action: self.perform_action(a))
            action_button.pack(side=tk.LEFT)

    def start_random_walk(self):
        if len(self.path) > 1:
            self.path = [self.current_state]
            self.total_probability = 1.0
            self.transition_count = 0
        
        self.perform_action()

    def initialize_actions(self):
        # Atualiza os botões de ação com as ações disponíveis para o estado inicial
        available_actions = self.df[self.df['Origin'] == self.current_state]['Action'].unique()
        self.update_action_buttons(available_actions)

    def perform_action(self, action=None):
        if self.transition_count == 0 or action is not None:
            self.action = action

        transitions = self.df[(self.df['Origin'] == self.current_state) & ((self.df['Action'] == self.action) | (self.df['Action'] == 'NA'))]
        

        if transitions.empty:
            messagebox.showinfo("Random Walk", "There are no valid transitions from this state.")
            return

        state_columns = [col for col in self.df.columns if col.startswith('S')]
        probabilities = transitions[state_columns].values.flatten()
        probabilities = probabilities / probabilities.sum()

        next_state_index = np.random.choice(len(state_columns), p=probabilities)
        next_state = state_columns[next_state_index]

        step_probability = probabilities[next_state_index]

        self.transition_count += 1
        self.current_state = next_state  # Atualiza o estado atual mesmo que seja o mesmo
        self.path.append(self.current_state)  # Adiciona o estado ao caminho mesmo que seja uma repetição
        self.total_probability *= step_probability

        self.update_graph()
        self.update_state_label(step_probability)  # Atualiza o label após cada ação

        available_actions = self.df[self.df['Origin'] == self.current_state]['Action'].unique()
        self.update_action_buttons(available_actions)

    def update_state_label(self, step_probability=None):
        path_info = f"Current State: {self.current_state}\nPath: {' -> '.join(self.path)}"
        if step_probability is not None:
            path_info += f"\nProbability of the last step: {step_probability:.4f}"
        path_info += f"\nTotal Probability: {self.total_probability:.4f}\nTransitions: {self.transition_count}"
        self.path_label.config(text=path_info)
        self.update()  # Força a atualização da UI

# Substitua 'df' com seu DataFrame real
if __name__ == "__main__":
    # Exemplo de DataFrame
    app = RandomWalkApp(df)
    app.mainloop()