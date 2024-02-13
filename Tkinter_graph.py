from matplotlib.patches import FancyArrowPatch, Circle
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mdp import run as run_mdp


class RandomWalkApp(tk.Tk):
    def __init__(self, printer):
        super().__init__()
        self.title("Random Walk Visualization")
        self.geometry("800x600")

        self.df = printer.transactions_prob  

        if "S0" not in printer.declared_states:
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
        self.plot.axis('off') 
        
        self.canvas = FigureCanvasTkAgg(self.figure, self)  
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.update_graph()
    
    def draw_arrow(self, start_pos, end_pos, radius=0.05):
        direction = np.array(end_pos) - np.array(start_pos)
        if np.array_equal(start_pos, end_pos):
            # Draw a circular arrow
            circle = Circle(start_pos, radius, fill=False, color='k', linewidth=2)
            self.plot.add_patch(circle)

        norm = np.linalg.norm(direction)
        
        if norm == 0:
            return

        direction = direction / norm
        adjusted_start_pos = np.array(start_pos) + direction * radius
        adjusted_end_pos = np.array(end_pos) - direction * radius

        arrow = FancyArrowPatch(adjusted_start_pos, 
                                adjusted_end_pos, 
                                arrowstyle='->', 
                                color='k', 
                                mutation_scale=20, 
                                linewidth=2)
        self.plot.add_patch(arrow)

    def update_graph(self):
        self.plot.clear()
        self.plot.axis('off')
        radius = 0.2  
        circle_radius = 0.06 

        num_states = len(self.df['Origin'].unique())
        angles = np.linspace(0, 2 * np.pi, num_states, endpoint=False)
        state_positions = {f"S{i}": (radius * np.cos(ang), radius * np.sin(ang)) for i, ang in enumerate(angles)}

        for state, pos in state_positions.items():
            self.plot.scatter(*pos, s=1000, label=state if state == self.current_state else "")
            self.plot.text(pos[0], pos[1], state, horizontalalignment='center', verticalalignment='center')

        # Draw the last transition
        if len(self.path) > 1:
            start_pos = state_positions[self.path[-2]]
            end_pos = state_positions[self.path[-1]]
            
            self.draw_arrow(start_pos, end_pos, circle_radius)
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

    def initialize_actions(self): # Refresh actions buttons 
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
        self.current_state = next_state  
        self.path.append(self.current_state)  
        self.total_probability *= step_probability

        self.update_graph()
        self.update_state_label(step_probability)  

        available_actions = self.df[self.df['Origin'] == self.current_state]['Action'].unique()
        self.update_action_buttons(available_actions)

    def update_state_label(self, step_probability=None):
        path_info = f"Current State: {self.current_state}\nPath: {' -> '.join(self.path)}"
        if step_probability is not None:
            path_info += f"\nProbability of the last step: {step_probability:.4f}"
        path_info += f"\nTotal Probability: {self.total_probability:.4f}\nTransitions: {self.transition_count}"
        self.path_label.config(text=path_info)
        self.update()  

if __name__ == "__main__":
    printer = run_mdp(path = "correct_ex.mdp", return_printer=True)
    app = RandomWalkApp(printer)
    app.mainloop()
    print(app.path) # We could return it if we wanted