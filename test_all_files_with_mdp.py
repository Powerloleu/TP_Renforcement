import os
from mdp import run as run_mdp


folder_path = "prof_examples"  
# Get a list of paths to all files and directories in the specified folder
paths = [os.path.join(folder_path, item) for item in os.listdir(folder_path)]

for path in paths:
    print(f"\n \n _________________Analyzing {path} ______________ \n \n")
    printer = run_mdp(path = path, return_printer=True, print_transactions=True, print_states=True)

