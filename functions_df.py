import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox
from mdp import run as run_mdp


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
            # Reset action to None if the user chooses to continue, allowing a new action choice on the next iteration
            action = None

    return path, total_probability

# Example of running the function without a predefined action
# random_walk_interactive_with_prob(df, "S0")

class RandomWalkApp(tk.Tk):
    def __init__(self, df):
        super().__init__()
        self.title("Random Walk Visualization")
        self.geometry("800x600")  # Increasing the size to accommodate new elements
        
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
        
        # Button to start the random walk
        self.start_button = tk.Button(self, text="Start Random Walk", command=self.start_random_walk)
        self.start_button.pack(pady=10)
        
        # Button to quit the application
        self.quit_button = tk.Button(self, text="Quit", command=self.destroy)
        self.quit_button.pack(pady=10)

    def update_action_buttons(self, actions):
        # Clear the previous action buttons
        for widget in self.action_buttons_frame.winfo_children():
            widget.destroy()
        
        # Create a button for each available action
        for action in actions:
            action_button = tk.Button(self.action_buttons_frame, text=f"Action: {action}", command=lambda a=action: self.perform_action(a))
            action_button.pack(side=tk.LEFT)

    def start_random_walk(self):
        # Reset the state if it has already started
        if len(self.path) > 1:
            self.path = [self.current_state]
            self.total_probability = 1.0
            self.transition_count = 0
            self.update_state_label()
        
        # Get available actions for the current state
        self.perform_action()

    def perform_action(self, action=None):
        if self.transition_count == 0 or action is not None:
            self.action = action

        # Find valid transitions for the current state and selected action
        transitions = self.df[(self.df['Origin'] == self.current_state) & ((self.df

['Action'] == self.action) | (self.df['Action'] == 'NA'))]

        if transitions.empty:
            messagebox.showinfo("Random Walk", "There are no valid transitions from this state.")
            return

        state_columns = [col for col in self.df.columns if col.startswith('S')]
        probabilities = transitions[state_columns].values.flatten()
        probabilities = probabilities / probabilities.sum()  # Normalizing probabilities

        next_state_index = np.random.choice(len(state_columns), p=probabilities)
        next_state = state_columns[next_state_index]  # Keep state identifiers as they are in the DataFrame

        step_probability = probabilities[next_state_index]

        self.transition_count += 1
        self.current_state = next_state  # Update directly without removing 'S'
        self.path.append(self.current_state)
        self.total_probability *= step_probability

        # Update the GUI
        self.update_state_label(step_probability)

        # Determine available actions in the new state
        available_actions = self.df[self.df['Origin'] == self.current_state]['Action'].unique()
        self.update_action_buttons(available_actions)

    def update_state_label(self, step_probability=None):
        path_info = f"Current State: {self.current_state}\nPath: {' -> '.join(self.path)}"
        if step_probability is not None:
            path_info += f"\nProbability of the last step: {step_probability:.4f}"
        path_info += f"\nTotal Probability: {self.total_probability:.4f}\nTransitions: {self.transition_count}"
        self.path_label.config(text=path_info)

def main():
    printer = run_mdp(path="correct_ex.mdp", return_printer=True)
    df = printer.transactions_prob
    app = RandomWalkApp(df)
    app.mainloop()

if __name__ == "__main__":
    main()
