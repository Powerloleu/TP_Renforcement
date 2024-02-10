import pandas as pd
from graphviz import Digraph
import numpy as np
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

data = {
    "Origin": ["S0", "S1", "S1", "S2"],
    "Action": ["NA", "a", "b", "NA"],
    "S0": [0.1, 0.2, 0.4, 0.3],
    "S1": [0.5, 0.3, 0.4, 0.3],
    "S2": [0.4, 0.5, 0.2, 0.4]
}

# Creating the DataFrame
df = pd.DataFrame(data)

def random_walk_interactive_with_prob(df, start_state="S0", action=None):
    current_state = start_state
    path = [current_state]
    total_probability = 1.0  # Initializes the total probability as 1 (100%)
    transition_count = 0  # Initializes the count of transitions

    while True:
        print(f"Current state: {current_state}")
        available_actions = df[df['Origin'] == current_state]['Action'].unique()
        
        # Automatically choose "NA" if it's the only action available
        if len(available_actions) == 1 and "NA" in available_actions:
            action = "NA"
        elif action is None:
            action_query = f"If the next state asks for an action, which one will you choose? ({', '.join(available_actions)})"
            action = input(action_query + ": ")

        transitions = df[(df['Origin'] == current_state) & ((df['Action'] == action) | (df['Action'] == "NA"))]

        if transitions.empty:
            print("There are no valid transitions from this state.")
            break

        state_columns = [col for col in df.columns if col.startswith('S')]
        probabilities = transitions[state_columns].values.flatten()
        probabilities = probabilities / probabilities.sum()  # Normalizes the probabilities
        
        next_state_index = np.random.choice(len(state_columns), p=probabilities)
        next_state = state_columns[next_state_index]
        step_probability = probabilities[next_state_index]

        transition_count += 1  # Increment the transition count
        print(f"Transitioning from state {current_state} to {next_state} with a probability of {step_probability:.2f}.")
        print(f"Number of transitions so far: {transition_count}")  # Print the number of transitions
        current_state = next_state
        path.append(current_state)
        
        total_probability *= step_probability
        print(f"Path so far: {' -> '.join(path)}")
        print(f"Total accumulated path probability: {total_probability:.4f}")

        continue_random_walk = input("Do you wish to continue the random walk? (y/n): ")
        print('-'*50 + "//" + "-"*50)
        
        if continue_random_walk.lower() != 'y':
            break
        else:
            # Reset action to None if user chooses to continue, allowing new action choice on next iteration
            action = None

    return path, total_probability

# Example of running the function without a predefined action
# random_walk_interactive_with_prob(df, "S0")

class RandomWalkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Random Walk Visualization")
        self.geometry("800x600")  # Aumentando o tamanho para acomodar novos elementos
        
        self.df = df
        self.current_state = "S0"
        self.path = [self.current_state]
        self.total_probability = 1.0
        self.transition_count = 0
        self.create_widgets()
    
    def create_widgets(self):
        self.current_state_label = tk.Label(self, text=f"Current State: {self.current_state}")
        self.current_state_label.pack(pady=10)
        
        self.path_label = tk.Label(self, text="Path: S0")
        self.path_label.pack(pady=10)

        self.action_buttons_frame = tk.Frame(self)
        self.action_buttons_frame.pack(pady=20)
        
        # Botão para iniciar o passeio aleatório
        self.start_button = tk.Button(self, text="Start Random Walk", command=self.start_random_walk)
        self.start_button.pack(pady=10)
        
        # Botão para sair do aplicativo
        self.quit_button = tk.Button(self, text="Quit", command=self.destroy)
        self.quit_button.pack(pady=10)

    def update_action_buttons(self, actions):
        # Limpa os botões de ação anteriores
        for widget in self.action_buttons_frame.winfo_children():
            widget.destroy()
        
        # Cria um botão para cada ação disponível
        for action in actions:
            action_button = tk.Button(self.action_buttons_frame, text=f"Action: {action}", command=lambda a=action: self.perform_action(a))
            action_button.pack(side=tk.LEFT)

    def start_random_walk(self):
        # Resetar o estado se já tiver começado
        if len(self.path) > 1:
            self.path = [self.current_state]
            self.total_probability = 1.0
            self.transition_count = 0
            self.update_state_label()
        
        # Obter ações disponíveis para o estado atual
        self.perform_action()

    def perform_action(self, action=None):
        if self.transition_count == 0 or action is not None:
            self.action = action

        # Encontrar transições válidas para o estado atual e ação selecionada
        transitions = self.df[(self.df['Origin'] == self.current_state) & ((self.df['Action'] == self.action) | (self.df['Action'] == 'NA'))]

        if transitions.empty:
            messagebox.showinfo("Random Walk", "There are no valid transitions from this state.")
            return

        state_columns = [col for col in self.df.columns if col.startswith('S')]
        probabilities = transitions[state_columns].values.flatten()
        probabilities = probabilities / probabilities.sum()  # Normalizando as probabilidades

        next_state_index = np.random.choice(len(state_columns), p=probabilities)
        next_state = state_columns[next_state_index]  # Mantenha os identificadores de estado conforme estão no DataFrame

        step_probability = probabilities[next_state_index]

        self.transition_count += 1
        self.current_state = next_state  # Atualize diretamente sem remover 'S'
        self.path.append(self.current_state)
        self.total_probability *= step_probability

        # Atualizar a interface gráfica
        self.update_state_label(step_probability)

        # Determinar as ações disponíveis no novo estado
        available_actions = self.df[self.df['Origin'] == self.current_state]['Action'].unique()

        # Atualizar botões de ação para as ações disponíveis, sem invocar automaticamente para "NA"
        self.update_action_buttons(available_actions)

    def update_state_label(self, step_probability=None):
        # Atualizando o label do estado atual e adicionando informações adicionais
        path_info = f"Current State: {self.current_state}\nPath: {' -> '.join(self.path)}"
        if step_probability is not None:
            path_info += f"\nProbability of the last step: {step_probability:.4f}"
        path_info += f"\nTotal Probability: {self.total_probability:.4f}\nTransitions: {self.transition_count}"
        self.path_label.config(text=path_info)


if __name__ == "__main__":
    app = RandomWalkApp()
    app.mainloop()